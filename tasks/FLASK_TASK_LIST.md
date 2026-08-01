# Flask Learning Lab — Step-by-Step Task Checklist (Production-Grade)

> **How to use:** Each step creates ONE file (or adds a few lines to an existing one). Work top to bottom.
> After every step, test with curl or browser. **Never skip a step** — each one builds on the last.
> **Every code block is self-contained for that step only** — no forward imports, no "comment this out for now."

---

## Prerequisites — What You Need Before Starting

### System Requirements

| Requirement | Version | How to Check |
|-------------|---------|---------------|
| Python | ≥ 3.11 | `python --version` |
| pip | ≥ 23.0 | `pip --version` |
| Docker | ≥ 24.0 | `docker --version` |
| Docker Compose | ≥ 2.20 | `docker compose version` |
| curl | any | `curl --version` |
| Git | any | `git --version` |

### Install Python (if not already installed)

**Linux (Debian/Ubuntu/Kali):**
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-dev
```

**macOS (Homebrew):**
```bash
brew install python@3.12
```

**Windows (winget):**
```powershell
winget install Python.Python.3.12
```

### Install Docker (if not already installed)

**Linux:**
```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER   # log out and back in after this
sudo apt install -y docker-compose-v2
```

**macOS / Windows:**
Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).

### Verify Everything

```bash
python --version        # ≥ 3.11
pip --version           # ≥ 23.0
docker --version        # ≥ 24.0
docker compose version  # ≥ 2.20
```

---

## Phase 0 — Project Scaffold (Production-Grade Foundation)

Everything starts here. By the end of Phase 0 you'll have a proper app factory, separate config classes per environment, all extensions in one file, a wsgi entry point for gunicorn, and a working health-check route.

---

### Step 0.1: Create the full folder structure

```bash
mkdir -p api/app/common/models
mkdir -p api/app/common/utils
mkdir -p api/app/modules
mkdir -p api/tests
mkdir -p api/uploads
mkdir -p api/migrations/versions

# Every __init__.py you'll ever need — created NOW so imports never fail
touch api/app/__init__.py
touch api/app/common/__init__.py
touch api/app/common/models/__init__.py
touch api/app/common/utils/__init__.py
touch api/app/modules/__init__.py
touch api/tests/__init__.py
touch api/migrations/versions/.gitkeep
```

**Why now:** Every file you create in later steps already has a home. No `mkdir`, no `touch __init__.py` in any later step.

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

### Step 0.3: Create `pyproject.toml`

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

[tool.setuptools.packages.find]
include = ["app*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

**Key points:**
- `[tool.setuptools.packages.find]` with `include = ["app*"]` — tells setuptools to only discover the `app/` package. Without this, it sees `app/`, `uploads/`, `migrations/`, `tests/` and refuses to build.
- `[project.optional-dependencies] dev` — pytest and httpx stay separate from production installs.
- PEP 621 standard — replaces `requirements.txt` + `requirements-dev.txt` + `setup.cfg`.

---

### Step 0.3a: Create and activate the virtual environment

```bash
cd api

# Create the venv
python3 -m venv .venv

# Activate it
source .venv/bin/activate     # Linux / macOS
# .venv\Scripts\activate      # Windows

# Verify
which python                   # Should show .../api/.venv/bin/python
python --version               # Should be 3.11+
```

**How venv works:**
- `.venv/` is an isolated copy of Python + pip. Everything you install goes here, not globally.
- Activating rewrites your shell's `PATH`. Type `deactivate` to leave.
- `.venv/` is gitignored — each developer creates their own.

---

### Step 0.3b: Install dependencies

```bash
# Make sure venv is active first!
pip install --upgrade pip
pip install -e ".[dev]"
```

**What each part does:**
- `-e` (editable) — changes to your code take effect immediately, no reinstall needed.
- `".[dev]"` — installs production deps + pytest/httpx from the optional-dependencies dev group.
- You can also use `pip install -e .` to skip dev tools — add `[dev]` when you reach Phase 10 (testing).

**Verify:**
```bash
pip list | grep -i flask    # Should show flask, flask-sqlalchemy, flask-pydantic, etc.
```

**Common errors:**

| Error | Fix |
|-------|-----|
| `error: command 'gcc' failed` | `sudo apt install -y gcc libpq-dev python3-dev` |
| Multiple top-level packages discovered | `pyproject.toml` is missing `[tool.setuptools.packages.find]` — fix Step 0.3 |
| Permission denied | You forgot to activate the venv: `source .venv/bin/activate` |

---

### Step 0.3c: Create standalone `docker-compose.db.yml` — Postgres + pgAdmin only

**Where:** `api/docker-compose.db.yml`

```yaml
# Standalone database services for development.
# Start:  docker compose -f docker-compose.db.yml up -d
# Stop:   docker compose -f docker-compose.db.yml down

services:
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
      - pgdata_dev:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U flask -d flask_learn"]
      interval: 5s
      timeout: 5s
      retries: 5

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

volumes:
  pgdata_dev:
