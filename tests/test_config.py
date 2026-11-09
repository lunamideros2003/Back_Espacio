from app.config import DEFAULT_ORIGINS, Settings, normalize_origin, settings


def test_normalize_origin_cleans_and_lowercases():
    assert normalize_origin("  https://Fron-Espacio.Vercel.App/ ") == "https://fron-espacio.vercel.app"
    assert normalize_origin("'http://localhost:5173/'") == "http://localhost:5173"


def test_normalize_origin_rejects_non_http_values():
    assert normalize_origin("") == ""
    assert normalize_origin("vercel.app") == ""


def test_postgres_scheme_is_normalized():
    configured = Settings(database_url="postgres://user:pass@host:6543/postgres")
    assert configured.database_url == "postgresql://user:pass@host:6543/postgres"


def test_cors_list_always_includes_defaults():
    assert settings.cors_list == list(dict.fromkeys(normalize_origin(origin) for origin in DEFAULT_ORIGINS))
