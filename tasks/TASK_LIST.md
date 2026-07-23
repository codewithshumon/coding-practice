# FastAPI Learning Lab — Task Checklist

> **How to use:** Work through each group in order. Each task tells you **what to create**,
> **what code to write**, and **how to test it** with curl or the browser.
> Mark `[x]` as you complete each task.

---

## Group 0 — Project Setup

### Task 0.1: Create the project folder
```bash
mkdir fastapi-learn
cd fastapi-learn
```

### Task 0.2: Create a virtual environment
```bash
python3 -m venv venv
```

### Task 0.3: Activate the virtual environment
```bash
source venv/bin/activate
```

### Task 0.4: Create requirements.txt
Create `requirements.txt` with these lines:
```
fastapi
uvicorn[standard]
pydantic
python-multipart
```

### Task 0.5: Install dependencies
```bash
pip install -r requirements.txt
```

### Task 0.6: Create the folder structure
```bash
mkdir routes models
touch routes/__init__.py models/__init__.py
```

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
- Create `app = FastAPI()` with title, description, version
- Register the router with `app.include_router(hello.router)`

### Task 1.3: Start the server
```bash
uvicorn main:app --reload
```

### Task 1.4: Test — browser
Open these URLs in your browser:
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/ping`
- `http://127.0.0.1:8000/docs` (Swagger UI)
- `http://127.0.0.1:8000/redoc` (ReDoc)

### Task 1.5: Test — curl
```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/ping
```

---

## Group 2 — HTTP Methods (GET, POST, PUT, PATCH, DELETE)

### Task 2.1: Create routes/http_methods.py
- Import `APIRouter`
- Create `router = APIRouter()`
- Set up a fake in-memory dict `fake_db: dict[int, dict] = {}` and `_next_id = 1`

### Task 2.2: Add GET /items — list all items
- Return all items from fake_db as a list

### Task 2.3: Add GET /items/{item_id} — get one item
- Accept `item_id: int` as a path parameter
- Return the item or `{"error": "Item not found"}`

### Task 2.4: Add POST /items — create an item
- Accept `name: str` and `price: float` as query parameters
- Create a new item dict, store it, increment `_next_id`
- Return the new item

### Task 2.5: Add PUT /items/{item_id} — full replace
- Accept `item_id: int` (path) and `name: str`, `price: float` (query)
- Replace the entire item, return it

### Task 2.6: Add PATCH /items/{item_id} — partial update
- Accept `item_id: int` (path) and `name: str | None = None`, `price: float | None = None`
- Only update the fields that are provided (not None)

### Task 2.7: Add DELETE /items/{item_id} — remove
- Accept `item_id: int`, remove from dict, return deleted item

### Task 2.8: Register the router in main.py
```python
from routes import http_methods
app.include_router(http_methods.router)
```

### Task 2.9: Test — curl (do these in order)
```bash
# Create
curl -X POST "http://127.0.0.1:8000/items?name=Laptop&price=999"
curl -X POST "http://127.0.0.1:8000/items?name=Phone&price=699"

# List
curl http://127.0.0.1:8000/items

# Get one
curl http://127.0.0.1:8000/items/1

# Partial update (PATCH)
curl -X PATCH "http://127.0.0.1:8000/items/1?name=GamingLaptop"

# Full replace (PUT)
curl -X PUT "http://127.0.0.1:8000/items/1?name=Tablet&price=399"

# Delete
curl -X DELETE http://127.0.0.1:8000/items/1

# Verify deleted
curl http://127.0.0.1:8000/items
```

---

## Group 3 — Path Parameters

### Task 3.1: Create routes/path_params.py
- Import `APIRouter`, `Enum`

### Task 3.2: Add GET /users/{user_id} — int path param
- `user_id: int` — return it and its Python type
- Test with: `curl http://127.0.0.1:8000/users/42`
- Test with: `curl http://127.0.0.1:8000/users/abc` (see the 422 error)

