# Analytical Problem-Solving Methodology

> **Category:** Troubleshooting & Soft Skills
> **Relevant at:** All five companies
> **Related tech docs:** `case/troubleshooting/troubleshoot-production-issues.md` (production incident response), `case/structures-architecture/backend-systems.md` (DSA §1–8 — algorithmic thinking), `case/code-quality/maintain-test-suites.md` (hypothesis verification via tests)

---

## 1. What This Means

Strong analytical and problem-solving skills mean having a **structured, repeatable methodology** for understanding complex problems, diagnosing root causes, and implementing effective solutions — rather than relying on intuition, guesswork, or trial-and-error.

**Scope:**
- **Problem decomposition** — breaking large, ambiguous problems into solvable pieces
- **Root cause analysis** — finding the actual cause, not just treating symptoms
- **Hypothesis-driven debugging** — forming and testing theories systematically
- **Data-informed decisions** — using metrics, logs, and evidence over gut feeling
- **Tradeoff evaluation** — comparing solutions across multiple dimensions (time, complexity, risk, maintainability)
- **Learning from outcomes** — post-resolution analysis that improves future problem-solving

**Why it matters:** the difference between a senior and junior engineer isn't just knowledge — it's **approach**. When faced with a novel, ambiguous problem, a strong problem-solver has a methodology that works regardless of the specific technology. They don't need to have seen the problem before to solve it.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The structured problem-solving framework:**
```
Define → Decompose → Hypothesize → Investigate → Verify → Fix → Learn
```

**Real-world scenarios where methodology matters:**
- **Intermittent production bug** — happens once every few days, no clear reproduction. Without methodology: random guesses, frustration, "can't reproduce → closing." With methodology: structured hypothesis, logging, narrowing, reproduction, fix.
- **Performance degradation** — the app is "slow" but nobody knows why. Without methodology: "add more servers." With methodology: profile end-to-end, isolate the bottleneck, apply Amdahl's law, fix the dominant cost.
- **Architecture decision** — choose between two approaches with different tradeoffs. Without methodology: "go with what I know." With methodology: evaluate against defined criteria (scalability, complexity, team skill, timeline), document the rationale (ADR).
- **New domain problem** — building something you've never built before. Without methodology: copy-paste from tutorials, hope it works. With methodology: decompose the problem, research each piece, build incrementally, validate at each step.

**The principle:** problem-solving is a **skill independent of technology**. The same methodology works whether the bug is in Python, JavaScript, a database query, or a cloud configuration.

---

## 3. How to Implement

### Step 1 — Define the Problem (Precisely)

```markdown
## A problem well-stated is a problem half-solved.

## BAD problem statement:
"The app is slow."

## GOOD problem statement:
"The `/orders` endpoint takes 3.2s (p95) when filtering by status='paid'
and date range > 30 days, for tenants with > 10,000 orders. Started after
the Dec 15 deploy. Affects ~200 users/hour during business hours."

## Define:
- **What** exactly is happening? (specific error, metric, behavior)
- **When** did it start? (deploy, traffic change, data growth?)
- **Where** in the system? (which endpoint, service, layer?)
- **How much** impact? (users affected, frequency, severity)
- **What's the expected behavior?** (what should happen instead?)

## If you can't state the problem clearly, you don't understand it yet.
```

### Step 2 — Decompose into Smaller Problems

```markdown
## Break the big, ambiguous problem into testable sub-problems:

"The `/orders` endpoint is slow"
   ├─ Is it the app code or the database?
   │   └─ Profile: DB queries take 95% of the time → focus on DB
   ├─ Is it a missing index?
   │   └─ EXPLAIN ANALYZE shows seq scan → yes
   ├─ Is it the filter, the sort, or the JOIN?
   │   └─ Test each in isolation → filter on status + date range is the bottleneck
   └─ Is a composite index the fix?
       └─ Test locally → yes, execution time drops from 3200ms to 4ms

## For each sub-problem, you can now form a specific, testable hypothesis.
```

### Step 3 — Form Hypotheses (and Test Them Systematically)

