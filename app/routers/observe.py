from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload

from app.auth import get_current_user, get_current_user_optional
from app.database import get_db
from app.models import CelestialObject, Observation, User
from app.services.nasa import get_iss_position
from app.services.sky import body_horizon, compass_from_azimuth, moon_info, star_horizon, visibility_label
from app.services.weather import get_night_sky_conditions

router = APIRouter(prefix="/api/observe", tags=["observe"])


class LogIn(BaseModel):
    objectSlug: str
    notes: str | None = None
    visible: bool = True


@router.get("/tonight")
async def tonight(
    lat: float | None = Query(None),
    lng: float | None = Query(None),
    date: str | None = Query(None),
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
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
    objects = db.query(CelestialObject).all()
    weather = await get_night_sky_conditions(latitude, longitude)
    try:
        iss = await get_iss_position()
    except Exception:
        iss = None

    recommendations = []
    for obj in objects:
        hor = (
            body_horizon(obj.astronomy_body, latitude, longitude, when)
            if obj.astronomy_body
            else star_horizon(obj.ra_hours, obj.dec_deg, latitude, longitude, when)
        )
        vis = visibility_label(hor["altitude"] if hor else None, obj.magnitude)
        altitude = hor["altitude"] if hor else 0
        score = (40 if vis["visible"] else 0) + max(0, altitude)
        if obj.magnitude is not None:
            score += max(0, 15 - obj.magnitude * 2)
        else:
            score += 5
        score -= weather["cloudCover"] / 8
        if vis["visible"]:
            recommendations.append(
                {
                    "object": {
                        "slug": obj.slug,
                        "name": obj.name,
                        "type": obj.type,
                        "magnitude": obj.magnitude,
                        "funFact": obj.fun_fact,
                    },
                    "altitude": round(hor["altitude"], 1) if hor else None,
                    "azimuth": round(hor["azimuth"], 1) if hor else None,
                    "direction": compass_from_azimuth(hor["azimuth"]) if hor else None,
                    "visible": vis["visible"],
                    "label": vis["label"],
                    "score": score,
                }
            )

    recommendations.sort(key=lambda r: r["score"], reverse=True)
    return {
        "when": when.isoformat(),
        "location": {"latitude": latitude, "longitude": longitude, "assumed": assumed},
        "weather": weather,
        "moon": moon_info(when),
        "iss": iss,
        "recommendations": recommendations[:8],
    }


@router.post("/log")
def log_observation(body: LogIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    obj = db.query(CelestialObject).filter(CelestialObject.slug == body.objectSlug).first()
    if not obj:
        raise HTTPException(404, "Objeto no encontrado")
    log = Observation(user_id=user.id, object_id=obj.id, notes=body.notes, visible=body.visible)
    db.add(log)
    db.commit()
    db.refresh(log)
    return {
        "observation": {
            "id": log.id,
            "notes": log.notes,
            "visible": log.visible,
            "date": log.date.isoformat(),
            "object": {"slug": obj.slug, "name": obj.name, "type": obj.type},
        }
    }


@router.get("/mine")
def mine(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = (
        db.query(Observation)
        .options(joinedload(Observation.object))
        .filter(Observation.user_id == user.id)
        .order_by(Observation.date.desc())
        .limit(50)
        .all()
    )
    return {
        "observations": [
            {
                "id": o.id,
                "notes": o.notes,
                "visible": o.visible,
                "date": o.date.isoformat(),
                "object": {"slug": o.object.slug, "name": o.object.name, "type": o.object.type},
            }
            for o in items
        ]
    }
