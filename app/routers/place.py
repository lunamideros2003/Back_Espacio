from fastapi import APIRouter, Depends, Query, Request

from app.auth import get_current_user_optional
from app.models import User
from app.services.geocode import search_places
from app.services.places import resolve_place

router = APIRouter(prefix="/api/place", tags=["place"])


@router.get("")
async def where(
    request: Request,
    lat: float | None = Query(None),
    lng: float | None = Query(None),
    user: User | None = Depends(get_current_user_optional),
):
    """Resolve the observer location without asking for manual coordinates."""
    host = request.client.host if request.client else None
    place = await resolve_place(lat, lng, user, dict(request.headers), host)
    return {"place": place}


@router.get("/search")
async def search(q: str = Query(..., min_length=2, max_length=80)):
    """Search cities by name so the UI never needs latitude/longitude fields."""
    return {"results": await search_places(q)}
