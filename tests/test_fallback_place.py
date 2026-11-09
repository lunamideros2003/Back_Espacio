from app.services.fallback_place import FALLBACK_PLACE, fallback_place


def test_fallback_has_expected_shape():
    place = fallback_place()
    assert place["source"] == "fallback"
    assert place["label"] == "Bogotá"
    assert -90 <= place["latitude"] <= 90
    assert -180 <= place["longitude"] <= 180


def test_fallback_returns_a_copy():
    first = fallback_place()
    first["label"] = "changed"
    assert FALLBACK_PLACE["label"] == "Bogotá"
    assert fallback_place()["label"] == "Bogotá"
