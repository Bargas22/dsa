from functools import wraps
import jwt
from flask import request, g, current_app
from core.errors import UnauthorizedError
from models import User

def auth_required(handler):
    @wraps(handler)
    def wrapped(*args, **kwargs):
        header = request.headers.get('Authorization', '')
        if not header.startswith('Bearer '):
            raise UnauthorizedError()
        try:
            payload = jwt.decode(header[7:], current_app.config['JWT_SECRET'], algorithms=['HS256'])
            g.user_id = int(payload['sub'])
        except (jwt.InvalidTokenError, KeyError, ValueError, TypeError):
            raise UnauthorizedError('Token inválido ou expirado.')
        user = User.buscar_por_id(g.user_id)
        if not user or not user.profile:
            raise UnauthorizedError()
        return handler(*args, **kwargs)
    return wrapped
