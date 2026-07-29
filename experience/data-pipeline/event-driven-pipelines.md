# Build Event-Driven Data Pipelines

> **Category:** Data Pipeline & Processing
> **Relevant at:** Codixel (financial news discovery → scraping → classification → publishing)
> **Related tech docs:** `case/structures-architecture/architecture-patterns.md` (Event-Driven §9–16, Microservices §1–8), `case/messaging/message-queues.md` (Queues & Pub/Sub §1–11, BullMQ §34–44), `case/cloud-service/cloud-platforms.md` (AWS Messaging §56–66), `case/media/media-processing.md` (full pipeline §1–33)

---

## 1. What This Means

Building event-driven data pipelines means designing systems that process real-time data **end-to-end** — from discovery through scraping, classification, and publishing — using **decoupled stages** connected by queues and event buses.

**Scope:**
- **Discovery** — finding new data sources/events to process (scheduled, webhook-triggered, or continuous)
- **Ingestion/scraping** — capturing the raw data reliably and at scale
- **Processing** — transforming, classifying, enriching, or transcribing the raw data
- **Publishing** — making results available to consumers (search index, API, downstream services)
- **Decoupled architecture** — each stage is independent, communicates via events/queues, scales and fails independently

**Why it matters:** a pipeline is only as reliable as its weakest stage. If discovery, scraping, and classification are tightly coupled, a slowdown in one stage blocks everything — and a failure loses data. Event-driven decoupling is what makes the pipeline resilient at scale.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The Codixel financial-news pipeline:**
```
Discovery → Scraping → Transcription → Classification → Publishing
   │           │            │                │             │
(cron)    (Playwright)  (WhisperX)       (LLM/ML)    (Elasticsearch)
   │           │            │                │             │
[Scheduler] [Browser]  [GPU Workers]    [AI Models]   [Search Index]
```

**Each stage is a separate, independently-deployable worker:**
- **Discovery:** scheduled jobs find upcoming earnings calls / financial events
- **Scraping:** Playwright records live webcasts from various sources (see `event-driven-pipelines` neighbor files)
- **Transcription:** WhisperX does GPU-accelerated word-level transcription with speaker diarization
- **Classification:** LLMs classify, extract entities, categorize events
- **Publishing:** results indexed in Elasticsearch and served via search APIs

**Why queue-decoupled (SQS/SNS/EventBridge):**
- Each stage runs at its own pace — transcription (slow, GPU-bound) doesn't block discovery (fast)
- Stages scale independently — more GPU workers for transcription, more CPU for classification
- Failures are isolated — a crash in classification doesn't stop discovery
- Spikes are buffered — a burst of events queues up instead of overwhelming workers

**The pipeline reliability model:**
- Every message has retry + dead-letter queue (DLQ)
- Idempotent processing — a redelivered message doesn't create duplicates
- Per-stage monitoring — throughput, error rate, latency, queue depth
- A failed message sits in the DLQ for inspection, not silently dropped

---

## 3. How to Implement

### The Decoupled Pipeline Pattern

```python
# Each stage is an independent worker consuming from one queue, producing to the next

# Stage 1: Discovery → emits scrape jobs
async def discover_events():
    events = await calendar_service.find_upcoming_earnings_calls()
    for event in events:
        await sqs.send(QueueUrl=SCRAPE_QUEUE,
                       MessageBody=json.dumps({"event_id": event.id, "url": event.webcast_url}))

# Stage 2: Scraping worker — consumes scrape queue, produces transcribe queue
async def scrape_worker():
    while True:
        messages = await sqs.receive(QueueUrl=SCRAPE_QUEUE, MaxNumberOfMessages=10,
                                      VisibilityTimeout=300)  # Playwright needs time
        for msg in messages:
            try:
                recording = await playwright_recorder.capture(json.loads(msg["body"])["url"])
                audio = await ffmpeg.extract_audio(recording)
                await sqs.send(QueueUrl=TRANSCRIBE_QUEUE,
                               MessageBody=json.dumps({"event_id": ..., "audio_path": audio}))
                await sqs.delete(QueueUrl=SCRAPE_QUEUE, ReceiptHandle=msg["receiptHandle"])
            except Exception as e:
                await handle_failure(msg, e)  # retry or DLQ

# Stage 3, 4, 5 follow the same shape, each specialized
```

**Why:** each worker is a small, focused, independently-deployable service. Adding capacity to transcription (more GPU workers) doesn't touch discovery or classification.

### Dead-Letter Queue (DLQ) — Failure Handling

```python
async def handle_failure(message: dict, error: Exception):
    """Route poison messages to DLQ, not lose them."""
    receive_count = int(message["attributes"]["ApproximateReceiveCount"])
    if receive_count >= MAX_RETRIES:
        # Move to DLQ for manual inspection
        await sqs.send(QueueUrl=DLQ_QUEUE, MessageBody=message["body"],
                       MessageAttributes={"error": str(error), "stage": "scraping"})
        await sqs.delete(message)  # remove from main queue
        await alert_ops(f"Message moved to DLQ: {error}")
    # else: let it become visible again for retry
```

### Idempotency — Safe Retries

```python
async def classify_worker():
    messages = await sqs.receive(QueueUrl=CLASSIFY_QUEUE, MaxNumberOfMessages=10)
    for msg in messages:
        event_id = json.loads(msg["body"])["event_id"]

        # Idempotency check — have we already classified this event?
        if await redis.exists(f"classified:{event_id}"):
            await sqs.delete(msg)  # already done — don't reprocess
            continue

        transcript = json.loads(msg["body"])["transcript"]
        classification = await llm.classify(transcript)
        await elasticsearch.index(event_id, classification)
        await redis.set(f"classified:{event_id}", "1", ex=86400)  # mark done

        await sqs.delete(msg)
```

**Why:** SQS delivers **at-least-once** — if a worker crashes after indexing but before deleting, the message redelivers and re-classifies. The idempotency key (`event_id`) prevents duplicate work and duplicate published data.

### EventBridge — Content-Based Routing

```python
# EventBridge routes events by content, not just to a fixed queue
async def publish_classification(event_id: str, classification: dict):
    await eventbridge.put_events(Entries=[{
        "Source": "pipeline.classification",
        "DetailType": "EventClassified",
        "Detail": json.dumps({
            "event_id": event_id,
            "category": classification["category"],
            "urgency": classification["urgency"],
        }),
    }])

# Rules route high-urgency events to a priority queue, others to standard
# No producer code change needed — routing is config-driven
```

### Pipeline Monitoring Checklist

- [ ] **Per-stage throughput** — events processed per minute (detect slowdowns)
- [ ] **Queue depth** — growing queue = consumer can't keep up
- [ ] **Error rate** per stage — isolated failure detection
- [ ] **DLQ depth + alerts** — never silently fill
- [ ] **End-to-end latency** — discovery to publishing (catches bottlenecks)
- [ ] **Idempotency key tracking** — confirm dedup is working

### Avoid These

- **Synchronous pipeline** — discovery calls scraping which calls classification inline. One slow stage blocks everything.
- **No DLQ** — poison messages vanish or retry forever
- **Non-idempotent processing** — retries produce duplicate published data
- **Monolithic worker** — one service doing discovery + scraping + transcription. Can't scale stages independently.
- **No monitoring** — a stage silently stops processing and data stops flowing for hours
- **Skipping idempotency** — "at-least-once delivery" means duplicates WILL happen
