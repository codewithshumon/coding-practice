"""
Application configuration — reads from .env file and environment variables.

Install pydantic-settings first:
    pip install pydantic-settings
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """All config values have sensible defaults. Override via .env or env vars."""

    # Server
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = False

    # App
    title: str = "FastAPI Learning Lab"
    version: str = "1.0.0"
    environment: str = "development"

    class Config:
        env_file = ".env"        # reads .env file automatically
        env_file_encoding = "utf-8"


# Create a single global instance — import this everywhere.
settings = Settings()
