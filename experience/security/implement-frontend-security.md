# Implement Frontend Security

> **Category:** Security
> **Relevant at:** As-Sunnah Foundation
> **Related tech docs:** `case/security/security-and-auth.md` (OAuth §9–16, JWT §17–24), `case/framework/nextjs/app-router-and-rendering.md` (Middleware §41–48, Server Actions §25–32), `case/web/web-quality.md`

---

## 1. What This Means

Implementing frontend security means building browser-side applications that are **safe from common web attacks** — with proper **authentication, authorization, secure session/token management, OAuth, JWT**, and defenses against **XSS, CSRF, and clickjacking**.

**Scope:**
- **Authentication flows** — OAuth 2. + PKCE, login/logout, session establishment
- **Token/session management** — where and how tokens are stored; refresh handling
- **Authorization on the client** — UI gating (while real authz stays server-side)
- **XSS prevention** — escaping, CSP, avoiding `dangerouslySetInnerHTML`
- **CSRF prevention** — tokens, SameSite cookies
- **Security headers** — CSP, X-Frame-Options, HSTS

**Why it matters:** the browser is a hostile environment — all client code is visible and mutable to an attacker. Frontend security isn't about trusting the client (you never fully can); it's about **not leaking secrets, not enabling injection, and ensuring the server is the real authority.**

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The trust boundary:** the client handles **UX and presentation**; the **server remains the authority** for auth and authz. Never rely on client-side checks alone to protect data.

```
Client (untrusted)              Server (authority)
  - Login UI                      - Validates credentials
  - Stores token securely         - Issues JWT/session
  - Gates UI (hide admin)         - Enforces authz per request
  - Sends token w/ requests       - Verifies token + scope
```

**Real-world decisions:**
- **Token storage** — JWT in `HttpOnly` cookie (XSS-safe) vs `localStorage` (XSS-stealable). HttpOnly cookie is preferred for web apps.
- **OAuth flow** — Authorization Code + PKCE for SPAs/Next.js; never the deprecated Implicit flow
- **Refresh tokens** — short-lived access tokens + refresh rotation; revoke on logout
- **XSS** — React auto-escapes, but `dangerouslySetInnerHTML` and user-content rendering need sanitization + CSP
- **CSRF** — SameSite cookies + CSRF tokens for cookie-based auth

---

## 3. How to Implement

### OAuth Authorization Code + PKCE

```tsx
// Login: redirect to provider with PKCE (never Implicit flow)
function login() {
  const codeVerifier = generateRandomString();
  const codeChallenge = base64Url(sha256(codeVerifier));
  sessionStorage.setItem("pkce_verifier", codeVerifier);

  window.location.href = providerAuthUrl +
    `?response_type=code&client_id=${CLIENT_ID}` +
    `&redirect_uri=${REDIRECT}&scope=openid profile` +
    `&code_challenge=${codeChallenge}&code_challenge_method=S256`;  // PKCE
}

// Callback: exchange code for token (ideally via a server route)
// The code_verifier proves the original requester — prevents code interception
```

### Secure Token Storage (HttpOnly Cookie Preferred)

```tsx
// BAD: JWT in localStorage — XSS can steal it
localStorage.setItem("token", jwt);

// GOOD: HttpOnly, Secure, SameSite cookie — JS can't read it
// Set by the server on login:
Set-Cookie: session=<jwt>; HttpOnly; Secure; SameSite=Lax; Max-Age=3600
// XSS that runs document.cookie still can't read it (HttpOnly)
```

### XSS Prevention

```tsx
// React auto-escapes — safe by default
<p>{userInput}</p>   {/* escaped, not executed */}

// DANGER: bypasses escaping — sanitize first
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userHtml) }} />

// Content Security Policy header — blocks inline scripts even if XSS occurs
// next.config.js headers:
{ source: "/(.*)", headers: [
  { key: "Content-Security-Policy",
    value: "default-src 'self'; script-src 'self'; object-src 'none'" },
]}
```

### CSRF Prevention (for Cookie-Based Auth)

```tsx
// SameSite cookies block most CSRF automatically
Set-Cookie: session=...; SameSite=Lax

// Double-submit token for extra defense
// Server issues a CSRF token; client sends it in a header on mutations
fetch("/api/orders", {
  method: "POST",
  headers: { "X-CSRF-Token": csrfToken },
  credentials: "include",
});
```

### Server-Side Authorization Is the Real Authority

```tsx
// UI gating (UX) — hide the admin button if not admin
{user.role === "admin" && <AdminButton />}

// But the SERVER must enforce it — client checks are cosmetic
// app/admin/page.tsx
export default async function AdminPage() {
  const user = await getCurrentUser();
  if (user.role !== "admin") notFound();   // server blocks access
  return <AdminDashboard />;
}
```

### Frontend Security Checklist

- [ ] **OAuth Authorization Code + PKCE** (never Implicit flow)
- [ ] **Tokens in HttpOnly cookies** (not localStorage) for web apps
- [ ] **Short-lived access tokens** + refresh-token rotation
- [ ] **Revoke on logout** — clear tokens/sessions
- [ ] **XSS prevented** — no unsafe HTML rendering; CSP header set
- [ ] **CSRF prevented** — SameSite cookies + CSRF tokens
- [ ] **Security headers** — CSP, HSTS, X-Frame-Options, X-Content-Type-Options
- [ ] **Server enforces authz** — client gating is UX only
- [ ] **No secrets in client code** — API keys/tokens belong server-side
- [ ] **Dependencies scanned** — known-vulnerable packages updated

### Avoid These

- **JWT in localStorage** — any XSS steals the token
- **Implicit OAuth flow** — token exposed in the URL
- **`dangerouslySetInnerHTML` without sanitization** — XSS
- **Trusting client-side authz** — hide-the-button ≠ security
- **Secrets in frontend code** — `NEXT_PUBLIC_API_KEY` is public; anyone can read it
- **No CSP** — one XSS hole compromises everything
- **Long-lived tokens without refresh** — a stolen token is a permanent credential
- **No CSRF protection** with cookie-based auth — cross-site forged requests
