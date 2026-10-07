from datetime import datetime

import httpx


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
    cloud = (hourly.get("cloud_cover") or [50])[idx]
    visibility = (hourly.get("visibility") or [10000])[idx]
    humidity = (hourly.get("relative_humidity_2m") or [60])[idx]
    daily = data.get("daily") or {}
    sunset = (daily.get("sunset") or [None])[0]
    sunrise = (daily.get("sunrise") or [None])[0]

    quality = "regular"
    message = "Hay nubes parciales; aún puedes ver planetas brillantes."
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
