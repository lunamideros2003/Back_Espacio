from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

IS_SQLITE = settings.database_url.startswith("sqlite")

engine_options = {
    "connect_args": {"check_same_thread": False} if IS_SQLITE else {},
    "pool_pre_ping": True,
}

if not IS_SQLITE:
    # Supabase closes idle connections; recycling keeps the pool healthy.
    engine_options.update({"pool_recycle": 1800, "pool_size": 5, "max_overflow": 5})

engine = create_engine(settings.database_url, **engine_options)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
