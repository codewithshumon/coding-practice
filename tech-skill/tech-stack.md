# Merged Technologies, Packages & Stacks

> Consolidated from: **Codixel**, **Impressive Security Limited**, **Eicra Soft Ltd**, **As-Sunnah Foundation**, and **MVI Solutions**. Items used at multiple companies are merged into single entries with sources noted in parentheses.

---

## Core Languages

- **Python** — Primary/secondary backend language across roles: production backend development, data pipelines, and AI/LLM integrations at Codixel (Python 3.12); APIs with FastAPI at Eicra Soft; web applications, scripting, and system integration with Django at MVI Solutions. (Codixel, Eicra Soft, MVI Solutions)
- **TypeScript** — Strongly typed JavaScript superset for static type checking, interfaces, and generics: cloud infrastructure as code (AWS CDK) at Codixel; large-scale NestJS backends at Impressive Security; production microservices at Eicra Soft (5.x); safer React/Next.js code at As-Sunnah Foundation. (All except MVI Solutions)
- **JavaScript (ES6+)** — Core scripting language: Node.js server-side logic at Impressive Security; modern web features (arrow functions, destructuring, modules, async/await) at As-Sunnah Foundation; DOM manipulation and interactivity in Django templates at MVI Solutions. (Impressive Security, As-Sunnah, MVI Solutions)
- **Java** — Statically typed, JVM-based language powering the API server layer with high performance and mature ecosystem. (Codixel)
- **Node.js** — Asynchronous, event-driven JavaScript runtime on Chrome's V8 engine for scalable, high-throughput network applications; Node.js 20 LTS as primary runtime for backend microservices and RESTful APIs. (Impressive Security, Eicra Soft)
- **SQL** — Structured Query Language for schema design, optimized queries, and relational data management. (MVI Solutions)

## Core Concepts & Skills

- **Data Structures & Algorithms** — Deep understanding of efficient data structures (trees, graphs, hashes, queues) and algorithmic patterns (sorting, searching, DP) for performant, scalable code. (Codixel)
- **Backend Architecture** — Layered architecture patterns, separation of concerns, and maintainable server-side system design. (Codixel)
- **Distributed Systems** — Consensus, replication, partitioning, fault tolerance, CAP theorem, and eventual consistency. (Codixel)
- **Scalable APIs** — APIs handling high throughput with proper pagination, rate limiting, caching, and horizontal scaling strategies. (Codixel)
- **Software Architecture** — Clean architecture, hexagonal architecture, DDD, and event-driven design for robust, scalable, maintainable backends. (Impressive Security)
- **Performance Tuning** — Profiling and optimizing Python code, Django ORM queries, template rendering, caching strategies, and server configuration. (MVI Solutions)
- **System Optimization** — End-to-end optimization of architecture, database queries, caching layers, API response times, and resource utilization. (MVI Solutions)

## Frameworks

### Backend

- **NestJS** — Progressive, opinionated Node.js framework with modular architecture, decorators, dependency injection, and first-class TypeScript support. (Impressive Security)
- **FastAPI** — Modern, high-performance Python web framework with automatic OpenAPI documentation, type hints, and async support. (Eicra Soft)
- **Django** — High-level Python web framework with built-in ORM, admin panel, authentication, and security features. (MVI Solutions)
- **Django ORM** — Object-Relational Mapping layer for database interaction via Python objects, supporting migrations, relationships, and query optimization. (MVI Solutions)
- **Django REST Framework** — Toolkit for building RESTful APIs on Django: serializers, viewsets, authentication classes, and browsable API interface. (MVI Solutions)

### Frontend

- **React 19+** — Component-based, declarative UI library with the latest features and concurrent rendering. (As-Sunnah Foundation)
- **Next.js 15+** — React meta-framework with App Router, file-based routing, SSR, static generation, and full-stack capabilities. (As-Sunnah Foundation)
- **jQuery** — Fast, feature-rich JavaScript library simplifying DOM traversal, event handling, animation, and AJAX calls. (MVI Solutions)
- **AJAX** — Asynchronous technique for server communication without full page reloads. (MVI Solutions)

## Web Standards & Styling

- **HTML5** — Semantic elements, native form validation, multimedia APIs, and improved document structure. (As-Sunnah Foundation, MVI Solutions)
- **CSS3** — Flexbox, grid, animations, custom properties, media queries, and advanced selectors. (As-Sunnah Foundation, MVI Solutions)
- **Tailwind CSS** — Utility-first CSS framework composing designs in markup for rapid, consistent UI development. (As-Sunnah Foundation)
- **Material UI (MUI)** — React component library implementing Google's Material Design with pre-built, customizable components. (As-Sunnah Foundation)
- **CSS Modules** — Locally scoped CSS class names per component/file, eliminating global namespace collisions. (As-Sunnah Foundation)
- **Sass/SCSS** — CSS preprocessor with variables, nesting, mixins, functions, and inheritance. (As-Sunnah Foundation)
- **Styled Components** — CSS-in-JS library for co-located, dynamic component styles. (As-Sunnah Foundation)
- **Emotion** — High-performance CSS-in-JS library with styled-component API and css-prop approach. (As-Sunnah Foundation)
- **shadcn/ui** — Component collection integrated by copying source into the project for full implementation control. (As-Sunnah Foundation)

