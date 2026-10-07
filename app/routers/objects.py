from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth import get_current_user_optional
from app.database import get_db
from app.models import CelestialObject, User
from app.services.nasa import search_nasa_image

router = APIRouter(prefix="/api/objects", tags=["objects"])


def serialize_object(obj: CelestialObject) -> dict:
    return {
        "id": obj.id,
        "slug": obj.slug,
        "name": obj.name,
        "type": obj.type,
        "constellation": obj.constellation,
        "magnitude": obj.magnitude,
        "raHours": obj.ra_hours,
        "decDeg": obj.dec_deg,
        "distance": obj.distance,
        "diameter": obj.diameter,
        "funFact": obj.fun_fact,
        "explainBeginner": obj.explain_beginner,
        "explainMedium": obj.explain_medium,
        "explainAdvanced": obj.explain_advanced,
        "imageQuery": obj.image_query,
        "tags": obj.tags,
        "bestMonths": obj.best_months,
        "astronomyBody": obj.astronomy_body,
    }


@router.get("")
def list_objects(
    type: str | None = None,
    q: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(CelestialObject)
    if type:
        query = query.filter(CelestialObject.type == type)
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                CelestialObject.name.ilike(like),
                CelestialObject.tags.ilike(like),
                CelestialObject.constellation.ilike(like),
            )
        )
    objects = query.order_by(CelestialObject.name.asc()).all()
    return {"objects": [serialize_object(o) for o in objects]}


@router.get("/{slug}")
async def get_object(
    slug: str,
    level: str | None = Query(None),
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    obj = db.query(CelestialObject).filter(CelestialObject.slug == slug).first()
    if not obj:
        raise HTTPException(404, "Objeto no encontrado")
    chosen = level or (user.level if user else "beginner")
    explanation = {
        "advanced": obj.explain_advanced,
        "intermediate": obj.explain_medium,
    }.get(chosen, obj.explain_beginner)
    image_url = None
    try:
        image_url = await search_nasa_image(obj.image_query or obj.name)
    except Exception:
        image_url = None
    return {
        "object": serialize_object(obj),
        "explanation": explanation,
        "level": chosen,
        "imageUrl": image_url,
    }