```

**Start it:**
```bash
docker compose -f docker-compose.db.yml up -d
docker compose -f docker-compose.db.yml ps    # Both should show "healthy" or "Up"
```

**Port choices (non-default — won't collide with existing services):**
| Service | Host Port | Container Port |
|---------|-----------|----------------|
| Postgres | 5600 | 5432 |
| pgAdmin | 5051 | 80 |

---

### Step 0.4: Create `.flaskenv`

**Where:** `api/.flaskenv`

```
FLASK_APP=run.py
FLASK_DEBUG=1
```

**Why:** The `flask` CLI auto-loads these. No need to set env vars manually every time.

---

### Step 0.5: Create `.env` (dev secrets)

**Where:** `api/.env`

```
FLASK_ENV=development
SECRET_KEY=change-me-in-production-abc123
PORT=5000
DATABASE_HOST=localhost
DATABASE_PORT=5600
DATABASE_USER=flask
DATABASE_PASSWORD=flask
DATABASE_NAME=flask_learn
```

**Why:** `.env` holds real values and is gitignored. Only the essentials for now — more keys added in later phases.

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

**Why:** Teammates copy this to `.env` and fill in real values. Shows every setting without exposing secrets. This file IS committed.

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

    # ── Swagger / Flasgger ──
    SWAGGER: dict = {
        "title": "Flask Learning API",
        "description": "Production-grade Flask REST API — all routes except /health require X-API-Key header.",
        "version": "0.1.0",
        "uiversion": 3,
        "openapi": "3.0.3",
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

| Extension | Role |
|-----------|------|
| `SQLAlchemy` | ORM — maps Python classes to Postgres tables |
| `Bcrypt` | Password hashing |
| `Migrate` | Alembic wrapper — generates DB migrations from model changes |
| `SocketIO` | WebSocket support |
| `CORS` | Cross-origin requests (SPA frontend calling this API) |
| `Talisman` | Security headers (HSTS, X-Content-Type-Options, etc.) |
| `Limiter` | Rate limiting (prevents abuse) |

---

### Step 0.9: Create `app/__init__.py` — the app factory (MINIMAL)

**Where:** `api/app/__init__.py`

**This step creates ONLY what works right now.** Placeholder comments mark exactly where you'll add things in later phases.

```python
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

    app.register_blueprint(health_bp)
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
    # (Step 2.2) from app.modules.items import models    # noqa: F401
    # (Step 5.1) from app.modules.users import models    # noqa: F401
    # NEW_MODEL_IMPORT ← add model imports above this line (after all blueprints)

    app.extensions["bcrypt"] = bcrypt
    return app
```

**What this file does RIGHT NOW:** Config loading → extension init → Flasgger at `/apidocs/` → health blueprint → returns the app. Everything else is a labeled placeholder — no commenting out needed, just ADD lines when each phase tells you to.

---

### Step 0.10: Create `wsgi.py` — gunicorn entry point

**Where:** `api/wsgi.py`

```python
"""WSGI entry point for production servers (gunicorn, uWSGI)."""
from app import create_app

app = create_app()
```

**Why separate from run.py:** `wsgi.py` is a bare module — gunicorn imports `app` from it. No `if __name__` block. `run.py` is for dev with `socketio.run()`.

---

### Step 0.11: Create `run.py` — dev server entry point

**Where:** `api/run.py`

```python
"""Development server entry point."""
from app import create_app
from app.extensions import socketio

app = create_app()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=app.config["PORT"], debug=True,
                  allow_unsafe_werkzeug=True)
```

**Note:** `from app import socketio` imports from `app.extensions`, which is available because `app/__init__.py` imports it.

---

### Step 0.12: Create health-check blueprint (first working route)

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
    """Health check.
    ---
    tags:
      - Health
    responses:
      200:
        description: API is healthy
    """
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
```

**Done.** The `__init__.py` from Step 0.9 already imports and registers `health_bp` — no changes needed there.

---

### Step 0.13: Run the dev server

```bash
# Pre-flight checks
which python                              # Is venv active?
pip list | grep -i flask                  # Are deps installed?
docker compose -f docker-compose.db.yml ps  # Is Postgres running?

# Start
python run.py
```

You should see:
```
 * Serving Flask app 'run.py'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

**Test:**
```bash
curl http://localhost:5000/health          # → {"status":"ok","timestamp":"..."}
```
Open [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/) → Swagger UI with the health endpoint.

`Ctrl+C` to stop.

---

### Step 0.14: Folder structure so far

```
api/
├── pyproject.toml
├── docker-compose.db.yml
├── .flaskenv
├── .env
├── .env.example
├── .gitignore
├── wsgi.py
├── run.py
├── uploads/
├── migrations/versions/.gitkeep
├── tests/__init__.py
└── app/
    ├── __init__.py          ← create_app() — minimal, with placeholders
    ├── config.py            ← Base/Dev/Test/Prod
    ├── extensions.py        ← db, bcrypt, migrate, socketio, cors, talisman, limiter
    ├── common/
    │   ├── models/
    │   └── utils/
    └── modules/
        ├── __init__.py
        └── health/
            ├── __init__.py
            └── routes.py    ← /health (Swagger-documented)
