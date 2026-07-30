# Flask — Complete Guide

> **Series:** Framework Documentation
> Flask — Python's minimal, unopinionated microframework. Related: `case/framework/django/django.md` (the batteries-included alternative), `case/framework/fastapi/fastapi.md` (the async alternative), `case/api/apis-and-communication.md` (REST §1–8), `case/security/security-and-auth.md` (OAuth/JWT §9–24).

---

## Table of Contents

- [1. What Is Flask?](#1-what-is-flask)
- [2. Flask vs Django vs FastAPI](#2-flask-vs-django-vs-fastapi)
- [3. How Flask Works](#3-how-flask-works)
- [4. Core Concepts and Features](#4-core-concepts-and-features)
- [5. Where to Use Flask](#5-where-to-use-flask)
- [6. Where NOT to Use Flask](#6-where-not-to-use-flask)
- [7. Installation and Setup](#7-installation-and-setup)
- [8. Project Structure and Configuration](#8-project-structure-and-configuration)
- [9. Flask Production Best Practices](#9-flask-production-best-practices)
- [10. Flask Real-World Examples](#10-flask-real-world-examples)
- [11. Flask Pitfalls](#11-flask-pitfalls)

---

## 1. What Is Flask?

**Flask** is a **minimal, unopinionated Python web framework** — a "microframework" that provides routing, request/response handling, and templating, leaving everything else (ORM, auth, forms, validation) to **extensions** you choose.

- **Micro by design** — the core is tiny; you compose your stack via extensions.
- **WSGI-based** (Waitress/Gunicorn), sync by default (async views supported since 2.0).
- **Jinja2** templating and **Werkzeug** routing/debugging are built in.
- The original Python microframework — huge ecosystem, lots of flexibility.

**One-liner:** Python's minimal microframework — you bring the architecture and extensions.

## 2. Flask vs Django vs FastAPI

| | Flask | Django | FastAPI |
|---|---|---|---|
| Philosophy | Minimal/unopinionated | Batteries-included | Modern async API-first |
| ORM/Auth | Via extensions (SQLAlchemy, Flask-Login) | Built-in | Via extensions |
| Async | Limited (sync-first, WSGI) | Partial | Native, first-class |
| Validation/Docs | Manual / add-ons | Via DRF | Auto (Pydantic + OpenAPI) |
| Best for | Small/custom apps, full control | Full apps, admin/CMS | High-performance async APIs |

**Rule of thumb:** Flask for **small-to-medium apps where you want full control and a custom stack**; Django for **batteries-included full apps**; FastAPI for **async, high-throughput APIs with auto docs**.

## 3. How Flask Works

- A **request** enters via the WSGI server → Flask's **app** routes it to a **view function**.
- **Routing** maps URL rules (with converters like `<int:id>`) to Python functions.
- **Contexts** — Flask makes `request` and `current_app` available as thread-locals during a request.
- **View functions** return a response (string, dict-as-JSON, rendered template, or `Response`).
- **Extensions** register themselves on the app and hook into the request lifecycle.

## 4. Core Concepts and Features

| Concept | What it is |
|---|---|
| **App** (`Flask(__name__)`) | The application instance |
| **Routing** | `@app.route("/x/<int:id>")` binds URLs to view functions |
| **View functions** | Plain Python functions handling a request |
| **Request/Response** | `request` (form, args, json, headers), `jsonify`, `render_template` |
| **Jinja2 templates** | Server-rendered HTML (`render_template`) |
| **Blueprints** | Modular route grouping (`flask.Blueprint`) |
| **Application factory** | `create_app()` pattern for config/test isolation |
| **Extensions** | Flask-SQLAlchemy, Flask-Login, Flask-Migrate, Flask-WTF, Flask-RESTful |
| **Contexts** | Application context + request context (thread-locals) |
| **CLI** | `flask run`, custom commands via `@app.cli` |

## 5. Where to Use Flask

- **Small-to-medium apps** where minimal is enough.
- **Custom stacks** — you want to pick your own ORM/auth/validator.
- **Internal tools, simple APIs, prototypes, MVPs**.
- **Adding a web layer to existing Python code** (Flask is lightweight to adopt).

## 6. Where NOT to Use Flask

- **Full apps needing admin/auth/ORM out of the box** → Django.
- **High-throughput async APIs** → FastAPI (Flask is sync/WSGI-first).
- **Large teams needing enforced structure** → Django or FastAPI + strict conventions.

## 7. Installation and Setup

```bash
pip install flask
flask --app app run --debug      # http://localhost:5000
```

```python
# app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.get("/items/<int:item_id>")
def get_item(item_id):                # URL converter → typed arg
    return jsonify({"id": item_id})

@app.post("/items")
def create_item():
    data = request.get_json()         # parse JSON body (validate yourself!)
    return jsonify(data), 201

if __name__ == "__main__":
    app.run(debug=True)
```

## 8. Project Structure and Configuration

```
app/
├── __init__.py            # application factory: create_app()
├── config.py              # config classes (Dev/Prod), env-driven
├── extensions.py          # db = SQLAlchemy(), login_manager = LoginManager()
├── auth/
│   ├── routes.py          # Blueprint (auth_bp)
│   └── models.py
├── api/
│   └── routes.py          # Blueprint (api_bp)
├── templates/             # Jinja2 HTML
└── models.py              # SQLAlchemy models
```

- **Application factory** (`create_app()`) — the idiomatic pattern; config-driven, test-friendly.
- **Blueprints** modularize routes; **extensions** instantiated once, init'd on the app.
- **Config via classes/env** (`app.config.from_object`, `from_envvar`); secrets from env, never committed.

## 9. Flask Production Best Practices

1. **Use the application factory** (`create_app()`) — config/test isolation.
2. **Run behind a WSGI server** (Gunicorn/Waitress) + reverse proxy (nginx), never the dev server.
3. **Validate all input** — Flask does no validation; use a schema lib (marshmallow/pydantic).
4. **Blueprints + services** — keep view functions thin; logic in service modules.
5. **Secrets from env** (`SECRET_KEY`, DB URL); `debug=False` in production.
6. **Use Flask-Migrate** (Alembic) for DB schema migrations.
7. **Offload heavy work** to a task queue (Celery) — don't block WSGI workers.
8. **Type-hint + lint** (mypy, ruff) — Flask doesn't enforce types or structure for you.

## 10. Flask Real-World Examples

### Example 1 — Application Factory + Blueprint
```python
# app/__init__.py
from flask import Flask
from .extensions import db

def create_app(config="app.config.ProdConfig"):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    from .api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    return app

# app/api/routes.py
from flask import Blueprint, jsonify
api_bp = Blueprint("api", __name__)

@api_bp.get("/items")
def list_items():
    return jsonify([{"id": 1}])
```
**Why:** config-driven app creation, modular routes, testable (create a fresh app per test).

### Example 2 — Validated Input (marshmallow)
```python
from marshmallow import Schema, fields, ValidationError

class ItemSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True, validate=lambda n: n > 0)

@api_bp.post("/items")
def create_item():
    try:
        data = ItemSchema().load(request.get_json())   # validated + typed
    except ValidationError as e:
        return jsonify(e.messages), 400
    return jsonify(data), 201
```
**Why:** Flask won't validate for you — a schema library prevents bad data reaching logic.

### Example 3 — SQLAlchemy Model + Query
```python
# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# app/models.py
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

# query
Item.query.filter_by(name="Widget").all()
```
**Why:** Flask-SQLAlchemy adds ORM support without Django's batteries — you opt in.

## 11. Flask Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| No input validation | Bad/injected data | Schema lib (marshmallow/pydantic) |
| Dev server in production | Slow, single-process, leaks | Gunicorn/Waitress + nginx |
| Logic in view functions | Untestable, repeated | Move to services |
| `debug=True` in prod | Code execution / info leak | `debug=False`, env-driven config |
| Sync I/O blocking workers | Slow under load | Async tasks (Celery) / consider FastAPI |
| Global state / no factory | Config + test isolation issues | Application factory pattern |
| Treating it like Django | Reinventing auth/ORM poorly | Use established extensions |
