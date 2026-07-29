# Design Data Models

> **Category:** Database & Data Modeling
> **Relevant at:** Codixel (DynamoDB, MongoDB, Elasticsearch)
> **Related tech docs:** `case/database/databases.md` (PostgreSQL §1–11, DynamoDB §23–33, MongoDB §34–44), `case/search/search-engines.md` (Elasticsearch §1–11), `case/structures-architecture/backend-systems.md` (DSA §1–8)

---

## 1. What This Means

Designing data models means choosing how data is **structured, stored, and accessed** in non-relational systems (DynamoDB, MongoDB) and search engines (Elasticsearch) — optimizing for the specific query patterns and access requirements of the application.

**Scope:**
- **DynamoDB** — key-value/document models designed around **known access patterns** (single-table design, partition keys, GSIs)
- **MongoDB** — document models with **embed-vs-reference** decisions based on read patterns
- **Elasticsearch** — index mappings, analyzers, and field types for **full-text search and analytics**
- **Indexing strategy** — choosing the right indexes for query patterns, not "index everything"
- **Retrieval efficiency** — structuring data so reads are fast without expensive scans/joins

**Why it matters:** in NoSQL and search systems, the data model is the access pattern. Unlike relational DBs (where you normalize and query ad-hoc), you **must design the model around how you'll read the data**. Getting this wrong means slow queries, hot partitions, or complete redesigns.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**DynamoDB (Codixel — earnings-call platform):**
- **Access-pattern-first design** — know every query before creating the table
- Example: "get all events for a company" → partition key = `company_id`, sort key = `event_date`
- Example: "get event by ID" → separate GSI or single-table design with entity prefixes
- **Single-table design** for complex multi-entity access patterns (advanced, powerful, but hard to change later)
- **Avoid scans** — every query should use a partition key

**MongoDB (Codixel — flexible document data):**
- **Embed vs reference** — embed data read together (order + items), reference data shared across documents (customer)
- **Schema validation** — flexible doesn't mean schemaless; enforce structure on critical fields
- **Index the query fields** — `{ company_id: 1, created_at: -1 }` for "company's recent events"
- **Aggregation pipelines** for analytics instead of pulling data to the app