```

**Request flow:** Browser → `run.py` → `create_app()` → config loaded → extensions init → Flasgger → blueprint routes matched → response

---

## Phase 1 — Docker, Database, Migrations

### Step 1.1: Create `Dockerfile` (multi-stage)

**Where:** `api/Dockerfile`

```dockerfile
# ── Stage 1: Build ──
FROM python:3.12-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*
COPY pyproject.toml .
RUN pip install --no-cache-dir --user -e ".[dev]"

# ── Stage 2: Runtime ──
FROM python:3.12-slim AS runtime
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .
RUN useradd --create-home flask && chown -R flask:flask /app
USER flask
EXPOSE 5000
CMD ["gunicorn", "wsgi:app", "-c", "gunicorn.conf.py"]
```

**Why multi-stage:** Builder has `gcc` for compiling `psycopg2`. Runtime doesn't — smaller image, fewer CVEs. Non-root `flask` user for security.

---

### Step 1.2: Create `docker-compose.yml` (full stack)

**Where:** `api/docker-compose.yml`

```yaml
services:
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

  redis:
    image: redis:7-alpine
    container_name: flask-redis
    restart: unless-stopped
    ports:
      - "6379:6379"

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

---

### Step 1.3: Update `.env` — add full credentials

**Where:** `api/.env` — replace content:

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

### Step 1.4: Start database services

```bash
docker compose -f docker-compose.db.yml up -d
docker compose -f docker-compose.db.yml ps   # postgres + pgadmin healthy
```

---

### Step 1.5: Initialize Flask-Migrate

```bash
flask db init
```

This creates `api/migrations/` — Alembic's version-control for your database schema.

**Why Flask-Migrate instead of `db.create_all()`:** `db.create_all()` can only create tables. It can't add a column or rename one. Flask-Migrate generates incremental migration scripts — the same way production databases are managed.

---

### Step 1.6: Verify database connection

```bash
flask shell
```

```python
from app.extensions import db
db.engine.connect()    # No error = connected
```

`Ctrl+D` to exit. If you get `OperationalError`, check Postgres is running (`docker compose -f docker-compose.db.yml ps`).

---

## Phase 2 — First CRUD (Items) with Proper Migrations

### Step 2.1: Create `app/common/models/base.py`

```python
"""Base model — id, timestamps, soft-delete, serialization."""
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
        """Serialize to dict, ISO-formatting datetime columns."""
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

```bash
mkdir -p api/app/modules/items
touch api/app/modules/items/__init__.py
```

**Where:** `api/app/modules/items/models.py`

```python
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

**Now add the model import to `__init__.py`** — find the comment `# (Step 2.2)` in `app/__init__.py` and replace it:

```python
# In app/__init__.py, find the MODEL DISCOVERY section and replace the comment:
# OLD:
# (Step 2.2) from app.modules.items import models    # noqa: F401
# NEW (uncommented):
from app.modules.items import models  # noqa: F401
```

---

### Step 2.3: Create Pydantic schemas

**Where:** `api/app/modules/items/schemas.py`

```python
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class CreateItemSchema(BaseModel):
    model_config = {"extra": "forbid"}

    name: str = Field(..., min_length=1, max_length=255, examples=["Laptop"])
    price: Decimal = Field(..., ge=0, examples=[999.99])
    description: Optional[str] = Field(None, max_length=1000)
    in_stock: Optional[bool] = True


class UpdateItemSchema(BaseModel):
    model_config = {"extra": "forbid"}

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[Decimal] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=1000)
    in_stock: Optional[bool] = None

    @model_validator(mode="after")
    def at_least_one_field(self):
        if all(v is None for v in self.__dict__.values()):
            raise ValueError("At least one field must be provided for update")
        return self
```

---

### Step 2.4: Create the service layer

**Where:** `api/app/modules/items/service.py`

```python
"""Item business logic — pure Python, no HTTP awareness."""
from datetime import datetime, timezone

from sqlalchemy import select

from app.extensions import db
from app.modules.items.models import Item


class ItemNotFoundError(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id
        super().__init__(f"Item {item_id} not found")


def create_item(data) -> Item:
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


def update_item(item_id: int, data) -> Item:
    item = get_item(item_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.session.commit()
    return item


def delete_item(item_id: int) -> None:
    item = get_item(item_id)
    item.deleted_at = datetime.now(timezone.utc)
    db.session.commit()
```

---

### Step 2.5: Create the routes

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
    """Create a new item.
    ---
    tags:
      - Items
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/CreateItemSchema'
    responses:
      201:
        description: Item created
      400:
        description: Validation error
    """
    item = service.create_item(body)
    return jsonify(item.to_dict()), 201


@items_bp.get("/")
def list_items():
    """List all items.
    ---
    tags:
      - Items
    responses:
      200:
        description: List of all non-deleted items
    """
    items = service.get_all_items()
    return jsonify([i.to_dict() for i in items])


@items_bp.get("/<int:item_id>")
def get_item(item_id: int):
    """Get a single item by ID.
    ---
    tags:
      - Items
    parameters:
      - in: path
        name: item_id
        type: integer
        required: true
    responses:
      200:
        description: Item found
      404:
        description: Item not found
    """
    return jsonify(service.get_item(item_id).to_dict())


