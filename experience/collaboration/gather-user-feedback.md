# Gather & Evaluate User Feedback

> **Category:** Collaboration & Product Development
> **Relevant at:** All five companies (universal responsibility across every role)
> **Related tech docs:** `case/collaboration/cross-functional-collaboration.md` (working with PMs/stakeholders), `case/leadership/lead-sdlc.md` (iterating post-launch), `case/devops/devops-and-cicd.md` (CI/CD — deploying fixes fast)

---

## 1. What This Means

Gathering and evaluating user feedback means systematically **collecting, analyzing, and acting on input** from real users — closing the loop between what users experience and what the engineering team builds next. It also means **building tools and processes that reduce errors** and proactively **improve the customer experience** before users have to report problems.

**Scope:**
- **Collecting feedback** — bug reports, feature requests, usability issues, satisfaction data
- **Evaluating and prioritizing** — separating signal from noise; deciding what to build/fix next
- **Closing the loop** — communicating back to users what changed and why
- **Error reduction tools** — building systems that catch issues before users see them
- **Proactive CX improvement** — monitoring, alerting, and automated quality checks

**Why it matters:** the distance between "users are frustrated" and "engineers know what to fix" is where products die. Engineers who build feedback loops and error-prevention tools ship better software faster — and build trust with users.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The feedback loop:**
```
Users experience an issue
   → Feedback is captured (bug report, analytics, support ticket)
      → Triaged and prioritized (severity, frequency, impact)
         → Fix or feature built
            → Deployed
               → Users notified — loop closed
```

**Two distinct responsibilities:**
1.  **Reactive** — users report bugs; you fix them (see `troubleshoot-production-issues.md`)
2.  **Proactive** — you build tools and monitoring that catch issues BEFORE users report them, and you systematically improve the experience based on usage data

**Error-reduction tools (the proactive side):**
- **Automated testing** — catch regressions in CI, not in production
- **Error monitoring** — Sentry, Datadog, CloudWatch alarms surface errors in real time
- **Feature flags** — ship to 1% of users first; roll back if error rates spike
- **Health checks + auto-healing** — detect unhealthy instances and replace them automatically
- **User analytics** — track where users struggle (rage clicks, drop-offs, support spikes)

**Real-world scenarios:**
- A user reports a bug → you reproduce, fix, deploy, and **reply to the user** confirming it's resolved
- Multiple users report the same confusion → it's a UX gap, not a support ticket → you log a feature improvement
- Error monitoring shows a spike in 500s → you find and fix the root cause **before users report it**
- Support tickets spike after a deploy → you roll back, investigate, and add a regression test
- A user suggests an improvement → you evaluate it against the roadmap; if you build it, you tell them

**The principle:** feedback isn't a chore — it's free product research. Every bug report, confusion, or suggestion tells you something about how real people use your software. Ignoring feedback is ignoring your best source of product insight.

---

## 3. How to Implement

### Collecting Feedback — Make It Easy

```markdown
## Feedback channels (make them visible and low-friction):
- **In-app feedback widget** — "Report a bug" / "Suggest a feature" with one click
- **Support ticketing system** — structured, searchable, linked to user accounts
- **Error monitoring (Sentry, Datadog)** — auto-capture crashes with context (user, URL, stack trace)
- **Analytics (Mixpanel, Amplitude)** — behavioral data: where users drop off, rage click, get stuck
- **User interviews / usability testing** — qualitative: why users struggle, not just where
- **NPS / satisfaction surveys** — quantitative: how do users feel over time?
```

### Triaging Feedback — Separate Signal from Noise

```markdown
## Triage framework (every piece of feedback gets assessed):
| Question | Why it matters |
|---|---|
| **How many users are affected?** | 1 user vs 1000 — different priority |
| **What's the impact?** | Data loss? Workaround possible? Cosmetic? |
| **How often does it happen?** | Every request? Once a month? |
| **Is it getting worse?** | Growing error rate = escalating priority |
| **What's the root cause?** | Bug in code? UX confusion? Missing feature? |

## Priority buckets:
- **P0 — Critical:** data loss, security, complete outage → fix immediately
- **P1 — High:** broken core feature, no workaround → fix this sprint
- **P2 — Medium:** partial workaround, affects some users → queue for next sprint
- **P3 — Low:** cosmetic, edge case, nice-to-have → backlog; evaluate collectively
```

