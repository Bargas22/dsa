from datetime import timedelta
from models import Appointment

class AppointmentRepository:
    """Busca conflitos de intervalos para um profissional."""
    @staticmethod
    def overlaps(professional, start, exclude_id=None):
        end = start + timedelta(minutes=professional.duration_minutes)
        query = Appointment.query.filter(Appointment.professional_id == professional.id, Appointment.status == 'scheduled', Appointment.appointment_date < end, Appointment.appointment_date > start - timedelta(minutes=professional.duration_minutes))
        if exclude_id:
            query = query.filter(Appointment.id != exclude_id)
        return query.first() is not None
