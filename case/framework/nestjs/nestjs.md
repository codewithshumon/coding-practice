# NestJS — Complete Guide

> **Series:** Framework Documentation
> NestJS — the progressive, opinionated Node.js framework (Angular-inspired, TypeScript-first). Related: `case/api/apis-and-communication.md` (REST §1–8), `case/state-management/react-state-management.md`, `case/security/security-and-auth.md` (JWT §17–24), `case/framework/expressjs/expressjs.md`, `case/framework/angular/angular.md` (the frontend counterpart — same patterns, server-side).

---

## Table of Contents

- [1. What Is NestJS?](#1-what-is-nestjs)
- [2. NestJS vs Express vs Fastify](#2-nestjs-vs-express-vs-fastify)
- [3. How NestJS Works](#3-how-nestjs-works)
- [4. Core Concepts and Features](#4-core-concepts-and-features)
- [5. Where to Use NestJS](#5-where-to-use-nestjs)
- [6. Where NOT to Use NestJS](#6-where-not-to-use-nestjs)
- [7. Installation and Setup](#7-installation-and-setup)
- [8. Project Structure and Configuration](#8-project-structure-and-configuration)
- [9. NestJS Production Best Practices](#9-nestjs-production-best-practices)
- [10. NestJS Real-World Examples](#10-nestjs-real-world-examples)
- [11. NestJS Pitfalls](#11-nestjs-pitfalls)

---

## 1. What Is NestJS?

**NestJS** is a progressive Node.js framework for building efficient, scalable server-side apps — using **TypeScript, modular architecture, decorators, and dependency injection**, heavily inspired by Angular.

- **Opinionated structure** — modules, controllers, providers give large codebases organization.
- **DI container** — services injected, easily testable and swappable.
- Built on **Express** by default (Fastify optional) — NestJS adds architecture, not a new HTTP core.

**One-liner:** the structured, Angular-inspired TypeScript backend framework for scalable Node.js apps.

## 2. NestJS vs Express vs Fastify

| | NestJS | Express | Fastify |
|---|---|---|---|
| Structure | Opinionated (modules/DI) | Minimal/unopinionated | Minimal, fast |
| TypeScript | First-class | Manual | Good |
| Architecture | Built-in (Angular-like) | You build it | You build it |
| Best for | Large/enterprise Node backends | Small/custom APIs | Max-throughput APIs |

**Rule of thumb:** NestJS for **structured, scalable Node backends** (teams, large codebases); Express for **small/custom**; Fastify for **raw throughput**.

## 3. How NestJS Works

- The app is a tree of **modules**; each module groups related controllers + providers.
- **Controllers** handle HTTP (`@Get`, `@Post`); **providers/services** hold business logic.
- **Dependency injection** — the framework instantiates and injects services (constructor-based).
- A **request** flows: Middleware → Guards → Pipes → Interceptor → Controller → Interceptor (response) → Exception filter.
- Runs on **Express or Fastify** underneath.

## 4. Core Concepts and Features

| Concept | What it is |
|---|---|
| **Modules** (`@Module`) | Organize the app into feature groups |
| **Controllers** (`@Controller`) | Route handlers (`@Get`/`@Post`) |
| **Providers/Services** | Injectable business logic (`@Injectable`) |
| **Dependency injection** | Framework wires services into constructors |
| **DTOs + Pipes** | Validation/transform (`class-validator`, `ValidationPipe`) |
| **Guards** | Authorization (`@UseGuards`, returns true/false) |
| **Interceptors** | Wrap logic (logging, mapping, caching) |
| **Middleware** | Pre-route processing (Express-style) |
| **Exception filters** | Centralized error handling |

## 5. Where to Use NestJS

- **Large/enterprise Node.js backends** — the modular structure scales with teams.
- **Microservices** — NestJS has first-class microservice transport support.
- **Teams wanting structure + DI** without building it from scratch.
- **Apps needing clear separation** (controller/service/repository layers).

## 6. Where NOT to Use NestJS

- **Small/simple APIs** — the architecture overhead exceeds the payoff.
- **Maximum raw throughput** — Fastify/Express are lighter (NestJS adds layers).
- Teams that prefer **minimal/unopinionated** tooling.

## 7. Installation and Setup

```bash
npm i -g @nestjs/cli
nest new myapp && cd myapp
nest generate resource users     # scaffolds module/controller/service/dto
npm run start:dev                # http://localhost:3000
```

```typescript
// users/users.controller.ts
@Controller("users")
export class UsersController {
  constructor(private readonly usersService: UsersService) {}   // injected

  @Get()
  findAll() { return this.usersService.findAll(); }

  @Post()
  create(@Body() dto: CreateUserDto) { return this.usersService.create(dto); }
}

// users/users.service.ts
@Injectable()
export class UsersService {
  findAll() { return [{ id: 1, name: "Shumon" }]; }
}
```

## 8. Project Structure and Configuration

```
src/
├── main.ts                 # bootstrap (app + global pipes/filters)
├── app.module.ts           # root module (imports feature modules)
├── users/
│   ├── users.module.ts     # @Module — controllers + providers
│   ├── users.controller.ts # routes
│   ├── users.service.ts    # @Injectable business logic
│   ├── dto/                # request/response DTOs
│   └── entities/           # domain models
└── common/                 # guards, pipes, filters, interceptors (shared)
```

- **Feature-based modules** — each domain (users, orders) is self-contained.
- **Global pipes/filters** set in `main.ts` (e.g., global `ValidationPipe`).
- **Config** via `@nestjs/config` (env-driven, validated).

## 9. NestJS Production Best Practices

1. **Feature-based modules** — one module per domain, self-contained.
2. **Thin controllers** — delegate to services; logic lives in `@Injectable`.
3. **Global `ValidationPipe`** — validate every DTO at the boundary.
4. **Guards for authz** — `@UseGuards(JwtAuthGuard)`, per-route roles.
5. **Exception filters** for consistent error responses.
6. **Depend on abstractions** where swapping matters (interfaces for repos/adapters).
7. **Config via env** (`@nestjs/config`); never hardcode secrets.
8. **Use Fastify adapter** if you need more throughput than Express.

## 10. NestJS Real-World Examples

### Example 1 — Validation via DTO + Global Pipe
```typescript
// main.ts
app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));

// dto/create-user.dto.ts
export class CreateUserDto {
  @IsEmail() email: string;
  @MinLength(8) password: string;
}
```
**Why:** every payload validated + stripped of extra fields automatically.

### Example 2 — JWT Auth Guard
```typescript
@Injectable()
export class JwtAuthGuard extends AuthGuard("jwt") {}

@Controller("users")
@UseGuards(JwtAuthGuard)            // protects every route
export class UsersController { ... }
```
**Why:** declarative authorization — protected routes are obvious from decorators.

### Example 3 — Injected Repository (Swappable)
```typescript
@Injectable()
export class UsersService {
  constructor(@Inject("IUserRepo") private repo: IUserRepository) {}
  findAll() { return this.repo.findAll(); }
}
// Swap Postgres/in-memory implementations without touching UsersService.
```
**Why:** DI + interfaces make the service testable and vendor-agnostic.

## 11. NestJS Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Logic in controllers | Untestable, repeated | Move to services |
| No global ValidationPipe | Bad data reaches logic | Enable global ValidationPipe |
| Manual `new` for services | Breaks DI/testing | Use constructor injection |
| One giant module | No organization | Feature-based modules |
| Hardcoded config/secrets | Leaked credentials | `@nestjs/config` + env |
| Over-using NestJS for tiny APIs | Needless overhead | Use Express/Fastify for small apps |
