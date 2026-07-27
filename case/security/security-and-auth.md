# Security & Authentication — Complete Guide

> **Series:** Security Documentation — Part 1
> This file covers the **API security discipline** (rate limiting, validation, CORS, OWASP, request signing) and the core **auth mechanisms** (OAuth 2.0 and JWT). More topics (CORS deep-dive, webhook verification, PKCE, mTLS) will be added as separate files later.

---

## Table of Contents

- [Shared Orientation — API Security vs Auth Mechanisms](#shared-orientation--api-security-vs-auth-mechanisms)
- **API Security**
  - [1. What Is API Security?](#1-what-is-api-security)
  - [2. API Security vs Application Security](#2-api-security-vs-application-security)
  - [3. Core API Threats](#3-core-api-threats)
  - [4. API Security Techniques](#4-api-security-techniques)
  - [5. Where API Security Matters Most](#5-where-api-security-matters-most)
  - [6. API Security Best Practices](#6-api-security-best-practices)
  - [7. API Security Real-World Examples](#7-api-security-real-world-examples)
  - [8. API Security Pitfalls](#8-api-security-pitfalls)
- **OAuth**
  - [9. What Is OAuth?](#9-what-is-oauth)
  - [10. OAuth vs API Keys vs Sessions](#10-oauth-vs-api-keys-vs-sessions)
  - [11. How OAuth Works](#11-how-oauth-works)
  - [12. OAuth Grant Types](#12-oauth-grant-types)
  - [13. Where to Use OAuth](#13-where-to-use-oauth)
  - [14. OAuth Best Practices](#14-oauth-best-practices)
  - [15. OAuth Real-World Examples](#15-oauth-real-world-examples)
  - [16. OAuth Pitfalls](#16-oauth-pitfalls)
- **JWT**
  - [17. What Is JWT?](#17-what-is-jwt)
  - [18. JWT vs Opaque Tokens vs Sessions](#18-jwt-vs-opaque-tokens-vs-sessions)
  - [19. How JWT Works](#19-how-jwt-works)
  - [20. JWT Claims and Structure](#20-jwt-claims-and-structure)
  - [21. Where to Use JWT](#21-where-to-use-jwt)
  - [22. JWT Best Practices](#22-jwt-best-practices)
  - [23. JWT Real-World Examples](#23-jwt-real-world-examples)
  - [24. JWT Pitfalls](#24-jwt-pitfalls)
- [Shared Foundations](#shared-foundations)
- [Quick Reference Card](#quick-reference-card)

---

## Shared Orientation — API Security vs Auth Mechanisms

API Security and auth mechanisms are different levels of the same problem — they compose, not compete:

| Topic | Level | What it covers |
|---|---|---|
| **API Security** | Practices (comprehensive) | Rate limiting, validation, CORS, OWASP, key management, signing — the full surface |
| **OAuth** | Auth mechanism (protocol) | Delegated access without exposing credentials |
| **JWT** | Auth mechanism (token format) | Stateless, signed tokens for authentication/authorization |

**How they compose:**
- **API Security** says: "Every endpoint needs auth, rate limiting, input validation, CORS, and signing."
- **OAuth** says: "Use this protocol so users authorize your app without sharing their password."
- **JWT** says: "Use this token format (often *via* OAuth) for stateless, signed auth claims."

**Rule of thumb:** API Security sets the *what* (protect every endpoint); OAuth and JWT provide the *how* (delegation protocol + token format). A real production API uses all three together.

---

# API Security

## 1. What Is API Security?

**API Security** is the set of practices to protect APIs from abuse, attacks, and data leaks — covering **rate limiting, input validation, CORS policies, OWASP mitigations, API key management, OAuth 2.0, JWT auth, and request signing**.

**One-liner:** every endpoint has an attack surface — API security reduces it.

## 2. API Security vs Application Security

| | API Security | Application Security |
|---|---|---|
| Focus | API endpoints (HTTP) | All code + infrastructure |
| Threats | Injection, DoS, data leaks, broken auth | Broader (XSS, CSRF, file uploads, etc.) |
| Overlap | Auth, rate limiting | Auth overall |

**Key point:** API security is a **subset** of application security — it focuses on the HTTP/API attack surface. For the architectural context, API security complements `architecture-patterns.md`'s Multi-Tenant (tenant isolation) and `api/apis-and-communication.md` (API design patterns).

## 3. Core API Threats

| Threat | What it is |
|---|---|
| **Broken authentication** | Weak/missing auth, leaked keys |
| **Injection** (SQL, NoSQL, command) | Unsanitized input reaching a backend |
| **Excessive data exposure** | Returning more data than needed |
| **Lack of rate limiting** | One client can exhaust resources (DoS) |
| **Broken CORS** | Unauthorized cross-origin access |
| **Mass assignment** | Client updates fields they shouldn't |
| **Leaked secrets** | API keys/credentials in code, logs, or URLs |

## 4. API Security Techniques

| Technique | What it does |
|---|---|
| **Rate limiting** | Cap requests per client/key (token bucket, sliding window) — see `caching.md` Redis rate-limiter example |
| **Input validation** | Schema-validate every payload — reject malformed, sanitize inputs |
| **CORS** | Restrict which origins can call your API |
| **OWASP mitigations** | Prepared queries, parameterization, escaping |
| **API key management** | Rotate, scope (least privilege), never commit to code |
| **OAuth 2.0** | Delegate access without sharing credentials — see this file §9–16 |
| **JWT** | Stateless signed auth tokens — see this file §17–24 |
| **Request signing** | HMAC/AWS SigV4 — prove the client is who they claim (see `aws.md` §3) |

**Rule of thumb:** defense in depth — no single technique protects everything. Layer rate limiting + validation + CORS + proper auth + signing.

## 5. Where API Security Matters Most

- **Public-facing APIs** (exposed to abuse).
- **Multi-tenant SaaS** (tenant isolation — see `architecture-patterns.md` §17–24).
- **Payment/auth endpoints** (data and money).
- APIs that accept **user input, file uploads**, or integrate with **third parties** (webhooks).

## 6. API Security Best Practices

1. **Rate-limit every endpoint** per client/key.
2. **Validate and sanitize all input** — never trust client data.
3. **Strong auth** — OAuth + JWT or API keys with least privilege.
4. **Proper CORS headers** — restrict origins, not `*`.
5. **Never leak secrets** — no keys in code, logs, URLs, or client-side code.
6. **Log security events** (failed auth, rate hits, blocked requests).
7. **Keep OWASP Top 10** as ongoing awareness.

## 7. API Security Real-World Examples

### Example 1 — Layered API Protection
**Why:** rate limiter stops abuse, input validation blocks injection, CORS locks origins, and JWT auth gates access — four layers at once.

### Example 2 — Key Rotation
**Why:** rotate API keys on a schedule and revoke leaked keys immediately — keys are credentials, not configuration.

## 8. API Security Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| No rate limiting | Abuse, DoS, runaway cost | Rate-limit per client/key |
| Trusting client input | Injection, mass assignment | Validate + sanitize all input |
| CORS `*` everywhere | Unauthorized cross-origin access | Restrict to known origins |
| Keys in code/logs | Leaked credentials | Secrets manager, no logging |
| Ignoring OWASP Top 10 | Unknown exposure surface | Stay current with OWASP |

---

# OAuth

## 9. What Is OAuth?

**OAuth 2.0** is an **open standard for access delegation** — a user can let a third-party application access their data *without sharing their password*.

- It's about **delegated authorization**, not just authentication.
- Widely used for "Sign in with Google/GitHub," letting apps access your resources.

**One-liner:** let an app access your stuff without giving it your password.

## 10. OAuth vs API Keys vs Sessions

| | OAuth | API Keys | Sessions |
|---|---|---|---|
| Model | Delegated, time-limited tokens | Static shared secret | Server-side cookie + session |
| User presence | Yes (authorizes scoped access) | Not directly | Yes (implicit via cookie) |
| Best for | Third-party apps, delegated access | Simple machine-to-machine | Traditional web apps |

**Rule of thumb:** **OAuth** for user-delegated access and third-party integrations; **API keys** for machine-to-machine; **sessions** for traditional web apps.

## 11. How OAuth Works

1. **Client** asks the user to **authorize** access (scope = what to access).
2. User **consents** (via the provider).
3. Client receives an **authorization code**.
4. Client **exchanges** the code for an **access token** (and optionally a refresh token).
5. Client uses the access token to call the API on the user's behalf.

**Key point:** the user never shares their password with the client — the provider issues scoped, time-limited tokens instead.

## 12. OAuth Grant Types

| Grant | When to use |
|---|---|
| **Authorization Code + PKCE** | Browser/web apps, mobile apps (with PKCE for security) |
| **Client Credentials** | Machine-to-machine (no user) |
| **Refresh Token** | Get a new access token without re-prompting |
| **Implicit** (deprecated) | Was used for SPAs; don't use |
| **Password** (deprecated) | Was used for trusted apps; don't use |

**Rule of thumb:** **Authorization Code + PKCE** for anything with a user; **Client Credentials** for automated services.

## 13. Where to Use OAuth

- **"Sign in with X"** (Google, GitHub, Facebook).
- Third-party apps needing access to a user's resources.
- **Delegated** authorization (fine-grained scopes).

## 14. OAuth Best Practices

1. **Use PKCE** with Authorization Code flow — always.
2. **Short-lived access tokens** (minutes/hours); use refresh tokens for longevity.
3. **Wide scopes defensively** — grant only what's needed.
4. **Use state/nonce** to prevent CSRF in the redirect.
5. **Rotate refresh tokens**; invalidate on logout.
6. Validate the **redirect URI**.

## 15. OAuth Real-World Examples

### Example 1 — Google Sign-In
**Why:** user clicks "Sign in with Google," consents to scopes (profile, email), and your app gets a short-lived access token — no password shared.

### Example 2 — GitHub App Access
**Why:** a tool requests `repo` scope; the user authorizes; the tool gets a token scoped only to the user's repos.

## 16. OAuth Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| No PKCE | Authorization code interception | Add PKCE |
| Implicit flow (deprecated) | Token exposed in URLs | Use Auth Code + PKCE |
| Overly broad scopes | Excessive access | Grant only needed scopes |
| Redirect URI not validated | Token theft | Validate URIs strictly |

---

# JWT

## 17. What Is JWT?

**JWT (JSON Web Token)** is a compact, URL-safe **token format** for transmitting signed (and optionally encrypted) claims between parties — commonly used for **stateless authentication and authorization**.

**One-liner:** a signed, portable token carrying auth claims.

## 18. JWT vs Opaque Tokens vs Sessions

| | JWT | Opaque Token | Session Cookie |
|---|---|---|---|
| State | Stateless (contains claims) | Server must verify | Server checks |
| Server lookup | No lookup needed | Requires DB/cache lookup | In-memory/cache |
| Best for | APIs, microservices, distributed | Where revocation is critical | Monolithic web apps |

**Rule of thumb:** **JWT** for stateless, distributed auth (no server lookup); **opaque tokens** when you need instant revocation; **sessions** for traditional server-rendered apps.

## 19. How JWT Works

1. **Server creates a JWT** with claims (user ID, roles, expiry), **signs** it.
2. Server sends the **signed token** to the client.
3. Client sends the token with requests (usually `Authorization: Bearer <token>`).
4. Server **validates the signature** (and claims), reads user info from the token — **no database lookup needed**.

**Key point:** the signature proves the token hasn't been tampered with; the server only needs the public/secret key to verify — not a DB hit.

## 20. JWT Claims and Structure

A JWT is three Base64-encoded parts: `header.payload.signature`

| Part | Contains |
|---|---|
| **Header** | Algorithm (`HS256`, `RS256`) and type (`JWT`) |
| **Payload** | Claims: `sub` (user), `iat`, `exp`, `roles`, custom |
| **Signature** | Crypto proof (HMAC or RSA/ECDSA) — the payload hasn't been modified |

**Claims to use:**
- `sub` — subject (user ID)
- `iss` — issuer; `aud` — audience (which API the token is for)
- `exp` — expiration (always set it)
- `iat` — issued at; `nbf` — not before

## 21. Where to Use JWT

- **Stateless APIs** (REST, GraphQL) — no server-side session store.
- **Microservices** — pass identity between services without a central session DB.
- **OAuth access tokens** — JWT is the common format for OAuth tokens.

## 22. JWT Best Practices

1. **Always set `exp`** — an unexpiring token is a permanent credential.
2. **Short-lived tokens** (minutes/hours) — use refresh mechanisms for longevity.
3. **Prefer RS256 (asymmetric)** — the auth server signs, other services verify with the public key.
4. **Validate everything** — signature, `exp`, `iss`, `aud`, `nbf`.
5. **Never store secrets in the payload** — the payload is encoded (base64), not encrypted.
6. **Use HTTPS only**; store tokens securely on the client.

## 23. JWT Real-World Examples

### Example 1 — Stateless API Auth
```
Client: POST /login { email, password } → Server: 200 + JWT { sub: user-42, exp: 1h }
Client: GET /profile + Authorization: Bearer <jwt> → Server verifies signature + exp
```
**Why:** the API authenticates requests without a session DB — stateless and horizontally scalable.

### Example 2 — OAuth Access Token
**Why:** after an OAuth flow, the auth server issues a JWT access token; the resource server verifies the signature (no call to the auth server needed).

## 24. JWT Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| No `exp` / very long-lived | Token never/infrequently expires | Short-lived + refresh |
| HS256 everywhere | All services share the secret | Prefer RS256 (public/private) |
| Sensitive data in payload | Encoded, not encrypted | Don't put secrets in JWT |
| Missing validation | Forged/expired tokens accepted | Validate signature + claims |
| Storing in localStorage | XSS can steal | HttpOnly cookie or secure storage |

---

## Shared Foundations

Concepts that recur across **all three topics**:

- **The threat model > the tools** — know what you're defending against (OWASP) before picking auth mechanisms. Layered defense: rate limiting + validation + CORS + OAuth + JWT.
- **Least privilege** — OAuth scopes, JWT claims, API key permissions: grant only what's needed.
- **Secrets management** — API keys, JWT signing keys, OAuth client secrets: never in code, logs, or URLs. Use a secrets manager.
- **Expiry and rotation** — tokens, keys, and secrets must expire and rotate.
- **Consistent error handling** — don't leak implementation details in auth errors; log but don't expose.

## Quick Reference Card

```
API SECURITY (the practices):
  ✓ Rate limiting      ✓ Input validation     ✓ CORS (restricted)
  ✓ OWASP awareness    ✓ API key management   ✓ Request signing

AUTH MECHANISM PICKER:
  User delegates access to a third party?  → OAuth 2.0
  Simple machine-to-machine?               → API Keys
  Stateless auth with no DB lookup?        → JWT
  Traditional web app auth?                → Sessions (+ cookies)

OAUTH:
  Flow → Authorization Code + PKCE (browser) or Client Credentials (M2M)
  Never → Implicit flow or Password grant (deprecated)

JWT:
  Structure → header.payload.signature (base64, not encrypted)
  Always → set exp; validate signature + claims; prefer RS256
  Never → put secrets in the payload; use localStorage

GOLDEN RULES:
  ✓ Defense in depth — no single technique is enough
  ✓ Least privilege — scopes, claims, key permissions
  ✓ Short-lived + rotation — tokens, keys, secrets
  ✓ HTTPS everywhere
  ✓ Never commit secrets; never log them
```

---

*This file covers the API security discipline and the core auth mechanisms. More topics (CORS deep-dive, webhook verification, PKCE details, mTLS, OWASP Top 10) will be added as separate files in this series over time.*
