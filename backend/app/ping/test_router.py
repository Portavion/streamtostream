from fastapi.testclient import TestClient

from .router import router

client = TestClient(router)


def test_return_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"msg": "pong"}
