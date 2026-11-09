from datetime import datetime

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.auth import get_current_user_optional
from app.database import get_db
from app.models import User
from app.services.chart import build_chart
from app.services.places import resolve_place

router = APIRouter(prefix="/api/sky", tags=["sky"])


@router.get("/chart")
async def sky_chart(
    request: Request,
    lat: float | None = Query(None),
    lng: float | None = Query(None),
    date: str | None = Query(None),
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    place = await resolve_place(
        lat,
        lng,
        user,
        dict(request.headers),
        request.client.host if request.client else None,
    )
    when = datetime.fromisoformat(date) if date else datetime.utcnow()
    payload = build_chart(place["latitude"], place["longitude"], when)
    payload["location"]["assumed"] = place["source"] != "browser"
    payload["location"]["label"] = place["label"]
    payload["location"]["source"] = place["source"]
    return payload

