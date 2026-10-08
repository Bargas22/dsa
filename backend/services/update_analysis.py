from models import FacialAnalysis
from services.common import client, owned, commit, analysis_values


class UpdateAnalysisService:
    def execute(self, user_id, item_id, data):
        item = owned(FacialAnalysis, item_id, user_id)
        merged = {**item.to_dict(), **data}
        item.atualizar(**analysis_values(merged))
        return commit(item)
