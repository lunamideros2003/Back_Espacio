from fastapi.testclient import TestClient

import app.routers.observe as observe
from app.main import app

client = TestClient(app, raise_server_exceptions=False)


async def fake_place(*_args, **_kwargs):
    return {"latitude": 1.0, "longitude": -77.0, "label": "Prueba", "source": "browser"}


def test_unhandled_error_returns_json_with_cors(monkeypatch):
    monkeypatch.setattr(observe, "resolve_place", fake_place)

    async def boom(*_args, **_kwargs):
        raise RuntimeError("explota")

    monkeypatch.setattr(observe, "get_night_sky_conditions", boom)

    response = client.get(
        "/api/observe/tonight?lat=1&lng=-77",
        headers={"Origin": "https://fron-espacio.vercel.app"},
    )

    assert response.status_code == 500
    assert response.json()["error"].startswith("Error interno")
    assert response.headers["access-control-allow-origin"] == "https://fron-espacio.vercel.app"


def test_unhandled_error_without_allowed_origin_has_no_cors(monkeypatch):
    monkeypatch.setattr(observe, "resolve_place", fake_place)

    async def boom(*_args, **_kwargs):
        raise RuntimeError("explota")

    monkeypatch.setattr(observe, "get_night_sky_conditions", boom)

    response = client.get(
        "/api/observe/tonight?lat=1&lng=-77",
        headers={"Origin": "https://otro-sitio.com"},
    )

    assert response.status_code == 500
    assert "access-control-allow-origin" not in response.headers
