# Design Multi-Tenant Schemas

> **Category:** Database & Data Modeling
> **Relevant at:** Eicra Soft (multi-tenant PostgreSQL SaaS)
> **Related tech docs:** `case/database/databases.md` (PostgreSQL §1–11, Database Optimization §45–55), `case/structures-architecture/architecture-patterns.md` (Multi-Tenant SaaS §17–24)

---

## 1. What This Means

Designing multi-tenant schemas means structuring a single database to serve **multiple tenants (customers) with isolated data** — choosing the isolation model (database-per-tenant, schema-per-tenant, or row-level with `tenant_id`) and writing queries that are **secure, scalable, and never leak data across tenants**.

**Scope:**
- **Isolation model selection** — the foundational decision (DB-per-tenant / schema-per-tenant / row-level)
- **Tenant context management** — resolving and propagating the tenant through every request
- **Row-Level Security (RLS)** — enforcing isolation at the database layer
- **Optimized queries** — writing PostgreSQL queries that are tenant-aware without performance degradation
- **Per-tenant concerns** — feature flags, configuration, backups, and resource isolation

**Why it matters:** a cross-tenant data leak is one of the most severe production incidents possible — it's a trust violation, often a legal one. The schema design is the foundation; getting isolation wrong at the data layer can't be fully fixed in application code.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The isolation model decision (Eicra Soft):**
| Model | Isolation | Cost | Best for |
|---|---|---|---|
| **Database-per-tenant** | Strongest | High (many DBs) | Regulated/large tenants |
| **Schema-per-tenant** | Strong | Medium | Balanced isolation + efficiency |
| **Row-level (`tenant_id`)** | Weakest | Lowest | Many small tenants |

Eicra Soft's B2B eCommerce SaaS likely uses **schema-per-tenant** or **row-level with RLS** — the balance of isolation and operational efficiency for many business customers.

**Tenant resolution flow:**
```
Request arrives → resolve tenant (subdomain/header/JWT)
   → set tenant context (Postgres session variable)
      → RLS auto-applies WHERE tenant_id = current_tenant to every query
         → query results are tenant-scoped automatically
```

**Real-world scenarios:**
- `acme.app.com` → tenant `acme` → all queries scoped to `acme`'s data
- An admin at `acme` should NEVER see `globex`'s orders, even with a bug in the app code
- Per-tenant backups — restore one customer's data without affecting others
- Per-tenant feature flags — `acme` has the advanced reporting module, `globex` doesn't

**The key principle:** **isolation enforced at the data layer (RLS/schema), not just in application code.** App-level `WHERE tenant_id = ?` filters are error-prone — one forgotten filter leaks data. RLS makes it impossible to forget.

---

## 3. How to Implement

### Model A — Row-Level with PostgreSQL RLS (recommended default)

```sql
-- Step 1: Every tenant-scoped table has a tenant_id column
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    customer_id UUID,
    total NUMERIC(10,2),
    created_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_orders_tenant_created ON orders (tenant_id, created_at DESC);

-- Step 2: Enable Row-Level Security
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Step 3: Policy — rows are visible only when tenant_id matches the session's tenant
CREATE POLICY tenant_isolation ON orders
    USING (tenant_id = current_setting('app.current_tenant')::UUID);

-- Step 4: Application sets the tenant context per request
-- (in a connection pool / middleware)
SET LOCAL app.current_tenant = 'acme-tenant-uuid';

-- Now every query is automatically scoped — even without a WHERE clause:
SELECT * FROM orders;  -- only returns acme's orders
```

**Why:** even if a developer forgets `WHERE tenant_id = ?`, RLS enforces it. The database refuses to return another tenant's rows.

### Model B — Schema-per-Tenant

```sql
-- Each tenant gets their own schema (isolated tables, same DB server)
CREATE SCHEMA tenant_acme;
CREATE TABLE tenant_acme.orders (...);
CREATE SCHEMA tenant_globex;
CREATE TABLE tenant_globex.orders (...);

-- Application sets the search_path per request
SET search_path TO tenant_acme, public;
SELECT * FROM orders;  -- reads from tenant_acme.orders

-- Per-tenant operations are clean: backup, migrate, drop one tenant
pg_dump --schema=tenant_acme > acme_backup.sql
```

**Why:** stronger isolation, easy per-tenant backup/migration, but more operational overhead (managing many schemas).

### Tenant Context in Application Code

```python
# FastAPI middleware — resolve + set tenant context per request
@app.middleware("http")
async def tenant_middleware(request: Request, call_next):
    tenant_id = resolve_tenant(request)   # from subdomain, header, or JWT
    if not tenant_id:
        return JSONResponse({"error": "tenant required"}, 401)

    # Set Postgres session variable for RLS (within a connection)
    async with db.connection() as conn:
        await conn.execute(f"SET LOCAL app.current_tenant = '{tenant_id}'")
        request.state.tenant_id = tenant_id
        return await call_next(request)

# Now repository code is simple — no manual tenant filtering
class OrderRepository:
    async def list_orders(self) -> list[Order]:
        # RLS handles isolation — no WHERE tenant_id = ?
        return await db.fetch_all("SELECT * FROM orders ORDER BY created_at DESC")
```

### Optimized Tenant-Aware Queries

```sql
-- Indexes MUST lead with tenant_id (tenant-scoped queries always filter on it)
CREATE INDEX idx_orders_tenant_status_date
    ON orders (tenant_id, status, created_at DESC);

-- Good: query uses the index (tenant first, then status, then sort)
SELECT * FROM orders
WHERE tenant_id = $1 AND status = 'paid'
ORDER BY created_at DESC LIMIT 20;

-- Bad: tenant_id not first → index can't be used efficiently
-- (Also unnecessary if RLS is active — RLS adds it implicitly)
SELECT * FROM orders WHERE status = 'paid' ORDER BY created_at DESC;
```

### Multi-Tenant Schema Checklist

- [ ] **Isolation model chosen deliberately** (DB/schema/row-level) — changing later is expensive
- [ ] **Isolation enforced at the data layer** (RLS or schema separation), not app code alone
- [ ] **Tenant context resolved** on every request (subdomain/header/JWT)
- [ ] **Tenant context propagated** via session variable / `search_path`
- [ ] **Indexes lead with `tenant_id`** (or are per-schema)
- [ ] **Tested for leaks** — automated tests that verify cross-tenant queries return nothing
- [ ] **Per-tenant capabilities** — backups, feature flags, rate limits
- [ ] **Noisy-neighbor protection** — one tenant can't degrade others

### Avoid These

- **App-level filtering only** — one forgotten `WHERE tenant_id = ?` leaks data
- **Indexes not starting with `tenant_id`** — queries scan all tenants' data (slow)
- **No isolation testing** — assuming it works; cross-tenant leaks go undetected
- **Shared mutable state** — caches/config not keyed by tenant
- **Choosing the wrong isolation model early** — migrating from row-level to DB-per-tenant later is extremely costly
- **No noisy-neighbor protection** — one tenant's heavy query degrades everyone
