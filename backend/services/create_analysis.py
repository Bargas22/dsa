from models import FacialAnalysis
from services.common import client, owned, commit, analysis_values


class CreateAnalysisService:
    def execute(self, user_id, data):
        values = analysis_values(data)
        item = FacialAnalysis(client_id=client(user_id).id, **values).salvar()
        return commit(item)
