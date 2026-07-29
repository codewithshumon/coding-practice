# Engineer Event-Driven Workflows

> **Category:** Data Pipeline & Processing
> **Relevant at:** Eicra Soft (EventBridge, SQS, SNS for microservice communication)
> **Related tech docs:** `case/structures-architecture/architecture-patterns.md` (Event-Driven §9–16, Microservices §1–8), `case/messaging/message-queues.md` (all §1–44), `case/cloud-service/cloud-platforms.md` (AWS Messaging §56–66)

---

## 1. What This Means

Engineering event-driven workflows means using **AWS messaging and queue services** (EventBridge, SQS, SNS) to enable **reliable, asynchronous communication** between microservices — so they're decoupled, scalable, and resilient to each other's failures.

**Scope:**
- **EventBridge** — serverless event bus for routing events between services by rules
- **SQS** — message queues for buffering work and decoupling producers from consumers
- **SNS** — pub/sub fan-out for notifications and one-to-many communication
- **Designing the workflow topology** — which events flow where, and how services react
- **Reliability** — idempotency, retries, dead-letter queues, ordering when needed

**Why it matters:** in a microservices architecture, synchronous service-to-service calls create tight coupling and cascading failures. Event-driven communication lets services react independently — one service's slowdown or outage doesn't take down the others.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The fan-out pattern (SNS → SQS):**
```
OrderService publishes "OrderCreated"
        │
        ▼
   [SNS Topic]
   /     |     \
  ▼      ▼      ▼
Inventory  Billing  Analytics
 (SQS)     (SQS)    (SQS)
  │         │        │
  ▼         ▼        ▼
Worker   Worker    Worker
```
- `OrderCreated` published **once** → three independent services each get their own copy via SQS subscriptions
- Each service processes at its own pace — billing being slow doesn't block inventory
- Adding a new consumer (e.g., Analytics) is just a new SQS subscription — zero changes to OrderService

**EventBridge for content-based routing:**
- Route `high-value` orders to a priority queue
- Route `international` orders to a compliance-check queue
- Routing is **config-driven** (rules), not code-driven — no producer changes needed

**Real-world scenarios:**
- **Order placed** → Inventory reserves stock, Billing charges, Analytics tracks, Notifications emails
- **User registered** → Welcome email sent, Profile created, Analytics tracked
- **Payment failed** → Retry scheduled, Support notified, Account flagged

**The key decision — when to use which service:**
| Need | Use |
|---|---|
| Buffer work between services | **SQS** |
| Fan-out to many subscribers | **SNS** |
| Route events by content/rules | **EventBridge** |
| Fan-out + buffering (most common) | **SNS → SQS** |

---

## 3. How to Implement

### Pattern 1 — Fan-Out via SNS → SQS

```python
# Publisher — publishes one event to a topic
async def publish_order_created(order: Order):
    await sns.publish(
        TopicArn=ORDER_TOPIC_ARN,
        Message=json.dumps({"event": "OrderCreated", "order": order.dict()}),
    )

# Three SQS queues subscribed to the topic (configured once via IaC/CDK)
# Each queue receives its own copy of every event

# Consumer (Inventory) — processes independently
async def inventory_worker():
    while True:
        messages = await sqs.receive(QueueUrl=INVENTORY_QUEUE, MaxNumberOfMessages=10)
        for msg in messages:
            order = json.loads(msg["body"])
            if order["event"] == "OrderCreated":
                await reserve_stock(order["order"])
            await sqs.delete(QueueUrl=INVENTORY_QUEUE, ReceiptHandle=msg["receiptHandle"])
```

### Pattern 2 — EventBridge Content-Based Routing

```python
# Publisher — sends to the event bus
async def publish_order(order: Order):
    await eventbridge.put_events(Entries=[{
        "Source": "eicra.orders",
        "DetailType": "OrderPlaced",
        "Detail": json.dumps({
            "order_id": order.id,
            "total": order.total,
            "country": order.country,
            "tenant_id": order.tenant_id,
        }),
    }])

# Rules (configured via CDK/Console) route events:
# Rule 1: total > 10000 → priority-queue
# Rule 2: country != "US" → compliance-queue
# Rule 3: all orders → standard-queue

# CDK rule example
rule = eb.Rule(self, "HighValueRule",
    event_pattern=eb.EventPattern(
        source=["eicra.orders"],
        detail={"total": [{"numeric": [">", 10000]}]},
    ))
rule.add_target(targets.SqsQueue(priority_queue))
```

**Why:** routing logic lives in config, not producer code. Adding a new rule doesn't require touching OrderService.

### Pattern 3 — Reliable Consumer (Idempotency + DLQ)

```python
async def reliable_consumer():
    while True:
        messages = await sqs.receive(QueueUrl=QUEUE, MaxNumberOfMessages=10,
                                      VisibilityTimeout=120,
                                      WaitTimeSeconds=20)  # long polling
        for msg in messages:
            event_id = json.loads(msg["body"])["event_id"]

            # 1. Idempotency — skip if already processed
            if await redis.exists(f"processed:{event_id}"):
                await sqs.delete(msg)
                continue

            try:
                # 2. Process
                await process_event(json.loads(msg["body"]))
                # 3. Mark done
                await redis.set(f"processed:{event_id}", "1", ex=86400)
                # 4. Acknowledge
                await sqs.delete(msg)
            except Exception as e:
                # 5. Failure → let retry happen (or DLQ after N attempts)
                logger.error(f"Failed: {e}")
                # (Don't delete — message becomes visible again for retry)
```

### Workflow Design Checklist

- [ ] **Producers are fire-and-forget** — they publish and move on, never wait for consumers
- [ ] **Consumers are idempotent** — at-least-once delivery means duplicates WILL happen
- [ ] **Every queue has a DLQ** — poison messages are captured, not lost
- [ ] **Visibility timeout** matches processing time — too short = reprocessing, too long = stuck messages
- [ ] **Long polling** (`WaitTimeSeconds=20`) — reduces empty receives and cost
- [ ] **Fan-out via SNS→SQS**, not direct service-to-service calls
- [ ] **Content routing via EventBridge rules** — config-driven, not code-driven
- [ ] **Monitor queue depth + DLQ** — growing queue = stuck consumers

### Avoid These

- **Synchronous service calls for events** — `OrderService` calling `BillingService.charge()` directly. Billing down = OrderService down.
- **Non-idempotent consumers** — duplicate events produce duplicate charges/reservations
- **No DLQ** — a poison message retries forever, blocking the queue
- **Wrong visibility timeout** — 30s timeout on a 5-min task means the message redelivers while still processing
- **Using SQS for fan-out** — SQS is one-consumer; use SNS or EventBridge for one-to-many
- **Hardcoding routing in producers** — producers should publish events, not know about every consumer
