import math

from app.services.projection import CENTER, RADIUS, cardinals, project, star_opacity, star_size


def test_zenith_is_center():
    point = project(90, 0)
    assert point["x"] == CENTER
    assert point["y"] == CENTER
    assert point["visible"] is True


def test_horizon_is_at_the_edge():
    point = project(0, 0)
    assert point["x"] == CENTER
    assert point["y"] == CENTER - RADIUS


def test_east_is_on_the_right():
    point = project(0, 90)
    assert point["x"] == CENTER + RADIUS
    assert point["y"] == CENTER


def test_below_horizon_is_not_visible():
    assert project(-10, 0)["visible"] is False


def test_star_size_is_clamped():
    assert star_size(None) == 2.5
    assert star_size(-5) == 7.0
    assert star_size(10) == 1.2


def test_star_opacity_is_clamped():
    assert star_opacity(-1) == 0.0
    assert star_opacity(90) == 1.0
    assert 0.4 <= star_opacity(10) <= 1.0


def test_cardinals_are_four_and_centered():
    points = cardinals()
    assert len(points) == 4
    north = points[0]
    assert north["label"] == "N"
    assert math.isclose(north["x"], CENTER)
