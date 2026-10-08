from datetime import datetime, timezone
from extensions import db
from models.base import PersistenceMixin

class Recommendation(PersistenceMixin, db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)
    analysis_id = db.Column(db.Integer, db.ForeignKey('facial_analyses.id'), nullable=False, index=True)
    category = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technical_reason = db.Column(db.Text)
    compatibility = db.Column(db.Integer)
    simulations = db.relationship('Simulation', backref='recommendation')
