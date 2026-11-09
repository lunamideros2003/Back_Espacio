from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_health_db():
    response = client.get("/api/health/db")
    assert response.status_code == 200
    assert response.json() == {"ok": True, "database": "up"}


def test_cors_debug_reports_allowed_origin():
    response = client.get("/api/debug/cors", headers={"Origin": "http://localhost:5173"})
    assert response.status_code == 200
    assert response.json()["permitido"] is True
