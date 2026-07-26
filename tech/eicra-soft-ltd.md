# Eicra Soft Ltd — Technologies, Packages & Stacks

## Primary Languages

- **Node.js 20 LTS** — Long-term support version of Node.js used as the primary runtime for building scalable, event-driven backend microservices and RESTful APIs.
- **TypeScript 5.x** — Latest major version of TypeScript providing static type checking, interfaces, generics, and superior tooling for writing clean, testable, and well-structured production code.
- **Python** — Secondary backend language used for building APIs and services, particularly with the FastAPI framework.
- **FastAPI** — Modern, high-performance Python web framework for building APIs with automatic OpenAPI documentation, type hints, and async support.

## Database

- **PostgreSQL 15+** — Latest version of the advanced open-source relational database, used with multi-tenant schema isolation patterns for SaaS data architecture.

## Cloud & DevOps (AWS)

- **Docker** — Containerization platform for packaging applications and dependencies into lightweight, portable containers for consistent local and production environments.
- **AWS ECS Fargate** — Serverless container compute engine for running Docker containers in production without managing the underlying EC2 instances.
- **AWS EventBridge** — Serverless event bus service for building event-driven architectures by routing events between AWS services, SaaS apps, and custom applications.
- **AWS SQS** — Fully managed message queuing service for decoupling microservices, buffering workloads, and enabling asynchronous communication.
- **AWS SNS** — Fully managed pub/sub messaging service for sending notifications and fan-out messages to multiple subscribers.
- **AWS S3 (Amazon S3)** — Scalable object storage service for file storage, backups, static assets, and data lakes with high durability and availability.
- **AWS RDS** — Managed relational database service for running PostgreSQL in production with automated backups, patching, and scaling.
- **LocalStack** — Local AWS cloud stack emulator for developing and testing AWS services offline without connecting to the actual cloud.

## Caching & Search

- **Redis** — In-memory data structure store used as a caching layer, session store, and message broker for reducing database load and improving response times.
- **OpenSearch** — Open-source distributed search and analytics engine for powering full-text search, log analytics, and real-time data indexing across the SaaS platform.

## Architecture Patterns

- **RESTful APIs** — HTTP-based API design following REST constraints with versioned JSON endpoints for clean, predictable, and scalable client-server communication.
- **Versioned JSON APIs** — API versioning strategy ensuring backward compatibility and controlled evolution of API contracts through explicit version identifiers.
- **Microservices** — Architectural pattern structuring the application as a collection of loosely coupled, independently deployable services communicating over lightweight protocols.
- **Event-Driven Architectures** — Pattern where services communicate by producing and consuming events via AWS EventBridge, SQS, and SNS, enabling loose coupling and async processing.

## AI-Assisted Development

- **Claude Code** — Anthropic's AI-powered CLI coding assistant used daily to accelerate coding, refactoring, code review, and documentation tasks.
- **Cursor** — AI-first code editor deeply integrating large language models into the development workflow for code generation and refactoring.
- **GitHub Copilot** — AI-powered code completion and generation tool integrated with IDEs for accelerating development with context-aware suggestions.

## Integration & Domain

- **Multi-Tenant SaaS** — Software architecture pattern where a single application instance serves multiple tenants with isolated data schemas, custom configurations, and per-tenant feature sets.
- **B2B eCommerce** — Business-to-business electronic commerce systems involving bulk ordering, negotiated pricing, account hierarchies, and complex procurement workflows.
- **ERP Integrations** — Enterprise Resource Planning system integrations for syncing inventory, orders, financials, and customer data between the SaaS platform and external ERP systems.
- **Linear** — Modern project management and issue tracking tool used for asynchronous collaboration, sprint planning, and task management with the US-based team.
