from models import HairHistory
from services.common import client, owned, commit, history_values


class DeleteHistoryService:
    def execute(self, user_id, item_id):
        owned(HairHistory, item_id, user_id).deletar()
        commit()
