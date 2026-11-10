import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_astroia.db")
os.environ.setdefault("AUTO_CREATE_TABLES", "1")
os.environ.setdefault("JWT_SECRET", "test-secret")
