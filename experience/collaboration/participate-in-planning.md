# Participate in Planning

> **Category:** Collaboration
> **Relevant at:** As-Sunnah Foundation
> **Related tech docs:** `case/leadership/lead-sdlc.md` (SDLC), `case/leadership/own-technical-decisions.md` (ADRs, architecture), `case/code-quality/review-code-standards.md` (documentation), `case/operations/troubleshoot-production-issues.md` (improvement from incidents)

---

## 1. What This Means

Participating in planning means actively engaging in the **upfront and strategic work** that shapes what gets built — architecture discussions, sprint planning, backlog refinement, technical documentation, and continuous improvement initiatives — so the team builds the *right things, in the right order, on a sound foundation*.

**Scope:**
- **Architecture discussions** — shaping technical direction before code is written
- **Sprint planning** — estimating, sequencing, and committing to realistic work
- **Backlog refinement** — clarifying, sizing, and prioritizing upcoming work
- **Technical documentation** — capturing architecture, decisions, and how-tos
- **Continuous improvement** — retrospectives, process changes, leveling up the team

**Why it matters:** the work done *before* coding — planning, design, prioritization — determines whether the coding effort is well-spent or wasted. Engineers who participate in planning ensure technical reality shapes the plan, not just business wishes.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The planning cadence:**
```
Backlog refinement  →  clarify & size upcoming work
  → Sprint planning  →  commit to a realistic chunk
    → Architecture discussion  →  design before build
      → Development  →  execute the plan
        → Retrospective  →  improve the process
```

**What "participating" means at each stage:**
- **Architecture discussions** — contribute technical reality: "that approach won't scale past X users; here's an alternative"
- **Sprint planning** — give honest estimates; flag dependencies and risks; don't overcommit
- **Backlog refinement** — ask clarifying questions *now* so stories are buildable *later*; spot gaps early
- **Technical documentation** — write the ADR, the architecture overview, the "how to add a feature" guide
- **Continuous improvement** — in retros, name what's not working and propose changes (not just complain)

**Real-world scenarios:**
- PM wants 5 features this sprint → you estimate honestly and negotiate scope (3 done well > 5 half-done)
- A backlog story is vague → you refine it in grooming: "what's the acceptance criteria? what data changes?"
- A new feature needs a design decision → you raise it in architecture discussion *before* sprint start
- The team's deploy process is painful → you bring it up in retro and propose a fix

**The principle:** engineers who shape the plan prevent the two biggest wastes — building the **wrong thing** (bad prioritization) and building it the **wrong way** (no design). Planning is where you protect both quality and sanity.

---

## 3. How to Implement

### Sprint Planning — Honest Estimates & Scope

```markdown
## In planning, contribute technical reality:
- **Estimate honestly** — "this is a 5, not a 2; it touches payments and needs tests"
- **Flag dependencies** — "feature B depends on feature A's API; sequence matters"
- **Surface risks** — "this integrates with a flaky third-party; build in buffer"
- **Negotiate scope** — "we can do all 5 poorly, or 3 done well with tests. I recommend 3."
- **Don't overcommit** — a missed sprint erodes trust; realistic commitments build it

## Estimation anchors (reference stories):
"This is about the size of the [previous feature X] — similar complexity."
```

### Backlog Refinement — Clarify Before You Build

```markdown
## In refinement, make stories buildable:
- **Ask for acceptance criteria** — "done" means what, exactly?
- **Identify data/model changes** — does this need a DB migration?
- **Spot edge cases early** — "what if the cart is empty? what if payment fails?"
- **Size the story** — is it one sprint's work or three?

## A well-refined story:
### As a user, I can cancel a pending order
- Acceptance: only orders with status=pending can be cancelled
- Acceptance: cancelled orders trigger a refund
- Acceptance: cancelled orders emit OrderCancelled event
- Tech notes: needs status guard + event + refund integration
```

### Architecture Discussions — Design Before Build

```markdown
## Bring technical decisions into the open before coding:
- "This feature has two viable approaches — here are the tradeoffs" (see own-technical-decisions.md ADRs)
- "This will need a new service — let's discuss the boundary"
- "This touches the auth flow — security review needed"

## Don't discover architecture problems mid-sprint:
# A 30-minute design discussion in planning saves days of rework in development.
```

### Technical Documentation — Capture It

```markdown
## Documentation that prevents repeated questions:
- **Architecture overview** — how the system fits together (diagram + description)
- **ADRs** — why we chose X over Y (decisions, not just current state)
- **"How to add a feature"** — onboarding guide; reduces bus factor
- **Runbooks** — how to handle common ops/incidents

## Rule: if you explained it twice, write it down.
```

### Continuous Improvement — Retrospectives That Change Things

```markdown
## In retros, be constructive (not just complainy):
- **What worked?** (keep doing it)
- **What didn't?** (name it specifically)
- **What will we change?** (actionable, owned, tracked)

## BAD retro: "deploys are painful" (vague, no owner, nothing changes)
## GOOD retro: "deploys take 2h of manual steps → Sam will automate
   the staging step this sprint (Linear #789)"
```

### Planning Participation Checklist

- [ ] **Honest estimates** — realistic, not optimistic; negotiate scope
- [ ] **Dependencies flagged** before the sprint starts
- [ ] **Stories refined** — acceptance criteria clear before build
- [ ] **Architecture discussed** for non-trivial work (design before code)
- [ ] **Technical documentation** written (architecture, ADRs, runbooks)
- [ ] **Retro action items** specific, owned, and tracked
- [ ] **Risks surfaced early** — not discovered mid-sprint
- [ ] **Voice contributes** technical reality to business-driven plans

### Avoid These

- **Overcommitting** — saying yes to everything; missing the sprint erodes trust
- **Vague estimates** — "it's easy" with no basis; surprises mid-sprint
- **Skipping refinement** — building ill-defined stories; rework and scope creep
- **No design discussion** — discovering architecture problems mid-build
- **Complaints without proposals** — naming problems but not solutions
- **Undocumented decisions** — "we discussed it in planning" that nobody recalls
- **Silent acceptance** of an unrealistic plan — engineers must shape it with technical reality
