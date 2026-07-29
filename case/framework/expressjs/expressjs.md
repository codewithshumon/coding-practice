# Express.js — Complete Guide

> **Series:** Framework Documentation
> Express.js — the minimal, unopinionated Node.js web framework. Related: `case/api/apis-and-communication.md` (REST §1–8), `case/framework/nestjs/nestjs.md` (the structured alternative), `case/security/security-and-auth.md` (JWT §17–24), `case/devops/devops-and-cicd.md`.

---

## Table of Contents

- [1. What Is Express.js?](#1-what-is-expressjs)
- [2. Express vs NestJS vs Fastify](#2-express-vs-nestjs-vs-fastify)
- [3. How Express Works](#3-how-express-works)
- [4. Core Concepts and Features](#4-core-concepts-and-features)
- [5. Where to Use Express](#5-where-to-use-express)
- [6. Where NOT to Use Express](#6-where-not-to-use-express)
- [7. Installation and Setup](#7-installation-and-setup)
- [8. Project Structure and Configuration](#8-project-structure-and-configuration)
- [9. Express Production Best Practices](#9-express-production-best-practices)
- [10. Express Real-World Examples](#10-express-real-world-examples)
- [11. Express Pitfalls](#11-express-pitfalls)

---

## 1. What Is Express.js?

**Express.js** is the de facto **minimal, unopinionated** web framework for Node.js — providing a thin layer of routing and middleware over Node's HTTP module, leaving architecture entirely to you.

- **Minimal core** — routing, request/response objects, middleware. That's it.
- **Unopinionated** — no forced structure, DI, or ORM; you compose your stack.
- The foundation under many frameworks (NestJS, Redwood) and countless apps.

**One-liner:** the minimal, flexible Node.js framework — you bring the architecture.

## 2. Express vs NestJS vs Fastify

| | Express | NestJS | Fastify |
|---|---|---|---|
| Philosophy | Minimal/unopinionated | Opinionated, structured | Minimal, performance-first |
| Structure | You build it | Built-in (modules/DI) | You build it |
| Performance | Good | Good (Express under) | Highest |
| Best for | Small/custom APIs, full control | Large structured backends | Max-throughput APIs |

**Rule of thumb:** Express for **flexibility and full control** (small APIs, custom architecture); NestJS for **structure**; Fastify for **raw speed**.

## 3. How Express Works

- An Express **app** is a chain of **middleware** + **route handlers**.
- Each **request** passes through the middleware stack in order: `(req, res, next)`.
- **Routes** (`app.get`, `app.post`) match HTTP method + path to handlers.
- **`next()`** passes control to the next middleware; ending with `res.send()`/`res.json()`.
- Single-threaded **event loop** — async I/O scales well; CPU-bound work blocks it.

## 4. Core Concepts and Features

| Concept | What it is |
|---|---|
| **App** (`express()`) | The application instance |
| **Routing** | `app.get`/`post`/`use` + `express.Router` for grouping |
| **Middleware** | Functions `(req, res, next)` in the request pipeline |
| **Request/Response** | Enhanced `req`/`res` objects (params, body, json, headers) |
| **`express.Router`** | Mini-apps for modular route grouping |
| **Error handling** | Error-handling middleware `(err, req, res, next)` |
| **Template engines** | Optional server-rendered HTML (Pug, EJS) |
| **Static files** | `express.static` for serving assets |

## 5. Where to Use Express

- **Small-to-medium APIs** where minimal is enough.
- **Custom architectures** — you want full control over structure.
- **Prototypes and MVPs** — fast to start.
- **As a base** under other tools/frameworks.

## 6. Where NOT to Use Express

- **Large/enterprise backends** needing enforced structure → NestJS.
- **Maximum throughput** → Fastify.
- **Async-heavy** with strong typing/validation needs → FastAPI (Python) or NestJS.

## 7. Installation and Setup

```bash
npm init -y && npm install express
node index.js        # http://localhost:3000
```

```javascript
const express = require("express");
const app = express();

app.use(express.json());               // body parsing middleware

app.get("/items/:id", (req, res) => {
  res.json({ id: req.params.id });     // path param
});

app.post("/items", (req, res) => {
  res.status(201).json(req.body);      // echo validated body
});

app.listen(3000);
```

## 8. Project Structure and Configuration

```
src/
├── app.js               # express app + global middleware
├── server.js            # listen (bootstrap)
├── routes/              # express.Router per domain (users, orders)
├── controllers/         # route handler logic
├── services/            # business logic
├── middleware/          # auth, error-handler, logging
├── models/              # data models (Mongoose, Sequelize, etc.)
└── config/              # env-driven config
```

- Express imposes **no structure** — this layout is a common, sensible convention.
- **`express.Router`** modularizes routes; **error-handler middleware** is registered **last**.
- **Config via env** (`dotenv`); validation via `zod`/`joi` (Express doesn't validate for you).

## 9. Express Production Best Practices

1. **Use TypeScript** — type safety at scale (plain JS gets unsafe in large apps).
2. **Validate all input** — `zod`/`joi`; Express does no validation by default.
3. **Centralized error handling** — one error-handler middleware, not try/catch everywhere.
4. **Structure the app** — routes/services/middleware; don't dump everything in one file.
5. **Security headers** — `helmet`; enable CORS deliberately (not `*` + credentials).
6. **Run behind a process manager** (PM2) or container; handle graceful shutdown.
7. **Async error handling** — wrap async handlers (unhandled rejections crash Node).
8. **Offload CPU-bound work** — don't block the event loop.

## 10. Express Real-World Examples

### Example 1 — Modular Router + Service
```javascript
// routes/users.js
const router = require("express").Router();
const usersService = require("../services/users");

router.get("/", async (req, res, next) => {
  try { res.json(await usersService.findAll()); }
  catch (e) { next(e); }              // delegate to error handler
});
module.exports = router;

// app.js
app.use("/users", require("./routes/users"));
```
**Why:** modular, testable routes — not a 2000-line `app.js`.

### Example 2 — Centralized Error Handler (registered last)
```javascript
// middleware/error-handler.js  — MUST be registered AFTER routes
app.use((err, req, res, next) => {
  logger.error(err);
  res.status(err.status || 500).json({ error: err.message || "Internal error" });
});
```
**Why:** one place for error responses; consistent format, no leaked stack traces.

### Example 3 — Input Validation (zod)
```javascript
const { z } = require("zod");
const CreateUser = z.object({ email: z.string().email(), password: z.string().min(8) });

router.post("/", (req, res, next) => {
  const parsed = CreateUser.safeParse(req.body);
  if (!parsed.success) return res.status(400).json({ errors: parsed.error.issues });
  // parsed.data is typed + valid
});
```
**Why:** Express won't validate for you — a schema library prevents bad data reaching logic.

## 11. Express Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| No input validation | Bad/injected data | `zod`/`joi` on every endpoint |
| Unhandled async errors | Process crash | Wrap handlers / `express-async-errors` |
| One giant `app.js` | Unmaintainable | Routes/services/middleware split |
| Blocking the event loop | All requests stall | Offload CPU-bound work |
| `cors({ origin: "*" })` + credentials | Security hole | Explicit allowed origins |
| Plain JS at scale | Type bugs | Use TypeScript |
| No error-handler middleware | Inconsistent/leaky errors | Centralized handler, registered last |
