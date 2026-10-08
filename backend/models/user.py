from datetime import datetime, timezone
from extensions import db
from models.base import PersistenceMixin

class User(PersistenceMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(190), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='client')
    avatar_url = db.Column(db.String(500))
    profile = db.relationship('ClientProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    professional = db.relationship('Professional', backref='user', uselist=False, cascade='all, delete-orphan')