@items_bp.patch("/<int:item_id>")
@validate()
def update_item(item_id: int, body: UpdateItemSchema):
    """Partially update an item (PATCH semantics).
    ---
    tags:
      - Items
    parameters:
      - in: path
        name: item_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/UpdateItemSchema'
    responses:
      200:
        description: Item updated
      404:
        description: Item not found
    """
    return jsonify(service.update_item(item_id, body).to_dict())


@items_bp.delete("/<int:item_id>")
def delete_item(item_id: int):
    """Soft-delete an item.
    ---
    tags:
      - Items
    parameters:
      - in: path
        name: item_id
        type: integer
        required: true
    responses:
      204:
        description: Item soft-deleted
      404:
        description: Item not found
    """
    service.delete_item(item_id)
    return "", 204
```

---

### Step 2.6: Register items blueprint in `__init__.py`

In `app/__init__.py`, find the BLUEPRINTS section. Add **two lines** below the health_bp lines:

```python
# Find these lines:
    from app.modules.health.routes import health_bp        # Step 0.12
    app.register_blueprint(health_bp)
    # NEW_BLUEPRINT_IMPORT   ← add blueprint imports above this line

# ADD the items_bp import and register:
    from app.modules.items.routes import items_bp           # Step 2.5
    app.register_blueprint(items_bp)
```

---

### Step 2.7: Generate and run your first migration

```bash
flask db migrate -m "create items table"
flask db upgrade
```

Verify:
```bash
docker exec flask-postgres psql -U flask -d flask_learn -c "\dt"
# Should show: items, alembic_version
```

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

# Update (PATCH — only name changes)
curl -X PATCH http://localhost:5000/api/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Gaming Laptop"}'

# Delete (soft)
curl -X DELETE http://localhost:5000/api/items/1

# List again — item 1 is gone
curl http://localhost:5000/api/items/
```

Open [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/) — Items endpoints are now documented.

---

### Step 2.9: Verify soft delete

```bash
docker exec flask-postgres psql -U flask -d flask_learn \
  -c "SELECT id, name, deleted_at FROM items;"
```

The deleted item still exists with `deleted_at` set. The API filters it out.

---

## Phase 3 — Query Parameters & Pagination

### Step 3.1: Add filter schema to schemas.py

**Where:** `api/app/modules/items/schemas.py` — **append** to the existing file:

```python

# ── Query Filters ──

class FilterItemSchema(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)
    name: Optional[str] = Field(None, description="Search by name (case-insensitive ILIKE)")
    max_price: Optional[Decimal] = Field(None, ge=0)
    in_stock: Optional[bool] = None

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
```

---

### Step 3.2: Add filtered query to service.py

**Where:** `api/app/modules/items/service.py` — **append** to the existing file:

```python

# ── Filtered / Paginated Query ──

from sqlalchemy import func
from app.modules.items.schemas import FilterItemSchema


def get_filtered_items(filters: FilterItemSchema) -> dict:
    stmt = select(Item).where(Item.deleted_at.is_(None))

    if filters.name:
        stmt = stmt.where(Item.name.ilike(f"%{filters.name}%"))
    if filters.max_price is not None:
        stmt = stmt.where(Item.price <= filters.max_price)
    if filters.in_stock is not None:
        stmt = stmt.where(Item.in_stock == filters.in_stock)

    total = db.session.scalar(select(func.count()).select_from(stmt.subquery()))

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

**Where:** `api/app/modules/items/routes.py` — **replace** the `list_items` function:

```python
from app.modules.items.schemas import FilterItemSchema  # add to top imports

@items_bp.get("/")
@validate()
def list_items(query: FilterItemSchema):
    """List items with filtering and pagination.
    ---
    tags:
      - Items
    parameters:
      - in: query
        name: page
        type: integer
        default: 1
      - in: query
        name: page_size
        type: integer
        default: 10
      - in: query
        name: name
        type: string
        required: false
        description: Filter by name (ILIKE)
      - in: query
        name: max_price
        type: number
        required: false
      - in: query
        name: in_stock
        type: boolean
        required: false
    responses:
      200:
        description: Paginated, filtered list of items
    """
    return jsonify(service.get_filtered_items(query))
```

---

### Step 3.4: Test pagination and filtering

```bash
curl "http://localhost:5000/api/items/?page=1&page_size=2"
curl "http://localhost:5000/api/items/?name=phone"
curl "http://localhost:5000/api/items/?max_price=500&in_stock=true"
curl "http://localhost:5000/api/items/?page_size=200"   # 400 — validation error
```

---

## Phase 4 — Validation & Error Handling (Global)

### Step 4.1: Create `app/common/errors.py`

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

**Now activate it in `__init__.py`.** Find the comment block `# (Step 4.1)` and uncomment those two lines:

```python
# In app/__init__.py — uncomment these two lines:
from app.common.errors import register_error_handlers
register_error_handlers(app)
```

---

### Step 4.2: Test validation errors

```bash
# Missing required field
curl -X POST http://localhost:5000/api/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": ""}'

# Unknown field (extra="forbid")
curl -X POST http://localhost:5000/api/items/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","price":10,"hacked":true}'

# Non-existent route
curl http://localhost:5000/api/nope
```