## State Management & Data Fetching

- **Redux Toolkit** — Official opinionated Redux toolset with simplified store setup and immutable update patterns. (As-Sunnah Foundation)
- **Zustand** — Lightweight, hook-based state management with no boilerplate or provider wrapping. (As-Sunnah Foundation)
- **TanStack Query** — Data-fetching and server-state library with caching, background refetching, pagination, and mutations (formerly React Query). (As-Sunnah Foundation)
- **Context API** — React's built-in mechanism for passing data through the component tree without prop drilling. (As-Sunnah Foundation)

## Next.js Architecture & Rendering

- **Next.js App Router** — File-system routing using `app/` directory with layouts, loading states, error boundaries, and nested routing. (As-Sunnah Foundation)
- **React Server Components** — Server-exclusive rendering shipping zero client-side JavaScript. (As-Sunnah Foundation)
- **Client Components** — Interactive browser-rendered components with event handlers, hooks, state, and effects. (As-Sunnah Foundation)
- **Server Actions** — Server-side async functions callable from Client Components for form submissions and mutations. (As-Sunnah Foundation)
- **Route Handlers** — Custom request handlers in the App Router (`route.ts`) supporting Web-standard Request/Response. (As-Sunnah Foundation)
- **Middleware** — Pre-request code for rewriting, redirects, header modification, and auth checks at the edge. (As-Sunnah Foundation)
- **React Router** — Client-side declarative routing with dynamic segments. (As-Sunnah Foundation)
- **SSR (Server-Side Rendering)** — Server-rendered HTML per request for better initial load and SEO. (As-Sunnah Foundation)
- **SSG (Static Site Generation)** — Build-time pre-rendered static HTML served from CDN. (As-Sunnah Foundation)
- **ISR (Incremental Static Regeneration)** — Per-page background regeneration of static content after build. (As-Sunnah Foundation)
- **Streaming** — Progressive HTML chunk delivery for faster Time-to-First-Byte. (As-Sunnah Foundation)
- **PPR (Partial Prerendering)** — Experimental combination of static shell prerendering with streamed dynamic content. (As-Sunnah Foundation)

## Architecture Patterns

- **Microservices** — Loosely coupled, independently deployable services communicating over lightweight protocols. (Impressive Security, Eicra Soft)
- **Event-Driven Architectures** — Services communicating via events through AWS EventBridge, SQS, and SNS for loose coupling and async processing. (Eicra Soft)
- **Multi-Tenant SaaS** — Single application instance serving multiple tenants with isolated data schemas, custom configurations, and per-tenant features. (Eicra Soft)
- **Serverless Architectures** — Event-driven, pay-per-use compute via AWS Lambda or Cloud Functions without managing servers. (Codixel)

## APIs & Communication

- **RESTful APIs** — REST principles with proper status codes, versioning, pagination, filtering, and resource-oriented design; versioned JSON endpoints for backward compatibility. (Codixel, Impressive Security, Eicra Soft, As-Sunnah Foundation, MVI Solutions)
- **GraphQL APIs** — Typed query language letting clients request exactly the data they need, reducing over/under-fetching. (As-Sunnah Foundation)
- **WebSockets** — Full-duplex persistent communication over a single TCP connection for real-time bidirectional data flow. (As-Sunnah Foundation)
- **Server-Sent Events (SSE)** — Server-push real-time updates over HTTP for notifications and live feeds. (As-Sunnah Foundation)
- **JSON APIs** — Lightweight data interchange format for API request/response payloads. (MVI Solutions)
- **XML APIs** — XML-based API format for integrating legacy systems (payments, CRMs, shipping providers). (MVI Solutions)
- **Third-Party Integrations** — External vendors, payment gateways, travel suppliers, and partner services via APIs and webhooks. (Impressive Security)

## Databases

- **PostgreSQL** — Advanced open-source relational database with ACID compliance, complex queries, JSONB support, and extensibility; PostgreSQL 15+ with multi-tenant schema isolation for SaaS. (Impressive Security, Eicra Soft)
- **MySQL** — Widely adopted relational database with strong read performance, replication, and mature ecosystem. (Impressive Security)
- **DynamoDB** — Fully managed serverless NoSQL key-value/document database by AWS with single-digit millisecond latency. (Codixel)
- **MongoDB** — Document-oriented NoSQL database using BSON for flexible schemas and horizontal scaling. (Codixel)
- **Database Optimization** — Query tuning, indexing strategies, connection pooling, read replicas, and schema denormalization. (Impressive Security)

