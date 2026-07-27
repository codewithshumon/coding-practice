# Architecture Patterns — Complete Guide

> **Series:** Structures & Architecture Documentation — Part 2
> This file goes deep on **four applied architecture patterns**: Microservices, Event-Driven Architectures, Multi-Tenant SaaS, and Serverless Architectures. Part 1 (`backend-systems.md`) covered the fundamentals (DSA, Backend/Software Architecture, Distributed Systems, etc.); this file expands the patterns that build on them. More topics (CQRS, Hexagonal deep-dive, Messaging) will be added later.

---

## Table of Contents

- [Shared Orientation — How These Four Compose](#shared-orientation--how-these-four-compose)
- **Microservices**
  - [1. What Are Microservices?](#1-what-are-microservices)
  - [2. Microservices Core Concepts](#2-microservices-core-concepts)
  - [3. How to Think About Microservices](#3-how-to-think-about-microservices)
  - [4. Microservices Patterns](#4-microservices-patterns)
  - [5. When to Use Microservices](#5-when-to-use-microservices)
  - [6. Microservices Best Practices](#6-microservices-best-practices)
  - [7. Microservices Examples](#7-microservices-examples)
  - [8. Microservices Pitfalls](#8-microservices-pitfalls)
- **Event-Driven Architectures**
  - [9. What Is Event-Driven Architecture?](#9-what-is-event-driven-architecture)
  - [10. Event-Driven Core Concepts](#10-event-driven-core-concepts)
  - [11. How Event-Driven Systems Work](#11-how-event-driven-systems-work)
  - [12. Event-Driven Patterns](#12-event-driven-patterns)
  - [13. When to Use Event-Driven Architecture](#13-when-to-use-event-driven-architecture)
  - [14. Event-Driven Best Practices](#14-event-driven-best-practices)
  - [15. Event-Driven Examples](#15-event-driven-examples)
  - [16. Event-Driven Pitfalls](#16-event-driven-pitfalls)
- **Multi-Tenant SaaS**
  - [17. What Is Multi-Tenant SaaS?](#17-what-is-multi-tenant-saas)
  - [18. Tenant Isolation Models](#18-tenant-isolation-models)
  - [19. How Multi-Tenancy Works](#19-how-multi-tenancy-works)
  - [20. Multi-Tenant Patterns](#20-multi-tenant-patterns)
  - [21. When to Build Multi-Tenant SaaS](#21-when-to-build-multi-tenant-saas)
  - [22. Multi-Tenant Best Practices](#22-multi-tenant-best-practices)
  - [23. Multi-Tenant Examples](#23-multi-tenant-examples)
  - [24. Multi-Tenant Pitfalls](#24-multi-tenant-pitfalls)
- **Serverless Architectures**
  - [25. What Is Serverless Architecture?](#25-what-is-serverless-architecture)
  - [26. Serverless Core Concepts](#26-serverless-core-concepts)
  - [27. How Serverless Works](#27-how-serverless-works)
  - [28. Serverless Patterns](#28-serverless-patterns)
  - [29. When to Use Serverless](#29-when-to-use-serverless)
  - [30. Serverless Best Practices](#30-serverless-best-practices)
  - [31. Serverless Examples](#31-serverless-examples)
  - [32. Serverless Pitfalls](#32-serverless-pitfalls)
- [Shared Foundations](#shared-foundations)
- [Quick Reference Card](#quick-reference-card)

---

## Shared Orientation — How These Four Compose

These patterns answer four different structural questions, and in modern systems they're usually **combined**:

| Pattern | Question it answers | One-liner |
|---|---|---|
| **Microservices** | How do I split the system into services? | Many small, independent services, not one monolith |
| **Event-Driven** | How do those services communicate? | React to events, don't call each other directly |
| **Multi-Tenant SaaS** | How do I serve many customers? | One app, many tenants, isolated data |
| **Serverless** | How do I run/scale the compute? | Functions the cloud runs, pay per use |

**Rule of thumb:** they're orthogonal axes, not alternatives. A typical cloud SaaS is a **serverless**, **event-driven**, **multi-tenant** system built from **microservices**. Pick each axis deliberately based on your scale, team, and domain.

**The common thread:** all four increase **loose coupling** and **scalability** — at the cost of operational complexity.

---

# Microservices

## 1. What Are Microservices?

**Microservices** decompose an application into small, **loosely coupled, independently deployable services**, each owning its data and communicating over lightweight protocols (HTTP, gRPC, or events).

- Each service is built around a **business capability** and can be deployed/scaled independently.
- Contrast with a **monolith**, where everything runs in one deployable unit.

**One-liner:** build a system as many small, autonomous services instead of one big monolith.

## 2. Microservices Core Concepts

| Concept | Role |
|---|---|
| **Service autonomy** | Each service owns its logic + data + lifecycle |
| **Bounded context** | Service boundary aligned to a business domain (DDD) |
| **Database-per-service** | No shared DB; data ownership is private |
| **Inter-service comms** | REST, gRPC (sync), or events (async) |
| **API Gateway** | Single entry point: routing, auth, aggregation |
| **Service discovery** | Services find each other dynamically |

**Key point:** independence is the defining trait — deploy, scale, and change a service without touching others.

## 3. How to Think About Microservices

- **Split along business capability boundaries** (use DDD bounded contexts), not technical layers.
- Each service **owns its data** — no shared databases, or you've just built a distributed monolith.
- Prefer **asynchronous** communication (events/queues) over chatty synchronous calls.
- Accept **eventual consistency** across services; reserve strong consistency for within a service.

**Rule of thumb:** if two services must change together to ship a feature, they're probably one service.

## 4. Microservices Patterns

- **API Gateway** — entry point, routing, auth, rate limiting.
- **Database-per-service** — private data, integration via APIs/events.
- **Saga** — distributed transactions via compensating actions.
- **Circuit breaker / bulkhead** — isolate failures, stop cascading.
- **BFF (Backend-for-Frontend)** — a service per client type (web, mobile).
- **Service mesh** — handle comms, retries, observability cross-cuttingly.

## 5. When to Use Microservices

- **Large/complex domains** splittable along clear business lines.
- **Multiple teams** that need to work/deploy independently.
- Need **independent scaling** of different parts (e.g., search vs. billing).
- Organizational maturity to handle distributed-systems complexity.

## 6. Microservices Best Practices

1. **Align services to business capabilities**, not technical concerns.
2. **Database-per-service** — never share a datastore.
3. **Prefer async** communication (events/queues) to reduce coupling.
4. **Automate** deployment, CI/CD, and observability from day one.
5. **Start with a modular monolith** if you're unsure — split later when boundaries are clear.
6. Invest in **distributed tracing** before you need it.

## 7. Microservices Examples

### Example 1 — E-commerce Split
```
[API Gateway] → Catalog Service (own DB)
              → Orders Service   (own DB)
              → Payments Service (own DB)
```
**Why:** each service scales and deploys independently; catalog can update without touching payments.

### Example 2 — Async Order Flow
**Why:** `Orders` publishes `OrderCreated`; `Inventory` and `Billing` react — no synchronous chain, resilient to individual service slowness.

## 8. Microservices Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Distributed monolith | Services coupled, deploy together | Loosen coupling; async comms; private data |
| Shared database | Hidden coupling via schema | Database-per-service |
| Chatty sync calls | Latency, cascading failures | Use async events/queues |
| Premature splitting | High complexity, low payoff | Start modular monolith |
| No observability | Can't debug distributed flows | Distributed tracing + logging |

---

# Event-Driven Architectures

## 9. What Is Event-Driven Architecture?

In an **Event-Driven Architecture (EDA)**, services communicate by **producing and consuming events** (via EventBridge, SQS, SNS, Kafka) rather than calling each other directly — enabling loose coupling and asynchronous processing.

- A service emits an event ("something happened"); interested services react **independently**.
- Producers don't know (or wait for) consumers.

**One-liner:** services react to events instead of calling each other directly.

## 10. Event-Driven Core Concepts

| Concept | Role |
|---|---|
| **Event** | An immutable fact ("OrderCreated") |
| **Producer / Consumer** | Emits / reacts to events |
| **Event bus / broker** | Routes events (EventBridge, Kafka, SNS) |
| **Queue** | Buffers work for consumers (SQS) |
| **Pub/Sub** | One event → many subscribers (fan-out) |
| **Eventual consistency** | State converges over time, not instantly |

## 11. How Event-Driven Systems Work

1. A service does something and **publishes an event**.
2. The broker **routes** it to subscribers (or queues it for workers).
3. Each consumer **reacts independently** — updating its own state, triggering more events, etc.
4. The system reaches consistency **eventually**, as events propagate.

**Key point:** the producer is fully decoupled from consumers — add a new consumer without touching the producer.

## 12. Event-Driven Patterns

- **Pub/Sub fan-out** — SNS topic → many SQS queues (one event, many reactions).
- **Event bus routing** — EventBridge routes by content/rules.
- **Queue-based work** — SQS absorbs load spikes; workers pull at their pace.
- **Event sourcing** — store events as the source of truth (optional, advanced).
- **Idempotent consumers** — safe to process the same event twice.

## 13. When to Use Event-Driven Architecture

- **Decoupling** services (producer shouldn't depend on consumers).
- **Async workflows** (don't block the request on slow downstream work).
- **Fan-out** — one event triggers many independent reactions.
- **Absorbing load spikes** via queues.

## 14. Event-Driven Best Practices

1. **Design idempotent consumers** — events can be delivered more than once.
2. **Version event schemas** — consumers and producers evolve independently.
3. **Embrace eventual consistency** — don't pretend it's synchronous.
4. **Use dead-letter queues** — capture poison messages for inspection.
5. **Monitor event lag** — detect slow/stuck consumers.
6. Keep events **small, named as past facts** (`OrderCreated`, not `CreateOrder`).

## 15. Event-Driven Examples

### Example 1 — Pub/Sub Fan-Out
```
Orders → publishes OrderCreated → [Inventory, Billing, Analytics] each react
```
**Why:** add an Analytics consumer later without changing Orders, Inventory, or Billing.

### Example 2 — Queue Absorbs a Spike
**Why:** an API enqueues `EmailSent` jobs to SQS and returns fast; workers send emails at their own pace even during traffic bursts.

### Example 3 — EventBridge Content Routing
**Why:** route `high-value` orders to a priority queue and others to a standard queue, by event content.

## 16. Event-Driven Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| No schema/versioning | Breaking consumers | Versioned event contracts |
| Non-idempotent consumers | Duplicate side effects | Make processing idempotent |
| Hidden event chains | Hard to trace logic | Map/document event flows |
| Eventual consistency ignored | Stale-UI bugs | Design UI for eventual consistency |
| No DLQ | Poison messages lost | Dead-letter queue + alerting |

---

# Multi-Tenant SaaS

## 17. What Is Multi-Tenant SaaS?

**Multi-Tenant SaaS** is a single application instance that serves **multiple tenants** (customers/organizations) with **isolated data**, custom configurations, and per-tenant features — all from one shared codebase.

- One deployment, many customers — economies of scale.
- Tenants must never see each other's data.

**One-liner:** one app, many customers, isolated data.

## 18. Tenant Isolation Models

| Model | Isolation | Cost/Complexity | Best for |
|---|---|---|---|
| **Database-per-tenant** | Strongest | High | Regulated/large tenants |
| **Schema-per-tenant** (shared DB) | Strong | Medium | Balanced isolation + efficiency |
| **Row-level** (shared schema, `tenant_id`) | Weakest | Lowest | Many small tenants |

**Key point:** the isolation model is the foundational decision — it drives security, cost, and operations. Changing it later is expensive.

## 19. How Multi-Tenancy Works

1. A request arrives; the system **resolves the tenant** (subdomain, header, JWT claim).
2. The **tenant context** flows through every query/route.
3. Data access is **scoped** to that tenant (RLS, schema, or separate DB).
4. Per-tenant **config/features** apply (feature flags, branding, limits).

**Rule of thumb:** tenant isolation must be enforced at the **data layer**, not relied upon in application code alone.

## 20. Multi-Tenant Patterns

- **Tenant resolution** — subdomain (`acme.app.com`), header, or JWT claim.
- **Row-Level Security (RLS)** — DB enforces `tenant_id` scoping.
- **Schema-per-tenant** — Postgres schema isolation.
- **Per-tenant feature flags / config** — toggle features per customer.
- **Tenant-aware caching/routing** — keys prefixed by tenant.

## 21. When to Build Multi-Tenant SaaS

- Building a **B2B SaaS** serving many customers from one codebase.
- Want **operational efficiency** (one deployment to maintain).
- Customers share most functionality with config/feature differences.

## 22. Multi-Tenant Best Practices

1. **Enforce isolation at the data layer** (RLS / schema / DB) — don't rely on app filters alone.
2. **Centralize tenant context** — never manually thread `tenant_id`.
3. **Never leak data across tenants** — test isolation rigorously.
4. **Per-tenant limits** — rate limits, quotas, backups to contain noisy neighbors.
5. **Plan tenant lifecycle** — onboarding, provisioning, and offboarding/data deletion.

## 23. Multi-Tenant Examples

### Example 1 — Schema-per-Tenant (Postgres)
**Why:** strong isolation and per-tenant backups/migrations, while sharing one DB server for efficiency.

### Example 2 — Row-Level with RLS
**Why:** Postgres RLS auto-appends `WHERE tenant_id = current` — even a forgotten app filter can't leak data.

### Example 3 — Subdomain → Tenant
**Why:** `acme.app.com` resolves to the `acme` tenant; branding/config follow automatically.

## 24. Multi-Tenant Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Cross-tenant data leak | One customer sees another's data | Enforce RLS/schema isolation |
| Missing tenant filter | Orphaned/broad queries | Centralize tenant context |
| Noisy neighbor | One tenant degrades others | Per-tenant quotas/rate limits |
| Wrong isolation model chosen early | Costly migration later | Choose deliberately upfront |
| Shared mutable state | Cross-tenant contamination | Keep all state tenant-scoped |

---

# Serverless Architectures

## 25. What Is Serverless Architecture?

**Serverless** is an event-driven, **pay-per-use** compute model where you run code (functions) **without managing servers** — the cloud provisions, scales, and operates the infrastructure (AWS Lambda, Google Cloud Functions, Azure Functions).

- You upload functions; the cloud runs them **on demand**, scaling to zero when idle.
- You pay **per invocation + duration**, not for idle servers.
- Often paired with **managed services** (BaaS) for DB, storage, auth.

**One-liner:** write functions, the cloud runs and scales them, you pay per use.

## 26. Serverless Core Concepts

| Concept | Role |
|---|---|
| **FaaS (Functions)** | Small, stateless functions triggered by events |
| **Triggers** | HTTP, queue, schedule, storage, stream events |
| **Auto-scaling to zero** | Scales with demand; no idle cost |
| **Pay-per-use** | Billed per invocation + execution time |
| **BaaS** | Managed backends (DynamoDB, S3, Cognito, Auth) |
| **Cold start** | Latency on first invocation after idle |

## 27. How Serverless Works

1. An **event** triggers a function (HTTP request, S3 upload, queue message, schedule).
2. The cloud **provisions** an execution environment (or reuses a warm one).
3. The function runs, does its work, and **returns/exits**.
4. You're billed only for the **invocation + duration**.

**Key point:** functions must be **stateless and short-lived** — store state in a DB/cache, not in the function.

## 28. Serverless Patterns

- **API backend** — API Gateway → Lambda → DynamoDB.
- **Event processing** — S3 upload → Lambda (resize, validate, enrich).
- **Scheduled jobs** — EventBridge cron → Lambda.
- **Stream processing** — DynamoDB Streams / Kinesis → Lambda.
- **Async fan-out** — SNS → many Lambdas.

## 29. When to Use Serverless

- **Variable/unpredictable load** (scales to zero, no over-provisioning).
- **Event-driven workloads** (react to uploads, messages, schedules).
- Want to **minimize operations** (no server patching/scaling).
- **Cost-sensitive low-traffic** apps (pay only when used).

## 30. Serverless Best Practices

1. **Keep functions small, stateless, and fast** — minimize cold-start impact.
2. **Use managed services (BaaS)** for DB/storage/auth — don't reimplement.
3. **Set timeouts + memory budgets** — avoid runaway cost.
4. **Decouple with queues** — absorb spikes, retry failures.
5. **Monitor per-invocation** — errors, duration, cost, cold starts.
6. **Optimize cold starts** — smaller packages, fewer deps, provisioned concurrency where needed.

## 31. Serverless Examples

### Example 1 — Image Processing
**Why:** user uploads to S3 → Lambda resizes/optimizes → stores derivatives — fully event-driven, scales with uploads, zero idle cost.

### Example 2 — Serverless API
```
Client → API Gateway → Lambda → DynamoDB
```
**Why:** no servers to manage; scales automatically with traffic.

### Example 3 — Scheduled Cleanup
**Why:** EventBridge runs a Lambda nightly to purge expired records — a cron job with zero infrastructure.

## 32. Serverless Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Cold-start latency | Slow first request | Smaller functions, provisioned concurrency |
| Vendor lock-in | Hard to migrate | Abstract cloud-specific code |
| Hard observability | Debugging distributed runs | Distributed tracing, structured logs |
| Cost at high scale | Cheaper to run servers | Model cost; consider reserved capacity |
| Over-engineering simple apps | Needless complexity | Use a simpler model if load is steady |

---

## Shared Foundations

Concepts that recur across **all four patterns**:

- **Loose coupling** — the unifying goal. Microservices decouple services; EDA decouples producers/consumers; multi-tenancy decouples tenants; serverless decouples you from infrastructure.
- **Data ownership & isolation** — microservices own their data; multi-tenant isolates tenant data; both demand clear boundaries.
- **Asynchrony & eventual consistency** — EDA and microservices lean on async communication; design for eventual, not instant, consistency.
- **Operational maturity** — all four increase architectural power but require **observability, automation, and discipline** to run reliably.
- **Tradeoffs** — each pattern trades simplicity for flexibility/scalability. Apply them where the payoff exceeds the added complexity; don't adopt because they're trendy.

## Quick Reference Card

```
FOUR ORTHOGONAL AXES (combine, don't choose one):
  How to SPLIT services?        → Microservices
  How services COMMUNICATE?     → Event-Driven
  How to SERVE many customers?  → Multi-Tenant SaaS
  How to RUN/scale compute?     → Serverless

TYPICAL MODERN SaaS:  serverless + event-driven + multi-tenant microservices

WHEN TO USE EACH:
  Microservices   → large domain, multiple teams, independent scaling
  Event-Driven    → decouple producers/consumers, async workflows, fan-out
  Multi-Tenant    → B2B SaaS, many customers, one codebase
  Serverless      → variable load, event-driven, minimize ops, low traffic

GOLDEN RULES:
  ✓ Microservices: database-per-service, async where possible
  ✓ Event-Driven:  idempotent consumers, versioned schemas, eventual consistency
  ✓ Multi-Tenant:  enforce isolation at the DATA layer (RLS/schema), never leak
  ✓ Serverless:    small/stateless functions, BaaS, watch cold starts + cost
  ✓ All four:      invest in observability before you need it
```

---

*This file covers four applied architecture patterns (Part 2 of the structures-architecture series). More patterns (CQRS, Hexagonal deep-dive, Saga, Messaging systems) will be added over time.*
