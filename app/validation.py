import re

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")


def normalize_email(value: str | None) -> str:
    return (value or "").strip().lower()


def is_valid_email(value: str | None) -> bool:
    return bool(EMAIL_PATTERN.match(normalize_email(value)))
