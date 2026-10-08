from models import Professional

class ListProfessionalsService:
    def execute(self, user_id):
        return [item.to_dict() for item in Professional.listar_todos()]
