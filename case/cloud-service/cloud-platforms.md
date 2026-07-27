# Cloud Platforms & AWS Services — Complete Guide

> **Series:** Cloud Service Documentation — Part 2
> This file covers the **cloud platform landscape** (AWS, GCP, Azure) and the **key AWS services** (ECS Fargate, Messaging, S3, RDS), plus **LocalStack** for local development. Part 1 (`aws.md`) covered the AWS *tooling* (SDK, CDK, CLI); this file covers the *platforms and services* you build with. Related: `database/databases.md` (RDS/DynamoDB deep-dives), `caching/caching.md` (ElastiCache/Redis), `structures-architecture/architecture-patterns.md` (Event-Driven, Serverless).

---

## Table of Contents

- [Shared Orientation — The Cloud Landscape](#shared-orientation--the-cloud-landscape)
- **AWS**
  - [1. What Is AWS?](#1-what-is-aws)
  - [2. AWS vs GCP vs Azure](#2-aws-vs-gcp-vs-azure)
  - [3. How AWS Works](#3-how-aws-works)
  - [4. AWS Service Categories](#4-aws-service-categories)
  - [5. Where AWS Fits Best](#5-where-aws-fits-best)
  - [6. When AWS May Not Fit](#6-when-aws-may-not-fit)
  - [7. Getting Started with AWS](#7-getting-started-with-aws)
  - [8. AWS Identity and Access Management](#8-aws-identity-and-access-management)
  - [9. AWS Production Best Practices](#9-aws-production-best-practices)
  - [10. AWS Real-World Examples](#10-aws-real-world-examples)
  - [11. AWS Pitfalls](#11-aws-pitfalls)
- **GCP**
  - [12. What Is Google Cloud Platform?](#12-what-is-google-cloud-platform)
  - [13. GCP vs AWS vs Azure](#13-gcp-vs-aws-vs-azure)
  - [14. How GCP Works](#14-how-gcp-works)
  - [15. GCP Service Categories](#15-gcp-service-categories)
  - [16. Where GCP Fits Best](#16-where-gcp-fits-best)
  - [17. When GCP May Not Fit](#17-when-gcp-may-not-fit)
  - [18. Getting Started with GCP](#18-getting-started-with-gcp)
  - [19. GCP Identity and Access Management](#19-gcp-identity-and-access-management)
  - [20. GCP Production Best Practices](#20-gcp-production-best-practices)
  - [21. GCP Real-World Examples](#21-gcp-real-world-examples)
  - [22. GCP Pitfalls](#22-gcp-pitfalls)
- **Azure**
  - [23. What Is Microsoft Azure?](#23-what-is-microsoft-azure)
  - [24. Azure vs AWS vs GCP](#24-azure-vs-aws-vs-gcp)
  - [25. How Azure Works](#25-how-azure-works)
  - [26. Azure Service Categories](#26-azure-service-categories)
  - [27. Where Azure Fits Best](#27-where-azure-fits-best)
  - [28. When Azure May Not Fit](#28-when-azure-may-not-fit)
  - [29. Getting Started with Azure](#29-getting-started-with-azure)
  - [30. Azure Identity and Access Management](#30-azure-identity-and-access-management)
  - [31. Azure Production Best Practices](#31-azure-production-best-practices)
  - [32. Azure Real-World Examples](#32-azure-real-world-examples)
  - [33. Azure Pitfalls](#33-azure-pitfalls)
- **Cloud Platforms (General)**
  - [34. What Is a Cloud Platform?](#34-what-is-a-cloud-platform)
  - [35. Cloud Platforms vs On-Premises](#35-cloud-platforms-vs-on-premises)
  - [36. How Cloud Platforms Work](#36-how-cloud-platforms-work)
  - [37. Cloud Service Models](#37-cloud-service-models)
  - [38. Where Cloud Platforms Fit](#38-where-cloud-platforms-fit)
  - [39. When Cloud May Not Fit](#39-when-cloud-may-not-fit)
  - [40. Adopting a Cloud Platform](#40-adopting-a-cloud-platform)
  - [41. Cloud Identity and Governance](#41-cloud-identity-and-governance)
  - [42. Cloud Platform Best Practices](#42-cloud-platform-best-practices)
  - [43. Cloud Platform Real-World Examples](#43-cloud-platform-real-world-examples)
  - [44. Cloud Platform Pitfalls](#44-cloud-platform-pitfalls)
- **AWS ECS Fargate**
  - [45. What Is AWS ECS Fargate?](#45-what-is-aws-ecs-fargate)
  - [46. Fargate vs EC2 vs Lambda](#46-fargate-vs-ec2-vs-lambda)
  - [47. How ECS Fargate Works](#47-how-ecs-fargate-works)
  - [48. ECS Fargate Key Concepts](#48-ecs-fargate-key-concepts)
  - [49. Where to Use ECS Fargate](#49-where-to-use-ecs-fargate)
  - [50. Where NOT to Use ECS Fargate](#50-where-not-to-use-ecs-fargate)
  - [51. Getting Started with ECS Fargate](#51-getting-started-with-ecs-fargate)
  - [52. ECS Fargate Networking and Access](#52-ecs-fargate-networking-and-access)
  - [53. ECS Fargate Production Best Practices](#53-ecs-fargate-production-best-practices)
  - [54. ECS Fargate Real-World Examples](#54-ecs-fargate-real-world-examples)
  - [55. ECS Fargate Pitfalls](#55-ecs-fargate-pitfalls)
- **AWS Messaging (SQS, SNS, EventBridge)**
  - [56. What Are AWS Messaging Services?](#56-what-are-aws-messaging-services)
  - [57. SQS vs SNS vs EventBridge](#57-sqs-vs-sns-vs-eventbridge)
  - [58. How AWS Messaging Works](#58-how-aws-messaging-works)
  - [59. AWS Messaging Key Concepts](#59-aws-messaging-key-concepts)
  - [60. Where to Use AWS Messaging](#60-where-to-use-aws-messaging)
  - [61. Where NOT to Use AWS Messaging](#61-where-not-to-use-aws-messaging)
  - [62. Setting Up AWS Messaging](#62-setting-up-aws-messaging)
  - [63. AWS Messaging Access and Auth](#63-aws-messaging-access-and-auth)
  - [64. AWS Messaging Production Best Practices](#64-aws-messaging-production-best-practices)
  - [65. AWS Messaging Real-World Examples](#65-aws-messaging-real-world-examples)
  - [66. AWS Messaging Pitfalls](#66-aws-messaging-pitfalls)
- **AWS S3**
  - [67. What Is Amazon S3?](#67-what-is-amazon-s3)
  - [68. S3 vs Block vs File Storage](#68-s3-vs-block-vs-file-storage)
  - [69. How S3 Works](#69-how-s3-works)
  - [70. S3 Key Concepts](#70-s3-key-concepts)
  - [71. Where to Use S3](#71-where-to-use-s3)
  - [72. Where NOT to Use S3](#72-where-not-to-use-s3)
  - [73. Getting Started with S3](#73-getting-started-with-s3)
  - [74. S3 Access Control and Security](#74-s3-access-control-and-security)
  - [75. S3 Production Best Practices](#75-s3-production-best-practices)
  - [76. S3 Real-World Examples](#76-s3-real-world-examples)
  - [77. S3 Pitfalls](#77-s3-pitfalls)
- **AWS RDS**
  - [78. What Is Amazon RDS?](#78-what-is-amazon-rds)
  - [79. RDS vs Self-Managed vs Aurora](#79-rds-vs-self-managed-vs-aurora)
  - [80. How RDS Works](#80-how-rds-works)
  - [81. RDS Key Concepts](#81-rds-key-concepts)
  - [82. Where to Use RDS](#82-where-to-use-rds)
  - [83. Where NOT to Use RDS](#83-where-not-to-use-rds)
  - [84. Getting Started with RDS](#84-getting-started-with-rds)
  - [85. RDS Access and Security](#85-rds-access-and-security)
  - [86. RDS Production Best Practices](#86-rds-production-best-practices)
  - [87. RDS Real-World Examples](#87-rds-real-world-examples)
  - [88. RDS Pitfalls](#88-rds-pitfalls)
- **LocalStack**
  - [89. What Is LocalStack?](#89-what-is-localstack)
  - [90. LocalStack vs Real AWS vs Mocks](#90-localstack-vs-real-aws-vs-mocks)
  - [91. How LocalStack Works](#91-how-localstack-works)
  - [92. LocalStack Key Concepts](#92-localstack-key-concepts)
  - [93. Where to Use LocalStack](#93-where-to-use-localstack)
  - [94. Where NOT to Use LocalStack](#94-where-not-to-use-localstack)
  - [95. Setting Up LocalStack](#95-setting-up-localstack)
  - [96. LocalStack Configuration](#96-localstack-configuration)
  - [97. LocalStack Best Practices](#97-localstack-best-practices)
  - [98. LocalStack Real-World Examples](#98-localstack-real-world-examples)
  - [99. LocalStack Pitfalls](#99-localstack-pitfalls)
- [Shared Foundations](#shared-foundations)
- [Quick Reference Card](#quick-reference-card)

---

## Shared Orientation — The Cloud Landscape

This file has two halves: the **cloud platforms** (the big providers) and the **key AWS services** (the building blocks you'd actually use).

**The big three platforms:**
| Platform | Strength | One-liner |
|---|---|---|
| **AWS** | Broadest service catalog, market leader | Most mature, most services |
| **GCP** | Data/ML, Kubernetes, developer-friendly | Strongest in data & containers |
| **Azure** | Enterprise/Microsoft integration, hybrid | Best for Microsoft shops |

**Key AWS services covered:**
| Service | Category | One-liner |
|---|---|---|
| **ECS Fargate** | Compute | Serverless containers, no EC2 to manage |
| **SQS / SNS / EventBridge** | Messaging | Queue / pub-sub / event bus |
| **S3** | Storage | Object storage for anything |
| **RDS** | Database | Managed relational DB |
| **LocalStack** | Dev tool | Run AWS locally for testing |

**Rule of thumb:** pick a **platform** (usually AWS for breadth), then compose **managed services** instead of self-hosting. Use **LocalStack** to develop against AWS without touching (or paying for) the real cloud. For the *tools* to interact with all this (SDK/CDK/CLI), see `aws.md`.

---

# AWS

## 1. What Is AWS?

**Amazon Web Services (AWS)** is the leading cloud platform, offering the **broadest catalog** of on-demand compute, storage, database, networking, and managed services.

- Pay-as-you-go; scale up/down on demand; no upfront hardware.
- The most mature ecosystem with the largest community and feature set.

**One-liner:** the market-leading, most complete cloud platform.

## 2. AWS vs GCP vs Azure

| | AWS | GCP | Azure |
|---|---|---|---|
| Services | Broadest | Strong in data/ML | Strong enterprise/hybrid |
| Maturity | Most mature | Growing | Strong in enterprises |
| Best for | General-purpose, breadth | Data/ML, Kubernetes | Microsoft shops |

**Rule of thumb:** default to AWS for breadth and maturity unless you have a specific GCP (data/ML) or Azure (Microsoft) reason.

## 3. How AWS Works

- **Regions** (geographic) → **Availability Zones** (isolated data centers) for resilience.
- Services are consumed via **Console, CLI, SDK, or IaC (CDK)** — see `aws.md`.
- **IAM** controls who can do what across all services.
- You compose **managed services** (S3, RDS, SQS…) instead of running your own.

## 4. AWS Service Categories

| Category | Key services |
|---|---|
| **Compute** | EC2, ECS/Fargate, Lambda |
| **Storage** | S3, EBS, EFS |
| **Database** | RDS, DynamoDB, ElastiCache |
| **Messaging** | SQS, SNS, EventBridge |
| **Networking** | VPC, CloudFront, API Gateway |
| **DevOps** | CodePipeline, CloudFormation, CDK |

## 5. Where AWS Fits Best

- **General-purpose** cloud for nearly any workload.
- When you want the **broadest managed-service catalog**.
- **Startups to enterprises** needing to scale without owning hardware.

## 6. When AWS May Not Fit

- **Data/ML-heavy** workloads where GCP's tools lead.
- **Deep Microsoft integration** needs where Azure is smoother.
- **Multi-cloud** strategies avoiding lock-in.

## 7. Getting Started with AWS

1. Create an **AWS account** (free tier to learn).
2. Set up **IAM users/roles** — never use the root account.
3. Configure the **CLI/SDK** (`aws configure`) — see `aws.md`.
4. Provision infrastructure with **CDK** — see `aws.md`.

## 8. AWS Identity and Access Management

- **IAM** is the security backbone: users, groups, roles, policies.
- **Roles** for services (Lambda/EC2/ECS); **policies** define permissions.
- **Least privilege** — grant only what's needed.

**Golden rule:** root account = billing/emergencies only; everything else via IAM roles.

## 9. AWS Production Best Practices

1. **Least-privilege IAM** everywhere.
2. **Use managed services** over self-hosting.
3. **Multi-AZ** for high availability.
4. **Tag resources** for cost allocation.
5. **Set budgets + alerts** — cloud costs sneak up.
6. **Infrastructure as Code** (CDK) — reproducible, reviewable.

## 10. AWS Real-World Examples

### Example 1 — Serverless API
```
API Gateway → Lambda → DynamoDB, static assets on S3 + CloudFront
```
**Why:** fully managed, scales automatically, near-zero idle cost.

### Example 2 — Event-Driven Backend
**Why:** S3 upload → EventBridge → Lambda → SQS → worker — decoupled, resilient, serverless.

## 11. AWS Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Using root account | Security risk | IAM roles only |
| No cost alerts | Surprise bills | Budgets + alerts |
| Self-hosting what AWS manages | Wasted effort | Use managed services |
| Single-AZ | Downtime on AZ failure | Multi-AZ |
| Overly broad IAM | Over-privileged | Least privilege |

---

# GCP

## 12. What Is Google Cloud Platform?

**Google Cloud Platform (GCP)** is Google's cloud, strong in **data analytics, machine learning, and Kubernetes** (GKE), with a developer-friendly experience.

**One-liner:** Google's cloud — strongest in data, ML, and containers.

## 13. GCP vs AWS vs Azure

| | GCP | AWS | Azure |
|---|---|---|---|
| Data/ML | Strongest (BigQuery, Vertex AI) | Good | Good |
| Kubernetes | GKE (Google invented K8s) | EKS | AKS |
| Ecosystem size | Smaller than AWS | Largest | Enterprise-strong |

**Rule of thumb:** choose GCP for **data analytics, ML, and Kubernetes-first** workloads.

## 14. How GCP Works

- **Projects** organize resources; **regions/zones** for placement.
- Services via Console, `gcloud` CLI, or client libraries.
- **IAM** controls access; strong defaults and networking.

## 15. GCP Service Categories

| Category | Key services |
|---|---|
| **Compute** | Compute Engine, GKE, Cloud Run, Cloud Functions |
| **Data/ML** | BigQuery, Dataflow, Vertex AI, Pub/Sub |
| **Storage** | Cloud Storage, Persistent Disk |
| **Database** | Cloud SQL, Firestore, Spanner, Bigtable |

## 16. Where GCP Fits Best

- **Data analytics** (BigQuery is best-in-class).
- **Machine learning** (Vertex AI, TPUs).
- **Kubernetes-native** workloads (GKE).

## 17. When GCP May Not Fit

- Need the **broadest service catalog** (AWS leads).
- **Deep Microsoft** integration (Azure).

## 18. Getting Started with GCP

1. Create a **GCP account** (free tier/credits).
2. Create a **project**; enable APIs.
3. Install **`gcloud` CLI**; authenticate (`gcloud auth login`).

## 19. GCP Identity and Access Management

- **IAM** with members, roles, policies at org/folder/project/resource levels.
- **Service accounts** for workloads (like AWS roles).
- **Least privilege** via predefined/custom roles.

## 20. GCP Production Best Practices

1. **Least-privilege IAM**; prefer service accounts.
2. Use **managed services** (Cloud Run, BigQuery).
3. **Budgets + alerts** for cost control.
4. **Multi-zone** for availability.
5. **IaC** (Terraform/Deployment Manager).

## 21. GCP Real-World Examples

### Example 1 — Data Analytics Pipeline
**Why:** Pub/Sub → Dataflow → BigQuery — serverless, petabyte-scale analytics with minimal ops.

### Example 2 — Containerized App
**Why:** Cloud Run deploys a container that scales to zero — pay only when serving.

## 22. GCP Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Over-permissive service accounts | Security risk | Least-privilege roles |
| BigQuery cost surprises | On-demand scan costs | Set cost controls, partition tables |
| Smaller ecosystem | Missing a niche service | Check service availability first |

---

# Azure

## 23. What Is Microsoft Azure?

**Microsoft Azure** is Microsoft's cloud, strong in **enterprise integration, hybrid cloud, and Microsoft-ecosystem** workloads (Windows, .NET, Active Directory, Office 365).

**One-liner:** Microsoft's cloud — best for enterprise and Microsoft shops.

## 24. Azure vs AWS vs GCP

| | Azure | AWS | GCP |
|---|---|---|---|
| Enterprise/MS | Strongest | Good | Weaker |
| Hybrid cloud | Strong (Azure Arc) | Growing | Growing |
| Microsoft integration | Native (AD, .NET, O365) | Limited | Limited |

**Rule of thumb:** choose Azure when you're a **Microsoft-centric organization** or need **hybrid/enterprise** integration.

## 25. How Azure Works

- **Subscriptions** → **resource groups** organize resources; **regions** for placement.
- Services via Portal, **Azure CLI**, or SDKs.
- **Azure AD (Entra ID)** for identity; RBAC for access.

## 26. Azure Service Categories

| Category | Key services |
|---|---|
| **Compute** | VMs, AKS, Azure Functions, App Service |
| **Data** | Azure SQL, Cosmos DB, Synapse |
| **Storage** | Blob Storage, Azure Files |
| **Integration** | Service Bus, Event Grid, Logic Apps |

## 27. Where Azure Fits Best

- **Microsoft-centric** enterprises (Windows, .NET, AD).
- **Hybrid cloud** (on-prem + cloud via Azure Arc).
- **Enterprise agreements** and compliance needs.

## 28. When Azure May Not Fit

- **Data/ML-first** workloads (GCP may lead).
- Need the **broadest catalog** (AWS).

## 29. Getting Started with Azure

1. Create an **Azure account** (free credits).
2. Create a **resource group**.
3. Install **Azure CLI**; authenticate (`az login`).

## 30. Azure Identity and Access Management

- **Microsoft Entra ID** (formerly Azure AD) for identity.
- **RBAC** — roles assigned at subscription/resource-group/resource scope.
- **Managed identities** for services (like AWS roles).

## 31. Azure Production Best Practices

1. **Least-privilege RBAC**; use managed identities.
2. Use **managed services** (App Service, Azure SQL).
3. **Cost management + budgets**.
4. **Multi-region/zone** for availability.
5. **IaC** (Bicep/Terraform/ARM).

## 32. Azure Real-World Examples

### Example 1 — Enterprise Web App
**Why:** App Service + Azure SQL + Entra ID — integrated auth and hosting for a .NET enterprise app.

### Example 2 — Hybrid Deployment
**Why:** Azure Arc manages on-prem + cloud resources uniformly — true hybrid operations.

## 33. Azure Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Over-permissive RBAC | Security risk | Least privilege, managed identities |
| Resource sprawl | Cost/complexity | Resource groups + tagging + policy |
| Ignoring hybrid options | Missed efficiency | Evaluate Azure Arc for hybrid |

---

# Cloud Platforms (General)

## 34. What Is a Cloud Platform?

A **cloud platform** (AWS, GCP, Azure, Vercel, etc.) provides **on-demand computing resources** — servers, storage, databases, networking, and managed services — over the internet, typically pay-as-you-go.

**One-liner:** rent computing instead of owning hardware.

## 35. Cloud Platforms vs On-Premises

| | Cloud | On-Premises |
|---|---|---|
| Cost model | OpEx (pay-as-you-go) | CapEx (buy hardware) |
| Scaling | Instant, elastic | Slow, capacity-limited |
| Ops burden | Provider manages infra | You manage everything |
| Control | Less low-level control | Full control |

**Rule of thumb:** cloud for **elasticity and speed**; on-prem for **strict control/compliance** or predictable steady loads.

## 36. How Cloud Platforms Work

- The provider runs **data centers**; you consume resources via APIs/Console.
- **Virtualization** abstracts hardware into VMs, containers, serverless.
- You pay for what you use (**metered billing**).
- **Managed services** offload undifferentiated ops (DBs, queues, etc.).

## 37. Cloud Service Models

| Model | You manage | Example |
|---|---|---|
| **IaaS** | OS, runtime, app | EC2, Compute Engine |
| **PaaS** | Just the app | App Service, App Engine |
| **SaaS** | Nothing | Gmail, Salesforce |
| **Serverless/FaaS** | Just the function | Lambda, Cloud Functions |

## 38. Where Cloud Platforms Fit

- **Startups** needing speed without CapEx.
- **Variable/spiky workloads** (elastic scaling).
- **Global reach** without building data centers.
- Teams wanting to **focus on product, not infra**.

## 39. When Cloud May Not Fit

- **Strict data-residency/compliance** requiring on-prem.
- **Predictable steady-state** loads where owned hardware is cheaper.
- **Extreme low-latency** edge needs.

## 40. Adopting a Cloud Platform

1. **Start small** — one workload, learn the model.
2. **Use managed services** — don't lift-and-shift everything to VMs.
3. **IaC from day one** — reproducible environments.
4. **Set up cost governance** early.

## 41. Cloud Identity and Governance

- **Centralized identity** (IAM/Entra) with least privilege.
- **Tagging + policies** for organization and cost control.
- **Budgets, alerts, quotas** — cloud costs require active governance.

## 42. Cloud Platform Best Practices

1. **Prefer managed services** over self-hosting.
2. **Design for elasticity** — scale out, not just up.
3. **Multi-zone/region** for resilience.
4. **IaC everything** — no console-click snowflakes.
5. **Govern costs** — budgets, tags, right-sizing.

## 43. Cloud Platform Real-World Examples

### Example 1 — Startup Web App
**Why:** deploy on PaaS/serverless, scale automatically, pay only for usage — no infra team needed.

### Example 2 — Global SaaS
**Why:** multi-region deployment + CDN serves users worldwide with low latency.

## 44. Cloud Platform Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Lift-and-shift to VMs | Missed cloud benefits | Use managed services |
| No cost governance | Surprise bills | Budgets, tags, alerts |
| Console-click infra | Snowflake environments | IaC |
| Single point of failure | Downtime | Multi-zone design |

---

# AWS ECS Fargate

## 45. What Is AWS ECS Fargate?

**AWS Fargate** is a **serverless compute engine for containers** that runs Docker containers **without managing EC2 instances** — you define the container, AWS runs it.

**One-liner:** run containers without managing servers.

## 46. Fargate vs EC2 vs Lambda

| | Fargate | EC2 (with ECS) | Lambda |
|---|---|---|---|
| Servers | None (serverless containers) | You manage | None |
| Workload | Long-running containers | Long-running, full control | Short event-driven functions |
| Control | Container-level | Instance-level | Function-level |

**Rule of thumb:** Fargate for **long-running containerized services** without server management; Lambda for **short event-driven** tasks; EC2 for **full control**.

## 47. How ECS Fargate Works

1. Define a **task** (container image, CPU, memory).
2. Create a **service** running N tasks.
3. Fargate provisions compute **on demand** — no EC2 to patch/scale.
4. Tasks run in your **VPC**; you pay for vCPU/memory per second.

**Key point:** you think in **containers**, not servers — AWS handles the instances.

## 48. ECS Fargate Key Concepts

- **Task definition** — container spec (image, resources, env).
- **Service** — keeps N tasks running, integrates with load balancers.
- **Cluster** — logical grouping of tasks/services.
- **awsvpc networking** — each task gets its own ENI/IP.

## 49. Where to Use ECS Fargate

- **Microservices/APIs** in containers (see `architecture-patterns.md`).
- **Long-running services** you want containerized without server ops.
- Workloads needing **container portability** + **no server management**.

## 50. Where NOT to Use ECS Fargate

- **Short, event-driven** tasks (Lambda is cheaper).
- Need **full instance control** (EC2).
- **Cost-sensitive steady high load** (EC2 reserved may be cheaper).

## 51. Getting Started with ECS Fargate

```bash
# Define a task + service (via Console, CLI, or CDK — see aws.md)
aws ecs create-cluster --cluster-name my-cluster
# Register a task definition (image, cpu, memory), then:
aws ecs create-service --cluster my-cluster --service-name api \
  --task-definition my-api --desired-count 2 --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],assignPublicIp=ENABLED}"
```

## 52. ECS Fargate Networking and Access

- **awsvpc mode** — tasks get their own IP; secure via **security groups**.
- **IAM task roles** — give tasks least-privilege AWS access.
- **Load balancer** (ALB) in front of services for HTTP traffic.

## 53. ECS Fargate Production Best Practices

1. **Right-size CPU/memory** — over-provisioning wastes money.
2. **Use task IAM roles** — least privilege per service.
3. **Health checks + auto-scaling** — resilience and cost-efficiency.
4. **Centralized logging** (CloudWatch) and **tracing** (X-Ray).
5. **Private subnets** for tasks; ALB in public subnets.

## 54. ECS Fargate Real-World Examples

### Example 1 — Microservices on Fargate
**Why:** each microservice is a Fargate service behind an ALB — independent scaling, no server management (relates to `architecture-patterns.md` Microservices).

## 55. ECS Fargate Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Over-provisioned tasks | High cost | Right-size resources |
| No health checks | Unhealthy tasks linger | Configure ALB/container health checks |
| Public tasks | Security exposure | Private subnets + ALB |
| Broad task roles | Over-privileged | Least-privilege task IAM |

---

# AWS Messaging (SQS, SNS, EventBridge)

## 56. What Are AWS Messaging Services?

AWS provides three core **messaging services** for decoupled, asynchronous communication:
- **SQS** — message **queues** (buffer work).
- **SNS** — **pub/sub** notifications (fan-out).
- **EventBridge** — serverless **event bus** (route events by rules).

**One-liner:** decouple services with queues, pub/sub, and event routing.

## 57. SQS vs SNS vs EventBridge

| | SQS | SNS | EventBridge |
|---|---|---|---|
| Model | Queue (pull) | Pub/sub (push, fan-out) | Event bus (rule routing) |
| Consumers | One per message | Many per message | Many, filtered by rules |
| Best for | Buffer work, decouple | Notifications, fan-out | Event-driven apps, SaaS integration |

**Rule of thumb:** **SQS** to buffer/queue work; **SNS** to fan out to many; **EventBridge** to route events between services/SaaS with filtering.

## 58. How AWS Messaging Works

- **SQS:** producers send messages; consumers **poll and process**; messages persist until consumed.
- **SNS:** publishers send to a **topic**; all **subscribers** (SQS, Lambda, email, HTTP) get a copy.
- **EventBridge:** events flow to an **event bus**; **rules** route matching events to targets.

**Key point:** these implement **Event-Driven Architecture** — see `architecture-patterns.md` §9–16 for the pattern.

## 59. AWS Messaging Key Concepts

- **Queue** (SQS) — buffer; **DLQ** for failed messages.
- **Topic** (SNS) — fan-out channel; **subscriptions** receive copies.
- **Event bus + rules** (EventBridge) — content-based routing.
- **Fan-out pattern** — SNS → multiple SQS queues.

## 60. Where to Use AWS Messaging

- **Decoupling microservices** (async communication).
- **Buffering workload spikes** (SQS).
- **Fan-out notifications** (SNS).
- **Event-driven workflows** across services/SaaS (EventBridge).

## 61. Where NOT to Use AWS Messaging

- **Synchronous request/response** needs (use direct API calls).
- **High-throughput streaming** (consider Kinesis/Kafka).

## 62. Setting Up AWS Messaging

```bash
# SQS queue
aws sqs create-queue --queue-name jobs

# SNS topic + subscribe a queue
aws sns create-topic --name order-events
aws sns subscribe --topic-arn <arn> --protocol sqs --notification-endpoint <queue-arn>

# EventBridge rule routing events to a target
aws events put-rule --name order-rule --event-pattern '{"source":["orders"]}'
```

## 63. AWS Messaging Access and Auth

- **IAM policies** control who can send/receive/publish.
- **Resource policies** on queues/topics for cross-account access.
- **Encryption** (KMS) for sensitive messages.

## 64. AWS Messaging Production Best Practices

1. **Idempotent consumers** — messages can be delivered more than once.
2. **Dead-letter queues** — capture failed messages for inspection.
3. **Visibility timeouts** tuned to processing time (SQS).
4. **Monitor queue depth/lag** — detect stuck consumers.
5. **Fan-out via SNS→SQS** rather than direct integrations.

## 65. AWS Messaging Real-World Examples

### Example 1 — SQS Buffers a Spike
**Why:** API enqueues jobs to SQS and returns fast; workers process at their own pace even under load.

### Example 2 — SNS Fan-Out
**Why:** `OrderCreated` → SNS topic → Inventory SQS + Billing SQS + Analytics SQS — each reacts independently.

### Example 3 — EventBridge Routing
**Why:** route `high-value` orders to a priority queue and others to standard — content-based, no producer changes.

## 66. AWS Messaging Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Non-idempotent consumers | Duplicate side effects | Idempotency keys |
| No DLQ | Poison messages lost | Configure DLQs |
| Wrong visibility timeout | Reprocessing/duplicates | Match timeout to processing time |
| Using SQS for fan-out | Complex workarounds | Use SNS/EventBridge for fan-out |

---

# AWS S3

## 67. What Is Amazon S3?

**Amazon S3 (Simple Storage Service)** is **object storage** for files, backups, static assets, and data lakes — offering extreme durability and scalability.

**One-liner:** infinitely scalable object storage for anything.

## 68. S3 vs Block vs File Storage

| | S3 (object) | EBS (block) | EFS (file) |
|---|---|---|---|
| Access | HTTP API | Attached to one EC2 | Shared file system |
| Best for | Files, backups, static | DB/boot volumes | Shared POSIX fs |
| Scaling | Virtually unlimited | Per-volume | Elastic |

**Rule of thumb:** S3 for **objects/files over HTTP**; block for **volumes**; file for **shared filesystems**.

## 69. How S3 Works

- **Buckets** hold **objects** (files) identified by **keys**.
- Objects are stored **durably** (11 nines) across AZs.
- Accessed via **HTTP API** (SDK/CLI/Console).
- **Storage classes** trade cost vs access speed (Standard, IA, Glacier).

## 70. S3 Key Concepts

- **Bucket** — top-level container (globally unique name).
- **Object/key** — a file + its path.
- **Storage classes** — Standard, Infrequent Access, Glacier.
- **Versioning** — keep object history.
- **Lifecycle rules** — auto-transition/expire objects.
- **Presigned URLs** — temporary, scoped access.

## 71. Where to Use S3

- **User uploads** (avatars, documents, media).
- **Backups** and **archives** (Glacier).
- **Static website assets** (with CloudFront).
- **Data lakes** (analytics source).

## 72. Where NOT to Use S3

- **POSIX file system** needs (use EFS).
- **Database storage** (use EBS/RDS).
- **Low-latency frequent small reads** at scale (consider a DB/cache).

## 73. Getting Started with S3

```bash
aws s3 mb s3://my-bucket
aws s3 cp file.txt s3://my-bucket/uploads/
aws s3 ls s3://my-bucket/uploads/
# Presigned URL for direct client upload (see aws.md SDK examples)
```

## 74. S3 Access Control and Security

- **Block Public Access** — on by default; keep it on unless intentional.
- **Bucket policies + IAM** — control access.
- **Encryption** — at rest (SSE) and in transit (TLS).
- **Presigned URLs** — grant temporary, scoped upload/download.

**Golden rule:** default to **private**; expose only via presigned URLs or CloudFront.

## 75. S3 Production Best Practices

1. **Keep buckets private** by default.
2. **Enable versioning** for important data.
3. **Lifecycle rules** — transition old data to cheaper classes, expire temp files.
4. **Presigned URLs** for client uploads (don't proxy through your API).
5. **Encrypt** sensitive data.
6. Use **CloudFront** in front for low-latency delivery.

## 76. S3 Real-World Examples

### Example 1 — Direct Client Upload (Presigned)
**Why:** browser uploads straight to S3 with a presigned URL — your API never touches the file (see `aws.md` §10).

### Example 2 — Lifecycle Cost Optimization
**Why:** move logs to Infrequent Access after 30 days, Glacier after 90, delete after a year — automatic cost control.

## 77. S3 Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Public bucket by accident | Data breach | Block Public Access + audit |
| No lifecycle rules | Growing storage costs | Automate transitions/expiry |
| Proxying uploads through API | Slow, memory-heavy | Presigned URLs |
| No versioning | Accidental overwrites/deletes | Enable versioning |

---

# AWS RDS

## 78. What Is Amazon RDS?

**Amazon RDS (Relational Database Service)** is a **managed relational database** service — AWS handles **backups, patching, and scaling** for engines like PostgreSQL, MySQL, and others.

**One-liner:** managed relational databases without the ops burden.

## 79. RDS vs Self-Managed vs Aurora

| | RDS | Self-managed (EC2) | Aurora |
|---|---|---|---|
| Ops | AWS manages | You manage | AWS manages (cloud-native) |
| Patching/backups | Automatic | Manual | Automatic |
| Performance | Standard | Standard | Higher (AWS-optimized) |

**Rule of thumb:** use **RDS** for managed relational DBs; **Aurora** for higher performance/scale; **self-manage** only for special needs. For engine details see `database/databases.md`.

## 80. How RDS Works

- Choose an **engine** (PostgreSQL, MySQL, etc.) and instance size.
- AWS provisions, **patches**, **backs up**, and monitors it.
- **Multi-AZ** for failover; **read replicas** for read scaling.
- You connect with standard DB drivers/connection strings.

## 81. RDS Key Concepts

- **Instance** — the managed DB server.
- **Multi-AZ** — synchronous standby for high availability.
- **Read replicas** — async copies for read scaling.
- **Automated backups + snapshots** — point-in-time recovery.
- **Parameter/option groups** — engine configuration.

## 82. Where to Use RDS

- **Relational workloads** (PostgreSQL/MySQL) without managing servers.
- Apps needing **automated backups/patching/HA**.
- When you want a managed DB but with standard engine compatibility.

## 83. Where NOT to Use RDS

- **NoSQL/key-value at massive scale** (DynamoDB — see `database/databases.md`).
- **Full control** over the DB OS/engine (self-manage).
- **Serverless/variable** DB load (consider Aurora Serverless).

## 84. Getting Started with RDS

```bash
aws rds create-db-instance --db-instance-identifier mydb \
  --engine postgres --db-instance-class db.t3.micro \
  --allocated-storage 20 --master-username admin --master-user-password <pw> \
  --multi-az
# Connect with a standard PostgreSQL client/ORM
```

## 85. RDS Access and Security

- **Private subnets** — don't expose RDS publicly.
- **Security groups** — restrict to app servers only.
- **IAM DB authentication** or standard users/passwords.
- **Encryption at rest** (KMS) and in transit (TLS).

## 86. RDS Production Best Practices

1. **Multi-AZ** for production (automatic failover).
2. **Read replicas** for read-heavy workloads.
3. **Automated backups** + tested restores.
4. **Private subnets** + tight security groups.
5. **Monitor** slow queries, connections, storage.
6. **Right-size** the instance; use storage autoscaling.

## 87. RDS Real-World Examples

### Example 1 — HA PostgreSQL for a SaaS
**Why:** Multi-AZ RDS + read replicas gives automatic failover and read scaling — no DBA needed (relates to `architecture-patterns.md` Multi-Tenant).

### Example 2 — Point-in-Time Recovery
**Why:** restore to just before a bad migration — automated backups make this routine.

## 88. RDS Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Publicly accessible DB | Security breach | Private subnets + security groups |
| Single-AZ in prod | Downtime on failure | Multi-AZ |
| No read replicas | Primary overloaded by reads | Add replicas |
| Untested backups | Can't restore when needed | Test restores regularly |

---

# LocalStack

## 89. What Is LocalStack?

**LocalStack** is a **local AWS cloud emulator** that runs AWS services on your machine (in Docker) for **offline development and testing** — no real AWS account or cost.

**One-liner:** run a fake AWS cloud locally for dev and tests.

## 90. LocalStack vs Real AWS vs Mocks

| | LocalStack | Real AWS | Code mocks (moto) |
|---|---|---|---|
| Fidelity | High (real API behavior) | Perfect | Moderate |
| Cost | Free | Pay per use | Free |
| Speed | Local, fast | Network latency | Fastest (in-process) |
| Scope | Many AWS services | All | Limited |

**Rule of thumb:** **LocalStack** for integration testing against realistic AWS behavior; **mocks** (moto) for fast unit tests; **real AWS** for final validation.

## 91. How LocalStack Works

- Runs as a **Docker container** exposing AWS service endpoints on `localhost:4566`.
- Your **SDK/CLI/CDK** points at LocalStack instead of real AWS (via `endpoint_url` or `AWS_ENDPOINT_URL`).
- Behaves like real AWS for most services — create buckets, queues, tables, etc.

**Key point:** your code thinks it's talking to AWS — but it's all local, free, and fast.

## 92. LocalStack Key Concepts

- **Single endpoint** (`localhost:4566`) for all services.
- **`awslocal` CLI** — AWS CLI configured for LocalStack.
- **`cdklocal`** — CDK against LocalStack.
- **Ephemeral/persistent state** — reset between runs or persist.

## 93. Where to Use LocalStack

- **Local development** against AWS without an account.
- **CI/CD integration tests** — realistic AWS behavior, zero cost.
- **Testing IaC** (CDK/CloudFormation) before deploying.

## 94. Where NOT to Use LocalStack

- **Final pre-production validation** — test against real AWS too.
- **Service features it doesn't emulate** perfectly (check coverage).

## 95. Setting Up LocalStack

```bash
# Run LocalStack
docker run -p 4566:4566 localstack/localstack

# Point the SDK at it (Python example)
import boto3
s3 = boto3.client("s3", endpoint_url="http://localhost:4566",
                  aws_access_key_id="test", aws_secret_access_key="test")
s3.create_bucket(Bucket="dev-bucket")

# Or use awslocal
awslocal s3 mb s3://dev-bucket
```

## 96. LocalStack Configuration

- **`SERVICES`** env var — limit which services start (faster).
- **Persistence** — enable to keep state across restarts.
- **`cdklocal` / `awslocal`** — wrapper CLIs for convenience.

## 97. LocalStack Best Practices

1. Use it for **integration tests in CI** — never hit real AWS from CI.
2. **Reset state** between test runs for isolation.
3. **Limit services** for faster startup.
4. **Still validate against real AWS** before production.
5. Pair with **`cdklocal`** to test infrastructure code.

## 98. LocalStack Real-World Examples

### Example 1 — CI Integration Tests
**Why:** run the full test suite against LocalStack in CI — realistic S3/SQS/DynamoDB behavior with zero cost or risk (see `aws.md` §10).

### Example 2 — Test CDK Stacks Locally
**Why:** `cdklocal deploy` provisions your stack against LocalStack — catch infra errors before touching real AWS.

## 99. LocalStack Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Assuming perfect parity | Feature behaves differently in prod | Validate against real AWS |
| Skipping it in CI | Tests hit real AWS (cost/risk) | Use LocalStack in CI |
| Shared state between tests | Flaky tests | Reset state per run |

---

## Shared Foundations

Concepts that recur across **all cloud topics**:

- **Managed services over self-hosting** — the core cloud value: offload undifferentiated ops (DBs, queues, storage) to the provider and focus on your product.
- **Regions & Availability Zones** — design for resilience with multi-AZ; pick regions near users for latency.
- **IAM / least privilege** — the security backbone of every cloud; grant only what's needed, use roles/identities for services.
- **Elasticity & pay-per-use** — scale out (not just up), and govern costs actively (budgets, tags, alerts) because pay-per-use cuts both ways.
- **Infrastructure as Code** — define infrastructure in code (CDK/Terraform) for reproducible, reviewable environments (see `aws.md`).
- **Event-driven & serverless** — the modern cloud architecture: decouple with messaging (SQS/SNS/EventBridge) and run compute without servers (Lambda/Fargate) — see `architecture-patterns.md`.

## Quick Reference Card

```
PLATFORM PICKER:
  Breadth + maturity?        → AWS
  Data/ML + Kubernetes?      → GCP
  Microsoft/enterprise?      → Azure
  (Local dev/testing?)       → LocalStack

KEY AWS SERVICES:
  Compute    → ECS Fargate (serverless containers), Lambda (functions)
  Messaging  → SQS (queue), SNS (fan-out), EventBridge (event bus)
  Storage    → S3 (objects; private by default, presigned URLs, lifecycle)
  Database   → RDS (managed relational; Multi-AZ + read replicas)

MESSAGING PICKER:
  Buffer work?     → SQS
  Fan-out to many? → SNS
  Route by rules?  → EventBridge

GOLDEN RULES:
  ✓ Managed services > self-hosting
  ✓ IAM least privilege; never use root
  ✓ Multi-AZ for HA; budgets + tags for cost
  ✓ IaC everything (see aws.md)
  ✓ LocalStack for dev/CI — never hit real AWS from tests
  ✓ Idempotent consumers + DLQs for messaging
```

---

*This file covers the cloud platform landscape and key AWS services (Part 2 of the cloud-service series). More topics (networking/VPC, CloudFront/CDN, IAM deep-dive, multi-cloud strategy) will be added as separate files over time.*
