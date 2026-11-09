import httpx

from app.services.place_cache import TtlCache
from app.services.place_label import format_label

BIGDATA_URL = "https://api.bigdatacloud.net/data/reverse-geocode-client"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/reverse"
USER_AGENT = "AstroIA/1.0 (https://github.com/lunamideros2003/Fron_Espacio)"
CACHE_SECONDS = 60 * 60 * 24

_cache = TtlCache(CACHE_SECONDS)


def label_from_bigdata(payload: dict) -> str | None:
    if not isinstance(payload, dict):
        return None
    city = payload.get("city") or payload.get("locality")
    return format_label(city, payload.get("countryName")) or None


def label_from_nominatim(payload: dict) -> str | None:
    if not isinstance(payload, dict):
        return None
    address = payload.get("address") or {}
    city = (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or address.get("municipality")
    )
    return format_label(city, address.get("country")) or None


async def _bigdata(latitude: float, longitude: float) -> str | None:
    try:
        async with httpx.AsyncClient(timeout=6.0) as client:
            response = await client.get(
                BIGDATA_URL,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "localityLanguage": "es",
                },
                headers={"User-Agent": USER_AGENT},
            )
            response.raise_for_status()
            return label_from_bigdata(response.json())
    except Exception:
        return None


async def _nominatim(latitude: float, longitude: float) -> str | None:
    try:
        async with httpx.AsyncClient(timeout=6.0) as client:
            response = await client.get(
                NOMINATIM_URL,
                params={
                    "format": "jsonv2",
                    "lat": latitude,
                    "lon": longitude,
                    "zoom": 10,
                    "accept-language": "es",
                },
                headers={"User-Agent": USER_AGENT},
            )
            response.raise_for_status()
            return label_from_nominatim(response.json())
    except Exception:
        return None


async def reverse_label(latitude: float, longitude: float) -> str | None:
    """Human readable city for a coordinate pair, with a second provider as backup."""
    cache_key = f"{round(latitude, 2)},{round(longitude, 2)}"
    cached = _cache.get(cache_key)
    if cached:
        return cached

    for resolver in (_bigdata, _nominatim):
        label = await resolver(latitude, longitude)
        if label:
            _cache.set(cache_key, label)
            return label
    return None
