import os
from pathlib import Path
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from extensions import db
from core.errors import AppError
import models

@event.listens_for(Engine, 'connect')
def sqlite_foreign_keys(connection, _):
    import sqlite3
    if isinstance(connection, sqlite3.Connection):
        connection.execute('PRAGMA foreign_keys=ON')

def create_app(config=None):
    load_dotenv(Path(__file__).with_name('.env'))
    app = Flask(__name__)
    app.config.update(SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///visagio.db'), SQLALCHEMY_TRACK_MODIFICATIONS=False, JWT_SECRET=os.getenv('JWT_SECRET'), MAX_CONTENT_LENGTH=1024 * 1024)
    if config:
        app.config.update(config)
    if not app.config['JWT_SECRET'] or len(app.config['JWT_SECRET']) < 32:
        raise RuntimeError('Defina JWT_SECRET com pelo menos 32 caracteres no backend/.env.')
    db.init_app(app)
    origins = os.getenv('CORS_ORIGINS', 'http://localhost:5000,http://127.0.0.1:5000').split(',')
    CORS(app, resources={r'/api/*': {'origins': origins}})
    from controllers.auth_controller import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    from controllers.profile_controller import profile_blueprint
    app.register_blueprint(profile_blueprint, url_prefix='/api/profile')
    from controllers.preference_controller import preference_blueprint
    app.register_blueprint(preference_blueprint, url_prefix='/api/preferences')
    from controllers.professional_controller import professional_blueprint
    app.register_blueprint(professional_blueprint, url_prefix='/api/appointments')
    from controllers.recommendation_controller import recommendation_blueprint
    app.register_blueprint(recommendation_blueprint, url_prefix='/api/recommendations')
    from controllers.analysis_controller import analysis_blueprint
    app.register_blueprint(analysis_blueprint, url_prefix='/api/analyses')
    from controllers.history_controller import history_blueprint
    app.register_blueprint(history_blueprint, url_prefix='/api/history')
    from controllers.appointment_controller import appointment_blueprint
    app.register_blueprint(appointment_blueprint, url_prefix='/api/appointments')
    from controllers.simulation_controller import simulation_blueprint
    app.register_blueprint(simulation_blueprint, url_prefix='/api/simulations')
    @app.errorhandler(AppError)
    def app_error(error):
        db.session.rollback()
        return jsonify(message=error.message), error.status_code

    @app.errorhandler(IntegrityError)
    def conflict(error):
        db.session.rollback()
        return jsonify(message='Conflito de dados. Atualize a tela e tente novamente.'), 409

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(message='Recurso não encontrado.'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error('Falha interna: %s', error)
        return jsonify(message='Erro interno da API.'), 500

    web = Path(__file__).resolve().parents[1] / 'frontend' / 'web'
    @app.get('/')
    def index():
        return send_from_directory(web, 'index.html')

    @app.get('/assets/<path:filename>')
    def assets(filename):
        return send_from_directory(web, filename)

    @app.cli.command('init-db')
    def init_db():
        db.create_all()
        print('Tabelas criadas. Execute seed-demo para cadastrar profissionais de demonstração.')

    @app.cli.command('seed-demo')
    def seed_demo():
        from services.seed_professionals import SeedProfessionalsService
        SeedProfessionalsService().execute()
        print('Profissionais de demonstração cadastrados.')
    return app

if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=int(os.getenv('FLASK_PORT', 5000)), debug=False)
