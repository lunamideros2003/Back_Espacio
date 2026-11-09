from fastapi.testclient import TestClient

from app.main import app
from app.routers import place as place_router

client = TestClient(app)


def test_city_search_returns_places(monkeypatch):
    async def fake_search(query):
        assert query == "Bogota"
        return [{"latitude": 4.6097, "longitude": -74.0817, "label": "Bogotá, Colombia", "source": "search"}]

    monkeypatch.setattr(place_router, "search_places", fake_search)
    response = client.get("/api/place/search", params={"q": "Bogota"})
    assert response.status_code == 200
    assert response.json()["results"][0]["label"] == "Bogotá, Colombia"


def test_city_search_requires_query():
    assert client.get("/api/place/search").status_code == 422


def test_place_endpoint_returns_a_place():
    response = client.get("/api/place")
    assert response.status_code == 200
    place = response.json()["place"]
    assert -90 <= place["latitude"] <= 90
    assert -180 <= place["longitude"] <= 180
    assert place["label"]
