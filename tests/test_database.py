from app.database import engine_options_for


def test_sqlite_engine_options():
    options = engine_options_for("sqlite:///./astroia.db")
    assert options["connect_args"] == {"check_same_thread": False}
    assert options["pool_pre_ping"] is True
    assert "pool_size" not in options
