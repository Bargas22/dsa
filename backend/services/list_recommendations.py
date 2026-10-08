from repositories.recommendation_repository import RecommendationRepository
from models import FacialAnalysis
from services.common import client, owned, integer, choice, CATEGORIES

class ListRecommendationsService:
    def execute(self, user_id, analysis_id=None, category=None):
        if analysis_id is not None:
            analysis_id = owned(FacialAnalysis, integer(analysis_id, 'Análise'), user_id).id
        if category:
            choice(category, CATEGORIES, 'Categoria')
        return [item.to_dict() for item in RecommendationRepository.search(client(user_id).id, analysis_id, category)]
