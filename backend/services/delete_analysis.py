from models import FacialAnalysis
from services.common import client, owned, commit, analysis_values


class DeleteAnalysisService:
    def execute(self, user_id, item_id):
        owned(FacialAnalysis, item_id, user_id).deletar()
        commit()
