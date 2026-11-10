from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


def engine_options_for(url: str) -> dict:
    sqlite = url.startswith("sqlite")
    options = {
        "connect_args": {"check_same_thread": False} if sqlite else {},
        "pool_pre_ping": True,
    }
    if not sqlite:
        options.update({"pool_recycle": 1800, "pool_size": 5, "max_overflow": 5, "pool_timeout": settings.db_pool_timeout})
    return options


IS_SQLITE = settings.database_url.startswith("sqlite")
engine = create_engine(settings.database_url, **engine_options_for(settings.database_url))
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def database_target(url=None) -> str:
    target = url or getattr(engine, "url", None)
    if target is None:
        return "desconocida"
    render = getattr(target, "render_as_string", None)
    return render(hide_password=True) if render else str(target)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
