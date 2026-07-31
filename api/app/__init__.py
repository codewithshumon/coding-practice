"""App factory — builds and configures the Flask application.

Every environment (dev, test, prod) calls create_app() with different config.
"""

import logging
from logging.config import dictConfig
from pathlib import Path

from flask import Flask

from app.config import DevelopmentConfig, ProductionConfig, TestingConfig

# Map FLASK_ENV to config class
CONFIG_MAP = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def configure_logging() -> None:
    """Structured JSON-line logging. In dev, plain-text for readability."""
    import os

    is_prod = os.getenv("FLASK_ENV") == "production"
    handler_class = "logging.StreamHandler"

    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json" if is_prod else "plain": {
                "()": "logging.Formatter",
                "format": (
                    '{"time":"%(asctime)s","level":"%(levelname)s",'
                    '"name":"%(name)s","message":"%(message)s"}'
                    if is_prod
                    else "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"
                ),
            },
        },
        "handlers": {
            "console": {
                "class": handler_class,
                "formatter": "json" if is_prod else "plain",
            },
        },
        "root": {"level": "INFO", "handlers": ["console"]},
    })


def create_app(env: str | None = None):
    """Build and return the Flask application.

    Args:
        env: 'development' | 'testing' | 'production'.
             Defaults to FLASK_ENV env var, falling back to 'development'.
    """
    import os

    flask_env = env or os.getenv("FLASK_ENV", "development")
    config_class = CONFIG_MAP.get(flask_env, DevelopmentConfig)

    configure_logging()

    app = Flask(__name__)
    app.config.from_object(config_class)

    # ── Attach extensions (the "two-phase" init pattern) ──
    from app.extensions import bcrypt, cors, db, limiter, migrate, socketio, talisman

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins="*")
    limiter.init_app(app)

    # CORS — allow all origins in dev, lock down in prod
    if app.config.get("DEBUG", False):
        cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    else:
        cors.init_app(app)

    # Talisman — security headers (only in production)
    if not app.config.get("DEBUG", False) and not app.config.get("TESTING", False):
        talisman.init_app(
            app,
            content_security_policy=None,
            force_https=False,  # set True behind a real load balancer
        )

    # ── Register blueprints (each module's routes) ──
    from app.modules.health.routes import health_bp
    from app.modules.items.routes import items_bp
    from app.modules.users.routes import users_bp
    from app.modules.demo.routes import demo_bp
    from app.modules.formfiles.routes import formfiles_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(demo_bp)
    app.register_blueprint(formfiles_bp)

    # ── Register global hooks ──
    from app.common.errors import register_error_handlers
    from app.common.auth import require_api_key
    from app.common.response_wrapper import wrap_response

    register_error_handlers(app)
    app.before_request(require_api_key)
    app.after_request(wrap_response)

    # ── Register WebSocket events (import for side-effects) ──
    from app.modules.websocket import events  # noqa: F401

    # ── Make extensions accessible as app.extensions for shell/scripts ──
    app.extensions["bcrypt"] = bcrypt

    return app