### Evaluating Feature Requests

```markdown
## Not every request should be built. Evaluate against:
- **Does it align with the product vision?** — or is it a one-off for one customer?
- **How many users want it?** — one loud voice vs. silent majority
- **What's the effort vs. impact?** — a day of work for massive improvement? Do it. Six months for marginal gain? Question it.
- **Can it be generalized?** — "Acme wants X" → can we build something that helps ALL customers?

## Track requests:
- Log every request in a single system (Linear, Jira, GitHub issues)
- Tag with "feedback" / "customer-request" / number-of-requesters
- Periodically review the backlog — patterns emerge when you see 10 requests for the same thing
```

### Building Error-Reduction Tools

```python
# 1. Automated health checks — catch issues before users do
@app.get("/health")
async def health_check():
    checks = {
        "db": await db.execute("SELECT 1"),
        "redis": await redis.ping(),
        "queue_depth": await sqs.get_queue_depth(),  # alert if growing
    }
    return checks   # orchestrator auto-replaces unhealthy instances

# 2. Error rate alerting — know when things break
# (CloudWatch alarm, Datadog monitor, Sentry alert)
ALERT_CONDITIONS = {
    "error_rate_gt_1pct": lambda m: m.error_rate > 0.01,
    "p99_latency_gt_2s": lambda m: m.latency_p99 > 2000,
    "queue_depth_growing_fast": lambda m: m.queue_depth_trend > 1.5,
}

# 3. Feature flags for safe rollout
if feature_flag.is_enabled("new-checkout", user_id=user.id):
    return new_checkout_flow()
else:
    return existing_checkout_flow()

# Rollout: 1% → 10% → 50% → 100%, with automated rollback if error rate spikes
```

### Proactive Customer Experience Improvement

```python
# 1. Client-side error reporting — catch JS errors in the browser
Sentry.init({ dsn: "...", tracesSampleRate: 0.1 })

# 2. Performance monitoring for real users (RUM)
# Track Core Web Vitals (LCP, INP, CLS) from real user sessions
# Slow pages = frustrated users, even if they don't report it

# 3. Usage analytics — find where users struggle
# High drop-off on a form? Add inline validation, auto-save, or simplify.
# Rage clicks (rapid repeated clicks)? The button isn't responding — fix the feedback.

# 4. Proactive notifications — tell users about issues before they ask
status_page.update("Payment processing delayed — we're on it")
```

### Closing the Loop — Communicating Back

```markdown
## When a user-reported issue is fixed:
- **Reply to the ticket/report** — "This is fixed in v2.4. Here's what changed."
- **Release notes** — include the fix; credit the reporter
- **Status page updates** — for downtime/incidents, keep users informed DURING and AFTER

## Why closing the loop matters:
- Users who are heard become advocates
- Users who are ignored churn
- A "this is fixed" reply turns a negative experience into a trust-building one
```

### Feedback & CX Checklist

- [ ] **Multiple feedback channels** available (in-app, support, error monitoring, analytics)
- [ ] **Triage process** defined — every piece of feedback assessed for impact and priority
- [ ] **Feature requests tracked** centrally — patterns reviewed periodically
- [ ] **Error monitoring** catches issues before users report them
- [ ] **Health checks + alerting** on all critical services
- [ ] **Feature flags** for incremental, safe rollouts
- [ ] **Real-user monitoring (RUM)** tracks actual experience, not just server metrics
- [ ] **Feedback loop closed** — users notified when their reported issue is resolved
- [ ] **Root causes addressed** — fixing the bug AND the process gap that allowed it

### Avoid These

- **Collecting feedback and ignoring it** — users notice; they stop reporting
- **Building every feature request** — you're a product team, not a bespoke dev shop
- **No triage** — everything is "P1" = nothing is really P1
- **Fixing symptoms, not causes** — user reports the same bug every release
- **No proactive monitoring** — only learning about issues from angry users
- **Not closing the loop** — fixing a bug without telling the reporter
- **Ignoring silent struggles** — a feature nobody complains about but everyone avoids
