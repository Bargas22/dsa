from services.common import client

class GetPreferencesService:
    def execute(self, user_id):
        item = client(user_id).preference
        return item.to_dict() if item else {}
