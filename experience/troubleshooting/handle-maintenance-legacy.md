# Handle Maintenance & Legacy Systems

> **Category:** Operations & Troubleshooting
> **Relevant at:** MVI Solutions
> **Related tech docs:** `case/code-quality/write-quality-code.md` (clean code), `case/code-quality/maintain-test-suites.md` (characterization tests), `case/devops/devops-and-cicd.md` (CI/CD §23–33), `case/database/databases.md` (Database Optimization §45–55)

---

## 1. What This Means

Handling maintenance and legacy systems means keeping **existing applications healthy** — troubleshooting bugs, performing upgrades, and independently delivering small-to-medium improvements (bug fixes, performance gains, feature enhancements) in codebases that may be old, undocumented, or fragile.

**Scope:**
- **Troubleshooting & debugging** existing code — often without full understanding or docs
- **Upgrading** — dependencies, frameworks, language versions (tech debt reduction)
- **Bug fixes** — diagnosing and resolving issues in production
- **Performance improvements** — optimizing slow parts of legacy code
- **Feature enhancements** — adding to existing systems safely (without breaking them)
- **Independent ownership** — handling small-to-medium tasks end-to-end without hand-holding

**Why it matters:** most professional engineering work is **maintaining existing systems**, not greenfield development. Legacy code is where the business value already lives — keeping it running, secure, and improving incrementally is often more valuable (and harder) than building new things.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**Working with legacy code (the reality):**
- Code that lacks tests, docs, or clear architecture
- Dependencies years out of date (security risks, incompatibilities)
- "Don't touch that — nobody knows what it does" fear zones
- Business logic encoded in obscure places

**The safe-change methodology (core skill):**
```
Understand before changing
  → add characterization tests (lock current behavior)
     → make the change in small, verifiable steps
        → test each step
           → deploy incrementally
```

**Real-world scenarios:**
- **Upgrade an outdated dependency** → check changelog/breaking changes → update → run tests → fix breakage → deploy
- **Fix a reported bug** → reproduce → read the relevant code → add a test that fails → fix → test passes → deploy
- **Improve a slow legacy endpoint** → profile → find the bottleneck → optimize → verify no regression → deploy
- **Add a feature to an old module** → understand the existing patterns → extend consistently → test → deploy

**The principle:** **legacy code demands discipline, not heroics.** Understand first, test to lock behavior, change in small steps, verify constantly. Reckless changes to fragile systems cause outages.

---

## 3. How to Implement

### Step 1 — Understand Before Changing

```python
# Read the code + its tests (if any) before touching anything
# Trace the data flow: where does input come from? where does output go?
# Identify the blast radius: what else depends on this code?

# If there are no tests, the code IS the spec — treat changes with extra caution
```

### Step 2 — Add Characterization Tests (Lock Current Behavior)

```python
# Before changing legacy code, capture what it CURRENTLY does
# (even if the behavior is "wrong" — lock it first, then change deliberately)

def test_legacy_pricing_current_behavior():
    # Document the existing (quirky) behavior with a test
    result = legacy_calculate_price(quantity=3, base_price=10)
    assert result == 35   # current behavior: 3 * 10 + 5 mystery fee
    # NOW you can safely refactor — this test will tell you if behavior changes
```

**Why:** characterization tests turn "I'm afraid to touch this" into "I'll know immediately if I break it."

### Step 3 — Make Changes in Small, Verifiable Steps

```bash
# Small commits — each one shippable and testable
git commit -m "refactor: extract discount logic from legacy_calculate_price"
git commit -m "test: add coverage for discount edge cases"
git commit -m "feat: support tiered discounts in pricing"
# NOT one giant "rewrote the whole pricing module" commit
```

### Step 4 — Upgrade Dependencies Safely

```bash
# Check what's changing before upgrading
pip index versions django          # what versions exist?
# Read the changelog/migration guide — know the breaking changes

# Upgrade one major version at a time (not 2.x → 5.x in one jump)
pip install django==3.2            # was 2.2
pytest                             # fix breakage
# then 3.2 → 4.x → 5.x, testing at each step

# Security-critical upgrades take priority (known CVEs)
pip-audit                          # find vulnerable deps
```

### Step 5 — Feature Enhancement Without Breaking

```python
# Extend, don't rewrite — add new behavior alongside old where possible

# BAD: rewrite the module (high risk in legacy code)
# GOOD: add a new code path, deprecate the old gradually

def calculate_price(quantity, base_price, *, tier=None):
    if tier:                          # NEW behavior (opt-in)
        return calculate_tiered_price(quantity, base_price, tier)
    return legacy_calculate_price(quantity, base_price)  # OLD behavior unchanged
```

### Maintenance & Legacy Checklist

- [ ] **Understand before changing** — trace data flow, know the blast radius
- [ ] **Characterization tests** added before refactoring untested code
- [ ] **Small, verifiable commits** — each step shippable and testable
- [ ] **Dependencies upgraded incrementally** (one major version at a time)
- [ ] **Security upgrades prioritized** (known CVEs fixed promptly)
- [ ] **Extend, don't rewrite** — add new behavior alongside old where possible
- [ ] **Existing patterns followed** — match the codebase's conventions
- [ ] **Manual verification** for critical paths (tests may be sparse in legacy)
- [ ] **Deploy incrementally** — feature flags / staged rollout for risky changes

### Avoid These

- **Changing code you don't understand** — guaranteed breakage in legacy systems
- **Big-bang rewrites** — high risk, long-lived branches, merge hell
- **Skipping characterization tests** — no safety net for refactoring untested code
- **Upgrading multiple major versions at once** — impossible to isolate breakage
- **Ignoring the codebase's conventions** — inconsistency makes maintenance harder
- **"Cleanup" commits mixed with feature changes** — can't revert one without the other
- **No manual verification** — sparse tests in legacy mean you must verify by hand
- **Touching "don't know what it does" code without locking behavior first**
