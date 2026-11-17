from app import db
from app.models import User


def register(client):
    return client.post("/register", data={
        "username": "tester",
        "email": "tester@example.com",
        "password": "password123",
    }, follow_redirects=True)


def login(client):
    return client.post("/login", data={
        "username": "tester",
        "password": "password123",
    }, follow_redirects=True)


def test_health_and_homepage(client):
    assert client.get("/health").json["status"] == "ok"
    assert client.get("/").status_code == 200


def test_authentication_and_dashboard(client, app):
    assert client.get("/dashboard").status_code == 302
    assert register(client).status_code == 200
    with app.app_context():
        assert User.query.count() == 1
    assert login(client).status_code == 200
    assert client.get("/dashboard").status_code == 200
    assert client.get("/infrastructure").status_code == 200


def test_ai_endpoint_requires_authentication(client):
    response = client.post("/api/ai/chat", json={"message": "What is Docker?"})
    assert response.status_code == 302


def test_ai_endpoint_validates_input(client):
    register(client)
    login(client)
    response = client.post("/api/ai/chat", json={"message": ""})
    assert response.status_code == 400

