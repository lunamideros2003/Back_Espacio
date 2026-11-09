"""Sky chart assembly: stars, constellation lines and solar system bodies."""

from datetime import datetime

from app.services.chart_bodies import CHART_BODIES
from app.services.constellation_lines import CONSTELLATION_LINES
from app.services.projection import CENTER, RADIUS, VIEWBOX, cardinals, project, star_opacity, star_size
from app.services.sky import body_horizon, star_horizon
from app.services.star_catalog import STAR_CATALOG


def build_chart(latitude: float, longitude: float, when: datetime | None = None) -> dict:
    """Build the full sky chart for one observer and one moment."""
    when = when or datetime.utcnow()

    stars = []
    positions: dict[str, dict] = {}
    for item in STAR_CATALOG:
        horizon = star_horizon(item["ra_hours"], item["dec_deg"], latitude, longitude, when)
        point = project(horizon["altitude"], horizon["azimuth"])
        entry = {
            **item,
            **point,
            "altitude": round(horizon["altitude"], 1),
            "azimuth": round(horizon["azimuth"], 1),
            "size": star_size(item["magnitude"]),
            "opacity": star_opacity(horizon["altitude"]),
        }
        stars.append(entry)
        positions[item["name"]] = entry

    lines = []
    for start, end in CONSTELLATION_LINES:
        a, b = positions.get(start), positions.get(end)
        if a and b:
            lines.append({"from": start, "to": end, "x1": a["x"], "y1": a["y"], "x2": b["x"], "y2": b["y"]})

    bodies = []
    for item in CHART_BODIES:
        horizon = body_horizon(item["astronomy_body"], latitude, longitude, when)
        if not horizon:
            continue
        point = project(horizon["altitude"], horizon["azimuth"])
        bodies.append(
            {
                "slug": item["slug"],
                "name": item["name"],
                "type": item["type"],
                "size": item["size"],
                **point,
                "altitude": round(horizon["altitude"], 1),
                "azimuth": round(horizon["azimuth"], 1),
                "opacity": star_opacity(horizon["altitude"]),
            }
        )

    return {
        "when": when.isoformat(),
        "location": {"latitude": latitude, "longitude": longitude},
        "viewBox": f"0 0 {VIEWBOX} {VIEWBOX}",
        "center": CENTER,
        "radius": RADIUS,
        "cardinals": cardinals(),
        "stars": stars,
        "lines": lines,
        "bodies": bodies,
    }
