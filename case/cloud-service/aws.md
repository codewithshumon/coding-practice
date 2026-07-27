# AWS — Complete Guide (SDK, CDK & CLI)

> **Series:** Cloud Service Documentation — Part 1
> This file holds the **three ways to interact with AWS at the code/tooling level**: the **SDK** (runtime code), the **CDK** (infrastructure as code), and the **CLI** (terminal). More cloud topics (GCP, Azure, deep-dives) will be added as separate files later.

---

## Table of Contents

- [Quick Orientation — SDK vs CDK vs CLI](#quick-orientation--sdk-vs-cdk-vs-cli)
- **AWS SDK**
  - [1. What is the AWS SDK?](#1-what-is-the-aws-sdk)
  - [2. SDK vs CDK vs CLI vs Raw HTTP](#2-sdk-vs-cdk-vs-cli-vs-raw-http)
  - [3. How Does It Work?](#3-how-does-the-sdk-work)
  - [4. SDKs by Language](#4-sdks-by-language)
  - [5. Where to Use It](#5-where-to-use-the-sdk)
  - [6. Where NOT to Use It](#6-where-not-to-use-the-sdk)
  - [7. Installation & Setup](#7-sdk-installation--setup)
  - [8. Authentication & Credentials](#8-sdk-authentication--credentials)
  - [9. Production Best Practices](#9-sdk-production-best-practices)
  - [10. Real-World Examples](#10-sdk-real-world-examples)
  - [11. Common Pitfalls](#11-sdk-common-pitfalls)
- **AWS CDK**
  - [12. What is the AWS CDK?](#12-what-is-the-aws-cdk)
  - [13. CDK vs Terraform vs CloudFormation](#13-cdk-vs-terraform-vs-cloudformation)
  - [14. How Does It Work?](#14-how-does-cdk-work)
  - [15. CDK Languages & Constructs](#15-cdk-languages--constructs)
  - [16. Where to Use CDK](#16-where-to-use-cdk)
  - [17. Where NOT to Use CDK](#17-where-not-to-use-cdk)
  - [18. Installation & Setup](#18-cdk-installation--setup)
  - [19. Authentication & Environments](#19-cdk-authentication--environments)
  - [20. Production Best Practices](#20-cdk-production-best-practices)
  - [21. Real-World Examples](#21-cdk-real-world-examples)
  - [22. Common Pitfalls](#22-cdk-common-pitfalls)
- **AWS CLI**
  - [23. What is the AWS CLI?](#23-what-is-the-aws-cli)
  - [24. CLI vs Console vs SDK](#24-cli-vs-console-vs-sdk)
  - [25. How Does It Work?](#25-how-does-the-cli-work)
  - [26. CLI Versions (v1 vs v2)](#26-cli-versions-v1-vs-v2)
  - [27. Where to Use the CLI](#27-where-to-use-the-cli)
  - [28. Where NOT to Use the CLI](#28-where-not-to-use-the-cli)
  - [29. Installation & Setup](#29-cli-installation--setup)
  - [30. Authentication, Profiles & SSO](#30-cli-authentication-profiles--sso)
  - [31. Production Best Practices](#31-cli-production-best-practices)
  - [32. Real-World Examples](#32-cli-real-world-examples)
  - [33. Common Pitfalls](#33-cli-common-pitfalls)
- [Shared Foundations](#shared-foundations)
- [Quick Reference Card](#quick-reference-card)

---

## Quick Orientation — SDK vs CDK vs CLI

These three tools are the standard ways to interact with AWS. They operate at **different stages** and are usually used **together**:

| Tool | One-line job | Runs when | Example |
|---|---|---|---|
| **AWS SDK** | Your **app code** calls AWS services | Runtime (inside your running app) | Upload a user's file to S3 |
| **AWS CDK** | Your **code defines & provisions** infrastructure | Deploy time (from terminal/CI) | Create the S3 bucket itself |
| **AWS CLI** | **You/scripts manage** AWS from the terminal | Ad-hoc / scripted terminal use | `aws s3 ls` to list buckets |

**Rule of thumb:** **CDK** creates the bucket → **SDK** puts files in it at runtime → **CLI** lets you inspect/manage it from the terminal. They are companions, not competitors.

**Decision guide:**
- *Need to call AWS from application code?* → **SDK**
- *Need to create/change infrastructure reproducibly?* → **CDK**
- *Need to inspect, debug, or run one-off commands?* → **CLI**

---

# AWS SDK

## 1. What is the AWS SDK?

The **AWS SDK (Software Development Kit)** is a set of official libraries that let your **application code** talk to AWS services (S3, DynamoDB, SQS, Lambda, etc.) programmatically.

- Instead of raw HTTP calls to AWS APIs, you call methods like `s3.upload()` or `dynamodb.getItem()`.
- The SDK handles the hard parts: **request signing, retries, auth, serialization, error handling**.
- It runs **inside your application** — not for provisioning infrastructure.

**One-liner:** SDK = how your *app* uses AWS services at runtime.

## 2. SDK vs CDK vs CLI vs Raw HTTP

| Option | Pros | Cons | Use when |
|---|---|---|---|
| **AWS SDK** | High-level, handles signing/retries/pagination | Adds a dependency | Your app needs AWS at runtime |
| **Raw HTTP / fetch** | Zero dependencies | You must implement SigV4 signing, retries, parsing yourself — error-prone | Almost never |
| **CDK / CLI** | Different stage (infra / terminal) | Can't run inside app request paths | Not applicable to runtime app calls |

**Key point:** For runtime AWS calls, always prefer the SDK over hand-rolled HTTP.

## 3. How Does the SDK Work?

The request lifecycle when your app calls an SDK method:

1. **Code calls a method** — e.g., `s3.send(new PutObjectCommand(...))`.
2. **SDK builds an HTTP request** — serializes params into AWS's wire format (JSON/XML).
3. **Request signing (SigV4)** — SDK signs the request with your credentials so AWS verifies identity.
4. **Sent over HTTPS** — to the service endpoint (e.g., `s3.us-east-1.amazonaws.com`).
5. **Automatic retries** — on throttle or network blip, SDK retries with exponential backoff.
6. **Response deserialized** — parsed into native objects (dicts/classes) and returned.

**Key point:** You never write HTTP, signatures, or retry logic — the SDK abstracts all of it.

## 4. SDKs by Language

| Language | Package | Install |
|---|---|---|
| Python | **Boto3** | `pip install boto3` |
| JavaScript/TypeScript | **AWS SDK v3** (`@aws-sdk/*`) | `npm install @aws-sdk/client-s3` |
| Java | **AWS SDK for Java 2.x** | Maven/Gradle |
| Go | **aws-sdk-go-v2** | `go get github.com/aws/aws-sdk-go-v2` |
| .NET / C# | **AWSSDK.*** | NuGet |
| PHP | **aws/aws-sdk-php** | Composer |
| Rust | **aws-sdk-rust** | Cargo |

**Notes:**
- **Node.js:** always use **v3** (modular — import only what you need, smaller bundles). v2 is legacy.
- **Python:** `boto3` is standard; `aioboto3` for async.

## 5. Where to Use the SDK

Use it whenever your **application logic needs an AWS service at runtime**:

- **File handling** — upload/download user files to S3 (avatars, invoices, media).
- **Async jobs** — push messages to SQS for background workers.
- **Notifications** — publish events to SNS (email/SMS fan-out).
- **NoSQL data** — read/write session data or logs in DynamoDB.
- **Invoke functions** — trigger a Lambda from your API server.
- **Secrets** — fetch DB passwords from Secrets Manager at startup.
- **Events** — send events to EventBridge in event-driven systems.
- **Local dev** — point the SDK at **LocalStack** to test without real AWS.

## 6. Where NOT to Use the SDK

- **Creating infrastructure** (buckets, tables, VPCs) → use **CDK/Terraform/CloudFormation**.
- **One-off admin tasks** (list buckets, check logs) → use the **CLI or Console**.
- **Frontend browsers with permanent credentials** → never embed secret keys in client code; use presigned URLs or Cognito instead.

## 7. SDK Installation & Setup

**Python (Boto3):**

```bash
pip install boto3
```

```python
import boto3

s3 = boto3.client("s3", region_name="us-east-1")
s3.upload_file("report.pdf", "my-bucket", "reports/report.pdf")
```

**Node.js (SDK v3):**

```bash
npm install @aws-sdk/client-s3
```

```typescript
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

const s3 = new S3Client({ region: "us-east-1" });
await s3.send(new PutObjectCommand({
  Bucket: "my-bucket", Key: "reports/report.pdf", Body: fileBuffer,
}));
```

**Pattern:** create the client **once** at module level, reuse it everywhere (client creation is expensive).

## 8. SDK Authentication & Credentials

The SDK resolves credentials via a **priority chain** (first match wins):

1. **Explicit in code** (hardcoded — ❌ never in production)
2. **Environment variables** — `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
3. **Shared credentials file** — `~/.aws/credentials` (via `aws configure`)
4. **IAM Role** — attached to EC2/ECS/Lambda (✅ best for production)
5. **SSO / Cognito / container credentials**

**Golden rules:**
- **In production on AWS:** use **IAM Roles** — no keys in code/env. AWS rotates them automatically.
- **Locally:** `aws configure` or SSO (`aws sso login`).
- **Never commit credentials** to git. Ever.

## 9. SDK Production Best Practices

1. **IAM Roles, not access keys** — attach roles to Lambda/ECS/EC2.
2. **Create clients once, reuse them** — module-level, not per request.
3. **Least-privilege IAM** — `s3:PutObject` on one bucket, not `s3:*` on `*`.
4. **Set explicit timeouts** — defaults can hang for minutes.
5. **Don't stack retries** — SDK retries internally; configure `maxAttempts`, don't wrap in your own loop.
6. **Handle throttling** — catch `ThrottlingException`; back off and queue work.
7. **Always paginate** — list APIs return partial results; loop with `NextToken`/paginators.
8. **Presigned URLs for client uploads** — browsers upload directly to S3; server only signs.
9. **Secrets out of code** — Secrets Manager / SSM at startup, not baked into images.
10. **Log & trace** — request IDs + X-Ray/CloudWatch for distributed debugging.
11. **Pin & update SDK versions** — security patches ship frequently.
12. **Mock AWS in tests** — LocalStack / `moto`, never hit real AWS from CI.
13. **Batch calls** — `BatchWriteItem`, `SendMessageBatch` — fewer round trips, lower cost.

## 10. SDK Real-World Examples

### Example 1 — S3 Presigned Upload (Python + FastAPI)
```python
import boto3
s3 = boto3.client("s3")

def get_upload_url(user_id: str) -> str:
    return s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": "avatars-prod", "Key": f"{user_id}.jpg",
                "ContentType": "image/jpeg"},
        ExpiresIn=300,  # 5 minutes
    )
```
**Why:** your API never touches file bytes — scales to huge uploads for free.

### Example 2 — SQS Background Queue (Node.js / NestJS)
```typescript
import { SQSClient, SendMessageCommand } from "@aws-sdk/client-sqs";
const sqs = new SQSClient({ region: "us-east-1" }); // once

async function queueWelcomeEmail(userId: string, email: string) {
  await sqs.send(new SendMessageCommand({
    QueueUrl: process.env.EMAIL_QUEUE_URL,
    MessageBody: JSON.stringify({ userId, email, type: "WELCOME" }),
  }));
}
```
**Why:** signup stays fast even if the email provider is slow/down.

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
**Why:** single-digit ms reads at any scale; TTL auto-deletes expired sessions.

### Example 4 — Secrets Manager at Startup (Node.js)
```typescript
import { SecretsManagerClient, GetSecretValueCommand } from "@aws-sdk/client-secrets-manager";
const sm = new SecretsManagerClient({});

export async function loadDbPassword() {
  const res = await sm.send(new GetSecretValueCommand({ SecretId: "prod/db/password" }));
  return JSON.parse(res.SecretString!).password;
}
```
**Why:** no passwords in env files; rotate secrets without redeploying.

### Example 5 — SNS Fan-Out (Python)
```python
import boto3, json
sns = boto3.client("sns")

def publish_order_created(order: dict):
    sns.publish(
        TopicArn="arn:aws:sns:us-east-1:123456789:order-events",
        Message=json.dumps({"event": "ORDER_CREATED", "order": order}),
    )
```
**Why:** one publish → email, analytics, and inventory services each get their copy via SQS subscriptions.

### Example 6 — Local Testing with LocalStack
```bash
docker run -p 4566:4566 localstack/localstack
```
```python
import boto3
s3 = boto3.client("s3", endpoint_url="http://localhost:4566",
                  aws_access_key_id="test", aws_secret_access_key="test")
s3.create_bucket(Bucket="dev-bucket")  # zero cost, zero risk
```
**Why:** full SDK behavior on your laptop — perfect for CI.

## 11. SDK Common Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Hardcoded credentials | Leaked keys, breach | IAM Roles / `aws configure` |
| New client per request | Latency, socket exhaustion | Create once at module level |
| Ignoring pagination | "Some records missing" | Loop with paginators/NextToken |
| Double retry loops | Request storms | Configure SDK `maxAttempts` |
| No timeouts | Hung requests | Set explicit connect/read timeouts |
| Proxying uploads through API | Slow API, high memory | Presigned URLs, direct-to-S3 |
| `s3:*` on `*` policy | Over-privileged | Least-privilege scoped policies |
| Testing against real AWS | Surprise bills | LocalStack / moto in CI |

---

# AWS CDK

## 12. What is the AWS CDK?

The **AWS CDK (Cloud Development Kit)** is an open-source framework for **defining cloud infrastructure as code** using familiar programming languages (TypeScript, Python, Java, C#).

- It replaces manual AWS Console clicking and massive hand-written JSON/YAML CloudFormation templates.
- You write real code with loops, conditionals, and functions to describe resources.
- On deploy, the CDK **compiles your code into a CloudFormation template** and provisions it.

**One-liner:** CDK = define AWS infrastructure with the expressiveness of a real programming language.

## 13. CDK vs Terraform vs CloudFormation

| Tool | Language | Model | Notes |
|---|---|---|---|
| **AWS CDK** | TS, Python, Java, C# | Imperative code → CloudFormation | Best when your team already codes; rich logic/abstraction |
| **Terraform** | HCL (declarative) | Multi-cloud | Best for multi-cloud or ops-heavy teams |
| **CloudFormation** | JSON/YAML (declarative) | AWS-native | Best for pure declarative, no build step |
| **Pulumi** | TS, Python, Go | Imperative → multi-cloud | Like CDK but cloud-agnostic |

**Rule of thumb:** already on AWS and want code-level abstraction? **CDK**. Multi-cloud? **Terraform/Pulumi**. Want zero build step? **CloudFormation**.

## 14. How Does CDK Work?

1. **You write constructs** — code objects representing AWS resources (a bucket, a queue).
2. **`cdk synth`** — the CDK compiles your app into a **CloudFormation template** (JSON/YAML).
3. **`cdk deploy`** — CDK uploads the template to CloudFormation, which creates/updates the real resources.
4. **CloudFormation does the actual provisioning** — CDK is a *generator*; CloudFormation is the *engine*.
5. **State lives in CloudFormation** — `cdk diff` and `cdk destroy` operate against the deployed stack.

**Key point:** CDK never provisions directly — it always goes through CloudFormation, so you keep drift detection, rollback, and stack history.

## 15. CDK Languages & Constructs

**Supported languages:** TypeScript, Python, Java, C# (.NET), Go.

**Construct levels:**
| Level | What it is | Example |
|---|---|---|
| **L1** | Raw CloudFormation resource (1:1) | `s3.CfnBucket` |
| **L2** | Opinionated, best-practice wrapper (recommended) | `s3.Bucket` (adds encryption, versioning defaults) |
| **L3 / Patterns** | Multi-resource bundle | `aws-s3-deployment.BucketDeployment` |

**Where it runs:** the CDK CLI is a **Node.js** tool — install it locally, on a VPS (centralized CI), or in **Docker** for reproducible versions. Pair with **LocalStack** to test stacks locally without hitting real AWS.

## 16. Where to Use CDK

- **Provisioning any AWS resource** — S3, DynamoDB, Lambda, VPC, ECS, queues, topics.
- **Repeatable environments** — spin up identical dev/staging/prod stacks.
- **Infrastructure with logic** — loops to create N buckets, conditionals per region.
- **Version-controlled infra** — review infrastructure changes in pull requests.
- **CI/CD pipelines** — deploy infra as part of your release process.

## 17. Where NOT to Use CDK

- **Calling AWS from app code at runtime** → that's the **SDK**.
- **Quick one-off inspection** (list a bucket, tail logs) → use the **CLI**.
- **Multi-cloud requirements** → Terraform/Pulumi are purpose-built for that.
- **Non-AWS resources** → CDK is AWS-specific (except community `cdktf`/`cdk8s` variants).

## 18. CDK Installation & Setup

**Step 1 — Install Node.js + the CDK CLI:**
```bash
npm install -g aws-cdk
cdk --version
```

**Step 2 — Init a project (e.g., Python):**
```bash
mkdir my-cdk-app && cd my-cdk-app
cdk init app --language python
```

**Step 3 — Define infrastructure** (`my_cdk_app/my_cdk_app_stack.py`):
```python
from aws_cdk import Stack
from aws_cdk import aws_s3 as s3
from constructs import Construct

class MyCdkAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        s3.Bucket(self, "MyFirstBucket", versioned=True)  # L2 construct
```

**Step 4 — Deploy:**
```bash
cdk bootstrap   # one-time per account/region
cdk synth       # preview the generated CloudFormation template
cdk diff        # see what will change vs. live stack
cdk deploy      # provision to your live AWS account
cdk destroy     # tear it down when done
```

**Pattern:** always run `cdk synth` + `cdk diff` **before** `cdk deploy` — catch mistakes before they hit your account.

## 19. CDK Authentication & Environments

The CDK CLI uses the **same credential chain as the SDK/CLI** (env vars → `~/.aws/credentials` → IAM Role → SSO). Two deployment concepts to know:

- **Bootstrap** — `cdk bootstrap` creates a one-time staging bucket + IAM roles in each **account/region** you deploy to.
- **Environments** — each Stack takes an `env={account, region}`. Pin it explicitly so a stack always deploys to the right account (never accidentally prod).

```python
from aws_cdk import Environment
MyCdkAppStack(app, "ProdStack", env=Environment(account="123456789012", region="us-east-1"))
```

**Golden rules:**
- Use **separate AWS accounts** for dev/staging/prod.
- Pass credentials via **env vars or IAM Role in CI** — never hardcode.
- Use **SSO** for human developers.

## 20. CDK Production Best Practices

1. **Prefer L2/L3 constructs over L1** — they bake in security best practices.
2. **Pin CDK + construct library versions** — upgrades can change generated templates.
3. **One-time bootstrap per account/region** — don't skip it; CI deploys will fail otherwise.
4. **Explicit `env` on every stack** — avoids accidental cross-account deploys.
5. **Review `cdk diff` in PRs** — treat infra changes like code changes.
6. **No secrets in stack code** — reference Secrets Manager / SSM, never inline passwords.
7. **Enable termination protection** on production stacks.
8. **Tag everything** — cost allocation via stack-level tags.
9. **Separate dev/prod CDK apps or stages** — use the `Stage`/`Environment` pattern.
10. **Use `cdk destroy` carefully** — it deletes real resources; protect prod with policies.
11. **Test with LocalStack or `cdk synth` in CI** — never `cdk deploy` to prod from a laptop.
12. **Set CloudWatch budgets/alarms** — catch cost surprises from misconfigured resources.

## 21. CDK Real-World Examples

### Example 1 — S3 Bucket with Encryption + Lifecycle (Python)
```python
from aws_cdk import Stack, Duration, RemovalPolicy
from aws_cdk import aws_s3 as s3
from constructs import Construct

class StorageStack(Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        s3.Bucket(self, "DataBucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=RemovalPolicy.RETAIN,  # don't delete on stack destroy
            lifecycle_rules=[{"expiration": Duration.days(90)}],
        )
```
**Why:** production-safe defaults — encrypted, retained, auto-expiring.

### Example 2 — Lambda Behind API Gateway (TypeScript)
```typescript
import * as cdk from "aws-cdk-lib";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as apigw from "aws-cdk-lib/aws-apigateway";

export class ApiStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string) {
    super(scope, id);
    const fn = new lambda.Function(this, "HelloHandler", {
      runtime: lambda.Runtime.NODEJS_20_X,
      handler: "index.handler",
      code: lambda.Code.fromAsset("lambda"),
    });
    new apigw.LambdaRestApi(this, "Endpoint", { handler: fn });
  });
}
```
**Why:** one pattern wires up a serverless HTTP API — no manual console config.

### Example 3 — DynamoDB Table with Autoscaling
```python
from aws_cdk import aws_dynamodb as ddb

table = ddb.Table(self, "Orders",
    partition_key=ddb.Attribute(name="order_id", type=ddb.AttributeType.STRING),
    billing_mode=ddb.BillingMode.PAY_PER_REQUEST,  # autoscaling built-in
    point_in_time_recovery_specification=True,
)
```
**Why:** on-demand capacity + PITR = no throttle tuning, recoverable.

### Example 4 — Multi-Environment (Dev/Prod) with Stages
```python
from aws_cdk import App, Environment

app = App()
MyStack(app, "Dev",  env=Environment(account="111111", region="us-east-1"))
MyStack(app, "Prod", env=Environment(account="222222", region="us-east-1"))
app.synth()
```
**Why:** same code, isolated accounts — `cdk deploy Dev` vs `cdk deploy Prod`.

### Example 5 — VPC + ECS Fargate Cluster
```typescript
const vpc = new ec2.Vpc(this, "Vpc", { maxAzs: 2 });
const cluster = new ecs.Cluster(this, "Cluster", { vpc });
cluster.addFargateCapacity... // Fargate services attach here
```
**Why:** reproducible network + compute in a few lines instead of hours of console clicking.

### Example 6 — Test Locally with LocalStack
```bash
cdklocal synth      # uses localstack instead of AWS
cdklocal deploy
```
**Why:** iterate on infra without touching (or paying for) the real cloud.

## 22. CDK Common Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Forgot `cdk bootstrap` | Deploy fails with missing roles | Run once per account/region |
| No explicit `env` | Deploys to wrong/random account | Set `env={account, region}` on every stack |
| Skipping `cdk diff` | Accidental destructive changes | Always review diff in PRs |
| Secrets in stack code | Credentials in CloudFormation/-git | Reference Secrets Manager/SSM |
| Unpinned versions | Upgrade silently changes infra | Pin CDK + construct versions |
| `cdk destroy` on prod | Real resources deleted | Termination protection + access controls |
| Using L1 everywhere | Missing best-practice defaults | Prefer L2/L3 constructs |
| Deploying prod from laptop | Untracked, risky changes | Deploy only via CI |

---

# AWS CLI

## 23. What is the AWS CLI?

The **AWS CLI (Command Line Interface)** is a unified tool to **manage AWS services from the terminal**. You run commands like `aws s3 ls`, `aws lambda invoke`, or `aws ec2 describe-instances`.

- It wraps the same AWS APIs the SDK uses, but for **human/scripted use**.
- Great for **inspection, debugging, automation scripts, and quick one-off tasks**.
- Output in **JSON, table, or text**; queryable with `--query` (JMESPath).

**One-liner:** CLI = manage AWS from the terminal, ad-hoc or scripted.

## 24. CLI vs Console vs SDK

| Option | Best for | Limitation |
|---|---|---|
| **AWS CLI** | Inspecting/debugging, shell scripts, quick ops | Not for in-app runtime calls |
| **AWS Console** | Visual exploration, first-time learning | Not reproducible/scriptable |
| **AWS SDK** | Calls inside your application code | Overkill for one-off commands |

**Rule of thumb:** exploring by hand → **Console**; scripting/inspecting → **CLI**; calling from app code → **SDK**.

## 25. How Does the CLI Work?

1. **Parse the command** — `aws <service> <operation>`, e.g., `aws s3 ls`.
2. **Resolve credentials** — same chain as SDK (env → profile → role → SSO).
3. **Sign + send the request** — botocore signs (SigV4) and calls the AWS API over HTTPS.
4. **Receive response** — CLI formats it (JSON/table/text) and prints.
5. **Auto-paginate** — list commands fetch all pages unless `--no-paginate`.

**Key point:** the CLI is essentially the SDK exposed as shell commands — same auth, same signing, same APIs.

## 26. CLI Versions (v1 vs v2)

| | **v1** | **v2 (current)** |
|---|---|---|
| Status | Legacy | **Recommended** |
| Install | `pip install awscli` | Official installer / package manager |
| SSO | Plugin needed | **Built-in** |
| Features | Older | Better streaming, Docker ECS auth, stable |

**Use v2** unless you have a specific reason. Install via the official installer (not pip) for v2.

## 27. Where to Use the CLI

- **Inspect resources** — `aws s3 ls`, `aws ec2 describe-instances`.
- **Debug** — tail logs, check queue depth, describe a stack.
- **Automation scripts** — bash/CI scripts that provision or query AWS.
- **Manage credentials/profiles** — `aws configure`, `aws sso login`.
- **Quick data pulls** — export a DynamoDB scan, list IAM users.
- **Glue between tools** — pipe AWS output into `jq` or other CLIs.

## 28. Where NOT to Use the CLI

- **In-app runtime calls** → use the **SDK** (shelling out to `aws` from app code is slow and fragile).
- **Reproducible infrastructure** → use **CDK/Terraform** (CLI commands aren't declarative state).
- **Anything needing a UI for exploration** → the **Console** may be faster.

## 29. CLI Installation & Setup

**Install v2 (Linux/macOS/Windows — official installer):** see `docs.aws.amazon.com/cli`. On most systems:
```bash
# macOS (Homebrew)
brew install awscli

# Ubuntu/Debian (v2 via official bundle)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install

aws --version
```

**Configure credentials:**
```bash
aws configure
# prompts for: Access Key ID, Secret Access Key, region, output format
```

**Output formats:** `json` (default, best with `jq`), `table` (human-readable), `text` (script-friendly).

## 30. CLI Authentication, Profiles & SSO

**Profiles** — manage multiple accounts/roles in `~/.aws/credentials` and `~/.aws/config`:
```bash
aws configure --profile work-prod        # set up a named profile
aws s3 ls --profile work-prod            # use it
export AWS_PROFILE=work-prod             # or set as default for the session
```

**SSO (recommended for orgs):**
```bash
aws sso login --profile my-sso           # opens browser, short-lived creds
```

**Priority chain** (same as SDK): explicit flags → env vars → `AWS_PROFILE` → default profile → IAM role → SSO.

**Golden rules:**
- Prefer **SSO or roles** over long-lived access keys.
- Use **named profiles** to avoid accidentally hitting prod.
- Set `AWS_PROFILE` explicitly in CI scripts.

## 31. CLI Production Best Practices

1. **Use v2** — built-in SSO, maintained.
2. **Prefer SSO/roles** over static access keys.
3. **Named profiles per environment** — `dev`, `staging`, `prod`.
4. **Pin output format** — `json` + `jq` for scripting; `--query` for targeted fields.
5. **Use `--dry-run`** on destructive ops to preview.
6. **Let the CLI paginate** — don't manually loop unless you need `--no-paginate`.
7. **`aws s3 sync` over `cp` loops** — sync handles diffs efficiently.
8. **Quote `--query` strings** — JMESPath is picky about shell escaping.
9. **Don't shell out from app code** — use the SDK instead.
10. **Protect credentials** — never echo keys in logs/CI output; rotate regularly.
11. **Combine with `jq`/`yq`** for powerful one-liners.

## 32. CLI Real-World Examples

### Example 1 — List S3 Buckets (JSON + jq)
```bash
aws s3 ls                          # simple human list
aws s3api list-buckets --query 'Buckets[].Name' --output text   # just names
```

### Example 2 — Upload/Sync a Folder
```bash
aws s3 cp ./reports s3://my-bucket/reports/ --recursive
aws s3 sync ./website s3://my-bucket/site/ --delete   # mirror, removing extras
```
**Why:** `sync` only transfers changed files — fast and cheap.

### Example 3 — Invoke a Lambda
```bash
aws lambda invoke --function-name my-fn --payload '{"key":"value"}' out.json
cat out.json
```

### Example 4 — Switch Profiles / SSO Login
```bash
aws sso login --profile work-sso
aws sts get-caller-identity --profile work-sso   # verify who you are
```

### Example 5 — Query EC2 Instances with --query
```bash
aws ec2 describe-instances \
  --query 'Reservations[].Instances[].[InstanceId,State.Name,InstanceType]' \
  --output table
```
**Why:** `--query` extracts exactly the columns you want — no post-processing.

### Example 6 — Debug a Deployed Stack
```bash
aws cloudformation describe-stacks --stack-name ProdStack
aws cloudformation describe-stack-events --stack-name ProdStack   # see failures
aws logs tail /aws/lambda/my-fn --follow                          # live logs
```

## 33. CLI Common Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Wrong profile active | Operates on prod accidentally | Use named profiles + `AWS_PROFILE` |
| Long-lived keys | Credential leak risk | SSO / IAM roles |
| Shelling out from app code | Slow, fragile, parsing hell | Use the SDK |
| Unquoted `--query` | Shell mangles JMESPath | Quote the query string |
| `cp` loop for many files | Slow, many requests | Use `aws s3 sync` |
| Using v1 | Missing SSO/features | Upgrade to v2 |
| Default region unset | "Region missing" errors | Set region in `aws configure` |
| Treating CLI as IaC | State drifts, not reproducible | Use CDK/Terraform |

---

## Shared Foundations

Concepts common to **all three tools** (SDK, CDK, CLI):

- **Regions & endpoints** — every call targets a region; pick the one closest to users. Set a default via `aws configure` or `AWS_DEFAULT_REGION`.
- **IAM least privilege** — grant only the exact actions/resources needed. Audits catch over-broad policies (`*:*`).
- **Credential chain** — all three resolve credentials the same way (env → file → role → SSO). Reuse one configured identity across all three.
- **SigV4 signing** — every AWS request is cryptographically signed; SDK/CLI/CDK handle it for you automatically.
- **Cost safety** — set CloudWatch **budgets + alarms**; use lifecycle rules/`cdk destroy`/`--dry-run` to avoid surprise bills. Test with **LocalStack** to never touch real AWS during development.

---

## Quick Reference Card

```
SDK  → app code talking to AWS at RUNTIME        (Boto3, @aws-sdk v3)
CDK  → code defining infrastructure at DEPLOY    (aws-cdk, → CloudFormation)
CLI  → manage AWS from the TERMINAL              (aws ..., v2)

THE FLOW:  CDK creates the bucket → SDK fills it → CLI inspects it

Auth chain (all three): explicit > env vars > ~/.aws profile > IAM role > SSO
Production:  IAM roles + least privilege  >  static keys (avoid)

Tool picker:
  App needs AWS at runtime?        → SDK
  Reproducible infra?              → CDK
  Inspect / one-off / script?      → CLI

Checklist:
  ✓ IAM roles, least privilege     ✓ Reuse SDK clients     ✓ Paginate
  ✓ Explicit timeouts              ✓ Presigned uploads     ✓ LocalStack for tests
  ✓ cdk diff before cdk deploy     ✓ Explicit stack env    ✓ Pin versions
  ✓ CLI v2 + SSO                   ✓ Named profiles        ✓ aws s3 sync
```

---

*This file covers the three core AWS interaction tools. More cloud topics (GCP, Azure, service deep-dives) will be added as separate files in this series over time.*
