from datetime import datetime, timezone
from extensions import db
from models.base import PersistenceMixin

class Simulation(PersistenceMixin, db.Model):
    __tablename__ = 'simulations'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)
    analysis_id = db.Column(db.Integer, db.ForeignKey('facial_analyses.id'), nullable=False, index=True)
    recommendation_id = db.Column(db.Integer, db.ForeignKey('recommendations.id'))
    before_image_url = db.Column(db.String(500))
    after_image_url = db.Column(db.String(500))
