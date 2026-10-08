from models import Simulation
from services.common import client, owned, commit, simulation_values


class UpdateSimulationService:
    def execute(self, user_id, item_id, data):
        item = owned(Simulation, item_id, user_id)
        merged = {**item.to_dict(), **data}
        item.atualizar(**simulation_values(merged, user_id))
        return commit(item)
