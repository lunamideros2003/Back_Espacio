"""Projection helpers for the circular sky chart."""

import math

VIEWBOX = 1000
CENTER = VIEWBOX / 2
RADIUS = 450.0
CARDINALS = [(0, "N"), (90, "E"), (180, "S"), (270, "O")]


def project(altitude: float, azimuth: float) -> dict:
    """Convert altitude/azimuth into circular chart coordinates.

    The zenith sits at the center, the horizon on the edge and north on top.
    Azimuth grows towards the east (right side).
    """
    radius = (90.0 - altitude) / 90.0 * RADIUS
    angle = math.radians(azimuth)
    return {
        "x": round(CENTER + radius * math.sin(angle), 1),
        "y": round(CENTER - radius * math.cos(angle), 1),
        "visible": altitude >= 0,
    }


def star_size(magnitude: float | None) -> float:
    if magnitude is None:
        return 2.5
    return round(max(1.2, min(7.0, 3.4 - magnitude)), 2)


def star_opacity(altitude: float) -> float:
    if altitude < 0:
        return 0.0
    return round(max(0.4, min(1.0, 0.5 + altitude / 60.0)), 2)


def cardinals() -> list[dict]:
    labels = []
    for azimuth, text in CARDINALS:
        angle = math.radians(azimuth)
        radius = RADIUS + 28
        labels.append(
            {
                "label": text,
                "x": round(CENTER + radius * math.sin(angle), 1),
                "y": round(CENTER - radius * math.cos(angle), 1),
            }
        )
    return labels
