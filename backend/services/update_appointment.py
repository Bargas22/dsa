from models import Appointment
from services.common import client, owned, commit, appointment_values


class UpdateAppointmentService:
    def execute(self, user_id, item_id, data):
        item = owned(Appointment, item_id, user_id)
        merged = {**item.to_dict(), **data}
        item.atualizar(**appointment_values(merged, current=item))
        return commit(item)
