# Flask Learning Lab — Step-by-Step Task Checklist (Production-Grade)

> **How to use:** Each step creates ONE file (or a small, related group). Work top to bottom.
> After every step, test with curl or browser. **Never skip a step** — each one builds on the last.

---

## Phase 0 — Project Scaffold (Production-Grade Foundation)

Everything starts here. By the end of Phase 0 you'll have a proper app factory, separate config classes per environment, all extensions in one file, a wsgi entry point for gunicorn, and a working health-check route.

---

### Step 0.1: Create the full folder structure

```bash
mkdir -p api/app/common/{models,utils}
mkdir -p api/app/modules
mkdir -p api/tests
mkdir -p api/uploads
```

**Why now:** Every file you create in later steps already has a home. No `mkdir` mid-build.

---

### Step 0.2: Create `.gitignore`

**Where:** `api/.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/

# Virtual environment
.venv/
venv/

# Environment (contains secrets — NEVER commit)
.env

# Uploaded files (dev)
uploads/*

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite3

# Migrations (commit these in real projects, but we regenerate during learning)
# In production: REMOVE this line — migrations ARE committed
migrations/versions/*
!migrations/versions/.gitkeep

# pytest
.pytest_cache/
htmlcov/
.coverage
```

**Why each section:**
- `.env` is gitignored — it holds real secrets. You'll create `.env.example` as a template.
- `migrations/versions/*` is gitignored here for learning. **In real production you commit these.**
- `uploads/*` — dev uploads shouldn't be in git.

---

### Step 0.3: Create `pyproject.toml` with ALL dependencies

**Where:** `api/pyproject.toml`

```toml
[project]
name = "flask-learning-api"
version = "0.1.0"
description = "Production-grade Flask REST API — learning lab"
requires-python = ">=3.11"
dependencies = [
    "flask>=3.1",
    "flask-sqlalchemy>=3.1",
    "psycopg2-binary>=2.9",
    "python-dotenv>=1.0",
    "pydantic[email]>=2.5",
    "flask-pydantic>=0.12",
    "flask-bcrypt>=1.0",
    "flask-socketio>=5.3",
    "flasgger>=0.9",
    "flask-migrate>=4.0",
    "flask-cors>=5.0",
    "flask-talisman>=1.1",
    "flask-limiter>=3.5",
    "gunicorn>=22.0",
    "celery[redis]>=5.4",
    "redis>=5.0",
    "email-validator>=2.1",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-flask>=1.3",
    "httpx>=0.27",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

**Why `pyproject.toml` not `requirements.txt`:**
- It's the modern Python packaging standard (PEP 621).
- Dependency groups (`dev`) keep test tools separate from production installs.
- A single file replaces `requirements.txt` + `requirements-dev.txt` + `setup.cfg`.

---

### Step 0.4: Create `.flaskenv`

**Where:** `api/.flaskenv`

```
FLASK_APP=run.py
FLASK_DEBUG=1
```

**Why:** The `flask` CLI (e.g. `flask run`, `flask db migrate`) auto-loads these. No need to set env vars manually every time.

---

### Step 0.5: Create `.env` (dev secrets)

**Where:** `api/.env`

```
FLASK_ENV=development
SECRET_KEY=change-me-in-production-abc123
PORT=5000
```

**Why:** `.env` holds real values and is gitignored. Only `FLASK_ENV` and `SECRET_KEY` for now — DB creds and API keys come in later phases.

---

### Step 0.6: Create `.env.example` (template for teammates)

**Where:** `api/.env.example`

```
FLASK_ENV=development
SECRET_KEY=change-me
PORT=5000
DATABASE_HOST=localhost
DATABASE_PORT=5600
DATABASE_USER=flask
DATABASE_PASSWORD=flask
DATABASE_NAME=flask_learn
API_KEY=dev-api-key
ADMIN_API_KEY=dev-admin-key
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

**Why:** Teammates copy this to `.env` and fill in real values. Shows every setting the app needs without exposing secrets. This file IS committed to git.

---

### Step 0.7: Create `app/config.py` — multi-environment config classes

**Where:** `api/app/config.py`

```python
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


class DevelopmentConfig(BaseConfig):
    """Local dev — verbose errors, auto-reload."""
    DEBUG: bool = True
    TESTING: bool = False


class TestingConfig(BaseConfig):
    """pytest runs — separate DB, no auth."""
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
```

**Why class hierarchy:** `TestingConfig` uses SQLite in-memory (fast, no Docker needed for tests). `ProductionConfig` disables debug. Each environment extends the base — no duplicated settings.

---

### Step 0.8: Create `app/extensions.py` — all extensions in one place

**Where:** `api/app/extensions.py`

```python
"""All Flask extensions live here — created once, attached via init_app() in the factory.

Why a separate file: avoids circular imports. Models import `db` from here,
routes import `bcrypt` from here — and this file imports nothing from the app itself.
"""

from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
socketio = SocketIO()
cors = CORS()
talisman = Talisman()
limiter = Limiter(key_func=get_remote_address)
```

**Why each extension:**
| Extension | Role |
|-----------|------|
| `SQLAlchemy` | ORM — maps Python classes to Postgres tables |
| `Bcrypt` | Password hashing |
| `Migrate` | Alembic wrapper — generates DB migrations from model changes |
| `SocketIO` | WebSocket support |
| `CORS` | Allows cross-origin requests (SPA frontend calling this API) |
| `Talisman` | Security headers (HSTS, X-Content-Type-Options, etc.) |
| `Limiter` | Rate limiting (prevents abuse) |

---

### Step 0.9: Create `app/__init__.py` — the app factory

**Where:** `api/app/__init__.py`

```python
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
```

**Why this structure:**
- `CONFIG_MAP` picks the right config class based on `FLASK_ENV`.
- Extensions are created in `extensions.py`, attached here — the standard "two-phase init" pattern.
- Blueprints are registered in one place (no hunting through files to find where a route comes from).
- Hooks (`before_request`, `after_request`, error handlers) are registered in order — auth runs first, response wrapper runs last.
- `configure_logging()` uses JSON in production (parseable by CloudWatch/ELK) and plain text in dev.

---

### Step 0.10: Create `wsgi.py` — gunicorn entry point

**Where:** `api/wsgi.py`

```python
"""WSGI entry point for production servers (gunicorn, uWSGI).

Usage:
    gunicorn wsgi:app -c gunicorn.conf.py
"""

from app import create_app

app = create_app()
```

**Why separate from run.py:**
- `run.py` — for `python run.py` (dev, debug, auto-reload).
- `wsgi.py` — for gunicorn (prod). Gunicorn imports `app` from here; no `if __name__` block runs.
- Same `create_app()` call, different entry points for different contexts.

---

### Step 0.11: Create `run.py` — dev server entry point

**Where:** `api/run.py`

