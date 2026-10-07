from datetime import datetime

import ephem

BODY_MAP = {
    "mercury": ephem.Mercury,
    "venus": ephem.Venus,
    "mars": ephem.Mars,
    "jupiter": ephem.Jupiter,
    "saturn": ephem.Saturn,
    "uranus": ephem.Uranus,
    "neptune": ephem.Neptune,
    "moon": ephem.Moon,
    "sun": ephem.Sun,
}


def _observer(latitude: float, longitude: float, when: datetime) -> ephem.Observer:
    obs = ephem.Observer()
    obs.lat = str(latitude)
    obs.lon = str(longitude)
    obs.date = when
    obs.horizon = "0"
    return obs


def body_horizon(astronomy_body: str | None, latitude: float, longitude: float, when: datetime | None = None):
    if not astronomy_body:
        return None
    cls = BODY_MAP.get(astronomy_body.lower())
    if not cls:
        return None
    when = when or datetime.utcnow()
    obs = _observer(latitude, longitude, when)
    body = cls()
    body.compute(obs)
    return {
        "altitude": float(body.alt) * 180 / ephem.pi,
        "azimuth": float(body.az) * 180 / ephem.pi,
        "ra": float(body.ra) * 12 / ephem.pi,
        "dec": float(body.dec) * 180 / ephem.pi,
    }


def star_horizon(ra_hours: float | None, dec_deg: float | None, latitude: float, longitude: float, when: datetime | None = None):
    if ra_hours is None or dec_deg is None:
        return None
    when = when or datetime.utcnow()
    obs = _observer(latitude, longitude, when)
    star = ephem.FixedBody()
    star._ra = ra_hours * ephem.pi / 12.0
    star._dec = dec_deg * ephem.pi / 180.0
    star.compute(obs)
    return {
        "altitude": float(star.alt) * 180 / ephem.pi,
        "azimuth": float(star.az) * 180 / ephem.pi,
        "ra": ra_hours,
        "dec": dec_deg,
    }


def moon_info(when: datetime | None = None) -> dict:
    when = when or datetime.utcnow()
    moon = ephem.Moon()
    moon.compute(when)
    phase_frac = float(moon.phase) / 100.0
    phase_deg = phase_frac * 360
    if phase_deg < 10 or phase_deg > 350:
        name = "Luna nueva"
    elif phase_deg < 80:
        name = "Creciente"
    elif phase_deg < 100:
        name = "Cuarto creciente"
    elif phase_deg < 170:
        name = "Gibosa creciente"
    elif phase_deg < 190:
        name = "Luna llena"
    elif phase_deg < 260:
        name = "Gibosa menguante"
    elif phase_deg < 280:
        name = "Cuarto menguante"
    else:
        name = "Menguante"
    return {
        "phaseDeg": round(phase_deg, 1),
        "phaseName": name,
        "illumination": round(float(moon.phase)),
    }


def visibility_label(altitude: float | None, magnitude: float | None) -> dict:
    if altitude is None:
        return {"visible": False, "label": "Sin coordenadas"}
    if altitude < 5:
        return {"visible": False, "label": "Bajo el horizonte"}
    if altitude < 15:
        return {"visible": True, "label": "Muy bajo en el cielo"}
    if magnitude is not None and magnitude > 6:
        return {"visible": True, "label": "Alto, pero débil (mejor con prismáticos)"}
    return {"visible": True, "label": "Bien visible"}


def compass_from_azimuth(az: float) -> str:
    dirs = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]
    return dirs[round(az / 45) % 8]
