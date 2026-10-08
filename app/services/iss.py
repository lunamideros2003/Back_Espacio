"""Seguimiento de la ISS: trayectoria sobre el mapa y pases visibles.

La API de where-the-iss-at acepta un maximo de 30 marcas de tiempo por
peticion, asi que las consultas largas se trocean.
"""

import math
import time
from datetime import datetime, timezone

import httpx

from app.services.sky import compass_from_azimuth

API = "https://api.wheretheiss.at/v1/satellites/25544"
EARTH_RADIUS_KM = 6371.0
MAX_TIMESTAMPS = 30
MAX_FINE_TIMESTAMPS = 600
MIN_ELEVATION = 10.0


def _iso(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def look_elevation(distance_km: float, altitude_km: float) -> float:
    """Altura sobre el horizonte (grados) de un satelite a esa distancia."""
    gamma = distance_km / EARTH_RADIUS_KM
    horizon = EARTH_RADIUS_KM / (EARTH_RADIUS_KM + altitude_km)
    return math.degrees(math.atan2(math.cos(gamma) - horizon, math.sin(gamma)))


def look_azimuth(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Azimut (desde el norte) del punto de subsatelite visto desde el observador."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    y = math.sin(dl) * math.cos(p2)
    x = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return (math.degrees(math.atan2(y, x)) + 360) % 360


async def _fetch_positions(client: httpx.AsyncClient, timestamps: list[int]) -> list[dict]:
    """Trae posiciones troceando para no pasar del limite de 30 por peticion."""
    points: list[dict] = []
    for start in range(0, len(timestamps), MAX_TIMESTAMPS):
        chunk = timestamps[start : start + MAX_TIMESTAMPS]
        query = ",".join(str(t) for t in chunk)
        res = await client.get(f"{API}/positions?timestamps={query}")
        res.raise_for_status()
        points.extend(res.json())
    return points


async def current_position() -> dict | None:
    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.get(API)
        if res.status_code != 200:
            return None
        data = res.json()
    return {
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "altitudeKm": data.get("altitude"),
        "velocityKmh": data.get("velocity"),
        "timestamp": data.get("timestamp"),
        "name": "Estacion Espacial Internacional (ISS)",
    }


async def track(minutes: int = 30, step: int = 300) -> dict:
    """Posicion actual mas la trayectoria alrededor de esa hora (para el mapa)."""
    minutes = max(5, min(180, minutes))
    step = max(60, step)
    now = int(time.time())
    half = minutes * 60
    timestamps = list(range(now - half, now + half + 1, step))

    current = await current_position()
    async with httpx.AsyncClient(timeout=25) as client:
        points = await _fetch_positions(client, timestamps)

    path = [
        {
            "latitude": p.get("latitude"),
            "longitude": p.get("longitude"),
            "altitudeKm": p.get("altitude"),
            "timestamp": p.get("timestamp"),
            "time": _iso(p.get("timestamp", now)),
        }
        for p in points
    ]
    return {
        "current": current,
        "path": path,
        "window": {
            "start": _iso(timestamps[0]),
            "end": _iso(timestamps[-1]),
            "stepSeconds": step,
        },
    }


async def overhead(latitude: float, longitude: float, hours: int = 24) -> dict:
    """Pases de la ISS sobre un punto: cuando pasa y que tan alto llega.

    Primero un barrido grueso de 24 h para localizar las ventanas cercanas y
    despues un muestreo cada minuto dentro de esas ventanas, para no hacer
    cientos de peticiones a la API.
    """
    hours = max(6, min(48, hours))
    coarse_step = 300
    fine_step = 60
    near_limit_km = 3000.0
    now = int(time.time())

    coarse_ts = list(range(now, now + hours * 3600 + 1, coarse_step))
    async with httpx.AsyncClient(timeout=60) as client:
        coarse = await _fetch_positions(client, coarse_ts)

        windows: list[list[int]] = []
        for p in coarse:
            distance = haversine_km(latitude, longitude, p.get("latitude"), p.get("longitude"))
            if distance <= near_limit_km:
                start = p["timestamp"] - coarse_step - 60
                end = p["timestamp"] + coarse_step + 60
                if windows and start <= windows[-1][1]:
                    windows[-1][1] = max(windows[-1][1], end)
                else:
                    windows.append([start, end])

        fine_ts: list[int] = []
        for start, end in windows:
            fine_ts.extend(range(start, end + 1, fine_step))
        fine_ts = sorted(set(fine_ts))[:MAX_FINE_TIMESTAMPS]
        points = await _fetch_positions(client, fine_ts) if fine_ts else []

    samples = []
    for p in points:
        lat = p.get("latitude")
        lon = p.get("longitude")
        distance = haversine_km(latitude, longitude, lat, lon)
        samples.append(
            {
                "timestamp": p.get("timestamp"),
                "latitude": lat,
                "longitude": lon,
                "elevation": round(look_elevation(distance, p.get("altitude") or 0), 1),
                "azimuth": round(look_azimuth(latitude, longitude, lat, lon), 1),
                "distanceKm": round(distance),
            }
        )

    runs: list[list[dict]] = []
    current: list[dict] = []
    for sample in samples:
        if sample["elevation"] >= MIN_ELEVATION:
            current.append(sample)
        elif current:
            runs.append(current)
            current = []
    if current:
        runs.append(current)

    passes = []
    for run in runs:
        peak = max(run, key=lambda s: s["elevation"])
        passes.append(
            {
                "start": _iso(run[0]["timestamp"]),
                "end": _iso(run[-1]["timestamp"]),
                "durationMinutes": round((run[-1]["timestamp"] - run[0]["timestamp"]) / 60, 1),
                "maxElevation": peak["elevation"],
                "azimuth": peak["azimuth"],
                "direction": compass_from_azimuth(peak["azimuth"]),
                "riseAzimuth": run[0]["azimuth"],
                "setAzimuth": run[-1]["azimuth"],
                "path": [{"latitude": s["latitude"], "longitude": s["longitude"]} for s in run],
            }
        )

    return {
        "location": {"latitude": latitude, "longitude": longitude},
        "checkedHours": hours,
        "minElevation": MIN_ELEVATION,
        "passes": passes,
        "nextPass": passes[0] if passes else None,
    }