All return proper JSON errors, not HTML pages.

---

## Phase 5 — Users Module (Password Hashing)

### Step 5.1: Create the User model

```bash
mkdir -p api/app/modules/users
touch api/app/modules/users/__init__.py
```

**Where:** `api/app/modules/users/models.py`

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

**Now add model discovery in `__init__.py`.** Find the comment `# (Step 5.1)` and replace:

```python
# In app/__init__.py, MODEL DISCOVERY section:
# Replace the commented line with:
from app.modules.users import models  # noqa: F401
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
        db.session.scalars(select(User).where(User.deleted_at.is_(None))).all()
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

### Step 5.6: Register users blueprint in `__init__.py`

In `app/__init__.py`, find the BLUEPRINTS section. Add **two lines**:

```python
# Add below the items_bp lines:
    from app.modules.users.routes import users_bp           # Step 5.5
    app.register_blueprint(users_bp)
```

---

### Step 5.7: Generate migration

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

# Duplicate email → 409
curl -X POST http://localhost:5000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice2","email":"alice@example.com","password":"password123"}'

curl http://localhost:5000/api/users/
```

---

## Phase 6 — API Key Auth (before_request Guard)

### Step 6.1: Update `.env` — add API keys

**Where:** `api/.env` — **append:**

```
API_KEY=dev-api-key
ADMIN_API_KEY=dev-admin-key
```

---

### Step 6.2: Create `app/common/auth.py`

```python
"""API-Key authentication — runs before every request."""
from flask import current_app, g, jsonify, request

EXEMPT_PREFIXES = ("/apidocs", "/flasgger_static", "/apispec", "/health")


def require_api_key():
    """Before-request hook — checks X-API-Key header."""
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

**Now activate it in `__init__.py`.** Find the comment block `# (Step 6.2)` and uncomment:

```python
# In app/__init__.py — uncomment these two lines:
from app.common.auth import require_api_key
app.before_request(require_api_key)
```

---

### Step 6.3: Test auth

```bash
# No key → 401
curl http://localhost:5000/api/items/

# Wrong key → 401
curl -H "X-API-Key: wrong" http://localhost:5000/api/items/

# Valid key → 200
curl -H "X-API-Key: dev-api-key" http://localhost:5000/api/items/

# Admin key → 200
curl -H "X-API-Key: dev-admin-key" http://localhost:5000/api/items/

# Health is exempt → no key needed
curl http://localhost:5000/health
```

---

## Phase 7 — Headers, Cookies, Status Codes, Form/Files

### Step 7.1: Create demo blueprint

```bash
mkdir -p api/app/modules/demo
touch api/app/modules/demo/__init__.py
```

**Where:** `api/app/modules/demo/routes.py`

```python
"""Demo routes — reading/setting headers, cookies, and status codes."""
from flask import Blueprint, jsonify, make_response, redirect, request

demo_bp = Blueprint("demo", __name__, url_prefix="/api/demo")


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


@demo_bp.get("/read-cookie")
def read_cookie():
    return jsonify({"session_id": request.cookies.get("session_id", "none")})


@demo_bp.get("/set-cookie")
def set_cookie():
    resp = make_response(jsonify({"message": "Cookie set!"}))
    resp.set_cookie("session_id", value="abc-123", httponly=True,
                    secure=False, samesite="Lax", max_age=3600)
    return resp


@demo_bp.get("/delete-cookie")
def delete_cookie():
    resp = make_response(jsonify({"message": "Cookie deleted"}))
    resp.delete_cookie("session_id")
    return resp


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

### Step 7.2: Create form-files blueprint

```bash
mkdir -p api/app/modules/formfiles
touch api/app/modules/formfiles/__init__.py
```

**Where:** `api/app/modules/formfiles/routes.py`

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

### Step 7.3: Register both blueprints in `__init__.py`

In `app/__init__.py`, find the BLUEPRINTS section. Add **four lines**:

```python
# Add below the users_bp lines:
    from app.modules.demo.routes import demo_bp              # Step 7.1
    from app.modules.formfiles.routes import formfiles_bp    # Step 7.2

    app.register_blueprint(demo_bp)
    app.register_blueprint(formfiles_bp)
```

---

### Step 7.4: Test

```bash
# Headers & cookies
curl -H "X-API-Key: dev-api-key" -H "User-Agent: MyApp" http://localhost:5000/api/demo/whoami
curl -H "X-API-Key: dev-api-key" -v http://localhost:5000/api/demo/set-cookie 2>&1 | grep -i set-cookie

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
"""After-request hook — wraps JSON success responses in a standard envelope."""
from datetime import datetime, timezone
from flask import jsonify, request

SKIP_PREFIXES = ("/apidocs", "/flasgger_static", "/apispec", "/socket.io")


def wrap_response(response):
    """Wrap JSON success responses in {success, data, timestamp}."""
    if request.path.startswith(SKIP_PREFIXES):
        return response
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

**Now activate it in `__init__.py`.** Find the comment block `# (Step 8.1)` and uncomment:

```python
# In app/__init__.py — uncomment these two lines:
from app.common.response_wrapper import wrap_response
app.after_request(wrap_response)
```

Now every success response is automatically wrapped:
```json
{"success": true, "data": { ... }, "timestamp": "2026-07-31T12:34:56.789Z"}
```

---

## Phase 9 — WebSockets

### Step 9.1: Create `app/modules/websocket/events.py`

```bash
mkdir -p api/app/modules/websocket
touch api/app/modules/websocket/__init__.py
```

**Where:** `api/app/modules/websocket/events.py`

```python
"""WebSocket event handlers — real-time messaging."""
from datetime import datetime, timezone
from flask import request
from flask_socketio import emit, join_room, leave_room
from app.extensions import socketio

connected_clients: dict[str, str] = {}


@socketio.on("connect")
def handle_connect():
    connected_clients[request.sid] = request.remote_addr
    emit("server_message", {
        "type": "connect", "sid": request.sid,
        "message": "Welcome!",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


@socketio.on("disconnect")
def handle_disconnect():
    connected_clients.pop(request.sid, None)
    emit("server_message", {
        "type": "disconnect", "sid": request.sid,
        "message": f"{request.sid} left",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }, broadcast=True)


@socketio.on("message")
def handle_message(payload):
    emit("message", {
        "from": request.sid,
        "text": payload if isinstance(payload, str) else payload.get("text", ""),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }, broadcast=True)


@socketio.on("join")
def handle_join(room: str):
    join_room(room)
    emit("server_message", {
        "type": "join", "sid": request.sid, "room": room,
        "message": f"Joined room: {room}",
    }, to=request.sid)


@socketio.on("leave")
def handle_leave(room: str):
    leave_room(room)
    emit("server_message", {
        "type": "leave", "sid": request.sid, "room": room,
        "message": f"Left room: {room}",
    }, to=request.sid)
```

**Now activate it in `__init__.py`.** Find the comment `# (Step 9.1)` and uncomment:

```python
# In app/__init__.py — uncomment:
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

socket.emit('message', 'Hello everyone!');
socket.emit('join', 'room-1');
```

---

## Phase 10 — Testing, Background Tasks, Production Deploy

### Step 10.1: Create pytest fixtures

**Where:** `api/tests/conftest.py`

```python
"""Shared pytest fixtures."""
import pytest
from app import create_app
from app.extensions import db as _db


@pytest.fixture
def app():
    _app = create_app(env="testing")
    with _app.app_context():
        _db.create_all()
        yield _app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def db(app):
    return _db


@pytest.fixture
def api_headers():
    return {"X-API-Key": "test-key", "Content-Type": "application/json"}
```

---

### Step 10.2: Write tests for the items module

**Where:** `api/tests/test_items.py`

```python
"""Tests for the Items module."""


class TestCreateItem:
    def test_create_valid_item(self, client, api_headers):
        resp = client.post("/api/items/", json={
            "name": "Test Item", "price": 19.99,
        }, headers=api_headers)
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["success"] is True
        assert data["data"]["name"] == "Test Item"

    def test_create_missing_price(self, client, api_headers):
        resp = client.post("/api/items/", json={"name": "No Price"}, headers=api_headers)
        assert resp.status_code == 400

    def test_create_no_auth(self, client):
        resp = client.post("/api/items/", json={"name": "Test", "price": 10})
        assert resp.status_code == 401


class TestListItems:
    def test_empty_list(self, client, api_headers):
        resp = client.get("/api/items/", headers=api_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["data"]["items"] == []
        assert data["data"]["total"] == 0

    def test_pagination(self, client, api_headers):
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

        resp = client.post("/api/items/", json={
            "name": "Delete Me", "price": 5.0,
        }, headers=api_headers)
        item_id = resp.get_json()["data"]["id"]

        resp = client.delete(f"/api/items/{item_id}", headers=api_headers)
        assert resp.status_code == 204

        item = db.session.get(Item, item_id)
        assert item is not None
        assert item.deleted_at is not None

        resp = client.get("/api/items/", headers=api_headers)
        assert resp.get_json()["data"]["total"] == 0
```

---

### Step 10.3: Run tests

```bash
pytest -v
```

Expected: all 6 tests PASSED.

---

### Step 10.4: Create `app/celery_worker.py`

