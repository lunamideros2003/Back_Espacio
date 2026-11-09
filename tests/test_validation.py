from app.validation import is_valid_email, normalize_email


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
