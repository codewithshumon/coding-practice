# Troubleshoot Production Issues

> **Category:** Operations & Troubleshooting
> **Relevant at:** Impressive Security, As-Sunnah Foundation, MVI Solutions
> **Related tech docs:** `case/devops/devops-and-cicd.md` (Linux §56–64, CI/CD §23–33), `case/performance-optimization/improve-platform-reliability.md` (reliability patterns), `case/code-quality/maintain-test-suites.md` (regression tests)

---

## 1. What This Means

Troubleshooting production issues means **diagnosing and resolving incidents** in live systems, performing **root cause analysis (RCA)** to understand *why* they happened, and implementing **reliable long-term solutions** that prevent recurrence — not just quick fixes that paper over the symptom.

**Scope:**
- **Incident response** — triage, mitigate, and resolve live production problems under pressure
- **Root cause analysis (RCA)** — find the actual cause, not just the symptom
- **Debugging complex issues** — distributed systems, intermittent failures, performance degradation
- **Long-term prevention** — fixes that stop recurrence (not band-aids)
- **Postmortems** — blameless learning from every incident

**Why it matters:** production incidents directly impact users, revenue, and trust. A good troubleshooter doesn't just restore service fast — they ensure the *same* problem can never happen again. Quick fixes that ignore root cause guarantee the incident repeats.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The incident lifecycle:**
```
Detect (alert/anomaly/user report)
  → Mitigate (stop the bleeding — rollback, scale, failover)
     → Diagnose (find root cause via logs, metrics, traces)
        → Fix (the actual solution, not a band-aid)
           → Prevent (postmortem → systemic fix so it never recurs)
```

**The two-phase mindset (critical):**
1. **Mitigate first** — restore service ASAP (rollback, scale out, switch to fallback). Don't debug while users are suffering.
2. **Diagnose second** — once stable, find *why* it happened and fix it properly.

**Real-world incident types:**
| Incident | Mitigation | Root cause to find |
|---|---|---|
| Deployment breaks the app | Rollback to previous version | What in the deploy broke it? (test gap) |
| Endpoint times out | Scale out / restart | DB lock? Missing index? Downstream outage? |
| Memory leak, OOM crashes | Restart / scale | What's accumulating? (unclosed resources) |
| Intermittent 500s | Circuit breaker / failover | Race condition? Flaky dependency? |
| Traffic spike, overload | Rate limit / autoscale | Capacity ceiling? Missing queue buffer? |

**The RCA discipline:** ask "why" repeatedly (5 Whys) until you reach a *systemic* cause — not "a developer made a mistake," but "our process allowed a bug to reach production undetected." Fix the system, not blame the person.

---

## 3. How to Implement

### Phase 1 — Mitigate (stop the bleeding)

```bash
# Fast rollback is your first tool — restore service before debugging
aws ecs update-service --service app --task-def previous-def   # redeploy last-known-good
# Or blue/green switch — flip traffic back to the stable stack
aws codedeploy stop-deployment --deployment-id $ID --auto-rollback-enabled

# Scale out if overloaded
aws autoscaling set-desired-capacity ... --desired-capacity 10

# Circuit break / failover a failing dependency
# (see improve-platform-reliability.md for circuit breaker patterns)
```

### Phase 2 — Diagnose (find root cause)

```bash
# The debugging trinity — logs, metrics, traces
# 1. Logs — what errors appeared and when?
journalctl -u my-service --since "1 hour ago" | grep -i error
kubectl logs <pod> --previous          # crashed container's last logs

# 2. Metrics — when did latency/errors spike? Correlate with deploys.
# (Datadog/CloudWatch/Grafana — overlay deploy markers on error rate)

# 3. Traces — where in the request path is time/failure occurring?
# (X-Ray/Jaeger — distributed trace shows the slow/failing hop)
```

```python
# Reproduce locally or in staging with the failing input
# Once reproduced, the fix is usually straightforward — reproduction is the hard part
```

### Phase 3 — RCA (5 Whys to systemic cause)

```markdown
## Postmortem Template (blameless)

### Incident
Brief description + impact (users affected, duration, revenue).

### Timeline
- 14:02 — Alert fired (error rate > 5%)
- 14:05 — On-call paged
- 14:10 — Rollback initiated
- 14:12 — Service restored

### Root Cause (5 Whys)
1. Why did errors spike? → The orders endpoint timed out.
2. Why did it time out? → DB queries took 30s.
3. Why were they slow? → A new query lacked an index.
4. Why was it unindexed? → No query review in the PR.
5. Why no review? → No DB-migration check in CI.
→ **Systemic fix:** add a CI check that flags slow queries / requires migration review.

### Action Items (prevent recurrence)
- [ ] Add EXPLAIN ANALYZE to CI on new queries
- [ ] Add a regression test for the slow query
- [ ] Update the runbook with this incident's mitigation
```

### Phase 4 — Prevent (long-term fixes)

```python
# A "fix" that doesn't prevent recurrence is a band-aid
# BAD: restarted the service, errors stopped (but the leak is still there)
# GOOD: found the unclosed resource, fixed it, added a test + memory alert

# Prevention always includes:
# 1. The actual code fix
# 2. A regression test (so it can't silently return)
# 3. An alert/runbook update (catch it faster if something similar happens)
```

### Troubleshooting Checklist

- [ ] **Mitigate first** — restore service before deep debugging
- [ ] **Rollback capability** tested and fast (you can always undo a deploy)
- [ ] **Logs + metrics + traces** available (you can't debug what you can't see)
- [ ] **Reproduce the issue** — fixes without reproduction are guesses
- [ ] **5 Whys RCA** — reach a systemic cause, not "human error"
- [ ] **Blameless postmortem** — learn, don't punish
- [ ] **Regression test** added for every fixed bug
- [ ] **Runbook updated** — next on-call handles it faster
- [ ] **Alerting** catches the failure class earlier next time

### Avoid These

- **Debugging while users suffer** — mitigate first, diagnose second
- **Fixing the symptom, not the cause** — "restarted it, works now" (until next time)
- **No rollback plan** — a bad deploy with no way back is prolonged downtime
- **Blame-focused postmortems** — people hide issues; learning stops
- **No regression test** — the exact bug returns months later
- **Action items not tracked** — postmortem written, nothing changes, incident repeats
- **Debugging in production** — reproduce in staging; poking prod risks making it worse
