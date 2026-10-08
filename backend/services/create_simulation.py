from models import Simulation
from services.common import client, owned, commit, simulation_values


class CreateSimulationService:
    def execute(self, user_id, data):
        values = simulation_values(data, user_id)
        item = Simulation(**values).salvar()
        return commit(item)
