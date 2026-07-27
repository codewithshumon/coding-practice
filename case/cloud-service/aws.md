# AWS SDK — Complete Guide

> **Series:** Cloud Service Documentation — Part 1
> This file will grow over time. New AWS topics (CDK deep-dive, Lambda patterns, DynamoDB design, etc.) will be appended as new sections below.

---

## Table of Contents

- **[AWS SDK](#aws-sdk--complete-guide)**
  - [1. What is the AWS SDK?](#1-what-is-the-aws-sdk)
  - [2. SDK vs CDK vs CLI — Know the Difference](#2-sdk-vs-cdk-vs-cli--know-the-difference)
  - [3. How Does It Work?](#3-how-does-it-work)
  - [4. Available SDKs by Language](#4-available-sdks-by-language)
  - [5. Where Should You Use It?](#5-where-should-you-use-it)
  - [6. Where NOT to Use It](#6-where-not-to-use-it)
  - [7. Installation & Setup](#7-installation--setup)
  - [8. Authentication & Credentials](#8-authentication--credentials)
  - [9. Production Best Practices](#9-production-best-practices)
  - [10. Real-World Examples](#10-real-world-examples)
  - [11. Common Pitfalls](#11-common-pitfalls)

---

## 1. What is the AWS SDK?

The **AWS SDK (Software Development Kit)** is a collection of official libraries that let your **application code** talk to AWS services (S3, DynamoDB, SQS, Lambda, etc.) programmatically.

- Instead of making raw HTTP calls to AWS APIs, you call simple methods like `s3.upload()` or `dynamodb.getItem()`.
- The SDK handles the hard parts: **request signing, retries, authentication, serialization, and error handling**.
- It runs **inside your application** — not for provisioning infrastructure.

**One-liner:** SDK = how your *app* uses AWS services at runtime.

---

## 2. SDK vs CDK vs CLI — Know the Difference

The pasted CDK text and the SDK are different tools. Don't confuse them:

| Tool | Purpose | When It Runs | Example |
|---|---|---|---|
| **AWS SDK** | Use AWS services from application code | Runtime (inside your app) | Upload a user's avatar to S3 |
| **AWS CDK** | Define/provision infrastructure as code | Deploy time (terminal/CI) | Create the S3 bucket itself |
| **AWS CLI** | Manage AWS from the command line | Manual/scripted terminal use | `aws s3 ls` to list buckets |

**Rule of thumb:**
- **CDK** creates the bucket → **SDK** puts files in the bucket → **CLI** lets you inspect the bucket.

---

## 3. How Does It Work?

The request lifecycle when your app calls an SDK method:

1. **Your code calls a method** — e.g., `s3.send(new PutObjectCommand(...))`.
2. **SDK builds an HTTP request** — serializes your parameters into AWS's wire format (JSON/XML).
3. **Request signing (SigV4)** — SDK signs the request with your credentials so AWS can verify identity.
4. **Sent over HTTPS** — to the service endpoint (e.g., `s3.us-east-1.amazonaws.com`).
5. **Automatic retries** — if AWS throttles or a network blip occurs, SDK retries with exponential backoff.
6. **Response deserialized** — AWS's response is parsed into native objects (dicts, structs, classes) and returned.

**Key point:** You never write HTTP, signatures, or retry logic — the SDK abstracts all of it.

---

## 4. Available SDKs by Language

| Language | Package Name | Install |
|---|---|---|
| Python | **Boto3** | `pip install boto3` |
| JavaScript/TypeScript (Node.js) | **AWS SDK v3** (`@aws-sdk/*`) | `npm install @aws-sdk/client-s3` |
| Java | **AWS SDK for Java 2.x** | Maven/Gradle dependency |
| Go | **aws-sdk-go-v2** | `go get github.com/aws/aws-sdk-go-v2` |
| .NET / C# | **AWSSDK.*** | NuGet |
| PHP | **aws/aws-sdk-php** | Composer |
| Rust | **aws-sdk-rust** | Cargo |

**Notes:**
- **Node.js:** Always use **v3** (modular — import only what you need, smaller bundles). v2 is legacy.
- **Python:** `boto3` is the standard; `aioboto3` exists for async.

---

## 5. Where Should You Use It?

Use the SDK whenever your **application logic needs an AWS service at runtime**:

- **File handling** — upload/download user files to S3 (avatars, invoices, media).
- **Async jobs** — push messages to SQS so workers process them in the background.
- **Notifications** — publish events to SNS (email/SMS fan-out).
- **NoSQL data** — read/write session data, leaderboards, or event logs in DynamoDB.
- **Invoking functions** — trigger a Lambda from your API server.
- **Secrets** — fetch DB passwords from Secrets Manager at startup.
- **Queues/events** — send events to EventBridge in event-driven architectures.
- **Local development** — point the SDK at **LocalStack** to test without real AWS.

---

## 6. Where NOT to Use It

- **Creating infrastructure** (buckets, tables, VPCs) → use **CDK/Terraform/CloudFormation** instead.
- **One-off admin tasks** (list buckets, check logs) → use the **CLI or Console**.
- **Frontend browsers with permanent credentials** → never embed secret keys in client-side code; use presigned URLs or Cognito instead.

---

## 7. Installation & Setup

### Python (Boto3)

```bash
pip install boto3
```

```python
import boto3

s3 = boto3.client("s3", region_name="us-east-1")
s3.upload_file("report.pdf", "my-bucket", "reports/report.pdf")
```

### Node.js (SDK v3)

```bash
npm install @aws-sdk/client-s3
```

```typescript
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

const s3 = new S3Client({ region: "us-east-1" });
await s3.send(new PutObjectCommand({
  Bucket: "my-bucket",
  Key: "reports/report.pdf",
  Body: fileBuffer,
}));
```

**Pattern:** Create the client once, reuse it everywhere (see best practices).

---

## 8. Authentication & Credentials

The SDK resolves credentials in a **priority chain** — first match wins:

1. **Explicit in code** (hardcoded — ❌ never in production)
2. **Environment variables** — `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
3. **Shared credentials file** — `~/.aws/credentials` (via `aws configure`)
4. **IAM Role** — attached to EC2/ECS/Lambda (✅ **best for production**)
5. **SSO / Cognito / container credentials**

**Golden rules:**
- **In production on AWS:** use **IAM Roles** — no keys in code, no keys in env files. AWS rotates them automatically.
- **Locally:** use `aws configure` or SSO (`aws sso login`).
- **Never commit credentials** to git. Ever.

---

## 9. Production Best Practices

1. **Use IAM Roles, not access keys** — attach roles to Lambda/ECS/EC2; let AWS handle rotation.
2. **Create clients once, reuse them** — client creation is expensive (TCP/TLS setup). Instantiate at module level, not per request.
3. **Least-privilege IAM policies** — grant only exact actions/resources needed (`s3:PutObject` on one bucket, not `s3:*` on `*`).
4. **Set timeouts explicitly** — defaults can hang requests for minutes; set connect/read timeouts per your SLA.
5. **Respect retries — don't stack them** — SDK retries internally; adding your own loop on top amplifies load (thundering herd). Configure `maxAttempts` instead.
6. **Handle throttling gracefully** — catch `ThrottlingException` / `ProvisionedThroughputExceededException`; back off and queue work.
7. **Use pagination helpers** — list APIs (`ListObjects`, `Scan`) return partial results; always loop with `NextToken`/paginators or you'll silently miss data.
8. **Use presigned URLs for client uploads** — browsers/mobile upload directly to S3; your server only signs. No proxying large files through your API.
9. **Keep secrets out of code** — load from Secrets Manager / SSM Parameter Store at startup, not from `.env` files baked into images.
10. **Enable logging & tracing** — log request IDs, integrate with X-Ray/CloudWatch for debugging distributed calls.
11. **Pin SDK versions & update regularly** — security patches and service updates ship frequently.
12. **Use LocalStack for tests** — never hit real AWS from CI; mock with LocalStack or `moto` (Python).
13. **Batch where possible** — `BatchWriteItem` (DynamoDB), `SendMessageBatch` (SQS) — fewer round trips, lower cost.
14. **Delete vs terminate lifecycle** — always clean up temp objects (S3 lifecycle rules) to avoid cost leaks.

---

## 10. Real-World Examples

### Example 1 — S3 Presigned Upload (Python + FastAPI)

User uploads a profile photo directly to S3; the server only generates a signed URL.

```python
import boto3

s3 = boto3.client("s3")

def get_upload_url(user_id: str) -> str:
    return s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": "avatars-prod", "Key": f"{user_id}.jpg",
                "ContentType": "image/jpeg"},
        ExpiresIn=300,  # URL valid for 5 minutes
    )
```

**Why:** your API never touches the file bytes — scales to huge uploads for free.

### Example 2 — SQS Background Job Queue (Node.js / NestJS)

API responds instantly; email sending happens asynchronously in a worker.

```typescript
import { SQSClient, SendMessageCommand } from "@aws-sdk/client-sqs";

const sqs = new SQSClient({ region: "us-east-1" }); // created once

async function queueWelcomeEmail(userId: string, email: string) {
  await sqs.send(new SendMessageCommand({
    QueueUrl: process.env.EMAIL_QUEUE_URL,
    MessageBody: JSON.stringify({ userId, email, type: "WELCOME" }),
  }));
}
```

**Why:** user signup stays fast even if the email provider is slow or down.

### Example 3 — DynamoDB Session Store (Python)

```python
import boto3
from datetime import datetime, timedelta, timezone

table = boto3.resource("dynamodb").Table("sessions")

def create_session(session_id: str, user_id: str):
    table.put_item(Item={
        "session_id": session_id,
        "user_id": user_id,
        "expires_at": int((datetime.now(timezone.utc) + timedelta(hours=24)).timestamp()),
    })
```

**Why:** single-digit ms reads at any scale; TTL auto-deletes expired sessions (free cleanup).

### Example 4 — Secrets Manager at Startup (Node.js)

```typescript
import { SecretsManagerClient, GetSecretValueCommand }
  from "@aws-sdk/client-secrets-manager";

const sm = new SecretsManagerClient({});

export async function loadDbPassword(): Promise<string> {
  const res = await sm.send(new GetSecretValueCommand({ SecretId: "prod/db/password" }));
  return JSON.parse(res.SecretString!).password;
}
```

**Why:** no passwords in env files or images; rotate secrets without redeploying.

### Example 5 — Fan-Out Event with SNS (Python)

```python
import boto3, json

sns = boto3.client("sns")

def publish_order_created(order: dict):
    sns.publish(
        TopicArn="arn:aws:sns:us-east-1:123456789:order-events",
        Message=json.dumps({"event": "ORDER_CREATED", "order": order}),
    )
```

**Why:** one publish → email service, analytics service, and inventory service each get their own copy via their SQS subscriptions (pub/sub fan-out).

### Example 6 — Local Testing with LocalStack

```bash
# Run mock AWS locally
docker run -p 4566:4566 localstack/localstack
```

```python
import boto3

s3 = boto3.client("s3", endpoint_url="http://localhost:4566",
                  aws_access_key_id="test", aws_secret_access_key="test")
s3.create_bucket(Bucket="dev-bucket")  # zero cost, zero risk
```

**Why:** full SDK behavior on your laptop — perfect for CI pipelines.

---

## 11. Common Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Hardcoded credentials | Leaked keys, security breach | IAM Roles / `aws configure` |
| New client per request | High latency, socket exhaustion | Create client once at module level |
| Ignoring pagination | "Some records randomly missing" | Always loop with paginators/NextToken |
| Double retry loops | Request storms during outages | Configure SDK `maxAttempts`, don't wrap in your own retry |
| No timeouts | Hung requests block workers | Set explicit connect/read timeouts |
| Proxying uploads through API | Slow API, high memory | Presigned URLs, direct-to-S3 |
| `s3:*` on `*` IAM policy | Over-privileged, audit failures | Least-privilege scoped policies |
| Testing against real AWS | Surprise bills, mutated prod data | LocalStack / moto in CI |

---

## Quick Reference Card

```
SDK  → app code talking to AWS services at RUNTIME
CDK  → code defining infrastructure at DEPLOY time
CLI  → humans/scripts managing AWS from TERMINAL

Auth priority: IAM Role > env vars > ~/.aws/credentials > hardcoded (never)

Production checklist:
✓ IAM roles, least privilege    ✓ Reuse clients      ✓ Pagination everywhere
✓ Explicit timeouts             ✓ Presigned URLs     ✓ LocalStack for tests
✓ Secrets Manager               ✓ Batch APIs         ✓ Pin & update versions
```

---

*More sections (AWS CDK deep-dive, Lambda patterns, DynamoDB design, etc.) will be added to this file over time.*
