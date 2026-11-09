from datetime import datetime

from app.services.chart import build_chart
from app.services.projection import CENTER, RADIUS


def test_chart_has_expected_sections():
    chart = build_chart(4.711, -74.0721, datetime(2024, 1, 1, 0, 0))
    assert chart["viewBox"] == "0 0 1000 1000"
    assert chart["center"] == CENTER
    assert chart["radius"] == RADIUS
    assert len(chart["cardinals"]) == 4
    assert len(chart["stars"]) > 50
    assert len(chart["bodies"]) == 9
    assert chart["lines"]


def test_visible_stars_stay_inside_the_chart():
    chart = build_chart(4.711, -74.0721, datetime(2024, 6, 1, 3, 0))
    for star in chart["stars"]:
        if not star["visible"]:
            continue
        distance = ((star["x"] - CENTER) ** 2 + (star["y"] - CENTER) ** 2) ** 0.5
        assert distance <= RADIUS + 0.2


def test_chart_lines_reference_catalog_names():
    chart = build_chart(4.711, -74.0721, datetime(2024, 1, 1, 0, 0))
    names = {star["name"] for star in chart["stars"]}
    for line in chart["lines"]:
        assert line["from"] in names
        assert line["to"] in names
