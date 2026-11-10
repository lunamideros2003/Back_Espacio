import asyncio

import httpx

from app.services import weather


class BrokenClient:
    def __init__(self, **_kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return False

    async def get(self, *_args, **_kwargs):
        raise httpx.ConnectError("sin internet")


def test_weather_returns_fallback_when_api_fails(monkeypatch):
    monkeypatch.setattr(weather.httpx, "AsyncClient", BrokenClient)
    data = asyncio.run(weather.get_night_sky_conditions(1.2, -77.2))
    assert data["cloudCover"] == 50
    assert data["quality"] == "regular"
    assert "clima" in data["message"].lower()


def test_pick_uses_default_for_missing_values():
    assert weather.pick([None, 3], 0, 7) == 7
    assert weather.pick([1, 3], 5, 7) == 7
    assert weather.pick([], 0, 7) == 7
    assert weather.pick([1, 3], 1, 7) == 3
