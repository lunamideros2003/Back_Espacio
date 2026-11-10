import re

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")
PASSWORD_MIN_LENGTH = 8
NAME_MIN_LENGTH = 2


def normalize_email(value: str | None) -> str:
    return (value or "").strip().lower()


def is_valid_email(value: str | None) -> bool:
    return bool(EMAIL_PATTERN.match(normalize_email(value)))


def is_valid_password(value: str | None) -> bool:
    return len((value or "").strip()) >= PASSWORD_MIN_LENGTH


def is_valid_name(value: str | None) -> bool:
    return len((value or "").strip()) >= NAME_MIN_LENGTH


FIELD_LABELS = {"name": "nombre", "email": "correo", "password": "contraseña"}


def validation_message(errors: list[dict] | None) -> str:
    if not errors:
        return "Revisa los datos del formulario."
    first = errors[0]
    raw = str(first.get("msg") or "").replace("Value error, ", "").strip()
    loc = first.get("loc") or ()
    field = str(loc[-1]) if loc else ""
    if raw and raw != "Field required":
        return raw
    label = FIELD_LABELS.get(field, field or "formulario")
    return f"Revisa el campo {label}."
