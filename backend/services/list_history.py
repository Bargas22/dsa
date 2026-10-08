from models import HairHistory
from services.common import client, owned, commit, history_values


class ListHistoryService:
    def execute(self, user_id):
        return [item.to_dict() for item in HairHistory.listar_todos(client_id=client(user_id).id)]
