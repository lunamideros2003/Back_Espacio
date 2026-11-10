from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session, joinedload

from app.auth import get_current_user, get_current_user_optional
from app.database import get_db
from app.models import CelestialObject, Observation, User
from app.schemas.observe import LogIn
from app.services.nasa import get_iss_position
from app.services.places import resolve_place
from app.services.sky import body_horizon, compass_from_azimuth, moon_info, star_horizon, visibility_label
from app.services.weather import get_night_sky_conditions

router = APIRouter(prefix="/api/observe", tags=["observe"])


@router.get("/tonight")
async def tonight(
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
    latitude = place["latitude"]
    longitude = place["longitude"]
    assumed = place["source"] != "browser"

    try:
        when = datetime.fromisoformat(date) if date else datetime.utcnow()
    except ValueError as exc:
        raise HTTPException(400, "La fecha no es valida") from exc
    objects = db.query(CelestialObject).all()
    weather = await get_night_sky_conditions(latitude, longitude)
    try:
        iss = await get_iss_position()
    except Exception:
        iss = None
    try:
        moon = moon_info(when)
    except Exception as exc:
        print(f"[AstroIA] Luna no disponible: {type(exc).__name__}: {exc}")
        moon = {"phaseDeg": 0, "phaseName": "Sin datos", "illumination": 0}

    recommendations = []
    for obj in objects:
        try:
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
        except Exception as exc:
            print(f"[AstroIA] Objeto omitido ({obj.slug}): {type(exc).__name__}: {exc}")
            continue
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
        "location": {
            "latitude": latitude,
            "longitude": longitude,
            "assumed": assumed,
            "label": place["label"],
            "source": place["source"],
        },
        "weather": weather,
        "moon": moon,
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
