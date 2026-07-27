# Messaging & Queues — Complete Guide

> **Series:** Messaging Documentation — Part 1
> This file covers the **messaging discipline** (queues & pub/sub) and the major **message brokers** (RabbitMQ, GCP Pub/Sub, Bull/BullMQ). Related: AWS messaging (SQS/SNS/EventBridge) is covered in `cloud-service/cloud-platforms.md` §56–66; the Event-Driven *architectural pattern* is in `structures-architecture/architecture-patterns.md` §9–16. More topics (Kafka, SQS deep-dive, message schema design) will be added later.

---

## Table of Contents

- [Shared Orientation — The Messaging Landscape](#shared-orientation--the-messaging-landscape)
- **Message Queues & Pub/Sub**
  - [1. What Are Message Queues and Pub/Sub?](#1-what-are-message-queues-and-pubsub)
  - [2. Queues vs Pub/Sub](#2-queues-vs-pubsub)
  - [3. How Messaging Works](#3-how-messaging-works)
  - [4. Messaging Core Concepts](#4-messaging-core-concepts)
  - [5. Where to Use Messaging](#5-where-to-use-messaging)
  - [6. Where NOT to Use Messaging](#6-where-not-to-use-messaging)
  - [7. Choosing and Setting Up a Broker](#7-choosing-and-setting-up-a-broker)
  - [8. Delivery Semantics and Guarantees](#8-delivery-semantics-and-guarantees)
  - [9. Messaging Production Best Practices](#9-messaging-production-best-practices)
  - [10. Messaging Real-World Examples](#10-messaging-real-world-examples)
  - [11. Messaging Pitfalls](#11-messaging-pitfalls)
- **RabbitMQ**
  - [12. What Is RabbitMQ?](#12-what-is-rabbitmq)
  - [13. RabbitMQ vs SQS vs Kafka](#13-rabbitmq-vs-sqs-vs-kafka)
  - [14. How RabbitMQ Works](#14-how-rabbitmq-works)
  - [15. RabbitMQ Key Concepts](#15-rabbitmq-key-concepts)
  - [16. Where to Use RabbitMQ](#16-where-to-use-rabbitmq)
  - [17. Where NOT to Use RabbitMQ](#17-where-not-to-use-rabbitmq)
  - [18. Installing and Setting Up RabbitMQ](#18-installing-and-setting-up-rabbitmq)
  - [19. RabbitMQ Connection and Auth](#19-rabbitmq-connection-and-auth)
  - [20. RabbitMQ Production Best Practices](#20-rabbitmq-production-best-practices)
  - [21. RabbitMQ Real-World Examples](#21-rabbitmq-real-world-examples)
  - [22. RabbitMQ Pitfalls](#22-rabbitmq-pitfalls)
- **GCP Pub/Sub**
  - [23. What Is GCP Pub/Sub?](#23-what-is-gcp-pubsub)
  - [24. GCP Pub/Sub vs SQS vs RabbitMQ](#24-gcp-pubsub-vs-sqs-vs-rabbitmq)
  - [25. How GCP Pub/Sub Works](#25-how-gcp-pubsub-works)
  - [26. GCP Pub/Sub Key Concepts](#26-gcp-pubsub-key-concepts)
  - [27. Where to Use GCP Pub/Sub](#27-where-to-use-gcp-pubsub)
  - [28. Where NOT to Use GCP Pub/Sub](#28-where-not-to-use-gcp-pubsub)
  - [29. Setting Up GCP Pub/Sub](#29-setting-up-gcp-pubsub)
  - [30. GCP Pub/Sub Access and Auth](#30-gcp-pubsub-access-and-auth)
  - [31. GCP Pub/Sub Production Best Practices](#31-gcp-pubsub-production-best-practices)
  - [32. GCP Pub/Sub Real-World Examples](#32-gcp-pubsub-real-world-examples)
  - [33. GCP Pub/Sub Pitfalls](#33-gcp-pubsub-pitfalls)
- **Bull / BullMQ**
  - [34. What Is Bull and BullMQ?](#34-what-is-bull-and-bullmq)
  - [35. Bull vs RabbitMQ vs SQS](#35-bull-vs-rabbitmq-vs-sqs)
  - [36. How Bull Works](#36-how-bull-works)
  - [37. Bull Key Concepts](#37-bull-key-concepts)
  - [38. Where to Use Bull](#38-where-to-use-bull)
  - [39. Where NOT to Use Bull](#39-where-not-to-use-bull)
  - [40. Setting Up Bull](#40-setting-up-bull)
  - [41. Bull Connection and Redis](#41-bull-connection-and-redis)
  - [42. Bull Production Best Practices](#42-bull-production-best-practices)
  - [43. Bull Real-World Examples](#43-bull-real-world-examples)
  - [44. Bull Pitfalls](#44-bull-pitfalls)
- [Shared Foundations](#shared-foundations)
- [Quick Reference Card](#quick-reference-card)

---

## Shared Orientation — The Messaging Landscape

Messaging is how services talk **asynchronously** through a broker instead of calling each other directly. There are two core models and many brokers.

**Two models:**
| Model | How it works | Use for |
|---|---|---|
| **Queue (point-to-point)** | One message → one consumer | Tasks, background jobs, work distribution |
| **Pub/Sub (fan-out)** | One message → many subscribers | Events, notifications, broadcasts |

**Broker landscape:**
| Broker | Type | One-liner |
|---|---|---|
| **AWS SQS/SNS/EventBridge** | Managed (AWS) | See `cloud-platforms.md` §56–66 |
| **RabbitMQ** | Self-hosted broker | Flexible routing, mature, AMQP |
| **GCP Pub/Sub** | Managed (GCP) | Global, auto-scaling pub/sub |
| **Bull / BullMQ** | Redis-based (Node.js) | Job queues embedded in a Node.js app |
| **Kafka** | Streaming platform | High-throughput event streams (not covered here) |

**Rule of thumb:** **queues** for tasks/jobs, **pub/sub** for events/fan-out. Pick a **managed broker** (SQS, Pub/Sub) to avoid ops, **RabbitMQ** for self-hosted flexible routing, or **BullMQ** for Node.js background jobs backed by Redis.

---

# Message Queues & Pub/Sub

## 1. What Are Message Queues and Pub/Sub?

**Message queues and pub/sub** are forms of **asynchronous messaging** where services communicate through a **broker** (AWS SQS, GCP Pub/Sub, Bull, RabbitMQ) instead of calling each other directly — enabling decoupling, background jobs, and absorbing workload spikes.

**One-liner:** services talk via a broker, not direct calls — decoupled and resilient.

## 2. Queues vs Pub/Sub

| | Queue (point-to-point) | Pub/Sub (fan-out) |
|---|---|---|
| Delivery | One message → one consumer | One message → many subscribers |
| Model | Producers enqueue, workers dequeue | Publishers publish, subscribers receive |
| Use for | Tasks, jobs, work distribution | Events, notifications, broadcasts |
| Example | SQS, RabbitMQ work queues | SNS, Pub/Sub topics |

**Rule of thumb:** **queue** when work should be done once by one worker; **pub/sub** when many services should react to the same event.

## 3. How Messaging Works

1. A **producer** sends a message to a **broker** (queue or topic).
2. The broker **stores/routes** it durably.
3. A **consumer** receives and processes it, then **acknowledges**.
4. On failure, the message is **retried** or sent to a **dead-letter queue**.

**Key point:** the producer doesn't wait for the consumer — the system is **decoupled** and can **buffer** spikes.

## 4. Messaging Core Concepts

| Concept | Meaning |
|---|---|
| **Producer / Consumer** | Sends / processes messages |
| **Broker** | The intermediary (queue/topic host) |
| **Ack / Nack** | Consumer confirms / rejects processing |
| **Delivery semantics** | At-most-once, at-least-once, exactly-once |
| **Ordering** | Whether message order is preserved |
| **DLQ** | Dead-letter queue for failed messages |
| **Durability** | Messages survive broker restarts |

## 5. Where to Use Messaging

- **Decoupling microservices** (async communication).
- **Background jobs** (emails, reports, image processing).
- **Absorbing workload spikes** (buffer via queues).
- **Fan-out** (one event → many reactions).
- **Async workflows** that shouldn't block the request.

## 6. Where NOT to Use Messaging

- **Synchronous request/response** needs (use direct API calls).
- **Strong immediate consistency** requirements.
- Simple cases where a **direct call** is genuinely enough.

## 7. Choosing and Setting Up a Broker

- **Managed** (SQS, GCP Pub/Sub) — no ops, scales automatically; cloud-specific.
- **Self-hosted** (RabbitMQ) — full control, flexible routing; you run it.
- **Embedded** (BullMQ) — Redis-backed, lives in your Node.js app.

**Rule of thumb:** prefer **managed** unless you need self-hosting/flexible routing (RabbitMQ) or Node.js-native job queues (BullMQ).

## 8. Delivery Semantics and Guarantees

- **At-least-once** (most common) — messages may be delivered **more than once** → consumers **must be idempotent**.
- **At-most-once** — may lose messages (rarely acceptable).
- **Exactly-once** — hard; usually emulated via idempotency + dedup.
- **Ordering** — often not guaranteed across a queue unless using FIFO/ordering keys.

**Key point:** design for **at-least-once** — assume duplicates and make processing idempotent.

## 9. Messaging Production Best Practices

1. **Idempotent consumers** — the #1 rule (at-least-once delivery).
2. **Dead-letter queues** — capture poison messages.
3. **Tune ack/visibility** to processing time.
4. **Monitor queue depth / lag** — detect stuck consumers.
5. **Apply backpressure** — don't let consumers drown.
6. **Version message schemas** — evolve producers/consumers independently.

## 10. Messaging Real-World Examples

### Example 1 — Background Job Queue
**Why:** API enqueues "send welcome email" and returns instantly; a worker sends it asynchronously — the user never waits.

### Example 2 — Fan-Out Notification
**Why:** `OrderCreated` published once → inventory, billing, and analytics each react independently.

### Example 3 — Spike Buffering
**Why:** a traffic burst floods the queue, but workers process at a steady rate — the system stays up.

## 11. Messaging Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Non-idempotent consumers | Duplicate side effects | Idempotency keys |
| No DLQ | Poison messages vanish/loop | Configure DLQs |
| Ignoring ordering | Out-of-order bugs | FIFO/ordering keys where needed |
| Treating as synchronous | Timeouts, confusion | Design for async |
| Unbounded queues | Memory/ops issues | Monitor + alert on depth |

---

# RabbitMQ

## 12. What Is RabbitMQ?

**RabbitMQ** is a mature, open-source **message broker** implementing AMQP, known for **flexible routing** (exchanges) and reliability.

**One-liner:** the mature, feature-rich, self-hosted message broker.

## 13. RabbitMQ vs SQS vs Kafka

| | RabbitMQ | SQS | Kafka |
|---|---|---|---|
| Hosting | Self-hosted | AWS managed | Self/managed |
| Routing | Flexible (exchanges) | Simple queue | Log/stream |
| Best for | Flexible routing, control | Managed AWS messaging | High-throughput streams |

**Rule of thumb:** RabbitMQ for **flexible routing + self-hosting**; SQS for **managed AWS**; Kafka for **high-throughput event streams**.

## 14. How RabbitMQ Works

1. **Producers** publish to an **exchange** (not directly to a queue).
2. The exchange **routes** messages to **queues** via **bindings** and **routing keys**.
3. **Consumers** subscribe to queues and process messages (with acks).

**Key point:** the **exchange/binding** model is RabbitMQ's power — sophisticated routing topologies.

## 15. RabbitMQ Key Concepts

- **Exchanges** — direct, topic, fanout, headers (routing logic).
- **Queues** — hold messages for consumers.
- **Bindings / routing keys** — connect exchanges to queues.
- **Channels** — lightweight connections within a connection.
- **Acks, durability, DLX** (dead-letter exchange).

## 16. Where to Use RabbitMQ

- **Flexible/complex routing** needs (topic/headers exchanges).
- **Self-hosted** messaging (full control, on-prem).
- **Background jobs** and work queues.
- **RPC-over-messaging** patterns.

## 17. Where NOT to Use RabbitMQ

- **Massive streaming throughput** (use Kafka).
- Want **fully managed** (use SQS/Pub/Sub).
- Simple needs where a lighter tool suffices.

## 18. Installing and Setting Up RabbitMQ

```bash
# Docker (with management UI on :15672)
docker run -p 5672:5672 -p 15672:15672 rabbitmq:3-management

# Declare an exchange + queue, publish, consume (via client library)
# Management UI: http://localhost:15672 (guest/guest)
```

## 19. RabbitMQ Connection and Auth

- **AMQP connection string** — `amqp://user:pass@host:5672/vhost`.
- **Users, vhosts, permissions** — isolate apps/tenants.
- **TLS** for encrypted connections in production.

## 20. RabbitMQ Production Best Practices

1. **Use exchanges** for routing, not direct-to-queue hacks.
2. **Durable queues + persistent messages** — survive restarts.
3. **Prefetch/QoS** — control how many unacked messages a consumer holds.
4. **Dead-letter exchanges (DLX)** — handle failures.
5. **Monitor queue depth** and consumer health.

## 21. RabbitMQ Real-World Examples

### Example 1 — Work Queue
**Why:** producers enqueue tasks; multiple workers share the load — natural work distribution.

### Example 2 — Topic Routing
**Why:** route `logs.error` to an alerting queue and `logs.*` to an archive queue — one exchange, content-based routing.

### Example 3 — Fanout Pub/Sub
**Why:** broadcast an event to all bound queues — every subscriber gets a copy.

## 22. RabbitMQ Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Non-durable queues | Data loss on restart | Durable queues + persistent messages |
| No DLX | Poison messages lost | Dead-letter exchange |
| No prefetch limit | Consumer overload | Set QoS/prefetch |
| Treating as a database | Misuse, bloat | It's a broker, not storage |

---

# GCP Pub/Sub

## 23. What Is GCP Pub/Sub?

**Google Cloud Pub/Sub** is a **fully managed, global messaging service** for asynchronous event ingestion and delivery at scale.

**One-liner:** Google Cloud's managed pub/sub — global and auto-scaling.

## 24. GCP Pub/Sub vs SQS vs RabbitMQ

| | GCP Pub/Sub | SQS | RabbitMQ |
|---|---|---|---|
| Hosting | GCP managed | AWS managed | Self-hosted |
| Model | Topic + subscriptions | Queue | Exchanges/queues |
| Scale | Global, automatic | AWS-scale | You scale it |

**Rule of thumb:** GCP Pub/Sub for **managed, global messaging on Google Cloud**; SQS on AWS; RabbitMQ for self-hosted control.

## 25. How GCP Pub/Sub Works

1. **Publishers** send messages to a **topic**.
2. **Subscriptions** attach to the topic (each gets its own copy).
3. **Subscribers** receive via **push** (webhook) or **pull**.
4. **At-least-once** delivery; subscribers **ack** messages.

**Key point:** one topic → many independent subscriptions = built-in fan-out.

## 26. GCP Pub/Sub Key Concepts

- **Topic** — the channel publishers send to.
- **Subscription** — a named consumer view (push or pull).
- **Message + attributes** — payload + metadata.
- **Ack / ack deadline**, **ordering keys**, **dead-letter topics**, **schemas**.

## 27. Where to Use GCP Pub/Sub

- **Event ingestion** at scale.
- **Decoupling GCP services**.
- **Streaming analytics pipelines** (source for Dataflow).
- **Global fan-out** across regions.

## 28. Where NOT to Use GCP Pub/Sub

- On **AWS/Azure** (use their native services).
- Need **exactly-once** or complex broker routing.

## 29. Setting Up GCP Pub/Sub

```bash
gcloud pubsub topics create order-events
gcloud pubsub subscriptions create order-sub --topic=order-events
gcloud pubsub topics publish order-events --message="hello"
gcloud pubsub subscriptions pull order-sub --auto-ack
```

## 30. GCP Pub/Sub Access and Auth

- **IAM roles** — `pubsub.publisher`, `pubsub.subscriber`.
- **Service accounts** for workloads (least privilege).

## 31. GCP Pub/Sub Production Best Practices

1. **Idempotent subscribers** — at-least-once means duplicates.
2. **Dead-letter topics** — handle poison messages.
3. **Ordering keys** — only where order matters (limits throughput).
4. **Flow control** — limit outstanding messages per subscriber.
5. **Monitor backlog/oldest unacked** — detect stuck consumers.

## 32. GCP Pub/Sub Real-World Examples

### Example 1 — Event Ingestion
**Why:** apps publish events to a topic; analytics and alerting subscriptions each consume independently.

### Example 2 — Dataflow Pipeline Source
**Why:** Pub/Sub feeds a Dataflow streaming job into BigQuery — serverless analytics pipeline.

## 33. GCP Pub/Sub Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Assuming exactly-once | Duplicate processing | Idempotent subscribers |
| No dead-letter topic | Lost poison messages | Configure DLQ |
| Overusing ordering keys | Reduced throughput | Order only where needed |
| Ignoring flow control | Subscriber overload | Set flow-control limits |

---

# Bull / BullMQ

## 34. What Is Bull and BullMQ?

**Bull** and its successor **BullMQ** are **Redis-based Node.js queue libraries** for background jobs — task queues that live inside your Node.js application.

**One-liner:** fast, Redis-backed job queues for Node.js apps.

## 35. Bull vs RabbitMQ vs SQS

| | Bull/BullMQ | RabbitMQ | SQS |
|---|---|---|---|
| Nature | Node.js library (Redis) | Standalone broker | AWS managed service |
| Scope | Within a Node.js app | Cross-service/polyglot | Cloud-scale, polyglot |
| Best for | Node.js background jobs | Flexible broker routing | Managed AWS messaging |

**Rule of thumb:** BullMQ for **Node.js background jobs backed by Redis**; RabbitMQ/SQS for **cross-service or polyglot** messaging.

## 36. How Bull Works

- **Jobs** are added to **Redis-backed queues**.
- **Workers** (processors) pull and process jobs.
- **Events** track the job lifecycle (waiting → active → completed/failed).
- Built entirely on **Redis** data structures.

**Key point:** BullMQ turns Redis into a full job-queue system — no separate broker to run.

## 37. Bull Key Concepts

- **Queue** — holds jobs of a type.
- **Job** — a unit of work (data + options).
- **Worker/processor** — the function that processes jobs.
- **Events** — `completed`, `failed`, `progress`.
- **Delayed/repeatable jobs**, **priorities**, **rate limiting**, **concurrency**.

## 38. Where to Use Bull

- **Node.js background jobs** — emails, reports, image/video processing.
- **Scheduled/cron jobs** (repeatable jobs).
- **Task queues** within a Node.js application.
- When you already run **Redis** and want simple job queues.

## 39. Where NOT to Use Bull

- **Cross-language/cross-service** messaging (use a broker).
- Want **fully managed/global** (SQS/Pub/Sub).
- **Very high-throughput streaming** (Kafka).

## 40. Setting Up Bull

```bash
npm install bullmq
```

```typescript
import { Queue, Worker } from "bullmq";

const emailQueue = new Queue("email", { connection: { host: "localhost", port: 6379 } });
await emailQueue.add("welcome", { userId: 42 });

new Worker("email", async (job) => {
  await sendEmail(job.data.userId);
}, { connection: { host: "localhost", port: 6379 } });
```

## 41. Bull Connection and Redis

- BullMQ connects to **Redis** — inherits Redis auth/TLS settings.
- The Redis instance holds all job state — size and secure it appropriately.
- See `caching/caching.md` for Redis setup, connection, and security.

## 42. Bull Production Best Practices

1. **Idempotent processors** — jobs may retry.
2. **Configure retries with backoff** — handle transient failures.
3. **Tune concurrency** — match workers to load.
4. **Separate queues by job type** — isolate workloads.
5. **Monitor via events** — track failed/stalled jobs.
6. **Watch Redis memory** — completed jobs should be cleaned up.

## 43. Bull Real-World Examples

### Example 1 — Email Queue
**Why:** API adds a "send email" job and responds instantly; a worker sends it — the request never blocks on SMTP.

### Example 2 — Scheduled Report
**Why:** a repeatable job runs a report nightly — cron-like scheduling without external infra.

### Example 3 — Image Processing Worker
**Why:** heavy image resizing runs in a worker with concurrency limits — keeps the API fast.

## 44. Bull Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Non-idempotent jobs | Duplicate side effects on retry | Idempotent processors |
| No retry config | Jobs fail permanently | Retries + backoff |
| Redis memory growth | OOM | Clean up completed jobs |
| Heavy sync work in processor | Blocks the event loop | Offload/keep processors async |
| Single Redis point of failure | Queue downtime | Redis HA (Sentinel/replica) |

---

## Shared Foundations

Concepts that recur across **all messaging topics**:

- **Async decoupling** — the core benefit: producers and consumers are independent; the broker buffers the difference. This underpins Event-Driven Architecture (see `architecture-patterns.md` §9–16).
- **Queues vs pub/sub** — point-to-point (work done once) vs fan-out (many react). Choose per use case.
- **At-least-once delivery** — the common default → **idempotent consumers are mandatory** (dedup/idempotency keys).
- **Dead-letter queues** — universal safety net for poison messages across every broker.
- **Backpressure & lag monitoring** — watch queue depth/oldest-unacked to catch stuck consumers before they become outages.
- **Managed vs self-hosted** — managed brokers (SQS, Pub/Sub) remove ops; self-hosted (RabbitMQ) gives control; embedded (BullMQ) keeps it simple within a Node.js app.

## Quick Reference Card

```
MODEL PICKER:
  Work done once by one worker?  → Queue (point-to-point)
  Many react to one event?       → Pub/Sub (fan-out)

BROKER PICKER:
  AWS, managed?        → SQS / SNS / EventBridge (see cloud-platforms.md)
  GCP, managed?        → GCP Pub/Sub
  Self-hosted routing? → RabbitMQ
  Node.js + Redis jobs?→ BullMQ
  High-throughput streams? → Kafka (not covered here)

UNIVERSAL RULES:
  ✓ Idempotent consumers (at-least-once delivery)
  ✓ Dead-letter queues for poison messages
  ✓ Monitor queue depth / lag / backlog
  ✓ Version message schemas
  ✓ Apply backpressure / flow control
  ✓ Design for async — never treat messaging as synchronous
```

---

*This file covers the messaging discipline and major brokers. More topics (Kafka & streaming, SQS deep-dive, message schema design) will be added as separate files in this series over time.*
