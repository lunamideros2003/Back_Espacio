from app.services.reverse_place import label_from_bigdata, label_from_nominatim


def test_bigdata_prefers_city():
    payload = {"city": "Bogotá", "locality": "Suba", "countryName": "Colombia"}
    assert label_from_bigdata(payload) == "Bogotá, Colombia"


def test_bigdata_falls_back_to_locality():
    payload = {"city": "", "locality": "Pasto", "countryName": "Colombia"}
    assert label_from_bigdata(payload) == "Pasto, Colombia"


def test_bigdata_handles_empty_payload():
    assert label_from_bigdata({}) is None
    assert label_from_bigdata(None) is None


def test_nominatim_reads_address_fields():
    payload = {"address": {"town": "Pasto", "country": "Colombia"}}
    assert label_from_nominatim(payload) == "Pasto, Colombia"


def test_nominatim_handles_missing_address():
    assert label_from_nominatim({}) is None
    assert label_from_nominatim(None) is None
