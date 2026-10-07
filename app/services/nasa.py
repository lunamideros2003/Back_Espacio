import httpx

from app.config import settings


async def get_apod() -> dict:
    url = f"https://api.nasa.gov/planetary/apod?api_key={settings.nasa_api_key}"
    async with httpx.AsyncClient(timeout=20) as client:
        res = await client.get(url)
        res.raise_for_status()
        data = res.json()
    return {
        "title": data.get("title"),
        "explanation": data.get("explanation"),
        "url": data.get("url"),
        "hdurl": data.get("hdurl"),
        "date": data.get("date"),
        "copyright": data.get("copyright") or "NASA",
        "mediaType": data.get("media_type"),
    }


async def search_nasa_image(query: str) -> str | None:
    url = "https://images-api.nasa.gov/search"
    async with httpx.AsyncClient(timeout=20) as client:
        res = await client.get(url, params={"q": query, "media_type": "image"})
        if res.status_code != 200:
            return None
        data = res.json()
    items = data.get("collection", {}).get("items") or []
    if not items:
        return None
    links = items[0].get("links") or []
    return links[0].get("href") if links else None


async def get_iss_position() -> dict | None:
    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.get("https://api.wheretheiss.at/v1/satellites/25544")
        if res.status_code != 200:
            return None
        data = res.json()
    return {
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "altitudeKm": data.get("altitude"),
        "velocityKmh": data.get("velocity"),
        "name": "Estación Espacial Internacional (ISS)",
    }
