from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth import create_token, get_current_user, hash_password, public_user, verify_password
from app.database import get_db
from app.models import User

router = APIRouter(prefix="/api/auth", tags=["auth"])


class RegisterIn(BaseModel):
    name: str
    email: str
    password: str
    level: str = "beginner"
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class LoginIn(BaseModel):
    email: str
    password: str


class ProfileIn(BaseModel):
    name: str | None = None
    level: str | None = None
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None


@router.post("/register")
def register(body: RegisterIn, db: Session = Depends(get_db)):
    email = body.email.lower().strip()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(409, "Ese correo ya está registrado")
    if not body.name or not body.password:
        raise HTTPException(400, "Nombre, correo y contraseña son obligatorios")
    level = body.level if body.level in {"beginner", "intermediate", "advanced"} else "beginner"
    user = User(
        name=body.name,
        email=email,
        password_hash=hash_password(body.password),
        level=level,
        city=body.city,
        latitude=body.latitude,
        longitude=body.longitude,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"token": create_token(user), "user": public_user(user)}


@router.post("/login")
def login(body: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email.lower().strip()).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(401, "Correo o contraseña incorrectos")
    return {"token": create_token(user), "user": public_user(user)}


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"user": public_user(user)}


@router.patch("/me")
def update_me(body: ProfileIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if body.name:
        user.name = body.name
    if body.level:
        user.level = body.level
    if body.city is not None:
        user.city = body.city
    if body.latitude is not None:
        user.latitude = body.latitude
    if body.longitude is not None:
        user.longitude = body.longitude
    db.commit()
    db.refresh(user)
    return {"user": public_user(user), "token": create_token(user)}
