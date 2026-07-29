# Lead End-to-End SDLC

> **Category:** Technical Leadership
> **Relevant at:** MVI Solutions
> **Related tech docs:** `case/code-quality/review-code-standards.md` (code review), `case/code-quality/maintain-test-suites.md` (testing), `case/devops/devops-and-cicd.md` (CI/CD §23–33), `case/operations/troubleshoot-production-issues.md` (post-launch support)

---

## 1. What This Means

Leading the end-to-end software development lifecycle means **owning a feature or project from start to finish** — from requirement analysis and system design, through development, testing, and deployment, to post-launch support — ensuring quality and value at every stage.

**Scope:**
- **Requirement analysis** — understanding the *problem* before building a *solution*
- **System design** — architecting the solution before writing code
- **Development** — leading the build with standards and quality
- **Testing** — ensuring the solution actually works (and keeps working)
- **Deployment** — shipping safely to production
- **Post-launch support** — monitoring, fixing, and iterating after release

**Why it matters:** most failures aren't coding failures — they're *process* failures: building the wrong thing, skipping design, under-testing, or abandoning the feature after launch. SDLC leadership ensures the *right* thing gets built, well, and stays healthy.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The lifecycle a leader drives:**
```
Requirements → Design → Development → Testing → Deployment → Support
     │            │           │           │           │           │
  "what & why"  "how"      "build"     "verify"     "ship"     "maintain"
```

**What "leading" means at each stage:**
- **Requirements:** push back on vague asks; clarify *the problem* and *success criteria* before building
- **Design:** sketch the architecture, identify risks/dependencies, before code is written
- **Development:** set standards, review code, unblock the team
- **Testing:** ensure coverage of critical paths and edge cases
- **Deployment:** plan the rollout (staged, rollback-ready), communicate the release
- **Support:** monitor after launch, fix issues, gather feedback for iteration

**Real-world scenarios:**
- A stakeholder says "build X" → the leader asks *why*, discovers the real problem, and proposes a better solution
- A feature is "done" but untested → the leader holds the line: it's not done until it's verified and deployable
- Launch day → the leader has a rollback plan, monitoring in place, and is ready to respond
- Post-launch bugs → the leader ensures they're fixed, not abandoned as "someone else's problem"

**The principle:** ownership doesn't end at deployment. A feature is owned through its entire life — including what happens after it ships.

---

## 3. How to Implement

### Stage 1 — Requirements (Understand the Problem)

```markdown
## Before building, answer:
- **What problem are we solving?** (not "what feature to build")
- **Who benefits, and how?**
- **What does success look like?** (measurable if possible)
- **What's out of scope?** (prevents scope creep)
- **What are the risks/constraints?** (time, dependencies, security)

# Push back on vague requirements — clarity here prevents wasted work later
```

### Stage 2 — System Design (Plan Before Coding)

```markdown
## Design Document (lightweight but real)
### Approach
How the solution works at a high level.

### Key Decisions
What patterns/tech, and why (alternatives considered).

### Data Model
What changes in the DB/schema.

### API Contract
New/changed endpoints.

### Risks & Mitigations
What could go wrong, and how we handle it.

### Testing Plan
What to test (unit/integration/E2E) and critical paths.

### Rollout Plan
Staged deploy, feature flag, rollback strategy.
```

### Stage 3–4 — Development & Testing

```markdown
## Leading the build:
- Break work into small, reviewable PRs
- Review code against standards (see review-code-standards.md)
- Ensure tests cover critical paths + edge cases (see maintain-test-suites.md)
- Unblock the team — remove obstacles, answer questions, pair when needed
- Keep main deployable at all times
```

### Stage 5 — Deployment (Ship Safely)

```bash
# Safe rollout — staged, observable, reversible
# 1. Deploy to staging → smoke test
# 2. Production — staged (canary or rolling), with monitoring
# 3. Have rollback ready (blue/green or previous task def)
# 4. Communicate the release (release notes, stakeholders informed)
```

### Stage 6 — Post-Launch Support (Own It After Shipping)

```markdown
## After launch:
- **Monitor** — watch metrics, errors, user feedback for 24–48h
- **Respond** — fix issues fast; have the rollback if needed
- **Gather feedback** — did it solve the problem? what's next?
- **Document** — update docs/runbooks so the team can support it
- **Iterate** — the first version is rarely the final one
```

### SDLC Leadership Checklist

- [ ] **Requirements clarified** — problem understood before solution designed
- [ ] **Success criteria defined** — you know when it's "done"
- [ ] **Design documented** — approach, decisions, risks, before coding
- [ ] **Work broken into small PRs** — reviewable, reversible
- [ ] **Standards enforced** in code review
- [ ] **Critical paths tested** — not just "it works on my machine"
- [ ] **Rollout plan** — staged, monitored, rollback-ready
- [ ] **Post-launch monitoring** — owned for at least 24–48h after ship
- [ ] **Docs/runbooks updated** — the team can support it
- [ ] **Feedback gathered** — iterate based on real outcomes

### Avoid These

- **Building before understanding the problem** — solves the wrong thing
- **No design phase** — coding into a void; expensive rework later
- **"Done" without testing/deployment plan** — it's not done until it's in users' hands
- **No rollback plan** — launch day becomes a crisis
- **Abandoning after launch** — post-launch bugs erode trust
- **Scope creep** — unclear boundaries inflate the project indefinitely
- **No documentation** — the team can't support what you built
