import httpx

from app.services.place_cache import TtlCache
from app.services.place_label import format_label

_cache = TtlCache(3600)


async def lookup_ip(ip: str | None) -> dict | None:
    key = ip or "self"
    cached = _cache.get(key)
    if cached:
        return cached
    url = f"https://ipwho.is/{ip}" if ip else "https://ipwho.is/"
    try:
        async with httpx.AsyncClient(timeout=6.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
    except Exception:
        return None
    if data.get("success") is False:
        return None
    lat = data.get("latitude")
    lng = data.get("longitude")
    if lat is None or lng is None:
        return None
    place = {
        "latitude": float(lat),
        "longitude": float(lng),
        "label": format_label(data.get("city"), data.get("region"), data.get("country")) or "Tu zona",
        "source": "ip",
    }
    _cache.set(key, place)
    return place
