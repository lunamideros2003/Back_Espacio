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