```python
"""Development server entry point.

Usage:
    python run.py           # manual
    flask run               # uses .flaskenv
"""

from app import create_app, socketio

app = create_app()

if __name__ == "__main__":
    # Use socketio.run so WebSockets work in dev (flask run doesn't support them)
    socketio.run(app, host="0.0.0.0", port=app.config["PORT"], debug=True)
```

---

### Step 0.12: Create a health-check blueprint (first working route)

**Why:** Before wiring the database, you need a route that proves the app factory + config + Swagger all work.

```bash
mkdir -p api/app/modules/health
touch api/app/modules/health/__init__.py
```

**Where:** `api/app/modules/health/routes.py`

```python
"""Health-check blueprint — proves the app is alive."""

from datetime import datetime, timezone

from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
```

**Note:** The `FormFilesModule` and `WebSocketModule` blueprints won't exist yet — the imports in `app/__init__.py` will fail. For now, **comment out** the lines that import blueprints you haven't created yet:

```python
# In app/__init__.py, comment out imports for blueprints not yet created:
# from app.modules.items.routes import items_bp
# from app.modules.users.routes import users_bp
# from app.modules.demo.routes import demo_bp
# from app.modules.formfiles.routes import formfiles_bp
# app.register_blueprint(items_bp)  ...etc
# from app.modules.websocket import events  # noqa: F401
```

Keep only the `health_bp` import and registration uncommented.

---

### Step 0.13: Install dependencies and verify

```bash
cd api
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Then:
```bash
python run.py
```

Open:
- [http://localhost:5000/health](http://localhost:5000/health) → `{"status":"ok","timestamp":"..."}`
- [http://localhost:5000/apidocs](http://localhost:5000/apidocs) → Swagger UI (mostly empty, one health route)

If you get import errors, make sure only the `health_bp` import is active in `app/__init__.py`.

---

### Step 0.14: Understand the production folder structure so far

```
api/
├── pyproject.toml              ← All deps + tool config
├── .flaskenv                   ← flask CLI auto-loads this
├── .env                        ← Real secrets (gitignored)
├── .env.example                ← Template (committed)
├── .gitignore
├── wsgi.py                     ← Gunicorn entry point (prod)
├── run.py                      ← Dev server entry point
├── uploads/                    ← Dev file uploads
├── tests/                      ← pytest tests (Phase 10)
│
└── app/
    ├── __init__.py             ← app factory: create_app()
    ├── config.py               ← Dev/Test/Prod config classes
    ├── extensions.py           ← db, bcrypt, migrate, socketio, cors, talisman, limiter
    │
    ├── common/
    │   ├── models/base.py      ← (Phase 2)
    │   ├── utils/password.py   ← (Phase 5)
    │   ├── auth.py             ← (Phase 6)
    │   ├── errors.py           ← (Phase 4)
    │   └── response_wrapper.py ← (Phase 8)
    │
    └── modules/
        ├── health/routes.py    ← Health check
        ├── items/              ← (Phase 2)
        ├── users/              ← (Phase 5)
        ├── demo/               ← (Phase 7)
        ├── formfiles/          ← (Phase 7)
        └── websocket/          ← (Phase 9)
```

**Request flow:** Browser → `run.py` → `create_app(env)` → config loaded → extensions init → hooks registered → blueprint routes matched → response

---

## Phase 1 — Docker, Database, Migrations

### Step 1.1: Create `Dockerfile` (multi-stage, production-ready)

**Where:** `api/Dockerfile`

```dockerfile
# ── Stage 1: Build ──
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system deps needed to compile psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir --user -e ".[dev]"

# ── Stage 2: Runtime ──
FROM python:3.12-slim AS runtime

WORKDIR /app

# Only the runtime lib needed (not gcc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home flask && chown -R flask:flask /app
USER flask

EXPOSE 5000

CMD ["gunicorn", "wsgi:app", "-c", "gunicorn.conf.py"]
```

**Why multi-stage:**
- Builder stage has `gcc` for compiling `psycopg2-binary`. Runtime stage doesn't — smaller image, fewer CVEs.
- Non-root `flask` user — container doesn't run as root. Standard security practice.

---

### Step 1.2: Create `docker-compose.yml` (all services)

**Where:** `api/docker-compose.yml`

```yaml
services:
  # ── Flask App ──
  app:
    build: .
    container_name: flask-app
    restart: unless-stopped
    ports:
      - "5000:5000"
    env_file:
      - .env
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./uploads:/app/uploads
      - ./migrations:/app/migrations

  # ── PostgreSQL ──
  postgres:
    image: postgres:16-alpine
    container_name: flask-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: flask
      POSTGRES_PASSWORD: flask
      POSTGRES_DB: flask_learn
    ports:
      - "5600:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U flask -d flask_learn"]
      interval: 5s
      timeout: 5s
      retries: 5

  # ── pgAdmin ──
  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: flask-pgadmin
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5051:80"
    depends_on:
      postgres:
        condition: service_healthy

  # ── Redis (for Celery + rate limiting in production) ──
  redis:
    image: redis:7-alpine
    container_name: flask-redis
    restart: unless-stopped
    ports:
      - "6379:6379"

  # ── Celery Worker ──
  celery:
    build: .
    container_name: flask-celery
    restart: unless-stopped
    command: celery -A app.celery_worker.celery worker --loglevel=info
    env_file:
      - .env
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./uploads:/app/uploads

volumes:
  pgdata:
```

**Port choices (so nothing collides with your other projects):**
| Service | Host Port | Container Port |
|---------|-----------|----------------|
| Flask app | 5000 | 5000 |
| Postgres | 5600 | 5432 |
| pgAdmin | 5051 | 80 |
| Redis | 6379 | 6379 |

---

### Step 1.3: Update `.env` — add full credentials

**Where:** `api/.env`

```
FLASK_ENV=development
SECRET_KEY=dev-secret-key-abc123
PORT=5000
DATABASE_HOST=localhost
DATABASE_PORT=5600
DATABASE_USER=flask
DATABASE_PASSWORD=flask
DATABASE_NAME=flask_learn
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

---

### Step 1.4: Start the database only (app needs more setup first)

```bash
docker compose up -d postgres pgadmin redis
docker compose ps   # verify postgres + pgadmin + redis are healthy
```

---

### Step 1.5: Initialize Flask-Migrate

```bash
flask db init
```

This creates `api/migrations/` — Alembic's version-control for your database schema.

**Why Flask-Migrate instead of `db.create_all()`:**
- `db.create_all()` can only create tables — it can't add a column to an existing table, or rename one.
- Flask-Migrate generates incremental migration scripts. You commit them. Every environment (dev, staging, prod) runs the same scripts in the same order.
- This is how production databases are managed.

---

### Step 1.6: Verify database connection

Make sure `app/__init__.py` has the `db.init_app(app)` and `migrate.init_app(app, db)` calls (they were added in Step 0.9).

```bash
flask shell
```

In the Python shell:
```python
from app.extensions import db
db.engine.connect()    # Should succeed — no error = connected
```

`Ctrl+D` to exit.

