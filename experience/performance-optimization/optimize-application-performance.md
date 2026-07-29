# Optimize Application Performance

> **Category:** Performance & Optimization
> **Relevant at:** Impressive Security, MVI Solutions, Codixel
> **Related tech docs:** `case/structures-architecture/backend-systems.md` (Performance Tuning §41–48), `case/database/databases.md` (Database Optimization §45–55), `case/caching/caching.md` (Redis §1–11, Caching Strategies §23–33), `case/api/apis-and-communication.md` (REST §1–8)

---

## 1. What This Means

Optimizing application performance means **continuously profiling and tuning the backend** — application speed, database queries, caching layers (Redis/Memcached), and API response times — to handle **high-traffic scenarios** without degradation.

**Scope:**
- **Bottleneck profiling** — finding the actual slow spot (not guessing)
- **Database query tuning** — indexes, N+1 elimination, slow-query analysis
- **Caching strategy** — Redis/Memcached to reduce DB load and latency
- **API performance** — pagination, payload size, async offloading
- **Application speed** — algorithmic efficiency, connection pooling, resource utilization

**Why it matters:** under high traffic, unoptimized backends degrade exponentially — a query that's fine at 100 requests/min becomes a cascade of timeouts at 10,000. Performance work is what separates a system that scales from one that collapses.

**The golden rule:** **measure first, never guess.** Intuition about bottlenecks is frequently wrong. Profile, find the real slow spot, fix it, re-measure.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The profiling loop (the core workflow):**
```
Slow endpoint / high latency reported
   → profile (APM, slow-query log, EXPLAIN ANALYZE)
      → identify the bottleneck (query? cache miss? N+1? CPU?)
         → apply the targeted fix
            → re-measure — confirm the improvement, watch for regressions
```

**Where bottlenecks usually live (in order of frequency):**
1. **Database** — missing indexes, N+1 queries, unbounded results (the #1 cause)
2. **Caching** — cache misses forcing expensive recomputation/DB hits
3. **External calls** — slow third-party APIs blocking the request
4. **Application code** — inefficient algorithms, heavy loops, serialization

**Real-world scenarios:**
- An orders endpoint slows as data grows → missing composite index → `EXPLAIN ANALYZE` shows a seq scan → add index → 1200ms → 4ms
- A detail page does 1 + N queries → `prefetch_related` → 101 queries → 2
- A report endpoint recomputes aggregations every request → cache the result with TTL → DB load drops 90%
- Heavy work (email sending, report generation) blocks the request → move to a background queue → endpoint responds instantly

**The principle:** focus on the **hot path** — the endpoints/queries called most frequently. Optimizing a rarely-used admin query wastes effort.

---

## 3. How to Implement

### Step 1 — Profile to Find the Real Bottleneck

```python
# APM (Datadog, New Relic, Sentry) shows WHERE time is spent
# Slow query log finds the worst DB queries by total time

# EXPLAIN ANALYZE on the suspect query
EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 42 AND status = 'paid'
ORDER BY created_at DESC LIMIT 20;
# Seq Scan on orders (rows removed by filter: 999983) → MISSING INDEX
```

### Step 2 — Database Tuning (usually the biggest win)

```sql
-- Composite index matching the query pattern (filter → sort)
CREATE INDEX idx_orders_customer_status_created
    ON orders (customer_id, status, created_at DESC);
-- Re-measure: Index Scan, 0.4ms (was 1240ms)
```

```python
# Eliminate N+1 — eager load related data
# BAD: 101 queries
orders = Order.objects.all()
for o in orders: print(o.items.count())

# GOOD: 2 queries
orders = Order.objects.prefetch_related("items")
```

### Step 3 — Caching (Redis / Memcached)

```python
# Cache-aside — DB hit only on miss
async def get_product(product_id: str):
    cache_key = f"product:{product_id}"
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)
    product = await db.products.find_by_id(product_id)   # expensive
    await redis.setex(cache_key, 300, json.dumps(product))  # TTL: 5 min
    return product

# Invalidate on write
async def update_product(product_id, data):
    await db.products.update(product_id, data)
    await redis.delete(f"product:{product_id}")   # stale cache busted
```

### Step 4 — API Performance

```python
# Paginate every list (cursor for large datasets)
GET /orders?cursor=abc&limit=20     # not GET /orders (returns everything)

# Offload heavy work to a queue — don't block the request
@router.post("/reports/generate")
async def generate_report(req):
    job_id = await queue.enqueue("generate_report", req.dict())
    return {"status": "accepted", "job_id": job_id}   # 202, not 30s wait
```

### Step 5 — Connection Pooling

```bash
# PgBouncer — reuse DB connections, avoid exhaustion under load
# Without: each request opens a connection → "too many connections"
# With: small pool serves many requests
```

### Application Performance Checklist

- [ ] **Profiling tool** in place (APM, slow-query log) — measure, don't guess
- [ ] **Indexes match query patterns** (composite indexes for filter + sort)
- [ ] **N+1 eliminated** — `prefetch_related`/`select_related`/`include`/JOINs
- [ ] **Caching on hot reads** — with explicit invalidation
- [ ] **Every list paginated** (cursor preferred for large data)
- [ ] **Heavy work offloaded** to background queues
- [ ] **Connection pooling** configured
- [ ] **Re-measured after changes** — confirm wins, catch regressions
- [ ] **Focus on hot paths** — optimize frequently-called endpoints first

### Avoid These

- **Optimizing without profiling** — fixing the wrong thing
- **Micro-optimizing cold paths** — effort with no user impact
- **Caching without invalidation** — stale data served
- **Over-indexing** — speeds reads but slows writes
- **Unbounded list queries** — works at 100 rows, dies at 100k
- **Blocking requests on heavy work** — synchronous report generation
- **No connection pooling** — connection exhaustion under load
