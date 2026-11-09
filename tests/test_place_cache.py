from app.services.place_cache import TtlCache


def test_cache_roundtrip():
    cache = TtlCache(ttl_seconds=60)
    cache.set("key", {"latitude": 1})
    assert cache.get("key") == {"latitude": 1}


def test_cache_expires(monkeypatch):
    clock = {"now": 1000.0}
    monkeypatch.setattr("app.services.place_cache.time.time", lambda: clock["now"])
    cache = TtlCache(ttl_seconds=10)
    cache.set("key", "value")
    clock["now"] = 1005.0
    assert cache.get("key") == "value"
    clock["now"] = 1011.0
    assert cache.get("key") is None


def test_cache_missing_key():
    assert TtlCache().get("missing") is None
