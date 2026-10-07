from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    port: int = 8000
    database_url: str = "sqlite:///./astroia.db"
    jwt_secret: str = "astroia-dev-secret-cambia-esto"
    nasa_api_key: str = "DEMO_KEY"
    groq_api_key: str = ""
    cors_origins: str = (
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"
    )

    @property
    def cors_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
