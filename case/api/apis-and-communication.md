# APIs & Communication — Complete Guide

> **Series:** APIs & Communication Documentation — Part 1
> This file covers **how systems talk to each other**: API styles (REST, GraphQL), real-time protocols (WebSockets, SSE), data formats (JSON, XML), and third-party integration. More topics (gRPC, tRPC, webhooks deep-dive, API gateways, API security) will be added as separate files later.

---

## Table of Contents

- [Shared Orientation — Choosing How Systems Talk](#shared-orientation--choosing-how-systems-talk)
- **RESTful APIs**
  - [1. What Is REST?](#1-what-is-rest)
  - [2. REST Core Concepts](#2-rest-core-concepts)
  - [3. How REST Works](#3-how-rest-works)
  - [4. REST Patterns](#4-rest-patterns)
  - [5. When to Use REST](#5-when-to-use-rest)
  - [6. REST Best Practices](#6-rest-best-practices)
  - [7. REST Examples](#7-rest-examples)
  - [8. REST Pitfalls](#8-rest-pitfalls)
- **GraphQL APIs**
  - [9. What Is GraphQL?](#9-what-is-graphql)
  - [10. GraphQL Core Concepts](#10-graphql-core-concepts)
  - [11. How GraphQL Works](#11-how-graphql-works)
  - [12. GraphQL Patterns](#12-graphql-patterns)
  - [13. When to Use GraphQL](#13-when-to-use-graphql)
  - [14. GraphQL Best Practices](#14-graphql-best-practices)
  - [15. GraphQL Examples](#15-graphql-examples)
  - [16. GraphQL Pitfalls](#16-graphql-pitfalls)
- **WebSockets**
  - [17. What Are WebSockets?](#17-what-are-websockets)
  - [18. WebSocket Core Concepts](#18-websocket-core-concepts)
  - [19. How WebSockets Work](#19-how-websockets-work)
  - [20. WebSocket Patterns](#20-websocket-patterns)
  - [21. When to Use WebSockets](#21-when-to-use-websockets)
  - [22. WebSocket Best Practices](#22-websocket-best-practices)
  - [23. WebSocket Examples](#23-websocket-examples)
  - [24. WebSocket Pitfalls](#24-websocket-pitfalls)
- **Server-Sent Events (SSE)**
  - [25. What Are Server-Sent Events?](#25-what-are-server-sent-events)
  - [26. SSE Core Concepts](#26-sse-core-concepts)
  - [27. How SSE Works](#27-how-sse-works)
  - [28. SSE Patterns](#28-sse-patterns)
  - [29. When to Use SSE](#29-when-to-use-sse)
  - [30. SSE Best Practices](#30-sse-best-practices)
  - [31. SSE Examples](#31-sse-examples)
  - [32. SSE Pitfalls](#32-sse-pitfalls)
- **JSON APIs**
  - [33. What Is a JSON API?](#33-what-is-a-json-api)
  - [34. JSON API Core Concepts](#34-json-api-core-concepts)
  - [35. How JSON APIs Work](#35-how-json-apis-work)
  - [36. JSON API Patterns](#36-json-api-patterns)
  - [37. When to Use JSON APIs](#37-when-to-use-json-apis)
  - [38. JSON API Best Practices](#38-json-api-best-practices)
  - [39. JSON API Examples](#39-json-api-examples)
  - [40. JSON API Pitfalls](#40-json-api-pitfalls)
- **XML APIs**
  - [41. What Is an XML API?](#41-what-is-an-xml-api)
  - [42. XML API Core Concepts](#42-xml-api-core-concepts)
  - [43. How XML APIs Work](#43-how-xml-apis-work)
  - [44. XML API Patterns](#44-xml-api-patterns)
  - [45. When to Use XML APIs](#45-when-to-use-xml-apis)
  - [46. XML API Best Practices](#46-xml-api-best-practices)
  - [47. XML API Examples](#47-xml-api-examples)
  - [48. XML API Pitfalls](#48-xml-api-pitfalls)
- **Third-Party Integrations**
  - [49. What Are Third-Party Integrations?](#49-what-are-third-party-integrations)
  - [50. Third-Party Integration Core Concepts](#50-third-party-integration-core-concepts)
  - [51. How Third-Party Integrations Work](#51-how-third-party-integrations-work)
  - [52. Third-Party Integration Patterns](#52-third-party-integration-patterns)
  - [53. When to Use Third-Party Integrations](#53-when-to-use-third-party-integrations)
  - [54. Third-Party Integration Best Practices](#54-third-party-integration-best-practices)
  - [55. Third-Party Integration Examples](#55-third-party-integration-examples)
  - [56. Third-Party Integration Pitfalls](#56-third-party-integration-pitfalls)
- [Shared Foundations](#shared-foundations)
- [Quick Reference Card](#quick-reference-card)

---

## Shared Orientation — Choosing How Systems Talk

These seven topics split into four groups. Each answers a different communication question:

| Group | Topics | Question it answers |
|---|---|---|
| **API styles** | REST, GraphQL | How do clients request data? |
| **Real-time protocols** | WebSockets, SSE | How do I push live updates? |
| **Data formats** | JSON, XML | What shape is the payload? |
| **Integration** | Third-Party | How do I connect to external vendors? |

**Decision guide:**
- CRUD / public API / wide compatibility? → **REST**
- Complex relational data, avoid over/under-fetching? → **GraphQL**
- Bidirectional real-time (chat, collab)? → **WebSockets**
- One-way server→client push (feeds, notifications)? → **SSE**
- New API payload format? → **JSON** (default)
- Legacy/enterprise system (payments, shipping, ERP)? → **XML/SOAP**
- External vendor (payments, travel, partners)? → **Adapters + webhooks**

---

# RESTful APIs

## 1. What Is REST?

**REST (Representational State Transfer)** is an architectural style for APIs built on HTTP: resources identified by URLs, manipulated with standard HTTP methods, and responses carrying proper status codes.

- The dominant style for web APIs — simple, stateless, cacheable.
- Typically returns JSON (see JSON APIs section).

**One-liner:** resource-oriented APIs over HTTP using standard verbs and status codes.

## 2. REST Core Concepts

| Concept | Meaning |
|---|---|
| **Resource** | A noun exposed at a URL (`/users/42`) |
| **HTTP methods** | GET (read), POST (create), PUT/PATCH (update), DELETE |
| **Status codes** | 200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Server Error |
| **Statelessness** | Each request carries all needed context; no server session |
| **Idempotency** | GET/PUT/DELETE are safe to repeat |
| **Versioning** | URL (`/v1/`), header, or media type |

## 3. How REST Works

1. Client sends an HTTP request to a resource URL with a method.
2. Server processes it (often with auth, validation) against that resource.
3. Server responds with a **status code** + payload (usually JSON).
4. Being **stateless**, the server holds no client context between requests.

**Key point:** model your domain as **resources** and let HTTP verbs express the action.

## 4. REST Patterns

- **CRUD endpoints** — `/users`, `/orders` with standard methods.
- **Nested resources** — `/users/42/orders` for relationships.
- **Pagination** — `?page=2&limit=20` (offset) or `?cursor=abc` (cursor, better for large data).
- **Filtering/sorting** — `?status=active&sort=-created_at`.
- **Versioning** — `/v1/users` or an `Accept-Version` header.

## 5. When to Use REST

- **Public APIs** needing wide client compatibility.
- **CRUD-heavy** services.
- When you want **HTTP caching**, simplicity, and universal tooling.

## 6. REST Best Practices

1. Use **nouns, not verbs** in URLs (`/orders`, not `/getOrders`).
2. Return **correct status codes** — don't return 200 for errors.
3. **Version** the API to protect clients from breaking changes.
4. **Paginate every list** — never return unbounded collections.
5. Use **idempotency keys** for writes (safe retries).
6. Keep **consistent naming** and error formats.

## 7. REST Examples

### Example 1 — CRUD + Pagination
```
GET    /users?page=2&limit=20     → 200 + user list
POST   /users                      → 201 + created user
PATCH  /users/42                   → 200 + updated user
DELETE /users/42                   → 204 No Content
```
**Why:** predictable, standard, self-describing via HTTP semantics.

### Example 2 — Versioned Endpoint
```
GET /v1/users   (stable contract)
GET /v2/users   (evolved schema)
```
**Why:** old clients keep working while new ones get improvements.

## 8. REST Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Verbs in URLs | `/getUser` non-idiomatic | Nouns + HTTP methods |
| Wrong status codes | 200 for errors | Use 4xx/5xx correctly |
| No versioning | Breaking clients on changes | Version from the start |
| Over/under-fetching | Too much/little data per call | Consider GraphQL for complex data |
| Unbounded lists | Slow, memory-heavy | Always paginate |

---

# GraphQL APIs

## 9. What Is GraphQL?

**GraphQL** is a typed query language and runtime where **clients request exactly the data they need** — nothing more, nothing less — from a single endpoint.

- Replaces "many fixed endpoints" with one flexible query interface.
- Strongly **typed schema** defines what's queryable.

**One-liner:** ask for exactly what you need, get exactly that.

## 10. GraphQL Core Concepts

| Concept | Role |
|---|---|
| **Schema** | Typed contract of all queryable data |
| **Query** | Read operation |
| **Mutation** | Write operation |
| **Resolver** | Function that fetches a field's data |
| **Subscription** | Real-time push (often over WebSockets) |
| **Single endpoint** | All requests go to `/graphql` |

## 11. How GraphQL Works

1. Client sends a **query document** describing the exact fields it wants.
2. The server validates it against the **schema**.
3. **Resolvers** fetch each requested field (from DB, APIs, etc.).
4. The response mirrors the query's shape — no over/under-fetching.

**Key point:** the client dictates the response shape; the server resolves fields on demand.

## 12. GraphQL Patterns

- **Schema-first design** — define the schema, then implement resolvers.
- **DataLoader** — batch/cache per-request to avoid N+1.
- **Connections** — cursor-based pagination (`edges`/`pageInfo`).
- **Persisted queries** — pre-register queries for safety + caching.
- **Fragments** — reusable field selections.

## 13. When to Use GraphQL

- **Complex/relational data** where REST needs many round trips.
- **Multiple clients** (web, mobile) needing different data shapes.
- Avoiding **over/under-fetching**.
- Rapid frontend iteration without backend changes.

## 14. GraphQL Best Practices

1. **Schema-first** — design the contract deliberately.
2. **Use DataLoader** — prevent N+1 resolver queries.
3. **Limit query depth/complexity** — prevent expensive/malicious queries.
4. **Persisted queries** in production (allowlist known operations).
5. **Cursor pagination** for lists.

## 15. GraphQL Examples

### Example 1 — Nested Query (one round trip)
```graphql
query {
  user(id: "42") {
    name
    orders { id total items { title } }
  }
}
```
**Why:** fetch a user + their orders + item titles in a single request — REST would need 3+ calls.

### Example 2 — Mutation
```graphql
mutation { createPost(title: "Hi") { id title } }
```
**Why:** writes are explicit and return exactly the fields you ask for.

## 16. GraphQL Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| N+1 resolvers | Slow nested queries | DataLoader batching |
| Unbounded query depth | DoS via expensive queries | Depth/complexity limits |
| Over-fetching by defaults | Bloated responses | Require explicit field selection |
| Caching complexity | Harder than REST's URL caching | Persisted queries, field-level caching |

---

# WebSockets

## 17. What Are WebSockets?

**WebSockets** provide a **full-duplex, persistent connection** over a single TCP connection, enabling real-time **bidirectional** data flow between client and server.

- After an HTTP **upgrade handshake**, both sides can send messages anytime.
- No request/response cycle — messages flow freely in both directions.

**One-liner:** a persistent two-way pipe for real-time data.

## 18. WebSocket Core Concepts

| Concept | Role |
|---|---|
| **Handshake** | HTTP `Upgrade: websocket` → persistent connection |
| **Frames** | Messages sent over the open connection |
| **Full-duplex** | Both directions, simultaneously |
| **Subprotocols** | Agreed message formats (e.g., JSON) |
| **Heartbeat** | Ping/pong to keep the connection alive |

## 19. How WebSockets Work

1. Client requests an **upgrade** over HTTP.
2. The connection switches to the **WebSocket protocol** (persistent).
3. Either side **sends frames** at any time — no polling.
4. Connection stays open until closed; heartbeats detect dead peers.

**Key point:** low-latency, always-on, two-way — ideal for interactive real-time.

## 20. WebSocket Patterns

- **Chat / messaging** — bidirectional by nature.
- **Live notifications** — push + ack.
- **Collaborative editing** — both sides send updates.
- **Live dashboards** — real-time metrics.
- **Presence** — who's online.

## 21. When to Use WebSockets

- **Low-latency, bidirectional** real-time (chat, collab, games).
- When **both** client and server push frequently.

## 22. WebSocket Best Practices

1. **Heartbeat (ping/pong)** — detect and drop dead connections.
2. **Reconnection logic** with backoff on the client.
3. **Authenticate on connect** (token during handshake).
4. **Scale across servers** with a pub/sub broker (Redis) — sockets are per-server.
5. **Apply backpressure** — don't let slow consumers pile up messages.

## 23. WebSocket Examples

### Example 1 — Chat
**Why:** messages flow both ways instantly — server pushes new messages to all room members.

### Example 2 — Collaborative Editing
**Why:** every participant's edits broadcast to others in real time.

## 24. WebSocket Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| No reconnection logic | Silent disconnects | Client auto-reconnect + backoff |
| No heartbeat | Zombie connections | Ping/pong keepalive |
| Scaling without a broker | Messages lost across servers | Redis/pub-sub behind servers |
| Unauthenticated sockets | Security hole | Auth token on connect |
| Using for one-way push | Overkill | Use SSE instead |

---

# Server-Sent Events (SSE)

## 25. What Are Server-Sent Events?

**SSE** lets a server **push real-time updates to a browser over plain HTTP** — a **one-way** (server→client) event stream.

- Uses the standard `EventSource` browser API.
- Simpler than WebSockets, but **one-directional**.

**One-liner:** one-way server→client streaming over plain HTTP.

## 26. SSE Core Concepts

| Concept | Role |
|---|---|
| **`text/event-stream`** | The HTTP content type |
| **EventSource** | Browser API that consumes the stream |
| **One-way push** | Server→client only |
| **Auto-reconnect** | Built into EventSource |
| **HTTP-based** | Works through proxies/firewalls easily |

## 27. How SSE Works

1. Client opens an HTTP request with `EventSource`.
2. Server responds with `text/event-stream` and **keeps the connection open**.
3. Server **writes events** as they happen.
4. If the connection drops, EventSource **auto-reconnects** (with `Last-Event-ID`).

**Key point:** simpler than WebSockets for one-way push — no upgrade handshake, plain HTTP.

## 28. SSE Patterns

- **Live notifications / feeds**.
- **Stock tickers / live scores**.
- **Progress updates** for long-running jobs.
- **Log / event streaming**.

## 29. When to Use SSE

- **One-way** server→client updates where you don't need client→server push.
- You want **simplicity** (plain HTTP, auto-reconnect) over WebSockets.

## 30. SSE Best Practices

1. **Use for one-way only** — WebSockets if you need two-way.
2. **Send heartbeats/comments** — prevent proxies from closing idle connections.
3. **Handle reconnection** (EventSource does most of it).
4. Set **proper headers** (`text/event-stream`, no buffering).

## 31. SSE Examples

### Example 1 — Live Feed
**Why:** server pushes new feed items as they arrive; browser updates with no polling.

### Example 2 — Job Progress
**Why:** a long export streams progress percentages; the UI shows a live progress bar.

## 32. SSE Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Using for two-way | Wrong tool | Use WebSockets |
| HTTP/1.1 connection limits | Few streams per browser | Use HTTP/2 |
| Proxy buffering | Delayed/no events | Disable buffering, send heartbeats |
| No heartbeat | Connections dropped | Periodic comment/keepalive |

---

# JSON APIs

## 33. What Is a JSON API?

A **JSON API** is an API that uses **JSON** as its request/response data format — the de facto standard for modern web APIs.

- **Lightweight, human-readable**, and parsed natively by virtually every language.
- The default payload format for REST and many GraphQL responses.

**One-liner:** the standard lightweight data-interchange format for modern APIs.

## 34. JSON API Core Concepts

| Concept | Role |
|---|---|
| **JSON structure** | Key-value objects, arrays, nesting |
| **Content-Type** | `application/json` |
| **UTF-8** | Standard encoding |
| **Language-agnostic** | Native parsers everywhere |
| **JSON:API (optional)** | A formal spec for consistent JSON APIs |

## 35. How JSON APIs Work

- Client sends a request with a JSON body (`POST`/`PUT`/`PATCH`).
- Server validates and parses the JSON.
- Server responds with a JSON payload + status code.
- Client parses the JSON into native objects.

**Key point:** JSON is the payload *format* — independent of the API *style* (REST, RPC, etc.).

## 36. JSON API Patterns

- **Consistent response envelopes** — `{ data, error, meta }`.
- **Consistent error objects** — `{ code, message, details }`.
- **JSON:API spec** — for teams wanting a strict convention.
- **Schema validation** — validate incoming JSON (zod, JSON Schema).

## 37. When to Use JSON APIs

- **Virtually all modern web APIs** — it's the default unless a system requires otherwise.

## 38. JSON API Best Practices

1. **Consistent key naming** (snake_case or camelCase — pick one).
2. Set **`application/json`** content-type correctly.
3. **Validate incoming JSON** against a schema.
4. **Consistent error format** across all endpoints.
5. Avoid **over-fetching** — return only what's needed.

## 39. JSON API Examples

### Example 1 — Request + Response
```json
// POST /users   (request)
{ "name": "Shumon", "email": "s@example.com" }

// 201 Created   (response)
{ "data": { "id": 42, "name": "Shumon" }, "error": null }
```
**Why:** lightweight, universally parseable, self-describing.

## 40. JSON API Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Inconsistent schemas | Client parsing bugs | Validate + document schemas |
| Over-fetching | Huge payloads | Return only needed fields |
| No validation | Bad data crashes handlers | Schema-validate input |
| Encoding issues | Corrupted unicode | Enforce UTF-8 |

---

# XML APIs

## 41. What Is an XML API?

An **XML API** uses **XML** for request/response payloads — verbose but strongly typed via schemas. Still required by many **legacy and enterprise systems** (payments, CRMs, shipping, ERP).

- Common in older enterprise integrations and **SOAP** web services.
- Largely superseded by JSON for new APIs.

**One-liner:** XML-based data format, mostly for legacy/enterprise integration.

## 42. XML API Core Concepts

| Concept | Role |
|---|---|
| **XML structure** | Tags, attributes, nesting |
| **XSD** | Schema for validation |
| **SOAP** | Protocol built on XML (envelope, headers) |
| **Namespaces** | Disambiguate element names |
| **XML-RPC** | RPC over XML |

## 43. How XML APIs Work

- Client sends an XML document (often a SOAP envelope).
- Server **validates against an XSD** and processes it.
- Server responds with an XML payload.
- Client parses the XML (namespaces, attributes, elements).

**Key point:** XML trades brevity for **strong typing** and **validation** via schemas — hence its persistence in enterprise.

## 44. XML API Patterns

- **SOAP web services** — enterprise integrations.
- **XSD validation** — enforce payload structure.
- **Legacy integrations** — payments (older gateways), shipping carriers, CRMs, ERPs.
- **XML-RPC** — lightweight RPC over XML.

## 45. When to Use XML APIs

- **Integrating with legacy/enterprise systems** that require XML/SOAP.
- When a partner's contract is defined in **XSD**.

## 46. XML API Best Practices

1. **Validate against XSD** — catch malformed payloads early.
2. **Handle namespaces carefully** — a common source of parsing bugs.
3. **Guard against XXE** (XML External Entity) attacks — disable external entities.
4. **Prefer JSON for new APIs** — use XML only when the system requires it.

## 47. XML API Examples

### Example 1 — SOAP Request
```xml
<soap:Envelope xmlns:soap="...">
  <soap:Body>
    <GetPrice><sku>ABC123</sku></GetPrice>
  </soap:Body>
</soap:Envelope>
```
**Why:** many legacy payment/shipping providers still speak SOAP/XML — you must integrate as-is.

## 48. XML API Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Verbose payloads | Bandwidth waste | Accept it (legacy), or wrap |
| Namespace complexity | Parsing bugs | Namespace-aware parsers |
| XXE injection | Security hole | Disable external entities |
| Harder parsing than JSON | Dev friction | Use mature XML libraries |

---

# Third-Party Integrations

## 49. What Are Third-Party Integrations?

**Third-Party Integrations** connect your application to **external vendors** — payment gateways, travel suppliers, partner services — via their **APIs** (outbound) and **webhooks** (inbound events).

- Outbound: you call their API (charge a card, search flights).
- Inbound: they call you (webhooks for payment success, booking updates).

**One-liner:** extend your system by consuming external APIs and reacting to their webhooks.

## 50. Third-Party Integration Core Concepts

| Concept | Role |
|---|---|
| **Outbound API calls** | You call the vendor's API |
| **Webhooks** | Vendor pushes events to your endpoint |
| **API keys / OAuth** | Vendor authentication |
| **Rate limits** | Vendor-imposed call quotas |
| **Idempotency** | Safe retries without duplicates |
| **Sandbox environments** | Safe testing against vendor |

## 51. How Third-Party Integrations Work

1. **Outbound:** your code calls the vendor's API with auth; handle their response/errors.
2. **Inbound:** the vendor POSTs events to your **webhook endpoint**; you verify the **signature**, process idempotently, and respond fast.
3. You wrap the vendor behind an **adapter** so your core code stays vendor-agnostic.

**Key point:** treat third parties as **unreliable and slow** — isolate them, handle failures, never let them block or break your core.

## 52. Third-Party Integration Patterns

- **Adapter / anti-corruption layer** — your interface wrapping the vendor.
- **Webhook receivers** — verify signatures, respond fast, process async.
- **Polling vs webhooks** — prefer webhooks; poll as a fallback.
- **Circuit breaker** — stop calling a failing vendor temporarily.
- **Retry + idempotency** — safe recovery from transient failures.

## 53. When to Use Third-Party Integrations

- **Payments** (Stripe, PayPal), **travel** (GDS/NDC suppliers), **shipping**, **CRMs**, **ERPs**.
- Any feature you'd rather **buy than build**.

## 54. Third-Party Integration Best Practices

1. **Wrap vendors in adapters** — swap vendors without touching core logic.
2. **Verify webhook signatures** — prevent spoofed events.
3. **Retry with backoff + idempotency keys** — survive transient failures.
4. **Respect rate limits** — queue/throttle outbound calls.
5. **Use sandbox environments** for testing.
6. **Circuit-break failing vendors** — don't let them cascade into your app.
7. **Monitor + alert** on integration failures.

## 55. Third-Party Integration Examples

### Example 1 — Payment Gateway Adapter
```python
class PaymentGateway(Protocol):
    def charge(self, amount, token) -> ChargeResult: ...

class StripeAdapter(PaymentGateway): ...
```
**Why:** your checkout code depends on your interface, not Stripe — swap processors freely.

### Example 2 — Secure Webhook Receiver
**Why:** verify the HMAC signature before processing a `payment_succeeded` event — reject spoofed/forged webhooks.

### Example 3 — Webhook + Polling Fallback
**Why:** rely on webhooks for real-time updates; a periodic poll catches any missed events.

## 56. Third-Party Integration Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| No signature verification | Spoofed webhooks | Verify HMAC signatures |
| Cascading failures | Vendor outage breaks your app | Circuit breakers, timeouts |
| Hardcoded to one vendor | Painful to switch | Adapter layer |
| Ignoring rate limits | 429s, throttling | Queue + throttle outbound calls |
| No retry/idempotency | Duplicate charges/jobs | Idempotency keys + backoff |

---

## Shared Foundations

Concepts that recur across **all seven topics**:

- **Request/response vs streaming** — REST/GraphQL/JSON/XML are request-driven; WebSockets/SSE are streaming. Choose by interaction model, not habit.
- **Contracts & schemas** — GraphQL schema, XSD, OpenAPI/JSON Schema: a clear contract prevents integration bugs and enables tooling.
- **Idempotency & retries** — essential everywhere: REST writes, webhook processing, third-party calls. Retries without idempotency cause duplicates.
- **Versioning & backward compatibility** — evolve APIs without breaking existing clients (REST versioning, GraphQL's additive schema, event schema versioning).
- **Reliability patterns** — timeouts, circuit breakers, backpressure, dead-letter handling — assume the network and the vendor will fail.
- **Security** — authenticate requests, verify webhook signatures, validate all payloads (and defend against XXE in XML).

## Quick Reference Card

```
PICK BY INTERACTION MODEL:
  CRUD / public / compatible?     → REST
  Complex relational data?        → GraphQL
  Two-way real-time?              → WebSockets
  One-way server push?            → SSE

PICK BY PAYLOAD:
  New API?        → JSON (default)
  Legacy/enterprise? → XML/SOAP (validate with XSD, guard XXE)

INTEGRATING VENDORS:
  Wrap in an adapter  +  verify webhook signatures
  +  retry/idempotency  +  circuit breaker  +  sandbox testing

GOLDEN RULES:
  ✓ REST: nouns + correct status codes + version + paginate
  ✓ GraphQL: schema-first, DataLoader, depth limits
  ✓ WebSockets: heartbeat, reconnect, broker for scale
  ✓ SSE: one-way only, heartbeats, auto-reconnect
  ✓ Integrations: never let a vendor cascade failures into you
```

---

*This file covers API styles, real-time protocols, data formats, and integration. More topics (gRPC, tRPC, webhooks deep-dive, API gateways, API security) will be added as separate files in this series over time.*
