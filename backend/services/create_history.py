from models import HairHistory
from services.common import client, owned, commit, history_values


class CreateHistoryService:
    def execute(self, user_id, data):
        values = history_values(data)
        item = HairHistory(client_id=client(user_id).id, **values).salvar()
        return commit(item)
