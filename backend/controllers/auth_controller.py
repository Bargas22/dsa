from flask import Blueprint, g, jsonify, request
from controllers.base import json_body
from middleware.auth_required import auth_required
from services.register_user import RegisterUserService
from services.login_user import LoginUserService

class AuthController:
    def register_user(self):
        result = RegisterUserService().execute(json_body())
        return jsonify(result), 201

    def login_user(self):
        result = LoginUserService().execute(json_body())
        return jsonify(result), 200

auth_blueprint = Blueprint('auth', __name__)
controller = AuthController()
auth_blueprint.add_url_rule('/register', view_func=controller.register_user, methods=['POST'])
auth_blueprint.add_url_rule('/login', view_func=controller.login_user, methods=['POST'])
