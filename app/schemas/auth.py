from pydantic import BaseModel


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
