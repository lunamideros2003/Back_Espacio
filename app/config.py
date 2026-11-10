from urllib.parse import quote_plus

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_ORIGINS = (
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "https://fron-espacio.vercel.app",
)


def normalize_origin(raw: str) -> str:
    origin = raw.strip().strip('"').strip("'").rstrip("/").lower()
    return origin if origin.startswith(("http://", "https://")) else ""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    port: int = 8000
    database_url: str = "sqlite:///./astroia.db"
    auto_create_tables: bool = True
    db_pool_timeout: int = 30
    jwt_secret: str = "astroia-dev-secret-cambia-esto"
    nasa_api_key: str = "DEMO_KEY"
    groq_api_key: str = ""
    gemini_api_key: str = ""
    supabase_url: str = ""
    supabase_publishable_key: str = ""
    supabase_secret_key: str = ""
    supabase_jwks_url: str = ""
    supabase_db_host: str = ""
    supabase_db_port: int = 5432
    supabase_db_name: str = "postgres"
    supabase_db_user: str = ""
    supabase_db_password: str = ""
    ai_provider: str = "auto"
    gemini_model: str = "gemini-3.5-flash"
    cors_origins: str = ""

    @field_validator("database_url")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        url = (value or "").strip()
        if url.startswith("postgres://"):
            url = "postgresql://" + url[len("postgres://") :]
        if url.startswith("postgresql://"):
            url = "postgresql+psycopg2://" + url[len("postgresql://") :]
        return url

    @model_validator(mode="after")
    def build_supabase_database_url(self):
        if not (self.supabase_db_host and self.supabase_db_user and self.supabase_db_password):
            return self
        if not self.database_url.startswith("sqlite"):
            return self
        host = self.supabase_db_host.strip().removeprefix("https://").removeprefix("http://").strip("/")
        user = quote_plus(self.supabase_db_user.strip())
        password = quote_plus(self.supabase_db_password)
        name = self.supabase_db_name.strip("/ ") or "postgres"
        self.database_url = (
            f"postgresql+psycopg2://{user}:{password}@{host}:{self.supabase_db_port}/{name}?sslmode=require"
        )
        return self

    @property
    def uses_supabase(self) -> bool:
        return "supabase." in self.database_url or "supabase.co" in self.database_url

    @property
    def cors_list(self) -> list[str]:
        seen: dict[str, None] = {}
        for raw in list(DEFAULT_ORIGINS) + self.cors_origins.split(","):
            origin = normalize_origin(raw)
            if origin:
                seen.setdefault(origin)
        return list(seen)


settings = Settings()