If you get `sqlalchemy.exc.OperationalError`, check:
- Postgres container is running (`docker compose ps`)
- `.env` has the correct `DATABASE_HOST=localhost` and `DATABASE_PORT=5600`

---

## Phase 2 — First CRUD (Items) with Proper Migrations

### Step 2.1: Create `app/common/models/base.py`

**Why:** Every table gets `id`, `created_at`, `updated_at`, `deleted_at` for free. Write once, reuse forever.

```python
from datetime import datetime, timezone

from app.extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def to_dict(self):
        """Serialize model to dict, ISO-formatting datetime columns."""
        from datetime import datetime as dt
        return {
            c.name: (
                getattr(self, c.name).isoformat()
                if isinstance(getattr(self, c.name), dt)
                else getattr(self, c.name)
            )
            for c in self.__table__.columns
        }
```

---

### Step 2.2: Create the Item model

**Where:** `api/app/modules/items/models.py`

```bash
touch api/app/modules/items/__init__.py
```

```python
from decimal import Decimal

from app.extensions import db
from app.common.models.base import BaseModel


class Item(BaseModel):
    __tablename__ = "items"

    name = db.Column(db.String(255), nullable=False, index=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    in_stock = db.Column(db.Boolean, nullable=False, default=True, server_default="true")

    def __repr__(self):
        return f"<Item {self.id}: {self.name}>"
```

**Key details:**
- `server_default="true"` — the DEFAULT is set at the database level, not just in Python. Safer for raw SQL inserts.
- `Numeric(10, 2)` — decimal type with fixed precision. Never use `Float` for money.
- `__repr__` — makes debugging in `flask shell` readable.

---

### Step 2.3: Create Pydantic schemas

**Where:** `api/app/modules/items/schemas.py`

```python
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class CreateItemSchema(BaseModel):
    """What the client sends to create an item."""
    model_config = {"extra": "forbid"}  # reject unknown fields

    name: str = Field(..., min_length=1, max_length=255, examples=["Laptop"])
    price: Decimal = Field(..., ge=0, examples=[999.99])
    description: Optional[str] = Field(None, max_length=1000)
    in_stock: Optional[bool] = True


class UpdateItemSchema(BaseModel):
    """All fields optional — only sent fields get updated (PATCH semantics)."""
    model_config = {"extra": "forbid"}

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[Decimal] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=1000)
    in_stock: Optional[bool] = None

    @model_validator(mode="after")
    def at_least_one_field(self):
        """Ensure the client sends at least one field to update."""
        if all(v is None for v in self.__dict__.values()):
            raise ValueError("At least one field must be provided for update")
        return self
```

**Why each piece:**
- `model_config = {"extra": "forbid"}` — rejects unknown fields. Flask's equivalent of NestJS's `forbidNonWhitelisted: true`.
- `ge=0` on `price` — rejects negative prices.
- `@model_validator("after")` on `UpdateItemSchema` — custom validation: reject empty `{}` PATCH requests.

---

### Step 2.4: Create the service layer

**Where:** `api/app/modules/items/service.py`

```python
"""Item business logic — pure Python, no HTTP awareness."""

from datetime import datetime, timezone

from sqlalchemy import select, func

from app.extensions import db
from app.modules.items.models import Item
from app.modules.items.schemas import CreateItemSchema, UpdateItemSchema


class ItemNotFoundError(Exception):
    """Raised when an item ID doesn't exist (or is soft-deleted)."""
    def __init__(self, item_id: int):
        self.item_id = item_id
        super().__init__(f"Item {item_id} not found")


def create_item(data: CreateItemSchema) -> Item:
    item = Item(**data.model_dump(exclude_unset=True))
    db.session.add(item)
    db.session.commit()
    return item


def get_all_items() -> list[Item]:
    return list(
        db.session.scalars(
            select(Item)
            .where(Item.deleted_at.is_(None))
            .order_by(Item.created_at.desc())
        ).all()
    )


def get_item(item_id: int) -> Item:
    item = db.session.get(Item, item_id)
    if item is None or item.deleted_at is not None:
        raise ItemNotFoundError(item_id)
    return item


def update_item(item_id: int, data: UpdateItemSchema) -> Item:
    item = get_item(item_id)  # reuses 404 logic
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.session.commit()
    return item


def delete_item(item_id: int) -> None:
    item = get_item(item_id)
    item.deleted_at = datetime.now(timezone.utc)  # soft delete
    db.session.commit()
```

**Key patterns:**
- Service functions are plain functions (not class methods) — no state, easy to test, easy to import.
- `get_item` reuses itself — `update_item` and `delete_item` call it so 404 logic lives in one place.
- Soft delete — sets `deleted_at`, doesn't actually remove the row.

---

### Step 2.5: Create the routes (blueprint)

**Where:** `api/app/modules/items/routes.py`

```python
from flask import Blueprint, jsonify
from flask_pydantic import validate

from app.modules.items import service
from app.modules.items.schemas import CreateItemSchema, UpdateItemSchema

items_bp = Blueprint("items", __name__, url_prefix="/api/items")


@items_bp.errorhandler(service.ItemNotFoundError)
def handle_not_found(err):
    return jsonify({"error": str(err)}), 404


@items_bp.post("/")
@validate()
def create_item(body: CreateItemSchema):
    item = service.create_item(body)
    return jsonify(item.to_dict()), 201


@items_bp.get("/")
def list_items():
    items = service.get_all_items()
    return jsonify([i.to_dict() for i in items])


@items_bp.get("/<int:item_id>")
def get_item(item_id: int):
    return jsonify(service.get_item(item_id).to_dict())


@items_bp.patch("/<int:item_id>")
@validate()
def update_item(item_id: int, body: UpdateItemSchema):
    return jsonify(service.update_item(item_id, body).to_dict())


@items_bp.delete("/<int:item_id>")
def delete_item(item_id: int):
    service.delete_item(item_id)
    return "", 204
```

**Note the `url_prefix="/api/items"`** — production APIs version their routes under `/api/`. All module prefixes will follow this pattern.

---

### Step 2.6: Register the blueprint and model

In `app/__init__.py`, **uncomment** (or add) these lines:

```python
from app.modules.items.routes import items_bp
app.register_blueprint(items_bp)

# AFTER registering blueprints, import models so Flask-Migrate discovers them:
from app.modules.items import models  # noqa: F401
from app.modules.users import models  # noqa: F401
```

Place the model imports **after** all `register_blueprint()` calls and **before** the `return app`.

---

### Step 2.7: Generate and run your first migration

```bash
flask db migrate -m "create items table"
```

This creates a file like `migrations/versions/abc123_create_items_table.py`. Open it — you'll see `op.create_table('items', ...)` with all your columns.

```bash
flask db upgrade
```

This applies the migration to Postgres. Verify:

```bash
docker exec flask-postgres psql -U flask -d flask_learn -c "\dt"
```

You should see `items`, `alembic_version`, and (if you created the health model) any other tables.

