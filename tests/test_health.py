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


def test_cors_allows_any_local_port():
    origin = "http://localhost:4173"
    response = client.options(
        "/api/health",
        headers={"Origin": origin, "Access-Control-Request-Method": "GET"},
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin


def test_cors_allows_vercel_preview():
    origin = "https://fron-espacio-git-main-luna.vercel.app"
    response = client.options(
        "/api/health",
        headers={"Origin": origin, "Access-Control-Request-Method": "GET"},
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin


def test_cors_rejects_other_origins():
    response = client.get("/api/debug/cors", headers={"Origin": "https://ejemplo.com"})
    assert response.json()["permitido"] is False
