from fastapi.testclient import TestClient
from firebase_admin import auth
from main import app
import pytest

client = TestClient(app)

@pytest.fixture
def test_create_task():
    response = client.post("/todolists", json={
        "category": "Maison",
        "tasks": [
            {"name": "Passer l'aspirateur", "priority": "High"}
        ]
    })
    assert response.status_code == 201
    data = response.json()
    assert data['category'] == "Maison"
    assert data['tasks'][0]['name'] == "Passer l'aspirateur"
    assert data['tasks'][0]['priority'] == "High"

@pytest.fixture
def created_user():
    user_credential = client.post("/auth/signup", json={
        "email": "test.user@gmail.com",
        "password": "password"
        })
    
    
@pytest.fixture
def auth_user(created_user):
    user_credential = client.post("/auth/login", data={
        "username": "test.user@gmail.com",
        "password": "password",
        })

    return user_credential.json()