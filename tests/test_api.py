
from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_predict_endpoint():
    response = client.post(
        "/predict",
        json={
            "review": "This movie was absolutely fantastic!"
        }
    )

    assert response.status_code == 200
    assert response.json()["sentiment"] == "positive"


def test_empty_review_rejected():
    response = client.post(
        "/predict",
        json={"review": "   "}
    )

    assert response.status_code == 422


def test_numeric_review_rejected():
    response = client.post(
        "/predict",
        json={"review": "123456"}
    )

    assert response.status_code == 422


def test_invalid_data_type_rejected():
    response = client.post(
        "/predict",
        json={"review": 12345}
    )

    assert response.status_code == 422
