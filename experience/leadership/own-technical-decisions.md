# Own Technical Decisions

> **Category:** Technical Leadership
> **Relevant at:** As-Sunnah Foundation
> **Related tech docs:** `case/structures-architecture/architecture-patterns.md` (maintainable architecture), `case/code-quality/write-quality-code.md`, `case/operations/handle-maintenance-legacy.md` (tech debt), `case/devops/devops-and-cicd.md` (developer experience — CI/CD)

---

## 1. What This Means

Owning technical decisions means taking **accountability for the architecture and technical direction** of a system — continuously improving it, **reducing technical debt**, and **enhancing developer experience (DX)** so the codebase stays healthy and the team stays productive.

**Scope:**
- **Technical decisions** — choosing patterns, tools, and approaches (and living with the consequences)
- **Architecture improvement** — evolving the system as it grows and requirements change
- **Technical debt reduction** — paying down accumulated shortcuts before they cripple velocity
- **Developer experience** — making the codebase and tooling a joy (not a chore) to work in

**Why it matters:** without ownership, technical decisions happen by accident — each PR adds a little debt, tools rot, and the codebase slowly becomes painful to change. Ownership keeps the system **intentionally healthy**, balancing feature delivery with the long-term viability of the codebase.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The three balances ownership requires:**
```
Feature delivery  ⟷  Technical debt reduction
Moving fast       ⟷  Sustainable architecture
What's needed now ⟷  What the system will need
```

**Real-world decisions an owner makes:**
- A quick hack ships a feature fast → the owner schedules debt repayment (a tracked ticket, not "later")
- The codebase has no tests → the owner prioritizes testing infrastructure (even over features)
- Builds take 10 minutes → the owner invests in CI speed (DX) because slow feedback hurts everyone
- A pattern is emerging across features → the owner extracts it into a shared, tested abstraction
- A framework is end-of-life → the owner plans the migration before it's an emergency

**The technical-debt reality:**
- Debt isn't evil — it's a tool (ship now, pay later). The problem is **untracked, unpaid** debt.
- An owner **makes debt visible** (tracked, prioritized) and **pays it down deliberately** — alongside features, not "when we have time" (which never comes).

**The DX reality:**
- Developer experience is a **multiplier** — fast builds, good tooling, clear docs, easy local setup make the whole team faster.
- An owner treats DX as a first-class concern, not an afterthought.

---

## 3. How to Implement

### Make Technical Decisions Deliberately (and Record Them)

```markdown
## Architecture Decision Record (ADR)
### Title
Use event-driven messaging between order and billing services.

### Context
Order and billing are tightly coupled; billing outages block orders.

### Decision
Decouple via SQS — order publishes, billing consumes async.

### Consequences
+ Billing outages no longer block orders
+ Independent scaling
- Eventual consistency (orders may briefly show "pending")
- Added operational complexity (DLQ, monitoring)

### Alternatives Considered
- Direct sync calls (rejected: cascading failures)
- Shared DB (rejected: distributed monolith)
```

**Why:** decisions are recorded, not lost to Slack history. The next developer understands *why*, not just *what*.

### Track & Prioritize Technical Debt

```markdown
## Tech Debt Register (visible, prioritized)
| Debt | Impact | Effort | Priority |
|---|---|---|---|
| No tests on pricing module | Can't refactor safely | M | High |
| Django 3.2 (EOL soon) | Security risk | L | High |
| Monolithic auth service | Hard to scale | XL | Medium |
| Inconsistent error handling | Debugging pain | S | Low |

## Rule: allocate ~20% of every sprint to debt repayment
# Don't let features consume 100% — debt compounds silently
```

### Reduce Debt Through Refactoring

```python
# The "boy scout rule" — leave the code better than you found it
# When touching a module for a feature, fix nearby debt too:

def add_tiered_pricing():
    # FEATURE: new tiered pricing
    ...
    # DEBT (opportunistically): extract the duplicated discount logic
    # you're already here, tests are already running — fix it now
```

### Improve Developer Experience (DX)

```markdown
## DX investments that multiply team productivity:
- **Fast CI** — feedback in minutes, not 20 min (parallelize, cache)
- **Easy local setup** — one command (`docker compose up`) to run everything
- **Good docs** — architecture, patterns, "how to add a feature"
- **Linting/formatting automated** — no style debates in review
- **Helpful error messages** — debug faster
- **Type safety** — catch bugs before runtime
# DX is not "nice to have" — it's leverage. A team blocked by tooling ships slowly.
```

### Continuous Architecture Improvement

```markdown
## Regular architecture reviews (not just at project start):
- What's working well? (keep doing it)
- What's causing pain? (where's the friction?)
- What's the biggest risk? (what will hurt us in 6 months?)
- What debt is accruing? (what needs paying down?)
# Architecture is a living thing — revisit it, don't set-and-forget
```

### Own Technical Decisions Checklist

- [ ] **Decisions recorded** (ADRs) — rationale preserved, not lost to chat
- [ ] **Tech debt visible** — tracked register, prioritized, not hidden
- [ ] **Debt repayment allocated** (~20% per sprint) — features don't consume 100%
- [ ] **Boy scout rule applied** — leave code better than found
- [ ] **DX treated as first-class** — fast CI, easy setup, good docs
- [ ] **Architecture reviewed regularly** — not set-and-forget
- [ ] **Tradeoffs made explicitly** — "we're taking this debt for X reason"
- [ ] **Reversibility considered** — prefer decisions you can undo

### Avoid These

- **Decisions by accident** — patterns emerging without anyone choosing them
- **Untracked debt** — "we'll fix it later" (later never comes)
- **Features consuming 100%** — debt compounds until velocity collapses
- **No ADRs** — "why did we do this?" with no answer; repeated debates
- **Ignoring DX** — slow builds, painful setup; the whole team drags
- **Set-and-forget architecture** — the system outgrew the design but nobody updated it
- **Rewrites over incremental improvement** — "burn it down" is rarely the right call
