# Harden API Security

> **Category:** Security
> **Relevant at:** Impressive Security
> **Related tech docs:** `case/security/security-and-auth.md` (API Security §1–8, OAuth §9–16, JWT §17–24), `case/api/apis-and-communication.md` (REST §1–8), `case/caching/caching.md` (Redis rate-limiting example §10)

---

## 1. What This Means

Hardening API security means protecting API endpoints from abuse, attacks, and data exposure — applying **rate limiting, input validation, CORS, OWASP mitigations, API key management, OAuth 2.0, JWT, and request signing** as layered defenses.

**Scope:**
- **Authentication & authorization** — OAuth 2.0 / JWT / API keys, least privilege
- **Input validation** — schema-validate every payload; prevent injection
- **Rate limiting** — cap requests per client/key to prevent abuse and DoS
- **CORS** — restrict which origins can call the API
- **OWASP mitigations** — defense against the API security top 10
- **Request signing / secrets** — prove caller identity; never leak credentials

**Why it matters:** every endpoint is an attack surface. A single missing control — unvalidated input, no rate limit, a leaked key — can lead to data breaches, abuse, or full compromise. API security is **defense in depth**: no single technique covers everything.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**Layered defense at every endpoint:**
```
Request → [TLS] → [CORS check] → [Rate limit] → [Auth (OAuth/JWT/key)]
   → [Input validation] → [Authorization (scope check)] → [Business logic]
```
Each layer rejects bad requests early, before they reach business logic.

**Real-world threats and their mitigations:**
| Threat | Mitigation |
|---|---|
| Abuse / DoS | Rate limiting per client/key |
| Injection (SQL/NoSQL/command) | Parameterized queries, input validation |
| Broken auth | OAuth + JWT, least privilege, short-lived tokens |
| Excessive data exposure | Return only needed fields; field-level auth |
| Mass assignment | Whitelist allowed fields (DTOs) |
| Leaked credentials | Secrets manager, no keys in code/logs |
| Broken CORS | Restrict origins (never `*` in production) |
| Forged requests | Request signing (HMAC/SigV4) |

**The principle:** validate at the boundary, fail closed (deny by default), and assume every input is hostile.

---

## 3. How to Implement

### Authentication + Authorization (separate concerns)

```python
# Authentication: who are you? (OAuth/JWT/API key)
# Authorization: what can you do? (scopes/roles — least privilege)

@router.get("/orders/{order_id}")
async def get_order(order_id: str, user: AuthUser = Depends(get_current_user)):
    # Auth done (JWT validated in dependency)
    # Authorization: can THIS user see THIS order?
    order = await orders.get(order_id)
    if order.tenant_id != user.tenant_id or order.customer_id != user.customer_id:
        raise HTTPException(403)   # fail closed
    return order
```

### Input Validation — Never Trust the Client

```python
from pydantic import BaseModel, validator

class CreateOrderDTO(BaseModel):
    customer_id: str
    items: list[OrderItem]
    # No arbitrary fields accepted — mass assignment prevented

    @validator("items")
    def non_empty(cls, v):
        if not v: raise ValueError("items required")
        return v

@router.post("/orders")
async def create(dto: CreateOrderDTO):   # invalid payloads rejected before logic
    ...

# Queries always parameterized — no string concatenation
await db.execute("SELECT * FROM orders WHERE id = $1", order_id)  # not f-string
```

### Rate Limiting

```python
# Redis token bucket — shared across instances (see case/caching/caching.md §10)
async def rate_limit(client_id: str, limit=100, window=60):
    key = f"rate:{client_id}"
    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, window)
    if count > limit:
        raise HTTPException(429, "Too Many Requests")
```

### CORS — Restrict, Don't Open

```python
# NEVER: allow_origins=["*"] with credentials in production
app.add_middleware(CORSMiddleware,
    allow_origins=["https://app.example.com"],   # explicit list
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization"],
    allow_credentials=True,
)
```

### API Key + Request Signing

```python
# Keys are credentials — rotate, scope, never commit
# Request signing (HMAC) proves the caller without sending the secret
def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)   # constant-time compare
```

### API Security Checklist

- [ ] **TLS everywhere** — no plaintext API traffic
- [ ] **Auth on every endpoint** (OAuth/JWT/API key), with **least-privilege authorization**
- [ ] **Input validation** on every payload (schemas/DTOs)
- [ ] **Parameterized queries** — no string-built SQL
- [ ] **Rate limiting** per client/key
- [ ] **CORS restricted** to known origins (never `*` + credentials)
- [ ] **Secrets in a secrets manager** — never in code, logs, or URLs
- [ ] **Return only needed fields** — no excessive data exposure
- [ ] **Whitelist writable fields** — prevent mass assignment
- [ ] **Security events logged** — failed auth, rate hits, blocked requests
- [ ] **OWASP API Top 10** tracked as ongoing awareness

### Avoid These

- **`200 OK` for errors** — breaks HTTP semantics and security tooling
- **String-concatenated queries** — SQL injection
- **CORS `*` with credentials** — any site can call your API authenticated
- **Keys in code/logs/URLs** — leaked credentials
- **No rate limiting** — abuse, DoS, runaway cost
- **Trusting client-supplied IDs for authorization** — IDOR (accessing others' resources)
- **Broad permissions** — over-privileged tokens/keys
