from pydantic import BaseModel


class LogIn(BaseModel):
    objectSlug: str
    notes: str | None = None
    visible: bool = True
