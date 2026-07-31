# Structures, Architecture & System Design — Complete Guide

> **Series:** Structures & Architecture Documentation — Part 1
> This file holds the **core backend & systems-engineering concepts**: Data Structures & Algorithms, Backend Architecture, Distributed Systems, Scalable APIs, Software Architecture, Performance Tuning, and System Optimization. Related: `case/structures-architecture/design-patterns.md` (MVC, MVP, MVT, MVVM & structural patterns). More topics (Concurrency, Messaging) will be added as separate files later.

---

## Table of Contents

- [Shared Orientation — How These Fit Together](#shared-orientation--how-these-fit-together)
- **Data Structures and Algorithms**
  - [1. What Are Data Structures and Algorithms?](#1-what-are-data-structures-and-algorithms)
  - [2. Core Data Structures and Access Patterns](#2-core-data-structures-and-access-patterns)
  - [3. Algorithmic Patterns and Big-O Complexity](#3-algorithmic-patterns-and-big-o-complexity)
  - [4. Choosing the Right Structure for the Job](#4-choosing-the-right-structure-for-the-job)
  - [5. Where DSA Matters in Production Code](#5-where-dsa-matters-in-production-code)
  - [6. DSA Production Best Practices](#6-dsa-production-best-practices)
  - [7. DSA Real-World Examples](#7-dsa-real-world-examples)
  - [8. DSA Pitfalls and Anti-Patterns](#8-dsa-pitfalls-and-anti-patterns)
- **Backend Architecture**
  - [9. What Is Backend Architecture?](#9-what-is-backend-architecture)
  - [10. Layers and Separation of Concerns](#10-layers-and-separation-of-concerns)
  - [11. Dependency Direction and Modularity](#11-dependency-direction-and-modularity)
  - [12. Common Backend Layering Patterns](#12-common-backend-layering-patterns)
  - [13. When Layering Pays Off](#13-when-layering-pays-off)
  - [14. Backend Architecture Best Practices](#14-backend-architecture-best-practices)
  - [15. Backend Architecture Examples](#15-backend-architecture-examples)
  - [16. Backend Architecture Pitfalls](#16-backend-architecture-pitfalls)
- **Distributed Systems**
  - [17. What Is a Distributed System?](#17-what-is-a-distributed-system)
  - [18. Consensus, Replication, and Partitioning](#18-consensus-replication-and-partitioning)
  - [19. The CAP Theorem and Consistency Models](#19-the-cap-theorem-and-consistency-models)
  - [20. Distributed Design Patterns](#20-distributed-design-patterns)
  - [21. When You Need Distribution](#21-when-you-need-distribution)
  - [22. Distributed Systems Best Practices](#22-distributed-systems-best-practices)
  - [23. Distributed Systems Examples](#23-distributed-systems-examples)
  - [24. Distributed Systems Pitfalls](#24-distributed-systems-pitfalls)
- **Scalable APIs**
  - [25. What Makes an API Scalable?](#25-what-makes-an-api-scalable)
  - [26. Throughput, Latency, and Backpressure](#26-throughput-latency-and-backpressure)
  - [27. Pagination, Rate Limiting, and Caching](#27-pagination-rate-limiting-and-caching)
  - [28. Scalable API Patterns](#28-scalable-api-patterns)
  - [29. When to Engineer for Scale](#29-when-to-engineer-for-scale)
  - [30. Scalable API Best Practices](#30-scalable-api-best-practices)
  - [31. Scalable API Examples](#31-scalable-api-examples)
  - [32. Scalable API Pitfalls](#32-scalable-api-pitfalls)
- **Software Architecture**
  - [33. What Is Software Architecture?](#33-what-is-software-architecture)
  - [34. Clean, Hexagonal, and DDD Concepts](#34-clean-hexagonal-and-ddd-concepts)
  - [35. Domain Isolation and Dependency Inversion](#35-domain-isolation-and-dependency-inversion)
  - [36. Architectural Patterns](#36-architectural-patterns)
  - [37. When to Apply Advanced Architecture](#37-when-to-apply-advanced-architecture)
  - [38. Software Architecture Best Practices](#38-software-architecture-best-practices)
  - [39. Software Architecture Examples](#39-software-architecture-examples)
  - [40. Software Architecture Pitfalls](#40-software-architecture-pitfalls)
- **Performance Tuning**
  - [41. What Is Performance Tuning?](#41-what-is-performance-tuning)
  - [42. Profiling and Finding Hot Paths](#42-profiling-and-finding-hot-paths)
  - [43. ORM, Query, and Template Optimization](#43-orm-query-and-template-optimization)
  - [44. Performance Tuning Techniques](#44-performance-tuning-techniques)
  - [45. When to Tune Performance](#45-when-to-tune-performance)
  - [46. Performance Tuning Best Practices](#46-performance-tuning-best-practices)
  - [47. Performance Tuning Examples](#47-performance-tuning-examples)
  - [48. Performance Tuning Pitfalls](#48-performance-tuning-pitfalls)
- **System Optimization**
  - [49. What Is System Optimization?](#49-what-is-system-optimization)
  - [50. End-to-End Bottleneck Analysis](#50-end-to-end-bottleneck-analysis)
  - [51. Caching Layers and Resource Utilization](#51-caching-layers-and-resource-utilization)
  - [52. System-Wide Optimization Patterns](#52-system-wide-optimization-patterns)
  - [53. When to Optimize the Whole System](#53-when-to-optimize-the-whole-system)
  - [54. System Optimization Best Practices](#54-system-optimization-best-practices)
  - [55. System Optimization Examples](#55-system-optimization-examples)
  - [56. System Optimization Pitfalls](#56-system-optimization-pitfalls)
- [Shared Foundations](#shared-foundations)
- [Quick Reference Card](#quick-reference-card)

---

## Shared Orientation — How These Fit Together

These seven topics are the foundation of backend & systems engineering. They overlap and reinforce each other:

| Topic | Core question | One-liner |
|---|---|---|
| **DSA** | How do I organize & process data efficiently? | Right structure + right algorithm = performance |
| **Backend Architecture** | How do I structure my server-side code? | Clear layers so change stays localized |
| **Distributed Systems** | How do many machines cooperate as one? | Trade consistency, availability, latency |
| **Scalable APIs** | How do endpoints survive growth & spikes? | Stay fast and fair under heavy load |
| **Software Architecture** | What's the big-picture code organization? | Isolate the domain; invert dependencies |
| **Performance Tuning** | How do I fix runtime bottlenecks? | Measure, then optimize the hot path |
| **System Optimization** | How do I optimize the whole stack? | Fix the system-wide bottleneck, not one layer |

**Rule of thumb:** **DSA** gives you efficient primitives → **Backend/Software Architecture** organizes them into maintainable systems → **Distributed Systems** & **Scalable APIs** let them grow → **Performance Tuning** & **System Optimization** keep them fast.

---

# Data Structures and Algorithms

## 1. What Are Data Structures and Algorithms?

**Data Structures** organize data for efficient access; **Algorithms** are step-by-step procedures to process it. Together they decide how fast and how much memory your code uses.

- The *same* problem can be O(n²) or O(log n) depending on your choices — that's the difference between slow and scalable.
- In backend code, DSA shows up in hot paths: lookups, ranking, dedup, scheduling, search.

**One-liner:** choosing the right structure + algorithm is the foundation of performant, scalable code.

## 2. Core Data Structures and Access Patterns

| Structure | Best for | Access |
|---|---|---|
| **Array / List** | Ordered, indexed data | O(1) index, O(n) search |
| **Hash Map / Dict** | Key→value lookup, dedup | O(1) avg lookup/insert |
| **Set** | Uniqueness, membership | O(1) avg |
| **Stack** | LIFO — undo, parsing | O(1) push/pop |
| **Queue** | FIFO — task order, BFS | O(1) enqueue/dequeue |
| **Heap / Priority Queue** | Top-K, scheduling | O(log n) insert/peek-min |
| **Tree (BST / Trie)** | Ordered data, autocomplete | O(log n) / O(k) |
| **Graph** | Relationships, networks | BFS/DFS O(V+E) |

**Key point:** match the structure to the **access pattern**, not the data shape.

## 3. Algorithmic Patterns and Big-O Complexity

- **Big-O** = how cost grows with input size (time & space). Know the common classes: O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ).
- **Reusable patterns:** two-pointer, sliding window, hash-map lookup, prefix sums, recursion + memoization, BFS/DFS, divide & conquer, greedy, dynamic programming.

**Rule of thumb:** most backend bottlenecks collapse to "you used an O(n) structure where O(1) or O(log n) existed."

## 4. Choosing the Right Structure for the Job

1. **Identify the access pattern** — lookup? insert? ordered iteration? top-K?
2. **Pick the structure matching it** — frequent key lookups → hash map; ordered range → tree; min/max repeatedly → heap.
3. **Stay within a complexity budget** — if a request must be <100ms at 1M items, O(n²) is out.
4. **Measure** — theory says what's possible; profiling says what's real.

## 5. Where DSA Matters in Production Code

- **Hot paths** — every-request lookups, validation, routing.
- **Large datasets** — feeds, logs, analytics where O(n²) is fatal.
- **Real-time queries** — search, autocomplete, ranking, recommendations.
- **Dedup & membership** — "have I seen this idempotency key before?"
- **Scheduling / ordering** — job queues, priority processing.

## 6. DSA Production Best Practices

1. **Know your access pattern first** — structure follows access, not the other way.
2. **Prefer O(1) lookups** (hash maps/sets) in hot paths.
3. **Avoid O(n²) in loops over growing data** — it works at 100 items, dies at 100k.
4. **Precompute & cache** expensive results instead of recomputing.
5. **Profile before optimizing** — fix the real bottleneck, not guessed ones.
6. **Mind space complexity** — an O(1)-time trick that eats all RAM isn't a win.
7. **Use bulk/batch operations** — one O(n) pass beats n O(1) round trips.

## 7. DSA Real-World Examples

### Example 1 — LRU Cache (hash map + doubly linked list)
```python
from collections import OrderedDict
cache = OrderedDict()           # O(1) get/put + move-to-end
cache["k"] = "v"; cache.move_to_end("k")
cache.popitem(last=False)       # evict least-recently-used
```
**Why:** O(1) get/put/evict — the backbone of in-memory caches.

### Example 2 — Autocomplete (trie)
**Why:** a trie shares prefixes, so "find all words starting with `ca`" is O(k) regardless of dictionary size.

### Example 3 — Top-K Trending (min-heap)
```python
import heapq
top = []
for item in stream:
    heapq.heappush(top, item)
    if len(top) > K: heapq.heappop(top)   # keep K largest
```
**Why:** O(n log K) instead of sorting everything O(n log n).

### Example 4 — Dedup / Idempotency (set)
```python
seen = set()
if tx_id in seen: return "duplicate"
seen.add(tx_id)
```
**Why:** O(1) duplicate detection — critical for exactly-once processing.

### Example 5 — Shortest Path (BFS / Dijkstra)
**Why:** BFS gives fewest hops in unweighted graphs; Dijkstra handles weighted — routing, dependency resolution.

### Example 6 — Job Scheduler (priority queue)
**Why:** always pop the highest-priority job in O(log n) instead of scanning the list O(n).

## 8. DSA Pitfalls and Anti-Patterns

| Pitfall | Symptom | Fix |
|---|---|---|
| Premature optimization | Wasted time on cold paths | Profile first |
| Wrong structure for access | Slow lookups in hot path | Match structure to access pattern |
| Ignoring space complexity | OOM crashes | Track memory, not just time |
| Nested loops on growing data | Falls over at scale | Replace O(n²) with hash/map |
| Off-by-one / boundary bugs | Silent wrong results | Test edge cases explicitly |
| Over-engineering | Complex code for small data | Keep it simple until profiling says otherwise |

---

# Backend Architecture

## 9. What Is Backend Architecture?

**Backend Architecture** is how you structure server-side code into clear layers and responsibilities so the system stays **maintainable** as it grows.

- Good architecture localizes change: a UI tweak doesn't touch the DB; a schema change doesn't rewrite business rules.
- It's about **boundaries and dependencies**, not frameworks.

**One-liner:** organize code so each change ripples as little as possible.

## 10. Layers and Separation of Concerns

| Layer | Responsibility |
|---|---|
| **Presentation / API** | HTTP, input parsing, response formatting |
| **Application / Service** | Use-case orchestration, workflows |
| **Domain** | Core business rules & invariants |
| **Data / Persistence** | DB, ORM, external I/O |

**Separation of Concerns (SoC):** each module has one reason to change. Business logic never lives in a controller or a SQL query.

## 11. Dependency Direction and Modularity

- **Dependencies point inward** — outer layers (HTTP, DB) depend on the domain; the domain depends on nothing.
- **Depend on abstractions, not details** — a `PaymentGateway` interface, not a concrete SDK class.
- **Modularity** = cohesive modules with stable, narrow interfaces.

**Key point:** the domain should be runnable/testable without a web server or database.

## 12. Common Backend Layering Patterns

- **Layered / n-tier** — Controller → Service → Repository (simple, ubiquitous).
- **MVC** — Model/View/Controller (web apps).
- **Service + Repository** — business logic in services, data access in repositories.
- **Module boundaries** — feature-based packages with explicit public APIs.
- **API contracts** — versioned interfaces between services.

## 13. When Layering Pays Off

- Any **non-trivial backend** — value grows with code size and team size.
- **Multiple consumers** — web + mobile + internal tools sharing one domain.
- **Long-lived systems** — where frameworks/DBs will eventually be swapped.
- **Teams** — clear boundaries let people work in parallel without conflicts.

## 14. Backend Architecture Best Practices

1. **One responsibility per module** — single reason to change.
2. **Depend on abstractions** — interfaces, not concrete classes.
3. **Keep logic out of controllers & SQL** — it belongs in the domain/service.
4. **Isolate third-party code** behind your own interface.
5. **Version your APIs** — protect consumers from breaking changes.
6. **Keep the domain framework-free** — testable in isolation.
7. **Don't over-layer trivial apps** — match structure to complexity.

## 15. Backend Architecture Examples

### Example 1 — Classic Layering
```
Controller (HTTP) → Service (use case) → Repository (DB)
```
**Why:** each layer is independently testable and swappable.

### Example 2 — Third-Party Isolation
```python
class PaymentGateway(Protocol):  # your interface
    def charge(self, amount): ...

class StripeAdapter(PaymentGateway): ...  # concrete detail behind it
```
**Why:** swap Stripe→PayPal without touching business logic.

### Example 3 — Domain Independent of ORM
**Why:** domain services take plain objects; the repository maps them to ORM rows — the domain never imports the ORM.

## 16. Backend Architecture Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Anemic domain model | Logic leaks into controllers/services | Put behavior in the domain |
| Fat controllers | Business rules in HTTP handlers | Move to services/domain |
| DB everywhere | ORM calls scattered, untestable | Centralize in repositories |
| Leaky abstractions | Domain imports framework | Invert dependencies |
| Over-engineering | Excess layers for a CRUD app | Match structure to real complexity |

---

# Distributed Systems

## 17. What Is a Distributed System?

A **Distributed System** is multiple networked nodes cooperating as one system to share load, data, or availability.

- You distribute when one machine can't handle the **load, data size, or availability** requirements alone.
- The defining reality: **networks fail, nodes crash, clocks skew** — design assumes partial failure.

**One-liner:** many machines working together, trading off consistency, availability, and latency.

## 18. Consensus, Replication, and Partitioning

| Concept | Meaning |
|---|---|
| **Replication** | Copy data across nodes for availability/durability |
| **Partitioning / Sharding** | Split data across nodes for scale |
| **Consensus** | Nodes agree on a value/leader (Raft, Paxos) |
| **Quorum** | Majority agreement for reads/writes |
| **Consistent hashing** | Even, low-reshuffle data distribution |
| **Idempotency** | Safe to retry an operation without side effects |

## 19. The CAP Theorem and Consistency Models

- **CAP:** during a network partition you choose **Consistency** or **Availability** — not both.
- **Consistency spectrum:** strong → read-your-writes → eventual.
- Most large systems choose **AP + eventual consistency** (DynamoDB, Cassandra); relational DBs lean **CP**.

**Rule of thumb:** embrace eventual consistency where you can; pay for strong consistency only where correctness demands it (payments, inventory).

## 20. Distributed Design Patterns

- **Leader election** — one node coordinates writes (Raft).
- **Quorum reads/writes** — R + W > N guarantees strong-ish consistency.
- **Consistent hashing** — stable shard assignment.
- **Saga** — coordinated multi-service transactions via compensating actions.
- **Circuit breaker / bulkhead** — isolate failures, stop cascading.
- **Retry + idempotency key** — safe retries without duplicates.

## 21. When You Need Distribution

- **Load** beyond one machine's CPU/RAM.
- **Data size** beyond one DB/storage node.
- **Availability** — survive a node/zone/region failure.
- **Geography** — serve users from nearby regions.
- **Microservices** — inherently distributed by design.

## 22. Distributed Systems Best Practices

1. **Make operations idempotent** — safe to retry (idempotency keys).
2. **Design for partial failure** — assume any node/call can die.
3. **Prefer eventual consistency** — reserve strong consistency for true needs.
4. **Bound retries with backoff + jitter** — avoid thundering herds.
5. **Isolate failures** — circuit breakers, bulkheads, timeouts.
6. **Monitor tail latency** (p99), not just averages.
7. **Handle clocks carefully** — don't rely on synchronized time for correctness.

## 23. Distributed Systems Examples

### Example 1 — Leader-Follower Replication
**Why:** writes go to the leader; followers replicate — reads scale across followers, durability via copies.

### Example 2 — Consistent Hashing for Sharding
**Why:** adding/removing a node moves only ~1/N of keys, not the whole dataset.

### Example 3 — Saga for Distributed Transactions
```
Order → ReserveStock → Charge → Confirm   (each step has a compensating undo)
```
**Why:** avoids locking across services (unlike 2PC); rolls back via compensations.

### Example 4 — Idempotency Key in Payments
**Why:** client sends one `Idempotency-Key`; duplicate retries return the same result — no double charges.

### Example 5 — DynamoDB (AP, tunable consistency)
**Why:** choose consistency per read — fast/scalable by default, strong when needed.

## 24. Distributed Systems Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Assuming network is reliable | Silent failures/timeouts | Timeouts, retries, circuit breakers |
| Ignoring clock skew | Ordering bugs | Use logical clocks/sequence numbers |
| Distributed tx everywhere | Deadlocks, latency | Use sagas + eventual consistency |
| Retries without idempotency | Duplicate side effects | Idempotency keys |
| Misunderstanding CAP | Wrong consistency promises | Choose deliberately per use case |

---

# Scalable APIs

## 25. What Makes an API Scalable?

A **Scalable API** stays fast and fair under growing load and traffic spikes.

- Scalability = the ability to handle more requests by **adding resources** (horizontal) without redesign.
- Keys: **statelessness, pagination, rate limiting, caching, and offloading heavy work.**

**One-liner:** design endpoints that survive growth and spikes.

## 26. Throughput, Latency, and Backpressure

- **Throughput** = requests/sec handled; **latency** = time per request. They often trade off.
- **Backpressure** = signaling upstream to slow down when you can't keep up (queues, 429s).
- **Horizontal scaling** = add more instances; only works if servers are **stateless**.

## 27. Pagination, Rate Limiting, and Caching

| Technique | Purpose |
|---|---|
| **Pagination** | Return chunks, not whole tables (cursor > offset for large data) |
| **Rate limiting** | Protect resources from abuse/overload (token bucket) |
| **Caching** | Serve hot data from memory/CDN, skip the DB |
| **Idempotency** | Safe retries on writes |
| **Async offloading** | Push slow work to queues, respond fast |

## 28. Scalable API Patterns

- **Cursor pagination** — stable & fast on large tables (vs slow offset).
- **Token-bucket rate limiting** — per client/key, in Redis.
- **Multi-level caching** — CDN → app → Redis → DB.
- **Read replicas** — scale reads separately from writes.
- **Idempotency-Key header** — safe retries for writes.
- **Async via message queues** — absorb write spikes (SQS/Kafka).

## 29. When to Engineer for Scale

- Expected **growth** in users/data.
- **Spiky traffic** (launches, sales, events).
- **Shared finite resources** (DB, third-party APIs with quotas).
- **Cost targets** — efficient APIs are cheaper to run.

## 30. Scalable API Best Practices

1. **Paginate every list endpoint** — never return unbounded collections.
2. **Rate-limit per client/key** — protect the backend from abuse.
3. **Cache aggressively** — with explicit invalidation.
4. **Keep servers stateless** — store sessions in Redis, not in-process.
5. **Use idempotency keys** for writes.
6. **Offload heavy work to queues** — keep request paths fast.
7. **Version the API** — evolve without breaking clients.
8. **Watch for N+1 queries** — the #1 silent API killer.

## 31. Scalable API Examples

### Example 1 — Cursor Pagination on a Feed
```
GET /feed?cursor=abc&limit=20   → returns next cursor
```
**Why:** O(limit) regardless of dataset size; offset pagination degrades on big tables.

### Example 2 — Redis Token-Bucket Rate Limiter
**Why:** shared across all instances — consistent limits in a scaled-out fleet.

### Example 3 — Cache Reads Behind a Key
```python
data = cache.get(key) or db_load(key); cache.set(key, data, ttl=60)
```
**Why:** DB hit only on cache miss — 100x fewer queries for hot data.

### Example 4 — SQS to Absorb Write Spikes
**Why:** API enqueues and returns 202 instantly; workers process at their own pace.

### Example 5 — Idempotency-Key on Payments
**Why:** duplicate client retries never double-charge.

## 32. Scalable API Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Offset pagination on big tables | Slow, gets worse over time | Cursor pagination |
| No rate limiting | Abuse, DoS, runaway costs | Token-bucket per client |
| Over-caching without invalidation | Stale/wrong data | Cache + clear invalidation rules |
| Stateful servers | Can't scale horizontally | Move state to Redis/DB |
| N+1 queries | Endpoint slows with data size | Eager-load (select_related) |

---

# Software Architecture

## 33. What Is Software Architecture?

**Software Architecture** is the **big-picture organization** of a system — its major components, their boundaries, dependencies, and interaction patterns.

- If backend architecture is "how I layer one service," software architecture is "how the whole system is shaped."
- Goal: robust, scalable, **maintainable** systems that survive changing requirements.

**One-liner:** the high-level structure — boundaries, dependencies, and flow.

## 34. Clean, Hexagonal, and DDD Concepts

| Approach | Core idea |
|---|---|
| **Clean Architecture** | Dependencies point inward; domain at center, frameworks outside |
| **Hexagonal (Ports & Adapters)** | Core logic talks to "ports"; DB/UI/HTTP are swappable "adapters" |
| **Domain-Driven Design (DDD)** | Model the business domain in code — entities, aggregates, bounded contexts |
| **Event-Driven Architecture** | Services communicate via events, not direct calls |

## 35. Domain Isolation and Dependency Inversion

- **Domain at the center** — no imports of frameworks, DB, or HTTP.
- **Dependency Inversion** — high-level policy depends on interfaces; low-level details implement them.
- **Testability** — the domain runs in unit tests with zero infrastructure.

**Key point:** frameworks, databases, and delivery mechanisms are **details** that should be pluggable.

## 36. Architectural Patterns

- **Clean / Hexagonal** — concentric layers, inverted dependencies.
- **DDD** — bounded contexts (split a big domain into cohesive parts), aggregates (consistency boundaries).
- **Event-Driven** — events as the integration mechanism between services.
- **CQRS** — separate read models from write models for independent scaling.
- **Microservices / Monolith** — deployment-unit choice, orthogonal to internal architecture.

## 37. When to Apply Advanced Architecture

- **Complex business domains** — where a rich domain model pays off.
- **Long-lived systems** — where swap-ability and testability matter.
- **Large teams** — where clear boundaries enable parallel work.
- **Multiple delivery channels** — web, mobile, CLI, jobs sharing one core.

**Caution:** don't apply Clean/DDD to a simple CRUD app — it's overhead with no payoff.

## 38. Software Architecture Best Practices

1. **Domain at the center, framework-free** — runnable in pure unit tests.
2. **Explicit bounded contexts** — split big domains along business seams.
3. **Communicate via stable contracts/events** — version them.
4. **Invert dependencies** — depend on interfaces, not concretions.
5. **Favor composition** over deep inheritance hierarchies.
6. **Keep decisions reversible** — delay hard-to-undo choices.
7. **Match architecture to complexity** — not every app needs DDD.

## 39. Software Architecture Examples

### Example 1 — Hexagonal Core with Swappable Adapters
```
[ HTTP adapter ] ─┐
[ DB adapter ]   ─┼─► ( Application Core / Domain ) ◄─ ports
[ CLI adapter ]  ─┘
```
**Why:** add a GraphQL adapter or swap Postgres→Mongo without touching the domain.

### Example 2 — DDD Aggregate Enforcing Invariants
**Why:** an `Order` aggregate won't let you add items after it's shipped — the rule lives with the data.

### Example 3 — Event-Driven Order Flow
```
OrderService → publishes OrderCreated → Inventory + Billing react independently
```
**Why:** services are decoupled; add a new reactor (e.g., Analytics) without touching existing services.

### Example 4 — CQRS Split
**Why:** optimize reads (denormalized read models) and writes (normalized domain) independently.

## 40. Software Architecture Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Over-abstracting simple systems | Needless complexity | Match architecture to real complexity |
| Anemic domain | Logic scattered, no invariants | Put behavior in domain entities |
| Leaky abstractions | Domain imports framework | Enforce dependency inversion |
| Events without schema/versioning | Breaking consumers | Versioned event contracts |
| DDD cargo-culting | Bounded contexts everywhere | Split only along real business seams |

---

# Performance Tuning

## 41. What Is Performance Tuning?

**Performance Tuning** is finding and fixing bottlenecks in **runtime code** — typically Python, ORM queries, templates, and server config.

- It's **local** optimization within a component (vs system-wide optimization).
- The golden rule: **measure first, then optimize the actual bottleneck.**

**One-liner:** profile, find the hot path, optimize it — never guess.

## 42. Profiling and Finding Hot Paths

- **Profile** before touching code — cProfile, py-spy, Django Debug Toolbar, APM (Datadog/New Relic).
- Identify the **hot path** — the small % of code taking most of the time (Amdahl's law).
- Re-measure after every change — confirm the win and catch regressions.

**Key point:** "premature optimization is the root of all evil" — optimize what the profiler shows, not what feels slow.

## 43. ORM, Query, and Template Optimization

- **N+1 queries** — the #1 backend killer; fix with `select_related`/`prefetch_related`.
- **Missing indexes** — add indexes matching your query/filter patterns.
- **Template rendering** — cache expensive fragments; avoid heavy logic in templates.
- **Query volume** — `EXPLAIN` slow queries; avoid fetching columns you don't need.

## 44. Performance Tuning Techniques

- Query profiling + `EXPLAIN`.
- Eager loading (eliminate N+1).
- DB indexing for query patterns.
- Caching (query results, rendered fragments).
- Batching (`bulk_create`, `BatchWriteItem`).
- Moving heavy work to background jobs.

## 45. When to Tune Performance

- **Slow endpoints** missing latency targets.
- **High CPU/memory** usage under load.
- **Slow page loads** hurting UX/SEO.
- **Scaling pain** — throwing hardware at an unoptimized codebase.

## 46. Performance Tuning Best Practices

1. **Measure before and after** — no blind optimization.
2. **Fix N+1 queries first** — usually the biggest win.
3. **Index for your query patterns** — not for every column.
4. **Cache stable/expensive results** — with clear invalidation.
5. **Paginate heavy queries** — never load unbounded rows.
6. **Minimize work in hot loops** — hoist invariants, avoid allocations.
7. **Don't micro-optimize cold paths** — focus where time is actually spent.

## 47. Performance Tuning Examples

### Example 1 — Fixing N+1 with prefetch_related
```python
# Bad: 1 + N queries
for o in Order.objects.all(): print(o.items.count())
# Good: 2 queries total
Order.objects.prefetch_related("items")
```
**Why:** turns 1,001 queries into 2 — massive speedup on lists.

### Example 2 — Adding a Composite Index
**Why:** a query filtering `(user_id, created_at)` drops from a full table scan to an index lookup.

### Example 3 — Caching a Rendered Fragment
**Why:** a complex sidebar rendered once per TTL instead of per request.

### Example 4 — bulk_create vs Per-Row Save
**Why:** one round trip instead of N — dramatically faster inserts.

### Example 5 — Moving a Report to a Background Job
**Why:** a 30-second report generation no longer blocks the API; user gets it async.

## 48. Performance Tuning Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Optimizing without profiling | Effort on cold paths | Profile, find the hot path |
| Micro-optimizing | Low impact, brittle code | Focus on dominant cost |
| Stale caches | Wrong data shown | Pair caching with invalidation |
| Indexes that slow writes | Inserts/updates slow | Index for reads, audit write cost |
| Ignoring the DB layer | App tweaks can't help | Start with queries/indexes |

---

# System Optimization

## 49. What Is System Optimization?

**System Optimization** is **end-to-end** tuning across the whole stack — architecture, databases, caching, APIs, and resources — not just one component.

- It's the **system-wide** counterpart to local performance tuning.
- Guided by **Amdahl's law**: optimize what dominates the total time.

**One-liner:** optimize the system as a whole — fix the dominant cross-layer bottleneck.

## 50. End-to-End Bottleneck Analysis

1. **Trace a request end-to-end** — client → CDN → app → cache → DB → external APIs.
2. **Find the dominant cost** — where is most wall-clock time spent?
3. **Apply Amdahl's law** — speeding the dominant stage gives the biggest system gain.
4. **Consider second-order effects** — caching reads may overload writes; scaling app may expose DB limits.

## 51. Caching Layers and Resource Utilization

- **Caching tiers:** CDN (static) → app memory → Redis → DB. Each tier removes load from the next.
- **Resource utilization:** CPU, memory, disk I/O, network — optimize the **saturated** one.
- **Right-sizing:** match instance/storage class to actual load; over-provisioning wastes money.

## 52. System-Wide Optimization Patterns

- Multi-tier caching with clear invalidation.
- Query & index tuning at the DB layer.
- Connection / session pooling.
- Read replicas for read-heavy loads.
- Async offloading (queues) for write-heavy paths.
- CDN for static + cacheable dynamic content.
- Horizontal vs vertical scaling chosen per bottleneck.

## 53. When to Optimize the Whole System

- **Local optimizations aren't enough** — you've tuned the code, it's still slow.
- **Cost reduction** — cloud bills too high for the traffic.
- **Latency/throughput SLOs** not being met.
- **Scale events** — Black Friday, viral launches, data migrations.

## 54. System Optimization Best Practices

1. **Optimize the dominant bottleneck first** — biggest system-level gain.
2. **Cache at every layer** — with explicit invalidation rules.
3. **Reduce round trips** — batching, joins, fewer external calls.
4. **Right-size resources** — avoid paying for idle capacity.
5. **Set latency budgets/SLOs** — know your targets before tuning.
6. **Continuously monitor** — regressions appear as load shifts.
7. **Apply backpressure/load shedding** — degrade gracefully, don't collapse.
8. **Fix the algorithm/architecture before adding hardware** — throwing servers at O(n²) is expensive.

## 55. System Optimization Examples

### Example 1 — Sync DB Writes → Queued Async
**Why:** request returns instantly; DB write load is smoothed by queue consumers.

### Example 2 — Redis Cache Tier in Front of Postgres
**Why:** hot reads never hit the DB — DB CPU drops, throughput rises.

### Example 3 — CDN for Static + Cacheable Dynamic
**Why:** users get content from a nearby edge; your origin handles far less traffic.

### Example 4 — Read Replicas for Read-Heavy Load
**Why:** scale reads across replicas; writes stay on the primary.

### Example 5 — Denormalize a Hot Read Path
**Why:** a precomputed/joined read model turns a 10-query report into 1 query.

## 56. System Optimization Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Optimizing the wrong layer | Little system-level gain | Trace end-to-end, find dominant cost |
| Local win, system loss | One part faster, whole slower | Check second-order effects |
| Over-caching complexity | Stale data, hard to reason about | Clear tiers + invalidation rules |
| Ignoring downstream effects | New bottleneck appears | Monitor after every change |
| Scaling hardware first | Expensive, temporary relief | Fix algorithm/architecture first |

---

## Shared Foundations

Concepts that recur across **all seven topics**:

- **Tradeoffs are unavoidable** — CAP (consistency vs availability), latency vs throughput, space vs time, consistency vs performance. Make them **deliberately**, not accidentally.
- **Measure before optimizing** — profiling is non-negotiable; intuition is frequently wrong.
- **Caching is cross-cutting** — appears in DSA, Scalable APIs, Performance Tuning, and System Optimization. Always pair with **invalidation**.
- **Idempotency & retries** — the bedrock of reliable distributed & API behavior.
- **Scalability levers** — statelessness (scale out), caching (less work), partitioning (split data), async (smooth load).
- **Complexity is a cost** — DDD/Clean/microservices have overhead; apply them where the payoff exceeds the cost.

---

## Quick Reference Card

```
THE STACK:
  DSA          → efficient primitives (right structure + algorithm)
  Architecture → organize code (layers, domain isolation, inverted deps)
  Distributed  → many machines (CAP, replication, idempotency)
  Scalable API → survive growth (paginate, rate-limit, cache, go stateless)
  Perf Tuning  → fix local bottlenecks (profile → N+1 → index → cache)
  System Opt   → fix the whole stack (Amdahl: optimize the dominant stage)

GOLDEN RULES (all topics):
  ✓ Measure first, never guess
  ✓ Match structure to access pattern (DSA)
  ✓ One responsibility per module; invert dependencies (Architecture)
  ✓ Assume failure; make ops idempotent (Distributed)
  ✓ Paginate + rate-limit + cache; stay stateless (Scalable API)
  ✓ Profile → fix hot path → re-measure (Performance)
  ✓ Optimize the dominant end-to-end bottleneck (System Opt)

TRADEOFFS TO CHOOSE DELIBERATELY:
  CAP: consistency vs availability
  latency vs throughput
  space vs time
  strong vs eventual consistency
  simplicity vs flexibility
```

---

*This file covers the seven core backend & systems-engineering concepts. More topics (Design Patterns, Concurrency, Messaging, Caching Deep-Dive) will be added as separate files in this series over time.*
