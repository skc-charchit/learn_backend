import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    APP_NAME: str = "Learn Backend"
    DEBUG: bool = True
    SKIP_DB_INIT: bool = False
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/learn_backend"
    )


settings = Settings()
