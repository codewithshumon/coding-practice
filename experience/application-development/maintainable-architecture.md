# Architect Maintainable Solutions

> **Category:** Application Development
> **Relevant at:** As-Sunnah Foundation, Eicra Soft
> **Related tech docs:** `case/structures-architecture/backend-systems.md` (Backend Architecture §9–16, Software Architecture §33–40), `case/structures-architecture/architecture-patterns.md` (all 4 patterns §1–32), `case/api/apis-and-communication.md` (REST §1–8)

---

## 1. What This Means

Architecting maintainable solutions means making **high-level structural decisions** so a system stays understandable, changeable, and testable over its lifetime — following **industry best practices and modern design patterns**.

**Scope:**
- Choosing architectural patterns (layered, clean, hexagonal, DDD, event-driven, microservices) that fit the domain complexity — not over-engineering simple apps
- Defining **boundaries and contracts** between parts of the system
- Making decisions that are **reversible** — avoiding choices that lock the team into a dead end
- Prioritizing **maintainability** over cleverness: the best architecture is the one the team can reason about

**Why it matters:** code that isn't architected rots — every change becomes harder, bugs multiply, and velocity drops. Good architecture is an investment that compounds.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**Choosing the right pattern for the complexity:**
- **Simple CRUD:** layered architecture (controller → service → repository) is enough. Clean/hexagonal is overkill.
- **Complex business domain:** Clean Architecture or DDD — isolate the domain, invert dependencies.
- **Multiple services:** microservices with event-driven communication.
- **Many customers:** multi-tenant SaaS with schema/row-level isolation.

**Making boundaries real:**
- **Bounded contexts** (DDD) split a large domain into cohesive pieces with clear interfaces.
- **API contracts** between services — versioned, documented, tested.
- **Third-party isolation** — every external vendor behind an adapter so swapping Stripe→PayPal doesn't rewrite business logic.

**Keeping options open:**
- **Delay irreversible decisions** until you have more information.
- **Ports & adapters** let you swap databases, frameworks, and delivery mechanisms later.
- **Modular monoliths** start simple and can split into microservices when the boundaries harden.

**The litmus test:** can a junior developer add a new feature without breaking three unrelated things? If not, the architecture needs attention.

---

## 3. How to Implement

### Step 1 — Match the Pattern to the Complexity

```
Simple CRUD → layered (controller/service/repository)
Domain-heavy → clean/hexagonal (domain at center)
Multi-service → microservices + event-driven
Multi-customer → multi-tenant (schema-per-tenant or RLS)
```

Don't use microservices for a team of 3 on a simple app. Don't use raw layered architecture for a complex insurance underwriting system.

### Step 2 — Draw the Boundaries

```python
# Port (interface) — in the domain, no framework import
class PaymentGateway(Protocol):
    def charge(self, amount: Decimal) -> bool: ...

# Adapter (implementation) — in infrastructure layer
class StripeGateway:
    def charge(self, amount: Decimal) -> bool:
        return stripe.Charge.create(amount=amount)
```

**Rule:** the domain defines *what* it needs (the port); infrastructure provides *how* (the adapter). The domain never imports Stripe.

### Step 3 — Make Contracts Explicit

- **Internal:** typed interfaces (Protocol, abstract classes, TypeScript interfaces)
- **Between services:** versioned REST/event schemas, documented in OpenAPI/AsyncAPI
- **With third parties:** adapter layer with integration tests (see `case/api/apis-and-communication.md` §49–56)

### Step 4 — Organize by Feature, Not by Layer

```
# Bad: folders by technical layer
/controllers  /services  /repositories  /models

# Good: folders by business capability
/orders/  OrdersController, OrdersService, OrdersRepo, Order
/users/   UsersController, UsersService, UsersRepo, User
```

**Why:** related code stays together. You can extract `/orders/` into its own service later without hunting through 4 folders.

### Step 5 — Continuously Improve

- **Refactor as you go** — architecture isn't set in stone. As patterns emerge, restructure.
- **Review architecture in PRs** — not just code correctness, but "does this belong here?"
- **Track technical debt** — make it visible, prioritize it alongside features.

### Cross-Framework Checklist

- [ ] Architecture complexity matches domain complexity (no over/under-engineering)
- [ ] Boundaries are explicit (interfaces, contracts, bounded contexts)
- [ ] Third-party code is behind adapters
- [ ] Key decisions are **reversible** or have migration paths
- [ ] Code is organized by business capability, not technical layer
- [ ] Architecture is discussed and reviewed, not assumed

### Avoid These

- **Resume-driven architecture:** picking microservices/CQRS/event-sourcing because they're trendy
- **No boundaries:** every module imports every other module — impossible to change
- **Leaky abstractions:** the domain imports `@nestjs/core` or `django.db.models` directly
- **Anemic domain:** empty objects with all logic in services — the database with extra steps
- **Premature microservices:** splitting before business boundaries are clear produces a distributed monolith
