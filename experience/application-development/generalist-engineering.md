# Operate as a Generalist Engineer

> **Category:** Application Development
> **Relevant at:** Eicra Soft
> **Related tech docs:** `case/structures-architecture/architecture-patterns.md` (Multi-Tenant SaaS §17–24, Event-Driven §9–16), `case/cloud-service/cloud-platforms.md` (AWS services §45–88), `case/api/apis-and-communication.md` (Third-Party Integrations §49–56)

---

## 1. What This Means

Operating as a generalist engineer means contributing **across the full stack** — internal SaaS product development and custom client integrations — with **equal proficiency** in both. It's the ability to switch context between building a shared multi-tenant platform and building bespoke connectors for a specific customer.

**Scope:**
- **Internal product work:** building and maintaining the core SaaS platform (microservices, APIs, databases, event-driven workflows)
- **Client integration work:** building structured connectors to third-party platforms (ERPs, eCommerce engines, external APIs) that integrate into the SaaS platform
- **Context switching:** moving between deep platform architecture and customer-specific integration code
- **Equal proficiency:** neither side is secondary — both require production-quality, maintainable code

**Why it matters:** SaaS companies that serve enterprise customers inevitably need both — a strong platform AND the ability to integrate with whatever systems the customer already uses. A generalist engineer bridges that gap without requiring separate "platform" and "integration" teams.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**Internal SaaS platform work:**
- Building **multi-tenant microservices** that serve all customers from one codebase
- Designing **event-driven workflows** (EventBridge, SQS, SNS) for async communication
- Managing **shared infrastructure** — caching (Redis), search (OpenSearch), storage (S3)
- Following the **architecture patterns** from `case/structures-architecture/architecture-patterns.md`

**Client integration work:**
- Integrating **ERP systems** — syncing inventory, orders, financial data between the SaaS and customer ERPs
- Connecting **eCommerce engines** — product feeds, order pipelines
- Building **structured connectors** — clean interfaces, error handling, retry logic, idempotency
- Writing **adapter layers** so the core platform stays vendor-agnostic

**The distinguishing skill:** building connectors that are **production-grade** — not one-off scripts. They need logging, monitoring, retry logic, circuit breakers, idempotency, and automated tests — the same quality standards as the core platform.

**The mental model:** the internal platform is the hub; client integrations are spokes. The hub must stay clean and generic; each spoke handles the specifics of one external system. An adapter/anti-corruption layer keeps the two from leaking into each other.

---

## 3. How to Implement

### Internal Platform — High-Quality, Multi-Tenant

```python
# Platform: multi-tenant schema isolation
class OrderService:
    def create_order(self, tenant_id: str, dto: CreateOrderDTO) -> Order:
        with tenant_context(tenant_id):          # scopes all queries to the tenant
            order = Order.create(dto)
            self.publish("OrderCreated", order)  # event-driven
            return order
```

**Key patterns:**
- **Tenant isolation** at the data layer (RLS, schema-per-tenant) — never rely on app filters
- **Event-driven** communication between services (EventBridge/SQS)
- **Caching** at every layer (Redis for hot reads, CDN for static assets)
- **Shared infrastructure** managed as code (IaC — see `case/iac/iac-tools.md`)

### Client Integration — Structured, Resilient

```python
# Integration: connector behind an adapter
class ERPConnector(Protocol):
    async def sync_inventory(self, tenant: str) -> Inventory: ...
    async def push_order(self, order: Order) -> str: ...       # external ID

class SAPAdapter(ERPConnector):          # one per ERP vendor
    def __init__(self, config): ...
    async def sync_inventory(self, tenant: str) -> Inventory:
        raw = await self._call_sap_api(f"/tenants/{tenant}/inventory")
        return self._transform(raw)      # SAP format → platform format

class NetSuiteAdapter(ERPConnector):     # swap without touching platform
    ...
```

**Why the adapter pattern matters:** the platform's `OrderService` depends on `ERPConnector` (the interface), not `SAPAdapter`. Adding a new ERP is a new adapter file, not a platform refactor. See `case/api/apis-and-communication.md` §49–56 for the full integration pattern.

### Resilience Checklist for Every Connector

- [ ] **Retry with exponential backoff** — the external system will fail
- [ ] **Idempotency keys** — safe to retry without duplicates
- [ ] **Circuit breaker** — stop calling when the external system is down
- [ ] **Dead-letter queue** — capture failures for inspection
- [ ] **Logging + alerts** — silent failures become production incidents
- [ ] **Sandbox/testing environment** — never test against a live customer ERP

```python
# Example: resilient API call in a connector
async def _call_sap_api(self, path: str, retries: int = 3):
    for attempt in range(retries):
        try:
            return await self.client.get(path, timeout=30)
        except TimeoutError:
            if attempt == retries - 1: raise
            await asyncio.sleep(2 ** attempt)    # exponential backoff
```

### Context-Switching — Staying Effective

- **Know which mode you're in** — platform engineering and integration coding have different mindsets (broad architecture vs. deep understanding of one external API)
- **Share patterns, not code** — the adapter pattern works for both, but each integration has unique business logic
- **Write integration tests** that run without the real external system — use mocks or recorded responses
- **Document the integration** — the next engineer shouldn't have to reverse-engineer a vendor's API docs

### Avoid These

- **Treating integrations as second-class code** — one-off scripts without tests, logging, or retries
- **Hardcoding vendor logic into the platform** — always use the adapter pattern
- **No circuit breaker** — an unresponsive third-party API shouldn't cascade into platform downtime
- **Testing integrations against live customer systems** — use sandboxes
- **Silent failures** — if an inventory sync fails, someone must know
