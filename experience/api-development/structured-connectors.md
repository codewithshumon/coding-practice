# Build Structured Connectors

> **Category:** API Development & Integration
> **Relevant at:** Eicra Soft
> **Related tech docs:** `case/api/apis-and-communication.md` (Third-Party Integrations §49–56), `case/structures-architecture/architecture-patterns.md` (Multi-Tenant SaaS §17–24, Event-Driven §9–16), `case/messaging/message-queues.md` (Queues §1–11, Bull §34–44)

---

## 1. What This Means

Building structured connectors means creating **production-grade integration modules** that connect complex third-party platforms — ERP systems, eCommerce engines, external data APIs — into a SaaS platform. These aren't one-off scripts; they're maintainable, resilient, and follow the same engineering standards as the core platform.

**Scope:**
- ERP integrations: syncing inventory, orders, financials, customers between the SaaS and external ERPs
- eCommerce connectors: product feeds, order pipelines, pricing synchronization
- Data API connectors: ingesting and normalizing data from external sources into the SaaS data model
- Building connectors that handle **rate limits, pagination, schema differences, and failure recovery** — with logging, monitoring, and alerting

**Why it matters:** enterprise SaaS customers expect the platform to "just work" with their existing systems. A connector that silently fails, drops data, or requires constant manual intervention undermines the entire SaaS value proposition.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The connector is a product, not a script:**
- It has its own **data model** (mapping external schemas → internal schemas)
- It has **error handling** (retries, dead-letter queues, alerting)
- It has **tests** (integration tests, recorded API responses)
- It has **monitoring** (sync frequency, error rates, latency)
- It runs on a **schedule or via events**, not manually

**ERP Integration Example (Eicra Soft — B2B eCommerce):**
- Every night: sync product inventory from the customer's ERP into the SaaS catalog
- Real-time: push new orders from the SaaS platform into the ERP for fulfillment
- Both directions need **idempotency** (same sync run twice = no duplicates)
- Schema mapping: ERP's `ITEM_NUMBER` → SaaS's `sku`, ERP's `QTY_ON_HAND` → SaaS's `stock_level`

**Architecture of a production connector:**
```
[Scheduler / Cron] → [Connector Service] → [External ERP API]
                            │
                            ▼
                     [Schema Mapper] → [Validation]
                            │
                            ▼
                     [SaaS Platform API]
                            │
                     [Dead-Letter Queue] (for failures)
                            │
                     [Alerting if failure rate > threshold]
```

**This is the same quality bar as the SaaS platform** — just focused on external-system interaction rather than internal business logic.

---

## 3. How to Implement

### Connector Architecture

```python
class ERPConnector:
    """Structured connector — production-grade, not a script."""

    def __init__(self, config: ERPConfig, mapper: SchemaMapper, platform: PlatformAPI):
        self.client = ResilientClient(config.base_url, config.api_key)
        self.mapper = mapper       # external format → internal format
        self.platform = platform   # your SaaS API

    async def sync_inventory(self, tenant_id: str) -> SyncResult:
        try:
            raw_items = await self._fetch_all_paginated("/api/inventory")
            mapped = [self.mapper.to_internal(item) for item in raw_items]
            validated = [item for item in mapped if self.mapper.validate(item)]
            results = await self.platform.upsert_inventory(tenant_id, validated)
            return SyncResult(synced=len(results), failed=len(mapped) - len(validated))
        except Exception as e:
            await self._handle_failure("inventory_sync", tenant_id, e)
            raise
```

### Schema Mapper — The Heart of Every Connector

```python
class SchemaMapper:
    """Maps external (often ugly) schemas to your clean internal model."""

    # External → Internal mapping table
    FIELD_MAP = {
        "ITEM_NUMBER":   "sku",           # ERP field → your field
        "QTY_ON_HAND":   "stock_level",
        "UNIT_PRICE":    "price",
        "DESCRIPTION":   "description",
    }

    def to_internal(self, erp_item: dict) -> dict:
        return {
            internal: self._transform(erp_item.get(external))
            for external, internal in self.FIELD_MAP.items()
        }

    def _transform(self, value):
        """Hook for per-field transforms (currency, units, etc.)"""
        return value

    def validate(self, item: dict) -> bool:
        return bool(item.get("sku") and item.get("price") is not None)
```

**Why:** when the ERP changes a field name or format, you change the mapper — not every consumer of the data.

### Resilience — Built In, Not Bolted On

```python
class ResilientClient:
    """HTTP client with retry, circuit breaker, and rate-limit awareness."""

    def __init__(self, base_url: str, api_key: str):
        self.client = httpx.AsyncClient(base_url=base_url, headers={"X-API-Key": api_key})
        self.breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)
        self.rate_limiter = TokenBucket(capacity=10, refill_rate=1)  # 10 req/sec

    async def _fetch_all_paginated(self, path: str) -> list[dict]:
        """Handle pagination — external APIs rarely return everything at once."""
        all_items = []
        cursor = None
        while True:
            params = {"limit": 100, "cursor": cursor} if cursor else {"limit": 100}
            response = await self._call_with_resilience("GET", path, params=params)
            data = response.json()
            all_items.extend(data["items"])
            cursor = data.get("next_cursor")
            if not cursor: break
        return all_items

    async def _call_with_resilience(self, method, path, **kwargs):
        await self.rate_limiter.acquire()         # respect rate limits
        for attempt in range(3):
            try:
                resp = await self.client.request(method, path, timeout=30, **kwargs)
                resp.raise_for_status()
                self.breaker.record_success()
                return resp
            except (httpx.TimeoutException, httpx.HTTPStatusError) as e:
                if attempt == 2: raise
                await asyncio.sleep(2 ** attempt)
```

### Connector Checklist

- [ ] **Schema mapper** — external format normalized to your model; mapper is the single source of truth
- [ ] **Pagination handling** — every list endpoint handled, no missing data
- [ ] **Rate limiting respected** — token bucket prevents hammering the external API
- [ ] **Retry with backoff** — transient failures recover
- [ ] **Circuit breaker** — external outage doesn't cascade
- [ ] **Idempotent syncs** — same data run twice ≠ duplicate rows
- [ ] **Dead-letter queue** — failed items preserved for inspection
- [ ] **Logging + alerting** — silent failures are production incidents
- [ ] **Integration tests** — recorded responses, no live API calls in CI
- [ ] **Health dashboard** — per-connector sync status, error rates, last success timestamp

### Avoid These

- **Ad-hoc scripts without structure** — "just import the CSV" becomes unmaintainable
- **No mapper layer** — the connector couples your platform's schema to the vendor's schema
- **Ignoring pagination** — silently syncing only the first page of data
- **No rate limiting** — getting throttled by the external API and losing data
- **Silent failures** — connector crashes at 3am, nobody knows until a customer reports stale data
- **Unbounded retries** — retrying a permanent error forever fills logs and burns resources
