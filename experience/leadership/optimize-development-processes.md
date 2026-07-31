# Optimize Product Development with Software Processes

> **Category:** Leadership & Process
> **Relevant at:** All five companies
> **Related tech docs:** `case/leadership/lead-sdlc.md` (end-to-end SDLC ownership), `case/collaboration/participate-in-planning.md` (sprint planning, backlog refinement), `case/devops/devops-and-cicd.md` (CI/CD §23–33 — automation as process), `case/code-quality/review-code-standards.md` (code review as process)

---

## 1. What This Means

Optimizing product development by leveraging software development processes means using **structured methodologies** (Agile, Scrum, Kanban, XP) not as rigid rituals but as **tools to deliver value faster, with higher quality, and with less waste**. It means continuously improving *how* the team works — not just *what* the team builds.

**Scope:**
- **Agile/Scrum/Kanban** — choosing and adapting the right process framework
- **Sprint cadences** — planning, daily standups, reviews, retrospectives
- **Workflow optimization** — minimizing bottlenecks, reducing cycle time, limiting WIP
- **Process automation** — CI/CD, automated testing, code quality gates
- **Continuous improvement** — retrospectives that produce real change
- **Measuring effectiveness** — velocity, cycle time, deployment frequency, defect rate

**Why it matters:** a great team with a broken process ships slowly. A good team with a great process ships consistently. Development processes aren't bureaucracy — they're the operating system for how work gets done. Optimizing them is among the highest-leverage work an engineer can do.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The process landscape:**
```
Agile (mindset) → Scrum or Kanban (framework) → Daily practices (standup, planning, retro)
```

**Agile principles (the mindset, not the ceremonies):**
1. **Individuals and interactions** over processes and tools
2. **Working software** over comprehensive documentation
3. **Customer collaboration** over contract negotiation
4. **Responding to change** over following a plan

**Scrum (sprint-based):**
```
Sprint (1–2 weeks)
   ├── Sprint Planning — what we'll build this sprint
   ├── Daily Standup — what I did, what I'll do, blockers (15 min)
   ├── Development — build, test, review, integrate
   ├── Sprint Review — demo working software to stakeholders
   └── Sprint Retrospective — what went well, what to improve
```

**Kanban (flow-based, no sprints):**
- Visualize work on a board (To Do → In Progress → Review → Done)
- Limit WIP (work in progress) — finish before starting new work
- Optimize flow — identify and fix bottlenecks
- Continuous delivery — ship when ready, not on a sprint boundary

**When to use which:**
| | Scrum | Kanban |
|---|---|---|
| Cadence | Fixed sprints | Continuous flow |
| Planning | Per sprint | On-demand |
| Best for | Teams building features in chunks | Ops/support/unpredictable work |
| Commitments | Sprint goal | No sprint commitment |

**Real-world scenarios:**
- **A team consistently misses sprint goals** → they're overcommitting; reduce WIP, improve estimation
- **Code review is a bottleneck** → PRs sit for days; add WIP limits, set review SLA, rotate reviewers
- **Retrospectives produce no change** → action items are vague and unowned; make them specific, assign owners, track completion
- **Deployments are painful** → manual steps, long cycles; automate CI/CD (see `manage-devops-workflows.md`)
- **Cycle time is increasing** → more time from "started" to "done"; find the bottleneck (review? testing? deployment?)

**The principle:** process is a **tool, not a religion**. The goal is to deliver value to users. If a ceremony isn't helping, change it or drop it. The best process is the one the team actually follows and improves.

---

## 3. How to Implement

### Choosing and Adapting Your Process

```markdown
## Start simple, add only what you need:

### Minimum viable process (any team):
- ✅ A visible backlog of work (ordered by priority)
- ✅ A way to know what everyone's working on
- ✅ Code review before merge
- ✅ Automated tests + CI
- ✅ A regular time to reflect and improve (retro)

### Add when needed:
- Sprint planning — when work needs predictable cadence and stakeholder alignment
- Daily standup — when the team needs sync (keep it short, focused)
- Sprint review/demo — when stakeholders need visibility
- WIP limits — when the team starts too many things and finishes few
- Estimation — when stakeholders need rough timelines (use story points or t-shirt sizes)

### Don't add:
- Ceremonies "because Scrum says so"
- Story points if hours work fine
- Detailed upfront specs if the domain is exploratory
```

### Optimizing the Workflow (Find and Fix Bottlenecks)

