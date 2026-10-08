from models import Recommendation, FacialAnalysis

class RecommendationRepository:
    """Consulta com junção, filtro opcional e ordenação por compatibilidade."""
    @staticmethod
    def search(client_id, analysis_id=None, category=None):
        query = Recommendation.query.join(FacialAnalysis).filter(FacialAnalysis.client_id == client_id)
        if analysis_id is not None:
            query = query.filter(Recommendation.analysis_id == analysis_id)
        if category:
            query = query.filter(Recommendation.category == category)
        return query.order_by(Recommendation.compatibility.desc(), Recommendation.id).all()
