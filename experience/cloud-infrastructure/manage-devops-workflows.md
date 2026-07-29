# Manage DevOps Workflows

> **Category:** Cloud & Infrastructure
> **Relevant at:** MVI Solutions (Git, CI/CD pipelines, deployment processes)
> **Related tech docs:** `case/devops/devops-and-cicd.md` (Git §1–11, CI/CD §23–33, GitHub Actions §34–44), `case/iac/iac-tools.md` (CDK §1–11, Terraform §12–22)

---

## 1. What This Means

Managing DevOps workflows means owning the **release pipeline** — Git-based version control, CI/CD automation, and deployment processes — so that code moves from development to production **reliably, repeatedly, and with minimal manual intervention**.

**Scope:**
- **Git workflow** — branching strategy, code review, merge policies, history hygiene
- **CI/CD pipelines** — automated build, test, and deploy stages
- **Deployment processes** — staging environments, rollout strategies, rollback
- **Environment management** — dev/staging/prod parity and promotion
- **Release reliability** — zero-downtime deploys, fast rollbacks, audit trail

**Why it matters:** a broken release process is a business risk — bad deploys cause downtime, lost data, and lost trust. A strong DevOps workflow turns releases from a risky manual event into a routine, boring, automated operation.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The Git → CI/CD → Production flow:**
```
Developer commits to feature branch
   → opens Pull Request
      → CI runs (lint, test, build) — blocks merge on failure
         → review + merge to main
            → CD deploys to staging automatically
               → manual/automated promotion to production
                  → monitoring + rollback if needed
```

**What "managing" means in practice:**
- **Git workflow:** defining the branching model (feature branches, trunk-based), enforcing PR reviews, protecting the main branch
- **CI pipeline:** ensuring every push/PR triggers lint + tests + build within minutes
- **CD pipeline:** automated staging deploys on merge; controlled production rollouts
- **Deployment strategy:** choosing rolling, blue/green, or canary for zero-downtime
- **Rollback:** having a tested, fast way to revert a bad deploy

**Real-world scenarios:**
- A hotfix needs to reach production in minutes — the pipeline automates build → test → deploy
- A bad deploy causes errors — blue/green or automated rollback reverts in seconds
- A junior developer breaks the build — CI catches it before merge, main stays green
- Onboarding a new developer — the Git workflow + pipeline are documented, so they're productive day one

**The principle:** **if it's not automated, it's not repeatable.** Manual deploy steps are liabilities — they're error-prone, undocumented, and impossible to audit.

---

## 3. How to Implement

### Git Workflow — Branch, Review, Merge

```bash
# Feature branch workflow
git checkout -b feature/payment-refunds
# ... develop ...
git add -A && git commit -m "feat: add payment refund endpoint"
git push origin feature/payment-refunds

# Open PR → CI runs → review → merge to main → CD deploys
# Main branch is protected: no direct pushes, requires passing CI + review
```

**Branch protection rules:**
- Require pull request reviews before merging
- Require status checks (CI) to pass before merging
- Require branches to be up-to-date before merging
- No force pushes to main

### CI Pipeline (GitHub Actions)

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt
      - run: ruff check .                    # lint — fast feedback first
      - run: pytest --cov=app                # tests
      - run: docker build -t app .           # build the image
```

### CD Pipeline — Automated Deploy

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]          # deploy when merged to main
jobs:
  deploy:
    needs: test               # only deploy if tests pass
    steps:
      - run: docker push $IMAGE_TAG
      - run: |
          # Deploy to staging (automatic)
          aws ecs update-service --cluster prod --service app --task-def new-def
          # Production promotion (manual approval gate or auto after health checks)
```

### Deployment Strategies

```bash
# Rolling — replace instances one by one (zero downtime with health checks)
aws ecs update-service --service app --deployment-controller type=ECS

# Blue/Green — new stack fully up before traffic switch (instant rollback)
aws codedeploy create-deployment --deployment-config-name CodeDeployDefault.ECSAllAtOnce

# Canary — small % of traffic first, ramp up if healthy
# (route via API Gateway weighted routing or App Mesh)
```

### Rollback

```bash
# Fast rollback — redeploy the previous task definition/image
aws ecs update-service --service app --task-def previous-def

# Blue/Green rollback — switch traffic back to the old (blue) stack
aws codedeploy stop-deployment --deployment-id $ID --auto-rollback-enabled
```

### DevOps Workflow Checklist

- [ ] **Git branching strategy** defined (feature branches / trunk-based)
- [ ] **Main branch protected** — no direct pushes, PR + CI required
- [ ] **CI on every PR** — lint + tests + build in minutes
- [ ] **CD on merge** — automated staging deploy
- [ ] **Production deploy** requires approval gate or passes health checks
- [ ] **Zero-downtime strategy** (rolling / blue-green / canary)
- [ ] **Tested rollback** — rehearsed and fast
- [ ] **Secrets in platform secret store**, never in pipeline code
- [ ] **Immutable artifacts** — build once, promote through environments
- [ ] **Pipeline as code** — versioned in the repo, reviewed in PRs
- [ ] **Monitoring post-deploy** — smoke tests, health checks, alerting

### Avoid These

- **Direct pushes to main** — bypasses review and CI
- **Manual deploy steps** — error-prone, unrepeatable, unauditable
- **No rollback strategy** — a bad deploy means downtime while you scramble
- **Slow CI** — developers lose trust and skip waiting for it
- **Secrets in pipeline code** — credentials in YAML/repo
- **Building per-environment** — build once, promote (same artifact everywhere)
- **No staging environment** — production is the first place you test
- **Deploying from laptops** — all deploys should go through the pipeline