### Task 3.3: Add GET /users/{username}/profile — string path param
- `username: str` — return a profile dict
- Test with: `curl http://127.0.0.1:8000/users/alice/profile`

### Task 3.4: Add GET /orgs/{org}/repos/{repo} — multiple params
- `org: str`, `repo: str` — return both
- Test with: `curl http://127.0.0.1:8000/orgs/microsoft/repos/vscode`

### Task 3.5: Add an Enum for category — constrained choices
- Create `class Category(str, Enum)` with values: `books`, `movies`, `music`
- Add `GET /catalog/{category}` where `category: Category`
- Test with: `curl http://127.0.0.1:8000/catalog/books` → works
- Test with: `curl http://127.0.0.1:8000/catalog/games` → 422 error

### Task 3.6: Register in main.py and test all

---

## Group 4 — Query Parameters

### Task 4.1: Create routes/query_params.py
- Import `APIRouter`, `Query`
- Create a fake list of items (list of dicts with id, name, price, in_stock)

### Task 4.2: Add GET /search — required + default query params
- `q: str` (required), `page: int = 1` (default)
- Test: `curl "http://127.0.0.1:8000/search?q=laptop"`
- Test: `curl "http://127.0.0.1:8000/search?q=laptop&page=2"`
- Test: `curl "http://127.0.0.1:8000/search"` → 422 (missing required q)

### Task 4.3: Add GET /filter — optional query params
- `name: str | None = None`, `max_price: float | None = None`
- Filter the items list based on which params are provided
- Test: `curl "http://127.0.0.1:8000/filter"`
- Test: `curl "http://127.0.0.1:8000/filter?max_price=500"`
- Test: `curl "http://127.0.0.1:8000/filter?name=Laptop"`
- Test: `curl "http://127.0.0.1:8000/filter?name=Laptop&max_price=1000"`

### Task 4.4: Add GET /items — validated query params with Query()
- `skip: int = Query(0, ge=0)`, `limit: int = Query(10, ge=1, le=100)`
- Test: `curl "http://127.0.0.1:8000/items?skip=2&limit=3"`
- Test: `curl "http://127.0.0.1:8000/items?limit=200"` → 422 error

### Task 4.5: Add GET /items/available — boolean query param
- `in_stock: bool = True`
- Test: `curl "http://127.0.0.1:8000/items/available?in_stock=false"`
- Test: `curl "http://127.0.0.1:8000/items/available?in_stock=yes"` (yes/true/1/on all = True)

### Task 4.6: Add GET /items/by-ids — list query param
- `ids: list[int] = Query([])` — same key repeated builds a list
- Test: `curl "http://127.0.0.1:8000/items/by-ids?ids=1&ids=3&ids=5"`

### Task 4.7: Register in main.py and test all

---

## Group 5 — Request Body (Pydantic Models)

### Task 5.1: Create routes/request_body.py
- Import `APIRouter`, `BaseModel`, `Field` from pydantic

### Task 5.2: Define an Item model
```python
class Item(BaseModel):
    name: str
    price: float
    description: str | None = None
    tax: float | None = None
```

### Task 5.3: Add POST /items — accept JSON body
- Accept `item: Item` as the request body
- FastAPI auto-parses JSON into an Item object
- Test with curl sending JSON body:
```bash
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.0}'
```
- Test validation error (missing required field):
```bash
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop"}'
```
- Test validation error (wrong type):
```bash
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": "cheap"}'
```

### Task 5.4: Add a model with Field() validation
- Create `ItemCreate` model using `Field(...)` with `gt`, `min_length`, `max_length`
- Add a new endpoint that uses this stricter model
- Test with empty name → 422
- Test with negative price → 422

### Task 5.5: Add a nested model (User with Address)
- Create `Address` model: `street`, `city`, `zip_code`
- Create `UserIn` model: `name`, `email`, `address: Address`, `tags: list[str]`
- Add `POST /users` endpoint
- Test with nested JSON:
```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice",
    "email": "alice@example.com",
    "address": {
      "street": "123 Main St",
      "city": "Springfield",
      "zip_code": "62701"
    },
    "tags": ["admin"]
  }'
```

