"""App factory — builds and configures the Flask application."""

import logging
import os
from logging.config import dictConfig

from flask import Flask

from app.config import DevelopmentConfig, ProductionConfig, TestingConfig

CONFIG_MAP = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def configure_logging() -> None:
    """Structured JSON-line logging. In dev, plain-text for readability."""
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
    """Build and return the Flask application."""
    flask_env = env or os.getenv("FLASK_ENV", "development")
    config_class = CONFIG_MAP.get(flask_env, DevelopmentConfig)

    configure_logging()

    app = Flask(__name__)
    app.config.from_object(config_class)

    # ── Attach extensions ──
    from app.extensions import bcrypt, cors, db, limiter, migrate, socketio, talisman

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins="*")
    limiter.init_app(app)

    if app.config.get("DEBUG", False):
        cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    else:
        cors.init_app(app)

    if not app.config.get("DEBUG", False) and not app.config.get("TESTING", False):
        talisman.init_app(app, content_security_policy=None, force_https=False)

    # ── Swagger / Flasgger ──
    from flasgger import Swagger

    swagger_config = app.config.get("SWAGGER", {})
    Swagger(app, template=swagger_config.get("template", {}), config=swagger_config)

    # =====================================================================
    # BLUEPRINTS — add import + register line per module as you build them
    # =====================================================================
    from app.modules.health.routes import health_bp        # Step 0.12
    from app.modules.items.routes import items_bp   

    app.register_blueprint(health_bp)
    app.register_blueprint(items_bp)
    # NEW_BLUEPRINT_IMPORT   ← add blueprint imports above this line
    # NEW_BLUEPRINT_REGISTER ← add app.register_blueprint() above this line

    # =====================================================================
    # GLOBAL HOOKS — uncomment each block as you build it
    # =====================================================================
    # (Step 4.1) from app.common.errors import register_error_handlers
    # (Step 4.1) register_error_handlers(app)
    # (Step 6.2) from app.common.auth import require_api_key
    # (Step 6.2) app.before_request(require_api_key)
    # (Step 8.1) from app.common.response_wrapper import wrap_response
    # (Step 8.1) app.after_request(wrap_response)

    # =====================================================================
    # WEBSOCKET EVENTS — uncomment when you build it
    # =====================================================================
    # (Step 9.1) from app.modules.websocket import events  # noqa: F401


    # ── Model discovery for Flask-Migrate ──
    from app.modules.items import models




    # (Step 5.1) from app.modules.users import models    # noqa: F401
    # NEW_MODEL_IMPORT ← add model imports above this line (after all blueprints)

    app.extensions["bcrypt"] = bcrypt
    return app