```python
# Hypothesis-driven debugging — state what you believe, then test it

# Hypothesis 1: "The query is slow because it's doing a sequential scan."
def test_hypothesis_1():
    plan = explain_analyze(SLOW_QUERY)
    assert "Seq Scan" in plan   # confirmed — missing index
    # Action: add composite index on (tenant_id, status, created_at)
    plan_after = explain_analyze(SLOW_QUERY)
    assert "Index Scan" in plan_after  # hypothesis verified, problem solved

# Hypothesis 2: "The intermittent 500 is caused by a race condition on concurrent updates."
def test_hypothesis_2():
    # Test: run concurrent updates, check for deadlocks
    results = run_concurrently(update_order, n=100)
    assert any(isinstance(r, DeadlockError) for r in results)  # confirmed
    # Action: add SELECT ... FOR UPDATE with NOWAIT

# BAD approach (no hypothesis):
# "Let me try restarting the server... changing this config... updating this library..."
# (shotgun debugging — no theory, just random attempts)
```

**The hypothesis testing loop:**
```
Form hypothesis → design a test → run the test → accept/reject → next hypothesis
```

A good hypothesis is:
- **Specific** — "the index on `status` is not being used because the query also filters on `tenant_id`"
- **Testable** — you can write a query or run a test that confirms/denies it
- **Falsifiable** — it's possible to prove it wrong

### Step 4 — Use Data, Not Intuition

```markdown
## Intuition is frequently wrong. Data is not.

## BAD: "I think the problem is in the caching layer."
## GOOD: "The distributed trace shows 82% of request time in the DB, 3% in cache
          lookup. The bottleneck is in the DB — let's look there first."

## Data sources for problem-solving:
- **Logs** — exact error messages, timestamps, request context
- **Metrics** — latency percentiles, error rates, throughput, resource usage
- **Traces** — where time is spent across services (distributed tracing)
- **Profiles** — where CPU/memory is spent within a single process
- **Experiments** — controlled changes with before/after measurement

## Rule: before applying a fix, have data showing it's the RIGHT fix.
```

### Step 5 — Evaluate Tradeoffs (Every Solution Has a Cost)

```markdown
## No solution is perfect — every fix involves tradeoffs:

| Solution | Speed | Complexity | Risk | Long-term |
|---|---|---|---|---|
| Add a composite index | ✅ Fast (minutes) | ✅ Low | ✅ Low (tested) | ✅ Great |
| Rewrite as materialized view | ❌ Slow (days) | ❌ High | ❌ Medium | ✅ Great for analytics |
| Cache the whole result | ⚠️ Medium | ⚠️ Medium | ❌ Stale data risk | ⚠️ Invalidation headache |
| Add a read replica | ❌ Slow (days) | ❌ High | ✅ Low | ✅ Scales reads broadly |

## The best solution isn't the most elegant — it's the one that:
1. Solves the actual problem
2. With acceptable risk
3. In a reasonable time
4. Without creating new problems
```

### Step 6 — Verify and Learn

```python
# Verification — prove the fix worked (before/after with data)
def verify_fix():
    before = measure_performance(QUERY)   # 3200ms p95
    apply_fix(ADD_COMPOSITE_INDEX)
    after = measure_performance(QUERY)    # 4ms p95
    assert after.latency < 100            # well under threshold
    assert after.error_rate == before.error_rate  # no regression
    # Verified: fix is deployed, monitoring confirms improvement

# Learning — prevent recurrence
# 1. Add a CI check: EXPLAIN ANALYZE on new queries, flag seq scans
# 2. Add to code review checklist: "Does this query have the right indexes?"
# 3. Share the RCA with the team (so everyone learns, not just you)
```

### Analytical Problem-Solving Checklist

- [ ] **Problem precisely defined** — what, when, where, how much, expected behavior
- [ ] **Decomposed** into testable sub-problems
- [ ] **Hypotheses formed** before investigating (not random poking)
- [ ] **Each hypothesis tested** systematically — accept, reject, or refine
- [ ] **Data used** to validate findings (logs, metrics, traces, profiles)
- [ ] **Tradeoffs evaluated** — speed vs. complexity vs. risk vs. maintainability
- [ ] **The fix verified** — before/after measurement, no regressions
- [ ] **Lessons captured** — root cause documented, prevention added, team informed

### Avoid These

- **Shotgun debugging** — random changes without a hypothesis
- **Fixing the symptom** — "restarted it, error stopped" (without finding why it errored)
- **Guessing without data** — "I think it's X" without evidence
- **Overcomplicating** — the simplest fix that works is usually the right one
- **Not verifying** — "it should work now" without measuring
- **Not learning** — fixing the bug without fixing the process that allowed it
- **Confirmation bias** — looking for evidence that supports your first theory, ignoring contradictory evidence
- **Paralysis by analysis** — analyzing forever without acting; at some point, act
