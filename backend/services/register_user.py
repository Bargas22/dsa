import re
from werkzeug.security import generate_password_hash
from models import User, ClientProfile
from services.common import text, token
from extensions import db
from core.errors import ValidationError, ConflictError

class RegisterUserService:
    def execute(self, data):
        name = text(data.get('name'), 'Nome', 120, True)
        email = text(data.get('email'), 'E-mail', 190, True).lower()
        password = data.get('password')
        if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email) or not isinstance(password, str) or not 8 <= len(password) <= 128:
            raise ValidationError('Informe e-mail válido e senha de 8 a 128 caracteres.')
        if User.query.filter_by(email=email).first():
            raise ConflictError('Este e-mail já está cadastrado.')
        user = User(name=name, email=email, password_hash=generate_password_hash(password)).salvar()
        ClientProfile(user_id=user.id).salvar()
        db.session.commit()
        return {'token': token(user), 'user': user.to_dict()}
