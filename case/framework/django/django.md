# Django — Complete Guide

> **Series:** Framework Documentation
> Django + Django REST Framework (DRF) — the batteries-included Python web framework. Related: `case/database/databases.md` (PostgreSQL §1–11, Database Optimization §45–55), `case/api/apis-and-communication.md` (REST §1–8), `case/security/security-and-auth.md` (Auth §9–24), `case/structures-architecture/design-patterns.md` (MVT §13–18).

---

## Table of Contents

- [1. What Is Django?](#1-what-is-django)
- [2. Django vs Flask vs FastAPI](#2-django-vs-flask-vs-fastapi)
- [3. How Django Works](#3-how-django-works)
- [4. Core Concepts and Features](#4-core-concepts-and-features)
- [5. Where to Use Django](#5-where-to-use-django)
- [6. Where NOT to Use Django](#6-where-not-to-use-django)
- [7. Installation and Setup](#7-installation-and-setup)
- [8. Project Structure and Configuration](#8-project-structure-and-configuration)
- [9. Django Production Best Practices](#9-django-production-best-practices)
- [10. Django Real-World Examples](#10-django-real-world-examples)
- [11. Django Pitfalls](#11-django-pitfalls)

---

## 1. What Is Django?

**Django** is a high-level Python web framework that encourages rapid development and clean, pragmatic design — with a **batteries-included** philosophy: ORM, admin panel, authentication, forms, templating, and security built in.

- "Batteries included" — most of what a web app needs ships with Django.
- **DRF (Django REST Framework)** adds powerful, flexible REST API tooling on top.
- Convention-over-configuration: a clear, opinionated structure that scales from prototype to production.

**One-liner:** the batteries-included Python web framework — build full apps fast, with security and structure by default.

## 2. Django vs Flask vs FastAPI

| | Django | Flask | FastAPI |
|---|---|---|---|
| Philosophy | Batteries-included | Micro, minimal | Modern async API-first |
| ORM | Built-in | Add-on (SQLAlchemy) | Add-on (SQLAlchemy/Tortoise) |
| Admin panel | Built-in | None | None |
| Async | Partial (improving) | Limited | Native, first-class |
| Best for | Full apps, content platforms, CMS | Small/custom apps | High-performance async APIs |

**Rule of thumb:** Django for **full apps where the batteries save time** (admin, auth, ORM, forms); FastAPI for **async, high-throughput APIs**; Flask for **minimal, highly customized** apps.

## 3. How Django Works

- **MVT pattern** (Model–View–Template): Models define data (ORM), Views contain logic, Templates render HTML.
- A **request** flows: URLconf routes → View → (Model/ORM for data) → Template/JSON response.
- The **ORM** translates Python objects into SQL — no raw queries needed for most operations.
- **Middleware** wraps request/response processing (auth, sessions, CSRF, security).
- **Migrations** evolve the DB schema in version-controlled steps.

## 4. Core Concepts and Features

| Concept | What it is |
|---|---|
| **Models / ORM** | Python classes → DB tables; query via Python, not SQL |
| **Migrations** | Version-controlled schema changes (`makemigrations`/`migrate`) |
| **Views** | Request handlers — functions (FBV) or classes (CBV) |
| **URLconf** | URL → view mapping (`urls.py`) |
| **Templates** | HTML rendering (Django Template Language) |
| **Admin** | Auto-generated CRUD admin panel for models |
| **Forms** | Validation + rendering of HTML forms |
| **Auth** | Built-in users, groups, permissions, login/logout |
| **Middleware** | Cross-cutting request/response processing |
| **Signals** | Decoupled event hooks (`post_save`, etc.) |
| **DRF** | Serializers, viewsets, authentication classes, browsable API |

## 5. Where to Use Django

- **Content/platform apps** — CMS, blogs, e-commerce, social platforms (the admin + ORM accelerate these).
- **Apps needing an admin panel** out of the box.
- **Rapid prototyping → production** in the same framework.
- **Internal tools and dashboards** (admin shines here).

## 6. Where NOT to Use Django

- **Async-heavy / real-time** (WebSockets, streaming) — FastAPI or async-native fits better.
- **Microservices needing tiny footprints** — Django is full-stack; a micro framework may be lighter.
- **No ORM / custom SQL-heavy** apps where the ORM gets in the way.

## 7. Installation and Setup

```bash
pip install django djangorestframework
django-admin startproject myproject && cd myproject
python manage.py startapp blog
python manage.py makemigrations && python manage.py migrate
python manage.py createsuperuser
python manage.py runserver        # http://localhost:8000
```

```python
# blog/models.py
from django.db import models
class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

# blog/admin.py  — instant admin CRUD
from django.contrib import admin
from .models import Post
admin.site.register(Post)
```

## 8. Project Structure and Configuration

```
myproject/
├── manage.py                 # CLI entry point
├── myproject/                # project package
│   ├── settings.py           # config (DB, apps, middleware, security)
│   ├── urls.py               # root URL routing
│   └── wsgi.py / asgi.py     # deployment entry points
└── blog/                     # an "app" (feature module)
    ├── models.py  views.py  urls.py  admin.py  serializers.py
    └── migrations/
```

- **Apps** are feature modules (blog, users, shop) — compose many into one project.
- **`settings.py`** holds all config: `INSTALLED_APPS`, `MIDDLEWARE`, DB, `SECRET_KEY`, security flags.
- **Split settings** for environments (`base.py` / `dev.py` / `prod.py`) in real projects.

## 9. Django Production Best Practices

1. **Never commit `SECRET_KEY`** — load from env; set `DEBUG=False` in prod.
2. **Use `select_related`/`prefetch_related`** to kill N+1 queries (see `database/databases.md` §45–55).
3. **Index hot query fields**; use `EXPLAIN` on slow queries.
4. **Cache** expensive views/fragments (Redis — see `caching/caching.md`).
5. **DRF**: use serializers for validation, viewsets for CRUD, permissions for authz.
6. **Keep business logic out of views** — services/domain layer.
7. **Run with a real server** (gunicorn/uvicorn) behind nginx; use a managed DB.
8. **Security defaults on**: CSRF, clickjacking, SSL redirect, HSTS.

## 10. Django Real-World Examples

### Example 1 — DRF REST API (ViewSet + Serializer)
```python
# blog/serializers.py
class PostSerializer(serializers.ModelSerializer):
    class Meta: model = Post; fields = "__all__"

# blog/views.py
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# blog/urls.py
router = routers.DefaultRouter()
router.register("posts", PostViewSet)
urlpatterns = router.urls
```
**Why:** full CRUD REST API in ~10 lines, with auth, validation, and a browsable UI.

### Example 2 — Fixing N+1
```python
# Bad: 1 + N queries
for p in Post.objects.all(): print(p.author.name)
# Good: JOIN in one query
Post.objects.select_related("author").all()
```
**Why:** turns N+1 into a single JOINed query.

### Example 3 — Cached Expensive View
```python
from django.views.decorators.cache import cache_page
@cache_page(60 * 5)   # cache for 5 minutes
def dashboard(request): ...
```
**Why:** heavy dashboard renders once per TTL, not per request.

## 11. Django Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| N+1 queries | Slow list views | `select_related`/`prefetch_related` |
| Fat views | Logic in HTTP handlers | Move to services/domain |
| `DEBUG=True` in prod | Info leak, security risk | `DEBUG=False`, env config |
| Blocking I/O in views | Slow under load | Offload to task queue (Celery) |
| Over-fetching via serializers | Huge payloads | `fields = [...]`, not `__all__` for big models |
| Treating ORM as SQL replacement blindly | Inefficient queries | `EXPLAIN`, watch for N+1/seq scans |
