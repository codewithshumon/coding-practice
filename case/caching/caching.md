# Caching — Complete Guide

> **Series:** Caching Documentation — Part 1
> This file covers the **in-memory caching stores** (Redis, Memcached) and **Caching Strategies** as a cross-cutting discipline. More topics (CDN deep-dive, cache invalidation patterns, distributed caching) will be added as separate files later.

---

## Table of Contents

- [Shared Orientation — Cache Tool vs Cache Strategy](#shared-orientation--cache-tool-vs-cache-strategy)
- **Redis**
  - [1. What Is Redis?](#1-what-is-redis)
  - [2. Redis vs Memcached vs Others](#2-redis-vs-memcached-vs-others)
  - [3. How Redis Works](#3-how-redis-works)
  - [4. Redis Data Structures and Use Cases](#4-redis-data-structures-and-use-cases)
  - [5. Where to Use Redis](#5-where-to-use-redis)
  - [6. Where NOT to Use Redis](#6-where-not-to-use-redis)
  - [7. Installing and Setting Up Redis](#7-installing-and-setting-up-redis)
  - [8. Redis Connection and Authentication](#8-redis-connection-and-authentication)
  - [9. Redis Production Best Practices](#9-redis-production-best-practices)
  - [10. Redis Real-World Examples](#10-redis-real-world-examples)
  - [11. Redis Pitfalls](#11-redis-pitfalls)
- **Memcached**
  - [12. What Is Memcached?](#12-what-is-memcached)
  - [13. Memcached vs Redis](#13-memcached-vs-redis)
  - [14. How Memcached Works](#14-how-memcached-works)
  - [15. Memcached Data Model and Key Features](#15-memcached-data-model-and-key-features)
  - [16. Where to Use Memcached](#16-where-to-use-memcached)
  - [17. Where NOT to Use Memcached](#17-where-not-to-use-memcached)
  - [18. Installing and Setting Up Memcached](#18-installing-and-setting-up-memcached)
  - [19. Memcached Connection and Security](#19-memcached-connection-and-security)
  - [20. Memcached Production Best Practices](#20-memcached-production-best-practices)
  - [21. Memcached Real-World Examples](#21-memcached-real-world-examples)
  - [22. Memcached Pitfalls](#22-memcached-pitfalls)
- **Caching Strategies**
  - [23. What Are Caching Strategies?](#23-what-are-caching-strategies)
  - [24. Caching Strategies vs Just Using Redis](#24-caching-strategies-vs-just-using-redis)
  - [25. How Caching Works](#25-how-caching-works)
  - [26. Caching Levels and Patterns](#26-caching-levels-and-patterns)
  - [27. Where to Apply Caching](#27-where-to-apply-caching)
  - [28. Caching Limits](#28-caching-limits)
  - [29. Caching Implementation and Tools](#29-caching-implementation-and-tools)
  - [30. Cache Invalidation and Measurement](#30-cache-invalidation-and-measurement)
  - [31. Caching Best Practices](#31-caching-best-practices)
  - [32. Caching Real-World Examples](#32-caching-real-world-examples)
  - [33. Caching Pitfalls](#33-caching-pitfalls)
- [Shared Foundations](#shared-foundations)
- [Quick Reference Card](#quick-reference-card)

---

## Shared Orientation — Cache Tool vs Cache Strategy

These three topics split into **two cache tools** and **one discipline** (strategy, which applies to both):

| Topic | Type | One-liner |
|---|---|---|
| **Redis** | Tool | Rich in-memory store — cache + sessions + queues + locks + pub/sub |
| **Memcached** | Tool | Simple, fast, distributed object cache (key-value only) |
| **Caching Strategies** | Discipline | Where/what/how to cache + how to invalidate |

**Decision guide:**
- Need rich data structures, persistence, locks, pub/sub, queues? → **Redis**
- Need a simple, ultra-fast object cache and nothing more? → **Memcached**
- Reducing DB load / speeding reads anywhere? → apply **Caching Strategies** (below)

**The common thread:** Redis and Memcached are the *tools*; caching strategy is *how you use them well* — the hardest part is never storing data, it's **invalidating** it correctly.

---

# Redis

## 1. What Is Redis?

**Redis** is an **in-memory data structure store** used as a database cache, session store, message broker, task queue, and distributed lock manager.

- Extremely fast (in-memory, single-digit microsecond to millisecond ops).
- Far more than a cache — rich data structures enable many use cases.

**One-liner:** a blazing-fast in-memory store that does much more than caching.

## 2. Redis vs Memcached vs Others

| | Redis | Memcached |
|---|---|---|
| Data structures | Rich (hashes, sets, sorted sets, streams) | Strings only |
| Persistence | Optional (RDB/AOF) | None |
| Features | Pub/sub, Lua, locks, queues, replication | Pure cache |
| Threading | Single-threaded event loop | Multithreaded |

**Rule of thumb:** Redis when you need **rich structures or extra features** (locks, queues, pub/sub, persistence); Memcached for **pure, simple object caching**.

## 3. How Redis Works

- **Single-threaded event loop** — extremely fast for small ops (no lock contention).
- **In-memory** with optional **persistence** (RDB snapshots / AOF log).
- **Data structures as values** — not just strings.
- **Replication + Sentinel/Cluster** for high availability and horizontal scale.

**Key point:** everything lives in RAM — speed is the point, but memory is the constraint.

## 4. Redis Data Structures and Use Cases

| Structure | Use case |
|---|---|
| **String** | Cache, counters, session tokens |
| **Hash** | Objects (user profiles) |
| **List** | Simple queues, recent items |
| **Set** | Uniqueness, tags, membership |
| **Sorted Set** | Leaderboards, rate windows, rankings |
| **Stream** | Event/log processing, task queues |
| **Pub/Sub** | Real-time messaging |

## 5. Where to Use Redis

- **Caching** (database/API results).
- **Session stores** (with TTL).
- **Rate limiting** (token bucket via INCR + EXPIRE).
- **Leaderboards** (sorted sets).
- **Task queues** (lists/streams).
- **Distributed locks** (SET NX PX).
- **Pub/sub messaging**.

## 6. Where NOT to Use Redis

- **Primary durable datastore** (unless persistence is carefully configured).
- **Datasets larger than memory**.
- **Complex relational queries** (use a relational DB).

## 7. Installing and Setting Up Redis

```bash
# Docker
docker run -p 6379:6379 redis:7

# CLI basics
redis-cli
> SET user:1 "shumon"
> GET user:1
> SET session:abc "data" EX 3600   # with 1-hour TTL
```

## 8. Redis Connection and Authentication

- **Connection string** — `redis://[:password@]host:6379/0`.
- **AUTH / ACL** (Redis 6+) — per-user permissions; use in production.
- **`requirepass`** — basic password (older style).
- **TLS** — for encrypted connections in production.
- **Connection pooling** — reuse connections via your client library.

**Golden rule:** never expose Redis to the public internet — bind to private interfaces + auth.

## 9. Redis Production Best Practices

1. **Always set TTLs** on cache keys — prevent unbounded memory growth.
2. **Use the right data structure** — don't force everything into strings.
3. **Never use `KEYS` in production** (blocks the server) — use `SCAN`.
4. **Set `maxmemory` + an eviction policy** (e.g., `allkeys-lru`).
5. **Pipeline** batched commands to cut round trips.
6. **Monitor memory, hit rate, and latency**.
7. **Enable AOF** if you need durability beyond a cache.

## 10. Redis Real-World Examples

### Example 1 — Cache-Aside
```python
val = redis.get(key)
if val is None:
    val = db_load(key)              # cache miss → hit DB
    redis.set(key, val, ex=300)     # repopulate with TTL
```
**Why:** the classic caching pattern — DB is hit only on misses.

### Example 2 — Rate Limiter
```python
count = redis.incr(f"rate:{user}")
if count == 1: redis.expire(f"rate:{user}", 60)
if count > 100: reject()            # 100 req/min
```
**Why:** a sliding-window rate limiter in two commands.

### Example 3 — Leaderboard
```python
redis.zadd("scores", {user: points})
top = redis.zrevrange("scores", 0, 9, withscores=True)   # top 10
```
**Why:** sorted sets give O(log n) ranking — perfect for leaderboards.

### Example 4 — Distributed Lock
```python
redis.set("lock:job", "1", nx=True, px=30000)   # acquire if not exists, 30s expiry
```
**Why:** coordinate work across servers without double-processing.

## 11. Redis Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| No TTL on keys | Memory grows until eviction | Always set TTLs |
| Using `KEYS` in prod | Server blocks | Use `SCAN` |
| No `maxmemory`/eviction | OOM crashes | Set memory limit + policy |
| Treating as durable (no AOF) | Data loss on restart | Enable AOF if needed |
| Huge values | Blocks single thread | Keep values small, split big ones |

---

# Memcached

## 12. What Is Memcached?

**Memcached** is a **high-performance, distributed in-memory object caching system** for speeding up dynamic web applications by reducing database load.

- A **simple** key-value cache — nothing more, by design.
- **Multithreaded** and extremely fast for get/set workloads.

**One-liner:** a simple, fast, distributed in-memory key-value cache.

## 13. Memcached vs Redis

| | Memcached | Redis |
|---|---|---|
| Data model | Strings only | Rich structures |
| Persistence | None | Optional |
| Threading | Multithreaded | Single-threaded |
| Features | Pure cache | Cache + locks/queues/pub-sub |
| Best for | Simple high-throughput caching | Richer use cases |

**Rule of thumb:** Memcached for **simple, high-throughput object caching**; Redis when you need structures, persistence, or extra features.

## 14. How Memcached Works

- **In-memory key-value store** — get/set/delete.
- **Multithreaded** — handles many concurrent connections.
- **LRU eviction** — least-recently-used items dropped when memory fills.
- **Client-side sharding** — clients distribute keys across servers (consistent hashing); servers are independent.
- **No persistence** — it's a cache, not a database.

**Key point:** simplicity is the feature — but that means no persistence and no rich structures.

## 15. Memcached Data Model and Key Features

- **Simple key-value** (strings/serialized objects).
- **TTL** per key (expiration).
- **Increment/decrement** for counters.
- **LRU eviction** under memory pressure.
- **Horizontal scaling** via client-side consistent hashing.

## 16. Where to Use Memcached

- **Simple object caching** — DB query results, rendered fragments.
- **Session caching**.
- **Read-heavy dynamic sites** needing to reduce DB load.
- When **simplicity + raw speed** matter more than features.

## 17. Where NOT to Use Memcached

- Need **data structures** (hashes, sets, sorted sets).
- Need **persistence**, **pub/sub**, or **distributed locks** — use Redis.
- As a **primary data store** (no persistence).

## 18. Installing and Setting Up Memcached

```bash
# Docker
docker run -p 11211:11211 memcached

# Basic usage (via a client library or telnet)
set user:1 0 300 6\r\nshumon\r\n     # set with 300s TTL
get user:1
```

## 19. Memcached Connection and Security

- **No built-in auth** (SASL optional) — rely on **network isolation** (private subnet, firewall).
- **Client connection pooling** — reuse connections.
- **Consistent hashing** on the client for sharding across servers.

**Golden rule:** Memcached has essentially no access control — never expose it beyond your private network.

## 20. Memcached Production Best Practices

1. **Set TTLs** on every key.
2. **Use key naming conventions** (namespaced: `user:1:profile`).
3. **Handle cache misses gracefully** — always have a fallback (DB).
4. **Cache read-heavy hot data** only.
5. **Monitor hit rate** — low hit rate means wrong keys/TTLs.
6. **Size memory** appropriately; watch eviction rates.

## 21. Memcached Real-World Examples

### Example 1 — Cache DB Query Results
**Why:** cache the result of an expensive query; on miss, query the DB and repopulate — big DB-load reduction on read-heavy pages.

### Example 2 — Session Caching
**Why:** store session data with a TTL; fast lookups, auto-expiry.

### Example 3 — Cache a Rendered Fragment
**Why:** cache a complex sidebar's HTML; render once per TTL instead of per request.

## 22. Memcached Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| No persistence | Cold cache after restart | Accept it (cache) or warm up |
| No auth exposed | Security breach | Network isolation only |
| Cache stampede on hot key expiry | DB spike | Locking/jittered TTLs |
| Not handling misses | Errors when cache empty | Always fall back to DB |
| Using for structures/locks | Wrong tool | Use Redis |

---

# Caching Strategies

## 23. What Are Caching Strategies?

**Caching strategies** are the discipline of using **multi-level caching** (in-memory, Redis, CDN-edge) to **reduce database load and improve throughput** — deciding *where*, *what*, and *how* to cache, and crucially *how to invalidate*.

**One-liner:** store copies closer to the consumer to avoid recomputation/refetch — and know how to invalidate.

## 24. Caching Strategies vs Just Using Redis

| | Caching Strategy | Just Using a Tool |
|---|---|---|
| Scope | Where/what/how + invalidation | One store, no plan |
| Key question | "How do I keep it fresh?" | "Where do I put this?" |
| Risk addressed | Stale data, stampedes | (none — just storage) |

**Rule of thumb:** Redis/Memcached are *tools*; a caching *strategy* is the plan for using them without serving stale data or causing stampedes.

## 25. How Caching Works

1. On a **cache hit** — serve the stored copy (fast, no DB).
2. On a **cache miss** — compute/fetch from the source, **store a copy** (with a TTL), serve it.
3. On **invalidation/expiry** — drop or refresh the copy.

**Key point:** the hard part isn't storing — it's **knowing when the copy is stale** and invalidating it.

## 26. Caching Levels and Patterns

**Levels (nearest → farthest from the user):**
- **Browser cache** → **CDN-edge** → **Application in-memory** → **Distributed cache (Redis/Memcached)** → **DB query cache**.

**Patterns:**
| Pattern | How it works |
|---|---|
| **Cache-aside (lazy)** | App checks cache → miss → load DB → populate cache |
| **Read-through** | Cache loads from DB automatically on miss |
| **Write-through** | Writes update cache + DB together |
| **Write-behind** | Writes go to cache, flushed to DB async |
| **Refresh-ahead** | Proactively refresh hot keys before expiry |

## 27. Where to Apply Caching

- **Hot read paths** — frequently-read, rarely-changing data.
- **Expensive computations** — reports, aggregations.
- **DB load reduction** — take pressure off the primary.
- **API responses** and **static assets** (CDN).

## 28. Caching Limits

- **Rapidly changing data needing strong consistency** — cache lag shows stale data.
- **Personalized data** — caching per-user is possible but tricky; wrong keys leak data.
- **When invalidation is too complex** — sometimes recomputing is simpler and safer.

## 29. Caching Implementation and Tools

- **Choose the layer** — in-memory (fastest, per-instance), Redis/Memcached (shared), CDN (edge).
- **Set TTLs** — every cached item needs an expiry.
- **Cache-aside** — the safe default pattern.
- **HTTP/CDN caching** — `Cache-Control`, ETags for static/dynamic-at-edge.

## 30. Cache Invalidation and Measurement

- **TTLs** — time-based expiry (the baseline).
- **Explicit invalidation** — delete/update the key when the source changes.
- **Cache versioning / namespacing** — bump a version to invalidate a group.
- **Tag-based invalidation** — invalidate all keys tagged to an entity.
- **Measure hit rate** — the key metric; low hit rate = wrong keys/TTLs.

## 31. Caching Best Practices

1. **Cache at every layer** — but with a clear invalidation plan.
2. **Always pair caching with invalidation** — no "set and forget."
3. **Set TTLs everywhere**.
4. **Version/namespace keys** — makes invalidation manageable.
5. **Prevent cache stampede** — locking, jittered TTLs, refresh-ahead.
6. **Monitor hit rate** — the measure of a healthy cache.
7. **Default to cache-aside** — simple and safe.

## 32. Caching Real-World Examples

### Example 1 — Cache-Aside with Redis
```python
data = redis.get(f"product:{id}")
if not data:
    data = db.get_product(id)
    redis.set(f"product:{id}", data, ex=300)
```
**Why:** DB is hit only on misses; TTL bounds staleness.

### Example 2 — Multi-Level Caching
```
Browser → CDN (static) → App in-memory → Redis → DB
```
**Why:** each layer removes load from the next; most requests never reach the DB.

### Example 3 — Stampede Protection
```python
# on miss, only one worker recomputes; others wait
if redis.set(f"lock:{key}", 1, nx=True, ex=5):
    data = recompute(); redis.set(key, data)
```
**Why:** prevents a thundering herd when a hot key expires.

## 33. Caching Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| No invalidation plan | Stale data served | TTLs + explicit invalidation |
| No TTL | Stale/growing cache | Always set TTLs |
| Cache stampede | DB spike on hot-key expiry | Locking/jitter/refresh-ahead |
| Over-caching | Complexity, hard to reason | Cache only hot/expensive data |
| Caching personalized data wrong | Data leaks across users | Careful per-user key scoping |

---

## Shared Foundations

Concepts that recur across **all three topics**:

- **The core tradeoff: speed vs freshness** — every cache trades up-to-date-ness for speed. The discipline is managing that tradeoff deliberately (TTLs + invalidation).
- **Cache-aside is the default pattern** — check cache, miss → load source → populate. Simple and safe.
- **Invalidation is the hard part** — "there are only two hard things in CS: cache invalidation and naming things." Plan it before you cache.
- **TTLs everywhere** — an unbounded cache is a memory leak and a staleness bug.
- **Stampede / thundering herd** — when a hot key expires, many workers recompute at once; protect with locks, jitter, or refresh-ahead.
- **Hit rate is the key metric** — a cache with a low hit rate is overhead, not optimization.

## Quick Reference Card

```
CACHE TOOL PICKER:
  Rich structures / locks / queues / pub-sub / persistence? → Redis
  Simple, ultra-fast object cache only?                      → Memcached

CACHING STRATEGY (applies to both):
  Default pattern → cache-aside (check cache → miss → load DB → populate)
  Layers → browser → CDN → app in-memory → Redis/Memcached → DB

GOLDEN RULES:
  ✓ Always set TTLs
  ✓ Always pair caching with an invalidation plan
  ✓ Version/namespace keys
  ✓ Protect against stampede (lock/jitter/refresh-ahead)
  ✓ Monitor hit rate — low hit rate = wrong keys/TTLs
  ✓ Redis: no KEYS in prod, set maxmemory + eviction
  ✓ Memcached: network isolation (no built-in auth)
```

---

*This file covers the in-memory caching stores and caching strategies. More topics (CDN deep-dive, cache invalidation patterns, distributed caching) will be added as separate files in this series over time.*
