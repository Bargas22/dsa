import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from extensions import db
from services.seed_professionals import SeedProfessionalsService

@pytest.fixture
def app():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite://', 'JWT_SECRET': 'integration-tests-only-secret-key-0001'})
    with app.app_context():
        db.create_all()
        SeedProfessionalsService().execute()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth(client):
    response = client.post('/api/auth/register', json={'name': 'Aluno', 'email': 'aluno@example.com', 'password': 'Teste12345'})
    assert response.status_code == 201
    return {'Authorization': 'Bearer '+response.json['token']}
