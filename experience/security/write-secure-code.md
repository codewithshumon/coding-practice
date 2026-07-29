# Write Secure Code

> **Category:** Security
> **Relevant at:** MVI Solutions, Impressive Security
> **Related tech docs:** `case/security/security-and-auth.md` (API Security §1–8), `case/devops/devops-and-cicd.md` (CI/CD §23–33 — security scanning in pipelines)

---

## 1. What This Means

Writing secure code means applying **secure-coding practices as a baseline discipline** across the entire codebase — so that every feature is built to be resilient against common vulnerabilities, not just the obviously sensitive ones.

**Scope:**
- **Input validation & output encoding** — the foundation of secure code
- **Secrets management** — credentials never in code, configs, or history
- **Least privilege** — code, services, and users get only the access they need
- **Dependency security** — keeping libraries free of known vulnerabilities
- **Secure defaults** — fail closed, deny by default, encrypt by default
- **Security in the SDLC** — code review, automated scanning, threat awareness

**Why it matters:** security isn't a feature you add at the end — it's a property of *how you write every line*. One unvalidated input, one committed secret, one outdated dependency is enough for a breach. Secure coding makes safety the default, not an afterthought.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**Secure coding as a habit, applied everywhere:**
- Every function that accepts input validates it
- Every external call has a timeout and error handling
- Every secret comes from a secrets manager, never hardcoded
- Every dependency is pinned and scanned
- Every new feature gets a security review alongside a code review

**The OWASP mindset:** the same classes of vulnerability appear everywhere — injection, broken access control, security misconfiguration, vulnerable components. Writing secure code means **actively defending against these by default**, in every module.

**Real-world scenarios:**
- A junior developer hardcodes a DB password for "quick testing" → it ships to production → breach. **Secure default:** secrets come from env/secrets manager; `.env` is gitignored.
- A new endpoint trusts a client-supplied ID → IDOR (user A reads user B's data). **Secure default:** authorization checks on every resource access.
- An outdated library has a known CVE → exploited. **Secure default:** automated dependency scanning in CI.
- An error handler dumps a stack trace to the user → leaks internals. **Secure default:** generic errors to clients; details only in logs.

**The principle:** **assume hostile input, fail closed, minimize privileges, and make secure the easy/default path** (so developers don't have to "remember" to be secure).

---

## 3. How to Implement

### Input Validation + Output Encoding (the foundation)

```python
from pydantic import BaseModel

# Validate ALL input at the boundary — never pass raw client data to logic
class RegisterUserDTO(BaseModel):
    email: EmailStr
    password: str  # hashed before storage
    role: Literal["user"] = "user"   # client can't escalate to "admin"

@router.post("/register")
async def register(dto: RegisterUserDTO):
    password_hash = bcrypt.hash(dto.password)   # never store plaintext
    ...

# Output encoding — escape when rendering user content (prevents XSS/injection)
# Frameworks do this by default; only bypass with explicit sanitization
```

### Secrets Management

```python
# BAD — hardcoded, committed, leaked
DB_PASSWORD = "hunter2"

# GOOD — from environment / secrets manager
DB_PASSWORD = os.environ["DB_PASSWORD"]            # env var
db_password = await secrets_manager.get("prod/db")  # AWS Secrets Manager

# .gitignore — never commit .env, credentials, keys
.env
*.pem
credentials.json
```

```bash
# Catch committed secrets before they ship — pre-commit hook + CI scan
# Tools: git-secrets, TruffleHog, Gitleaks
gitleaks detect --source . --commit-since="2024-01-01"
```

### Least Privilege

```python
# Code/services/users get only the access they need — nothing more

# IAM role for a Lambda: only the specific actions/resources it needs
{
  "Effect": "Allow",
  "Action": ["s3:GetObject"],
  "Resource": "arn:aws:s3:::my-bucket/uploads/*"   # not s3:* on *
}

# DB user for the app: only CRUD on app tables — not DROP/ALTER
GRANT SELECT, INSERT, UPDATE, DELETE ON app.* TO 'app_user';
```

### Dependency Security

```bash
# Pin versions (no surprise breaking/malicious updates)
requirements.txt: django==5.0.1   # pinned, not >=

# Scan for known vulnerabilities in CI
pip-audit            # Python
npm audit            # Node.js
snyk test            # multi-language
# Block the build if high/critical CVEs are found
```

### Secure Defaults (fail closed)

```python
# Deny by default — opt INTO access, not out of it
DEFAULT_ALLOW = False   # access must be explicitly granted

# Encrypt by default
S3_BUCKET_ENCRYPTION = True
DB_TLS = True

# Timeouts on all external calls (prevent hanging/DoS)
await httpx.get(url, timeout=10)   # always set a timeout

# Generic errors to clients; details in logs only
except Exception as e:
    logger.error(e)                    # full detail in logs
    raise HTTPException(500, "Internal error")  # generic to client
```

### Security in the SDLC

```yaml
# CI: automated security checks on every PR
jobs:
  security:
    steps:
      - run: gitleaks detect            # secret scanning
      - run: pip-audit                  # dependency CVEs
      - run: bandit -r app/             # static analysis (Python)
      - run: npm audit                  # Node deps
# Code review checklist includes: input validation, authz, secrets, error handling
```

### Write Secure Code Checklist

- [ ] **All input validated** at boundaries (schemas/DTOs)
- [ ] **Output encoded** when rendering untrusted content
- [ ] **Secrets from env/secrets manager** — never hardcoded or committed
- [ ] **`.gitignore`** covers `.env`, keys, credentials
- [ ] **Least privilege** — code/services/users get minimum access
- [ ] **Dependencies pinned + scanned** in CI
- [ ] **Timeouts** on every external call
- [ ] **Secure defaults** — fail closed, encrypt by default
- [ ] **Generic errors to clients** — details in logs only
- [ ] **Security review** part of code review (not separate)
- [ ] **Secret scanning + SAST + dependency audit** in CI

### Avoid These

- **Hardcoded secrets** — "just for testing" leaks to production
- **Trusting client input** — validate everything at the boundary
- **Over-privileged code/services** — `s3:*`, admin DB users
- **Unpinned dependencies** — surprise breaking or malicious updates
- **No timeouts** — hanging calls enable DoS
- **Detailed errors to clients** — stack traces leak internals
- **Security as a final step** — bolted-on security misses everything
- **No secret scanning** — committed credentials are the #1 breach cause
