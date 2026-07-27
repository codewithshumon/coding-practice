# Databases — Complete Guide

> **Series:** Databases Documentation — Part 1
> This file covers the **core database systems** (PostgreSQL, MySQL, DynamoDB, MongoDB) and **Database Optimization** as a cross-cutting discipline. More topics (Redis, Elasticsearch, time-series DBs, database internals) will be added as separate files later.

---

## Table of Contents

- [Shared Orientation — Choosing a Database](#shared-orientation--choosing-a-database)
- **PostgreSQL**
  - [1. What Is PostgreSQL?](#1-what-is-postgresql)
  - [2. PostgreSQL vs MySQL vs NoSQL](#2-postgresql-vs-mysql-vs-nosql)
  - [3. How PostgreSQL Works](#3-how-postgresql-works)
  - [4. PostgreSQL Data Model and Key Features](#4-postgresql-data-model-and-key-features)
  - [5. Where to Use PostgreSQL](#5-where-to-use-postgresql)
  - [6. Where NOT to Use PostgreSQL](#6-where-not-to-use-postgresql)
  - [7. Installing and Setting Up PostgreSQL](#7-installing-and-setting-up-postgresql)
  - [8. PostgreSQL Connection and Authentication](#8-postgresql-connection-and-authentication)
  - [9. PostgreSQL Production Best Practices](#9-postgresql-production-best-practices)
  - [10. PostgreSQL Real-World Examples](#10-postgresql-real-world-examples)
  - [11. PostgreSQL Pitfalls](#11-postgresql-pitfalls)
- **MySQL**
  - [12. What Is MySQL?](#12-what-is-mysql)
  - [13. MySQL vs PostgreSQL](#13-mysql-vs-postgresql)
  - [14. How MySQL Works](#14-how-mysql-works)
  - [15. MySQL Data Model and Key Features](#15-mysql-data-model-and-key-features)
  - [16. Where to Use MySQL](#16-where-to-use-mysql)
  - [17. Where NOT to Use MySQL](#17-where-not-to-use-mysql)
  - [18. Installing and Setting Up MySQL](#18-installing-and-setting-up-mysql)
  - [19. MySQL Connection and Authentication](#19-mysql-connection-and-authentication)
  - [20. MySQL Production Best Practices](#20-mysql-production-best-practices)
  - [21. MySQL Real-World Examples](#21-mysql-real-world-examples)
  - [22. MySQL Pitfalls](#22-mysql-pitfalls)
- **DynamoDB**
  - [23. What Is DynamoDB?](#23-what-is-dynamodb)
  - [24. DynamoDB vs Relational vs MongoDB](#24-dynamodb-vs-relational-vs-mongodb)
  - [25. How DynamoDB Works](#25-how-dynamodb-works)
  - [26. DynamoDB Data Model and Key Features](#26-dynamodb-data-model-and-key-features)
  - [27. Where to Use DynamoDB](#27-where-to-use-dynamodb)
  - [28. Where NOT to Use DynamoDB](#28-where-not-to-use-dynamodb)
  - [29. Setting Up DynamoDB](#29-setting-up-dynamodb)
  - [30. DynamoDB Access and Authentication](#30-dynamodb-access-and-authentication)
  - [31. DynamoDB Production Best Practices](#31-dynamodb-production-best-practices)
  - [32. DynamoDB Real-World Examples](#32-dynamodb-real-world-examples)
  - [33. DynamoDB Pitfalls](#33-dynamodb-pitfalls)
- **MongoDB**
  - [34. What Is MongoDB?](#34-what-is-mongodb)
  - [35. MongoDB vs Relational vs DynamoDB](#35-mongodb-vs-relational-vs-dynamodb)
  - [36. How MongoDB Works](#36-how-mongodb-works)
  - [37. MongoDB Data Model and Key Features](#37-mongodb-data-model-and-key-features)
  - [38. Where to Use MongoDB](#38-where-to-use-mongodb)
  - [39. Where NOT to Use MongoDB](#39-where-not-to-use-mongodb)
  - [40. Installing and Setting Up MongoDB](#40-installing-and-setting-up-mongodb)
  - [41. MongoDB Connection and Authentication](#41-mongodb-connection-and-authentication)
  - [42. MongoDB Production Best Practices](#42-mongodb-production-best-practices)
  - [43. MongoDB Real-World Examples](#43-mongodb-real-world-examples)
  - [44. MongoDB Pitfalls](#44-mongodb-pitfalls)
- **Database Optimization**
  - [45. What Is Database Optimization?](#45-what-is-database-optimization)
  - [46. DB Optimization vs General Performance Tuning](#46-db-optimization-vs-general-performance-tuning)
  - [47. How Database Optimization Works](#47-how-database-optimization-works)
  - [48. Core Database Optimization Techniques](#48-core-database-optimization-techniques)
  - [49. Where to Apply Database Optimization](#49-where-to-apply-database-optimization)
  - [50. Database Optimization Limits](#50-database-optimization-limits)
  - [51. Database Optimization Tools and Setup](#51-database-optimization-tools-and-setup)
  - [52. Measurement and Profiling](#52-measurement-and-profiling)
  - [53. Database Optimization Best Practices](#53-database-optimization-best-practices)
  - [54. Database Optimization Real-World Examples](#54-database-optimization-real-world-examples)
  - [55. Database Optimization Pitfalls](#55-database-optimization-pitfalls)
- [Shared Foundations](#shared-foundations)
- [Quick Reference Card](#quick-reference-card)

---

## Shared Orientation — Choosing a Database

These five topics split into two groups: **four database systems** and **one cross-cutting discipline** (optimization, which applies to all of them).

| Database | Model | Sweet spot | One-liner |
|---|---|---|---|
| **PostgreSQL** | Relational (+JSONB) | Feature-rich, complex queries, data integrity | Most capable open-source relational DB |
| **MySQL** | Relational | Simple, read-heavy web apps, huge ecosystem | Popular, battle-tested workhorse |
| **DynamoDB** | NoSQL (key-value/doc) | AWS serverless, massive scale, known access patterns | Serverless NoSQL, single-digit ms |
| **MongoDB** | NoSQL (document) | Flexible schemas, rapid iteration, JSON-like data | Schemaless document store |
| **DB Optimization** | (discipline) | Any database | Index, tune, pool, replicate, denormalize |

**Decision guide:**
- Need power + correctness + flexibility (JSONB, extensions)? → **PostgreSQL**
- Straightforward read-heavy web app, big ecosystem? → **MySQL**
- AWS serverless, key-based access, huge scale? → **DynamoDB**
- Flexible/evolving document schema, rich ad-hoc queries? → **MongoDB**
- Any DB feeling slow? → apply **Database Optimization** (below)

**The common thread:** your **data model and access patterns** drive everything — pick the DB that matches how you read/write, then optimize around those patterns.

---

# PostgreSQL

## 1. What Is PostgreSQL?

**PostgreSQL** is an advanced open-source **relational database** known for **ACID compliance**, powerful query capabilities, **JSONB** (document) support, and extensibility.

- The most standards-compliant and feature-rich open-source relational DB.
- Handles both relational data **and** document-style data (JSONB) in one system.

**One-liner:** the most capable open-source relational database.

## 2. PostgreSQL vs MySQL vs NoSQL

| | PostgreSQL | MySQL | NoSQL (Mongo/Dynamo) |
|---|---|---|---|
| Features | Richest (JSONB, extensions, CTEs, window fns) | Simpler, read-optimized | Flexible schema, no joins |
| Data integrity | Strongest | Strong | Varies |
| Ad-hoc queries | Excellent | Good | Limited (esp. DynamoDB) |
| Best for | Complex/feature-rich apps | Simple read-heavy web apps | Scale/flexible schema |

**Rule of thumb:** choose Postgres when you want **power, correctness, and flexibility** in one database.

## 3. How PostgreSQL Works

- **Relational model** — tables, rows, columns, relationships, SQL.
- **ACID transactions** — guaranteed correctness via multi-version concurrency control (**MVCC**).
- **Query planner/optimizer** — picks an execution plan using statistics + indexes.
- **Indexes** — B-tree (default), GIN/GiST (JSONB, full-text), partial indexes.

**Key point:** MVCC gives high concurrency without read/write blocking; the planner's choices depend on your indexes and stats.

## 4. PostgreSQL Data Model and Key Features

- **Relational** — normalized tables, foreign keys, joins, constraints.
- **JSONB** — store/query documents with relational power (best of both).
- **Advanced SQL** — CTEs, window functions, full-text search.
- **Extensions** — PostGIS (geo), pg_trgm (fuzzy), and more.
- **Row-Level Security (RLS)** — built-in multi-tenant data isolation.
- **Rich indexing** — partial, expression, GIN/GiST indexes.

## 5. Where to Use PostgreSQL

- **General-purpose relational** workloads needing integrity.
- **Complex queries** (reporting, joins, aggregations).
- **Mixed relational + document** (JSONB) in one DB.
- **Multi-tenant SaaS** (schema-per-tenant or RLS isolation).

## 6. Where NOT to Use PostgreSQL

- **Extreme write-scale simple key-value** (DynamoDB may fit better).
- Pure **schemaless** at massive scale with no relational needs.
- Trivial use cases where its power is over-engineering.

## 7. Installing and Setting Up PostgreSQL

```bash
# Docker (quickest for dev)
docker run -e POSTGRES_PASSWORD=pass -p 5432:5432 postgres:15

# Connect
psql -h localhost -U postgres

# Create a database and table
CREATE DATABASE app;
CREATE TABLE users (id serial PRIMARY KEY, email text UNIQUE, data jsonb);
```

## 8. PostgreSQL Connection and Authentication

- **Connection string** — `postgresql://user:pass@host:5432/db`.
- **Roles & privileges** — `CREATE ROLE`, `GRANT` (least privilege).
- **`pg_hba.conf`** — controls who can connect from where + auth method (SCRAM recommended).
- **Connection pooling** — use **PgBouncer** (Postgres connections are expensive).

**Golden rule:** never let app servers open unbounded direct connections — pool them.

## 9. PostgreSQL Production Best Practices

1. **Index for your query patterns** — not every column.
2. **EXPLAIN ANALYZE** slow queries before tuning.
3. **Use connection pooling** (PgBouncer) — essential at scale.
4. **Normalize first, denormalize selectively** for hot reads.
5. **Use JSONB** for genuinely flexible attributes, not to avoid modeling.
6. **Use RLS** for multi-tenant isolation (see architecture-patterns.md).
7. **Monitor vacuum/bloat** — Postgres needs routine maintenance.

## 10. PostgreSQL Real-World Examples

### Example 1 — Table + Index + JSONB
```sql
CREATE INDEX ON orders ((data->>'status'));   -- index inside JSONB
SELECT * FROM orders WHERE data->>'status' = 'paid';
```
**Why:** query document fields at relational speed — flexible schema without losing performance.

### Example 2 — Multi-Tenant with RLS
```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_iso ON orders USING (tenant_id = current_setting('app.tenant')::int);
```
**Why:** the DB enforces tenant isolation — even a forgotten app filter can't leak data.

### Example 3 — ACID Transaction
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;   -- both or neither
```
**Why:** money transfers are atomic — no partial updates.

## 11. PostgreSQL Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Missing indexes | Slow queries, seq scans | Index for query patterns |
| No connection pooling | "Too many connections" | PgBouncer |
| Overusing JSONB | Losing relational benefits | Model relationally; JSONB for true flexibility |
| Ignoring vacuum/bloat | Degrading performance | Monitor autovacuum, tune it |
| N+1 queries | Slow endpoints | Eager-load / join |

---

# MySQL

## 12. What Is MySQL?

**MySQL** is a widely adopted open-source **relational database** known for **strong read performance**, **replication**, and a **mature ecosystem** (hosting, tooling, community).

- The classic web-app database (LAMP stack).
- Simple, fast for reads, and available everywhere.

**One-liner:** the popular, battle-tested relational workhorse.

## 13. MySQL vs PostgreSQL

| | MySQL | PostgreSQL |
|---|---|---|
| Philosophy | Simple, fast reads | Feature-rich, standards |
| Advanced SQL | Basic | Rich (CTEs, window fns, JSONB) |
| Ecosystem/hosting | Huge, ubiquitous | Large, growing |
| Best for | Read-heavy web apps | Complex/feature-rich apps |

**Rule of thumb:** MySQL for straightforward read-heavy web apps; Postgres when you need advanced features and richer SQL.

## 14. How MySQL Works

- **Relational model** — tables, SQL, relationships.
- **Storage engines** — **InnoDB** (default) provides ACID transactions and row-level locking.
- **Replication** — primary handles writes; replicas serve reads.

**Key point:** always use **InnoDB** — the older MyISAM engine lacks transactions and foreign keys.

## 15. MySQL Data Model and Key Features

- **InnoDB engine** — ACID, foreign keys, row-level locking.
- **Replication** — primary/replica read scaling.
- **Partitioning** — split large tables.
- **JSON support** — present but less powerful than Postgres JSONB.
- **Full-text search** — built-in.

## 16. Where to Use MySQL

- **Web applications** (classic LAMP/LEMP).
- **Read-heavy workloads** scaled via replicas.
- When **ecosystem, hosting, or team familiarity** matters.

## 17. Where NOT to Use MySQL

- Need **advanced SQL** (CTEs, window functions, rich JSON) — Postgres.
- Need **extensibility** (custom types, PostGIS-like extensions).
- **Extreme write-scale key-value** — consider NoSQL.

## 18. Installing and Setting Up MySQL

```bash
# Docker
docker run -e MYSQL_ROOT_PASSWORD=pass -p 3306:3306 mysql:8

# Connect + create
mysql -h localhost -u root -p
CREATE DATABASE app;
CREATE USER 'app'@'%' IDENTIFIED BY 'secret';
GRANT ALL ON app.* TO 'app'@'%';
```

## 19. MySQL Connection and Authentication

- **Connection string** — `mysql://user:pass@host:3306/db`.
- **Users & grants** — `CREATE USER`, `GRANT` (least privilege).
- **Connection pooling** — use a pool in your app/ORM (don't open a connection per request).

## 20. MySQL Production Best Practices

1. **Use InnoDB** — never MyISAM.
2. **Index for your queries** — verify with EXPLAIN.
3. **Read replicas** for read scaling.
4. **Avoid `SELECT *`** — fetch only needed columns.
5. **Connection pooling** — essential under load.
6. Keep **transactions short** to reduce lock contention.

## 21. MySQL Real-World Examples

### Example 1 — Indexed Query
```sql
CREATE INDEX idx_email ON users(email);
EXPLAIN SELECT id, email FROM users WHERE email = 'a@b.com';  -- uses idx_email
```
**Why:** turns a full table scan into an index lookup.

### Example 2 — Read Replica Routing
**Why:** send reads to replicas, writes to the primary — scale reads horizontally without touching write capacity.

## 22. MySQL Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Using MyISAM | No transactions/foreign keys | Use InnoDB |
| Missing indexes | Slow queries | Index for query patterns |
| Single primary | Reads overwhelm one node | Read replicas |
| `SELECT *` | Over-fetching, slow | Select only needed columns |
| No pooling | Connection exhaustion | App/ORM connection pool |

---

# DynamoDB

## 23. What Is DynamoDB?

**DynamoDB** is a **fully managed, serverless NoSQL** key-value/document database by AWS, delivering **single-digit millisecond latency** at virtually any scale.

- No servers to manage — AWS handles provisioning, scaling, and replication.
- Scales to enormous throughput; you design around **access patterns**.

**One-liner:** AWS's serverless NoSQL — infinite scale, zero servers.

## 24. DynamoDB vs Relational vs MongoDB

| | DynamoDB | Relational (PG/MySQL) | MongoDB |
|---|---|---|---|
| Model | Key-value / document | Relational (joins, SQL) | Document (rich queries) |
| Scaling | Automatic, massive | Vertical + read replicas | Sharding |
| Query flexibility | Low (key-based) | High (ad-hoc SQL) | Medium-high |
| Ops | None (serverless) | You manage | Self-host or Atlas |

**Rule of thumb:** DynamoDB for **key-based access at massive scale** when you **know your access patterns**; relational for complex/ad-hoc queries.

## 25. How DynamoDB Works

- **Tables** with a **partition key** (+ optional **sort key**) — data is distributed by partition key.
- **Automatic partitioning & scaling** — no capacity planning with on-demand mode.
- **Eventually consistent** reads by default (strong consistency optional).
- **GSIs/LSIs** (indexes) enable alternate query patterns.

**Key point:** you **design the table around your access patterns** — there's no ad-hoc querying like SQL.

## 26. DynamoDB Data Model and Key Features

- **Key-value + document** items.
- **Partition + sort keys** — the core access design.
- **Global Secondary Indexes (GSI)** — alternate query patterns.
- **Streams** — change data capture (trigger Lambdas).
- **TTL** — auto-expire items (free cleanup).
- **Transactions**, **on-demand vs provisioned** capacity.

## 27. Where to Use DynamoDB

- **Serverless applications** on AWS.
- **Key-based access at massive scale** — sessions, leaderboards, user profiles, event data.
- When you **know your access patterns** upfront.
- **Single-digit ms latency** requirements.

## 28. Where NOT to Use DynamoDB

- Need **joins, complex ad-hoc queries**, or relational integrity.
- **Unknown/evolving access patterns** — redesigning keys is painful.
- Heavy **aggregation/analytics** (use a relational or OLAP store).

## 29. Setting Up DynamoDB

No install (fully managed). Create a table via Console, SDK, or CDK:

```python
import boto3
ddb = boto3.resource("dynamodb")
table = ddb.create_table(
    TableName="sessions",
    KeySchema=[{"AttributeName": "session_id", "KeyType": "HASH"}],
    AttributeDefinitions=[{"AttributeName": "session_id", "AttributeType": "S"}],
    BillingMode="PAY_PER_REQUEST",
)
```

**Local dev:** point the SDK at **LocalStack** (see aws.md) — zero cost.

## 30. DynamoDB Access and Authentication

- **IAM-based auth** — not username/password. Use **IAM roles/policies** (least privilege: specific tables + actions).
- Access via the **AWS SDK** (Boto3, `@aws-sdk/client-dynamodb`).
- No connection strings — the SDK signs requests with IAM credentials.

## 31. DynamoDB Production Best Practices

1. **Design around access patterns** (single-table design) — know them before creating the table.
2. **Choose good partition keys** — high cardinality to avoid **hot partitions**.
3. **Use GSIs sparingly** — they add cost and complexity.
4. **Use TTL** for expiring data (sessions, tokens).
5. **Prefer on-demand** capacity for variable/unpredictable load.
6. **Avoid scans** — use queries; scans read the whole table.
7. **Batch operations** (`BatchGetItem`/`BatchWriteItem`) for efficiency.

## 32. DynamoDB Real-World Examples

### Example 1 — Put/Get by Key
```python
table.put_item(Item={"session_id": "abc", "user_id": "42", "expires_at": 1730})
item = table.get_item(Key={"session_id": "abc"})["Item"]
```
**Why:** single-digit ms key lookups at any scale.

### Example 2 — TTL for Sessions
**Why:** enable TTL on `expires_at`; expired sessions are deleted automatically — free cleanup, no cron job.

### Example 3 — Query by Partition + Sort Key
**Why:** `user_id` (partition) + `created_at` (sort) lets you fetch a user's recent items in one efficient query — no scan.

## 33. DynamoDB Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Hot partitions | Throttling on popular keys | High-cardinality partition keys |
| Scans instead of queries | Slow, expensive | Design keys/GSIs for queries |
| Wrong key design | Can't support new access pattern | Plan access patterns upfront |
| Treating it like relational | Missing joins, frustration | Design key-based, denormalize |
| Capacity cost surprises | Unexpected bills | On-demand for variable load |

---

# MongoDB

## 34. What Is MongoDB?

**MongoDB** is a **document-oriented NoSQL** database storing **BSON** (binary JSON) documents with **flexible schemas** and built-in **horizontal scaling** (sharding).

- Documents map naturally to application objects (JSON-like).
- **Schemaless** — fields can vary between documents; evolve without migrations.

**One-liner:** a schemaless document store for flexible, evolving data.

## 35. MongoDB vs Relational vs DynamoDB

| | MongoDB | Relational | DynamoDB |
|---|---|---|---|
| Model | Document (rich, nested) | Relational (joins) | Key-value/document |
| Schema | Flexible | Rigid | Flexible |
| Query flexibility | Medium-high | High (SQL) | Low (key-based) |
| Hosting | Self-host or Atlas | Self-host or managed | AWS only |

**Rule of thumb:** MongoDB for **flexible documents with rich ad-hoc queries**; DynamoDB for pure key-value at AWS scale; relational for integrity + complex joins.

## 36. How MongoDB Works

- **Collections** of BSON **documents**.
- **Indexes** for query performance (like relational).
- **Replica sets** for high availability; **sharding** for horizontal scale.
- **Aggregation pipeline** for transformations/analytics.

**Key point:** you model data as **documents** — embed related data or reference it, based on access patterns.

## 37. MongoDB Data Model and Key Features

- **Documents (BSON)** — nested, JSON-like.
- **Embed vs reference** — denormalize by embedding, or normalize via references.
- **Indexes** — single, compound, text, geospatial.
- **Aggregation pipeline** — powerful data transformations.
- **Change streams** — react to data changes.
- **Multi-document transactions**, **schema validation**.

## 38. Where to Use MongoDB

- **Flexible/evolving schemas** — rapid iteration, varied data.
- **Content management, catalogs, product data**.
- **JSON-like data** that maps naturally to documents.

## 39. Where NOT to Use MongoDB

- Heavy **relational integrity / many joins**.
- When a **rigid, well-defined schema** is actually better.
- Extreme key-value scale where DynamoDB's simplicity wins.

## 40. Installing and Setting Up MongoDB

```bash
# Docker
docker run -p 27017:27017 mongo:7

# Connect
mongosh

# Insert + query
use app
db.users.insertOne({ name: "Shumon", tags: ["admin", "dev"] })
db.users.find({ name: "Shumon" })
```

Or use **MongoDB Atlas** (managed cloud) — no install.

## 41. MongoDB Connection and Authentication

- **Connection string** — `mongodb://user:pass@host:27017/db` (or `mongodb+srv://` for Atlas).
- **Users & roles** — role-based access (read, readWrite, dbAdmin).
- **SCRAM auth**; enable it in production (never run unauthenticated).
- **Connection pooling** — built into the driver; configure pool size.

## 42. MongoDB Production Best Practices

1. **Model around access patterns** — embed what you read together, reference what you don't.
2. **Index for your queries** — verify with `explain()`.
3. **Avoid unbounded arrays** — documents cap at 16MB.
4. **Use the aggregation pipeline** instead of many round trips.
5. **Use schema validation** — flexible ≠ unstructured.
6. **Project only needed fields** — don't fetch whole documents.

## 43. MongoDB Real-World Examples

### Example 1 — Embed vs Reference
```js
// Embed (read together): order with its items
{ _id: 1, customer: "Acme", items: [{ sku: "A", qty: 2 }] }
```
**Why:** one read fetches everything you display together — no joins.

### Example 2 — Indexed Query
```js
db.users.createIndex({ email: 1 })
db.users.find({ email: "a@b.com" }).explain()  // uses the index
```
**Why:** index turns a collection scan into a fast lookup.

### Example 3 — Aggregation Pipeline
```js
db.orders.aggregate([
  { $match: { status: "paid" } },
  { $group: { _id: "$customer", total: { $sum: "$amount" } } }
])
```
**Why:** compute per-customer totals in the DB — no pulling all rows to the app.

## 44. MongoDB Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Unbounded arrays | Docs hit 16MB limit | Reference instead of embed |
| Missing indexes | Slow queries, COLLSCAN | Index for query patterns |
| Over/under-embedding | Awkward reads or bloat | Model around access patterns |
| No schema validation | Inconsistent data | Add validation rules |
| Treating it like relational | Painful joins | Embrace the document model |

---

# Database Optimization

## 45. What Is Database Optimization?

**Database Optimization** is the discipline of making a database fast and efficient at scale — through **query tuning, indexing, connection pooling, read replicas, and schema design** (normalization/denormalization).

- It's **database-specific** — complementing app-level performance work.
- The same principles apply across relational and NoSQL systems.

**One-liner:** make the DB fast via indexes, query tuning, pooling, replication, and smart schema.

## 46. DB Optimization vs General Performance Tuning

| | DB Optimization | App Performance Tuning |
|---|---|---|
| Focus | Queries, indexes, connections, schema | Code, algorithms, rendering |
| Tools | EXPLAIN, slow query log, DB stats | Profilers, APM |
| Lever | Data access | Computation |

**Key point:** this is the **database-specific** slice — for app-level tuning see `backend-systems.md` (Performance Tuning §41–48, System Optimization §49–56).

## 47. How Database Optimization Works

1. **Measure first** — EXPLAIN query plans, slow query log, DB statistics.
2. **Find the bottleneck** — usually a missing index, N+1, or unbounded query.
3. **Apply the right lever** — index, rewrite query, pool connections, add a replica, denormalize.
4. **Re-measure** — confirm the improvement, watch for regressions (e.g., writes slowing from too many indexes).

**Rule of thumb:** the #1 fix is almost always **indexing for your actual query patterns**.

## 48. Core Database Optimization Techniques

- **Indexing** — composite, covering, partial indexes for query patterns.
- **Connection pooling** — reuse connections; avoid per-request connect overhead.
- **Read replicas** — scale reads horizontally.
- **Denormalization** — precompute/duplicate for hot read paths.
- **Partitioning/sharding** — split large tables/collections.
- **Caching** — cache hot query results (Redis).
- **Query rewriting** — eliminate N+1, avoid `SELECT *`, use joins/batching.

## 49. Where to Apply Database Optimization

- **Slow queries** and endpoints.
- **High load** / growing data volumes.
- **Read-heavy** workloads (replicas).
- **Connection exhaustion** under concurrency.
- **Scaling pain** before throwing hardware at it.

## 50. Database Optimization Limits

- **Too many indexes slow writes** — every write updates every index.
- **Denormalization risks inconsistency** — duplicated data can drift.
- **Replicas add lag** — read-your-writes issues.
- **Optimization can't fix a wrong data model** — sometimes redesign (e.g., access-pattern-driven NoSQL keys) is the real fix.

## 51. Database Optimization Tools and Setup

- **EXPLAIN / EXPLAIN ANALYZE** — inspect query plans (Postgres, MySQL).
- **Slow query log** — find the worst offenders.
- **`pg_stat_statements`** (Postgres) — aggregate query statistics.
- **Connection poolers** — PgBouncer (Postgres), app/ORM pools.
- **APM / monitoring** — Datadog, CloudWatch, slow-query dashboards.

## 52. Measurement and Profiling

- **Baseline first** — record current latency/throughput before changing anything.
- **Profile the query plan** — is it a seq scan (missing index) or index scan?
- **Watch the slow query log** — optimize the top offenders by total time.
- **Re-measure after each change** — confirm the win and catch regressions.

## 53. Database Optimization Best Practices

1. **Index for query patterns**, not for every column.
2. **EXPLAIN before optimizing** — don't guess.
3. **Pool connections** — never connect per request.
4. **Use read replicas** for read-heavy load.
5. **Denormalize selectively** for hot reads only.
6. **Eliminate N+1** — eager-load or batch.
7. **Monitor continuously** — regressions appear as data grows.

## 54. Database Optimization Real-World Examples

### Example 1 — Composite Index
```sql
CREATE INDEX ON orders (user_id, created_at DESC);
-- a query filtering user_id + sorting by created_at now uses one index
```
**Why:** one index serves both the filter and the sort — no separate sort step.

### Example 2 — EXPLAIN Analysis
```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE status = 'paid';
-- "Seq Scan" → missing index; add one → "Index Scan"
```
**Why:** the plan tells you exactly why it's slow.

### Example 3 — Read Replica Routing
**Why:** send reporting/analytics reads to a replica so the primary stays fast for writes.

### Example 4 — Denormalize a Hot Report
**Why:** precompute a `daily_totals` table instead of aggregating millions of rows per request.

## 55. Database Optimization Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Missing indexes | Seq scans, slow queries | Index for query patterns |
| Too many indexes | Slow writes | Index only what's queried |
| No connection pooling | Connection exhaustion | Use a pooler |
| N+1 queries | Endpoint slows with data | Eager-load / batch |
| Ignoring EXPLAIN | Guessing, wrong fixes | Measure first |
| Over-normalization | Costly joins on hot paths | Denormalize selectively |

---

## Shared Foundations

Concepts that recur across **all five topics**:

- **ACID vs BASE** — relational DBs prioritize **ACID** (strong consistency); NoSQL often favors **BASE/eventual consistency** (availability + scale). Choose based on your correctness needs.
- **Data model drives everything** — relational (joins, integrity), document (flexible nesting), key-value (scale + speed). Pick the model matching your **access patterns**.
- **Indexing is the #1 optimization** — across every database, the right index is the highest-leverage fix.
- **Scaling levers** — vertical (bigger machine), read replicas (scale reads), sharding/partitioning (scale writes/data). Know which bottleneck you're solving.
- **Access-pattern-driven design** — especially for NoSQL (DynamoDB, MongoDB): design the schema/keys around how you read, not around the data's shape.
- **Measure, then optimize** — EXPLAIN, slow query logs, and stats before changing anything.

## Quick Reference Card

```
DATABASE PICKER:
  Power + correctness + JSONB?      → PostgreSQL
  Simple read-heavy web app?        → MySQL
  AWS serverless, key-based scale?  → DynamoDB
  Flexible documents, rich queries? → MongoDB

MODELS:
  Relational (PG/MySQL)  → joins, ACID, ad-hoc SQL
  Document  (MongoDB)    → flexible, nested, embed vs reference
  Key-Value (DynamoDB)   → key-based, massive scale, design for access patterns

OPTIMIZATION CHECKLIST (any DB):
  ✓ Index for query patterns (not every column)
  ✓ EXPLAIN before tuning
  ✓ Pool connections
  ✓ Read replicas for read-heavy load
  ✓ Eliminate N+1
  ✓ Denormalize hot reads selectively
  ✓ Monitor slow queries continuously
```

---

*This file covers the core database systems and database optimization. More topics (Redis, Elasticsearch, time-series DBs, database internals) will be added as separate files in this series over time.*
