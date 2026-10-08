from models import Appointment
from services.common import client, owned, commit, appointment_values


class DeleteAppointmentService:
    def execute(self, user_id, item_id):
        owned(Appointment, item_id, user_id).deletar()
        commit()
