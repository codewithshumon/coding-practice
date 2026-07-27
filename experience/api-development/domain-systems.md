# Develop Domain Systems

> **Category:** API Development & Integration
> **Relevant at:** Impressive Security (flight booking engines, payment processing, supplier connectivity), Codixel (event-driven financial data pipelines — discovery → scraping → classification → publishing)
> **Related tech docs:** `case/structures-architecture/architecture-patterns.md` (Event-Driven §9–16, Microservices §1–8), `case/messaging/message-queues.md` (Queues & Pub/Sub §1–11), `case/media/media-processing.md` (Playwright §12–22, WhisperX §1–11, FFmpeg §23–33), `case/database/databases.md` (Elasticsearch §34–44)

---

## 1. What This Means

Developing domain systems means building **end-to-end backend subsystems** for specific business domains — not generic CRUD, but specialized processing engines that handle complex domain logic, real-time data flows, and high reliability requirements.

**Scope:**
- **Travel domain systems:** flight booking engines, payment processing modules, supplier connectivity layers that orchestrate multiple airline/hotel APIs
- **Financial data pipelines:** event-driven systems that discover, scrape, classify, and publish real-time financial news at scale
- Both require deep understanding of the **domain rules** (how booking works, what constitutes a financial event) and **production engineering** (pipeline reliability, error recovery, throughput)

**Why it matters:** domain systems are the core IP of a business. A flight booking engine IS the travel company's product. A financial data pipeline IS the earnings-call platform. Getting them right isn't a nice-to-have — it's the business.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

### Travel Domain Systems (Impressive Security)

**Flight Booking Engine:**
- Orchestrates a multi-step workflow: search → select → price → book → ticket → confirm
- Must be **transactional** — a booking either completes fully or rolls back
- Calls multiple external systems: airline APIs (GDS/NDC), payment gateways, notification services
- **Compensating transactions** (saga pattern) — if payment fails after booking, cancel the booking

**Payment Processing Module:**
- Handles authorization, capture, refund, and reconciliation
- Must be **idempotent** — double-charging is unacceptable
- Integrates with payment gateways behind an adapter layer

**Supplier Connectivity Layer:**
- Normalizes different airline/hotel API formats into a unified model
- Each supplier speaks a different "language" — GDS, NDC, OTA, direct APIs
- The layer translates between supplier format ↔ unified model

### Financial Data Pipeline (Codixel)

**End-to-end flow:**
```
Discovery → Scraping → Transcription → Classification → Publishing
   │           │            │                │             │
(Cron)    (Playwright)  (WhisperX)      (LLM/ML)     (Elasticsearch)
   │           │            │                │             │
[Scheduler] [Browser]  [GPU Workers]   [AI Models]   [Search Index]
```

**Each stage is a production subsystem:**
- **Discovery:** scheduled jobs find new financial events to process
- **Scraping:** Playwright records live earnings-call webcasts from various sources at scale
- **Transcription:** WhisperX processes GPU-accelerated, word-level transcription with speaker diarization (see `case/media/media-processing.md`)
- **Classification:** LLMs (OpenAI/Claude/Gemini) classify, extract entities, and categorize events
- **Publishing:** results indexed in Elasticsearch, served via search APIs

**Reliability at scale:**
- Hundreds of events daily — pipeline must handle volume without data loss
- Each stage has retry + dead-letter handling
- Queue-based (SQS) decoupling so a slowdown in transcription doesn't block discovery

---

## 3. How to Implement

### Pattern A — Travel Transaction (Saga)

