from fastapi.testclient import TestClient
from main import app
from fastapi import status


clinet = TestClient(app)


def test_return_health_check():
    response = clinet.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'Healthy'}
