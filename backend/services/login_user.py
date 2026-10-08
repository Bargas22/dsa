from werkzeug.security import check_password_hash
from models import User
from services.common import text, token
from core.errors import UnauthorizedError

class LoginUserService:
    def execute(self, data):
        email = text(data.get('email'), 'E-mail', 190).lower()
        password = data.get('password')
        if not isinstance(password, str) or len(password) > 128:
            raise UnauthorizedError('E-mail ou senha inválidos.')
        user = User.query.filter_by(email=email).first()
        if not user or not user.profile or not check_password_hash(user.password_hash, password):
            raise UnauthorizedError('E-mail ou senha inválidos.')
        return {'token': token(user), 'user': user.to_dict()}
