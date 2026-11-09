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


def test_supabase_parts_build_the_database_url():
    configured = Settings(
        supabase_db_host="aws-1-us-west-2.pooler.supabase.com",
        supabase_db_port=6543,
        supabase_db_user="postgres.abcdefgh",
        supabase_db_password="secreto",
    )
    assert configured.database_url == (
        "postgresql://postgres.abcdefgh:secreto@aws-1-us-west-2.pooler.supabase.com:6543/postgres?sslmode=require"
    )
    assert configured.uses_supabase is True


def test_supabase_password_is_url_encoded():
    configured = Settings(
        supabase_db_host="host.supabase.co",
        supabase_db_user="postgres.abc",
        supabase_db_password="p@ss:#/1",
    )
    assert "p%40ss%3A%23%2F1" in configured.database_url


def test_explicit_database_url_wins_over_parts():
    configured = Settings(
        database_url="postgresql://user:pass@host:5432/postgres",
        supabase_db_host="other.supabase.co",
        supabase_db_user="postgres.abc",
        supabase_db_password="secreto",
    )
    assert configured.database_url == "postgresql://user:pass@host:5432/postgres"


def test_cors_list_always_includes_defaults():
    assert settings.cors_list == list(dict.fromkeys(normalize_origin(origin) for origin in DEFAULT_ORIGINS))
