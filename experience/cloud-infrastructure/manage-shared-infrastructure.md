# Manage Shared Infrastructure

> **Category:** Cloud & Infrastructure
> **Relevant at:** Eicra Soft (Redis caching, OpenSearch, S3 storage, API gateways)
> **Related tech docs:** `case/caching/caching.md` (Redis §1–11, Caching Strategies §23–33), `case/search/search-engines.md` (OpenSearch §12–22), `case/cloud-service/cloud-platforms.md` (S3 §67–77, API Gateway), `case/iac/iac-tools.md` (CDK §1–11)

---

## 1. What This Means

Managing shared infrastructure means operating the **cross-cutting platform services** that the whole application depends on — caching (Redis), search (OpenSearch), file storage (S3), and API gateways — ensuring they're **reliable, performant, and shared efficiently** across services.

**Scope:**
- **Redis** — caching layer, session store, rate limiting (see `case/caching/caching.md`)
- **OpenSearch** — search and analytics engine for the SaaS platform
- **S3** — shared object/file storage
- **API Gateway** — single entry point routing, auth, and rate limiting for backend services
- **Reliability + performance** — these are shared resources, so mismanagement affects every service

**Why it matters:** shared infrastructure is the foundation everyone builds on. If Redis is misconfigured, every cached read slows down. If OpenSearch is down, search breaks across the whole platform. Managing these well is managing the *reliability of the entire product*.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The shared-infrastructure topology:**
```
                    [API Gateway]
                    (routing, auth, rate limit)
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   [Microservice A]  [Microservice B]  [Microservice C]
        │                │                │
        └────────┬───────┴────────┬───────┘
                 ▼                ▼
             [Redis]          [OpenSearch]      ← shared infrastructure
           (cache, sessions)  (search/analytics)
                 │
                 ▼
              [S3] (shared file storage)
```

**What "managing" means in practice:**
- **Redis:** set memory limits + eviction policies, monitor hit rate, ensure no key grows unbounded
- **OpenSearch:** design mappings/analyzers, size shards properly, monitor cluster health
- **S3:** configure lifecycle rules (move old data to cheaper tiers), keep buckets private, use presigned URLs
- **API Gateway:** route to services, enforce auth/rate-limiting, handle CORS

**The shared-resource challenge:**
- A single misbehaving microservice can overwhelm Redis (memory exhaustion) or OpenSearch (heavy queries)
- Caching invalidation must be coordinated — stale data served to all services is worse than no cache
- API Gateway is a single point of routing — its config affects every consumer

---

## 3. How to Implement

### Redis — Managed as a Shared Cache

```python
# Centralized cache client — all services use the same patterns
class SharedCache:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url, max_connections=50)

    async def get_or_set(self, key: str, loader, ttl: int = 300):
        """Cache-aside pattern — DB hit only on miss."""
        cached = await self.redis.get(key)
        if cached:
            return json.loads(cached)
        value = await loader()           # expensive DB/API call
        await self.redis.setex(key, ttl, json.dumps(value))
        return value
```

**Redis production config:**
```conf
maxmemory 4gb
maxmemory-policy allkeys-lru     # evict least-recently-used when full
timeout 300                      # drop idle connections
```

### OpenSearch — Managed Search Cluster

```python
# Shared search index — all services index/query through one client
class SearchService:
    def __init__(self, endpoint: str):
        self.client = OpenSearch(hosts=[endpoint])

    async def index_document(self, index: str, doc_id: str, body: dict):
        """All services index through this — consistent mappings."""
        self.client.index(index=index, id=doc_id, body=body)

    async def search(self, index: str, query: dict, filters: dict):
        """Tenant-scoped search — see multi-tenant-schemas.md."""
        return self.client.search(index=index, body={
            "query": {"bool": {"must": {"match": query}, "filter": filters}}
        })
```

### API Gateway — Centralized Routing + Auth

```yaml
# API Gateway config (via CDK/OpenAPI)
# Single entry point for all microservices
paths:
  /api/v1/orders:
    x-amazon-apigateway-integration:
      uri: arn:aws:apigateway:...:orders-service  # routes to Orders MS
  /api/v1/search:
    x-amazon-apigateway-integration:
      uri: arn:aws:apigateway:...:search-service  # routes to OpenSearch proxy
# Shared concerns applied here:
#   - Auth (JWT verification)
#   - Rate limiting (per client/key)
#   - CORS
#   - Request/response logging
```

### S3 — Shared Storage with Lifecycle

```bash
# Lifecycle rule: move old recordings to cheaper storage, expire temp files
aws s3api put-bucket-lifecycle-configuration --bucket recordings --lifecycle-configuration '{
  "Rules": [
    {"ID": "archive-old", "Status": "Enabled",
     "Filter": {"Prefix": "recordings/"},
     "Transitions": [{"Days": 30, "StorageClass": "STANDARD_IA"},
                     {"Days": 90, "StorageClass": "GLACIER"}]},
    {"ID": "expire-temp", "Status": "Enabled",
     "Filter": {"Prefix": "temp/"}, "Expiration": {"Days": 7}}
  ]
}'
```

### Shared Infrastructure Checklist

- [ ] **Redis:** memory limit + eviction policy set; hit rate monitored; TTLs on all keys
- [ ] **OpenSearch:** mappings explicit; shards sized properly; cluster health monitored
- [ ] **S3:** buckets private; lifecycle rules for cost; presigned URLs for client uploads
- [ ] **API Gateway:** routing, auth, rate limiting, CORS centralized
- [ ] **Centralized clients** — all services use shared cache/search clients (consistent patterns)
- [ ] **Monitoring** on every shared resource — memory, hit rate, cluster health, latency
- [ ] **Alerting** before exhaustion — Redis memory, OpenSearch disk, S3 cost anomalies
- [ ] **Provisioned as code** (CDK) — reproducible infrastructure
- [ ] **Noisy-neighbor protection** — one service can't overwhelm shared resources

### Avoid These

- **Redis with no memory limit** — grows until OOM crashes the cache
- **OpenSearch dynamic mappings** — wrong field types break search/aggregation
- **Public S3 buckets** — accidental data exposure
- **Each service managing its own Redis/OpenSearch** — duplicate infra, inconsistent patterns
- **No lifecycle rules on S3** — storage costs grow unbounded
- **No monitoring on shared resources** — a silent OpenSearch failure breaks search platform-wide
- **One service overwhelming shared resources** — no rate limiting or quotas between services
