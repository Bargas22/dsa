from datetime import date, datetime, timezone
from urllib.parse import urlparse
from flask import current_app
import jwt
from extensions import db
from core.errors import ValidationError, NotFoundError, UnauthorizedError
from models import User, FacialAnalysis, Recommendation, Professional

HAIR_TYPES = {'straight', 'wavy', 'curly', 'coily'}
LENGTHS = {'short', 'medium', 'long'}
CATEGORIES = {'haircut', 'beard', 'coloring', 'care'}

def text(value, label, maximum=2000, required=False):
    if value is None:
        value = ''
    if not isinstance(value, str):
        raise ValidationError(f'{label}: informe um texto.')
    value = value.strip()
    if (required and not value) or len(value) > maximum:
        raise ValidationError(f'{label}: obrigatório e/ou limite de {maximum} caracteres excedido.')
    return value

def choice(value, options, label):
    if not isinstance(value, str) or value not in options:
        raise ValidationError(f'{label} inválido.')
    return value

def integer(value, label):
    if isinstance(value, bool) or not str(value).isdigit():
        raise ValidationError(f'{label} deve ser um inteiro positivo.')
    try:
        result = int(value)
    except (TypeError, ValueError):
        raise ValidationError(f'{label} deve ser um inteiro positivo.')
    if result < 1:
        raise ValidationError(f'{label} deve ser positivo.')
    return result

def iso_date(value, label, optional=False):
    if not value and optional:
        return None
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValidationError(f'{label}: data inválida.')

def url(value):
    value = text(value, 'URL', 500)
    try:
        valid = not value or (urlparse(value).scheme in ('http', 'https') and bool(urlparse(value).netloc))
    except ValueError:
        valid = False
    if not valid:
        raise ValidationError('Informe uma URL http ou https válida.')
    return value or None

def client(user_id):
    user = User.buscar_por_id(user_id)
    if not user or not user.profile:
        raise UnauthorizedError()
    return user.profile

def owned(model, item_id, user_id):
    profile = client(user_id)
    item = model.buscar_por_id(integer(item_id, 'ID'))
    owner_id = None if not item else (item.client_id if hasattr(item, 'client_id') else item.analysis.client_id)
    if not item or owner_id != profile.id:
        raise NotFoundError('Registro não encontrado.')
    return item

def commit(item=None):
    db.session.commit()
    return item.to_dict() if item is not None else None

def profile_dict(profile):
    return {**profile.user.to_dict(), 'client_id': profile.id, 'phone': profile.phone, 'birth_date': profile.birth_date.isoformat() if profile.birth_date else None, 'notes': profile.notes}

def token(user):
    from datetime import timedelta
    return jwt.encode({'sub': str(user.id), 'exp': datetime.now(timezone.utc) + timedelta(hours=8)}, current_app.config['JWT_SECRET'], algorithm='HS256')

def analysis_values(data):
    result = {}
    for key in ('face_shape', 'hair_type', 'hair_texture', 'hair_density', 'current_length'):
        result[key] = text(data.get(key), key, 50)
    choice(result['face_shape'], {'oval', 'round', 'square', 'heart', 'long', 'diamond'}, 'Formato do rosto')
    choice(result['hair_type'], HAIR_TYPES, 'Tipo de cabelo')
    choice(result['current_length'], LENGTHS, 'Comprimento')
    score = data.get('score')
    if score is not None and (isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= 100):
        raise ValidationError('Pontuação deve ser um inteiro de 0 a 100.')
    result.update(score=score, image_url=url(data.get('image_url')), observations=text(data.get('observations'), 'Observações'))
    return result

def history_values(data):
    procedure = iso_date(data.get('procedure_date'), 'Data do procedimento')
    maintenance = iso_date(data.get('next_maintenance_date'), 'Manutenção', True)
    if maintenance and maintenance < procedure:
        raise ValidationError('A manutenção não pode anteceder o procedimento.')
    return dict(procedure_type=text(data.get('procedure_type'), 'Procedimento', 100, True), description=text(data.get('description'), 'Descrição'), image_url=url(data.get('image_url')), procedure_date=procedure, next_maintenance_date=maintenance)

def appointment_values(data, current=None):
    from repositories.appointment_repository import AppointmentRepository
    professional_id = integer(data.get('professional_id'), 'Profissional')
    # Serializa reservas para o mesmo profissional no MySQL.
    professional = Professional.query.filter_by(id=professional_id).with_for_update().first()
    if not professional:
        raise ValidationError('Profissional inválido.')
    try:
        when = datetime.fromisoformat(data.get('appointment_date', '').replace('Z', '+00:00'))
        if when.tzinfo:
            when = when.astimezone(timezone.utc).replace(tzinfo=None)
    except (TypeError, ValueError, AttributeError):
        raise ValidationError('Data e horário inválidos.')
    status = choice(data.get('status', 'scheduled'), {'scheduled', 'completed', 'cancelled'}, 'Status')
    if not current and status != 'scheduled':
        raise ValidationError('Novo agendamento deve estar marcado.')
    if status == 'scheduled':
        if when <= datetime.now(timezone.utc).replace(tzinfo=None):
            raise ValidationError('Escolha uma data futura.')
        if AppointmentRepository.overlaps(professional, when, current.id if current else None):
            from core.errors import ConflictError
            raise ConflictError('Este horário está ocupado.')
    if status == 'completed' and when > datetime.now(timezone.utc).replace(tzinfo=None):
        raise ValidationError('Não é possível concluir um atendimento futuro.')
    return dict(professional_id=professional_id, appointment_date=when, service_name=text(data.get('service_name'), 'Serviço', 150, True), notes=text(data.get('notes'), 'Observações'), status=status)

def simulation_values(data, user_id):
    analysis = owned(FacialAnalysis, data.get('analysis_id'), user_id)
    recommendation_id = data.get('recommendation_id') or None
    if recommendation_id:
        recommendation = owned(Recommendation, recommendation_id, user_id)
        if recommendation.analysis_id != analysis.id:
            raise ValidationError('A recomendação deve pertencer à análise selecionada.')
        recommendation_id = recommendation.id
    return dict(analysis_id=analysis.id, recommendation_id=recommendation_id, before_image_url=url(data.get('before_image_url')), after_image_url=url(data.get('after_image_url')))
