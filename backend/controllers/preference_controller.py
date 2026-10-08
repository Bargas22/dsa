from flask import Blueprint, g, jsonify, request
from controllers.base import json_body
from middleware.auth_required import auth_required
from services.get_preferences import GetPreferencesService
from services.save_preferences import SavePreferencesService

class PreferenceController:
    @auth_required
    def get_preferences(self):
        result = GetPreferencesService().execute(g.user_id)
        return jsonify(result), 200

    @auth_required
    def save_preferences(self):
        result = SavePreferencesService().execute(g.user_id, json_body())
        return jsonify(result), 200

preference_blueprint = Blueprint('preference', __name__)
controller = PreferenceController()
preference_blueprint.add_url_rule('', view_func=controller.get_preferences, methods=['GET'])
preference_blueprint.add_url_rule('', view_func=controller.save_preferences, methods=['PUT'])
