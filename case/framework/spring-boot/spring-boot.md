# Spring Boot — Complete Guide

> **Series:** Framework Documentation
> Spring Boot — the opinionated, production-grade Java framework (enterprise backend). Related: `case/api/apis-and-communication.md` (REST §1–8), `case/database/databases.md` (PostgreSQL §1–11), `case/security/security-and-auth.md` (OAuth/JWT §9–24), `case/iac/iac-tools.md` (deployment).

---

## Table of Contents

- [1. What Is Spring Boot?](#1-what-is-spring-boot)
- [2. Spring Boot vs Other Frameworks](#2-spring-boot-vs-other-frameworks)
- [3. How Spring Boot Works](#3-how-spring-boot-works)
- [4. Core Concepts and Features](#4-core-concepts-and-features)
- [5. Where to Use Spring Boot](#5-where-to-use-spring-boot)
- [6. Where NOT to Use Spring Boot](#6-where-not-to-use-spring-boot)
- [7. Installation and Setup](#7-installation-and-setup)
- [8. Project Structure and Configuration](#8-project-structure-and-configuration)
- [9. Spring Boot Production Best Practices](#9-spring-boot-production-best-practices)
- [10. Spring Boot Real-World Examples](#10-spring-boot-real-world-examples)
- [11. Spring Boot Pitfalls](#11-spring-boot-pitfalls)

---

## 1. What Is Spring Boot?

**Spring Boot** is an opinionated, production-ready Java framework that simplifies the Spring ecosystem — providing **auto-configuration, embedded servers, and starters** so you can build standalone, production-grade apps with minimal XML/config.

- "Convention over configuration" — sensible defaults, auto-wired beans.
- **Embedded Tomcat** — run as a standalone JAR (no WAR deployment to an external server).
- **Starters** bundle dependencies (`spring-boot-starter-web`, `-data-jpa`, `-security`).
- The dominant choice for **enterprise Java** backends.

**One-liner:** the production-ready, batteries-included Java framework for enterprise backends.

## 2. Spring Boot vs Other Frameworks

| | Spring Boot | NestJS | Django | Express |
|---|---|---|---|---|
| Language | Java (JVM) | TypeScript (Node) | Python | JavaScript (Node) |
| Type system | Strong, static | Static (TS) | Dynamic | Dynamic |
| Ecosystem | Massive (enterprise) | Growing | Full-stack | Huge (npm) |
| Best for | Enterprise, large teams | Structured Node backends | Full apps | Lightweight APIs |

**Rule of thumb:** Spring Boot for **enterprise Java backends, large teams, performance-sensitive JVM workloads**; NestJS for a structured TypeScript backend; Django for Python full-stack; Express for minimal Node APIs.

## 3. How Spring Boot Works

- **Inversion of Control (IoC)** — the Spring container manages objects (**beans**) and injects dependencies.
- **Auto-configuration** — Spring Boot inspects the classpath and wires beans automatically (e.g., a DB driver present → configure a datasource).
- A **request** flows: DispatcherServlet → **Controller** → **Service** → **Repository** (JPA) → response (often JSON via Jackson).
- **Annotations** (`@RestController`, `@Service`, `@Autowired`) declare roles and wiring.
- **Embedded server** (Tomcat) starts with the app — `java -jar app.jar` runs it.

## 4. Core Concepts and Features

| Concept | What it is |
|---|---|
| **IoC / DI** | Container manages beans; `@Autowired` injects dependencies |
| **Beans** | Spring-managed objects (`@Component`, `@Service`, `@Repository`) |
| **Auto-configuration** | Classpath-driven bean wiring (`@SpringBootApplication`) |
| **Spring MVC** | `@RestController` + `@GetMapping`/`@PostMapping` for REST |
| **Spring Data JPA** | Repository interfaces → SQL auto-generated (like an ORM) |
| **Spring Security** | Auth, authorization, OAuth2/JWT integration |
| **Starters** | Opinionated dependency bundles |
| **Actuator** | Production metrics, health checks, info endpoints |
| **Profiles** | Environment-specific config (`dev`, `prod`) |
| **Validation** | Bean Validation (`@Valid`, `@NotNull`, `@Size`) |

## 5. Where to Use Spring Boot

- **Enterprise backends** — large, long-lived systems with complex domains.
- **Teams wanting strong typing + structure** (Java + layered architecture).
- **Performance-sensitive** JVM workloads (concurrency, throughput).
- **Microservices** on the JVM (Spring Cloud ecosystem).

## 6. Where NOT to Use Spring Boot

- **Rapid prototyping / small APIs** — the JVM + Spring overhead is heavier than Python/Node options.
- **Teams without Java expertise** — the ecosystem assumes Java/JVM knowledge.
- **Serverless/cold-start-sensitive** — JVM startup can be slow (consider native images or a lighter runtime).

## 7. Installation and Setup

```bash
# Using Spring Initializr (start.spring.io) — generates a Maven/Gradle project
# Or via CLI:
spring init --dependencies=web,data-jpa,postgresql myapp
cd myapp && ./mvnw spring-boot:run    # http://localhost:8080
```

```java
// src/main/java/com/example/myapp/MyappApplication.java
@SpringBootApplication
public class MyappApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyappApplication.class, args);
    }
}

// A REST controller
@RestController
@RequestMapping("/api/items")
public class ItemController {
    @Autowired private ItemService service;
    @GetMapping("/{id}")
    public Item get(@PathVariable Long id) { return service.get(id); }
}
```

## 8. Project Structure and Configuration

```
src/main/
├── java/com/example/myapp/
│   ├── MyappApplication.java     # entry point (@SpringBootApplication)
│   ├── controller/               # REST controllers
│   ├── service/                  # business logic (@Service)
│   ├── repository/               # Spring Data JPA interfaces
│   ├── model/                    # JPA entities
│   └── config/                   # @Configuration beans, security config
└── resources/
    └── application.properties    # config (DB, server port, profiles)
```

- **Layered**: Controller → Service → Repository → Entity (classic clean architecture).
- **`application.properties`/`.yml`** holds config; **profiles** switch per environment.
- **Maven/Gradle** manage dependencies via starters.

## 9. Spring Boot Production Best Practices

1. **Use profiles** (`dev`/`prod`) to separate environment config.
2. **Externalize config** — secrets/DB via env vars, not in `application.properties`.
3. **Keep layers clean** — controllers thin; logic in `@Service`; data in repositories.
4. **Validate inputs** (`@Valid` + Bean Validation) at the controller boundary.
5. **Use Spring Data JPA** for data access; watch for N+1 (entity graphs/fetch types).
6. **Enable Actuator** for health checks + metrics in production.
7. **Connection pooling** (HikariCP — default); tune pool size.
8. **Containerize** (Docker) and run as an embedded-server JAR.

## 10. Spring Boot Real-World Examples

### Example 1 — Full Layered CRUD (Controller/Service/Repository)
```java
// Entity
@Entity public class Item {
    @Id @GeneratedValue private Long id;
    private String name; private BigDecimal price;
}

// Repository — SQL auto-generated
public interface ItemRepository extends JpaRepository<Item, Long> {}

// Service
@Service public class ItemService {
    @Autowired private ItemRepository repo;
    public Item get(Long id) { return repo.findById(id).orElseThrow(); }
    public Item create(Item i) { return repo.save(i); }
}

// Controller
@RestController @RequestMapping("/api/items")
public class ItemController {
    @Autowired private ItemService service;
    @PostMapping public Item create(@Valid @RequestBody Item i) { return service.create(i); }
}
```
**Why:** full CRUD with near-zero SQL — the repository interface generates it.

### Example 2 — Profile-Based Config
```properties
# application-prod.properties
spring.datasource.url=${DB_URL}
spring.datasource.password=${DB_PASSWORD}
server.port=8080
```
**Why:** environment-specific config without code changes; secrets from env.

### Example 3 — Validation at the Boundary
```java
public class CreateItemDTO {
    @NotBlank private String name;
    @DecimalMin("0.0") private BigDecimal price;
}
@PostMapping public Item create(@Valid @RequestBody CreateItemDTO dto) { ... }
```
**Why:** invalid payloads rejected before reaching service logic.

## 11. Spring Boot Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| N+1 with JPA lazy relations | Slow list endpoints | Entity graphs / `@EntityGraph` / fetch joins |
| Logic in controllers | Untestable, repeated | Move to `@Service` layer |
| Secrets in properties files | Leaked credentials | Env vars / external config |
| Heavy startup | Slow cold starts | Native images (GraalVM) or accept JVM warmup |
| Over-fetching entities | Large payloads | Use DTOs/projections, not raw entities |
| Tight coupling (manual `new`) | Hard to test/mock | Use DI (`@Autowired`/constructor injection) |
