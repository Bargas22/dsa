from datetime import datetime, timezone
from extensions import db
from models.base import PersistenceMixin

class ClientProfile(PersistenceMixin, db.Model):
    __tablename__ = 'client_profiles'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    phone = db.Column(db.String(25))
    birth_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    preference = db.relationship('VisualPreference', backref='client', uselist=False, cascade='all, delete-orphan')
    analyses = db.relationship('FacialAnalysis', backref='client', cascade='all, delete-orphan')
    history = db.relationship('HairHistory', backref='client', cascade='all, delete-orphan')
    appointments = db.relationship('Appointment', backref='client', cascade='all, delete-orphan')
