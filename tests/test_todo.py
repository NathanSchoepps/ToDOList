from firebase_admin import auth
from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_create_todolists_success(auth_user):
    res = client.post("/todolists", headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
        }, json={
        "category": "Travail",
        "tasks": [{"name": "Complete project proposal", "priority": "High"}]
        })
    assert res.status_code == 200

def test_get_all_todo_lists_success(auth_user):
    res = client.get("/todolists/", headers={"Authorization": f"Bearer {auth_user['access_token']}"})
    assert res.status_code == 200

def test_get_all_todo_lists_no_auth():
    res = client.get("/todolists/")
    assert res.status_code == 401

def test_get_todo_lists_by_category_success(auth_user):
    res = client.get("/todolists/Travail", headers={"Authorization": f"Bearer {auth_user['access_token']}"})
    assert res.status_code == 200

def test_create_todo_list_success(auth_user):
    payload = {"category": "Loisirs", "tasks": [{"name": "Jouer au tennis", "priority": "Low"}]}
    res = client.post("/todolists/", headers={"Authorization": f"Bearer {auth_user['access_token']}"}, json=payload)
    assert res.status_code == 200
    assert res.json()['category'] == "Loisirs"

def test_create_todo_list_no_auth():
    payload = {"category": "Loisirs", "tasks": [{"name": "Jouer au tennis", "priority": "Low"}]}
    res = client.post("/todolists/", json=payload)
    assert res.status_code == 401

def test_add_task_to_todo_list_success(auth_user):
    task = {"name": "New Report", "priority": "Medium"}
    res = client.post(f"/todolists/Travail", headers={"Authorization": f"Bearer {auth_user['access_token']}"}, json=task)
    assert res.status_code == 200
    assert any(t['name'] == "New Report" for t in res.json()['tasks'])

def test_add_task_to_todo_list_not_found(auth_user):
    task = {"name": "New Report", "priority": "Medium"}
    res = client.post(f"/todolists/Unknown", headers={"Authorization": f"Bearer {auth_user['access_token']}"}, json=task)
    assert res.status_code == 404

