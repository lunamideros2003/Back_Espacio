from sqlalchemy.engine import make_url

from app.database import database_target, engine_options_for


def test_sqlite_engine_options():
    options = engine_options_for("sqlite:///./astroia.db")
    assert options["connect_args"] == {"check_same_thread": False}
    assert options["pool_pre_ping"] is True
    assert "pool_size" not in options


def test_postgres_engine_options():
    options = engine_options_for("postgresql://user:pass@host:6543/postgres")
    assert options["connect_args"] == {}
    assert options["pool_pre_ping"] is True
    assert options["pool_size"] == 5
    assert options["max_overflow"] == 5
    assert options["pool_recycle"] == 1800
    assert options["pool_timeout"] > 0


def test_database_target_hides_the_password():
    url = make_url("postgresql://postgres.abc:secreto@host.supabase.com:6543/postgres")
    target = database_target(url)
    assert "secreto" not in target
    assert "postgres.abc" in target
    assert "host.supabase.com" in target
