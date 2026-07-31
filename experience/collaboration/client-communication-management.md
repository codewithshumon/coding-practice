# Client Communication & Management

> **Category:** Collaboration & Soft Skills
> **Relevant at:** MVI Solutions, Impressive Security, Eicra Soft (all client-facing engineering roles)
> **Related tech docs:** `case/collaboration/cross-functional-collaboration.md` (translating between technical and business), `case/leadership/own-technical-decisions.md` (communicating tradeoffs), `case/collaboration/participate-in-planning.md` (negotiating scope and timelines)

---

## 1. What This Means

Client communication and management means effectively interacting with **external clients, stakeholders, and non-technical partners** — translating technical complexity into business-understandable language, managing expectations, negotiating scope and timelines, and building trust through clarity and reliability.

**Scope:**
- **Translating technical → business** — explaining what's possible, what's hard, and why, in terms clients understand
- **Managing expectations** — setting realistic timelines, flagging risks early, never over-promising
- **Negotiating scope** — helping clients understand tradeoffs (speed vs. quality vs. features vs. cost)
- **Presenting progress** — demos, status updates, milestone reviews that build confidence
- **Handling difficult conversations** — delays, bugs, scope changes — with honesty and solutions, not excuses
- **Building long-term trust** — being the reliable engineer the client asks for by name

**Why it matters:** technical skill alone doesn't retain clients. The engineer who can explain a complex migration in plain English, set honest timelines, and handle a production incident calmly is more valuable than one who just writes perfect code. Client trust is the foundation of every successful project.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The client-engineering interface:**
```
Client: "We need X feature by Friday."
Engineer (bad):  "Okay." (Friday comes, it's not done — trust broken.)
Engineer (good): "Let me understand what you need. X has three parts —
                   A is quick (2 days), B needs design (1 week), C depends on
                   a third-party API (2 weeks). Can we ship A by Friday and
                   plan B + C for the next sprint?"
```

**Real-world scenarios:**
- **Scope negotiation** — the client wants everything; you explain the tradeoffs and help them prioritize
- **Status demos** — showing working software every sprint builds more confidence than a weekly "we're on track" email
- **Bad news delivery** — a delay, a bug, a blocked dependency — communicated early with a plan, not hidden until the deadline
- **Technical explanation** — "why can't you just copy what [competitor] does?" — explained in product terms, not architecture
- **Pushing back professionally** — the client asks for something technically harmful; you explain why and propose a better approach
- **Emergency communication** — production is down; you communicate clearly, frequently, and calmly

**The trust stack:**
1.  **Reliability** — do what you say, when you say you'll do it
2.  **Transparency** — share bad news early, with a plan
3.  **Competence** — demonstrable progress, working software
4.  **Empathy** — understand their business problem, not just the technical spec

**The principle:** clients don't hire engineers for code — they hire engineers to **solve problems**. Communication is how you align on what problem to solve, set expectations on how long it takes, and demonstrate that it's solved.

---

## 3. How to Implement

### Translating Technical → Business

```markdown
## BAD (jargon to a client):
"We need to refactor the ORM layer and implement a caching strategy
with Redis to reduce query latency under concurrent load."

## GOOD (business language):
"The app slows down when many users are on it. We can fix this in two weeks
by adding a fast data-access layer. Here's how much faster it'll be [before/after]."

## The translation skill:
| If the engineer says... | The client hears... |
|---|---|
| Refactor the data layer | "Improve performance" |
| Implement rate limiting | "Protect against abuse / save costs" |
| Set up CI/CD pipeline | "Ship updates faster and more reliably" |
| Migrate to microservices | "Scale the app as your business grows" |
| Fix technical debt | "Prevent future bugs and speed up future features" |

## Rule: lead with the BENEFIT, then offer the technical explanation if they ask.
```

### Managing Expectations (Never Over-Promise)

