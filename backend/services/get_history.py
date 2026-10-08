from models import HairHistory
from services.common import client, owned, commit, history_values


class GetHistoryService:
    def execute(self, user_id, item_id):
        return owned(HairHistory, item_id, user_id).to_dict()
