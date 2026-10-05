from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """ typed configuration: read from .env """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://snip:snip@localhost:5432/snip"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str  # mandatory : app won't run without it
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60
    cors_origins: list[str] = ["http://localhost:3000"]
    public_base_url: str = "http://localhost:8000"
    link_cache_ttl_seconds: int = 3600
    create_rate_limit_per_minute: int = 10

settings = Settings()