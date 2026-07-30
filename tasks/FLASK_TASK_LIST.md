# Flask Learning Lab — Step-by-Step Task Checklist

> **How to use:** Each step creates ONE file (or a small, related group). Work top to bottom.
> After every step, run `flask --app run run --debug` (or `python run.py`) and test with curl or browser.

---

## Phase 0 — Project on Its Feet (Scaffold + First Route)

### Step 0.1: Create the project folder and virtualenv
```bash
mkdir api && cd api
python -m venv .venv
source .venv/bin/activate
```
**What you get:** An isolated Python environment so dependencies don't leak between projects.

### Step 0.2: Create `run.py` — a working "Hello World" app
```python
from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def hello():
    return jsonify({"message": "Hello World!"})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
```

### Step 0.3: Verify it runs
```bash
python run.py
```
Open [http://localhost:5000](http://localhost:5000). You should see `{"message": "Hello World!"}`.

### Step 0.4: Understand the moving parts

| Piece | What it does |
|------|-------------|
| `Flask(__name__)` | The application object — the registry of everything the app uses |
| `@app.get("/")` | A route — GET on `/` returns a message |
| `jsonify()` | Turns a Python dict into a JSON response |
| `app.run()` | Entry point — starts the dev server |

**Request flow:** Browser → `run.py` → `Flask` app → route function `hello()` → "Hello World!"

### Step 0.5: Install ALL packages you'll need
```bash
pip install flask flask-sqlalchemy psycopg2-binary python-dotenv pydantic flask-pydantic flask-bcrypt flask-socketio flasgger
pip freeze > requirements.txt
```
**Why now:** One install, never stop mid-build again.

### Step 0.6: Create `.env`
```
PORT=5000
```
**Where:** `api/.env` (project root)
**Why:** We'll wire config next.

### Step 0.7: Create `config.py` — settings loaded from `.env`
```python
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    PORT = int(os.getenv("PORT", 5000))
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
        f"@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}"
        f"/{os.getenv('DATABASE_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY = os.getenv("API_KEY")
    ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")
```
**Why:** One class holds every setting. Never hardcode the port or DB credentials in route code — they come from `.env` via this config object.

### Step 0.8: Refactor to the app-factory pattern — `app/__init__.py`
**Why:** Flask's version of NestJS's `AppModule`. A factory function builds and configures the app — required once you add extensions (SQLAlchemy, SocketIO) to avoid circular imports.
```bash
mkdir app
```
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

from config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ── Extensions ──
    db.init_app(app)
    Swagger(app, template={
        "info": {
            "title": "Flask Learning API",
            "description": "Learning Flask routing concepts",
            "version": "1.0",
        }
    })

    # ── Routes ──
    from app.modules.items.routes import items_bp
    app.register_blueprint(items_bp)

    return app
```
**Why each block:**
- `db = SQLAlchemy()` at module level, `db.init_app(app)` inside the factory — create the extension once, attach it to the app later (avoids circular imports)
- `Swagger` — flasgger gives you interactive API docs at `/apidocs`, like FastAPI's `/docs`
- `register_blueprint` — Flask's version of registering a module/controller

New `run.py`:
```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=app.config["PORT"], debug=True)
```

### Step 0.9: Test
```bash
python run.py
```
- [http://localhost:5000](http://localhost:5000) → 404 for now (no blueprint yet) — create a stub `app/modules/items/routes.py`:
```bash
mkdir -p app/modules/items
touch app/__init__.py  # already exists; ensure app/modules/__init__.py and app/modules/items/__init__.py exist
```
```python
from flask import Blueprint, jsonify

items_bp = Blueprint("items", __name__, url_prefix="/items")


@items_bp.get("/health")
def health():
    return jsonify({"message": "Hello World!"})
```
- [http://localhost:5000/items/health](http://localhost:5000/items/health) → `{"message": "Hello World!"}`
- [http://localhost:5000/apidocs](http://localhost:5000/apidocs) → Swagger UI (mostly empty)

---

## Phase 1 — Docker + Database Connection

### Step 1.1: Create `docker-compose.yml`
**Where:** `api/docker-compose.yml`
```yaml
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

