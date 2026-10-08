from services.common import client, choice, HAIR_TYPES, LENGTHS, commit
from models import VisualPreference

class SavePreferencesService:
    def execute(self, user_id, data):
        profile = client(user_id)
        values = dict(hair_type=choice(data.get('hair_type'), HAIR_TYPES, 'Tipo de cabelo'), hair_length=choice(data.get('hair_length'), LENGTHS, 'Comprimento'))
        item = profile.preference or VisualPreference(client_id=profile.id)
        item.atualizar(**values)
        return commit(item)
