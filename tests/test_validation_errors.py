from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_without_at_returns_spanish_error():
    response = client.post(
        "/api/auth/register",
        json={"name": "Luna", "email": "luna.astroia.dev", "password": "astroia123"},
    )
    assert response.status_code == 422
    body = response.json()
    assert "correo" in body["error"].lower()
    assert "@" in body["error"]


def test_login_without_at_returns_spanish_error():
    response = client.post(
        "/api/auth/login",
        json={"email": "luna.astroia.dev", "password": "astroia123"},
    )
    assert response.status_code == 422
    assert "correo" in response.json()["error"].lower()


def test_missing_field_returns_spanish_error():
    response = client.post("/api/auth/login", json={"email": "luna@astroia.dev"})
    assert response.status_code == 422
    assert "campo" in response.json()["error"].lower()
