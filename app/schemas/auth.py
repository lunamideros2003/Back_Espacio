from pydantic import BaseModel, field_validator

from app.validation import is_valid_email, is_valid_name, is_valid_password, normalize_email


class RegisterIn(BaseModel):
    name: str
    email: str
    password: str
    level: str = "beginner"
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not is_valid_name(value):
            raise ValueError("Escribe tu nombre (al menos 2 letras)")
        return value.strip()

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if not is_valid_email(value):
            raise ValueError("Escribe un correo válido con @ y dominio, por ejemplo nombre@correo.com")
        return normalize_email(value)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not is_valid_password(value):
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return value


class LoginIn(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if not is_valid_email(value):
            raise ValueError("Escribe un correo válido con @ y dominio, por ejemplo nombre@correo.com")
        return normalize_email(value)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not (value or "").strip():
            raise ValueError("Escribe tu contraseña")
        return value


class ProfileIn(BaseModel):
    name: str | None = None
    level: str | None = None
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None