**Why this matters:** In a real project with teammates, you'd commit the migration file. They run `flask db upgrade` and get the exact same schema. No `db.create_all()` guesswork.

---

### Step 2.8: Test full CRUD

```bash
# Create
curl -X POST http://localhost:5000/api/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99}'

curl -X POST http://localhost:5000/api/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Phone", "price": 699.00}'

# List
curl http://localhost:5000/api/items/

# Get one
curl http://localhost:5000/api/items/1

# Update (partial — only name changes, price stays)
curl -X PATCH http://localhost:5000/api/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Gaming Laptop"}'

# Delete (soft)
curl -X DELETE http://localhost:5000/api/items/1

# List again — item 1 is gone from results
curl http://localhost:5000/api/items/

# Open Swagger: http://localhost:5000/apidocs
```

---

### Step 2.9: Check soft delete in the database

```bash
docker exec flask-postgres psql -U flask -d flask_learn -c "SELECT id, name, deleted_at FROM items;"
```

The deleted item still exists — its `deleted_at` is set. `get_all_items()` filters it out.

---

## Phase 3 — Query Parameters & Pagination

### Step 3.1: Add a filter schema

**Where:** `api/app/modules/items/schemas.py` — append to existing file:

```python
class FilterItemSchema(BaseModel):
    """GET query parameters for listing items."""
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)
    name: Optional[str] = Field(None, description="Search by name (case-insensitive ILIKE)")
    max_price: Optional[Decimal] = Field(None, ge=0)
    in_stock: Optional[bool] = None

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
```

**Why no `@Type(() => Number)`:** Pydantic auto-coerces query string `"2"` → `2` and `"true"` → `True`. No manual transformer needed.

---

### Step 3.2: Add filtered query to the service

**Where:** `api/app/modules/items/service.py` — add:

```python
from app.modules.items.schemas import FilterItemSchema  # add to existing imports


def get_filtered_items(filters: FilterItemSchema) -> dict:
    """Paginated, filtered item list."""
    stmt = select(Item).where(Item.deleted_at.is_(None))

    if filters.name:
        stmt = stmt.where(Item.name.ilike(f"%{filters.name}%"))
    if filters.max_price is not None:
        stmt = stmt.where(Item.price <= filters.max_price)
    if filters.in_stock is not None:
        stmt = stmt.where(Item.in_stock == filters.in_stock)

    # Count total before pagination
    total = db.session.scalar(
        select(func.count()).select_from(stmt.subquery())
    )

    # Apply ordering + pagination
    items = db.session.scalars(
        stmt.order_by(Item.created_at.desc())
        .offset(filters.offset)
        .limit(filters.page_size)
    ).all()

    return {
        "items": [i.to_dict() for i in items],
        "total": total,
        "page": filters.page,
        "page_size": filters.page_size,
    }
```

---

### Step 3.3: Update the list route

**Where:** `api/app/modules/items/routes.py` — replace the `list_items` function:

```python
from app.modules.items.schemas import FilterItemSchema  # add to imports


@items_bp.get("/")
@validate()
def list_items(query: FilterItemSchema):
    return jsonify(service.get_filtered_items(query))
```

---

### Step 3.4: Test pagination and filtering

```bash
curl "http://localhost:5000/api/items/?page=1&page_size=2"
curl "http://localhost:5000/api/items/?name=phone"
curl "http://localhost:5000/api/items/?max_price=500&in_stock=true"
curl "http://localhost:5000/api/items/?page_size=200"   # 400 — validation error (>100)
```

---

## Phase 4 — Validation & Error Handling (Global)

### Step 4.1: Create `app/common/errors.py`

**Why:** A single module registers all error handlers on the app — Flask's equivalent of NestJS's global `ValidationPipe`.

```bash
touch api/app/common/__init__.py
```

```python
"""Global error handlers — registered once in create_app()."""

from flask import jsonify
from pydantic import ValidationError


def register_error_handlers(app):
    """Attach all error handlers to the Flask app."""

    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        return jsonify({
            "error": "Validation failed",
            "details": err.errors(),
        }), 400

    @app.errorhandler(400)
    def handle_400(err):
        return jsonify({"error": "Bad request", "details": str(err)}), 400

    @app.errorhandler(404)
    def handle_404(err):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(405)
    def handle_405(err):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def handle_500(err):
        app.logger.exception("Internal server error: %s", err)
        return jsonify({"error": "Internal server error"}), 500
```

In `app/__init__.py`, this is already called (added in Step 0.9):
```python
from app.common.errors import register_error_handlers
register_error_handlers(app)
```

**Why global error handlers:**
- One place for every error shape. No per-blueprint duplication.
- `handle_500` logs the traceback — production-critical for debugging.
- The `ValidationError` handler catches pydantic validation failures from every route.

---

### Step 4.2: Test validation errors

```bash
# Missing required field (price)
curl -X POST http://localhost:5000/api/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": ""}'

# Unknown field (model_config extra="forbid")
curl -X POST http://localhost:5000/api/items/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","price":10,"hacked":true}'

# Non-existent route
curl http://localhost:5000/api/nope
```

All return proper JSON error responses, not HTML 404/500 pages.

---

## Phase 5 — Users Module (Password Hashing)

### Step 5.1: Create the User model

**Where:** `api/app/modules/users/models.py`

```bash
touch api/app/modules/users/__init__.py
```

```python
from app.extensions import db
from app.common.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False, server_default="false")

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"
```

---

### Step 5.2: Create user schemas

**Where:** `api/app/modules/users/schemas.py`

```python
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class CreateUserSchema(BaseModel):
    model_config = {"extra": "forbid"}

    username: str = Field(..., min_length=3, max_length=100, examples=["alice"])
    email: EmailStr = Field(..., examples=["alice@example.com"])
    password: str = Field(..., min_length=8, examples=["password123"])
    is_admin: Optional[bool] = False


class UpdateUserSchema(BaseModel):
    model_config = {"extra": "forbid"}

    username: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    is_admin: Optional[bool] = None
```

---

### Step 5.3: Create password helper

**Where:** `api/app/common/utils/password.py`

```bash
touch api/app/common/utils/__init__.py
```

```python
from app.extensions import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.generate_password_hash(password).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.check_password_hash(hashed, password)
```

---

### Step 5.4: Create the user service

**Where:** `api/app/modules/users/service.py`