volumes:
  pgdata:
```
**Why:** Same setup as your other projects, just different credentials (`flask`/`flask`/`flask_learn`) and ports so containers don't collide.

### Step 1.2: Start the database
```bash
docker compose up -d
docker compose ps   # verify both containers are running
```

### Step 1.3: Update `.env` — add database credentials
```
PORT=5000
DATABASE_HOST=localhost
DATABASE_PORT=5600
DATABASE_USER=flask
DATABASE_PASSWORD=flask
DATABASE_NAME=flask_learn
```
**Why port 5600:** Your docker-compose maps host `5600` to container `5432`, avoiding conflicts with the Postgres instances from your FastAPI (5400) / NestJS (5500) projects.

### Step 1.4: Auto-create tables on startup (dev only)
In `app/__init__.py`, inside `create_app`, after registering blueprints:
```python
    # ── Create tables (DEV ONLY — use Flask-Migrate/Alembic in production) ──
    with app.app_context():
        db.create_all()
```
**Why:** `db.create_all()` reads your model classes and creates missing tables automatically — Flask-SQLAlchemy's equivalent of TypeORM's `synchronize: true`. In production you use migrations.

### Step 1.5: Test database connection
```bash
python run.py
```
If there's no error about database connection, Phase 1 is done. (No models exist yet, so no tables are created — that comes next.)

---

## Phase 2 — Your First CRUD (Items)

### Step 2.1: Create `app/common/models/base.py`
**Why:** Every table gets `id`, `created_at`, `updated_at`, `deleted_at` for free. Write once, reuse forever.
```bash
mkdir -p app/common/models app/common/utils
touch app/common/__init__.py app/common/models/__init__.py
```
```python
from datetime import datetime, timezone

from app import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def to_dict(self):
        return {
            c.name: (getattr(self, c.name).isoformat()
                     if isinstance(getattr(self, c.name), datetime)
                     else getattr(self, c.name))
            for c in self.__table__.columns
        }
```

### Step 2.2: Create the Item model — `app/modules/items/models.py`
```python
from app import db
from app.common.models.base import BaseModel


class Item(BaseModel):
    __tablename__ = "items"

    name = db.Column(db.String(255), nullable=False, index=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    in_stock = db.Column(db.Boolean, nullable=False, default=True)
```
**Why this structure:**
- `__tablename__ = "items"` — maps this class to the `items` table in Postgres
- `extends BaseModel` — inherits `id`, `created_at`, `updated_at`, `deleted_at` for free
- `db.Column(...)` — each attribute becomes a database column
- Python is snake_case everywhere, so `in_stock` is the same in code and in the DB (no camelCase translation like NestJS)

### Step 2.3: Create the schemas — `app/modules/items/schemas.py`
**Why:** Pydantic models are Flask's DTOs — they define and validate what the client sends.
```python
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class CreateItemSchema(BaseModel):
    name: str = Field(..., max_length=255, examples=["Laptop"])
    price: Decimal = Field(..., ge=0, examples=[999.99])
    description: Optional[str] = Field(None, max_length=1000)
    in_stock: Optional[bool] = True


class UpdateItemSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    price: Optional[Decimal] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=1000)
    in_stock: Optional[bool] = None
```
**Why each piece:**
- `Field(..., max_length=255)` — required field, rejects strings over 255 chars (like `@MaxLength`)
- `ge=0` — rejects negative prices (like `@Min(0)`)
- `Optional[...] = None` — field can be omitted entirely (like `@IsOptional()`)
- `UpdateItemSchema` with all-optional fields — Flask's version of `PartialType()`

### Step 2.4: Create the service — `app/modules/items/service.py`
**Why:** Services hold business logic. Routes only handle HTTP — they call services.
```python
from sqlalchemy import select

from app import db
from app.modules.items.models import Item
from app.modules.items.schemas import CreateItemSchema, UpdateItemSchema


