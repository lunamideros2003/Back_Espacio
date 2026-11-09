from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.auth import create_token, decode_token, hash_password, public_user, verify_password


def test_password_roundtrip():
    stored = hash_password("astroia123")
    assert stored != "astroia123"
    assert verify_password("astroia123", stored) is True
    assert verify_password("wrong", stored) is False


def test_password_rejects_malformed_hash():
    assert verify_password("astroia123", "not-a-hash") is False


def test_token_roundtrip():
    user = SimpleNamespace(id=7, email="luna@astroia.dev", name="Luna", level="beginner")
    token = create_token(user)
    payload = decode_token(token)
    assert payload["id"] == 7
    assert payload["email"] == "luna@astroia.dev"


def test_invalid_token_raises_401():
    with pytest.raises(HTTPException) as error:
        decode_token("not-a-token")
    assert error.value.status_code == 401


def test_public_user_hides_password():
    user = SimpleNamespace(
        id=1,
        name="Luna",
        email="luna@astroia.dev",
        level="beginner",
        latitude=4.7,
        longitude=-74.1,
        city="Bogotá",
        password_hash="secret",
    )
    data = public_user(user)
    assert "password_hash" not in data
    assert data["city"] == "Bogotá"
