from models import Appointment
from services.common import client, owned, commit, appointment_values


class CreateAppointmentService:
    def execute(self, user_id, data):
        values = appointment_values(data)
        item = Appointment(client_id=client(user_id).id, **values).salvar()
        return commit(item)
