# Write Quality Code

> **Category:** Code Quality & Testing
> **Relevant at:** As-Sunnah Foundation, MVI Solutions
> **Related tech docs:** `case/structures-architecture/backend-systems.md` (Backend Architecture §9–16, Software Architecture §33–40), `case/devops/devops-and-cicd.md` (Git §1–11)

---

## 1. What This Means

Writing quality code means producing code that is **clean, modular, reusable, well-tested, and well-documented** — following established engineering standards so the code is understandable, changeable, and reliable over its lifetime.

**Scope:**
- **Clean** — readable, intention-revealing names, small focused functions, minimal complexity
- **Modular** — cohesive modules with clear boundaries; separation of concerns
- **Reusable** — DRY (don't repeat yourself), composable, no copy-paste duplication
- **Well-tested** — testable by design (dependency injection, pure functions)
- **Well-documented** — self-documenting code first; comments/docs for the *why*

**Why it matters:** code is read far more often than it's written. Quality code reduces bugs, speeds up future changes, and lets new team members contribute quickly. Low-quality code accrues technical debt that eventually makes every change slow and risky.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**Quality is visible in the everyday decisions:**
- A function does **one thing** (single responsibility) — you can name it accurately
- A module's **public API is small** — internals are hidden, boundaries are clear
- Duplication is **extracted** into a shared helper, not copy-pasted
- Tests exist because the code was **designed to be testable** (dependencies injected, not hardcoded)
- Comments explain **why**, not *what* (the code already shows what)

**Real-world signals of quality vs. debt:**
| Quality code | Low-quality code |
|---|---|
| Small, focused functions | 300-line methods doing everything |
| Clear names (`fetchActiveUsers`) | Cryptic names (`getData`, `proc2`) |
| One responsibility per module | God classes touching everything |
| Duplication extracted | Copy-pasted blocks everywhere |
| Testable (DI, pure functions) | Hardcoded dependencies, hidden state |
| Comments explain why | Comments restate the code |

**The principle:** write code for the **next developer to read** (who might be you in six months), not for the compiler. Optimze for clarity first, performance second (premature optimization harms clarity).

---

## 3. How to Implement

### Small, Focused Functions (Single Responsibility)

```python
# BAD: does fetching, filtering, transformation, and formatting
def process_users():
    raw = db.query("SELECT * FROM users")
    active = [u for u in raw if u["status"] == "active"]
    formatted = [{"name": u["name"].upper(), "email": u["email"]} for u in active]
    return formatted

# GOOD: each function does one thing, composable + testable
def fetch_users(status: str | None = None) -> list[User]:
    return db.users.filter(status=status) if status else db.users.all()

def format_user(user: User) -> dict:
    return {"name": user.name.upper(), "email": user.email}

def get_active_users_formatted() -> list[dict]:
    return [format_user(u) for u in fetch_users(status="active")]
```

### Meaningful Names

```python
# BAD — names that lie or obscure intent
def proc(d): ...           # what does it process? what's d?
data = get_stuff()         # what stuff?

# GOOD — names reveal intent
def calculate_order_total(items: list[OrderItem]) -> Decimal: ...
active_users = fetch_users(status="active")
```

### DRY — Extract Duplication

```python
# BAD: the same validation logic copy-pasted in 5 endpoints
def create_order(dto): validate(dto); ...
def update_order(dto): validate(dto); ...

# GOOD: one function, reused — fix a bug once, it's fixed everywhere
def validate_order(dto: OrderDTO) -> None:
    if not dto.items: raise ValidationError("items required")
    if dto.total <= 0: raise ValidationError("total must be positive")
```

### Testable by Design (Dependency Injection)

```python
# BAD — hard to test (real DB + real email hardcoded)
def register_user(email):
    user = db.save(email)           # hits real DB
    send_email(email, "welcome")    # sends real email

# GOOD — dependencies injected, easy to mock in tests
def register_user(email, db: UserRepo, mailer: Mailer):
    user = db.save(email)
    mailer.send(email, "welcome")
    return user
```

### Self-Documenting + Comments for "Why"

```python
# Good code documents WHAT by being clear — comments explain WHY
def retry_with_backoff(fn, max_attempts=3):
    """Retry a flaky operation with exponential backoff."""
    for attempt in range(max_attempts):
        try:
            return fn()
        except TransientError:
            if attempt == max_attempts - 1:
                raise
            # WHY: exponential backoff avoids hammering a recovering service
            sleep(2 ** attempt)
```

### Write Quality Code Checklist

- [ ] **Small, focused functions** — one responsibility each
- [ ] **Intention-revealing names** — no `data`/`proc`/`tmp`
- [ ] **DRY** — duplication extracted into shared, tested helpers
- [ ] **Modular** — clear boundaries; small public APIs
- [ ] **Testable by design** — DI, pure functions, no hidden state
- [ ] **Comments explain why**, not what
- [ ] **Consistent style** — follows the team's linter/formatter
- [ ] **No dead code / commented-out blocks** — version control remembers

### Avoid These

- **God functions/classes** — doing everything, hard to test or change
- **Cryptic or misleading names** — `data`, `handle`, `temp2`
- **Copy-paste duplication** — fix-once breaks; bugs replicated across copies
- **Hardcoded dependencies** — untestable; can't swap implementations
- **Comments rehashing the code** — noise that rots as code changes
- **Premature optimization** — sacrificing clarity for hypothetical speed
- **Deep nesting** — guard clauses flatten logic and improve readability
