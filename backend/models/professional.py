from datetime import datetime, timezone
from extensions import db
from models.base import PersistenceMixin

class Professional(PersistenceMixin, db.Model):
    __tablename__ = 'professionals'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    studio_name = db.Column(db.String(140))
    specialty = db.Column(db.String(120))
    rating = db.Column(db.Float, default=5)
    duration_minutes = db.Column(db.Integer, default=60)
    appointments = db.relationship('Appointment', backref='professional')

    def to_dict(self):
        return {**super().to_dict(), 'name': self.user.name, 'avatar_url': self.user.avatar_url}