### Task 5.6: Register in main.py and test via /docs (easier for complex JSON!)

---

## Group 6 — Response Models

### Task 6.1: Create routes/response_models.py
- Import `APIRouter`, `BaseModel`

### Task 6.2: Define internal vs public models
- `UserInDB`: id, username, email, hashed_password, is_admin
- `UserOut`: username, email (safe fields only)
- Create a fake users dict

### Task 6.3: Add GET /users/{user_id} with response_model=UserOut
- The `hashed_password` and `is_admin` are stripped from the response
- Test: `curl http://127.0.0.1:8000/users/1` — notice missing fields

### Task 6.4: Add GET /users/{user_id}/admin with response_model_exclude
- Use `response_model=UserInDB, response_model_exclude={"hashed_password"}`
- Test: `curl http://127.0.0.1:8000/users/1/admin`

### Task 6.5: Add response_model_exclude_none
- Create an endpoint with `response_model_exclude_none=True`
- Fields with `None` values are omitted from the JSON entirely
- Test: compare two endpoints — one with exclude_none, one without

### Task 6.6: Return a list with response_model=list[SomeModel]
- Add `GET /items` returning `list[ItemSummary]`
- Each item is filtered to match ItemSummary

### Task 6.7: Register in main.py and test all

---

## Group 7 — Headers & Cookies

### Task 7.1: Create routes/headers_cookies.py
- Import `APIRouter`, `Header`, `Cookie`, `Response`
- Import `Annotated` from typing

### Task 7.2: Add GET /whoami — read User-Agent header
- `user_agent: Annotated[str | None, Header()] = None`
- Test: `curl -H "User-Agent: MyApp/1.0" http://127.0.0.1:8000/whoami`

### Task 7.3: Add GET /custom — read custom header
- Read `X-Request-Id` header
- Test: `curl -H "X-Request-Id: abc-123" http://127.0.0.1:8000/custom`

### Task 7.4: Add GET /read-cookie — read a cookie
- `session_id: Annotated[str | None, Cookie()] = None`
- Test: `curl -b "session_id=hello123" http://127.0.0.1:8000/read-cookie`

### Task 7.5: Add GET /set-cookie — set a cookie in response
- Accept `response: Response` and use `response.set_cookie(...)`
- Test: `curl -v http://127.0.0.1:8000/set-cookie` (look for Set-Cookie header)

### Task 7.6: Add GET /set-headers — set custom response headers
- Use `response.headers["X-Custom"] = "value"`
- Test: `curl -v http://127.0.0.1:8000/set-headers`

### Task 7.7: Register in main.py and test all

---

## Group 8 — Status Codes

### Task 8.1: Create routes/status_codes.py
- Import `APIRouter`, `Response`, `status`

### Task 8.2: Add POST /items with status_code=201
- Use `status_code=status.HTTP_201_CREATED` in the decorator
- Test: `curl -v -X POST "http://127.0.0.1:8000/items?name=A&price=10"` (look for 201)

### Task 8.3: Add endpoint with dynamic status code
- Accept `response: Response` and set `response.status_code` conditionally
- Return 200 if item exists, 201 if created
- Test each case and check the status code

### Task 8.4: Add DELETE with 204 No Content
- Use `status_code=status.HTTP_204_NO_CONTENT`
- Even if you return something, the body is empty for 204
- Test: `curl -v -X DELETE http://127.0.0.1:8000/items/1`

### Task 8.5: Add a redirect (301)
- Return a Response with `status_code=301` and `headers={"Location": "/new-path"}`
- Test: `curl -v http://127.0.0.1:8000/old-path` (follow redirect, see you land on /new-path)

### Task 8.6: Register in main.py and test all

---

