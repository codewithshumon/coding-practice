# FastAPI Learning Lab — Task Checklist (PostgreSQL Edition)

> **How to use:** Work through each group in order. Each task tells you **what to create**,
> **what code to write**, and **how to test it** with curl or the browser.
> Mark `[x]` as you complete each task.
>
> **Big change from v1:** No more fake in-memory dicts. Everything goes through a real
> PostgreSQL database using SQLAlchemy ORM. Docker Compose spins up the DB for you.

---

## Group 0 — Project Setup + Docker + Database

### Task 0.1: Create the project folder
```bash
mkdir fastapi-learn
cd fastapi-learn
```

### Task 0.2: Create docker-compose.yml
Create `docker-compose.yml` — copy from the companion file `docker-compose.yml` in this folder.

### Task 0.3: Start PostgreSQL and pgAdmin
```bash
docker compose up -d
```

### Task 0.4: Verify containers are running
```bash
docker compose ps
```
You should see `postgres` (healthy) and `pgadmin` running.

### Task 0.5: Verify pgAdmin
Open [http://localhost:5050](http://localhost:5050) in your browser.
- Email: `admin@admin.com`
- Password: `admin`
- Add a server: host=`postgres` (container name), port=`5432`, user=`fastapi`, password=`fastapi`, database=`fastapi_learn`

### Task 0.6: Create a virtual environment
```bash
python3 -m venv venv
```

### Task 0.7: Activate the virtual environment
```bash
source venv/bin/activate
```

### Task 0.8: Create requirements.txt
```
fastapi
uvicorn[standard]
pydantic
pydantic-settings
python-multipart
sqlalchemy
psycopg2-binary
```

### Task 0.9: Install dependencies
```bash
pip install -r requirements.txt
```

### Task 0.10: Create the folder structure
```bash
mkdir routes models db
touch routes/__init__.py models/__init__.py db/__init__.py
```

### Task 0.11: Create db/database.py — the database connection
- Import `create_engine`, `sessionmaker` from sqlalchemy
- Import `declarative_base` from sqlalchemy.orm
- Create a `DATABASE_URL` pointing to `postgresql://fastapi:fastapi@localhost:5432/fastapi_learn`
- Create `engine = create_engine(DATABASE_URL)`
- Create `SessionLocal = sessionmaker(bind=engine)`
- Create `Base = declarative_base()`

### Task 0.12: Create db/database.py — the get_db dependency
In the same file, add:
- `def get_db()` — yields a session and closes it after the request

### Task 0.13: Test the database connection
Write a small script that creates a session, executes `SELECT 1`, and prints "Connected!"

### Task 0.14: Create .env
```
HOST=127.0.0.1
PORT=4000
DEBUG=true
ENVIRONMENT=development
DATABASE_URL=postgresql://fastapi:fastapi@localhost:5432/fastapi_learn
```

### Task 0.15: Create config.py
- Use pydantic-settings `BaseSettings`
- Read `host`, `port`, `debug`, `database_url` from env
- Create global `settings` object

### Task 0.16: Create .env.example (committed to git)
```
HOST=127.0.0.1
PORT=8000
DEBUG=false
ENVIRONMENT=development
DATABASE_URL=postgresql://fastapi:fastapi@localhost:5432/fastapi_learn
```

### Task 0.17: Create .gitignore
```
venv/
__pycache__/
*.py[cod]
.env
*.egg-info/
dist/
.vscode/
.idea/
.DS_Store
```

### Task 0.18: Create pyproject.toml
- Project metadata
- `[tool.uvicorn]` with host, port, reload, log-level

---

## Group 1 — Your First Route (Hello World)

### Task 1.1: Create routes/hello.py
- Import `APIRouter` from fastapi
- Create `router = APIRouter()`
- Add a `GET /` endpoint that returns `{"message": "Hello, World!"}`
- Add a `GET /ping` endpoint that returns `{"status": "ok"}`

### Task 1.2: Create main.py
- Import `FastAPI`
- Import the hello router from `routes.hello`
- Import `settings` from `config`
- Import `Base`, `engine` from `db.database`
- Create `app = FastAPI()` with title, description, version
- Register the hello router
- Add startup event: `Base.metadata.create_all(bind=engine)` — creates all tables on startup

### Task 1.3: Start the server
```bash
uvicorn main:app
```

### Task 1.4: Test — browser
- `http://127.0.0.1:4000/`
- `http://127.0.0.1:4000/ping`
- `http://127.0.0.1:4000/docs`

### Task 1.5: Test — curl
```bash
curl http://127.0.0.1:4000/
curl http://127.0.0.1:4000/ping
```

---

## Group 2 — SQLAlchemy Models + HTTP Methods (CRUD with Real DB)

### Task 2.1: Create models/item.py — the SQLAlchemy model
- Import `Column`, `Integer`, `String`, `Float`, `Boolean` from sqlalchemy
- Import `Base` from `db.database`
- Create `class Item(Base):`
  - `__tablename__ = "items"`
  - `id`: Integer, primary key, index
  - `name`: String, index
  - `price`: Float
  - `description`: String, nullable
  - `in_stock`: Boolean, default True

### Task 2.2: Create schemas/item.py — the Pydantic schemas
- `ItemBase`: name (str), price (float), description (Optional[str]), in_stock (bool)
- `ItemCreate(ItemBase)`: pass
- `ItemUpdate`: all fields Optional (for PATCH)
- `ItemRead(ItemBase)`: id (int)
  - Add `model_config = {"from_attributes": True}` — enables ORM mode

### Task 2.3: Create routes/items.py — full CRUD
- Import `APIRouter`, `Depends`, `HTTPException`, `status`
- Import `Session` from sqlalchemy.orm
- Import `get_db` from `db.database`
- Create `router = APIRouter(prefix="/items", tags=["Items"])`

### Task 2.4: Add GET /items — list all items
- Inject `db: Session = Depends(get_db)`
- Query all items: `db.query(Item).all()`
- Return the list

### Task 2.5: Add GET /items/{item_id} — get one item
- Query by id: `db.query(Item).filter(Item.id == item_id).first()`
- If None, `raise HTTPException(status_code=404, detail="Item not found")`
- Return the item

### Task 2.6: Add POST /items — create an item
- Accept `item_in: ItemCreate` as JSON body
- Create SQLAlchemy Item: `db_item = Item(**item_in.model_dump())`
- `db.add(db_item)`, `db.commit()`, `db.refresh(db_item)`
- Return the created item with status 201

### Task 2.7: Add PUT /items/{item_id} — full replace
- Accept `item_in: ItemCreate` as JSON body
- Find item by id, raise 404 if not found
- Update ALL fields from item_in
- `db.commit()`, `db.refresh()`
- Return updated item

### Task 2.8: Add PATCH /items/{item_id} — partial update
- Accept `item_in: ItemUpdate` as JSON body
- Find item by id, raise 404 if not found
- Only update fields that are NOT None: `item_in.model_dump(exclude_unset=True)`
- `db.commit()`, `db.refresh()`
- Return updated item

### Task 2.9: Add DELETE /items/{item_id} — remove
- Find item by id, raise 404 if not found
- `db.delete(item)`, `db.commit()`
- Return 204 No Content

### Task 2.10: Register in main.py
```python
from routes import items
app.include_router(items.router)
```

### Task 2.11: Test the full CRUD
```bash
# Create
curl -X POST http://127.0.0.1:4000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.0}'

curl -X POST http://127.0.0.1:4000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Phone", "price": 699.0}'

# List
curl http://127.0.0.1:4000/items

# Get one
curl http://127.0.0.1:4000/items/1

# Partial update (only name)
curl -X PATCH http://127.0.0.1:4000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Gaming Laptop"}'

# Full replace
curl -X PUT http://127.0.0.1:4000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Tablet", "price": 399.0}'

# Delete
curl -X DELETE http://127.0.0.1:4000/items/1

# Verify deleted
curl http://127.0.0.1:4000/items

# Open pgAdmin at http://localhost:5050 and check the items table!
```

---

## Group 3 — Path Parameters

### Task 3.1: Create routes/path_params.py
- Import `APIRouter`, `Enum`

### Task 3.2: Add GET /users/{user_id} — int path param
- `user_id: int` — return it and its Python type
- Test: `curl http://127.0.0.1:4000/users/42`
- Test: `curl http://127.0.0.1:4000/users/abc` (422 error)

### Task 3.3: Add GET /users/{username}/profile — string path param
- `username: str` — return a profile dict
- Test: `curl http://127.0.0.1:4000/users/alice/profile`

### Task 3.4: Add GET /orgs/{org}/repos/{repo} — multiple params
- `org: str`, `repo: str` — return both
- Test: `curl http://127.0.0.1:4000/orgs/microsoft/repos/vscode`

### Task 3.5: Add an Enum for category — constrained choices
- `class Category(str, Enum)` with values: `books`, `movies`, `music`
- Add `GET /catalog/{category}` where `category: Category`
- Test: `curl http://127.0.0.1:4000/catalog/books` → works
- Test: `curl http://127.0.0.1:4000/catalog/games` → 422 error

### Task 3.6: Register in main.py and test all

---

## Group 4 — Query Parameters (with Real DB Filtering)

### Task 4.1: Create routes/query_params.py
- Import `APIRouter`, `Query`, `Depends`
- Import `Session`, `get_db`, `Item` model, `ItemRead` schema

### Task 4.2: Add GET /search — required + default query params
- `q: str` (required), `page: int = 1` (default)
- Test: `curl "http://127.0.0.1:4000/search?q=laptop"`
- Test: `curl "http://127.0.0.1:4000/search"` → 422

### Task 4.3: Add GET /items/filter — DB-backed filtering
- `name: str | None = None`, `max_price: float | None = None`, `in_stock: bool | None = None`
- Build the query dynamically:
  - Start with `query = db.query(Item)`
  - `if name: query = query.filter(Item.name.ilike(f"%{name}%"))`
  - `if max_price is not None: query = query.filter(Item.price <= max_price)`
  - `if in_stock is not None: query = query.filter(Item.in_stock == in_stock)`
- Execute and return results
- Test each combination of filters

### Task 4.4: Add GET /items — validated pagination
- `skip: int = Query(0, ge=0)`, `limit: int = Query(10, ge=1, le=100)`
- Use `db.query(Item).offset(skip).limit(limit).all()`
- Test: `curl "http://127.0.0.1:4000/items?skip=0&limit=2"`
- Test: `curl "http://127.0.0.1:4000/items?limit=200"` → 422

### Task 4.5: Add GET /items/available — boolean query
- `in_stock: bool = True`
- Filter in DB
- Test: `curl "http://127.0.0.1:4000/items/available?in_stock=false"`

### Task 4.6: Add GET /items/by-ids — list query param
- `ids: list[int] = Query([])`
- Use `Item.id.in_(ids)`
- Test: `curl "http://127.0.0.1:4000/items/by-ids?ids=1&ids=3"`

### Task 4.7: Register in main.py and test all

---

## Group 5 — Request Body (Pydantic Models with DB)

### Task 5.1: Create routes/request_body.py
- Import `APIRouter`, `Depends`
- Import Pydantic `BaseModel`, `Field`
- Import `Session`, `get_db`

### Task 5.2: Create a User SQLAlchemy model
In `models/user.py`:
- `class User(Base)`: id, username, email, hashed_password, is_admin
- Create matching Pydantic schemas in `schemas/user.py`

### Task 5.3: Define nested Pydantic models (without DB for demo)
- `Address` model: street, city, zip_code
- `UserWithAddress` model: name, email, address (nested), tags (list)
- `POST /users/register` — accepts the nested body, returns it

### Task 5.4: Test nested JSON
```bash
curl -X POST http://127.0.0.1:4000/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice",
    "email": "alice@example.com",
    "address": {
      "street": "123 Main St",
      "city": "Springfield",
      "zip_code": "62701"
    },
    "tags": ["admin", "beta"]
  }'
```

### Task 5.5: Register in main.py and test via /docs

---

## Group 6 — Response Models (with DB)

### Task 6.1: Create routes/response_models.py
- Use existing `ItemRead` as `response_model`
- Show how DB model fields get filtered through the Pydantic schema

### Task 6.2: Add GET /items with response_model=list[ItemRead]
- Query DB, return items — each is filtered through ItemRead

### Task 6.3: Add GET /items/{item_id} with response_model=ItemRead
- Only fields defined in ItemRead make it to the response
- If your DB model has extra internal fields, they're stripped

### Task 6.4: Add response_model_exclude_none endpoint
- Create an item with some None fields
- Compare response with/without `response_model_exclude_none=True`

### Task 6.5: Register in main.py and test all

---

## Group 7 — Headers & Cookies

Same as before — no DB needed for these concepts.

### Task 7.1: Create routes/headers_cookies.py
- Import `APIRouter`, `Header`, `Cookie`, `Response`, `Annotated`

### Task 7.2: Add GET /whoami — read User-Agent
- Test: `curl -H "User-Agent: MyApp/1.0" http://127.0.0.1:4000/whoami`

### Task 7.3: Add GET /custom — read X-Request-Id header
- Test: `curl -H "X-Request-Id: abc-123" http://127.0.0.1:4000/custom`

### Task 7.4: Add GET /read-cookie
- Test: `curl -b "session_id=hello123" http://127.0.0.1:4000/read-cookie`

### Task 7.5: Add GET /set-cookie — set response cookie
- Test: `curl -v http://127.0.0.1:4000/set-cookie`

### Task 7.6: Add GET /set-headers — custom response headers
- Test: `curl -v http://127.0.0.1:4000/set-headers`

### Task 7.7: Register in main.py and test all

---

## Group 8 — Status Codes

### Task 8.1: Create routes/status_codes.py
- Import `APIRouter`, `Response`, `status`

### Task 8.2: Add POST /products with status_code=201
- Use existing Item model
- Test: `curl -v -X POST http://127.0.0.1:4000/products ...` → 201

### Task 8.3: Dynamic status code (200 if exists, 201 if created)
- Check DB, set `response.status_code` accordingly

### Task 8.4: DELETE returns 204 No Content
- `status_code=status.HTTP_204_NO_CONTENT`

### Task 8.5: 301 redirect
- `Response(status_code=301, headers={"Location": "/new-path"})`

### Task 8.6: Register in main.py and test all

---

## Group 9 — Form Data & File Uploads

### Task 9.1: Create routes/form_files.py
- Import `APIRouter`, `Form`, `UploadFile`, `File`, `Annotated`

### Task 9.2: Add POST /login — form data
- `username: Annotated[str, Form()]`, `password: Annotated[str, Form()]`
- Test: `curl -X POST http://127.0.0.1:4000/login -d "username=alice&password=secret"`

### Task 9.3: Add POST /upload — single file
- `file: UploadFile = File(...)`
- Read contents, return filename + size
- Test: `curl -X POST http://127.0.0.1:4000/upload -F "file=@test.txt"`

### Task 9.4: Add POST /upload-multiple — multiple files
- `files: list[UploadFile] = File(...)`
- Test: `curl -X POST http://127.0.0.1:4000/upload-multiple -F "files=@a.txt" -F "files=@b.txt"`

### Task 9.5: Add POST /profile — form + file
- `name: Annotated[str, Form()]` + `avatar: UploadFile`
- Test: `curl -X POST http://127.0.0.1:4000/profile -F "name=Alice" -F "avatar=@photo.png"`

### Task 9.6: Register in main.py and test all

---

## Group 10 — Dependencies (Database Dependency + Auth)

### Task 10.1: You already have get_db! That's a dependency.

### Task 10.2: Create a pagination dependency
- `def get_pagination(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100)) -> dict`
- Use with `Depends(get_pagination)` alongside `Depends(get_db)`

### Task 10.3: Multiple dependencies in one route
```python
@router.get("/items")
def list_items(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination),
):
    return db.query(Item).offset(pagination["offset"]).limit(pagination["limit"]).all()
```

### Task 10.4: Create an API key guard dependency
- Read `X-API-Key` header, raise 401 if invalid
- `def verify_api_key(x_api_key: Annotated[str, Header()]) -> str`

### Task 10.5: Create nested dependency — require admin
- Depends on `verify_api_key`, also checks role
- Protect admin routes with it

### Task 10.6: Test all combinations

---

## Group 11 — Error Handling

### Task 11.1: Create routes/error_handling.py
- Add DB-backed endpoints that raise HTTPException properly

### Task 11.2: Try getting a non-existent item → 404 from the DB query

### Task 11.3: Custom exception class + handler
- `class ItemNotFoundError(Exception)`
- Register custom handler in main.py with `app.add_exception_handler()`

### Task 11.4: Test: 404, 400, 500

---

## Group 12 — Middleware

### Task 12.1: Create custom_middleware.py
- Request timer middleware
- Add `X-Request-Id` and `X-Response-Time-ms` headers

### Task 12.2: Register in main.py

### Task 12.3: Add CORS middleware

### Task 12.4: Test: `curl -v` to see headers

---

## Group 13 — Background Tasks

### Task 13.1: Create routes/background_tasks.py
- Simulated email sending, audit logging
- Fire tasks after DB operations

### Task 13.2: On item creation, background-task an email notification

### Task 13.3: Test: response is instant, logs appear after

---

## Group 14 — WebSockets

### Task 14.1: Create routes/websocket_demo.py
- Echo WebSocket
- Chat room WebSocket with ConnectionManager
- Real-time clock WebSocket

### Task 14.2: Test with browser console

---

## Group 15 — Advanced Routing (Prefixes, Tags, Nesting)

### Task 15.1: Organize item routes under `/api/v1/items`

### Task 15.2: Create admin routes under `/api/v1/admin`
- Protected by router-level dependency

### Task 15.3: Nest everything under a parent router

### Task 15.4: Test the URL hierarchy

---

## Group 16 — Build Your Own (Database-Backed)

Now combine everything into a real database-backed API.

### Option A: Todo API with PostgreSQL
- CRUD for todos (id, title, done, created_at)
- SQLAlchemy model + Pydantic schemas
- Filter by done status (query param → DB filter)
- Pagination (offset/limit)
- Proper status codes (201, 204)
- Background task on completion

### Option B: Blog API with PostgreSQL
- Posts (id, title, body, author, published_at) + SQLAlchemy
- Comments (id, post_id, body, author) — relationship!
- List with pagination + tag filter
- File upload for images
- Protected admin routes (API key guard)

### Option C: E-Commerce Product Catalog
- Products, Categories, Reviews — 3 tables with relationships
- SQLAlchemy ForeignKey + relationship()
- Filter by category, price range, rating
- Full CRUD with proper status codes

---

## Cheat Sheet — Testing Commands

### Query parameters
```bash
curl "http://127.0.0.1:4000/items?skip=0&limit=5"
```

### Path parameters
```bash
curl http://127.0.0.1:4000/items/1
```

### Request body (JSON)
```bash
curl -X POST http://127.0.0.1:4000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.0}'
```

### Headers
```bash
curl -H "X-API-Key: secret" http://127.0.0.1:4000/secure-data
```

### Form data
```bash
curl -X POST http://127.0.0.1:4000/login -d "username=alice&password=pass"
```

### File upload
```bash
curl -X POST http://127.0.0.1:4000/upload -F "file=@myfile.txt"
```

### Show response headers
```bash
curl -v http://127.0.0.1:4000/items
```

### Docker
```bash
docker compose up -d          # start
docker compose down           # stop
docker compose down -v        # stop + delete data
docker compose ps             # status
docker compose logs postgres  # DB logs
```

### PostgreSQL in Docker
```bash
# Connect directly
docker exec -it fastapi-postgres psql -U fastapi -d fastapi_learn

# Inside psql:
\dt              # list tables
SELECT * FROM items;
\d items         # describe table
\q               # quit
```

---

## Database Connection — The Golden Pattern

Every route that needs the DB follows this exact pattern:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models.item import Item
from schemas.item import ItemCreate, ItemRead

router = APIRouter()

@router.get("/items", response_model=list[ItemRead])
def list_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

@router.post("/items", response_model=ItemRead, status_code=201)
def create_item(item_in: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item_in.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
```

`Depends(get_db)` is the magic — it injects a fresh database session for every request.
You never open/close connections manually.

---

**Done!** Work through each group, build with PostgreSQL from day one, and by the end
you'll have hands-on experience with FastAPI + real database patterns.
