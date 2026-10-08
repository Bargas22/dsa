from models import FacialAnalysis, Recommendation
from services.common import owned
from services.suggest_styles import SuggestStylesService
from extensions import db

class GenerateRecommendationsService:
    def execute(self, user_id, item_id):
        analysis = owned(FacialAnalysis, item_id, user_id)
        for old in list(analysis.recommendations):
            old.deletar()
        items = [Recommendation(analysis_id=analysis.id, **values).salvar() for values in SuggestStylesService().execute(analysis)]
        db.session.commit()
        return [item.to_dict() for item in items]