```markdown
## The expectation-setting formula:
1. **Understand** — what problem are they really trying to solve?
2. **Assess** — what's the realistic effort? (then add buffer — things go wrong)
3. **Communicate** — "Here's what we can do by [date], here's what comes after."
4. **Flag risks early** — "This part depends on [external factor]; if that slips, we slip."
5. **Update proactively** — don't wait for them to ask "how's it going?"

## Saying no (professionally):
"I can build that, but here's the tradeoff: it takes X weeks, which means
[other priority] moves to next month. Alternatively, we can do Y which
achieves 80% of the goal in 2 days. Which direction do you prefer?"

## Handling timeline pressure:
Client: "Can you get this done by Friday?"
Engineer (bad):  "I'll try." (vague promise, likely missed)
Engineer (good): "The full feature needs until next Wednesday. But I can
                  deliver [the core part that works] by Friday so you can
                  start testing. Will that help?"
```

### Status Updates & Demos

```markdown
## Weekly update template (clear, brief, honest):
### This week
- ✅ Completed: [specific, demonstrable]
- 🔄 In progress: [specific, % done, any blockers]
- ❌ Didn't get to: [why, when it'll happen]

### Next week
- [Priorities with expected outcomes]

### Risks / Need input on
- [Flag anything the client needs to decide or know]

## Demos — show, don't tell:
- Demo working software every sprint (even if incomplete)
- A 10-minute clickable demo > a 30-minute slide deck
- Let the client drive the demo when possible
- Record demos for async stakeholders
```

### Handling Difficult Conversations

```markdown
## The bad-news formula:
1. **Say it early** — the day you know, not the day it's due
2. **State the impact** — what happened, what it means for the timeline/scope
3. **Own it** — no excuses; "we missed this" > "the API was slow"
4. **Present the plan** — here's what we're doing about it, here's the new ETA
5. **Prevent recurrence** — here's what we're changing so it doesn't happen again

## Example — delay announcement:
"We found a data issue during testing that'll push the launch from Friday to
next Tuesday. Here's what happened [brief, technical root cause in plain terms],
here's the fix [plan], and here's the new timeline. We're adding automated tests
to catch this class of issue earlier. I'll update you Monday on progress."

## Why this works:
- Early = you're proactive, not hiding problems
- Owned = you're accountable, not defensive
- Plan = you're in control, not flailing
- Prevention = you're learning, not repeating
```

### Building Long-Term Trust

```markdown
## Trust is built through consistency:
- **Do what you say** — under-promise, over-deliver every time
- **Be reachable** — respond within the agreed SLA (even if just "saw this, will look tomorrow")
- **Be proactive** — suggest improvements they haven't asked for; flag risks they haven't seen
- **Learn their business** — understand their industry, competitors, and constraints
- **Celebrate together** — share wins, metrics, and positive user feedback

## Trust moves at the speed of honesty:
- A missed deadline honestly communicated builds more trust than a deadline "met" with hidden corners cut.
- A "I don't know, let me find out" builds more trust than a confident wrong answer.
- A "this approach is wrong, let's change it" builds more trust than silently building the wrong thing.
```

### Client Communication Checklist

- [ ] **Technical→business translation** — every technical decision communicated in benefit-first language
- [ ] **Expectations set early** — scope, timeline, risks, dependencies
- [ ] **Weekly status updates** — consistent format, honest progress
- [ ] **Regular demos** — working software shown, not just described
- [ ] **Bad news delivered early** — with ownership, plan, and prevention
- [ ] **Scope changes negotiated** — tradeoffs explained, not just "yes" or "no"
- [ ] **Responsive communication** — SLA-respecting reply times
- [ ] **Proactive suggestions** — you're a partner, not an order-taker
- [ ] **Client's business understood** — industry, goals, constraints

### Avoid These

- **Over-promising** — "yes" to every timeline creates a track record of being late
- **Jargon without translation** — "implementing CQRS with eventual consistency" means nothing
- **Hiding bad news** — the client always finds out; better from you, early, with a plan
- **Going silent when stuck** — a two-day silence on a blocker erodes trust
- **"That's not my job"** — the client has one point of contact; you're it
- **Defensive responses to bugs** — "it worked on my machine" damages credibility
- **Ignoring the client's business context** — understanding their goal improves your technical decisions
- **No demos, only status reports** — talking about progress ≠ showing progress
