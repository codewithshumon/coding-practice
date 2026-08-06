import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Settings shared by all environments."""
    # ── Flask ──
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me")
    PORT: int = int(os.getenv("PORT", "5000"))

    # ── Database ──
    SQLALCHEMY_DATABASE_URI: str = (
        f"postgresql://"
        f"{os.getenv('DATABASE_USER', 'flask')}:"
        f"{os.getenv('DATABASE_PASSWORD', 'flask')}@"
        f"{os.getenv('DATABASE_HOST', 'localhost')}:"
        f"{os.getenv('DATABASE_PORT', '5600')}/"
        f"{os.getenv('DATABASE_NAME', 'flask_learn')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # ── Auth ──
    API_KEY: str = os.getenv("API_KEY", "dev-api-key")
    ADMIN_API_KEY: str = os.getenv("ADMIN_API_KEY", "dev-admin-key")

    # ── Celery ──
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

    # ── Rate Limiting ──
    RATELIMIT_STORAGE_URI: str = os.getenv("RATELIMIT_STORAGE_URI", "memory://")
    RATELIMIT_DEFAULT: str = "200 per day;50 per hour"

    # ── Swagger / Flasgger ──
    SWAGGER: dict = {
        "title": "Flask Learning API",
        "description": "Production-grade Flask REST API — all routes except /health require X-API-Key header.",
        "version": "0.1.0",
        "uiversion": 3,
        "static_url_path": "/flasgger_static",
        "openapi": "3.0.2",
        "specs_route": "/apidocs/",
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
            },
        ],
        "headers": [],
    }


class DevelopmentConfig(BaseConfig):
    """Local dev — verbose errors, auto-reload."""
    DEBUG: bool = True
    TESTING: bool = False


class TestingConfig(BaseConfig):
    """pytest — SQLite in-memory, no auth required."""
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"
    API_KEY: str = "test-key"
    ADMIN_API_KEY: str = "test-admin-key"
    RATELIMIT_ENABLED: bool = False


class ProductionConfig(BaseConfig):
    """Deployed — no debug, strict security."""
    DEBUG: bool = False
    TESTING: bool = False
    RATELIMIT_STORAGE_URI: str = os.getenv("RATELIMIT_STORAGE_URI", "redis://redis:6379/1")