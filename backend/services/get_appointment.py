from models import Appointment
from services.common import client, owned, commit, appointment_values


class GetAppointmentService:
    def execute(self, user_id, item_id):
        return owned(Appointment, item_id, user_id).to_dict()