## Caching

- **Redis** — In-memory data store used as database cache, session store, message broker, task queue, and distributed lock manager. (Impressive Security, Eicra Soft, MVI Solutions)
- **Memcached** — High-performance distributed memory object caching for speeding up dynamic web applications. (MVI Solutions)
- **Caching (strategies)** — Multi-level caching (in-memory, Redis, CDN-edge) to reduce database load and improve throughput. (Impressive Security)

## Search & Analytics

- **Elasticsearch** — Distributed RESTful search/analytics engine on Apache Lucene for full-text search, log analytics, and real-time indexing. (Codixel)
- **OpenSearch** — Open-source Elasticsearch fork for distributed search, analytics, and observability. (Codixel, Eicra Soft)
- **Solr** — Open-source enterprise search platform on Apache Lucene with full-text and faceted search. (Codixel)

## Cloud Platforms

- **AWS** — Primary cloud platform across roles. Services used: Lambda, DynamoDB, SQS/SNS, S3, CloudFront, API Gateway, EC2, ECS, RDS, ElastiCache, EventBridge, ECS Fargate. (Codixel, Impressive Security, Eicra Soft)
- **AWS ECS Fargate** — Serverless container compute running Docker containers without managing EC2 instances. (Eicra Soft)
- **AWS EventBridge** — Serverless event bus routing events between AWS services, SaaS apps, and custom applications. (Eicra Soft)
- **AWS SQS** — Fully managed message queuing for decoupling microservices and buffering workloads. (Codixel, Eicra Soft)
- **AWS SNS** — Fully managed pub/sub messaging for notifications and fan-out. (Codixel, Eicra Soft)
- **AWS S3** — Scalable object storage for files, backups, static assets, and data lakes. (Codixel, Eicra Soft)
- **AWS RDS** — Managed relational database service with automated backups, patching, and scaling. (Eicra Soft)
- **GCP** — Google Cloud Platform for compute, storage, and Pub/Sub messaging. (Codixel)
- **Azure** — Microsoft's cloud platform for managed services and infrastructure. (Codixel)
- **Cloud Platforms (general)** — Hosting, scaling, and managing applications on AWS, Google Cloud, Azure, or Vercel. (Impressive Security, As-Sunnah Foundation, MVI Solutions)
- **LocalStack** — Local AWS cloud stack emulator for offline development and testing. (Eicra Soft)

## Messaging & Queues

- **Message Queues & Pub/Sub** — Asynchronous messaging (AWS SQS, GCP Pub/Sub, Bull, RabbitMQ) for decoupling services, background jobs, and workload spikes. (Codixel, Impressive Security)

## Infrastructure as Code (IaC)

- **AWS CDK** — IaC framework using TypeScript to define and provision AWS resources with constructs and stacks. (Codixel)
- **Terraform** — HashiCorp's declarative HCL tool for multi-cloud infrastructure provisioning. (Codixel)
- **CloudFormation** — AWS-native IaC using JSON/YAML templates. (Codixel)
- **Pulumi** — Modern IaC using general-purpose languages (Python, TypeScript, Go). (Codixel)

## AI & LLM

- **OpenAI** — GPT models for text generation, classification, extraction, summarization, and conversational AI. (Codixel)
- **Anthropic Claude** — AI model for safe, steerable, high-quality text generation and analysis. (Codixel)
- **Google Gemini** — Google's multimodal AI model for advanced reasoning and multi-format processing. (Codixel)
- **LLM Integrations** — Integrating LLMs into pipelines for classification, entity extraction, sentiment analysis, and conversational interfaces. (Codixel)
- **Prompt Engineering** — Designing, iterating, and optimizing prompts for reliable production LLM outputs. (Codixel)

## AI-Assisted Development Tools

- **Claude Code** — Anthropic's AI-powered CLI assistant for codebase exploration, editing, debugging, refactoring, and documentation. (Codixel, Eicra Soft, As-Sunnah Foundation)
- **Cursor** — AI-first code editor deeply integrating LLMs into the development workflow. (Codixel, Eicra Soft, As-Sunnah Foundation)
- **GitHub Copilot** — AI-powered code completion and generation integrated with IDEs. (Codixel, Eicra Soft, As-Sunnah Foundation)
- **ChatGPT** — OpenAI's conversational AI for code generation, debugging, and concept explanation. (As-Sunnah Foundation)

## Media Processing

- **WhisperX** — GPU-accelerated speech-to-text built on OpenAI's Whisper with word-level timestamps and speaker diarization. (Codixel)
- **Playwright** — Browser automation for Chromium, Firefox, and WebKit to record and interact with live webcasts. (Codixel)
- **FFmpeg** — Cross-platform solution for recording, converting, and streaming audio/video in media pipelines. (Codixel)

