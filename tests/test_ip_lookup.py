import asyncio

from app.services import ip_lookup
from app.services.place_cache import TtlCache


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeClient:
    def __init__(self, payload=None, error=None):
        self.payload = payload
        self.error = error
        self.url = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return False

    async def get(self, url):
        self.url = url
        if self.error:
            raise self.error
        return FakeResponse(self.payload)


def install(monkeypatch, client):
    monkeypatch.setattr(ip_lookup, "_cache", TtlCache(3600))
    monkeypatch.setattr(ip_lookup.httpx, "AsyncClient", lambda **_kwargs: client)
    return client


def test_lookup_ip_builds_a_place(monkeypatch):
    client = install(
        monkeypatch,
        FakeClient({"success": True, "latitude": 6.24, "longitude": -75.58, "city": "Medellin", "region": "Antioquia", "country": "Colombia"}),
    )
    place = asyncio.run(ip_lookup.lookup_ip("190.1.2.3"))
    assert client.url.endswith("190.1.2.3")
    assert place == {
        "latitude": 6.24,
        "longitude": -75.58,
        "label": "Medellin, Antioquia",
        "source": "ip",
    }


def test_lookup_ip_uses_self_without_an_address(monkeypatch):
    client = install(monkeypatch, FakeClient({"success": True, "latitude": 1, "longitude": 2, "country": "Colombia"}))
    asyncio.run(ip_lookup.lookup_ip(None))
    assert client.url == "https://ipwho.is/"


def test_lookup_ip_returns_none_on_failure(monkeypatch):
    install(monkeypatch, FakeClient({"success": False}))
    assert asyncio.run(ip_lookup.lookup_ip("190.1.2.3")) is None


def test_lookup_ip_returns_none_on_network_error(monkeypatch):
    install(monkeypatch, FakeClient(error=RuntimeError("offline")))
    assert asyncio.run(ip_lookup.lookup_ip("190.1.2.4")) is None


def test_lookup_ip_rejects_missing_coordinates(monkeypatch):
    install(monkeypatch, FakeClient({"success": True, "city": "Nada"}))
    assert asyncio.run(ip_lookup.lookup_ip("190.1.2.5")) is None


def test_lookup_ip_uses_the_cache(monkeypatch):
    client = install(monkeypatch, FakeClient({"success": True, "latitude": 3, "longitude": 4, "country": "Colombia"}))
    first = asyncio.run(ip_lookup.lookup_ip("190.1.2.6"))
    client.error = RuntimeError("should not be called")
    second = asyncio.run(ip_lookup.lookup_ip("190.1.2.6"))
    assert first == second
