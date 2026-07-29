# Collaborate Async with Distributed Teams

> **Category:** Collaboration
> **Relevant at:** Eicra Soft (async work with US-based Solutions Architects via Linear)
> **Related tech docs:** `case/code-quality/review-code-standards.md` (async code review), `case/leadership/own-technical-decisions.md` (written specs/ADRs), `case/devops/devops-and-cicd.md` (Git §1–11)

---

## 1. What This Means

Collaborating asynchronously with distributed teams means working effectively **across time zones and without real-time conversation** — relying on **written communication, proactive code review, and clear specs** (via tools like Linear) to maintain strict engineering standards and momentum when teammates aren't online simultaneously.

**Scope:**
- **Written-first communication** — specs, decisions, and context captured in writing (not "let's hop on a call")
- **Proactive async code review** — thorough, timely reviews that don't block on sync time
- **Strict standards without sync enforcement** — quality maintained through process, not presence
- **Timezone-aware workflow** — handing off work, minimizing blocking dependencies

**Why it matters:** distributed/async teams can't rely on tapping a colleague's shoulder. The cost of unclear communication is **delayed by a full day** (you ask at your EOD; they answer at theirs). Async mastery turns a timezone gap from a friction into a 24-hour work cycle.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The async reality (Eicra Soft — working with US architects):**
```
Your day (Asia)          Their day (US)
  morning ────────────── their evening (offline)
  ──────────── handoff ────────────
  their morning ──────── your evening (offline)
```
- You can't wait for a synchronous answer — a vague question costs a full day
- **Clarity and completeness** in every message, PR, and spec is the currency

**What "async-native" work looks like:**
- **Written specs before code** — the US architect reviews the spec async, you build to approval
- **Self-directed progress** — you don't block on a quick question; you note it and continue
- **Thorough PR descriptions** — context, screenshots, decisions, so review needs no verbal explanation
- **Linear for everything** — issues, status, decisions, and blockers are tracked in writing

**The standards-without-presence challenge:**
- Without sync oversight, quality can drift — so standards are enforced through **process** (CI gates, review requirements, documented conventions) rather than a senior watching over your shoulder
- **Proactive review** — you review others' PRs promptly and thoroughly, expecting the same back

**The principle:** in async work, **writing is the work**. A clear spec, PR description, or status update *is* the collaboration — it's what keeps the team moving across time zones.

---

## 3. How to Implement

### Write Specs Before Code

```markdown
## Feature Spec (in Linear / docs) — reviewed async before building
### Problem
What we're solving and why.

### Proposed Approach
How, at a high level. Key decisions + alternatives.

### Open Questions
Things you need the architect's input on — flagged clearly.

### Scope
What's in/out. Acceptance criteria.

# The architect reviews this on their morning; you start building on yours
# with approved direction — no day lost to ambiguity.
```

### Write PR Descriptions That Need No Verbal Explanation

```markdown
## Pull Request
### What
Added order cancellation endpoint.

### Why
Users couldn't cancel pending orders (Linear #123).

### How
- New `DELETE /orders/:id` (only cancellable if status=pending)
- Emits `OrderCancelled` event for inventory/billing
- Refund handled async by the billing service

### Testing
- Unit tests for the status guard
- Integration test for the event emission
- Manually verified cancellation + refund flow in staging

### Screenshots
[before/after of the UI]

# A reviewer across the world has everything they need — no "let's chat" needed.
```

### Proactive Async Code Review

```markdown
## Review promptly and thoroughly:
- Review PRs from the other timezone **first thing** in your morning
  (so they have your feedback during their workday)
- Be specific and complete — "looks good" helps nobody async
- Ask questions in the PR (written), not via message they'll miss
- Approve clearly when it's ready — don't leave it ambiguous

## The async review etiquette:
- Don't block on style that a linter can enforce
- Explain reasoning (no context to clarify in person)
- If you'd reject, say so clearly + constructively in writing
```

### Manage Blocking Dependencies

```markdown
## Minimize "I'm blocked waiting for X":
- **Identify blockers at your EOD** — flag them so the other timezone can resolve overnight
- **Batch questions** — one thorough message beats ten small ones across the day
- **Have a parallel task** — if blocked on architect input, switch to unblocked work
- **Hand off cleanly** — leave the work in a reviewable state when you sign off

## The handoff:
"This is ready for your review (PR #456). Open question on line 23 about
the refund timing — your call. I'll start on the reporting feature meanwhile."
```

### Async Collaboration Checklist

- [ ] **Written specs** before code (reviewed async, not in a meeting)
- [ ] **Thorough PR descriptions** — self-contained, no verbal needed
- [ ] **Proactive, prompt review** — prioritize others' PRs first thing
- [ ] **Linear/issues** track all decisions, status, blockers
- [ ] **Blockers flagged at EOD** — resolved overnight, not next morning
- [ ] **Parallel work available** — never fully blocked on one thread
- [ ] **Standards enforced via process** (CI, review rules) not presence
- [ ] **Clear, complete writing** — ambiguity costs a full day
- [ ] **Decisions documented** — written record, not verbal memory

### Avoid These

- **"Let's hop on a call"** for things a written message could resolve — wastes a day across timezones
- **Vague questions** — "is this right?" with no context; they can't answer without a thread of clarification
- **Blocking on quick questions** — note it and continue; don't stall
- **Thin PR descriptions** — forces the reviewer to dig or message you (you're offline)
- **Leaving status ambiguous** — "is this approved?" shouldn't be a question in async
- **Relying on sync oversight for quality** — standards drift without process enforcement
- **Ten small messages** instead of one complete one — fragments context across the day
