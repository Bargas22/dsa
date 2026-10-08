from datetime import datetime, timezone
from extensions import db
from models.base import PersistenceMixin

class Appointment(PersistenceMixin, db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client_profiles.id'), nullable=False, index=True)
    appointment_date = db.Column(db.DateTime, nullable=False)
    service_name = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(20), default='scheduled', nullable=False)
    notes = db.Column(db.Text)

    def to_dict(self):
        p = self.professional
        return {**super().to_dict(), 'professional_name': p.user.name, 'studio_name': p.studio_name, 'specialty': p.specialty, 'rating': p.rating, 'duration_minutes': p.duration_minutes}
