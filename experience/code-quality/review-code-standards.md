# Review Code & Maintain Standards

> **Category:** Code Quality & Testing
> **Relevant at:** Impressive Security, As-Sunnah Foundation, Eicra Soft
> **Related tech docs:** `case/devops/devops-and-cicd.md` (Git §1–11, CI/CD §23–33), `case/code-quality/write-quality-code.md` (neighbor file)

---

## 1. What This Means

Reviewing code and maintaining standards means owning **team-wide code quality** — reviewing pull requests, enforcing coding standards, promoting best practices, and ensuring consistently high engineering quality across the whole team, not just one's own work.

**Scope:**
- **Pull request review** — constructive, thorough feedback before merge
- **Enforcing standards** — linting, formatting, conventions applied uniformly
- **Promoting best practices** — sharing knowledge, documenting patterns
- **Mentoring through review** — teaching, not just correcting
- **Maintaining the bar** — consistency across the team and over time

**Why it matters:** code review is where team quality is made or lost. Without strong review, standards drift, knowledge stays siloed, and bugs/tech debt accumulate. With it, the whole team levels up, knowledge spreads, and the codebase stays healthy as it grows.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The review is a quality gate, not a rubber stamp:**
- Every change is reviewed before merge — no direct pushes to main
- Reviews catch bugs, enforce conventions, and **spread knowledge** (the reviewer learns the change; the author learns the standard)
- Automated checks (lint, tests, formatting) handle the mechanical; humans focus on **design, correctness, and maintainability**

**Real-world review focus areas:**
| Aspect | What the reviewer checks |
|---|---|
| **Correctness** | Does it do what it claims? Edge cases handled? |
| **Design** | Right abstractions? Clear boundaries? Not over-engineered? |
| **Standards** | Follows conventions? Naming, structure, patterns? |
| **Tests** | Are there tests? Do they cover the change + edge cases? |
| **Security** | Input validation? Authz? No secrets? |
| **Readability** | Will the next dev understand this? |

**The mentoring dimension (especially at Impressive Security, Eicra Soft):**
- Junior developers learn standards *through* review feedback
- Reviews are **constructive** — explain *why*, suggest alternatives, not just "change this"
- Over time, the team converges on shared standards without rigid enforcement

**The principle:** review for **the team and the codebase's future**, not just "does this PR work right now." A merge is a commitment to maintain this code forever.

---

## 3. How to Implement

### The Review Workflow

```bash
# Branch → PR → CI (lint/test/build) → review → merge
git checkout -b feature/payment-refunds
# ... develop, commit ...
git push origin feature/payment-refunds
# Open PR → CI must pass → at least one approval → merge to main (protected)
```

### What a Good Review Looks Like

```markdown
## Review Feedback (constructive, specific, explains why)

✅ "Nice extraction — `calculate_discount` is much cleaner now."

❓ "Should `process_payment` also handle the `INSUFFICIENT_FUNDS` error case?
    Currently it would throw an unhandled exception."   ← catches a bug

💡 "Consider using the existing `retry_with_backoff` helper here instead of
     a custom retry loop — keeps it DRY and tested."   ← promotes a pattern

⚡ "This query is missing an index on `(tenant_id, status)` — it'll seq scan
     as data grows. Added in the DB migration?"   ← catches performance debt
```

### Enforce Standards Automatically (Free the Humans)

```yaml
# Let tools handle the mechanical; humans handle the meaningful
jobs:
  checks:
    steps:
      - run: ruff check .            # lint (style + bugs)
      - run: black --check .         # formatting
      - run: mypy app/               # type checking
      - run: pytest                  # tests
# Reviewers now focus on design/correctness, not commas and naming
```

### PR Conventions That Maintain Quality

```markdown
## PR Template (enforced on every pull request)
### What
Brief description of the change.

### Why
The motivation / business reason.

### How
Key design decisions + alternatives considered.

### Testing
- [ ] Unit tests added/updated
- [ ] Manually verified the happy path
- [ ] Checked edge cases

### Checklist
- [ ] No secrets / credentials
- [ ] Follows existing patterns
- [ ] Updated documentation if needed
```

### Review & Standards Checklist

- [ ] **Every change reviewed** before merge (main branch protected)
- [ ] **CI gates** — lint, format, type-check, tests must pass
- [ ] **Reviews are constructive** — explain why, suggest alternatives
- [ ] **Standards documented** — conventions, patterns, architecture decisions
- [ ] **Reviews cover** correctness, design, tests, security, readability
- [ ] **Knowledge spreads** — rotate reviewers so context doesn't silo
- [ ] **Small PRs encouraged** — easier to review thoroughly than 1000-line dumps
- [ ] **Automated where possible** — tools enforce the mechanical
- [ ] **ADR pattern** — architectural decisions recorded, not lost to chat history

### Avoid These

- **Rubber-stamp reviews** — "looks good 👍" without reading — defeats the purpose
- **Nitpicking style** that tools can enforce — waste of human review time
- **Large, unreviewable PRs** — too big to assess thoroughly
- **Harsh/personal feedback** — erodes psychological safety; review the code, not the person
- **No documented standards** — each reviewer enforces their own opinion; inconsistency
- **Reviewing only the author's close friends** — knowledge silos; context doesn't spread
- **Approving without understanding** — "it has tests, ship it" without reading the logic
