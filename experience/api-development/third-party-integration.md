# Integrate Third-Party APIs

> **Category:** API Development & Integration
> **Relevant at:** Impressive Security (travel suppliers, payment gateways, airline systems), MVI Solutions (payments, CRMs, shipping providers)
> **Related tech docs:** `case/api/apis-and-communication.md` (Third-Party Integrations §49–56, REST §1–8, JSON §33–40, XML §41–48), `case/security/security-and-auth.md` (API Security §1–8)

---

## 1. What This Means

Integrating third-party APIs means connecting your application to **external vendor systems** — payment gateways, CRMs, shipping providers, travel suppliers, partner services — via REST, JSON, XML, and webhooks.

**Scope:**
- **Outbound:** calling vendor APIs (charge a payment, search flights, ship a package)
- **Inbound:** receiving vendor webhooks (payment confirmed, booking updated, shipment delivered)
- Format diversity: modern JSON APIs AND legacy XML/SOAP APIs from older systems
- **Resilience:** vendors are unreliable — you must handle timeouts, rate limits, and failures gracefully

**Why it matters:** your application's reliability is only as good as its weakest integration. A payment gateway outage shouldn't take your entire checkout flow down.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**Payment Gateways (Impressive Security, MVI Solutions):**
- Charging cards, processing refunds, handling webhooks
- **Idempotency is critical** — duplicate charges are unacceptable
- Webhook signature verification — you must prove the payload came from the payment provider

**Travel Suppliers (Impressive Security):**
- Searching flights, booking, ticketing across multiple supplier APIs (GDS, NDC, OTAs)
- Each supplier has a different API format — normalization into a common model is essential
- Real-time availability and pricing — caching needs careful TTL management

**CRMs & Shipping (MVI Solutions):**
- Syncing customer data with CRMs
- Rate quoting, label generation, tracking from shipping carriers
- Often XML/SOAP-based (legacy) — requires different parsing, namespaces, XSD validation

**JSON vs XML integration:**
- Modern APIs (Stripe, Twilio) → JSON, clean SDKs
- Legacy systems (older payment/ERP/shipping) → XML/SOAP, verbose, namespace-heavy
- Both need the same resilience patterns regardless of format

---

## 3. How to Implement

### The Adapter Pattern — Universal for All Integrations

```python
# Your interface — lives in your domain, knows nothing about the vendor
class PaymentGateway(Protocol):
    async def charge(self, amount: Decimal, token: str, idempotency_key: str) -> ChargeResult: ...

# Vendor adapter — lives in infrastructure, only this file imports Stripe
class StripeAdapter(PaymentGateway):
    async def charge(self, amount: Decimal, token: str, idempotency_key: str) -> ChargeResult:
        try:
            charge = stripe.Charge.create(
                amount=int(amount * 100),
                source=token,
                idempotency_key=idempotency_key,   # Stripe handles dedup
            )
            return ChargeResult(success=True, tx_id=charge.id)
        except stripe.error.CardError as e:
            return ChargeResult(success=False, error=str(e))
```

**Why:** the checkout service depends on `PaymentGateway` (your interface), not Stripe. Swap to PayPal by writing a `PayPalAdapter` — zero changes to business logic.

### XML/SOAP Integration — Handling Legacy Formats

```python
# XML-based shipping API
class FedExAdapter(ShippingProvider):
    async def get_rates(self, package: Package) -> list[Rate]:
        # Build SOAP envelope
        request_xml = self._build_rate_request(package)
        response = await self.client.post(self.endpoint, content=request_xml,
                                          headers={"Content-Type": "text/xml"})
        # Parse XML response with namespace handling
        return self._parse_rate_response(response.text)

    def _parse_rate_response(self, xml_str: str) -> list[Rate]:
        root = ET.fromstring(xml_str)
        ns = {"ns": "http://fedex.com/ws/rate/v26"}
        rates = []
        for entry in root.findall(".//ns:RateReplyDetails", ns):
            rates.append(Rate(
                service=entry.find("ns:ServiceType", ns).text,
                amount=Decimal(entry.find(".//ns:Amount", ns).text),
            ))
        return rates
```

**Why:** the adapter handles the XML misery — the application doesn't know or care if the shipping provider speaks SOAP.

### Webhook Receiver — Verify Then Process

```python
@router.post("/webhooks/payment")
async def payment_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("x-signature")

    # 1. Verify the webhook came from the provider
    if not verify_hmac(payload, signature, WEBHOOK_SECRET):
        raise HTTPException(status_code=401)

    # 2. Process idempotently (webhooks redeliver)
    event = json.loads(payload)
    existing = await db.find_by_webhook_id(event["id"])
    if existing:
        return {"status": "already_processed"}

    # 3. Handle the event
    await handle_payment_event(event)
    await db.save_webhook_id(event["id"])
    return {"status": "ok"}
```

**Why:** signature verification prevents spoofed webhooks. Idempotent processing prevents duplicate handling when the provider redelivers.

### Resilience for All Integrations

```python
# Every outbound call needs this
async def call_vendor_api(request, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await client.post(url, data=request, timeout=10)
        except (TimeoutError, ConnectionError):
            if attempt == max_retries - 1:
                raise VendorUnavailableError(vendor)
            await asyncio.sleep(2 ** attempt)

# Circuit breaker — stop calling when it's clearly down
breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=60)

async def safe_vendor_call(request):
    if not breaker.is_open:
        result = await call_vendor_api(request)
        breaker.record_success()
        return result
    else:
        return fallback_response()   # graceful degradation
```

### Integration Checklist

- [ ] Vendor behind an adapter/interface — never direct imports in business logic
- [ ] **Idempotency keys** on every write (charges, shipments, bookings)
- [ ] **Webhook signatures verified** — never process unverified payloads
- [ ] **Circuit breaker** — the vendor's outage is not your outage
- [ ] **Retry with exponential backoff** — transient failures recover
- [ ] Both JSON and XML handled with equivalent resilience
- [ ] Sandbox/test environment used during development
- [ ] Logging + alerts on integration failures

### Avoid These

- **No adapter layer** — Stripe/PayPal imports scattered through business code. Changing processors rewrites the system.
- **Unverified webhooks** — anyone can POST to your webhook endpoint
- **Non-idempotent payment processing** — a retry produces a double charge
- **No circuit breaker** — payment gateway down = your whole checkout down
- **Calling vendor APIs directly in tests** — hitting live payment/test systems from CI
