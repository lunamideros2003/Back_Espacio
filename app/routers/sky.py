from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth import get_current_user_optional
from app.database import get_db
from app.models import User
from app.services.chart import build_chart

router = APIRouter(prefix="/api/sky", tags=["sky"])


@router.get("/chart")
def sky_chart(
    lat: float | None = Query(None),
    lng: float | None = Query(None),
    date: str | None = Query(None),
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    """Carta celeste circular para un observador y un momento dados."""
    latitude = lat
    longitude = lng
    assumed = lat is None or lng is None
    if assumed:
        if user and user.latitude is not None and user.longitude is not None:
            latitude = user.latitude
            longitude = user.longitude
        else:
            latitude, longitude = 4.711, -74.0721

    when = datetime.fromisoformat(date) if date else datetime.utcnow()
    payload = build_chart(latitude, longitude, when)
    payload["location"]["assumed"] = assumed
    return payload
