from app.services.place_label import format_label


def test_format_label_joins_two_parts():
    assert format_label("Bogotá", "Colombia") == "Bogotá, Colombia"


def test_format_label_drops_duplicates_and_blanks():
    assert format_label(" Bogotá ", "Bogotá", None, "Colombia") == "Bogotá, Colombia"


def test_format_label_collapses_whitespace():
    assert format_label("  Nueva   York ", " Estados   Unidos ") == "Nueva York, Estados Unidos"


def test_format_label_respects_limit():
    assert len(format_label("x" * 200)) <= 80


def test_format_label_empty():
    assert format_label(None, "", "   ") == ""
