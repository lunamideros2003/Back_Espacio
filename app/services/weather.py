from datetime import datetime

import httpx

FALLBACK = {
    "cloudCover": 50,
    "visibilityKm": 10.0,
    "humidity": 60,
    "sunset": None,
    "sunrise": None,
    "quality": "regular",
    "message": "No pudimos consultar el clima ahora. Aun asi puedes intentar observar.",
    "timezone": None,
}


def pick(values: list, idx: int, default):
    if not values or idx >= len(values) or values[idx] is None:
        return default
    return values[idx]


async def get_night_sky_conditions(latitude: float, longitude: float) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "cloud_cover,visibility,relative_humidity_2m",
        "daily": "sunrise,sunset",
        "timezone": "auto",
        "forecast_days": 1,
    }
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            res = await client.get(url, params=params)
            res.raise_for_status()
            data = res.json()

        hours = data.get("hourly", {}).get("time") or []
        now = datetime.now()
        idx = 0
        for i, stamp in enumerate(hours):
            try:
                if datetime.fromisoformat(stamp) >= now.replace(tzinfo=None):
                    idx = i
                    break
            except ValueError:
                continue

        hourly = data.get("hourly") or {}
        cloud = pick(hourly.get("cloud_cover"), idx, 50)
        visibility = pick(hourly.get("visibility"), idx, 10000)
        humidity = pick(hourly.get("relative_humidity_2m"), idx, 60)
        daily = data.get("daily") or {}
        sunset = pick(daily.get("sunset"), 0, None)
        sunrise = pick(daily.get("sunrise"), 0, None)
    except Exception as exc:
        print(f"[AstroIA] Clima no disponible: {type(exc).__name__}: {exc}")
        return dict(FALLBACK)

    quality = "regular"
    message = "Hay nubes parciales; aun puedes ver planetas brillantes."
    if cloud < 25 and visibility > 8000:
        quality = "excelente"
        message = "Cielo despejado: noche ideal para observar."
    elif cloud < 50:
        quality = "buena"
        message = "Buena noche, con algunas nubes. Prioriza objetos brillantes."
    elif cloud > 80:
        quality = "mala"
        message = "Mucha nubosidad: mejor planear para otra noche."

    return {
        "cloudCover": cloud,
        "visibilityKm": round((visibility or 0) / 1000, 1),
        "humidity": humidity,
        "sunset": sunset,
        "sunrise": sunrise,
        "quality": quality,
        "message": message,
        "timezone": data.get("timezone"),
    }
