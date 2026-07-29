# Maintain Test Suites

> **Category:** Code Quality & Testing
> **Relevant at:** As-Sunnah Foundation
> **Related tech docs:** `case/devops/devops-and-cicd.md` (CI/CD §23–33, GitHub Actions §34–44), `case/framework/nextjs/app-router-and-rendering.md`

---

## 1. What This Means

Maintaining test suites means writing and sustaining **unit, integration, and end-to-end tests** using modern frameworks — so the application is **reliable** (bugs caught before production) and **maintainable** (safe to change without fear of regressions).

**Scope:**
- **Unit tests** — test individual functions/modules in isolation (fast, many)
- **Integration tests** — test components working together (DB, APIs, services)
- **End-to-end (E2E) tests** — test full user flows through the real application (slow, few)
- **Test pyramid** — the right balance: many unit, some integration, few E2E
- **Maintenance** — keeping tests fast, reliable (not flaky), and meaningful (not just coverage)

**Why it matters:** tests are a **safety net** that enables change. Without them, every modification is risky — you don't know what you've broken. With them, you refactor confidently, catch bugs early (when they're cheap), and document expected behavior.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The test pyramid (the guiding model):**
```
        E2E          few, slow, whole-system (Playwright, Cypress)
       /     \
   Integration     some, medium, components together (DB + service)
   /           \
Unit  Unit  Unit  Unit   many, fast, isolated functions/modules
```
- **Unit** — the foundation: fast, precise, run on every save
- **Integration** — catches wiring bugs (does the service talk to the DB correctly?)
- **E2E** — catches flow bugs (can a user actually complete checkout?) — but expensive

**Real-world decisions:**
- A bug slips to production → **add a regression test** so it never returns
- Tests are slow → devs skip running them → **move heavy tests out of the pre-commit path**
- A test fails randomly (flaky) → **fix it immediately** — flaky tests erode trust in the whole suite
- Coverage is 90% but bugs still ship → **coverage ≠ quality** — test the *right things* (edge cases, not trivial getters)

**The principle:** tests should be **fast, reliable, and meaningful**. A slow, flaky, or trivial test suite is worse than no tests — it gives false confidence and wastes time.

---

## 3. How to Implement

### Unit Tests — Isolated, Fast, Precise

```python
# Test pure functions/logic in isolation — mock external dependencies
def test_calculate_order_total_applies_discount():
    items = [OrderItem(price=100, qty=2), OrderItem(price=50, qty=1)]
    total = calculate_order_total(items, discount=0.1)
    assert total == Decimal("225.00")   # (100*2 + 50) * 0.9

# Test edge cases, not just happy paths
def test_calculate_order_total_rejects_negative_price():
    with pytest.raises(ValueError):
        calculate_order_total([OrderItem(price=-10, qty=1)])
```

### Integration Tests — Components Together

```python
# Test service + DB together (use a real test DB, not mocks)
@pytest.mark.asyncio
async def test_order_service_persists_to_db(test_db):
    service = OrderService(repo=OrderRepo(test_db))
    order = await service.create(CreateOrderDTO(customer_id="42", items=[...]))

    persisted = await test_db.orders.find_by_id(order.id)
    assert persisted.status == "created"
    assert persisted.total == order.total
```

### E2E Tests — Full User Flows

```typescript
// Playwright — test the real application through the browser
test("user can complete checkout", async ({ page }) => {
  await page.goto("/cart");
  await page.click("text=Checkout");
  await page.fill("[name=email]", "test@example.com");
  await page.fill("[name=card]", "4242424242424242");
  await page.click("text=Pay");
  await expect(page.locator(".confirmation")).toBeVisible();
});
```

### What to Test (and What Not To)

```
TEST:                          DON'T TEST (trivial/low-value):
- Business logic               - Getters/setters
- Edge cases & error paths     - Framework internals
- Boundary conditions          - Third-party libraries
- Critical user flows (E2E)    - 100% coverage for its own sake
- Regressions (bug → test)     - Implementation details (test behavior)
```

### Test Suite Maintenance

```yaml
# CI: run fast tests on every PR, full suite (incl. E2E) on merge
jobs:
  unit-integration:        # ~2 min — blocks PR merge
    steps: [pytest -m "not e2e"]
  e2e:                     # ~10 min — runs on merge to main
    steps: [playwright test]

# Fix flaky tests immediately — quarantine if needed, but don't ignore
# Measure: test duration, flakiness rate, coverage of critical paths
```

### Test Suite Checklist

- [ ] **Test pyramid balanced** — many unit, some integration, few E2E
- [ ] **Unit tests run in seconds** — devs run them constantly
- [ ] **E2E covers critical flows** (login, checkout, core workflows)
- [ ] **Edge cases + error paths tested** — not just happy paths
- [ ] **No flaky tests** (or they're quarantined + fixed fast)
- [ ] **Tests run in CI** — blocking on PR before merge
- [ ] **Bugs get regression tests** — never the same bug twice
- [ ] **Coverage measured on critical paths** — not vanity 100%
- [ ] **Tests are independent** — order doesn't matter; one failure doesn't cascade

### Avoid These

- **Ice-cream cone (all E2E, no unit)** — slow, flaky, hard to localize failures
- **Testing implementation details** — breaks on refactors even when behavior is correct
- **Flaky tests ignored** — erodes trust; devs stop believing failures
- **100% coverage as the goal** — testing trivial code wastes time
- **No integration tests** — wiring bugs (service ↔ DB) slip through
- **Tests depend on order** — one failure cascades; can't run in isolation
- **Not testing error paths** — the happy path works; the error handler crashes
