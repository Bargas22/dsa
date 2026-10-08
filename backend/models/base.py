from datetime import date, datetime
from decimal import Decimal
from extensions import db

class PersistenceMixin:
    """CRUD comum. A transação é concluída pelo caso de uso (Service)."""
    def salvar(self):
        db.session.add(self)
        db.session.flush()
        return self

    def atualizar(self, **values):
        for key, value in values.items():
            setattr(self, key, value)
        return self.salvar()

    def deletar(self):
        db.session.delete(self)
        db.session.flush()

    @classmethod
    def listar_todos(cls, **filters):
        return cls.query.filter_by(**filters).order_by(cls.id.desc()).all()

    @classmethod
    def buscar_por_id(cls, item_id):
        return db.session.get(cls, item_id)

    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            if column.name == 'password_hash':
                continue
            value = getattr(self, column.name)
            if isinstance(value, (date, datetime)):
                value = value.isoformat()
            elif isinstance(value, Decimal):
                value = float(value)
            result[column.name] = value
        return result