class ItemNotFoundError(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id
        super().__init__(f"Item {item_id} not found")


def create_item(data: CreateItemSchema) -> Item:
    item = Item(**data.model_dump(exclude_unset=True))
    db.session.add(item)
    db.session.commit()
    return item


def get_all_items() -> list[Item]:
    return db.session.scalars(
        select(Item).where(Item.deleted_at.is_(None)).order_by(Item.created_at.desc())
    ).all()


def get_item(item_id: int) -> Item:
    item = db.session.get(Item, item_id)
    if item is None or item.deleted_at is not None:
        raise ItemNotFoundError(item_id)
    return item


def update_item(item_id: int, data: UpdateItemSchema) -> Item:
    item = get_item(item_id)  # reuses get_item (which raises 404)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)  # merges schema fields into item
    db.session.commit()
    return item


def delete_item(item_id: int) -> None:
    from datetime import datetime, timezone

    item = get_item(item_id)
    item.deleted_at = datetime.now(timezone.utc)  # soft delete — sets deleted_at, doesn't actually delete
    db.session.commit()
```
**Key patterns:**
- `db.session` — Flask-SQLAlchemy's unit of work; add objects, then `commit()` (like the TypeORM repository's `save()`)
- Soft delete — set `deleted_at` instead of removing the row, and filter it out of every query
- `get_item` reuses itself — `update_item` and `delete_item` call it so 404 logic lives in one place

### Step 2.5: Create the routes — `app/modules/items/routes.py`
**Why:** The blueprint translates HTTP requests into service calls.
```python
from flask import Blueprint, jsonify
from flask_pydantic import validate
from pydantic import ValidationError

from app.modules.items import service
from app.modules.items.schemas import CreateItemSchema, UpdateItemSchema

items_bp = Blueprint("items", __name__, url_prefix="/items")


@items_bp.errorhandler(service.ItemNotFoundError)
def handle_not_found(err):
    return jsonify({"error": str(err)}), 404


@items_bp.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify({"error": "Validation failed", "details": err.errors()}), 400


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
**Key patterns:**
- `url_prefix="/items"` — every route in this blueprint starts with `/items`
- `<int:item_id>` — extracts `item_id` from the URL AND validates it's an integer (like `ParseIntPipe`)
- `@validate()` (flask-pydantic) — parses and validates the request body against the schema; injects it as the `body` argument
- `201` on POST, `204` with empty body on DELETE — same status-code discipline as NestJS's `@HttpCode`

### Step 2.6: The blueprint is already registered — verify imports
In `app/__init__.py` you already have:
```python
from app.modules.items.routes import items_bp
app.register_blueprint(items_bp)
```
Also make sure models are imported so `db.create_all()` sees them — add inside `create_app`, before `db.create_all()`:
```python
    from app.modules.items import models  # noqa: F401 — registers models with SQLAlchemy
```

### Step 2.7: Test full CRUD
```bash
# Create
curl -X POST http://localhost:5000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99}'

curl -X POST http://localhost:5000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Phone", "price": 699.00}'

# List
curl http://localhost:5000/items/

# Get one
curl http://localhost:5000/items/1

# Update
curl -X PATCH http://localhost:5000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Gaming Laptop"}'

# Delete
curl -X DELETE http://localhost:5000/items/1

# List again — item 1 is gone
curl http://localhost:5000/items/

# Open Swagger: http://localhost:5000/apidocs
```

### Step 2.8: Check the database
```bash
docker exec flask-postgres psql -U flask -d flask_learn -c "SELECT * FROM items;"
```
Notice the soft-deleted item still exists — it just has a `deleted_at` timestamp.

---

## Phase 3 — Query Parameters & Pagination

### Step 3.1: Add a filter schema — `app/modules/items/schemas.py`
**Why:** Separate schema for GET query parameters. Pagination defaults plus filter fields.
```python
class FilterItemSchema(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)
    name: Optional[str] = Field(None, description="Search by name (case-insensitive)")
    max_price: Optional[Decimal] = Field(None, ge=0)
    in_stock: Optional[bool] = None

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
```
**Why no type-coercion decorator:** Pydantic converts `"2"` → `2` and `"true"` → `True` automatically — no `@Type(() => Number)` needed like in class-validator.

### Step 3.2: Update `service.py` — add filter + pagination function
```python
def get_filtered_items(filters) -> dict:
    stmt = select(Item).where(Item.deleted_at.is_(None))

    if filters.name:
        stmt = stmt.where(Item.name.ilike(f"%{filters.name}%"))
    if filters.max_price is not None:
        stmt = stmt.where(Item.price <= filters.max_price)
    if filters.in_stock is not None:
        stmt = stmt.where(Item.in_stock == filters.in_stock)

    total = db.session.scalar(
        select(db.func.count()).select_from(stmt.subquery())
    )
    items = db.session.scalars(
        stmt.order_by(Item.created_at.desc())
        .offset(filters.offset)
        .limit(filters.page_size)
    ).all()
    return {"items": [i.to_dict() for i in items], "total": total}
```

### Step 3.3: Update `routes.py` — replace list_items with filtered version
```python
from app.modules.items.schemas import FilterItemSchema


@items_bp.get("/")
@validate()
def list_items(query: FilterItemSchema):
    return jsonify(service.get_filtered_items(query))
```
`@validate()` maps query params into `query:` when the schema is used that way.

### Step 3.4: Test pagination and filtering
```bash
curl "http://localhost:5000/items/?page=1&page_size=2"
curl "http://localhost:5000/items/?name=phone"
curl "http://localhost:5000/items/?max_price=500&in_stock=true"
curl "http://localhost:5000/items/?page_size=200"   # 400 — validation error
```

---

## Phase 4 — Validation & Error Handling

### Step 4.1: Global error handlers — `app/common/errors.py`
**Why:** Flask has no global ValidationPipe — instead you register error handlers once on the app, and they catch validation/404 errors from every blueprint.
```python
from flask import jsonify
from pydantic import ValidationError


def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        return jsonify({"error": "Validation failed", "details": err.errors()}), 400

    @app.errorhandler(404)
    def handle_404(err):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def handle_500(err):
        return jsonify({"error": "Internal server error"}), 500
```
In `app/__init__.py`, inside `create_app`:
```python
    from app.common.errors import register_error_handlers
    register_error_handlers(app)
```
(You can now delete the blueprint-level `ValidationError` handler from Step 2.5 — the global one covers it.)
**Why:** One place catches every validation error app-wide — the Flask equivalent of `app.useGlobalPipes(new ValidationPipe(...))`.

### Step 4.2: Test validation
```bash
curl -X POST http://localhost:5000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": ""}'     # 400 — price missing

curl -X POST http://localhost:5000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","price":10,"hacked":true}'
```
**Note:** Pydantic ignores unknown fields by default (NestJS's `whitelist` behavior). To reject them like `forbidNonWhitelisted`, add to each schema:
```python
    model_config = {"extra": "forbid"}
```

---

## Phase 5 — Users Module (Password Hashing)

### Step 5.1: Create `app/modules/users/models.py`
```bash
mkdir -p app/modules/users
touch app/modules/users/__init__.py
```
```python
from app import db
from app.common.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
```

### Step 5.2: Create `app/modules/users/schemas.py`
```python
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class CreateUserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=100, examples=["alice"])
    email: EmailStr = Field(..., examples=["alice@example.com"])
    password: str = Field(..., min_length=8, examples=["password123"])  # plain text → hashed before DB
    is_admin: Optional[bool] = False


class UpdateUserSchema(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    is_admin: Optional[bool] = None
```
(`EmailStr` needs `pip install email-validator` — add it to requirements.)

### Step 5.3: Create password helper — `app/common/utils/password.py`
Flask-Bcrypt is set up once in `app/__init__.py`:
```python
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
# inside create_app:
bcrypt.init_app(app)
```
```python
from app import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.generate_password_hash(password).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.check_password_hash(hashed, password)
```

### Step 5.4: Create `app/modules/users/service.py`
```python
from sqlalchemy import select

from app import db
from app.common.utils.password import hash_password
from app.modules.users.models import User


class UserNotFoundError(Exception):
    pass


class EmailConflictError(Exception):
    pass


def create_user(data) -> User:
    existing = db.session.scalar(select(User).where(User.email == data.email))
    if existing:
        raise EmailConflictError("Email already registered")

    fields = data.model_dump(exclude={"password"}, exclude_unset=True)
    user = User(**fields, hashed_password=hash_password(data.password))
    db.session.add(user)
    db.session.commit()
    return user


def get_all_users() -> list[User]:
    return db.session.scalars(select(User).where(User.deleted_at.is_(None))).all()


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
    from datetime import datetime, timezone

    user = get_user(user_id)
    user.deleted_at = datetime.now(timezone.utc)
    db.session.commit()
```
**Why the password dance:** Client sends `password` (plain text). DB stores `hashed_password`. The service hashes it between receiving and saving.

### Step 5.5: Create `app/modules/users/routes.py`
```python
from flask import Blueprint, jsonify
from flask_pydantic import validate

from app.modules.users import service
from app.modules.users.schemas import CreateUserSchema, UpdateUserSchema

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.errorhandler(service.UserNotFoundError)
def handle_not_found(err):
    return jsonify({"error": str(err)}), 404


@users_bp.errorhandler(service.EmailConflictError)
def handle_conflict(err):
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

### Step 5.6: Register the blueprint in `app/__init__.py`
```python
from app.modules.users.routes import users_bp
app.register_blueprint(users_bp)

from app.modules.users import models  # noqa: F401 — before db.create_all()
```

### Step 5.7: Test
```bash
curl -X POST http://localhost:5000/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"password123"}'

curl http://localhost:5000/users/
```

---

## Phase 6 — API Key Auth (before-request hook)

### Step 6.1: Update `.env` — add API keys
```
PORT=5000
DATABASE_HOST=localhost
DATABASE_PORT=5600
DATABASE_USER=flask
DATABASE_PASSWORD=flask
DATABASE_NAME=flask_learn
API_KEY=dev-api-key
ADMIN_API_KEY=dev-admin-key
```

### Step 6.2: Create `app/common/auth.py`
```python
from flask import current_app, g, jsonify, request

# Routes that skip auth (health checks, docs)
EXEMPT_PATHS = ("/apidocs", "/flasgger_static", "/apispec")


def require_api_key():
    if request.path.startswith(EXEMPT_PATHS):
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

### Step 6.3: Apply globally in `app/__init__.py`
Inside `create_app`:
```python
    from app.common.auth import require_api_key
    app.before_request(require_api_key)
```
**Why `before_request`:** This runs before EVERY route automatically — Flask's equivalent of registering a guard with `APP_GUARD`. No decorator needed on every blueprint.

### Step 6.4: Test auth
```bash
curl http://localhost:5000/items/                                # 401 — no key
curl -H "X-API-Key: wrong" http://localhost:5000/items/          # 401 — wrong key
curl -H "X-API-Key: dev-api-key" http://localhost:5000/items/    # 200
curl -H "X-API-Key: dev-admin-key" http://localhost:5000/items/  # 200 (admin key also works)
```

---

## Phase 7 — Headers, Cookies, Status Codes, Form/Files

These are small, self-contained blueprints. Each follows the same pattern: `mkdir`, create `routes.py`, register in `create_app`.

### Step 7.1: Headers & Cookies — `app/modules/demo/`
```bash
mkdir -p app/modules/demo
touch app/modules/demo/__init__.py
```

`app/modules/demo/routes.py`:
```python
from flask import Blueprint, jsonify, make_response, request

demo_bp = Blueprint("demo", __name__, url_prefix="/demo")


@demo_bp.get("/whoami")
def whoami():
    return jsonify({"userAgent": request.headers.get("User-Agent")})


@demo_bp.get("/read-cookie")
def read_cookie():
    return jsonify({"sessionId": request.cookies.get("session_id", "none")})


@demo_bp.get("/set-cookie")
def set_cookie():
    resp = make_response(jsonify({"message": "Cookie set!"}))
    resp.set_cookie("session_id", "abc-123", httponly=True, max_age=3600)
    return resp


@demo_bp.get("/set-headers")
def set_headers():
    resp = make_response(jsonify({"message": "Headers set!"}))
    resp.headers["X-Custom"] = "hello"
    return resp
```

Register in `create_app`, then test:
```bash
curl -H "X-API-Key: dev-api-key" -H "User-Agent: MyApp" http://localhost:5000/demo/whoami
curl -H "X-API-Key: dev-api-key" -b "session_id=test123" http://localhost:5000/demo/read-cookie
curl -H "X-API-Key: dev-api-key" -v http://localhost:5000/demo/set-cookie
```

### Step 7.2: Status Codes — add to the same blueprint
```python
@demo_bp.post("/created")
def created():
    return jsonify({"id": 1}), 201


@demo_bp.delete("/removed")
def removed():
    return "", 204


@demo_bp.get("/redirect")
def redirect_demo():
    from flask import redirect
    return redirect("/items/", code=301)
```

Test: `curl -v -H "X-API-Key: dev-api-key" http://localhost:5000/demo/redirect`

### Step 7.3: Form Data & File Uploads — `app/modules/formfiles/`
```bash
mkdir -p app/modules/formfiles uploads
touch app/modules/formfiles/__init__.py
```
```python
import os

from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename

formfiles_bp = Blueprint("formfiles", __name__, url_prefix="/form-files")


@formfiles_bp.post("/login")
def login():
    return jsonify({"username": request.form.get("username")})


@formfiles_bp.post("/upload")
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided"}), 400
    filename = secure_filename(file.filename)
    file.save(os.path.join("uploads", filename))
    return jsonify({"filename": file.filename, "size": os.path.getsize(f"uploads/{filename}")})
```

Register in `create_app`. Test:
```bash
curl -X POST http://localhost:5000/form-files/login -H "X-API-Key: dev-api-key" -d "username=alice&password=pass"
curl -X POST http://localhost:5000/form-files/upload -H "X-API-Key: dev-api-key" -F "file=@test.txt"
```

---

## Phase 8 — Response Wrapper (Standardized API Responses)

### Step 8.1: Create an after-request hook — `app/common/response_wrapper.py`
**Why:** Flask's version of a global interceptor — wraps every JSON response in a standard envelope.
```python
from datetime import datetime, timezone

from flask import jsonify, request

# Don't double-wrap errors, docs, or redirects
SKIP_PREFIXES = ("/apidocs", "/flasgger_static", "/apispec")


def wrap_response(response):
    if request.path.startswith(SKIP_PREFIXES):
        return response
    if response.content_type != "application/json" or response.status_code >= 400:
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

### Step 8.2: Register globally in `app/__init__.py`
```python
    from app.common.response_wrapper import wrap_response
    app.after_request(wrap_response)
```

Now every response is automatically wrapped:
```json
{
  "success": true,
  "data": { "id": 1, "name": "Laptop", ... },
  "timestamp": "2026-07-30T..."
}
```

---

## Phase 9 — WebSockets

### Step 9.1: Flask-SocketIO is already installed (Phase 0)

### Step 9.2: Create `app/modules/websocket/events.py`
```bash
mkdir -p app/modules/websocket
touch app/modules/websocket/__init__.py
```
In `app/__init__.py`, create the extension at module level and init it in the factory:
```python
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")

# inside create_app:
socketio.init_app(app)

# register events (import for side effects):
from app.modules.websocket import events  # noqa: F401
```
```python
from datetime import datetime, timezone

from flask import request
from flask_socketio import emit

from app import socketio


@socketio.on("connect")
def handle_connect():
    print(f"WS connected: {request.sid}")


@socketio.on("disconnect")
def handle_disconnect():
    print(f"WS disconnected: {request.sid}")


@socketio.on("message")
def handle_message(payload):
    emit("message", {
        "from": request.sid,
        "text": payload,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }, broadcast=True)
```

Update `run.py` — SocketIO needs its own runner:
```python
from app import create_app, socketio

app = create_app()

if __name__ == "__main__":
    socketio.run(app, port=app.config["PORT"], debug=True)
```

### Step 9.3: Test in browser console
```js
const socket = io('http://localhost:5000');
socket.on('message', data => console.log('Received:', data));
socket.emit('message', 'Hello from browser!');
```

---

## Where You Are Now

```
api/
├── docker-compose.yml
├── .env
├── requirements.txt
├── config.py
├── run.py
├── uploads/
│
└── app/
    ├── __init__.py                    ← app factory (create_app), extensions init
    │
    ├── common/
    │   ├── models/
    │   │   └── base.py                ← id, created_at, updated_at, deleted_at
    │   ├── utils/
    │   │   └── password.py            ← bcrypt hash/verify
    │   ├── auth.py                    ← Global auth via X-API-Key header (before_request)
    │   ├── errors.py                  ← Global error handlers
    │   └── response_wrapper.py        ← Standardized {success, data, timestamp} (after_request)
    │
    └── modules/
        ├── items/
        │   ├── schemas.py             ← CreateItemSchema, UpdateItemSchema, FilterItemSchema
        │   ├── models.py              ← Item model
        │   ├── service.py             ← business logic
        │   └── routes.py              ← items_bp blueprint
        │
        ├── users/
        │   ├── schemas.py             ← CreateUserSchema, UpdateUserSchema
        │   ├── models.py              ← User model
        │   ├── service.py
        │   └── routes.py              ← users_bp blueprint
        │
        ├── demo/
        │   └── routes.py              ← headers, cookies, status codes
        │
        ├── formfiles/
        │   └── routes.py              ← form data & file uploads
        │
        └── websocket/
            └── events.py              ← SocketIO event handlers
```

---

## Flask → NestJS Parallel (What You Already Know)

| Concept | NestJS | Flask |
|---------|--------|-------|
| Route | `@Get()` in a `@Controller('items')` | `@items_bp.get("/")` in a `Blueprint("items", url_prefix="/items")` |
| Path param | `@Param('id', ParseIntPipe) id: number` | `/<int:item_id>` → `def route(item_id: int)` |
| Query param | `@Query() filters: FilterItemDto` | `@validate() ... query: FilterItemSchema` |
| Body validation | class-validator DTO | Pydantic `BaseModel` + `flask_pydantic.validate()` |
| DI | `constructor(private service: ItemService)` | Plain function imports (`from app.modules.items import service`) |
| ORM model | `class Item extends BaseEntity` | `class Item(BaseModel)` with `db.Column` |
| Create table | `synchronize: true` or migrations | `db.create_all()` or Flask-Migrate/Alembic |
| Swagger | `@ApiProperty()` decorators | flasgger at `/apidocs` (docstring YAML or specs) |
| Exception | `NotFoundException()` | Custom exception + `@app.errorhandler` |
| Module registry | `@Module({ imports: [...] })` | `app.register_blueprint(bp)` in `create_app` |
| Global guard | `APP_GUARD` + `CanActivate` | `@app.before_request` hook |
| Global interceptor | `APP_INTERCEPTOR` / `useGlobalInterceptors` | `@app.after_request` hook |
| Global pipe | `app.useGlobalPipes(ValidationPipe)` | Global `ValidationError` errorhandler |
| App entry | `main.ts` + `AppModule` | `run.py` + `create_app()` factory |
| Config | `@nestjs/config` + `ConfigService` | `config.py` class + `app.config.from_object` |
| WebSocket | `@WebSocketGateway()` | Flask-SocketIO `@socketio.on("event")` |
| Env file | `.env` (same) | `.env` (same) |

## Flask → FastAPI Parallel (What You Already Know)

| Concept | FastAPI | Flask |
|---------|---------|-------|
| Route | `@router.get("/items")` | `@items_bp.get("/")` |
| Path param | `item_id: int` | `/<int:item_id>` |
| Query param | `q: str = None` | `query: FilterItemSchema` via `@validate()` |
| Body validation | Pydantic `BaseModel` | Pydantic `BaseModel` (same library!) |
| DI | `Depends(get_db)` | `db.session` (thread-local, no Depends needed) |
| ORM model | `class Item(Base)` | `class Item(BaseModel)` (db.Model) |
| Swagger | Automatic at `/docs` | flasgger at `/apidocs` |
| Exception | `HTTPException(404)` | Custom exception + errorhandler |
| Middleware | `@app.middleware("http")` | `@app.before_request` / `@app.after_request` |
| WebSocket | `@router.websocket("/ws")` | Flask-SocketIO `@socketio.on(...)` |
| Settings | `pydantic-settings` | `python-dotenv` + `config.py` |
