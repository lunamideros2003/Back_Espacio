import httpx

from app.services.place_cache import TtlCache
from app.services.place_label import format_label

SEARCH_URL = "https://geocoding-api.open-meteo.com/v1/search"
CACHE_SECONDS = 60 * 60 * 24
MAX_QUERY = 80

_cache = TtlCache(CACHE_SECONDS)


def normalize_query(text: str | None) -> str:
    """Collapse whitespace and cap the query so the upstream API stays happy."""
    return " ".join((text or "").split())[:MAX_QUERY]


def parse_results(payload: dict) -> list[dict]:
    """Convert an Open-Meteo geocoding payload into our place shape."""
    rows = payload.get("results") or []
    results: list[dict] = []
    seen: set[tuple[float, float]] = set()

    for row in rows:
        try:
            latitude = float(row.get("latitude"))
            longitude = float(row.get("longitude"))
        except (TypeError, ValueError):
            continue
        if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            continue

        label = format_label(row.get("name"), row.get("country"))
        if not label:
            continue

        key = (round(latitude, 4), round(longitude, 4))
        if key in seen:
            continue
        seen.add(key)
        results.append(
            {
                "latitude": round(latitude, 4),
                "longitude": round(longitude, 4),
                "label": label,
                "source": "search",
            }
        )

    return results


async def search_places(query: str | None, count: int = 6) -> list[dict]:
    """Search cities by name. Results are cached for a day."""
    text = normalize_query(query)
    if len(text) < 2:
        return []

    cache_key = f"search:{text.lower()}"
    cached = _cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        async with httpx.AsyncClient(timeout=6.0) as client:
            response = await client.get(
                SEARCH_URL,
                params={"name": text, "count": count, "language": "es", "format": "json"},
            )
            response.raise_for_status()
            payload = response.json()
    except Exception:
        return []

    results = parse_results(payload)
    _cache.set(cache_key, results)
    return results
