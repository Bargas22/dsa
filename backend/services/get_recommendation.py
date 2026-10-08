from models import Recommendation
from services.common import owned

class GetRecommendationService:
    def execute(self, user_id, item_id):
        return owned(Recommendation, item_id, user_id).to_dict()
