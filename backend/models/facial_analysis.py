from datetime import datetime, timezone
from extensions import db
from models.base import PersistenceMixin

class FacialAnalysis(PersistenceMixin, db.Model):
    __tablename__ = 'facial_analyses'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client_profiles.id'), nullable=False, index=True)
    face_shape = db.Column(db.String(50))
    hair_type = db.Column(db.String(50))
    hair_texture = db.Column(db.String(50))
    hair_density = db.Column(db.String(50))
    current_length = db.Column(db.String(50))
    image_url = db.Column(db.String(500))
    score = db.Column(db.Integer)
    observations = db.Column(db.Text)
    recommendations = db.relationship('Recommendation', backref='analysis', cascade='all, delete-orphan')
    simulations = db.relationship('Simulation', backref='analysis', cascade='all, delete-orphan')
