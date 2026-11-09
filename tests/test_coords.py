import math

import pytest

from app.services.coords import coords_ok, parse_coord


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, None),
        ("", None),
        ("nope", None),
        ("4.711", 4.711),
        ("  -74.0721  ", -74.0721),
        (float("nan"), None),
        (float("inf"), None),
        (float("-inf"), None),
    ],
)
def test_parse_coord(value, expected):
    assert parse_coord(value) == expected


@pytest.mark.parametrize(
    ("latitude", "longitude", "expected"),
    [
        (0, 0, True),
        (90, 180, True),
        (-90, -180, True),
        (91, 0, False),
        (0, 181, False),
        (-91, 0, False),
    ],
)
def test_coords_ok(latitude, longitude, expected):
    assert coords_ok(latitude, longitude) is expected


def test_parse_coord_returns_float():
    assert isinstance(parse_coord("12.5"), float)
    assert not math.isnan(parse_coord("12.5"))