## Security & Authentication

- **API Security** — Rate limiting, input validation, CORS, OWASP mitigations, API key management, OAuth 2.0, JWT, and request signing. (Impressive Security)
- **OAuth** — Open standard for access delegation without exposing credentials. (As-Sunnah Foundation)
- **JWT (JSON Web Tokens)** — Compact, URL-safe token format for stateless authentication and authorization. (As-Sunnah Foundation)

## Performance & Quality

- **Core Web Vitals** — Google's user-centric metrics (LCP, INP, CLS) for loading, interactivity, and visual stability. (As-Sunnah Foundation)
- **WCAG** — International accessibility standards covering perceivable, operable, understandable, and robust principles. (As-Sunnah Foundation)
- **SEO** — Technical, on-page, and content optimizations for search visibility and ranking. (As-Sunnah Foundation)

## DevOps & CI/CD

- **Git** — Distributed version control for source management, branching strategies, and collaborative workflows. (All five companies)
- **Docker** — Containerization platform packaging applications and dependencies into portable containers. (Codixel, Impressive Security, Eicra Soft, As-Sunnah Foundation)
- **CI/CD Pipelines** — Automated build, test, and deployment workflows for reliable, repeatable, zero-downtime releases. (Codixel, Impressive Security, As-Sunnah Foundation, MVI Solutions)
- **GitHub Actions** — GitHub's built-in CI/CD for automating workflows directly from the repository. (Codixel)
- **AWS CodePipeline** — Managed continuous delivery service automating build, test, and deploy stages. (Codixel)
- **Automated Deployments** — End-to-end automated release workflows ensuring zero-downtime production deployments. (Codixel)
- **Linux** — Server OS proficiency: shell scripting, process management, system administration. (Impressive Security)

## Domain-Specific

### Travel (Impressive Security Limited)

- **Airline APIs** — Flight search, booking, ticketing, check-in, status, and ancillary services.
- **OTA (Online Travel Agency) APIs** — Aggregator APIs for flights, hotels, car rentals, and ancillaries.
- **GDS (Global Distribution System)** — Travel distribution networks (Amadeus, Sabre, Travelport) for real-time inventory, pricing, and booking.
- **NDC (New Distribution Capability)** — IATA's XML-based standard for airlines to distribute rich content and personalized offers.
- **Hotel APIs** — Hotel search, availability, rate plans, and booking management.
- **Travel APIs** — Ground transportation, activities, insurance, and other travel services.

### SaaS & eCommerce (Eicra Soft Ltd)

- **B2B eCommerce** — Bulk ordering, negotiated pricing, account hierarchies, and complex procurement workflows.
- **ERP Integrations** — Syncing inventory, orders, financials, and customer data with external ERP systems.

## Collaboration & Project Management

- **Linear** — Project management and issue tracking for asynchronous collaboration and sprint planning. (Eicra Soft)

---

## Cross-Company Technology Matrix

| Technology | Codixel | Impressive Security | Eicra Soft | As-Sunnah | MVI Solutions |
|---|---|---|---|---|---|
| Python | ✅ (3.12) | — | ✅ | — | ✅ |
| TypeScript | ✅ (IaC) | ✅ | ✅ (5.x) | ✅ | — |
| JavaScript | — | ✅ | — | ✅ (ES6+) | ✅ |
| Node.js | — | ✅ | ✅ (20 LTS) | — | — |
| Java | ✅ | — | — | — | — |
| React / Next.js | — | — | — | ✅ (19+ / 15+) | — |
| Django / DRF | — | — | — | — | ✅ |
| NestJS | — | ✅ | — | — | — |
| FastAPI | — | — | ✅ | — | — |
| PostgreSQL | — | ✅ | ✅ (15+) | — | — |
| MySQL | — | ✅ | — | — | — |
| Redis | — | ✅ | ✅ | — | ✅ |
| Elasticsearch/OpenSearch | ✅ | — | ✅ | — | — |
| AWS | ✅ | ✅ | ✅ | — | — |
| GCP / Azure | ✅ | — | — | — | — |
| Docker | ✅ | ✅ | ✅ | ✅ | — |
| Git | ✅ | ✅ | ✅ | ✅ | ✅ |
| CI/CD | ✅ | ✅ | — | ✅ | ✅ |
| AI/LLM Integrations | ✅ | — | — | — | — |
| AI-Assisted Dev Tools | ✅ | — | ✅ | ✅ | — |
| Microservices | — | ✅ | ✅ | — | — |
| Travel APIs (GDS/NDC/OTA) | — | ✅ | — | — | — |
| Multi-Tenant SaaS | — | — | ✅ | — | — |