## Group 9 — Form Data & File Uploads

### Task 9.1: Create routes/form_files.py
- Import `APIRouter`, `Form`, `UploadFile`, `File`
- Import `Annotated`

### Task 9.2: Add POST /login — form data
- Accept `username: Annotated[str, Form()]` and `password: Annotated[str, Form()]`
- Test (form-encoded, NOT JSON):
```bash
curl -X POST http://127.0.0.1:8000/login \
  -d "username=alice&password=secret"
```

### Task 9.3: Add POST /upload — single file
- `file: UploadFile = File(...)`
- Read with `await file.read()`, return filename, content_type, size
- Create a test file: `echo "hello world" > test.txt`
- Test:
```bash
curl -X POST http://127.0.0.1:8000/upload \
  -F "file=@test.txt"
```

### Task 9.4: Add POST /upload-multiple — multiple files
- `files: list[UploadFile] = File(...)`
- Loop through and read each
- Test:
```bash
curl -X POST http://127.0.0.1:8000/upload-multiple \
  -F "files=@test.txt" -F "files=@test2.txt"
```

### Task 9.5: Add POST /profile — form + file together
- `name: Annotated[str, Form()]` + `avatar: UploadFile = File(...)`
- Test:
```bash
curl -X POST http://127.0.0.1:8000/profile \
  -F "name=Alice" -F "avatar=@test.txt"
```

### Task 9.6: Register in main.py and test all

---

## Group 10 — Dependencies (Depends)

### Task 10.1: Create routes/dependencies.py
- Import `APIRouter`, `Depends`, `HTTPException`, `Header`, `Query`
- Import `Annotated`

### Task 10.2: Create a shared pagination dependency
- `def get_pagination(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100))`
- Returns `{"offset": (page-1)*page_size, "limit": page_size}`
- Use it in a route: `pagination: Annotated[dict, Depends(get_pagination)]`
- Test: `curl "http://127.0.0.1:8000/posts?page=2&page_size=5"`

### Task 10.3: Create an API key guard dependency
- Read `X-API-Key` header, raise 401 if invalid
- Protect a `/secure-data` endpoint with it
- Test without header: `curl http://127.0.0.1:8000/secure-data` → 422 or 401
- Test with wrong key: `curl -H "X-API-Key: wrong" http://127.0.0.1:8000/secure-data` → 401
- Test with correct key: `curl -H "X-API-Key: secret-key-123" http://127.0.0.1:8000/secure-data` → 200

### Task 10.4: Create a class-based dependency (Database)
- Create a Database class with `all()` and `get()` methods
- Create `get_db()` that returns a db instance
- Use it: `db: Annotated[Database, Depends(get_db)]`
- Test: `curl http://127.0.0.1:8000/todos`

### Task 10.5: Create nested dependencies (3 levels deep)
- Level 1: `get_current_user` — extracts user from API key header
- Level 2: `require_admin` — takes Level 1's output, checks role == "admin", raises 403 if not
- Level 3: Route uses `require_admin` as its dependency
- Test with admin key → works
- Test with non-admin key → 403

### Task 10.6: Register in main.py and test all

---

## Group 11 — Error Handling

### Task 11.1: Create routes/error_handling.py
- Import `APIRouter`, `HTTPException`

### Task 11.2: Add GET /items/{item_id} — raise 404
- If item not found: `raise HTTPException(status_code=404, detail="Item X not found")`
- Test: `curl http://127.0.0.1:8000/items/999` (status 404)

### Task 11.3: Add GET /divide — raise 400 for business logic
- If `b == 0`: `raise HTTPException(status_code=400, detail="Cannot divide by zero")`
- Test: `curl "http://127.0.0.1:8000/divide?a=10&b=0"` (status 400)

### Task 11.4: Create a custom exception class
- `class ItemNotFoundError(Exception):` with `item_id` attribute
- Add a route that raises it when item not found