```python
class FlightBookingSaga:
    """Orchestrates a multi-step booking with compensating actions."""

    async def book(self, request: BookingRequest) -> BookingResult:
        steps = [
            SagaStep(
                action=lambda: self._reserve_seats(request),
                compensate=lambda: self._release_seats(result),
            ),
            SagaStep(
                action=lambda: self._charge_payment(request),
                compensate=lambda: self._refund_payment(result),
            ),
            SagaStep(
                action=lambda: self._issue_ticket(result),
                compensate=lambda: self._void_ticket(result),
            ),
        ]
        return await SagaExecutor(steps).execute()

class SagaExecutor:
    async def execute(self, steps: list[SagaStep]) -> SagaResult:
        completed = []
        try:
            result = None
            for step in steps:
                result = await step.action()
                completed.append(step)
            return BookingResult(success=True, data=result)
        except Exception:
            # Rollback in reverse order
            for step in reversed(completed):
                try: await step.compensate()
                except Exception as e: logger.error(f"Compensation failed: {e}")
            raise
```

**Why:** each step has an undo. If ticketing fails after charging, the payment is refunded and seats are released — the system returns to a clean state.

### Pattern B — Supplier Connectivity (Adapter Layer)

```python
# Each supplier has its own adapter
class AmadeusAdapter(FlightSupplier):
    async def search(self, criteria: SearchCriteria) -> list[Flight]:
        raw = await self._call_gds("Flight_Search", self._to_amadeus_format(criteria))
        return [self._to_unified_model(r) for r in raw]

class NDCAdapter(FlightSupplier):
    async def search(self, criteria: SearchCriteria) -> list[Flight]:
        raw = await self._call_ndc_api(self._to_ndc_xml(criteria))
        return [self._to_unified_model(r) for r in raw]

# The booking engine depends on the abstraction
class FlightSearchService:
    def __init__(self, suppliers: list[FlightSupplier]):
        self.suppliers = suppliers

    async def search_all(self, criteria: SearchCriteria) -> list[Flight]:
        results = await asyncio.gather(*[s.search(criteria) for s in self.suppliers])
        return self._dedupe_and_rank(flatten(results))
```

### Pattern C — Event-Driven Data Pipeline

```python
# Pipeline stage: discovery → scraping
async def discover_and_scrape():
    events = await discovery_service.find_upcoming_events()
    for event in events:
        await sqs.send(ScrapeRequest(event_id=event.id, url=event.webcast_url))

# Pipeline stage: scraping → transcription
async def scrape_worker():
    while True:
        msgs = await sqs.receive(max=10)
        for msg in msgs:
            recording = await playwright_recorder.capture(msg.url)
            audio = await ffmpeg.extract_audio(recording)      # see case/media/
            await sqs.send(TranscribeRequest(event_id=msg.event_id, audio_path=audio))
            await sqs.delete(msg)

# Pipeline stage: transcription → classification
async def transcribe_worker():
    while True:
        msgs = await sqs.receive(max=5)
        for msg in msgs:
            transcript = whisperx.transcribe(msg.audio_path, diarize=True)
            await sqs.send(ClassifyRequest(event_id=msg.event_id, transcript=transcript))
            await sqs.delete(msg)

# Pipeline stage: classification → publishing
async def classify_worker():
    while True:
        msgs = await sqs.receive(max=10)
        for msg in msgs:
            classified = await llm.classify(msg.transcript)
            await elasticsearch.index(classified)               # see case/database/
            await sqs.delete(msg)
```

**Why queue-based:** each stage runs at its own pace, independently scalable, resilient to individual stage failures.

### Domain System Checklist

- [ ] Each domain system is **self-contained** with clear inputs and outputs
- [ ] **Multi-step transactions** use sagas with compensating actions
- [ ] **External systems abstracted** behind adapters (supplier APIs, payment gateways)
- [ ] **Pipeline stages decoupled** via queues (SQS/SNS)
- [ ] Each stage has **retry + dead-letter** handling
- [ ] **Idempotent** processing at every stage
- [ ] Monitoring per stage (throughput, error rate, latency)

### Avoid These

- **Tight coupling to supplier APIs** — a supplier change rewrites the booking engine
- **Monolithic pipeline** — a failure in transcription shouldn't block discovery
- **No compensation in transactions** — a partial booking is worse than a failed one
- **Silent pipeline failures** — a stage silently stops and data stops flowing
- **Non-idempotent processing** — a retry after a network blip produces duplicate classifications
