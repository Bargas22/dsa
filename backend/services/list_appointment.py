from models import Appointment
from services.common import client, owned, commit, appointment_values


class ListAppointmentService:
    def execute(self, user_id):
        return [item.to_dict() for item in Appointment.listar_todos(client_id=client(user_id).id)]
