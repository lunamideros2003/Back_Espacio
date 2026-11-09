from app.validation import is_valid_email, is_valid_name, is_valid_password, normalize_email


def test_email_requires_at_and_domain():
    assert is_valid_email("luna@astroia.dev") is True
    assert is_valid_email("luna.astroia.dev") is False
    assert is_valid_email("luna@astroia") is False
    assert is_valid_email("luna@astroia.") is False
    assert is_valid_email("") is False


def test_email_is_normalized():
    assert normalize_email("  Luna@AstroIA.dev ") == "luna@astroia.dev"


def test_email_rejects_spaces():
    assert is_valid_email("lu na@astroia.dev") is False
    assert is_valid_email("luna @astroia.dev") is False


def test_password_requires_eight_characters():
    assert is_valid_password("astroia123") is True
    assert is_valid_password("astroia") is False
    assert is_valid_password("") is False
    assert is_valid_password("        ") is False


def test_name_requires_two_letters():
    assert is_valid_name("Luna") is True
    assert is_valid_name(" Lu ") is True
    assert is_valid_name("L") is False
    assert is_valid_name(None) is False
