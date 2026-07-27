# Infrastructure as Code (IaC) — Complete Guide

> **Series:** IaC Documentation — Part 1
> This file covers the four core **IaC tools**: AWS CDK, Terraform, CloudFormation, and Pulumi. Related: AWS CDK's AWS-specific operational details (bootstrap, environments, SDK/CLI integration) are in `cloud-service/aws.md` §12–22; this file focuses on CDK as one IaC tool among the four. More topics (Pulumi deep-dive, GitOps, policy-as-code) will be added later.

---

## Table of Contents

- [Shared Orientation — The IaC Landscape](#shared-orientation--the-iac-landscape)
- **AWS CDK**
  - [1. What Is AWS CDK?](#1-what-is-aws-cdk)
  - [2. CDK vs Terraform vs CloudFormation vs Pulumi](#2-cdk-vs-terraform-vs-cloudformation-vs-pulumi)
  - [3. How AWS CDK Works](#3-how-aws-cdk-works)
  - [4. CDK Key Concepts](#4-cdk-key-concepts)
  - [5. Where to Use AWS CDK](#5-where-to-use-aws-cdk)
  - [6. Where NOT to Use AWS CDK](#6-where-not-to-use-aws-cdk)
  - [7. Installing and Setting Up CDK](#7-installing-and-setting-up-cdk)
  - [8. CDK Authentication and Environments](#8-cdk-authentication-and-environments)
  - [9. CDK Production Best Practices](#9-cdk-production-best-practices)
  - [10. CDK Real-World Examples](#10-cdk-real-world-examples)
  - [11. CDK Pitfalls](#11-cdk-pitfalls)
- **Terraform**
  - [12. What Is Terraform?](#12-what-is-terraform)
  - [13. Terraform vs CDK vs CloudFormation vs Pulumi](#13-terraform-vs-cdk-vs-cloudformation-vs-pulumi)
  - [14. How Terraform Works](#14-how-terraform-works)
  - [15. Terraform Key Concepts](#15-terraform-key-concepts)
  - [16. Where to Use Terraform](#16-where-to-use-terraform)
  - [17. Where NOT to Use Terraform](#17-where-not-to-use-terraform)
  - [18. Installing and Setting Up Terraform](#18-installing-and-setting-up-terraform)
  - [19. Terraform State and Backends](#19-terraform-state-and-backends)
  - [20. Terraform Production Best Practices](#20-terraform-production-best-practices)
  - [21. Terraform Real-World Examples](#21-terraform-real-world-examples)
  - [22. Terraform Pitfalls](#22-terraform-pitfalls)
- **CloudFormation**
  - [23. What Is AWS CloudFormation?](#23-what-is-aws-cloudformation)
  - [24. CloudFormation vs CDK vs Terraform](#24-cloudformation-vs-cdk-vs-terraform)
  - [25. How CloudFormation Works](#25-how-cloudformation-works)
  - [26. CloudFormation Key Concepts](#26-cloudformation-key-concepts)
  - [27. Where to Use CloudFormation](#27-where-to-use-cloudformation)
  - [28. Where NOT to Use CloudFormation](#28-where-not-to-use-cloudformation)
  - [29. Setting Up CloudFormation](#29-setting-up-cloudformation)
  - [30. CloudFormation Access and State](#30-cloudformation-access-and-state)
  - [31. CloudFormation Production Best Practices](#31-cloudformation-production-best-practices)
  - [32. CloudFormation Real-World Examples](#32-cloudformation-real-world-examples)
  - [33. CloudFormation Pitfalls](#33-cloudformation-pitfalls)
- **Pulumi**
  - [34. What Is Pulumi?](#34-what-is-pulumi)
  - [35. Pulumi vs CDK vs Terraform](#35-pulumi-vs-cdk-vs-terraform)
  - [36. How Pulumi Works](#36-how-pulumi-works)
  - [37. Pulumi Key Concepts](#37-pulumi-key-concepts)
  - [38. Where to Use Pulumi](#38-where-to-use-pulumi)
  - [39. Where NOT to Use Pulumi](#39-where-not-to-use-pulumi)
  - [40. Installing and Setting Up Pulumi](#40-installing-and-setting-up-pulumi)
  - [41. Pulumi State and Backends](#41-pulumi-state-and-backends)
  - [42. Pulumi Production Best Practices](#42-pulumi-production-best-practices)
  - [43. Pulumi Real-World Examples](#43-pulumi-real-world-examples)
  - [44. Pulumi Pitfalls](#44-pulumi-pitfalls)
- [Shared Foundations](#shared-foundations)
- [Quick Reference Card](#quick-reference-card)

---

## Shared Orientation — The IaC Landscape

**Infrastructure as Code (IaC)** means defining infrastructure in **code** (reviewed, versioned, reproducible) instead of clicking in a console. The four tools split along two axes.

| Tool | Style | Cloud | Language |
|---|---|---|---|
| **AWS CDK** | Imperative | AWS only | TypeScript, Python, Java, C# |
| **Terraform** | Declarative | Multi-cloud | HCL |
| **CloudFormation** | Declarative | AWS only | JSON / YAML |
| **Pulumi** | Imperative | Multi-cloud | Python, TypeScript, Go |

**Decision guide:**
- AWS-only + want code-level abstraction? → **AWS CDK**
- Multi-cloud + declarative + huge ecosystem? → **Terraform**
- AWS-only + pure declarative, no build step? → **CloudFormation**
- Multi-cloud + real programming languages? → **Pulumi**

**Rule of thumb:** pick by **cloud scope** (AWS-only vs multi-cloud) and **style** (imperative code vs declarative config). Whatever you choose, the benefits are the same: reproducible, version-controlled, reviewable infrastructure.

---

# AWS CDK

## 1. What Is AWS CDK?

**AWS CDK (Cloud Development Kit)** is an IaC framework that lets you define AWS resources using **real programming languages** (TypeScript, Python, Java, C#) via **constructs**, compiled down to CloudFormation.

**One-liner:** write AWS infrastructure in a real programming language.

## 2. CDK vs Terraform vs CloudFormation vs Pulumi

| | CDK | Terraform | CloudFormation | Pulumi |
|---|---|---|---|---|
| Style | Imperative code | Declarative HCL | Declarative YAML | Imperative code |
| Cloud | AWS only | Multi-cloud | AWS only | Multi-cloud |
| State | CloudFormation | State file | AWS-managed | Pulumi/self |

**Rule of thumb:** CDK for **AWS + code-level abstraction** (loops, conditionals, reusable constructs).

## 3. How AWS CDK Works

1. You write **constructs** (code objects = AWS resources).
2. **`cdk synth`** compiles to a **CloudFormation template**.
3. **`cdk deploy`** hands it to CloudFormation, which provisions the resources.

**Key point:** CDK is a *generator*; CloudFormation is the *engine* (state, rollback, drift). For the AWS-specific details (bootstrap, environments, SDK/CLI integration), see `aws.md` §12–22.

## 4. CDK Key Concepts

- **App → Stack → Construct** hierarchy.
- **L1/L2/L3 constructs** — raw CFN resources → opinionated wrappers → patterns.
- **`cdk.json`**, **bootstrap**, **`synth`/`diff`/`deploy`/`destroy`**.

## 5. Where to Use AWS CDK

- **AWS infrastructure** with code-level logic and abstraction.
- Teams that **already code** and want reusable constructs.
- **Repeatable environments** defined programmatically.

## 6. Where NOT to Use AWS CDK

- **Multi-cloud** (Terraform/Pulumi).
- **Pure declarative** preference (CloudFormation/Terraform).
- Simple infra where a full framework is overkill.

## 7. Installing and Setting Up CDK

```bash
npm install -g aws-cdk
mkdir my-app && cd my-app
cdk init app --language typescript
cdk bootstrap     # one-time per account/region
cdk synth && cdk diff && cdk deploy
```

## 8. CDK Authentication and Environments

- Uses the **same credential chain as SDK/CLI** (env vars, profiles, IAM roles, SSO).
- **`cdk bootstrap`** per account/region.
- Set explicit **`env`** on stacks to pin account/region. See `aws.md` §19.

## 9. CDK Production Best Practices

1. **Prefer L2/L3 constructs** — best-practice defaults.
2. **Explicit `env`** on every stack.
3. **Review `cdk diff`** in pull requests.
4. **No secrets in stack code** — reference Secrets Manager/SSM.
5. **Pin versions**; test with `cdk synth`/LocalStack.

## 10. CDK Real-World Examples

### Example 1 — S3 Bucket (L2 Construct)
```typescript
new s3.Bucket(this, "Data", { versioned: true, encryption: s3.BucketEncryption.S3_MANAGED });
```
**Why:** one line gets an encrypted, versioned bucket with safe defaults.

### Example 2 — Multi-Environment Stacks
**Why:** same code deploys Dev and Prod to separate accounts — repeatable, reviewable.

## 11. CDK Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| No explicit `env` | Deploys to wrong account | Set env on stacks |
| Skipping `cdk diff` | Accidental destructive changes | Review diff in PRs |
| Secrets in code | Credentials in templates | Secrets Manager/SSM |
| Unpinned versions | Silent infra changes | Pin CDK versions |

---

# Terraform

## 12. What Is Terraform?

**Terraform** is HashiCorp's **declarative IaC** tool using **HCL** to provision infrastructure across **many clouds** via a huge provider ecosystem.

**One-liner:** declarative, multi-cloud infrastructure as code.

## 13. Terraform vs CDK vs CloudFormation vs Pulumi

| | Terraform | CDK | CloudFormation | Pulumi |
|---|---|---|---|---|
| Style | Declarative HCL | Imperative | Declarative | Imperative |
| Cloud | Multi-cloud | AWS | AWS | Multi-cloud |
| State | State file (you manage) | CloudFormation | AWS-managed | Pulumi/self |

**Rule of thumb:** Terraform for **multi-cloud, declarative IaC** with a massive provider ecosystem.

## 14. How Terraform Works

1. Write **`.tf` files** (HCL) describing desired resources.
2. **`terraform init`** → downloads providers; **`plan`** → preview changes; **`apply`** → provision.
3. A **state file** tracks what exists (mapping config → real resources).
4. **Providers** translate HCL into cloud API calls.

**Key point:** Terraform is **declarative** — you describe the *end state*, and it figures out how to get there. The **state file** is the critical piece.

## 15. Terraform Key Concepts

- **Providers** — plugins for clouds (AWS, GCP, Azure…).
- **Resources / data sources** — things to create / read.
- **Variables / outputs** — parameterization / exported values.
- **State** — the source of truth for what exists.
- **Modules** — reusable bundles; **workspaces** — separate states per env.

## 16. Where to Use Terraform

- **Multi-cloud** infrastructure.
- **Declarative** IaC with a huge ecosystem.
- Ops-heavy teams wanting a standard, mature tool.

## 17. Where NOT to Use Terraform

- **AWS-only** wanting code-level abstraction (CDK).
- Simple AWS infra where CloudFormation suffices.

## 18. Installing and Setting Up Terraform

```bash
# Install (see terraform.io), then:
terraform init
terraform plan
terraform apply
```

```hcl
# main.tf
provider "aws" { region = "us-east-1" }
resource "aws_s3_bucket" "data" { bucket = "my-tf-bucket" }
```

## 19. Terraform State and Backends

- **State** maps your config to real resources — losing/corrupting it is dangerous.
- **Local state** (default) is fine for learning only.
- **Remote backend** (e.g., S3 + DynamoDB locking) — shared, locked, versioned state for teams.

**Golden rule:** always use a **remote, locked backend** in real projects; never commit state with secrets.

## 20. Terraform Production Best Practices

1. **Remote state + locking** — prevent conflicts/corruption.
2. **Modules** — reuse and standardize.
3. **`plan` in pull requests** — review before apply.
4. **Pin provider versions**.
5. **Workspaces / separate states** per environment.
6. **Never edit resources manually** — causes drift.

## 21. Terraform Real-World Examples

### Example 1 — Multi-Cloud
**Why:** one tool provisions AWS + GCP + Azure with the same workflow — the core multi-cloud benefit.

### Example 2 — A Reusable Module
**Why:** package a VPC/web-app stack as a module; instantiate it per environment with different variables.

## 22. Terraform Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Local state | Lost/corrupted state | Remote backend |
| No state locking | Concurrent-apply conflicts | Enable locking |
| Secrets in state | Exposure | Manage secrets carefully |
| Unpinned providers | Breaking changes | Pin versions |
| Manual console changes | Drift from state | All changes via Terraform |

---

# CloudFormation

## 23. What Is AWS CloudFormation?

**AWS CloudFormation** is AWS's **native declarative IaC** service — you write **JSON/YAML templates**, and CloudFormation provisions and manages the resources.

**One-liner:** AWS's native declarative infrastructure as code.

## 24. CloudFormation vs CDK vs Terraform

| | CloudFormation | CDK | Terraform |
|---|---|---|---|
| Style | Declarative YAML/JSON | Imperative code | Declarative HCL |
| Cloud | AWS only | AWS only | Multi-cloud |
| State | AWS-managed | CloudFormation | State file |
| Build step | None | `cdk synth` | None |

**Rule of thumb:** CloudFormation for **pure declarative, AWS-native IaC** with no build step and AWS-managed state.

## 25. How CloudFormation Works

1. Write a **template** declaring **resources**.
2. **Create a stack** — CloudFormation provisions the resources in order.
3. It **manages state**, supports **rollback** on failure, and detects **drift**.
4. **Change sets** preview updates before applying.

**Key point:** no build step and no state file to manage — AWS handles state, rollback, and drift for you.

## 26. CloudFormation Key Concepts

- **Template** — the JSON/YAML definition.
- **Stack** — a deployed collection of resources.
- **Parameters / outputs** — inputs / cross-stack references.
- **Change sets** — preview updates.
- **Drift detection**, **rollback**, **nested stacks**.

## 27. Where to Use CloudFormation

- **AWS-native declarative** IaC.
- When you want **no build step** and **AWS-managed state/rollback**.
- Teams comfortable with YAML/JSON over code.

## 28. Where NOT to Use CloudFormation

- **Multi-cloud** (Terraform/Pulumi).
- Want **code-level abstraction/logic** (CDK/Pulumi) — YAML logic is limited.

## 29. Setting Up CloudFormation

```yaml
# template.yaml
Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      VersioningConfiguration: { Status: Enabled }
```
```bash
aws cloudformation deploy --template-file template.yaml --stack-name my-stack
```

## 30. CloudFormation Access and State

- **IAM** controls who can create/update stacks and which resources CloudFormation may manage.
- **State is AWS-managed** — no state file to secure (unlike Terraform).

## 31. CloudFormation Production Best Practices

1. **Use change sets** — preview before applying.
2. **Parameters** for config; **outputs** for cross-stack references.
3. **Nested stacks** for large infrastructure.
4. **Termination protection** on production stacks.
5. **Drift detection** regularly.

## 32. CloudFormation Real-World Examples

### Example 1 — S3 Bucket Template
**Why:** a declarative, AWS-managed bucket with rollback and drift detection — no build step.

### Example 2 — Change Set Review
**Why:** preview exactly what an update will change before applying — catch destructive changes early.

## 33. CloudFormation Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Verbose YAML | Hard to maintain large templates | Nested stacks, or use CDK |
| Limited logic | Complex conditionals awkward | Use CDK/Pulumi for logic |
| Manual changes | Drift | All changes via templates |
| No change-set review | Surprise changes | Review change sets |

---

# Pulumi

## 34. What Is Pulumi?

**Pulumi** is a modern IaC platform using **general-purpose languages** (Python, TypeScript, Go, C#) for **multi-cloud** infrastructure.

**One-liner:** infrastructure as code in real programming languages, across clouds.

## 35. Pulumi vs CDK vs Terraform

| | Pulumi | CDK | Terraform |
|---|---|---|---|
| Style | Imperative code | Imperative code | Declarative HCL |
| Cloud | Multi-cloud | AWS only | Multi-cloud |
| State | Pulumi Service / self | CloudFormation | State file |

**Rule of thumb:** Pulumi for **multi-cloud + real programming languages** (CDK's style, Terraform's reach).

## 36. How Pulumi Works

1. Write infra in a **general-purpose language**.
2. **`pulumi up`** — the engine provisions via providers.
3. **State** is tracked (Pulumi Service or self-hosted backend).
4. Use **functions, loops, classes** for real abstraction.

**Key point:** like CDK's code-first model but **multi-cloud** and **not tied to CloudFormation**.

## 37. Pulumi Key Concepts

- **Project** — the program; **stack** — a deployed instance (dev/prod).
- **Resources / providers**.
- **State** — Pulumi Service (managed) or self-hosted (S3, etc.).
- **`pulumi up / preview / destroy`**.

## 38. Where to Use Pulumi

- **Multi-cloud** with real programming languages.
- Teams wanting **code-level abstraction** beyond AWS.
- Reusing existing language tooling (testing, packages).

## 39. Where NOT to Use Pulumi

- **AWS-only** (CDK integrates more tightly with AWS).
- **Pure declarative** preference (Terraform/CloudFormation).

## 40. Installing and Setting Up Pulumi

```bash
# Install (see pulumi.com), then:
pulumi new aws-python
pulumi up
```

```python
# __main__.py
import pulumi_aws as aws
bucket = aws.s3.Bucket("my-bucket", versioning={"enabled": True})
```

## 41. Pulumi State and Backends

- **Pulumi Service** — managed state (default, easiest).
- **Self-hosted backend** (S3, etc.) — full control.
- State is **per stack** (dev/prod isolated).

## 42. Pulumi Production Best Practices

1. **Use real-language abstraction** — functions, loops, components.
2. **Remote state** (Pulumi Service or self-hosted).
3. **`pulumi preview` in pull requests**.
4. **Secrets via Pulumi config/ESC** — never inline.
5. **Pin provider versions**.

## 43. Pulumi Real-World Examples

### Example 1 — S3 Bucket in Python
**Why:** define infra with real code — loops to create N resources, conditionals per environment.

### Example 2 — Multi-Cloud
**Why:** one program provisions AWS + GCP using familiar Python — CDK-style ergonomics, multi-cloud reach.

## 44. Pulumi Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| State management confusion | Lost/shared state | Pick a backend deliberately |
| Unpinned versions | Breaking changes | Pin providers |
| Inline secrets | Exposure | Pulumi config/ESC |
| Manual changes | Drift | All changes via Pulumi |

---

## Shared Foundations

Concepts that recur across **all IaC tools**:

- **Why IaC** — infrastructure becomes **reproducible, version-controlled, and reviewable** (like application code), replacing error-prone console clicking.
- **Declarative vs imperative** — declarative (Terraform, CloudFormation) describes the end state; imperative (CDK, Pulumi) uses code logic to build it. Choose per team preference and complexity.
- **State management** — the critical concern. Terraform/Pulumi use state files (secure + lock them); CDK/CloudFormation let AWS manage state. Understand where your state lives.
- **Review before apply** — `plan`, `diff`, `preview`, or change sets: always preview changes (ideally in pull requests) before they touch real infrastructure.
- **Drift** — manual console changes diverge from code. Make all changes through IaC and detect drift.
- **No secrets in code** — reference Secrets Manager/SSM/config, never inline credentials.

## Quick Reference Card

```
IaC PICKER (two axes: cloud scope + style):
  AWS-only  + imperative code?   → AWS CDK
  AWS-only  + declarative?       → CloudFormation
  Multi-cloud + declarative?     → Terraform
  Multi-cloud + imperative code? → Pulumi

STATE:
  Terraform/Pulumi → state file (use remote + locking)
  CDK/CloudFormation → AWS manages state for you

UNIVERSAL RULES:
  ✓ Review before apply (plan / diff / preview / change sets)
  ✓ Remote, locked state where applicable
  ✓ No secrets in code (Secrets Manager / SSM / config)
  ✓ Pin tool + provider versions
  ✓ Never edit resources manually (causes drift)
  ✓ IaC everything — no console-click snowflakes
```

---

*This file covers the four core IaC tools. More topics (GitOps, policy-as-code, Terraform deep-dive, CDK patterns) will be added as separate files in this series over time.*