```python
from datetime import datetime, timezone

from sqlalchemy import select

from app.extensions import db
from app.common.utils.password import hash_password
from app.modules.users.models import User


class UserNotFoundError(Exception):
    pass


class EmailConflictError(Exception):
    pass


class UsernameConflictError(Exception):
    pass


def create_user(data) -> User:
    # Check uniqueness
    if db.session.scalar(select(User).where(User.email == data.email)):
        raise EmailConflictError("Email already registered")
    if db.session.scalar(select(User).where(User.username == data.username)):
        raise UsernameConflictError("Username already taken")

    fields = data.model_dump(exclude={"password"}, exclude_unset=True)
    user = User(**fields, hashed_password=hash_password(data.password))
    db.session.add(user)
    db.session.commit()
    return user


def get_all_users() -> list[User]:
    return list(
        db.session.scalars(
            select(User).where(User.deleted_at.is_(None))
        ).all()
    )


def get_user(user_id: int) -> User:
    user = db.session.get(User, user_id)
    if user is None or user.deleted_at is not None:
        raise UserNotFoundError(f"User {user_id} not found")
    return user


def update_user(user_id: int, data) -> User:
    user = get_user(user_id)
    fields = data.model_dump(exclude_unset=True)
    if "password" in fields:
        user.hashed_password = hash_password(fields.pop("password"))
    for field, value in fields.items():
        setattr(user, field, value)
    db.session.commit()
    return user


def delete_user(user_id: int) -> None:
    user = get_user(user_id)
    user.deleted_at = datetime.now(timezone.utc)
    db.session.commit()
```

**Why the password dance:** Client sends `password` (plain text). DB stores `hashed_password`. The service hashes between receiving and saving. The plain text password never touches the database.

---

### Step 5.5: Create user routes

**Where:** `api/app/modules/users/routes.py`

```python
from flask import Blueprint, jsonify
from flask_pydantic import validate

from app.modules.users import service
from app.modules.users.schemas import CreateUserSchema, UpdateUserSchema

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.errorhandler(service.UserNotFoundError)
def handle_not_found(err):
    return jsonify({"error": str(err)}), 404


@users_bp.errorhandler(service.EmailConflictError)
def handle_conflict(err):
    return jsonify({"error": str(err)}), 409


@users_bp.errorhandler(service.UsernameConflictError)
def handle_username_conflict(err):
    return jsonify({"error": str(err)}), 409


@users_bp.post("/")
@validate()
def create_user(body: CreateUserSchema):
    user = service.create_user(body)
    return jsonify(user.to_dict()), 201


@users_bp.get("/")
def list_users():
    return jsonify([u.to_dict() for u in service.get_all_users()])


@users_bp.get("/<int:user_id>")
def get_user(user_id: int):
    return jsonify(service.get_user(user_id).to_dict())


@users_bp.patch("/<int:user_id>")
@validate()
def update_user(user_id: int, body: UpdateUserSchema):
    return jsonify(service.update_user(user_id, body).to_dict())


@users_bp.delete("/<int:user_id>")
def delete_user(user_id: int):
    service.delete_user(user_id)
    return "", 204
```

---

### Step 5.6: Register the blueprint and model

In `app/__init__.py`:

```python
from app.modules.users.routes import users_bp
app.register_blueprint(users_bp)

# The model import is already there from Step 2.6:
from app.modules.users import models  # noqa: F401
```

---

### Step 5.7: Generate migration for users table

```bash
flask db migrate -m "create users table"
flask db upgrade
```

---

### Step 5.8: Test

```bash
curl -X POST http://localhost:5000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"password123"}'

# Duplicate email — should get 409
curl -X POST http://localhost:5000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice2","email":"alice@example.com","password":"password123"}'

curl http://localhost:5000/api/users/
```

---

## Phase 6 — API Key Auth (before_request Guard)

### Step 6.1: Update `.env` — add API keys

```
FLASK_ENV=development
SECRET_KEY=dev-secret-key-abc123
PORT=5000
DATABASE_HOST=localhost
DATABASE_PORT=5600
DATABASE_USER=flask
DATABASE_PASSWORD=flask
DATABASE_NAME=flask_learn
API_KEY=dev-api-key
ADMIN_API_KEY=dev-admin-key
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

---

### Step 6.2: Create `app/common/auth.py`

```python
"""API-Key authentication — runs before every request."""

from flask import current_app, g, jsonify, request

# Paths that bypass authentication
EXEMPT_PREFIXES = (
    "/apidocs",
    "/flasgger_static",
    "/apispec",
    "/health",
)


def require_api_key():
    """Before-request hook — checks X-API-Key header.

    Returns None if allowed, or a (response, status) tuple if denied.
    Flask's before_request: returning anything other than None
    cancels the request and returns that value as the response.
    """
    if request.path.startswith(EXEMPT_PREFIXES):
        return None

    api_key = request.headers.get("X-API-Key")
    if not api_key:
        return jsonify({"error": "Missing X-API-Key header"}), 401

    valid_key = current_app.config["API_KEY"]
    admin_key = current_app.config["ADMIN_API_KEY"]

    if api_key in (valid_key, admin_key):
        g.is_admin = api_key == admin_key
        return None

    return jsonify({"error": "Invalid API key"}), 401
```

In `app/__init__.py`, this is already wired (added in Step 0.9):
```python
from app.common.auth import require_api_key
app.before_request(require_api_key)
```

**Why `before_request`:** Flask's equivalent of NestJS's `APP_GUARD` — runs before every route automatically. No decorator needed on every blueprint. `g.is_admin` is available in any route that needs admin-only access.

---

### Step 6.3: Test auth

```bash
# No key — 401
curl http://localhost:5000/api/items/

# Wrong key — 401
curl -H "X-API-Key: wrong" http://localhost:5000/api/items/

# Valid key — 200
curl -H "X-API-Key: dev-api-key" http://localhost:5000/api/items/

# Admin key also works — 200
curl -H "X-API-Key: dev-admin-key" http://localhost:5000/api/items/

# Health endpoint is exempt — no key needed
curl http://localhost:5000/health
```

---

## Phase 7 — Headers, Cookies, Status Codes, Form/Files

### Step 7.1: Create the demo blueprint (headers, cookies, status codes)

**Where:** `api/app/modules/demo/routes.py`

```bash
mkdir -p api/app/modules/demo
touch api/app/modules/demo/__init__.py
```

```python
"""Demo routes — reading/setting headers, cookies, and status codes."""

from flask import Blueprint, jsonify, make_response, redirect, request

demo_bp = Blueprint("demo", __name__, url_prefix="/api/demo")


# ── Headers ──
@demo_bp.get("/whoami")
def whoami():
    return jsonify({
        "user_agent": request.headers.get("User-Agent", "unknown"),
        "host": request.headers.get("Host"),
    })


@demo_bp.get("/set-headers")
def set_headers():
    resp = make_response(jsonify({"message": "Custom header set"}))
    resp.headers["X-Custom-Header"] = "hello-from-flask"
    resp.headers["X-Response-Time"] = "42ms"
    return resp


# ── Cookies ──
@demo_bp.get("/read-cookie")
def read_cookie():
    return jsonify({
        "session_id": request.cookies.get("session_id", "none"),
    })


@demo_bp.get("/set-cookie")
def set_cookie():
    resp = make_response(jsonify({"message": "Cookie set!"}))
    resp.set_cookie(
        "session_id",
        value="abc-123",
        httponly=True,
        secure=False,   # True in production (HTTPS only)
        samesite="Lax",
        max_age=3600,   # 1 hour
    )
    return resp


