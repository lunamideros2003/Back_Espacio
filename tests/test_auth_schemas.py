import pytest
from pydantic import ValidationError

from app.schemas.auth import LoginIn, ProfileIn, RegisterIn


def test_register_normalizes_email():
    data = RegisterIn(name="Luna", email="  LUNA@AstroIA.dev ", password="astroia123")
    assert data.email == "luna@astroia.dev"
    assert data.name == "Luna"


def test_register_rejects_email_without_at():
    with pytest.raises(ValidationError) as error:
        RegisterIn(name="Luna", email="luna.astroia.dev", password="astroia123")
    assert "correo" in str(error.value).lower()


def test_register_rejects_short_password():
    with pytest.raises(ValidationError) as error:
        RegisterIn(name="Luna", email="luna@astroia.dev", password="corta")
    assert "8 caracteres" in str(error.value)


def test_register_rejects_empty_name():
    with pytest.raises(ValidationError) as error:
        RegisterIn(name=" ", email="luna@astroia.dev", password="astroia123")
    assert "nombre" in str(error.value).lower()


def test_login_requires_at_in_email():
    with pytest.raises(ValidationError):
        LoginIn(email="luna.astroia.dev", password="astroia123")


def test_login_normalizes_email():
    assert LoginIn(email="LUNA@AstroIA.dev", password="astroia123").email == "luna@astroia.dev"


def test_login_requires_password():
    with pytest.raises(ValidationError):
        LoginIn(email="luna@astroia.dev", password="   ")


def test_profile_name_is_optional():
    assert ProfileIn().name is None
    assert ProfileIn(name=" Luna ").name == "Luna"


def test_profile_rejects_short_name():
    with pytest.raises(ValidationError):
        ProfileIn(name="L")
