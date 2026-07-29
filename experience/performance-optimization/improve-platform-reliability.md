# Improve Platform Reliability

> **Category:** Performance & Optimization
> **Relevant at:** Codixel
> **Related tech docs:** `case/structures-architecture/backend-systems.md` (System Optimization §49–56, Distributed Systems §17–24), `case/structures-architecture/architecture-patterns.md` (Event-Driven §9–16, Microservices §1–8), `case/cloud-service/cloud-platforms.md` (AWS services §45–88)

---

## 1. What This Means

Improving platform reliability means taking a **system-wide view** of performance, scalability, and reliability — continuously profiling across layers, removing bottlenecks, and applying best practices so the **entire platform** stays fast and available as it grows.

**Scope:**
- **End-to-end profiling** — tracing a request across all layers (client → CDN → app → cache → DB → external APIs)
- **System-wide bottleneck removal** — fixing the dominant cost, not just local hotspots (Amdahl's law)
- **Scalability** — ensuring the platform grows without rearchitecture (statelessness, decoupling, horizontal scaling)
- **Reliability patterns** — circuit breakers, graceful degradation, retries, failover, health checks
- **SLOs + error budgets** — defining and measuring what "reliable" means quantitatively

**Why it matters:** this is distinct from local performance tuning (making one endpoint fast). It's about the **whole system staying up and fast under growth and failure** — the difference between "this query is slow" and "the platform survives a 10x traffic spike."

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**End-to-end bottleneck analysis (Amdahl's law):**
```
Trace a request: Client → CDN → App → Redis → Postgres → External API
                                                       ↑
                              if 80% of time is here, optimize HERE first
```
- Local optimization (app code) won't help if the DB or external API dominates
- The biggest system-level gain comes from optimizing the **dominant stage**

**Real-world reliability scenarios:**
- A third-party supplier API goes down → circuit breaker prevents cascading failure; the platform degrades gracefully instead of crashing
- Traffic spikes 5x → stateless services scale out automatically; queues buffer the spike
- A slow query overloads the DB → read replicas absorb read traffic; primary stays healthy
- A microservice fails → event-driven decoupling means others keep working; failed messages sit in a DLQ for recovery

**The reliability model:**
- **SLOs** define the target (e.g., "99.9% of requests < 500ms")
- **Error budgets** balance velocity vs. stability — if you're burning budget, freeze feature work for reliability
- **Graceful degradation** — when something fails, the platform degrades (cached data, fallback responses) rather than errors out

**The principle:** assume **failure is normal** — networks fail, services crash, traffic spikes. Reliability engineering designs the platform to **stay up and degrade gracefully** when components fail.

---

## 3. How to Implement

### End-to-End Profiling

```python
# Distributed tracing (X-Ray, Jaeger, Datadog) shows where time goes across services
@tracer.capture_method
async def process_event(event_id):
    with tracer.subsegment("fetch") as seg:
        event = await db.events.get(event_id)         # how long?
    with tracer.subsegment("classify"):
        result = await llm.classify(event.transcript) # usually the bottleneck
    with tracer.subsegment("publish"):
        await elasticsearch.index(result)
    # Trace shows: classify = 80% of total → optimize there first
```

### Circuit Breakers + Graceful Degradation

```python
breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=30)

async def get_supplier_data(request):
    """Don't let a failing external service take down the platform."""
    if breaker.is_open:
        # Graceful degradation — serve cached/stale data instead of crashing
        cached = await redis.get(f"supplier:{request.id}")
        return cached or FallbackResponse("data temporarily unavailable")

    try:
        result = await supplier_api.fetch(request)
        breaker.record_success()
        await redis.setex(f"supplier:{request.id}", 300, result)  # cache for fallback
        return result
    except (TimeoutError, SupplierError):
        breaker.record_failure()
        return await get_supplier_data(request)  # recursion hits the open-breaker branch
```

### Scalability — Design for Horizontal Growth

```python
# Stateless services — any instance can handle any request (scale out freely)
# State lives in Redis/DB, not in the process
@app.get("/profile")
async def get_profile(user_id: str):
    # No in-memory session — fetch from Redis/DB every time
    return await redis.get(f"session:{user_id}")

# Async decoupling — spikes buffered by queues, not crashing workers
@app.post("/events")
async def ingest(event):
    await sqs.send(event)         # enqueue, respond fast
    return {"status": "queued"}   # workers process at their own pace

# Read replicas — scale reads separately from writes
read_db = Postgres(replica=True)   # analytics/reporting reads
write_db = Postgres(primary=True)  # writes only
```

### SLOs + Error Budgets

```python
# Define measurable reliability targets
SLO = ServiceLevelObjective(
    name="api-latency",
    target=0.999,                    # 99.9% of requests
    condition="latency_p99 < 500ms",
    window=timedelta(days=28),
)
# Error budget = 100% - SLO target = 0.1% of requests can miss the target
# If budget is burning fast → freeze features, focus on reliability
```

### Platform Reliability Checklist

- [ ] **Distributed tracing** across services — know where time/failures occur
- [ ] **Circuit breakers** around external dependencies — their failure isn't yours
- [ ] **Graceful degradation** — cached/fallback data when a dependency fails
- [ ] **Stateless services** — scale horizontally without shared state
- [ ] **Async decoupling** (queues) — spikes buffered, not cascading
- [ ] **Read replicas** for read-heavy load — protect the primary
- [ ] **Retries with backoff + jitter** — recover from transient failures without thundering herds
- [ ] **Health checks + auto-healing** — unhealthy instances replaced automatically
- [ ] **SLOs defined + monitored** — reliability is measured, not assumed
- [ ] **Error budgets tracked** — balance feature velocity vs. stability
- [ ] **DLQs** on every queue — failures captured, not lost
- [ ] **Capacity planning** — know limits before traffic hits them

### Avoid These

- **Optimizing the wrong layer** — app tweaks when the DB or external API dominates
- **No circuit breakers** — one failing dependency cascades into platform-wide outage
- **Stateful services** — can't scale horizontally; one instance's loss loses data
- **Synchronous chains** — A calls B calls C; one slow hop blocks everything
- **No graceful degradation** — a dependency down = errors to every user
- **No SLOs** — "reliable" is undefined; you can't improve what you don't measure
- **Burning error budget without response** — shipping features while reliability degrades
- **Single points of failure** — one DB, one queue, one region with no failover
