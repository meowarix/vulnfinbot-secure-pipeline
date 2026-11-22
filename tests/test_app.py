import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}


def test_chat_success(client):
    response = client.post("/api/chat", json={
        "message": "How can I save money?"
    })

    assert response.status_code == 200
    assert "response" in response.json


def test_empty_message(client):
    response = client.post("/api/chat", json={
        "message": ""
    })

    assert response.status_code == 400


def test_missing_message(client):
    response = client.post("/api/chat", json={})
    assert response.status_code == 400


def test_invalid_json(client):
    response = client.post(
        "/api/chat",
        data="{invalid}",
        content_type="application/json"
    )

    assert response.status_code == 400


def test_long_message(client):
    response = client.post("/api/chat", json={
        "message": "a" * 501
    })

    assert response.status_code == 400


def test_invalid_type(client):
    response = client.post("/api/chat", json={
        "message": 123
    })

    assert response.status_code == 400