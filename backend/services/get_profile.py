from services.common import client, profile_dict

class GetProfileService:
    def execute(self, user_id):
        return profile_dict(client(user_id))
