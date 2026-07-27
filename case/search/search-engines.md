# Search & Analytics — Complete Guide

> **Series:** Search & Analytics Documentation — Part 1
> This file covers the **core search engines** (Elasticsearch, OpenSearch, Solr) — all built on Apache Lucene, all distributed, all for full-text search and analytics. More topics (vector/semantic search, relevance tuning, ELK/observability stacks) will be added as separate files later.

---

## Table of Contents

- [Shared Orientation — Choosing a Search Engine](#shared-orientation--choosing-a-search-engine)
- **Elasticsearch**
  - [1. What Is Elasticsearch?](#1-what-is-elasticsearch)
  - [2. Elasticsearch vs OpenSearch vs Solr](#2-elasticsearch-vs-opensearch-vs-solr)
  - [3. How Elasticsearch Works](#3-how-elasticsearch-works)
  - [4. Elasticsearch Data Model and Key Features](#4-elasticsearch-data-model-and-key-features)
  - [5. Where to Use Elasticsearch](#5-where-to-use-elasticsearch)
  - [6. Where NOT to Use Elasticsearch](#6-where-not-to-use-elasticsearch)
  - [7. Installing and Setting Up Elasticsearch](#7-installing-and-setting-up-elasticsearch)
  - [8. Elasticsearch Connection and Security](#8-elasticsearch-connection-and-security)
  - [9. Elasticsearch Production Best Practices](#9-elasticsearch-production-best-practices)
  - [10. Elasticsearch Real-World Examples](#10-elasticsearch-real-world-examples)
  - [11. Elasticsearch Pitfalls](#11-elasticsearch-pitfalls)
- **OpenSearch**
  - [12. What Is OpenSearch?](#12-what-is-opensearch)
  - [13. OpenSearch vs Elasticsearch](#13-opensearch-vs-elasticsearch)
  - [14. How OpenSearch Works](#14-how-opensearch-works)
  - [15. OpenSearch Data Model and Key Features](#15-opensearch-data-model-and-key-features)
  - [16. Where to Use OpenSearch](#16-where-to-use-opensearch)
  - [17. Where NOT to Use OpenSearch](#17-where-not-to-use-opensearch)
  - [18. Installing and Setting Up OpenSearch](#18-installing-and-setting-up-opensearch)
  - [19. OpenSearch Connection and Security](#19-opensearch-connection-and-security)
  - [20. OpenSearch Production Best Practices](#20-opensearch-production-best-practices)
  - [21. OpenSearch Real-World Examples](#21-opensearch-real-world-examples)
  - [22. OpenSearch Pitfalls](#22-opensearch-pitfalls)
- **Solr**
  - [23. What Is Apache Solr?](#23-what-is-apache-solr)
  - [24. Solr vs Elasticsearch and OpenSearch](#24-solr-vs-elasticsearch-and-opensearch)
  - [25. How Solr Works](#25-how-solr-works)
  - [26. Solr Data Model and Key Features](#26-solr-data-model-and-key-features)
  - [27. Where to Use Solr](#27-where-to-use-solr)
  - [28. Where NOT to Use Solr](#28-where-not-to-use-solr)
  - [29. Installing and Setting Up Solr](#29-installing-and-setting-up-solr)
  - [30. Solr Connection and Security](#30-solr-connection-and-security)
  - [31. Solr Production Best Practices](#31-solr-production-best-practices)
  - [32. Solr Real-World Examples](#32-solr-real-world-examples)
  - [33. Solr Pitfalls](#33-solr-pitfalls)
- [Shared Foundations](#shared-foundations)
- [Quick Reference Card](#quick-reference-card)

---

## Shared Orientation — Choosing a Search Engine

All three are **distributed search engines built on Apache Lucene** — same underlying technology, different ecosystems and licensing.

| Engine | Backed by | License | Sweet spot | One-liner |
|---|---|---|---|---|
| **Elasticsearch** | Elastic | Source-available (SSPL/Elastic) | Fullest ecosystem (Kibana, Beats, ML) | The leading search/analytics engine |
| **OpenSearch** | AWS + community | Apache 2.0 (fully open) | Fully-open or AWS-managed search | The open Elasticsearch fork |
| **Solr** | Apache | Apache 2.0 | Mature enterprise/faceted search | The veteran Lucene search server |

**Decision guide:**
- Want the richest ecosystem + managed Elastic Cloud? → **Elasticsearch**
- Want a fully-open license, or AWS-managed search? → **OpenSearch**
- Want mature, proven **faceted enterprise search**? → **Solr**

**The common thread:** all three are **search engines, not databases** — they excel at full-text search and analytics, but aren't ACID transactional stores. Use them *alongside* a primary database, not instead of one.

---

# Elasticsearch

## 1. What Is Elasticsearch?

**Elasticsearch** is a distributed, RESTful **search and analytics engine** built on Apache Lucene — used for full-text search, log analytics, and real-time indexing.

- The center of the **Elastic Stack (ELK)**: Elasticsearch + Logstash + Kibana + Beats.
- Near-real-time: indexed documents become searchable in ~1 second.

**One-liner:** the leading distributed search and analytics engine.

## 2. Elasticsearch vs OpenSearch vs Solr

| | Elasticsearch | OpenSearch | Solr |
|---|---|---|---|
| Ecosystem | Richest (Kibana, Beats, ML) | Growing, AWS-aligned | Mature, focused |
| License | Source-available (SSPL) | Apache 2.0 | Apache 2.0 |
| Best for | Full ELK stack, latest features | Open/AWS-managed | Faceted enterprise search |

**Rule of thumb:** Elasticsearch when you want the **fullest ecosystem and latest features**; OpenSearch for **openness/AWS**; Solr for **mature faceting**.

## 3. How Elasticsearch Works

- Documents (JSON) are **indexed** into Lucene **inverted indexes**.
- Indexes are split into **shards**, distributed and **replicated** across nodes.
- You interact via a **REST API** (index, search, aggregate).
- **Near-real-time** — a refresh makes new docs searchable in ~1s.

**Key point:** the inverted index (term → documents) is what makes full-text search fast — it's fundamentally different from a relational B-tree lookup.

## 4. Elasticsearch Data Model and Key Features

- **Documents** (JSON) stored in **indexes**.
- **Mappings** — define field types and how they're analyzed.
- **Analyzers** — tokenize/normalize text for search.
- **Shards & replicas** — distribution + high availability.
- **Aggregations** — analytics (metrics, buckets) over your data.
- **Relevance scoring** — ranks results by how well they match.

## 5. Where to Use Elasticsearch

- **Full-text search** (site/product/document search).
- **Log & observability analytics** (ELK stack).
- **Real-time indexing** of events/metrics.
- **Autocomplete**, **faceted search**, **relevance-ranked results**.

## 6. Where NOT to Use Elasticsearch

- **Primary transactional datastore** — not ACID, no joins, no strong relational integrity.
- **Small datasets** where a DB `LIKE`/full-text index suffices.
- Workloads needing **complex relational queries**.

## 7. Installing and Setting Up Elasticsearch

```bash
# Docker
docker run -p 9200:9200 -e "discovery.type=single-node" elasticsearch:8

# Index a document
curl -X POST localhost:9200/products/_doc -H 'Content-Type: application/json' -d'
{ "name": "Wireless Mouse", "price": 25 }'

# Search
curl localhost:9200/products/_search?q=name:wireless
```

## 8. Elasticsearch Connection and Security

- **REST endpoint** — `http://host:9200` (HTTPS in production).
- **API keys / basic auth** — secure access in production.
- **TLS** — encrypt node + client traffic.
- **Index-level access control** — restrict which users/roles see which indexes.

**Golden rule:** never run Elasticsearch unsecured on a public network.

## 9. Elasticsearch Production Best Practices

1. **Design mappings/analyzers deliberately** — don't rely on dynamic mapping for important fields.
2. **Size shards properly** — avoid too many tiny shards (oversharding hurts).
3. **Use index aliases** — enables reindexing without downtime.
4. **Avoid deep pagination** — use `search_after` or `scroll` for large result sets.
5. **Use ILM (Index Lifecycle Management)** — for time-series/log data (hot→warm→delete).
6. **Bulk-index** — batch indexing operations for throughput.
7. **Monitor cluster health** — shard allocation, heap, disk.

## 10. Elasticsearch Real-World Examples

### Example 1 — Full-Text Match
```json
GET /products/_search
{ "query": { "match": { "name": "wireless mouse" } } }
```
**Why:** analyzed full-text search with relevance ranking — far beyond SQL `LIKE`.

### Example 2 — Bool Query (filter + match)
```json
{ "query": { "bool": {
    "must":   { "match": { "name": "mouse" } },
    "filter": { "range": { "price": { "lte": 30 } } }
} } }
```
**Why:** combine relevance-ranked matching with exact filtering.

### Example 3 — Aggregation (analytics)
```json
{ "aggs": { "by_category": { "terms": { "field": "category" } } } }
```
**Why:** compute per-category counts/stats over millions of docs — fast analytics.

## 11. Elasticsearch Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Treating it as primary DB | Data integrity issues | Use alongside a real DB |
| Deep pagination | Slow, memory-heavy | `search_after` / scroll |
| Oversharding | Cluster strain | Right-size shard count |
| Leading-wildcard queries | Very slow | Use proper analyzers/ngrams |
| Relying on dynamic mapping | Wrong field types | Define mappings explicitly |

---

# OpenSearch

## 12. What Is OpenSearch?

**OpenSearch** is the **open-source fork of Elasticsearch** (created by AWS in 2021), providing distributed search, analytics, and observability under the permissive **Apache 2.0 license**.

- Forked from Elasticsearch 7.10, before Elastic changed its license.
- Available self-hosted or as a **managed AWS service**.

**One-liner:** the community-driven, AWS-backed, fully-open Elasticsearch.

## 13. OpenSearch vs Elasticsearch

| | OpenSearch | Elasticsearch |
|---|---|---|
| Origin | Fork of ES 7.10 | Original (Elastic) |
| License | Apache 2.0 (fully open) | Source-available (SSPL) |
| Security/alerting | Free, open plugins | Some features paid |
| Managed by | AWS (Amazon OpenSearch Service) | Elastic Cloud |

**Rule of thumb:** OpenSearch when you need a **fully-open license** or **AWS-managed** search; Elasticsearch for Elastic's **latest proprietary features**.

## 14. How OpenSearch Works

- **Same core as Elasticsearch** — Lucene inverted indexes, shards/replicas, REST API, near-real-time.
- Adds **open plugins** for security, alerting, anomaly detection, and observability.
- See [How Elasticsearch Works](#3-how-elasticsearch-works) — the architecture is shared.

**Key point:** if you know Elasticsearch, you know OpenSearch's core — the differences are licensing, governance, and the open plugin ecosystem.

## 15. OpenSearch Data Model and Key Features

- Same **document/index/mapping/analyzer** model as Elasticsearch.
- **Open security plugin** — free fine-grained access control.
- **Alerting & anomaly detection** — built-in, open.
- **Observability** — log/trace analytics dashboards.
- **SQL / PPL** — query with SQL-like syntax in addition to the DSL.

## 16. Where to Use OpenSearch

- **Full-text search** and **log analytics/observability**.
- When **license openness** matters (no SSPL restrictions).
- **AWS-managed search** (Amazon OpenSearch Service).

## 17. Where NOT to Use OpenSearch

- Need **Elastic's latest proprietary-only features** (some ML/advanced capabilities).
- **Primary transactional datastore** (same as Elasticsearch).

## 18. Installing and Setting Up OpenSearch

```bash
# Docker
docker run -p 9200:9200 -e "discovery.type=single-node" opensearchproject/opensearch:2

# Index + search (same REST API shape as Elasticsearch)
curl -X POST localhost:9200/logs/_doc -H 'Content-Type: application/json' -d'
{ "level": "error", "msg": "timeout" }'
```

## 19. OpenSearch Connection and Security

- **REST endpoint** — `https://host:9200`.
- **Built-in open security plugin** — auth, TLS, role-based access (free, unlike legacy X-Pack).
- **Fine-grained access control** — index/document/field level.

## 20. OpenSearch Production Best Practices

1. Apply the **same Elasticsearch practices** — mappings, shard sizing, ILM, bulk indexing, avoid deep pagination.
2. **Use the open security plugin** — don't run unsecured.
3. **Leverage built-in alerting/observability** — no extra cost.
4. **Monitor cluster health** continuously.

## 21. OpenSearch Real-World Examples

### Example 1 — Index + Search
**Why:** identical workflow to Elasticsearch — migrate with minimal changes.

### Example 2 — Observability Log Analytics
**Why:** built-in dashboards + alerting for logs/traces without licensing fees — a full open observability stack.

## 22. OpenSearch Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Assuming 100% ES feature parity | Missing newer ES features | Check feature availability |
| Deep pagination | Slow | `search_after` |
| Wrong shard sizing | Cluster strain | Size shards properly |
| Treating as primary DB | Integrity issues | Use alongside a real DB |

---

# Solr

## 23. What Is Apache Solr?

**Solr** is an **open-source enterprise search platform** built on Apache Lucene, known for **full-text and faceted search**.

- One of the oldest, most mature Lucene-based search servers.
- Strong in **faceted navigation** and **enterprise document search**.

**One-liner:** the veteran Lucene-based enterprise search server.

## 24. Solr vs Elasticsearch and OpenSearch

| | Solr | Elasticsearch / OpenSearch |
|---|---|---|
| Maturity | Oldest, very stable | Newer |
| Faceting | Excellent | Good |
| Log/observability | Weaker ecosystem | Strong (ELK/OpenSearch) |
| Real-time analytics | Less suited | Better suited |

**Rule of thumb:** Solr for **mature faceted enterprise/e-commerce search**; Elasticsearch/OpenSearch for **logs, real-time analytics, and modern ecosystems**.

## 25. How Solr Works

- Lucene-based; documents are indexed into **cores/collections**.
- **SolrCloud** distributes indexes across nodes, coordinated by **ZooKeeper**.
- Query via a **REST API** (rich query parsers, faceting).
- Strong **faceting** — compute category/filter counts alongside results.

**Key point:** Solr's **faceting** and mature query features make it a long-time favorite for e-commerce and enterprise search.

## 26. Solr Data Model and Key Features

- **Documents** in cores/collections.
- **Faceting** — category counts for navigation/filtering.
- **Rich query parsers** — flexible query building.
- **Spellcheck, highlighting, more-like-this**.
- **SolrCloud** — distributed mode with ZooKeeper.

## 27. Where to Use Solr

- **Enterprise search** and **document search**.
- **E-commerce product search** (faceted navigation).
- When you want a **mature, proven** search server.

## 28. Where NOT to Use Solr

- **Log analytics/observability** — Elasticsearch/OpenSearch ecosystems are stronger.
- **Real-time streaming analytics**.
- As a **primary database**.

## 29. Installing and Setting Up Solr

```bash
# Docker
docker run -p 8983:8983 solr:9

# Create a core, index a document, search
docker exec -it <container> solr create_core -c products
curl 'localhost:8983/solr/products/update/json/docs' -H 'Content-Type: application/json' -d'
{ "id": "1", "name": "Wireless Mouse", "category": "electronics" }'
curl 'localhost:8983/solr/products/select?q=name:wireless'
```

## 30. Solr Connection and Security

- **HTTP API** — `http://host:8983/solr`.
- **SolrCloud + ZooKeeper** — coordination for distributed mode.
- **Basic auth / Kerberos** — secure in production.
- Keep Solr behind your private network.

## 31. Solr Production Best Practices

1. **Design the schema** deliberately — field types drive search behavior.
2. **Use faceting** for navigation/filtering UI.
3. **Tune relevance** — Solr's strength is configurable ranking.
4. **Size SolrCloud properly** — shards/replicas for scale + HA.
5. **Monitor** — ZooKeeper health, query latency, index size.

## 32. Solr Real-World Examples

### Example 1 — Faceted Product Search
```
q=mouse & facet=true & facet.field=category & facet.field=brand
```
**Why:** returns matching products **plus** category/brand counts for filter navigation — classic e-commerce search.

### Example 2 — Full-Text Search with Highlighting
**Why:** show users **why** a document matched (highlighted snippets) — great for document search UX.

## 33. Solr Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Treating as primary DB | Integrity issues | Use alongside a real DB |
| ZooKeeper complexity | Ops overhead | Manage/plan SolrCloud carefully |
| Deep pagination | Slow | Cursor-based paging |
| Ignoring relevance tuning | Poor result quality | Tune field boosts/analyzers |

---

## Shared Foundations

Concepts that recur across **all three search engines**:

- **Inverted index** — the core of search: a map from term → documents. This is what makes full-text search fast (vs a relational B-tree scan). All three are Lucene-based, so this is shared.
- **Search engine ≠ database** — none are ACID transactional stores; no joins, eventual consistency. Use them **alongside** a primary DB, syncing data in.
- **Distributed by design** — sharding (split data) + replication (copies for HA) across nodes. Right-sizing shards is a universal concern.
- **Mappings/analyzers/schema** — how text is tokenized and indexed determines search quality. Design it deliberately; don't rely on defaults.
- **Relevance scoring** — results are ranked by match quality, not just filtered. Tuning relevance is a search-specific discipline.
- **Avoid deep pagination** — all three degrade on large offsets; use cursor/scroll/`search_after`.

## Quick Reference Card

```
SEARCH ENGINE PICKER:
  Richest ecosystem (Kibana/Beats/ML), latest features? → Elasticsearch
  Fully-open license, or AWS-managed?                    → OpenSearch
  Mature faceted enterprise/e-commerce search?           → Solr

ALL THREE: Lucene-based, distributed (shards+replicas), REST API, near-real-time

KEY MENTAL MODEL:
  Inverted index (term → docs) = fast full-text search
  Search engine ≠ database (not ACID, no joins) → use alongside a primary DB

GOLDEN RULES:
  ✓ Design mappings/analyzers/schema deliberately
  ✓ Size shards properly (avoid oversharding)
  ✓ Avoid deep pagination (cursor/scroll/search_after)
  ✓ Bulk-index for throughput
  ✓ ILM for time-series/log data (ES/OpenSearch)
  ✓ Never run unsecured on a public network
```

---

*This file covers the core Lucene-based search engines. More topics (vector/semantic search, relevance tuning, ELK/observability stacks) will be added as separate files in this series over time.*