### Task 11.5: Create a custom exception handler in a separate file
- In `custom_handlers.py`, create a handler function that catches `ItemNotFoundError`
- Returns a JSONResponse with 404 and structured error body
- Register it in main.py: `app.add_exception_handler(ItemNotFoundError, handler)`

### Task 11.6: Register in main.py and test the custom handler

---

## Group 12 — Middleware

### Task 12.1: Create custom_middleware.py
- Import `BaseHTTPMiddleware` from starlette
- Create a `TimerMiddleware` class:
  - `dispatch(self, request, call_next)` — async
  - Record start time before `call_next(request)`
  - Add `X-Response-Time-ms` header after
  - Print/log the request method, path, duration, status

### Task 12.2: Create routes/middleware_demo.py
- Add a few simple endpoints: `/fast`, `/slow` (with `time.sleep(1)`), `/error` (raises ValueError)

### Task 12.3: Register middleware in main.py
```python
from custom_middleware import TimerMiddleware
app.add_middleware(TimerMiddleware)
```

### Task 12.4: Test middleware
- `curl -v http://127.0.0.1:8000/fast` — look for `X-Response-Time-ms` header
- `curl -v http://127.0.0.1:8000/slow` — higher response time
- Watch terminal logs for printed request info

### Task 12.5: Try built-in CORS middleware
- Add `CORSMiddleware` in main.py with `allow_origins=["*"]`

---

## Group 13 — Background Tasks

### Task 13.1: Create routes/background_tasks.py
- Import `APIRouter`, `BackgroundTasks`
- Create some simulated slow functions: `send_welcome_email(email, username)`, `write_audit_log(action, user)`
- Each should `time.sleep()` and print something

### Task 13.2: Add POST /register with background task
- Accept `BackgroundTasks` in the route
- Call `bg.add_task(send_welcome_email, email, username)`
- Return success immediately — email is sent in background
- Test: `curl -X POST "http://127.0.0.1:8000/register?email=a@b.com&username=alice"`
- Notice: response is instant, but watch terminal for the "email sent" print 2 seconds later

### Task 13.3: Add POST /purchase with multiple background tasks
- Fire 2+ tasks: audit log + analytics
- Test and watch terminal

### Task 13.4: Register in main.py and test all

---

## Group 14 — WebSockets

### Task 14.1: Create routes/websocket_demo.py
- Import `APIRouter`, `WebSocket`, `WebSocketDisconnect`

### Task 14.2: Add WebSocket /ws/echo
- `@router.websocket("/ws/echo")`
- `async def echo(websocket: WebSocket)`
- `await websocket.accept()` then loop: `receive_text()` → `send_text(f"Echo: {data}")`
- Catch `WebSocketDisconnect`

### Task 14.3: Test the echo WebSocket
In your browser console (on any page, like /docs):
```js
let ws = new WebSocket("ws://127.0.0.1:8000/ws/echo");
ws.onmessage = e => console.log("Server:", e.data);
ws.onopen = () => ws.send("Hello from browser!");
```
Or use `websocat` if you have it:
```bash
echo "hello" | websocat ws://127.0.0.1:8000/ws/echo
```

### Task 14.4: Add WebSocket /ws/chat/{room}/{username}
- Create a `ConnectionManager` class that tracks active connections per room
- Accept connection, broadcast join/leave messages, broadcast chat messages
- Test: open two browser tabs, connect to same room, send messages

### Task 14.5: Add WebSocket /ws/clock — push JSON every second
- Use `await asyncio.sleep(1)` in a loop
- `await websocket.send_json({"time": ...})`
- Test in browser console

### Task 14.6: Register in main.py and test all

---

## Group 15 — Advanced Routing (APIRouter, Prefixes, Tags)

### Task 15.1: Create routes/advanced_routing.py
- Import `APIRouter`, `Depends`, `HTTPException`, `Query`

