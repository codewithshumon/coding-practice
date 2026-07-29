# Cross-Functional Collaboration

> **Category:** Collaboration
> **Relevant at:** All five companies (the only responsibility present in every role)
> **Related tech docs:** `case/leadership/lead-sdlc.md` (SDLC ownership), `case/code-quality/review-code-standards.md` (code review), `case/api/apis-and-communication.md` (integration contracts)

---

## 1. What This Means

Cross-functional collaboration means working **across disciplines** — frontend/backend engineers, QA, DevOps, UI/UX designers, product managers, and infrastructure teams — throughout the full software delivery lifecycle to ensure seamless integration, thorough testing, reliable deployments, and **alignment between business requirements and technical implementation**.

**Scope:**
- **Translating across roles** — turning PM business goals into technical specs; turning technical constraints into business tradeoffs PMs understand
- **Coordinating integration** — backend/frontend contract alignment; DevOps deployment coordination; QA test planning
- **Bridging the gap** — the engineer who understands *both* the technical and the business view is the integration point that makes projects succeed

**Why it matters:** software is built by teams, not individuals. The features that fail usually fail at the *seams* between roles — a frontend that doesn't match the backend contract, a deploy that QA didn't expect, a feature that solves the wrong problem. Cross-functional collaboration is what prevents seam failures.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The collaboration touchpoints across the SDLC:**
```
Requirements  → with PM: clarify the problem, negotiate scope
Design        → with backend/frontend/infra: agree on contracts & architecture
Development   → with other engineers: integrate, review, unblock
Testing       → with QA: define what to test, provide testable features
Deployment    → with DevOps: plan rollout, coordinate release
Support       → with everyone: respond to issues, iterate on feedback
```

**Real-world scenarios:**
- **Backend + frontend contract** → agree on the API shape *before* building, so neither blocks the other (mock the contract)
- **Engineer + PM** → translate "users are confused" into a concrete technical change; explain why a feature takes 2 weeks, not 2 days
- **Engineer + QA** → flag the tricky edge cases to test; provide a testable feature (with flags/staging), not a surprise deploy
- **Engineer + DevOps** → coordinate the deploy window, rollback plan, and monitoring before launch
- **Engineer + Designer** → push back on a design that's technically expensive; propose an alternative that achieves the same UX goal

**The principle:** the engineer who can **speak both languages** — technical and business — becomes the connective tissue that makes cross-functional work succeed. Most project failures are communication failures at the seams.

---

## 3. How to Implement

### Agree on Contracts Early (Backend ⟷ Frontend)

```markdown
## Before either side builds, define the contract:
### POST /api/v1/orders
Request:  { customer_id, items: [{sku, qty}] }
Response: 201 { id, status: "created", total }

# Frontend mocks this immediately; backend builds to it.
# Neither blocks the other. Contract drift caught at integration, not launch.
```

### Translate Between Technical and Business

```markdown
## To the PM (business language):
"This feature needs 2 weeks because we're adding payment processing —
that's security-critical, needs idempotency, and integration tests.
We can ship a simpler version (manual invoicing) in 3 days if the
deadline is tight. Which do you prefer?"

## To the team (technical language):
"PM needs this for the Q3 launch. The core is payment processing;
let's scope the MVP and defer the reporting dashboard."

# The skill: same decision, framed for each audience's concerns.
```

### Coordinate with Each Function

```markdown
## QA: "Here's what to test"
- The critical paths (checkout, payment, login)
- The edge cases (empty cart, expired card, concurrent orders)
- How to reproduce in staging (feature flag X, test data Y)

## DevOps: "Here's the deploy plan"
- Deploy window, staged rollout, rollback command
- What to monitor post-deploy (error rate, latency)
- Who's on call during launch

## Designer: "Here's what's feasible"
- "That animation is GPU-heavy on mobile; here's a lighter alternative
  that achieves the same feel"
- "This layout needs 3 API calls; we can pre-fetch to keep it snappy"
```

### Cross-Functional Checklist

- [ ] **API contracts agreed** before building (no frontend/backend blocking)
- [ ] **PM aligned** on scope, tradeoffs, and timeline (no surprises)
- [ ] **QA informed** of what to test and how to reproduce
- [ ] **DevOps coordinated** on deploy plan, monitoring, rollback
- [ ] **Designer consulted** on technical feasibility (push back early)
- [ ] **Tradeoffs communicated** in the audience's language (technical ↔ business)
- [ ] **Dependencies identified** early (who blocks whom?)
- [ ] **Decisions documented** (not lost to hallway conversations)

### Avoid These

- **Building in a silo** — the backend and frontend integrate for the first time at launch
- **Surprising QA/DevOps** — a deploy they didn't know was coming
- **Technical jargon to PMs** — "we need to refactor the ORM" means nothing to them
- **Saying yes to everything** — no pushback when scope or design is unfeasible
- **Undocumented decisions** — "we agreed in the meeting" that nobody remembers
- **Ignoring dependencies** — your feature blocks three others but you didn't flag it
