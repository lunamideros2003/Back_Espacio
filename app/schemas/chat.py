from pydantic import BaseModel


class ChatIn(BaseModel):
    message: str
    history: list[dict] = []
    level: str | None = None


class ClassifyIn(BaseModel):
    brightness: int = 3
    color: str = "white"
    moving: str = "no"
    shape: str = "point"
