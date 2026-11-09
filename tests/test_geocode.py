from app.services.geocode import normalize_query, parse_results


def test_normalize_query_collapses_spaces_and_caps_length():
    assert normalize_query("  Bogota   Colombia ") == "Bogota Colombia"
    assert len(normalize_query("x" * 200)) == 80
    assert normalize_query(None) == ""


def test_parse_results_keeps_valid_rows():
    payload = {
        "results": [
            {"name": "Bogotá", "country": "Colombia", "latitude": 4.6097, "longitude": -74.0817},
            {"name": "Pasto", "country": "Colombia", "latitude": 1.2136, "longitude": -77.2811},
        ]
    }
    results = parse_results(payload)
    assert results == [
        {"latitude": 4.6097, "longitude": -74.0817, "label": "Bogotá, Colombia", "source": "search"},
        {"latitude": 1.2136, "longitude": -77.2811, "label": "Pasto, Colombia", "source": "search"},
    ]


def test_parse_results_skips_bad_rows_and_duplicates():
    payload = {
        "results": [
            {"name": "A", "country": "X", "latitude": "bad", "longitude": 1},
            {"name": "B", "country": "X", "latitude": 1, "longitude": 2},
            {"name": "B2", "country": "X", "latitude": 1, "longitude": 2},
            {"name": "C", "country": "X", "latitude": 100, "longitude": 2},
        ]
    }
    results = parse_results(payload)
    assert len(results) == 1
    assert results[0]["label"] == "B, X"


def test_parse_results_empty_payload():
    assert parse_results({}) == []
