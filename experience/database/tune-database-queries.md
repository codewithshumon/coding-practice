# Tune Database Queries

> **Category:** Database & Data Modeling
> **Relevant at:** Impressive Security, MVI Solutions
> **Related tech docs:** `case/database/databases.md` (Database Optimization §45–55, PostgreSQL §1–11), `case/structures-architecture/backend-systems.md` (Performance Tuning §41–48, System Optimization §49–56)

---

## 1. What This Means

Tuning database queries means **profiling, analyzing, and optimizing** SQL queries so they run efficiently at scale — using indexes strategically, eliminating N+1 patterns, and ensuring the query planner does the least work possible.

**Scope:**
- **Profiling** — `EXPLAIN ANALYZE`, slow query logs, query statistics
- **Index strategy** — composite, covering, and partial indexes matched to query patterns
- **N+1 elimination** — eager loading (`select_related` / `prefetch_related` / joins)
- **Query rewriting** — avoiding `SELECT *`, reducing subqueries, using CTEs judiciously
- **Connection management** — pooling, avoiding connection exhaustion under load

**Why it matters:** slow queries are the #1 cause of slow endpoints and outages. An unindexed query scanning a million rows takes seconds; the same query with the right index takes milliseconds. Query tuning is the highest-leverage performance work in most applications.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The profiling loop (the core workflow):**
```
Slow endpoint identified
   → EXPLAIN ANALYZE the offending query
      → find the bottleneck (seq scan? missing index? N+1?)
         → apply the fix (add index, eager-load, rewrite)
            → re-measure — confirm the improvement
```

**Common scenarios:**
- **List endpoint slows as data grows** — missing index on the filter/sort columns; query does a sequential scan
- **N+1 on a detail page** — fetching a list, then one query per item for related data; fixed with `select_related`/`prefetch_related`
- **Dashboard query times out** — aggregating millions of rows; fixed with a covering index or materialized view
- **Connections exhausted** — too many concurrent queries opening DB connections; fixed with a pooler (PgBouncer)

**Real-world examples:**
- An orders endpoint that filters by `(customer_id, status)` and sorts by `created_at` — needs a composite index `(customer_id, status, created_at DESC)` to avoid a seq scan + sort
- A Django list view doing 1 + N queries (one for the list, one per order's items) — `prefetch_related("items")` turns 101 queries into 2

**The principle:** **measure first, never guess.** Intuition about what's slow is frequently wrong. `EXPLAIN ANALYZE` shows exactly what the planner does.

---

## 3. How to Implement

### Step 1 — Profile with EXPLAIN ANALYZE

```sql
-- Before: a slow query — WHY is it slow?
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE customer_id = 42 AND status = 'paid'
ORDER BY created_at DESC LIMIT 20;

-- Output shows:
-- Seq Scan on orders  (cost=0.00..48231.00 rows=1 width=...)  ← BAD: scans everything
--   Filter: (customer_id = 42 AND status = 'paid')
--   Rows Removed by Filter: 999983   ← scanned a million rows to find 17
-- Planning Time: 0.12 ms  Execution Time: 1240.00 ms
```

**Read the plan:**
- **Seq Scan** = full table scan (bad, usually means missing index)
- **Index Scan / Index Only Scan** = using an index (good)
- **Sort** = sorting in memory/disk (can be avoided if index matches sort order)
- **Rows Removed by Filter** = how many rows it scanned and threw away (high = missing index)

### Step 2 — Add the Right Index

```sql
-- Composite index matching the query's filter + sort
CREATE INDEX idx_orders_customer_status_created
    ON orders (customer_id, status, created_at DESC);

-- Re-measure
EXPLAIN ANALYZE SELECT * FROM orders
WHERE customer_id = 42 AND status = 'paid'
ORDER BY created_at DESC LIMIT 20;

-- Output now:
-- Index Scan using idx_orders_customer_status_created  (cost=0.42..8.34 rows=17)
--   Index Cond: (customer_id = 42 AND status = 'paid')
-- Execution Time: 0.43 ms   ← 1240ms → 0.43ms
```

**Index design rules:**
- **Column order matters** — filter columns first, then sort columns (so the index serves both)
- **Covering index** — include selected columns (`INCLUDE`) for index-only scans (no table lookup)
- **Partial index** — index only matching rows (`WHERE status = 'active'`) for smaller, faster indexes
- **Don't over-index** — every index slows writes; index only what you query

### Step 3 — Eliminate N+1 Queries

```python
# BAD: N+1 — 1 query for orders, then 1 per order for items (101 total)
orders = Order.objects.all()
for order in orders:
    print(order.items.count())   # hits the DB each time

# GOOD (Django): prefetch_related for many-to-many / reverse FK
orders = Order.objects.prefetch_related("items")
for order in orders:
    print(order.items.all())   # no extra queries — 2 total

# GOOD (Django): select_related for foreign key (JOIN)
orders = Order.objects.select_related("customer")
for order in orders:
    print(order.customer.name)   # JOIN'd in one query
```

```typescript
// BAD: N+1 in a loop (Prisma/TypeORM)
const orders = await prisma.order.findMany();
for (const o of orders) {
  const items = await prisma.item.findMany({ where: { orderId: o.id } }); // N queries
}

// GOOD: include the relation in one query
const orders = await prisma.order.findMany({ include: { items: true } }); // 1 query (or 2)
```

### Step 4 — Connection Pooling

```bash
# PgBouncer — reuse connections, avoid exhaustion under load
# Without pooler: each request opens a connection → "too many connections" at scale
# With PgBouncer: a small pool of connections serves many requests

# pgbouncer.ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb
[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
```

### Query Tuning Checklist

- [ ] **EXPLAIN ANALYZE** run on slow queries — know what the planner does
- [ ] **Indexes match query patterns** (filter columns first, then sort)
- [ ] **N+1 eliminated** — `select_related`/`prefetch_related`/`include`/JOINs
- [ ] **No `SELECT *`** — fetch only needed columns (covering index helps)
- [ ] **Pagination on large lists** (cursor preferred)
- [ ] **Connection pooling** (PgBouncer / app pool)
- [ ] **Slow query log monitored** — find the worst offenders by total time
- [ ] **Re-measured after changes** — confirm the win, watch for regressions
- [ ] **Write performance considered** — don't add indexes that slow writes

### Avoid These

- **Tuning without profiling** — guessing what's slow wastes effort on the wrong query
- **Single-column indexes for multi-column queries** — a composite index serves the query in one lookup
- **Ignoring N+1** — the most common silent killer; endpoints slow as data grows
- **Over-indexing** — every index speeds reads but slows writes
- **`SELECT *`** — fetches unnecessary data, prevents index-only scans
- **No connection pooling** — connection exhaustion under load
- **Optimizing cold paths** — focus on queries in the hot path (frequently-called endpoints)