```python
"""Celery app — async/background tasks."""
from celery import Celery
from celery.schedules import crontab


def make_celery(app):
    celery = Celery(app.import_name,
                    broker=app.config["CELERY_BROKER_URL"],
                    backend=app.config["CELERY_RESULT_BACKEND"])
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


from app import create_app
flask_app = create_app()
celery = make_celery(flask_app)


@celery.task(name="tasks.send_email")
def send_email(recipient: str, subject: str, body: str):
    import logging
    log = logging.getLogger(__name__)
    log.info(f"[EMAIL] To: {recipient}, Subject: {subject}")
    return {"status": "sent", "recipient": recipient}


@celery.task(name="tasks.generate_report")
def generate_report(report_type: str):
    import time, logging
    log = logging.getLogger(__name__)
    log.info(f"[REPORT] Generating {report_type} report...")
    time.sleep(5)
    log.info(f"[REPORT] {report_type} report complete")
    return {"status": "done", "report": report_type}


@celery.task(name="tasks.cleanup_old_uploads")
def cleanup_old_uploads():
    import time
    from pathlib import Path

    upload_dir = Path("uploads")
    if not upload_dir.exists():
        return {"deleted": 0}

    cutoff = time.time() - 86400
    deleted = 0
    for file in upload_dir.iterdir():
        if file.is_file() and file.stat().st_mtime < cutoff:
            file.unlink()
            deleted += 1
    return {"deleted": deleted}


celery.conf.beat_schedule = {
    "cleanup-uploads-every-3-hours": {
        "task": "tasks.cleanup_old_uploads",
        "schedule": crontab(minute=0, hour="*/3"),
    },
}
celery.conf.timezone = "UTC"
```

**Usage:**
```bash
celery -A app.celery_worker.celery worker --loglevel=info
celery -A app.celery_worker.celery beat --loglevel=info   # separate terminal
```

---

### Step 10.5: Create `gunicorn.conf.py`

**Where:** `api/gunicorn.conf.py`

```python
"""Gunicorn configuration for production."""
import os

workers = int(os.getenv("GUNICORN_WORKERS", "4"))
worker_class = "sync"
threads = int(os.getenv("GUNICORN_THREADS", "2"))
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("LOG_LEVEL", "info")
access_log_format = (
    '{"remote_addr":"%(h)s","method":"%(m)s","path":"%(U)s",'
    '"status":"%(s)s","response_time_ms":"%(M)s","bytes":"%(b)s"}'
)
proc_name = "flask-api"
timeout = 30
graceful_timeout = 15
max_requests = 1000
max_requests_jitter = 100
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

### Step 10.7: Build and run full stack with Docker

```bash
docker compose build
docker compose up -d
docker compose ps
# Expected: app, postgres, pgadmin, redis, celery — all Up/healthy

docker compose exec app flask db upgrade
curl -H "X-API-Key: dev-api-key" http://localhost:5000/api/items/
curl http://localhost:5000/health
```

---

### Step 10.8: Add Celery beat to docker-compose.yml

In `api/docker-compose.yml`, add under `services:`:

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

## Complete Production Tree

```
api/
├── pyproject.toml                ← All deps + tool config
├── Dockerfile                    ← Multi-stage production build
├── docker-compose.yml            ← Full stack: App + Postgres + pgAdmin + Redis + Celery
├── docker-compose.db.yml         ← Lightweight: Postgres + pgAdmin only (dev)
├── .dockerignore
├── .flaskenv                     ← FLASK_APP, FLASK_DEBUG
├── .env                          ← Real secrets (gitignored)
├── .env.example                  ← Template (committed)
├── .gitignore
├── gunicorn.conf.py              ← Production WSGI server config
├── wsgi.py                       ← Gunicorn entry point
├── run.py                        ← Dev server entry (socketio.run)
├── uploads/                      ← File uploads (gitignored)
├── migrations/                   ← Alembic versions
│   └── versions/.gitkeep
├── tests/
│   ├── __init__.py
│   ├── conftest.py               ← pytest fixtures
│   └── test_items.py             ← Item CRUD tests
│
└── app/
    ├── __init__.py               ← create_app() factory (built incrementally)
    ├── config.py                 ← Dev / Test / Prod config classes
    ├── extensions.py             ← db, bcrypt, migrate, socketio, cors, talisman, limiter
    ├── celery_worker.py          ← Celery app + tasks + beat schedule
    │
    ├── common/
    │   ├── __init__.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   └── base.py           ← id, created_at, updated_at, deleted_at
    │   ├── utils/
    │   │   ├── __init__.py
    │   │   └── password.py       ← bcrypt hash/verify
    │   ├── auth.py               ← X-API-Key guard (before_request)
    │   ├── errors.py             ← Global error handlers
    │   └── response_wrapper.py   ← {success, data, timestamp} envelope
    │
    └── modules/
        ├── __init__.py
        ├── health/
        │   ├── __init__.py
        │   └── routes.py         ← /health
        ├── items/
        │   ├── __init__.py
        │   ├── schemas.py        ← CreateItemSchema, UpdateItemSchema, FilterItemSchema
        │   ├── models.py         ← Item (SQLAlchemy)
        │   ├── service.py        ← Business logic
        │   └── routes.py         ← CRUD /api/items
        ├── users/
        │   ├── __init__.py
        │   ├── schemas.py        ← CreateUserSchema, UpdateUserSchema
        │   ├── models.py         ← User (SQLAlchemy)
        │   ├── service.py        ← Password hashing, uniqueness checks
        │   └── routes.py         ← CRUD /api/users
        ├── demo/
        │   ├── __init__.py
        │   └── routes.py         ← Headers, cookies, status codes
        ├── formfiles/
        │   ├── __init__.py
        │   └── routes.py         ← Form parsing, file uploads
        └── websocket/
            ├── __init__.py
            └── events.py         ← SocketIO connect/message/join/leave
