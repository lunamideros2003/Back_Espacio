import asyncio
from types import SimpleNamespace

from app.services.places import resolve_place


def run(coro):
    return asyncio.run(coro)


async def fake_reverse(latitude, longitude):
    return f"Ciudad {latitude}"


async def fake_lookup(ip):
    return {"latitude": 1.5, "longitude": -2.5, "label": "IP", "source": "ip"}


def test_browser_coordinates_win():
    place = run(resolve_place("4.7", "-74.1", None, {}, None, fake_lookup, fake_reverse))
    assert place == {
        "latitude": 4.7,
        "longitude": -74.1,
        "label": "Ciudad 4.7",
        "source": "browser",
    }


def test_profile_coordinates_are_second_choice():
    user = SimpleNamespace(latitude=2.2, longitude=-3.3, city="Perfil")
    place = run(resolve_place(None, None, user, {}, None, fake_lookup, fake_reverse))
    assert place == {"latitude": 2.2, "longitude": -3.3, "label": "Perfil", "source": "profile"}


def test_ip_lookup_is_third_choice():
    place = run(resolve_place(None, None, None, {"X-Forwarded-For": "8.8.8.8"}, None, fake_lookup, fake_reverse))
    assert place["source"] == "ip"
    assert place["label"] == "IP"


def test_fallback_when_nothing_works():
    async def no_lookup(ip):
        return None

    place = run(resolve_place(None, None, None, {}, None, no_lookup, fake_reverse))
    assert place["source"] == "fallback"
    assert place["label"] == "Bogotá"


def test_invalid_coordinates_are_ignored():
    place = run(resolve_place("500", "900", None, {}, None, fake_lookup, fake_reverse))
    assert place["source"] == "ip"


def test_profile_without_label_uses_default():
    user = SimpleNamespace(latitude=2.2, longitude=-3.3, city=None)
    place = run(resolve_place(None, None, user, {}, None, fake_lookup, fake_reverse))
    assert place["label"] == "Tu perfil"
