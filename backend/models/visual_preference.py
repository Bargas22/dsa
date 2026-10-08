from datetime import datetime, timezone
from extensions import db
from models.base import PersistenceMixin

class VisualPreference(PersistenceMixin, db.Model):
    __tablename__ = 'visual_preferences'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client_profiles.id'), nullable=False, unique=True)
    hair_type = db.Column(db.String(20), nullable=False)
    hair_length = db.Column(db.String(20), nullable=False)
