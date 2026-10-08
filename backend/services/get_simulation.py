from models import Simulation
from services.common import client, owned, commit, simulation_values


class GetSimulationService:
    def execute(self, user_id, item_id):
        return owned(Simulation, item_id, user_id).to_dict()
