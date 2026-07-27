# Build & Maintain APIs

> **Category:** API Development & Integration
> **Relevant at:** Codixel (high-throughput earnings call platform), Impressive Security (travel supplier & payment integrations), Eicra Soft (versioned microservice APIs)
> **Related tech docs:** `case/api/apis-and-communication.md` (REST §1–8, JSON §33–40, XML §41–48), `case/structures-architecture/architecture-patterns.md` (Microservices §1–8, Event-Driven §9–16), `case/security/security-and-auth.md` (API Security §1–8)

---

## 1. What This Means

Building and maintaining APIs means creating **RESTful backend services** that handle high throughput reliably — with proper versioning, pagination, error handling, and integration with external systems.

**Scope:**
- Designing APIs that are **scalable** (horizontal scaling, caching, rate limiting) and **resilient** (circuit breakers, retries, idempotency)
- Handling **high-throughput event processing** — hundreds of events daily with low latency (Codixel earnings calls)
- Integrating with **external domain systems** — travel suppliers, payment gateways, airline APIs (Impressive Security)
- Building **versioned microservice APIs** — backward-compatible contract evolution (Eicra Soft)

**Why it matters:** an API is the contract between services and clients. Poor API design — missing pagination, wrong status codes, no versioning — creates cascading problems for every consumer downstream.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**High-Throughput Event Processing (Codixel):**
- APIs that ingest, classify, and publish financial events at scale
- Low-latency responses required — every millisecond counts in financial data
- Stateless API servers behind a load balancer → horizontal scaling
- Event-driven: API receives, enqueues to SQS, worker processes and publishes

**Travel Domain APIs (Impressive Security):**
- Building REST APIs that orchestrate calls to multiple external suppliers (GDS, NDC, OTA)
- Payment processing modules that talk to payment gateways
- Supplier connectivity layers that normalize different airline/hotel API formats into a unified model
- API versioning critical — travel integrations are long-lived contracts

**Versioned Microservice APIs (Eicra Soft):**
- Each microservice exposes a versioned REST API (`/v1/`, `/v2/`)
- Backward compatibility maintained across versions
- Clean service boundaries with well-defined contracts
- Multi-tenant: every request carries tenant context

**The common thread across all three:** RESTful design principles + domain-specific business logic + production resilience (retries, idempotency, monitoring).

---

## 3. How to Implement

### REST API Design Fundamentals

```
GET    /v1/orders?cursor=abc&limit=20     → 200 + paginated results
POST   /v1/orders                          → 201 Created + Location header
GET    /v1/orders/{id}                     → 200 or 404
PATCH  /v1/orders/{id}                     → 200
DELETE /v1/orders/{id}                     → 204 No Content
```

**Always:**
- Nouns, not verbs (`/orders`, not `/createOrder`)
- **Paginate every list** (cursor > offset for large datasets)
- Return correct status codes
- **Version from day one** (`/v1/`)

### High-Throughput API Pattern

```python
@router.post("/events")
async def ingest_event(event: FinancialEvent, queue: SQSClient = Depends()):
    # Validate and respond fast — don't process synchronously
    await queue.send(EventQueued(event_id=event.id, data=event.json()))
    return {"status": "accepted", "event_id": event.id}   # 202 Accepted

# Worker processes asynchronously
async def process_events():
    while True:
        messages = await queue.receive(max=10)
        for msg in messages:
            await classify_and_publish(msg)
            await queue.delete(msg)
```

**Why:** the API responds in single-digit ms — the heavy work (classification, publishing) happens asynchronously. The queue absorbs spikes.

### Versioned Microservice API

```typescript
// v1: original contract
@Controller("v1/orders")
export class OrdersV1Controller {
  @Post() create(@Body() dto: CreateOrderV1Dto) { ... }
}

// v2: evolved contract, v1 still served
@Controller("v2/orders")
export class OrdersV2Controller {
  @Post() create(@Body() dto: CreateOrderV2Dto) { ... }   // richer schema
}
```

**Why:** old clients keep working on v1; new features go to v2. When v1 traffic drops to zero, deprecate and remove.

### Resilience Patterns for Every API

```python
# Circuit breaker around external calls
@circuit_breaker(failure_threshold=5, recovery_timeout=30)
async def call_supplier_api(request: SupplierRequest) -> SupplierResponse:
    return await http_client.post(url, json=request.dict())

# Idempotency for safe retries
@router.post("/payments")
async def create_payment(idempotency_key: str = Header(...)):
    existing = await db.find_by_idempotency_key(idempotency_key)
    if existing: return existing   # duplicate → return same result
    payment = await process_payment()
    await db.save_with_idempotency_key(idempotency_key, payment)
    return payment
```

### Cross-Framework Checklist

- [ ] All list endpoints are paginated (cursor preferred for large data)
- [ ] API is versioned (`/v1/`, `/v2/`)
- [ ] Correct HTTP status codes used throughout
- [ ] Idempotency keys on all write endpoints
- [ ] Circuit breakers around external service calls
- [ ] Rate limiting per client/key
- [ ] Consistent error format across all endpoints
- [ ] Request/response validation (schemas, DTOs)
- [ ] OpenAPI/Swagger documentation

### API Monitoring

- **Latency (p50, p95, p99):** catch slow endpoints before users notice
- **Error rate:** spikes means bugs or downstream failures
- **Throughput:** are you handling the expected volume?
- **Circuit breaker state:** how often is it opening?

### Avoid These

- **Unbounded lists** — no pagination on a `/users` endpoint that returns 100k rows
- **200 OK for errors** — `{ "error": "not found" }` with status 200 breaks every HTTP tool
- **No versioning** — changing a field type breaks clients silently
- **Non-idempotent writes** — retry on network timeout = duplicate charge
- **Blocking on heavy work** — if processing takes 30 seconds, don't make the API wait