```python
# Measure what matters — optimize the constraint
# Key metrics (pick 2–3; don't measure everything):

# 1. Cycle time — time from "started" to "shipped"
#    Trend: increasing = bottleneck somewhere
# 2. Deployment frequency — how often you ship
#    Trend: more frequent = healthier process
# 3. Change failure rate — % of deploys that cause incidents
#    Trend: increasing = quality gap
# 4. Mean time to recovery (MTTR) — how fast you fix incidents
#    Trend: decreasing = better ops maturity

# Find the bottleneck (Theory of Constraints):
# 1. Identify the constraint — which stage has the biggest queue?
#    (Is it code review? Testing? Deployment?)
# 2. Exploit the constraint — maximize throughput at the bottleneck
#    (e.g., if review is slow: make PRs smaller, add review SLA)
# 3. Subordinate everything else — don't produce more than the bottleneck can handle
#    (limit WIP so work doesn't pile up in front of the bottleneck)
# 4. Elevate the constraint — add capacity (automate, hire, train)
# 5. Repeat — find the next constraint
```

### Effective Retrospectives (That Actually Change Things)

```markdown
## Retro format that produces real improvement:

### 1. Set the stage (2 min)
- "We're here to improve how we work. Be honest, be constructive."

### 2. Gather data (5 min)
- **What went well?** (keep doing)
- **What didn't go well?** (change or stop)
- **What's confusing/unclear?** (clarify)

### 3. Generate insights (5 min)
- "Where's the biggest friction in our workflow right now?"
- "What slows us down the most?"

### 4. Decide what to do (5 min)
- Pick 1–2 action items (not 10)
- Make them SPECIFIC and OWNED:
  ❌ "Improve code review" (vague, nobody owns it)
  ✅ "Shumon will set up CODEOWNERS and a review SLA of <4 business hours
      by next Friday (Linear #789)"

### 5. Track completion
- Review last retro's action items at the start of the next retro
- "Did we do what we said we'd do?"
- If not, why not? (too ambitious? not prioritized? forgotten?)
```

### Automating Quality Gates (Process Enforced by Tools)

```yaml
# CI pipeline — quality gates that run on EVERY change
# Process enforced automatically = no human needs to remember:
jobs:
  lint:
    steps:
      - run: ruff check .            # style + common bugs
      - run: prettier --check .      # formatting
  type-check:
    steps:
      - run: tsc --noEmit           # TypeScript type safety
      - run: mypy app/               # Python type safety
  test:
    steps:
      - run: pytest --cov=app        # unit + integration tests
  security:
    steps:
      - run: gitleaks detect         # no committed secrets
      - run: pip-audit               # no known vulnerable deps
  build:
    steps:
      - run: docker build -t app .   # build succeeds (immutable artifact)

# PR rules (enforced in repo settings):
# - Must pass all CI checks before merge
# - At least one approving review
# - Branch must be up-to-date with main
```

### Estimation That Works (Without Being a Burden)

```markdown
## The goal of estimation isn't precision — it's alignment.

### T-shirt sizing (fast, rough):
- S = hours, M = 1–3 days, L = ~1 week, XL = >1 week

### Story points (relative, not hours):
- Use reference stories: "this is about the size of [shipping last month's X feature]"
- Estimate as a team (planning poker) — avoids individual bias
- Track velocity over time — how many points per sprint? (don't compare across teams)

### Estimation anti-patterns:
- ❌ Converting points to hours — defeats the purpose
- ❌ Estimating alone — individual estimates are inaccurate
- ❌ Using velocity as a performance metric — creates gaming, bad behavior
- ❌ 100% precision upfront — estimates improve as you learn

### Good enough:
- "Will this fit in one sprint? Yes/No/Maybe" — often all you need
- For larger estimates: t-shirt size + buffer for uncertainty
- For stakeholders: always give a range, never a single date
```

### Development Process Optimization Checklist

- [ ] **Process matches team size and work type** — Scrum for feature teams, Kanban for ops/support, simple backlog for small teams
- [ ] **Ceremonies are useful** — if a meeting isn't providing value, change or drop it
- [ ] **WIP limited** — the team finishes before starting new work
- [ ] **Bottlenecks identified** and actively addressed (not just accepted)
- [ ] **Retrospectives produce action items** — specific, owned, tracked, reviewed
- [ ] **Quality gates automated** — lint, type-check, test, security scan in CI
- [ ] **Code review SLA** — PRs reviewed within agreed timeframe
- [ ] **Deployment automated** — CI/CD pipeline, not manual steps
- [ ] **Process measured** — cycle time, deployment frequency, failure rate (pick 2–3)
- [ ] **Process continuously improved** — retrospectives that change things

### Avoid These

- **Process for process's sake** — ceremonies that no one finds useful
- **Rigid Scrum** — "Scrum says we must…" without evaluating whether it helps
- **No retrospectives** — the team never reflects; the same problems persist for years
- **Retro action items unowned** — "we should…" with no who or when
- **Over-measurement** — tracking 15 metrics; nobody acts on any of them
- **Estimation as performance review** — using story points to evaluate individuals
- **Ignoring the bottleneck** — optimizing stages that aren't the constraint
- **Allowing WIP to balloon** — everyone busy, nothing shipping (busy ≠ productive)
- **Process by edict** — imposed from above without team buy-in
- **No process at all** — "we're agile" (meaning: no planning, no tracking, chaos)