### Task 15.2: Create a public router with prefix and tags
```python
public_router = APIRouter(
    prefix="/v1",
    tags=["Public"],
    responses={404: {"description": "Not found"}},
)
```
- Add `GET /health` (becomes `/v1/health`)
- Add `GET /products` with optional category filter

### Task 15.3: Create a private router with router-level dependency
```python
private_router = APIRouter(
    prefix="/v1/admin",
    tags=["Admin"],
    dependencies=[Depends(verify_admin_key)],
)
```
- Create a `verify_admin_key` dependency (checks `x_admin_key` query param)
- Add `GET /stats` and `GET /users` endpoints
- Every route in this router is automatically protected

### Task 15.4: Nest routers inside a parent router
```python
router = APIRouter(prefix="/api")
router.include_router(public_router)    # → /api/v1/*
router.include_router(private_router)   # → /api/v1/admin/*
```
- Add a `GET /version` directly on the parent router (becomes `/api/version`)

### Task 15.5: Register the parent router in main.py
```python
from routes import advanced_routing
app.include_router(advanced_routing.router)
```

### Task 15.6: Test the URL hierarchy
```bash
curl http://127.0.0.1:8000/api/v1/health
curl "http://127.0.0.1:8000/api/v1/products?category=electronics"
curl "http://127.0.0.1:8000/api/v1/admin/stats?x_admin_key=admin-secret"
curl "http://127.0.0.1:8000/api/v1/admin/stats"  # → 403 forbidden
curl http://127.0.0.1:8000/api/version
```

### Task 15.7: Open /docs and see how tags group the endpoints
- Public endpoints appear under "Public" tag
- Admin endpoints appear under "Admin" tag

---

## Group 16 — Create Shared Models (Optional)

### Task 16.1: Create models/schemas.py
- Define reusable models: `UserBase`, `UserCreate`, `UserRead`
- Define a `PaginatedResponse` generic model
- Import and use these in multiple route files instead of redefining models

---

## Group 17 — Build Your Own Mini Project

Now combine everything into a small real API. Pick one:

### Option A: Todo API
- CRUD for todos (id, title, done, created_at)
- Filter by `done` status (query param)
- Pagination (skip/limit)
- Proper status codes (201 for create, 204 for delete)
- Response model that hides any internal fields
- Background task that logs todo completion

### Option B: Blog API
- CRUD for posts (id, title, body, author, published_at, tags)
- List posts with pagination + tag filter
- Search posts by keyword (query param)
- File upload for post images
- Protected admin routes for create/update/delete (API key guard)
- Nested comments (path: `/posts/{id}/comments`)

### Option C: URL Shortener
- POST to create short URL (accept long URL in JSON body, return short code)
- GET /{code} redirects to original URL (use 302 redirect)
- GET /{code}/stats returns click count
- List all URLs with pagination
- Background task that logs redirect events

---

## Cheat Sheet — Testing Commands Reference

### Query parameters
```bash
curl "http://127.0.0.1:8000/search?q=test&page=2"
```

### Path parameters
```bash
curl http://127.0.0.1:8000/users/42/profile
```

### Request body (JSON)
```bash
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.0}'
```

### Headers
```bash
curl -H "X-API-Key: secret" http://127.0.0.1:8000/secure-data
```

### Cookies
```bash
curl -b "session_id=abc123" http://127.0.0.1:8000/read-cookie
```

### Form data
```bash
curl -X POST http://127.0.0.1:8000/login -d "username=alice&password=pass"
```

### File upload
```bash
curl -X POST http://127.0.0.1:8000/upload -F "file=@myfile.txt"
```

### Show response headers (verbose)
```bash
curl -v http://127.0.0.1:8000/items
```

### WebSocket (browser console)
```js
let ws = new WebSocket("ws://127.0.0.1:8000/ws/echo");
ws.onmessage = e => console.log(e.data);
ws.send("Hello!");
```

---

**Done!** Work through each group, tick the boxes as you go, and by the end
you'll have hands-on experience with every FastAPI routing concept.
