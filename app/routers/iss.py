from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import get_current_user_optional
from app.database import get_db
from app.models import User
from app.services import iss

router = APIRouter(prefix="/api/iss", tags=["iss"])


def _resolve_location(lat: float | None, lng: float | None, user: User | None) -> tuple[float, float, bool]:
    assumed = lat is None or lng is None
    if not assumed:
        return lat, lng, False
    if user and user.latitude is not None and user.longitude is not None:
        return user.latitude, user.longitude, True
    return 4.711, -74.0721, True


@router.get("/track")
async def iss_track(
    minutes: int = Query(30, ge=5, le=180),
    step: int = Query(300, ge=60, le=900),
):
    """Posicion actual de la ISS y su trayectoria alrededor de esa hora."""
    try:
        return await iss.track(minutes=minutes, step=step)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="No se pudo consultar la posicion de la ISS") from exc


@router.get("/overhead")
async def iss_overhead(
    lat: float | None = Query(None),
    lng: float | None = Query(None),
    hours: int = Query(24, ge=6, le=48),
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    """Proximos pases de la ISS visibles desde un punto del planeta."""
    latitude, longitude, assumed = _resolve_location(lat, lng, user)
    try:
        payload = await iss.overhead(latitude, longitude, hours=hours)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="No se pudieron calcular los pases de la ISS") from exc
    payload["location"]["assumed"] = assumed
    return payload
