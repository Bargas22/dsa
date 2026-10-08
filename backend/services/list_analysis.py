from models import FacialAnalysis
from services.common import client, owned, commit, analysis_values


class ListAnalysisService:
    def execute(self, user_id):
        return [item.to_dict() for item in FacialAnalysis.listar_todos(client_id=client(user_id).id)]
