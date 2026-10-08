from services.common import client, profile_dict, text, url, iso_date
from extensions import db
from core.errors import ValidationError
from datetime import date

class UpdateProfileService:
    def execute(self, user_id, data):
        profile = client(user_id)
        merged = {**profile_dict(profile), **data}
        birth = iso_date(merged.get('birth_date'), 'Nascimento', True)
        if birth and birth > date.today():
            raise ValidationError('Nascimento não pode estar no futuro.')
        profile.user.atualizar(name=text(merged.get('name'), 'Nome', 120, True), avatar_url=url(merged.get('avatar_url')))
        profile.atualizar(phone=text(merged.get('phone'), 'Telefone', 25), birth_date=birth, notes=text(merged.get('notes'), 'Observações'))
        db.session.commit()
        return profile_dict(profile)