@demo_bp.get("/delete-cookie")
def delete_cookie():
    resp = make_response(jsonify({"message": "Cookie deleted"}))
    resp.delete_cookie("session_id")
    return resp


# ── Status Codes ──
@demo_bp.post("/created")
def created():
    return jsonify({"id": 1}), 201


@demo_bp.delete("/removed")
def removed():
    return "", 204


@demo_bp.get("/redirect")
def redirect_demo():
    return redirect("/api/items/", code=301)


@demo_bp.get("/not-modified")
def not_modified():
    return "", 304
```

---

### Step 7.2: Create the form-files blueprint

**Where:** `api/app/modules/formfiles/routes.py`

```bash
mkdir -p api/app/modules/formfiles
touch api/app/modules/formfiles/__init__.py
```

```python
"""Form data parsing and file uploads."""

import os
import uuid

from flask import Blueprint, current_app, jsonify, request
from werkzeug.utils import secure_filename

formfiles_bp = Blueprint("formfiles", __name__, url_prefix="/api/form-files")

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "csv"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@formfiles_bp.post("/login")
def login():
    """Parse form-urlencoded body."""
    return jsonify({
        "username": request.form.get("username"),
        "has_password": "password" in request.form,
    })


@formfiles_bp.post("/upload")
def upload():
    """Accept a single file upload."""
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        }), 400

    # Secure the filename + add UUID to prevent collisions
    original = secure_filename(file.filename)
    name, ext = os.path.splitext(original)
    saved_name = f"{name}_{uuid.uuid4().hex[:8]}{ext}"

    upload_dir = os.path.join(current_app.root_path, "..", "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    file.save(os.path.join(upload_dir, saved_name))

    return jsonify({
        "original_filename": file.filename,
        "saved_filename": saved_name,
        "size_bytes": os.path.getsize(os.path.join(upload_dir, saved_name)),
    }), 201
```

---

### Step 7.3: Register both blueprints

In `app/__init__.py`, **uncomment** (or add):

```python
from app.modules.demo.routes import demo_bp
from app.modules.formfiles.routes import formfiles_bp

app.register_blueprint(demo_bp)
app.register_blueprint(formfiles_bp)
```

---

### Step 7.4: Test

```bash
# Headers & cookies
curl -H "X-API-Key: dev-api-key" -H "User-Agent: MyApp" http://localhost:5000/api/demo/whoami
curl -H "X-API-Key: dev-api-key" -b "session_id=test123" http://localhost:5000/api/demo/read-cookie
curl -H "X-API-Key: dev-api-key" -v http://localhost:5000/api/demo/set-cookie 2>&1 | grep -i set-cookie

# Status codes
curl -v -H "X-API-Key: dev-api-key" http://localhost:5000/api/demo/redirect 2>&1 | grep "< HTTP"

# Form data
curl -X POST http://localhost:5000/api/form-files/login \
  -H "X-API-Key: dev-api-key" \
  -d "username=alice&password=pass"

# File upload
echo "test content" > /tmp/test.txt
curl -X POST http://localhost:5000/api/form-files/upload \
  -H "X-API-Key: dev-api-key" \
  -F "file=@/tmp/test.txt"
```

---

## Phase 8 — Response Wrapper (Standardized Envelope)

### Step 8.1: Create `app/common/response_wrapper.py`

```python
"""After-request hook — wraps every JSON success response in a standard envelope."""

from datetime import datetime, timezone

from flask import jsonify, request

SKIP_PREFIXES = ("/apidocs", "/flasgger_static", "/apispec", "/socket.io")


def wrap_response(response):
    """Wrap JSON success responses in {success, data, timestamp}."""
    if request.path.startswith(SKIP_PREFIXES):
        return response

    # Don't wrap non-JSON or error responses
    if response.content_type != "application/json":
        return response
    if response.status_code >= 400:
        return response

    data = response.get_json()
    wrapped = jsonify({
        "success": True,
        "data": data,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    wrapped.status_code = response.status_code
    return wrapped
```

In `app/__init__.py`, this is already wired (added in Step 0.9):
```python
from app.common.response_wrapper import wrap_response
app.after_request(wrap_response)
```

Now every response automatically gets wrapped:
```json
{
  "success": true,
  "data": { "id": 1, "name": "Laptop", "price": "999.99", ... },
  "timestamp": "2026-07-30T12:34:56.789Z"
}
```

---

## Phase 9 — WebSockets

### Step 9.1: Create `app/modules/websocket/events.py`

```bash
mkdir -p api/app/modules/websocket
touch api/app/modules/websocket/__init__.py
```

```python
"""WebSocket event handlers — real-time messaging."""

from datetime import datetime, timezone

from flask import request
from flask_socketio import emit, join_room, leave_room

from app.extensions import socketio

# Track connected clients (in production, use Redis pub/sub for multi-worker)
connected_clients: dict[str, str] = {}


@socketio.on("connect")
def handle_connect():
    connected_clients[request.sid] = request.remote_addr
    print(f"WS connected: {request.sid} from {request.remote_addr}")
    emit("server_message", {
        "type": "connect",
        "sid": request.sid,
        "message": "Welcome!",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


@socketio.on("disconnect")
def handle_disconnect():
    connected_clients.pop(request.sid, None)
    print(f"WS disconnected: {request.sid}")
    emit("server_message", {
        "type": "disconnect",
        "sid": request.sid,
        "message": f"{request.sid} left",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }, broadcast=True)


@socketio.on("message")
def handle_message(payload):
    """Broadcast a chat message to all connected clients."""
    emit("message", {
        "from": request.sid,
        "text": payload if isinstance(payload, str) else payload.get("text", ""),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }, broadcast=True)


@socketio.on("join")
def handle_join(room: str):
    """Join a named room."""
    join_room(room)
    emit("server_message", {
        "type": "join",
        "sid": request.sid,
        "room": room,
        "message": f"Joined room: {room}",
    }, to=request.sid)


@socketio.on("leave")
def handle_leave(room: str):
    """Leave a named room."""
    leave_room(room)
    emit("server_message", {
        "type": "leave",
        "sid": request.sid,
        "room": room,
        "message": f"Left room: {room}",
    }, to=request.sid)
```

In `app/__init__.py`, this is already wired (added in Step 0.9):
```python
from app.modules.websocket import events  # noqa: F401
```

---

### Step 9.2: Test WebSockets

In browser console (open any page on `localhost:5000`):

```js
const socket = io('http://localhost:5000');

socket.on('connect', () => console.log('Connected:', socket.id));

socket.on('server_message', data => console.log('Server:', data));
socket.on('message', data => console.log('Chat:', data));

// Send a chat message
socket.emit('message', 'Hello everyone!');

// Join a room
socket.emit('join', 'room-1');

// Broadcast stays: all clients in room-1 get this
socket.emit('message', {text: 'Hello room-1!'});
```

---

## Phase 10 — Testing, Background Tasks, Security, Production Deploy

### Step 10.1: Create pytest fixtures

**Where:** `api/tests/conftest.py`

```python
"""Shared pytest fixtures — database, test client, sample data."""

import pytest

from app import create_app
from app.extensions import db as _db


@pytest.fixture
def app():
    """Create app with TestingConfig (SQLite in-memory, no auth needed)."""
    _app = create_app(env="testing")

    with _app.app_context():
        _db.create_all()
        yield _app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    """Test client — simulates HTTP requests."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """CLI runner — for testing flask commands."""
    return app.test_cli_runner()


@pytest.fixture
def db(app):
    """Database session for tests."""
    return _db


@pytest.fixture
def api_headers():
    """Default headers including auth key (TestingConfig key)."""
    return {"X-API-Key": "test-key", "Content-Type": "application/json"}
```

---

### Step 10.2: Write a test for the items module

**Where:** `api/tests/test_items.py`

```bash
mkdir -p api/tests
```

```python
"""Tests for the Items module."""


class TestCreateItem:
    def test_create_valid_item(self, client, api_headers):
        resp = client.post("/api/items/", json={
            "name": "Test Item",
            "price": 19.99,
        }, headers=api_headers)
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["success"] is True
        assert data["data"]["name"] == "Test Item"

    def test_create_missing_price(self, client, api_headers):
        resp = client.post("/api/items/", json={
            "name": "No Price",
        }, headers=api_headers)
        assert resp.status_code == 400

    def test_create_no_auth(self, client):
        resp = client.post("/api/items/", json={
            "name": "Test", "price": 10,
        })
        assert resp.status_code == 401


class TestListItems:
    def test_empty_list(self, client, api_headers):
        resp = client.get("/api/items/", headers=api_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["data"]["items"] == []
        assert data["data"]["total"] == 0

    def test_pagination(self, client, api_headers):
        # Create 5 items
        for i in range(5):
            client.post("/api/items/", json={
                "name": f"Item {i}", "price": 10.0,
            }, headers=api_headers)

        resp = client.get("/api/items/?page=1&page_size=3", headers=api_headers)
        data = resp.get_json()
        assert len(data["data"]["items"]) == 3
        assert data["data"]["total"] == 5


class TestDeleteItem:
    def test_soft_delete(self, client, api_headers, db):
        from app.modules.items.models import Item

        # Create
        resp = client.post("/api/items/", json={
            "name": "Delete Me", "price": 5.0,
        }, headers=api_headers)
        item_id = resp.get_json()["data"]["id"]

        # Delete
        resp = client.delete(f"/api/items/{item_id}", headers=api_headers)
        assert resp.status_code == 204

        # Row still exists (soft delete)
        item = db.session.get(Item, item_id)
        assert item is not None
        assert item.deleted_at is not None

        # Not in list
        resp = client.get("/api/items/", headers=api_headers)
        assert resp.get_json()["data"]["total"] == 0
```

---

### Step 10.3: Run the tests

```bash
pytest -v
```

You should see all tests pass:
```
tests/test_items.py::TestCreateItem::test_create_valid_item PASSED
tests/test_items.py::TestCreateItem::test_create_missing_price PASSED
tests/test_items.py::TestCreateItem::test_create_no_auth PASSED
tests/test_items.py::TestListItems::test_empty_list PASSED
tests/test_items.py::TestListItems::test_pagination PASSED
tests/test_items.py::TestDeleteItem::test_soft_delete PASSED
```

---

### Step 10.4: Create `app/celery_worker.py` — background tasks

```python
"""Celery app — handles async/background work.

Usage:
    celery -A app.celery_worker.celery worker --loglevel=info
"""

from celery import Celery


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        backend=app.config["CELERY_RESULT_BACKEND"],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


# Create a Flask app just to configure Celery (not for serving)
from app import create_app

flask_app = create_app()
celery = make_celery(flask_app)


# ── Example tasks ──

@celery.task(name="tasks.send_email")
def send_email(recipient: str, subject: str, body: str):
    """Simulate sending an email (logs instead of actually sending)."""
    import logging
    log = logging.getLogger(__name__)
    log.info(f"[EMAIL] To: {recipient}, Subject: {subject}")
    log.info(f"[EMAIL] Body: {body[:100]}...")
    return {"status": "sent", "recipient": recipient}


@celery.task(name="tasks.generate_report")
def generate_report(report_type: str):
    """Simulate a long-running report generation."""
    import time
    import logging
    log = logging.getLogger(__name__)
    log.info(f"[REPORT] Generating {report_type} report...")
    time.sleep(5)  # simulate work
    log.info(f"[REPORT] {report_type} report complete")
    return {"status": "done", "report": report_type}


@celery.task(name="tasks.cleanup_old_uploads")
def cleanup_old_uploads():
    """Periodic task — remove uploads older than 24 hours."""
    import os
    import time
    from pathlib import Path

    upload_dir = Path("uploads")
    if not upload_dir.exists():
        return {"deleted": 0}

    cutoff = time.time() - 86400  # 24 hours
    deleted = 0
    for file in upload_dir.iterdir():
        if file.is_file() and file.stat().st_mtime < cutoff:
            file.unlink()
            deleted += 1

    return {"deleted": deleted}
```

---

### Step 10.5: Create `gunicorn.conf.py` — production server config

**Where:** `api/gunicorn.conf.py`

```python
"""Gunicorn configuration for production."""

import os

# ── Worker Processes ──
workers = int(os.getenv("GUNICORN_WORKERS", "4"))
worker_class = "sync"
threads = int(os.getenv("GUNICORN_THREADS", "2"))

# ── Binding ──
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"

# ── Logging ──
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = os.getenv("LOG_LEVEL", "info")
access_log_format = (
    '{"remote_addr":"%(h)s","method":"%(m)s","path":"%(U)s",'
    '"status":"%(s)s","response_time_ms":"%(M)s","bytes":"%(b)s"}'
)

# ── Process Naming ──
proc_name = "flask-api"

# ── Graceful Shutdown ──
timeout = 30
graceful_timeout = 15
max_requests = 1000
max_requests_jitter = 100
```

**Usage in production:**
```bash
gunicorn wsgi:app -c gunicorn.conf.py
```

---

### Step 10.6: Create `.dockerignore`

**Where:** `api/.dockerignore`

```
.venv/
__pycache__/
*.pyc
.env
.git/
.gitignore
uploads/*
tests/
README.md
```

---

### Step 10.7: Build and run the full stack with Docker

```bash
# Build
docker compose build

# Start everything
docker compose up -d

# Check all services
docker compose ps
# Expected: app, postgres, pgadmin, redis, celery — all "Up" or "healthy"

# Run migrations inside the app container
docker compose exec app flask db upgrade

# Test
curl -H "X-API-Key: dev-api-key" http://localhost:5000/api/items/
curl http://localhost:5000/health
```

---

### Step 10.8: Add a Celery beat schedule (periodic tasks)

**Where:** `api/app/celery_worker.py` — append to the existing file:

```python
from celery.schedules import crontab

celery.conf.beat_schedule = {
    "cleanup-uploads-every-3-hours": {
        "task": "tasks.cleanup_old_uploads",
        "schedule": crontab(minute=0, hour="*/3"),
    },
}
celery.conf.timezone = "UTC"
```

Run the beat scheduler alongside the worker:
```bash
celery -A app.celery_worker.celery beat --loglevel=info
```

In `docker-compose.yml`, add:
```yaml
  celery-beat:
    build: .
    container_name: flask-celery-beat
    restart: unless-stopped
    command: celery -A app.celery_worker.celery beat --loglevel=info
    env_file:
      - .env
    depends_on:
      - redis
      - postgres
```

---

## Where You Are Now (Complete Production Tree)

```
api/
├── pyproject.toml                ← All deps + tool config
├── Dockerfile                    ← Multi-stage production build
├── docker-compose.yml            ← App + Postgres + pgAdmin + Redis + Celery
├── .dockerignore
├── .flaskenv                     ← FLASK_APP, FLASK_DEBUG
├── .env                          ← Real secrets (gitignored)
├── .env.example                  ← Template (committed)
├── .gitignore
├── gunicorn.conf.py              ← Production WSGI server config
├── wsgi.py                       ← Gunicorn entry point
├── run.py                        ← Dev server entry (socketio.run)
├── uploads/                      ← File uploads (gitignored)
├── migrations/                   ← Alembic versions (commit in real projects)
├── tests/
│   ├── conftest.py               ← pytest fixtures
│   └── test_items.py             ← Item CRUD tests
│
└── app/
    ├── __init__.py               ← create_app() factory
    ├── config.py                 ← Dev / Test / Prod config classes
    ├── extensions.py             ← db, bcrypt, migrate, socketio, cors, talisman, limiter
    ├── celery_worker.py          ← Celery app + tasks + beat schedule
    │
    ├── common/
    │   ├── models/base.py        ← id, created_at, updated_at, deleted_at
    │   ├── utils/password.py     ← bcrypt hash/verify
    │   ├── auth.py               ← X-API-Key guard (before_request)
    │   ├── errors.py             ← Global error handlers
    │   └── response_wrapper.py   ← {success, data, timestamp} envelope (after_request)
    │
    └── modules/
        ├── health/routes.py      ← /health (no auth)
        │
        ├── items/
        │   ├── schemas.py        ← CreateItemSchema, UpdateItemSchema, FilterItemSchema
        │   ├── models.py         ← Item (SQLAlchemy)
        │   ├── service.py        ← Business logic
        │   └── routes.py         ← POST/GET/PATCH/DELETE /api/items
        │
        ├── users/
        │   ├── schemas.py        ← CreateUserSchema, UpdateUserSchema
        │   ├── models.py         ← User (SQLAlchemy)
        │   ├── service.py        ← Password hashing, uniqueness checks
        │   └── routes.py         ← POST/GET/PATCH/DELETE /api/users
        │
        ├── demo/
        │   └── routes.py         ← Headers, cookies, status codes
        │
        ├── formfiles/
        │   └── routes.py         ← Form parsing, file uploads
        │
        └── websocket/
            └── events.py         ← SocketIO connect/message/join/leave
```

---

## Flask → NestJS Parallel

| Concept | NestJS | Flask (Production) |
|---------|--------|---------------------|
| Route | `@Get()` in a `@Controller('items')` | `@items_bp.get("/")` in a `Blueprint("items", url_prefix="/api/items")` |
| Path param | `@Param('id', ParseIntPipe) id: number` | `/<int:item_id>` → `def route(item_id: int)` |
| Query validation | `@Query() filters: FilterItemDto` | `@validate() ... query: FilterItemSchema` |
| Body validation | class-validator DTO | Pydantic `BaseModel` + `flask_pydantic.validate()` |
| DI | `constructor(private service: ItemService)` | Plain function imports (`from app.modules.items import service`) |
| ORM model | `class Item extends BaseEntity` | `class Item(BaseModel)` with `db.Column` |
| Migrations | TypeORM migrations | Flask-Migrate (Alembic) — `flask db migrate` |
| Swagger | `@ApiProperty()` decorators | flasgger at `/apidocs` |
| Exception | `NotFoundException()` | Custom exception + `@app.errorhandler` |
| Module registry | `@Module({ imports: [...] })` | `app.register_blueprint(bp)` in `create_app` |
| Extensions init | `TypeOrmModule.forRootAsync()` | `db.init_app(app)` in factory |
| Global guard | `APP_GUARD` + `CanActivate` | `@app.before_request` |
| Global interceptor | `APP_INTERCEPTOR` | `@app.after_request` |
| Validation pipe | `app.useGlobalPipes(ValidationPipe)` | Pydantic schema + global `ValidationError` handler |
| CORS | `app.enableCors()` | `CORS(app)` via extensions |
| Security headers | `helmet()` | `Talisman(app)` |
| Rate limiting | `@nestjs/throttler` | `Flask-Limiter` |
| App entry | `main.ts` + `AppModule` | `wsgi.py` (prod) / `run.py` (dev) |
| Config | `@nestjs/config` + `ConfigService` | `app/config.py` with Dev/Test/Prod classes |
| WebSocket | `@WebSocketGateway()` | Flask-SocketIO `@socketio.on("event")` |
| Background tasks | `@nestjs/bull` + Redis | Celery + Redis |
| Tests | Jest | pytest + pytest-flask |
| Production server | Node.js cluster | gunicorn |
| Env file | `.env` (same) | `.env` (same) |

---

## Flask → FastAPI Parallel

| Concept | FastAPI | Flask (Production) |
|---------|---------|---------------------|
| Route | `@router.get("/items")` | `@items_bp.get("/")` |
| Path param | `item_id: int` | `/<int:item_id>` |
| Query validation | `q: str = None` | `query: FilterItemSchema` via `@validate()` |
| Body validation | Pydantic `BaseModel` | Pydantic `BaseModel` (same library!) |
| DI | `Depends(get_db)` | `db.session` (thread-local) |
| ORM model | `class Item(Base)` | `class Item(BaseModel)` |
| Migrations | Alembic | Flask-Migrate (Alembic — same tool!) |
| Swagger | Automatic at `/docs` | flasgger at `/apidocs` |
| Exception | `HTTPException(404)` | Custom exception + `@app.errorhandler` |
| Middleware | `@app.middleware("http")` | `@app.before_request` / `@app.after_request` |
| Background tasks | `BackgroundTasks` or Celery | Celery (same) |
| WebSocket | `@router.websocket("/ws")` | Flask-SocketIO |
| Settings | `pydantic-settings` | `python-dotenv` + `app/config.py` |
| Security headers | `Secure()` middleware | `Talisman` |
| CORS | `CORSMiddleware` | `CORS(app)` |
| Rate limiting | slowapi | Flask-Limiter |
