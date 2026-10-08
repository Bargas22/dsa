from models import HairHistory
from services.common import client, owned, commit, history_values


class UpdateHistoryService:
    def execute(self, user_id, item_id, data):
        item = owned(HairHistory, item_id, user_id)
        merged = {**item.to_dict(), **data}
        item.atualizar(**history_values(merged))
        return commit(item)
