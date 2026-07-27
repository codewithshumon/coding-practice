# DevOps & CI/CD — Complete Guide

> **Series:** DevOps Documentation — Part 1
> This file covers the **core DevOps tools and practices**: Git (version control), Docker (containerization), CI/CD Pipelines + Automated Deployments (workflow discipline), GitHub Actions, AWS CodePipeline, and Linux (server proficiency). More topics (Terraform ops, Kubernetes, monitoring/observability) will be added as separate files later.

---

## Table of Contents

- [Shared Orientation — The DevOps Pipeline](#shared-orientation--the-devops-pipeline)
- **Git**
  - [1. What Is Git?](#1-what-is-git)
  - [2. Git vs Other VCS](#2-git-vs-other-vcs)
  - [3. How Git Works](#3-how-git-works)
  - [4. Git Commands and Workflows](#4-git-commands-and-workflows)
  - [5. Where Git Is Essential](#5-where-git-is-essential)
  - [6. Where Git Falls Short](#6-where-git-falls-short)
  - [7. Installing and Setting Up Git](#7-installing-and-setting-up-git)
  - [8. Git Authentication and Remotes](#8-git-authentication-and-remotes)
  - [9. Git Production Best Practices](#9-git-production-best-practices)
  - [10. Git Real-World Examples](#10-git-real-world-examples)
  - [11. Git Pitfalls](#11-git-pitfalls)
- **Docker**
  - [12. What Is Docker?](#12-what-is-docker)
  - [13. Docker vs Virtual Machines](#13-docker-vs-virtual-machines)
  - [14. How Docker Works](#14-how-docker-works)
  - [15. Docker Key Concepts](#15-docker-key-concepts)
  - [16. Where to Use Docker](#16-where-to-use-docker)
  - [17. Where NOT to Use Docker](#17-where-not-to-use-docker)
  - [18. Installing and Setting Up Docker](#18-installing-and-setting-up-docker)
  - [19. Docker Registries and Image Management](#19-docker-registries-and-image-management)
  - [20. Docker Production Best Practices](#20-docker-production-best-practices)
  - [21. Docker Real-World Examples](#21-docker-real-world-examples)
  - [22. Docker Pitfalls](#22-docker-pitfalls)
- **CI/CD Pipelines & Automated Deployments**
  - [23. What Is CI/CD?](#23-what-is-cicd)
  - [24. CI/CD vs Manual Deployments](#24-cicd-vs-manual-deployments)
  - [25. How CI/CD Works](#25-how-cicd-works)
  - [26. CI/CD Pipeline Stages](#26-cicd-pipeline-stages)
  - [27. Where CI/CD Matters](#27-where-cicd-matters)
  - [28. Where CI/CD May Be Overkill](#28-where-cicd-may-be-overkill)
  - [29. CI/CD Pipeline Setup Principles](#29-cicd-pipeline-setup-principles)
  - [30. Deployment Strategies](#30-deployment-strategies)
  - [31. CI/CD Best Practices](#31-cicd-best-practices)
  - [32. CI/CD Real-World Examples](#32-cicd-real-world-examples)
  - [33. CI/CD Pitfalls](#33-cicd-pitfalls)
- **GitHub Actions**
  - [34. What Is GitHub Actions?](#34-what-is-github-actions)
  - [35. GitHub Actions vs Other CI/CD Platforms](#35-github-actions-vs-other-cicd-platforms)
  - [36. How GitHub Actions Works](#36-how-github-actions-works)
  - [37. GitHub Actions Key Concepts](#37-github-actions-key-concepts)
  - [38. Where to Use GitHub Actions](#38-where-to-use-github-actions)
  - [39. Where NOT to Use GitHub Actions](#39-where-not-to-use-github-actions)
  - [40. Setting Up GitHub Actions](#40-setting-up-github-actions)
  - [41. GitHub Actions Secrets and Permissions](#41-github-actions-secrets-and-permissions)
  - [42. GitHub Actions Production Best Practices](#42-github-actions-production-best-practices)
  - [43. GitHub Actions Real-World Examples](#43-github-actions-real-world-examples)
  - [44. GitHub Actions Pitfalls](#44-github-actions-pitfalls)
- **AWS CodePipeline**
  - [45. What Is AWS CodePipeline?](#45-what-is-aws-codepipeline)
  - [46. CodePipeline vs GitHub Actions vs Jenkins](#46-codepipeline-vs-github-actions-vs-jenkins)
  - [47. How CodePipeline Works](#47-how-codepipeline-works)
  - [48. CodePipeline Key Concepts](#48-codepipeline-key-concepts)
  - [49. Where to Use CodePipeline](#49-where-to-use-codepipeline)
  - [50. Where NOT to Use CodePipeline](#50-where-not-to-use-codepipeline)
  - [51. Setting Up CodePipeline](#51-setting-up-codepipeline)
  - [52. CodePipeline Access and Auth](#52-codepipeline-access-and-auth)
  - [53. CodePipeline Production Best Practices](#53-codepipeline-production-best-practices)
  - [54. CodePipeline Real-World Examples](#54-codepipeline-real-world-examples)
  - [55. CodePipeline Pitfalls](#55-codepipeline-pitfalls)
- **Linux**
  - [56. What Is Linux (for DevOps)?](#56-what-is-linux-for-devops)
  - [57. Linux vs Other Server OSs](#57-linux-vs-other-server-oss)
  - [58. Core Linux Server Skills](#58-core-linux-server-skills)
  - [59. Shell Scripting Essentials](#59-shell-scripting-essentials)
  - [60. Where Linux Proficiency Matters](#60-where-linux-proficiency-matters)
  - [61. Where Linux Is the Wrong Platform](#61-where-linux-is-the-wrong-platform)
  - [62. Linux Server Best Practices](#62-linux-server-best-practices)
  - [63. Linux Real-World Examples](#63-linux-real-world-examples)
  - [64. Linux Pitfalls](#64-linux-pitfalls)
- [Shared Foundations](#shared-foundations)
- [Quick Reference Card](#quick-reference-card)

---

## Shared Orientation — The DevOps Pipeline

These six topics form a delivery pipeline — from source code to running production services:

| Stage | Topic | One-liner |
|---|---|---|
| **Source** | Git | Version control — where everything starts |
| **Package** | Docker | Containerize the app (consistent everywhere) |
| **Automate** | CI/CD Pipelines + Deployments | Build, test, deploy — automatic and repeatable |
| **CI Platform** | GitHub Actions | GitHub-native CI workflows |
| **CI Platform** | AWS CodePipeline | AWS-managed CI/CD for AWS workloads |
| **Run** | Linux | The OS where most of this actually runs |

**Rule of thumb:** the flow is **Git → Docker → CI/CD (Actions/CodePipeline) → Linux server**. The CI/CD pipeline is the central orchestrator — it pulls from Git, builds Docker images, and deploys to Linux.

**The two CI platforms are alternatives:** GitHub Actions for GitHub-centric workflow automation; AWS CodePipeline for AWS-centric, managed CI/CD with deep AWS integration. Use both where appropriate — Actions for PR checks, CodePipeline for production AWS deployments.

---

# Git

## 1. What Is Git?

**Git** is a **distributed version control system** (DVCS) for tracking source code changes, enabling **branching, merging, and collaborative workflows** — the foundation of modern software development.

**One-liner:** the universal version-control backbone of modern development.

## 2. Git vs Other VCS

| | Git | Older VCS (SVN, CVS) |
|---|---|---|
| Model | Distributed (every clone is full repo) | Centralized (one server) |
| Branching | Lightweight, first-class | Heavy, folder-like |
| Adoption | Universal | Legacy |

**Rule of thumb:** Git is the standard. There's no practical alternative for new projects.

## 3. How Git Works

- Commits are **snapshots** of the project at a point in time, forming a **DAG** (directed acyclic graph).
- **Branches** are lightweight movable pointers to commits.
- **Merging and rebasing** integrate changes between branches.
- **Remotes** are references to other repositories (origin, upstream).

**Key point:** everything is local until you `push` — fast, offline-capable. The distributed model means every clone is a backup.

## 4. Git Commands and Workflows

| Area | Key commands |
|---|---|
| **Daily** | `add`, `commit`, `push`, `pull`, `status`, `log` |
| **Branching** | `branch`, `checkout`/`switch`, `merge`, `rebase` |
| **Undo** | `reset`, `revert`, `checkout -- <file>`, `stash` |
| **Workflows** | GitFlow, trunk-based, GitHub Flow |
| **Advanced** | `cherry-pick`, `reflog`, `bisect`, `squash` |

## 5. Where Git Is Essential

- **Every software project** — it's the default expectation.
- **Collaboration** — branches, pull requests, code review.
- **History and audit trail** — `git log`, `git blame`, `bisect`.

## 6. Where Git Falls Short

- **Large binary files** (use Git LFS).
- **Huge monorepos** without tooling help.

## 7. Installing and Setting Up Git

```bash
# Install (apt/brew/download), then:
git config --global user.name "Name" && git config --global user.email "email"
git init / git clone <url>
git add . && git commit -m "message"
git push origin main
```

## 8. Git Authentication and Remotes

- **SSH keys** — recommended for secure, password-less access.
- **HTTPS + Personal Access Tokens (PAT)**.
- **Multiple remotes** — `origin` (your fork), `upstream` (original).

**Golden rule:** never commit credentials; use SSH keys or PATs, and `.gitignore` sensitive files.

## 9. Git Production Best Practices

1. **Write meaningful commit messages** — what and why.
2. **Small, focused commits** — reviewable and revertible.
3. **Branch per feature** — use a consistent workflow (feature branches, trunk-based).
4. **Pull request + review** before merging to stable branches.
5. **Protect main/master** — require reviews, passing CI.
6. **`.gitignore`** sensitive and generated files.
7. **Learn `reflog`** — it saves you when things go wrong.

## 10. Git Real-World Examples

### Example 1 — Feature Branch Workflow
```
main ← feature/login → PR → review → merge → delete branch
```
**Why:** isolates work, enables review, keeps main stable.

### Example 2 — `git bisect` to Find a Bug
**Why:** binary search through commits to find exactly which one introduced a regression — fast root-cause.

## 11. Git Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Committed secrets | Credentials in history | Rotate secrets, `BFG`/`filter-branch` to clean |
| Large, bad commit messages | Unclear history | Meaningful messages |
| Not branching/protecting | Direct pushes to main | Branch + protect main |
| Merge-conflict-heavy habits | Painful integration | Frequent pulls, small commits |
| Ignoring `.gitignore` | Generated/secrets files tracked | Set up early |

---

# Docker

## 12. What Is Docker?

**Docker** is a **containerization platform** that packages applications and their dependencies into **lightweight, portable containers** — running consistently on any machine.

**One-liner:** package once, run anywhere — without virtual-machine overhead.

## 13. Docker vs Virtual Machines

| | Docker Containers | Virtual Machines |
|---|---|---|
| Isolation | Process-level (shares host kernel) | Full OS per VM |
| Overhead | Minimal (MBs, fast start) | Heavier (GBs, slow boot) |
| Speed | Near-native | Virtualized |
| Portability | "Works on my machine" = everywhere | Heavier to move |

**Rule of thumb:** Docker for **app packaging and deployment**; VMs for **full OS isolation** or running different kernels.

## 14. How Docker Works

1. A **Dockerfile** declares the image build steps.
2. `docker build` creates a layered **image**.
3. `docker run` creates a **container** from the image.
4. Containers share the host kernel but run in **isolated namespaces** (process, network, filesystem).

**Key point:** images are immutable + layered (caching); containers are ephemeral by default.

## 15. Docker Key Concepts

| Concept | What it is |
|---|---|
| **Image** | Immutable, layered snapshot of an app + deps |
| **Container** | A running instance of an image |
| **Dockerfile** | Build instructions (FROM, COPY, RUN, CMD) |
| **Registry** | Store/share images (Docker Hub, ECR) |
| **Volume** | Persistent data (outside the container lifecycle) |
| **Compose** | Multi-container app definitions |

## 16. Where to Use Docker

- **Consistent local dev** across a team.
- **CI/CD pipelines** — build/test in isolated, reproducible environments.
- **Production deployment** — same image from dev to prod.
- **Local testing of cloud services** — AWS LocalStack, Redis, Postgres (see `aws.md`, `caching.md`, `database/databases.md` for Docker setup examples).
- **Multi-service apps** via Docker Compose.

## 17. Where NOT to Use Docker

- Need **full kernel-level isolation** (use VMs).
- **Very lightweight/simple CLI tools** where container overhead is overkill.
- **Persistent state** without careful volume management.

## 18. Installing and Setting Up Docker

```bash
# Docker Engine (see docs.docker.com) + Compose
docker version && docker compose version

# Build and run
echo 'FROM python:3.12-slim\nCOPY app.py .\nCMD ["python","app.py"]' > Dockerfile
docker build -t my-app . && docker run my-app
```

## 19. Docker Registries and Image Management

- **Docker Hub** (default, public), **AWS ECR**, **GCR**, private registries.
- `docker push` / `docker pull` to share images.
- **Version with tags** — never rely on `:latest` in production.
- **Authenticate** (`docker login`) for private registries.

## 20. Docker Production Best Practices

1. **Multi-stage builds** — keep final images small (separate build deps).
2. **Pin base images** by digest, not just tag.
3. **One process per container** — Docker way.
4. **Don't run as root** inside the container.
5. **Use volumes** for persistent data; don't store data in the container.
6. **Never put secrets in images** — pass via env, secrets manager, or mounted volumes.
7. **Health checks** — `HEALTHCHECK` in Dockerfile.

## 21. Docker Real-World Examples

### Example 1 — Multi-Stage Build
```dockerfile
FROM node:20 AS build
COPY . . && npm ci && npm run build

FROM node:20-slim
COPY --from=build /dist ./dist && CMD ["node","dist/server.js"]
```
**Why:** final image is slim (no dev deps/toolchain) — smaller, faster, more secure.

### Example 2 — Compose: App + DB + Cache
```yaml
services:
  app: { build: ., ports: ["3000:3000"] }
  db:  { image: postgres:15, volumes: ["pg-data:/var/lib/postgresql/data"] }
  redis: { image: redis:7 }
```
**Why:** one command (`docker compose up`) brings up the full stack — consistent across all dev environments.

## 22. Docker Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| `:latest` tag in production | Unexpected version changes | Pin tags/digests |
| Data in containers (no volumes) | Data loss on restart | Use volumes |
| Running as root | Security escalation risk | Use a non-root USER |
| Bloated images | Slow builds and pulls | Multi-stage builds |
| Secrets in image layers | Leaked credentials | Pass at runtime |

---

# CI/CD Pipelines & Automated Deployments

## 23. What Is CI/CD?

**CI/CD (Continuous Integration / Continuous Delivery)** is the practice of automating the **build, test, and deployment** pipeline so code changes flow to production **reliably, repeatedly, and with minimal manual intervention**.

- **CI:** merge → build → test automatically (catch problems early).
- **CD:** tested changes are automatically deployed to staging/production.

**One-liner:** code to production — automatic, repeatable, and safe.

## 24. CI/CD vs Manual Deployments

| | CI/CD | Manual Deployments |
|---|---|---|
| Speed | Minutes | Hours/days |
| Reliability | Consistent, tested | Error-prone |
| Rollback | Automated | Manual scramble |
| Feedback | Immediate (tests pass/fail) | Delayed |

**Rule of thumb:** if it's not automated, it's not repeatable. Manual deploys are a risk, not a process.

## 25. How CI/CD Works

1. **Push triggers** the pipeline (commit to a branch).
2. **Build** — compile, install deps, build artifacts.
3. **Test** — lint, unit, integration tests.
4. **Stage / approve** — deploy to a staging environment.
5. **Deploy to production** — with automated validation and rollback capability.

**Key point:** the pipeline is the **single source of truth** for "what's in production." All changes go through it.

## 26. CI/CD Pipeline Stages

| Stage | What happens |
|---|---|
| **Source** | Code change triggers the pipeline |
| **Build** | Compile, bundle, build Docker image |
| **Test** | Lint, unit tests, integration tests |
| **Stage** | Deploy to a staging environment for manual/automated QA |
| **Deploy** | Promote to production (possibly with canary/blue-green) |
| **Validate** | Smoke tests, health checks, monitoring |

## 27. Where CI/CD Matters

- **Every team shipping software** — it's the modern baseline.
- **Zero-downtime deployments** — automated rollouts replace risky manual updates.
- **Frequent releases** — enables shipping multiple times a day.

## 28. Where CI/CD May Be Overkill

- Prototypes and throwaway code.
- Truly static applications that rarely change.

## 29. CI/CD Pipeline Setup Principles

- **Pipeline as code** — defined in the repo (`.github/workflows/`, `buildspec.yml`, CDK, Jenkinsfile).
- **Idempotent** — rerunning the pipeline doesn't cause side effects.
- **Fast feedback** — linting + unit tests in minutes; longer tests later.
- **Immutable artifacts** — build once, promote through environments (same Docker image).

## 30. Deployment Strategies

| Strategy | How it works | Best for |
|---|---|---|
| **Rolling** | Replace one by one | Simple, with health checks |
| **Blue/Green** | New stack → switch traffic | Instant rollback |
| **Canary** | Small % → ramp up | Risk reduction |

## 31. CI/CD Best Practices

1. **Pipeline as code** — versioned with the app.
2. **Fast CI feedback** — linting + unit tests in < 10 min.
3. **Immutable artifacts** — build once, promote.
4. **Zero-downtime deploys** — rolling, blue/green, or canary.
5. **Automated rollbacks** — deploy fails → revert automatically.
6. **Secrets out of pipeline code** — platform secret stores.
7. **Monitor post-deploy** — smoke tests and health checks.

## 32. CI/CD Real-World Examples

### Example 1 — Full Pipeline
```
Push → lint + test → build Docker image → deploy to staging → deploy to prod (rolling)
```
**Why:** every step is automated; no one clicks "deploy" from a laptop.

### Example 2 — Blue/Green Zero-Downtime
**Why:** the new stack is fully up before traffic switches — instant cutover and instant rollback.

## 33. CI/CD Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Manual deploy steps | Human error, inconsistency | Automate the full pipeline |
| Secrets in pipeline code | Leaked credentials | Platform secret stores |
| No rollback strategy | Downtime on bad deploy | Blue/green, rolling with rollback |
| Slow CI | Devs skip/wait | Parallelize, separate fast/slow checks |
| Deploying from laptops | Untracked, risky | All deploys via pipeline |

---

# GitHub Actions

## 34. What Is GitHub Actions?

**GitHub Actions** is GitHub's built-in **CI/CD platform** — automate builds, tests, and deployments directly from your repository via YAML workflow files.

**One-liner:** CI/CD natively integrated with GitHub repos.

## 35. GitHub Actions vs Other CI/CD Platforms

| | GitHub Actions | AWS CodePipeline | Jenkins |
|---|---|---|---|
| Hosting | Managed (GitHub) | Managed (AWS) | Self-hosted |
| Integration | Native GitHub (PRs, issues) | Native AWS | Open-ended |
| Best for | GitHub projects | AWS-heavy pipelines | Complex custom pipelines |

**Rule of thumb:** **GitHub Actions** for GitHub-centric CI/CD; **CodePipeline** for AWS-native pipelines.

## 36. How GitHub Actions Works

1. A **workflow** YAML file in `.github/workflows/` defines triggers and jobs.
2. Triggers: `push`, `pull_request`, schedule, manual.
3. Jobs run on **GitHub-hosted runners** (or self-hosted).
4. Steps: checkout code → setup → build → test → deploy.

**Key point:** lives in the repo. A PR can add/change the CI pipeline right alongside the code.

## 37. GitHub Actions Key Concepts

- **Workflow** — the pipeline (`.github/workflows/ci.yml`).
- **Job** — a group of steps on one runner.
- **Step** — an action or shell command.
- **Actions** — reusable building blocks (from the marketplace).
- **Secrets** — encrypted vars (`${{ secrets.XXX }}`).
- **Matrix** — run a job across many configurations.

## 38. Where to Use GitHub Actions

- **CI** — test on every push/PR (lint, unit, build).
- **CD** — deploy to staging/production.
- **Scheduled jobs** (cron-like).
- **Release automation** — npm publish, Docker push, tag/release.

## 39. Where NOT to Use GitHub Actions

- **AWS-heavy, complex multi-stage deployments** (CodePipeline may be a better fit).
- **Non-GitHub source** repos.

## 40. Setting Up GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci && npm test
```

## 41. GitHub Actions Secrets and Permissions

- **Secrets** — stored encrypted in repo/org settings, passed via `${{ secrets.XXX }}`.
- **Permissions** — `GITHUB_TOKEN` for repo operations (scoped, auto-generated).
- **Never log or echo secrets.**

## 42. GitHub Actions Production Best Practices

1. **Pin action versions** (by tag or SHA) — never `@main`.
2. **Use matrix** for multi-config testing.
3. **Cache dependencies** (`actions/cache`) for speed.
4. **Secrets in repo/org settings** — never in workflow files.
5. **Fast feedback first** — lint/tests early; slow jobs later.
6. **Review workflow changes in PRs** — pipeline code, not just app code.

## 43. GitHub Actions Real-World Examples

### Example 1 — CI on PR
**Why:** on every PR: lint → test → build — blocks merge on failure.

### Example 2 — Deploy on Merge to Main
**Why:** merge to main → build Docker image → push to ECR → deploy to ECS — full CD from GitHub.

## 44. GitHub Actions Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Unpinned actions | Breaking changes | Pin by version/SHA |
| Secrets in workflow YAML | Leaked in plain text | Use `secrets.XXX` |
| Non-cached deps | Slow CI | Cache node_modules, pip, etc. |
| No workflow review | Pipeline changes un-reviewed | Review `.github/workflows/` in PRs |

---

# AWS CodePipeline

## 45. What Is AWS CodePipeline?

**AWS CodePipeline** is a **fully managed CI/CD service** that automates the **build, test, and deploy stages** of your release process — deeply integrated with AWS services.

**One-liner:** AWS-managed continuous delivery for AWS workloads.

## 46. CodePipeline vs GitHub Actions vs Jenkins

| | CodePipeline | GitHub Actions | Jenkins |
|---|---|---|---|
| Hosting | AWS managed | GitHub managed | Self-hosted |
| AWS integration | Deepest (CodeBuild, ECS, Lambda) | Via AWS CLI/actions | Via plugins |
| Best for | AWS-native pipelines | GitHub-native CI/CD | Complex custom pipelines |

**Rule of thumb:** **CodePipeline** for production AWS deployments with deep AWS integration; **GitHub Actions** for PR checks and non-AWS-heavy workflows.

## 47. How CodePipeline Works

1. A **source stage** triggers on a git change (CodeCommit, GitHub, S3).
2. A **build stage** runs (CodeBuild or Jenkins) — compile, test, build artifact.
3. A **deploy stage** pushes to target (ECS, Lambda, S3, CloudFormation).
4. Each stage can have **manual approval** gates.

**Key point:** CodePipeline orchestrates the stages — the actual building and deploying is done by **CodeBuild** and deployment services.

## 48. CodePipeline Key Concepts

- **Pipeline** — the orchestrated release flow.
- **Stage** — a phase (Source → Build → Test → Deploy → Approve).
- **Action** — what happens in a stage (CodeBuild, CloudFormation, manual approval, etc.).
- **Artifacts** — files passed between stages (S3-backed).
- **Transitions** — can be auto or manual-approval.

## 49. Where to Use CodePipeline

- **AWS-native deployments** — directly to ECS, Lambda, S3, CloudFormation.
- **Auto-Deploy on push** with CDK/CloudFormation integration.
- When you want a **fully managed** pipeline with no runner infrastructure.

## 50. Where NOT to Use CodePipeline

- **Non-AWS** deployment targets.
- **Simple PR checks** where GitHub Actions is lighter and faster.

## 51. Setting Up CodePipeline

Via Console, CloudFormation, or CDK:

```typescript
// CDK pipeline
new pipelines.CodePipeline(this, "Pipeline", {
  synth: new pipelines.ShellStep("Synth", { ... }),
});
```

For CDK pipelines specifically, see `aws.md` §12–22 and `iac/iac-tools.md` §1–11.

## 52. CodePipeline Access and Auth

- **IAM roles** — the pipeline, CodeBuild, and deploy actions each need scoped permissions.
- **Secrets** via AWS Secrets Manager / SSM Parameter Store.
- **Manual approvals** via SNS notification or console.

## 53. CodePipeline Production Best Practices

1. **Pipeline as code** — define it in CDK or CloudFormation.
2. **Immutable artifacts** — build once, deploy to each environment.
3. **Manual approval gates** before production.
4. **Separate accounts** for dev/staging/production pipelines.
5. **Monitor pipeline execution** — CloudWatch events on failures.
6. **Store secrets in Secrets Manager**, not in pipeline configuration.

## 54. CodePipeline Real-World Examples

### Example 1 — Source → Build → Deploy
```
Git Push → CodeBuild (compile + test + Docker build) → Deploy to ECS (rolling update)
```
**Why:** fully automated AWS-native pipeline — code push to production in minutes.

### Example 2 — Multi-Environment with Approval
```
Source → Build → Deploy-Stage → Manual Approval → Deploy-Prod
```
**Why:** promote to staging automatically, require an explicit approval gate before production.

## 55. CodePipeline Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Broad IAM roles | Over-permission | Least-privilege pipeline roles |
| No manual approval gate | Push goes straight to prod | Add approval stages |
| Pipeline not as code | Snowflake pipelines | Define in CDK/CFN |
| Slow builds | Long feedback | Optimize build + parallelize |

---

# Linux

## 56. What Is Linux (for DevOps)?

**Linux** is the **dominant server operating system** — proficiency meaning shell scripting, process management, and system administration for running and debugging production services.

**One-liner:** the OS running your servers, containers, and CI runners.

## 57. Linux vs Other Server OSs

| | Linux | Windows Server | macOS |
|---|---|---|---|
| Servers | Dominant | Enterprise/Microsoft | Desktop/dev only |
| Cost | Free (open-source) | Licensed | Hardware-locked |
| Cloud | Universal | Supported | Not supported |

**Rule of thumb:** Linux is the default server OS in cloud, containers, and CI — proficiency is a baseline DevOps skill.

## 58. Core Linux Server Skills

| Skill | What you do |
|---|---|
| **Shell / bash** | Write scripts, automate tasks |
| **Process management** | `ps`, `top`, `htop`, `kill`, signal handling |
| **File system** | Navigating, permissions (`chmod`, `chown`), `find`, `grep` |
| **Systemd / services** | Managing services (`systemctl`), journal/logs (`journalctl`) |
| **Networking** | `curl`, `ss`, `iptables`, `tcpdump` basics |
| **Package management** | `apt`, `yum` — install, update, remove |
| **SSH** | Remote access, key management |

## 59. Shell Scripting Essentials

```bash
#!/bin/bash
set -euo pipefail    # safe defaults: exit on error, unset vars, pipe failures

for dir in */; do
  echo "Processing $dir..."
done

if [ -f "config.txt" ]; then
  source ./config.txt
fi
```

**Key point:** `set -euo pipefail` is the safe-bash golden rule — it prevents silent failures in scripts.

## 60. Where Linux Proficiency Matters

- **Debugging production issues** (logs, process state, network).
- **Writing CI/CD scripts** and server automation.
- **Managing Docker hosts** (Linux is the container runtime).
- **Server administration** and security hardening.

## 61. Where Linux Is the Wrong Platform

- **Desktop applications** — each OS for its users.
- **WSL / CI runners** — both are ubiquitous.

## 62. Linux Server Best Practices

1. **Use `set -euo pipefail`** in every script.
2. **SSH keys, not passwords** — more secure and automatable.
3. **Principle of least privilege** — run services as their own users, not root.
4. **Rotate logs** (`logrotate`), monitor disk and memory (`df`, `free`).
5. **Automate updates** (security patches).

## 63. Linux Real-World Examples

### Example 1 — Shell Script for CI
**Why:** a bash script runs tests and deploys — standard, portable, universally understood by CI tools.

### Example 2 — Debugging a Production Service
**Why:** `systemctl status`, `journalctl -u service-name -f`, `htop` — the trinity of production debugging.

## 64. Linux Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Scripts without error handling | Silent failures | `set -euo pipefail` |
| Running as root | Security risk | App-specific users |
| No log rotation | Disk fills up | `logrotate` + monitoring |
| SSH password auth | Brute-force risk | SSH keys only |

---

## Shared Foundations

Concepts that recur across **all DevOps topics**:

- **Automation is the goal** — manual steps are liabilities. Git enables collaboration, Docker standardizes packaging, CI/CD automates delivery, and Linux scripting ties it together.
- **Reproducibility** — the same code, environment, and pipeline produce the same result every time. Docker images, pipeline-as-code, and scripting achieve this.
- **Secrets management** — credentials belong in secret stores, never in code, repos, images, or scripts.
- **Code, config, and pipeline — all version-controlled** — Git doesn't just track source; it tracks Dockerfiles, CI workflows, and IaC definitions (see `iac/iac-tools.md`).
- **The pipeline as the single source of truth** — only what goes through the CI/CD pipeline reaches production. No ad-hoc deploys.

## Quick Reference Card

```
DEVOPS FLOW:
  Git → source code
  Docker → package
  CI/CD Pipeline → automate (build → test → deploy)
  GitHub Actions / CodePipeline → CI platform
  Linux → runs it all

VERSION CONTROL:
  ✓ Branch per feature, PR + review, protect main
  ✓ Meaningful commits, small changes
  ✓ .gitignore early; never commit secrets

DOCKER:
  ✓ Multi-stage builds (small images)
  ✓ Pin tags, non-root, volumes, health checks
  ✓ Secrets at runtime, not in images

CI/CD:
  ✓ Pipeline as code, fast CI feedback first
  ✓ Immutable artifacts (build once, promote)
  ✓ Zero-downtime deploys + automated rollbacks
  ✓ Secrets separate from pipeline code

CI PLATFORM:
  GitHub-centric?     → GitHub Actions
  AWS-heavy deploys?  → CodePipeline

LINUX (DEVOPS):
  ✓ set -euo pipefail in every script
  ✓ SSH keys, not passwords
  ✓ systemctl + journalctl for debugging
  ✓ App-specific users, not root
```

---

*This file covers the core DevOps tools and practices. More topics (Kubernetes, Terraform ops, monitoring/observability, incident response) will be added as separate files in this series over time.*
