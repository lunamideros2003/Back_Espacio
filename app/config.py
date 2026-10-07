from pydantic_settings import BaseSettings, SettingsConfigDict

# Origenes que SIEMPRE se permiten, aunque la variable de entorno
# no exista o este mal escrita. Cubre desarrollo y el despliegue en Vercel.
DEFAULT_ORIGINS = (
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "https://fron-espacio.vercel.app",
)


def normalize_origin(raw: str) -> str:
    """Limpia espacios, saltos de linea y barra final: 'https://x.vercel.app/ ' -> 'https://x.vercel.app'"""
    origin = raw.strip().strip('"').strip("'").rstrip("/").lower()
    return origin if origin.startswith(("http://", "https://")) else ""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    port: int = 8000
    database_url: str = "sqlite:///./astroia.db"
    jwt_secret: str = "astroia-dev-secret-cambia-esto"
    nasa_api_key: str = "DEMO_KEY"
    groq_api_key: str = ""
    gemini_api_key: str = ""
    # auto | groq | gemini | local
    ai_provider: str = "auto"
    gemini_model: str = "gemini-3.5-flash"
    # Origenes extra separados por coma. Se SUMAN a DEFAULT_ORIGINS.
    cors_origins: str = ""

    @property
    def cors_list(self) -> list[str]:
        seen: dict[str, None] = {}
        for raw in list(DEFAULT_ORIGINS) + self.cors_origins.split(","):
            origin = normalize_origin(raw)
            if origin:
                seen.setdefault(origin)
        return list(seen)


settings = Settings()
