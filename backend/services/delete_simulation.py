from models import Simulation
from services.common import client, owned, commit, simulation_values


class DeleteSimulationService:
    def execute(self, user_id, item_id):
        owned(Simulation, item_id, user_id).deletar()
        commit()
