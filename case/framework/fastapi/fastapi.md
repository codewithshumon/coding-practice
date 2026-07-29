# FastAPI — Complete Guide

> **Series:** Framework Documentation
> FastAPI — the modern, async, high-performance Python API framework. Related: `case/api/apis-and-communication.md` (REST §1–8), `case/database/databases.md` (PostgreSQL §1–11), `case/security/security-and-auth.md` (OAuth/JWT §9–24), `case/framework/django/django.md`.

---

## Table of Contents

- [1. What Is FastAPI?](#1-what-is-fastapi)
- [2. FastAPI vs Django vs Flask](#2-fastapi-vs-django-vs-flask)
- [3. How FastAPI Works](#3-how-fastapi-works)
- [4. Core Concepts and Features](#4-core-concepts-and-features)
- [5. Where to Use FastAPI](#5-where-to-use-fastapi)
- [6. Where NOT to Use FastAPI](#6-where-not-to-use-fastapi)
- [7. Installation and Setup](#7-installation-and-setup)
- [8. Project Structure and Configuration](#8-project-structure-and-configuration)
- [9. FastAPI Production Best Practices](#9-fastapi-production-best-practices)
- [10. FastAPI Real-World Examples](#10-fastapi-real-world-examples)
- [11. FastAPI Pitfalls](#11-fastapi-pitfalls)

---

## 1. What Is FastAPI?

**FastAPI** is a modern Python web framework for building **async, high-performance APIs** — with automatic OpenAPI docs, type-hint-driven validation, and dependency injection.

- Built on **Starlette** (ASGI) + **Pydantic** (validation) — fast, near Node.js/Go throughput.
- **Type hints are the API**: they drive validation, serialization, and docs.
- **Native async/await** — ideal for I/O-bound, concurrent workloads.

**One-liner:** the fast, async, type-driven Python API framework.

## 2. FastAPI vs Django vs Flask

| | FastAPI | Django | Flask |
|---|---|---|---|
| Async | Native, first-class | Partial | Limited |
| Performance | Very high | Moderate | Moderate |
| Validation/Docs | Auto (Pydantic + OpenAPI) | Via DRF | Manual/add-ons |
| Batteries | Minimal (API-focused) | Full-stack | Minimal |
| Best for | Async APIs, microservices | Full apps, admin/CMS | Small/custom apps |

**Rule of thumb:** FastAPI for **high-performance async APIs and microservices**; Django for **full-stack apps with admin/auth**; Flask for **minimal/custom**.

## 3. How FastAPI Works

- A **path operation** (`@app.get`, `@app.post`) maps a route to an async function.
- **Pydantic models** validate request bodies and shape responses automatically.
- **Dependency injection** (`Depends`) provides shared logic (DB sessions, auth, config).
- Runs on an **ASGI server** (Uvicorn) — true async concurrency for I/O-bound work.
- **Automatic OpenAPI** docs generated from type hints (`/docs`, `/redoc`).

## 4. Core Concepts and Features

| Concept | What it is |
|---|---|
| **Path operations** | Route decorators (`@app.get("/x")`) bound to functions |
| **Pydantic models** | Typed schemas — auto-validate request, serialize response |
| **Path/Query params** | Type-annotated, auto-parsed + validated |
| **Dependency injection** | `Depends()` for DB sessions, auth, reusable logic |
| **Async support** | `async def` endpoints — concurrent I/O |
| **Background tasks** | Run work after responding (FastAPI `BackgroundTasks`) |
| **Security utilities** | OAuth2/JWT helpers (`OAuth2PasswordBearer`) |
| **Auto OpenAPI** | Interactive docs at `/docs` (Swagger) and `/redoc` |

## 5. Where to Use FastAPI

- **High-throughput async APIs** (I/O-bound, many concurrent requests).
- **Microservices** — lightweight, fast, typed contracts.
- **AI/ML-serving APIs** (LLM endpoints, model inference) — async fits waiting on models.
- **APIs with rich validation/docs** needs.

## 6. Where NOT to Use FastAPI

- **Full-stack apps needing admin/auth/templates** (Django is better).
- **CPU-bound** work without offloading (async doesn't help CPU-bound; use workers/processes).
- When you need **server-rendered HTML/MVC** (FastAPI is API-focused).

## 7. Installation and Setup

```bash
pip install "fastapi[all]"     # FastAPI + Uvicorn + Pydantic
uvicorn main:app --reload      # http://localhost:8000, docs at /docs
```

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):           # validated request/response schema
    name: str
    price: float

@app.get("/items/{item_id}")
async def read_item(item_id: int):           # path param auto-parsed
    return {"item_id": item_id}

@app.post("/items", status_code=201)
async def create_item(item: Item):           # body auto-validated
    return item
```

## 8. Project Structure and Configuration

```
app/
├── main.py                # app instance, routers mounted
├── core/
│   ├── config.py          # settings (Pydantic BaseSettings, env)
│   └── security.py        # JWT/OAuth2 helpers
├── api/
│   └── routes/
│       ├── items.py       # APIRouter per domain
│       └── users.py
├── models/                # SQLAlchemy / data models
├── schemas/               # Pydantic request/response schemas
├── db/                    # session, engine, base
└── deps.py                # shared dependencies (DB, current_user)
```

- **Routers** (`APIRouter`) split endpoints by domain — mounted in `main.py`.
- **Pydantic `BaseSettings`** loads env config with validation.
- **Dependencies** in `deps.py` (e.g., `get_db`, `get_current_user`).

## 9. FastAPI Production Best Practices

1. **Run behind Uvicorn/Gunicorn workers** (not the dev `--reload` server) + a reverse proxy (nginx).
2. **Async everywhere for I/O** — use async DB drivers (`asyncpg`) and `httpx`; avoid blocking calls in async endpoints.
3. **Pydantic schemas** for all inputs — never trust raw request data.
4. **Dependency injection** for DB sessions, auth, config — testable and reusable.
5. **Offload CPU-bound/heavy work** to background tasks or a queue (don't block the event loop).
6. **Use `APIRouter`** to organize; keep endpoints thin (logic in services).
7. **Version APIs** (`/v1/`); document with the auto-generated OpenAPI.

## 10. FastAPI Real-World Examples

### Example 1 — Dependency Injection (DB session + auth)
```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.get("/items")
async def list_items(db: Session = Depends(get_db),
                     user: User = Depends(get_current_user)):
    return db.query(Item).all()
```
**Why:** shared, testable logic injected — swap mocks in tests easily.

### Example 2 — Async Concurrent Calls
```python
import httpx
@app.get("/aggregate")
async def aggregate():
    async with httpx.AsyncClient() as client:
        a, b = await asyncio.gather(
            client.get("https://api.a"), client.get("https://api.b"))
    return {"a": a.json(), "b": b.json()}
```
**Why:** both calls run concurrently — ~half the latency of sequential awaits.

### Example 3 — Background Task After Responding
```python
from fastapi import BackgroundTasks
@app.post("/send")
async def send(email: str, tasks: BackgroundTasks):
    tasks.add_task(send_email, email)   # runs after response sent
    return {"status": "queued"}
```
**Why:** respond instantly; the email sends without blocking the request.

## 11. FastAPI Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Blocking I/O in async endpoint | Event loop stalls, throughput drops | Use async libs (`httpx`, `asyncpg`) |
| CPU-bound work in async | Blocks all requests | Offload to worker/queue |
| No Pydantic validation | Bad data reaches logic | Type every input with schemas |
| `def` (sync) endpoints everywhere | No async benefit | Use `async def` for I/O |
| Logic in endpoints | Untestable, repeated | Move to services; inject via `Depends` |
| Running dev server in prod | Slow, single-process | Uvicorn/Gunicorn workers + nginx |
