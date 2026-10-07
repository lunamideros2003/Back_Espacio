from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth import get_current_user_optional
from app.database import get_db
from app.models import CelestialObject, ChatMessage, User
from app.routers.objects import serialize_object
from app.services.ai import chat_with_astroia, classify_description

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatIn(BaseModel):
    message: str
    history: list[dict] = []
    level: str | None = None


class ClassifyIn(BaseModel):
    brightness: int = 3
    color: str = "white"
    moving: str = "no"
    shape: str = "point"


@router.post("")
async def chat(
    body: ChatIn,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    if not body.message:
        raise HTTPException(400, "Escribe un mensaje")
    objects = db.query(CelestialObject).all()
    level = body.level or (user.level if user else "beginner")
    result = await chat_with_astroia(body.message, objects, level, body.history)
    db.add(ChatMessage(user_id=user.id if user else None, role="user", content=body.message[:2000]))
    db.add(ChatMessage(user_id=user.id if user else None, role="assistant", content=result["reply"]))
    db.commit()
    return {**result, "level": level}


@router.post("/classify")
def classify(body: ClassifyIn, db: Session = Depends(get_db)):
    result = classify_description(body.brightness, body.color, body.moving, body.shape)
    similar_type = "phenomenon" if result["type"] == "satellite" else result["type"]
    similar = db.query(CelestialObject).filter(CelestialObject.type == similar_type).limit(4).all()
    return {**result, "similar": [serialize_object(o) for o in similar]}