```

---

## Flask → NestJS Parallel

| Concept | NestJS | Flask (Production) |
|---------|--------|---------------------|
| Route | `@Get()` in `@Controller('items')` | `@items_bp.get("/")` in `Blueprint("items", url_prefix="/api/items")` |
| Path param | `@Param('id', ParseIntPipe)` | `/<int:item_id>` |
| Query validation | `@Query() filters: FilterItemDto` | `@validate() query: FilterItemSchema` |
| Body validation | class-validator DTO | Pydantic `BaseModel` + `flask_pydantic.validate()` |
| DI | `constructor(private service: ItemService)` | Plain function imports |
| ORM model | `class Item extends BaseEntity` | `class Item(BaseModel)` |
| Migrations | TypeORM migrations | Flask-Migrate (Alembic) |
| Swagger | `@ApiProperty()` decorators | flasgger at `/apidocs` |
| Exception | `NotFoundException()` | Custom exception + `@app.errorhandler` |
| Module registry | `@Module({ imports: [...] })` | `app.register_blueprint(bp)` |
| Global guard | `APP_GUARD` + `CanActivate` | `@app.before_request` |
| Global interceptor | `APP_INTERCEPTOR` | `@app.after_request` |
| Validation pipe | `app.useGlobalPipes(ValidationPipe)` | Pydantic schema + global `ValidationError` handler |
| CORS | `app.enableCors()` | `CORS(app)` |
| Security headers | `helmet()` | `Talisman(app)` |
| Rate limiting | `@nestjs/throttler` | `Flask-Limiter` |
| App entry | `main.ts` + `AppModule` | `wsgi.py` (prod) / `run.py` (dev) |
| Config | `@nestjs/config` | `app/config.py` with Dev/Test/Prod classes |
| WebSocket | `@WebSocketGateway()` | Flask-SocketIO |
| Background tasks | `@nestjs/bull` + Redis | Celery + Redis |
| Tests | Jest | pytest |
| Production server | Node.js cluster | gunicorn |
| Env file | `.env` | `.env` |

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

---

## Troubleshooting Guide

### Import Errors

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: No module named 'flask'` | Activate venv: `source .venv/bin/activate && pip install -e ".[dev]"` |
| `ModuleNotFoundError: No module named 'app'` | `cd api && pip install -e ".[dev]"` |
| `ImportError: cannot import name 'items_bp'` | You're trying to use a blueprint before creating it. Follow phases in order. |

### Database Errors

| Error | Fix |
|-------|-----|
| `could not connect to server` | `docker compose -f docker-compose.db.yml up -d` |
| `database "flask_learn" does not exist` | `docker compose -f docker-compose.db.yml down -v && docker compose -f docker-compose.db.yml up -d` |
| `relation "items" does not exist` | `flask db upgrade` |
| `Target database is not up to date` | `flask db upgrade` |

### Docker Errors

| Error | Fix |
|-------|-----|
| `port is already allocated` | Stop conflicting containers or change ports in compose file |
| `Cannot connect to Docker daemon` | `sudo systemctl start docker` (Linux) or start Docker Desktop |
| `permission denied` | `sudo usermod -aG docker $USER`, log out and back in |

### Runtime Errors

| Error | Fix |
|-------|-----|
| `401 Missing X-API-Key header` | Auth is active. Add `-H "X-API-Key: dev-api-key"` to curl |
| `400 extra fields not permitted` | Pydantic `extra="forbid"` — remove unknown fields from request body |
| `KeyError: 'API_KEY'` | `.env` missing or not loaded — check `.env` exists in `api/` |

### Swagger Errors

| Error | Fix |
|-------|-----|
| `/apidocs/` 404 or blank | Flasgger not initialized — check `Swagger(app, ...)` in `__init__.py` |
| "No operations defined in spec" | Routes don't have Swagger docstrings yet — add YAML docstrings |

### Testing Errors

| Error | Fix |
|-------|-----|
| `pytest: command not found` | `pip install -e ".[dev]"` |
| Tests connecting to real Postgres | Make sure `create_app(env="testing")` — uses SQLite in-memory |
| `assert 401 == 201` | Use `headers={"X-API-Key": "test-key"}` (matches TestingConfig) |

### WebSocket Errors

| Error | Fix |
|-------|-----|
| WebSocket connection fails | Use `python run.py`, not `flask run` — flask CLI doesn't support WebSockets |

### Quick Reset (Start Over)

```bash
docker compose -f docker-compose.db.yml down -v
rm -rf .venv migrations/versions/*
touch migrations/versions/.gitkeep
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
docker compose -f docker-compose.db.yml up -d
flask db init && flask db migrate -m "initial" && flask db upgrade
python run.py
```

### "My App Won't Start" Checklist

1. ☐ Venv active? `which python`
2. ☐ Deps installed? `pip list | grep -i flask`
3. ☐ Postgres running? `docker compose -f docker-compose.db.yml ps`
4. ☐ In `api/` directory? `pwd`
5. ☐ `.env` exists? `cat .env`
6. ☐ Migrations run? `flask db upgrade`
7. ☐ Port 5000 free? `lsof -i :5000`
8. ☐ Read the actual error — what line in which file?