**Elasticsearch (Codixel — search + classification):**
- **Mappings define everything** — field types (text vs keyword), analyzers for tokenization
- `text` fields for full-text search (analyzed); `keyword` fields for exact match/filtering/aggregation (not analyzed)
- **Indexing the classified events** so they're searchable by content, category, company, date
- **Denormalization** — duplicate data into the search index to avoid joins (search engines don't join)

**The unifying principle:** all three reward **designing for the query, not the data shape**. The model follows the access pattern.

---

## 3. How to Implement

### DynamoDB — Access-Pattern-Driven Design

```python
# Step 1: List every access pattern BEFORE creating the table
ACCESS_PATTERNS = [
    "Get event by ID",
    "Get all events for a company (sorted by date)",
    "Get events by category (e.g., 'earnings') in a date range",
    "Get upcoming events (next 7 days)",
]

# Step 2: Design keys + indexes to serve those patterns
table = ddb.create_table(
    TableName="events",
    KeySchema=[
        {"AttributeName": "pk", "KeyType": "HASH"},   # partition
        {"AttributeName": "sk", "KeyType": "RANGE"},   # sort
    ],
    AttributeDefinitions=[
        {"AttributeName": "pk", "AttributeType": "S"},
        {"AttributeName": "sk", "AttributeType": "S"},
        {"AttributeName": "category", "AttributeType": "S"},   # for GSI
    ],
    GlobalSecondaryIndexes=[{
        "IndexName": "category-date-index",
        "KeySchema": [
            {"AttributeName": "category", "KeyType": "HASH"},
            {"AttributeName": "sk", "KeyType": "RANGE"},
        ],
    }],
    BillingMode="PAY_PER_REQUEST",
)

# Step 3: Single-table design — entity type embedded in keys
# pk: "COMPANY#amzn" | sk: "EVENT#2024-11-01"  → company's events sorted by date
# pk: "EVENT#xyz123" | sk: "META"              → event metadata
```

**Querying by access pattern:**
```python
# "Get all events for Amazon, sorted by date"
events = table.query(
    KeyConditionExpression="pk = :pk AND begins_with(sk, :sk)",
    ExpressionAttributeValues={":pk": "COMPANY#amzn", ":sk": "EVENT#"},
)
# "Get earnings events across all companies" (via GSI)
earnings = table.query(IndexName="category-date-index",
    KeyConditionExpression="category = :cat AND sk BETWEEN :start AND :end",
    ExpressionAttributeValues={":cat": "earnings", ":start": "2024-11", ":end": "2024-12"},
)
```

**Why:** every query uses a partition key — no scans, fast at any scale. Single-table design serves many access patterns from one table.

### MongoDB — Embed vs Reference

```python
# Decision: embed what you read together, reference what you don't

# EMBED: order document contains its items (read together)
order = {
    "_id": ObjectId("..."),
    "customer_id": ObjectId("..."),    # reference (shared, updated separately)
    "status": "paid",
    "items": [                          # embed (always read with the order)
        {"sku": "ABC", "qty": 2, "price": 25.00},
        {"sku": "DEF", "qty": 1, "price": 50.00},
    ],
    "total": 100.00,
    "created_at": datetime.utcnow(),
}

# Index for the query pattern: "customer's recent paid orders"
db.orders.create_index([("customer_id", 1), ("status", 1), ("created_at", -1)])

# Query uses the index
recent = db.orders.find({
    "customer_id": customer_id,
    "status": "paid",
}).sort("created_at", -1).limit(10)
```

### Elasticsearch — Mappings + Analyzers

```json
// Mapping: define field types deliberately (don't rely on dynamic mapping)
PUT /events
{
  "mappings": {
    "properties": {
      "title":        { "type": "text", "analyzer": "english" },   // full-text search
      "category":     { "type": "keyword" },                         // exact match + aggregation
      "company":      { "type": "keyword" },
      "event_date":   { "type": "date" },
      "transcript":   { "type": "text", "analyzer": "english" },
      "speakers":     { "type": "keyword" },
      "sentiment":    { "type": "keyword" }
    }
  }
}
```

**Why:** `text` (analyzed) for searching content; `keyword` (not analyzed) for filtering, sorting, and aggregation. Getting this wrong breaks search quality or aggregations.

**Querying — full-text + filter + aggregate:**
```json
POST /events/_search
{
  "query": {
    "bool": {
      "must":     { "match": { "transcript": "revenue growth guidance" } },
      "filter": [
        { "term":  { "category": "earnings" } },
        { "range": { "event_date": { "gte": "2024-01-01" } } }
      ]
    }
  },
  "aggs": { "by_company": { "terms": { "field": "company", "size": 10 } } }
}
```

### Data Modeling Checklist

- [ ] **Access patterns listed** before any table/index/collection is created
- [ ] **No scans** in DynamoDB — every query uses a partition key
- [ ] **Embed-vs-reference** decided per relationship in MongoDB
- [ ] **Mappings explicit** in Elasticsearch (not dynamic)
- [ ] **Indexes designed for queries** (composite indexes matching query + sort)
- [ ] **Denormalized for search** (Elasticsearch doesn't join — duplicate data in)
- [ ] **Schema validation** in MongoDB (flexible ≠ schemaless)
- [ ] **Pagination** designed from the start (cursor for DynamoDB/Mongo)

### Avoid These

- **Designing the model before knowing the queries** — the #1 NoSQL mistake
- **Scanning DynamoDB** — expensive and slow at scale; design keys instead
- **Unbounded embedded arrays in MongoDB** — documents cap at 16MB
- **Dynamic Elasticsearch mappings** — wrong field types break search/aggregation
- **Treating NoSQL like relational** — expecting joins and ad-hoc queries
- **Over-indexing** — indexes speed reads but slow writes; index only what you query
- **No pagination** — "get all" queries break as data grows
