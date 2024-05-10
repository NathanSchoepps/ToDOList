from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_docs():
    res = client.get("/")
    print(res.status_code)
    assert res.status_code == 200