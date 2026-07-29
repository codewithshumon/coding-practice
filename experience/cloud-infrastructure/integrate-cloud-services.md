# Integrate Cloud Services

> **Category:** Cloud & Infrastructure
> **Relevant at:** Codixel (Lambda, EC2, ECS, S3, DynamoDB, SQS/SNS, CloudFront — resilient event-driven systems)
> **Related tech docs:** `case/cloud-service/cloud-platforms.md` (AWS services §45–88, ECS Fargate §45–55), `case/cloud-service/aws.md` (SDK §1–11, CDK §12–22), `case/structures-architecture/architecture-patterns.md` (Event-Driven §9–16, Serverless §25–32)

---

## 1. What This Means

Integrating cloud services means composing **managed AWS building blocks** (compute, storage, messaging, CDN) into a cohesive system — choosing the right service for each job and wiring them together to build **resilient, event-driven** platforms.

**Scope:**
- **Compute:** Lambda (serverless functions), EC2 (VMs), ECS (containers) — picking per workload
- **Storage:** S3 (objects/files), DynamoDB (NoSQL data) — durable, scalable persistence
- **Messaging:** SQS/SNS — decoupling and asynchronous communication
- **CDN:** CloudFront — global low-latency content delivery
- **Event-driven wiring:** S3 → Lambda, SQS → worker, DynamoDB Streams → triggers

**Why it matters:** the cloud isn't one product — it's a catalog. The engineering skill is knowing *which* service solves *which* problem, and *how to wire them together* so failures are isolated and the system scales automatically rather than collapsing under load.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The Codixel event-driven platform:**
```
                    [CloudFront] ── global content delivery
                         │
[API Gateway] ── [Lambda / ECS] ── [DynamoDB]  (data)
       │              │
       │              ▼
       │         [S3]  (webcast recordings, transcripts)
       │              │
       ▼              ▼
   [SQS] ◄──── [SNS] (event fan-out)
       │
       ▼
   [Worker (ECS/Lambda)] ── processes transcription/classification
```

**Service selection per workload:**
- **API layer** → API Gateway + Lambda (or ECS for long-running services)
- **Event ingestion** → SQS buffers spikes; SNS fans out to multiple consumers
- **Data storage** → DynamoDB for key-value event data; S3 for large media files
- **Content delivery** → CloudFront caches/serves static assets + recordings globally

**Resilience patterns in practice:**
- An S3 upload triggers Lambda automatically (event-driven, no polling)
- SQS absorbs traffic spikes — workers process at their own pace
- DynamoDB scales automatically — no capacity planning needed (on-demand)
- CloudFront absorbs read traffic — origin (S3/EC2) handles far less load

**The skill:** knowing that Lambda fits short event-driven functions, ECS fits long-running services, S3 fits large files, DynamoDB fits key-based data — and that the magic is in **how they connect**, not the individual services.

---

## 3. How to Implement

### Event-Driven Wiring (S3 → Lambda → SQS → Worker)

```python
# Trigger: S3 upload automatically invokes Lambda
def on_webcast_uploaded(event, context):
    """S3 → Lambda: process new webcast recordings automatically."""
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        # Enqueue transcription job — don't process inline
        sqs.send_message(
            QueueUrl=TRANSCRIBE_QUEUE,
            MessageBody=json.dumps({"event_id": extract_id(key), "s3_key": key}),
        )
    return {"status": "queued"}

# Worker (ECS service or Lambda): pulls from SQS
async def transcription_worker():
    while True:
        messages = sqs.receive_message(QueueUrl=TRANSCRIBE_QUEUE, MaxNumberOfMessages=10)
        for msg in messages["Messages"]:
            job = json.loads(msg["Body"])
            await process_transcription(job)        # heavy GPU work (ECS, not Lambda)
            sqs.delete_message(QueueUrl=TRANSCRIBE_QUEUE, ReceiptHandle=msg["ReceiptHandle"])
```

**Why:** S3 → Lambda is automatic (no polling); SQS decouples the trigger from the slow GPU work (Lambda has 15-min limit — GPU transcription needs ECS).

### Service Selection Decision Framework

```
COMPUTE:
  Short event-driven function (< 15 min)?  → Lambda
  Long-running service / heavy compute?    → ECS (Fargate: no servers)
  Full OS control?                         → EC2

STORAGE:
  Large files / media / backups?           → S3
  Key-value / document data?               → DynamoDB
  Relational data (ACID)?                  → RDS

MESSAGING:
  Buffer work / queue?                     → SQS
  Fan-out to many?                         → SNS
  Route by rules?                          → EventBridge

DELIVERY:
  Global low-latency content?              → CloudFront (in front of S3/ALB)
```

### Provisioning with CDK (Infrastructure as Code)

```python
# Define the whole stack in code — see case/cloud-service/aws.md §12-22
from aws_cdk import aws_s3 as s3, aws_lambda as _lambda, aws_sqs as sqs, aws_s3_notifications as s3n

bucket = s3.Bucket(self, "Recordings")
queue = sqs.Queue(self, "TranscribeQueue")
fn = _lambda.Function(self, "OnUpload",
    runtime=_lambda.Runtime.PYTHON_3_12,
    handler="index.on_webcast_uploaded",
    code=_lambda.Code.from_asset("lambda"),
)
# Wire: S3 upload → Lambda → SQS (all in code)
bucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3n.LambdaDestination(fn))
fn.add_environment("TRANSCRIBE_QUEUE", queue.queue_url)
queue.grant_send_messages(fn)
```

**Why:** the entire event-driven wiring is versioned, reviewable, and reproducible — no console clicking.

### Resilience Checklist

- [ ] **Compute matches workload** — Lambda for short events, ECS for long/heavy, EC2 for control
- [ ] **Storage matches data** — S3 for files, DynamoDB for key-value, RDS for relational
- [ ] **SQS/SNS decouple** stages — no synchronous chains that cascade failures
- [ ] **Event triggers wired** (S3→Lambda, DynamoDB Streams→Lambda) — no polling
- [ ] **CloudFront** in front of S3/origin for global delivery + read offloading
- [ ] **On-demand DynamoDB** for variable load (no capacity planning)
- [ ] **DLQs** on every queue — failures are captured, not lost
- [ ] **Provisioned as code** (CDK) — reproducible, reviewable infrastructure

### Avoid These

- **Using Lambda for long-running/heavy compute** — it has a 15-min timeout and limited resources
- **Polling instead of event triggers** — S3→Lambda is automatic; polling wastes resources
- **Synchronous service chains** — A calls B calls C; one failure cascades
- **Self-hosting what AWS manages** — running your own message queue on EC2 when SQS exists
- **Ignoring CloudFront** — serving large files directly from S3/EC2 when a CDN would halve latency
- **Console-clicked infrastructure** — snowflake setups that can't be reproduced or reviewed
