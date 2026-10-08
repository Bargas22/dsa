from models import Simulation
from services.common import client, owned, commit, simulation_values


class ListSimulationService:
    def execute(self, user_id):
        return [item.to_dict() for item in [item for analysis in client(user_id).analyses for item in analysis.simulations]]
