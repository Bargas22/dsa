from models import FacialAnalysis
from services.common import client, owned, commit, analysis_values


class GetAnalysisService:
    def execute(self, user_id, item_id):
        return owned(FacialAnalysis, item_id, user_id).to_dict()
