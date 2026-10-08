from datetime import datetime, timezone
from extensions import db
from models.base import PersistenceMixin

class HairHistory(PersistenceMixin, db.Model):
    __tablename__ = 'hair_history'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client_profiles.id'), nullable=False, index=True)
    procedure_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    procedure_date = db.Column(db.Date, nullable=False)
    next_maintenance_date = db.Column(db.Date)
