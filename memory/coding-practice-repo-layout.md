# Coding-Practice Repo Layout

> Folder taxonomy of the `case/` documentation tree — where new topic docs go.

---

## Table of Contents

- [Category Folders](#category-folders)
- [Conventions](#conventions)
- [Pattern Selection](#pattern-selection)
- [Adding a New Doc](#adding-a-new-doc)

---

## Category Folders

| Folder | Holds | Status |
|---|---|---|
| `case/cloud-service/` | Cloud-platform docs | `aws.md` (SDK/CDK/CLI) + `cloud-platforms.md` (AWS services, GCP/Azure, LocalStack) |
| `case/framework/<name>/` | Framework-specific docs (one subfolder per framework) | `nextjs/` done; **FastAPI, Django, Spring Boot planned** |
| `case/state-management/` | Cross-framework state topic | `react-state-management.md` |
| `case/structures-architecture/` | Conceptual / architectural fundamentals | `backend-systems.md` |
| `case/api/` | API & communication topics (REST, GraphQL, WebSockets, SSE, formats, integrations) | `apis-and-communication.md` |
| `case/database/` | Database systems (PostgreSQL, MySQL, DynamoDB, MongoDB) + optimization | `databases.md` |
| `case/caching/` | In-memory caching stores (Redis, Memcached) + caching strategies | `caching.md` |
| `case/search/` | Search engines (Elasticsearch, OpenSearch, Solr) | `search-engines.md` |
| `case/messaging/` | Messaging discipline + brokers (RabbitMQ, GCP Pub/Sub, BullMQ); AWS messaging in cloud-service | `message-queues.md`; Kafka planned |
| `case/iac/` | IaC tools (AWS CDK, Terraform, CloudFormation, Pulumi) | `iac-tools.md` |

## Conventions

- **One combined doc per related batch** of topics (e.g., `aws.md` holds SDK+CDK+CLI; `backend-systems.md` holds 7 concepts). Related items sharing concepts → one file; unrelated → separate files.
- **Descriptive filenames** tied to content (`aws.md`, `backend-systems.md`, `react-state-management.md`, `app-router-and-rendering.md`).
- Framework docs live in `case/framework/<framework-lowercase>/`.

## Pattern Selection

| Content type | Pattern | Sections |
|---|---|---|
| **Tool / library** (install + code: SDK, CDK, CLI, React state libs) | Tool pattern (`cloud-service-doc-pattern.md`) | 11 (swap §4→Core API, §8→Common Patterns for non-AWS libs) |
| **Concept / architecture** (DSA, distributed systems, App Router, rendering) | Concept pattern (`concept-doc-pattern.md`) | 8 (no install/auth) |

## Adding a New Doc

1. **Identify the category** → folder (create it if missing).
2. **Pick the pattern** by content type (tool vs concept).
3. **Create a combined file** following the shared shell:
   - H1 + series blockquote
   - Hierarchical TOC (parent topic → nested numbered items)
   - Continuous section numbering
   - Shared Orientation hub
   - Shared Foundations appendix
   - Quick Reference Card
