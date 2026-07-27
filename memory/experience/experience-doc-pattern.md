# Experience-Doc Pattern

> For **professional experience / responsibility** topic docs in `experience/<category>/*.md`.
> Distinct from the tool pattern (`cloud-service-doc-pattern.md`) and concept pattern (`concept-doc-pattern.md`), which are for technical reference.
> Established by `experience/application-development/` and `experience/api-development/` (10 files across 2 categories).

---

## Table of Contents

- [When to Use This vs the Case Patterns](#when-to-use-this-vs-the-case-patterns)
- [Category and File Structure](#category-and-file-structure)
- [The 3-Section Template](#the-3-section-template)
- [Cross-Referencing to Case](#cross-referencing-to-case)
- [Style Rules](#style-rules)
- [Quick Checklist](#quick-checklist)

---

## When to Use This vs the Case Patterns

| Content type | Pattern | Key signal |
|---|---|---|
| **Technical reference** (SDK, database, protocol) | Tool or concept pattern (`case/`) | "What is X? How does it work?" |
| **Professional experience** (responsibility, skill) | **This pattern** (`experience/`) | "What did I do? How do I implement it in production?" |

The experience pattern answers a different question: not "what is this technology?" but **"how do I actually perform this responsibility in a production environment?"**

## Category and File Structure

```
experience/
└── <category-kebab-case>/
    ├── <responsibility-1>.md
    ├── <responsibility-2>.md
    └── ...
```

- **One category folder per skills section** (matching skills.md's sections).
- **One file per responsibility item** within that section.
- **Kebab-case filenames** describing the responsibility: `scalable-applications.md`, `third-party-integration.md`, `domain-systems.md`.
- Categories built so far: `application-development/`, `api-development/`.

## The 3-Section Template

Every file follows this exact structure:

### Header Block

```markdown
# <Responsibility Title>

> **Category:** <Category Name>
> **Relevant at:** <Company> (<context>), <Company> (<context>)
> **Related tech docs:** `case/<path>.md` (section §N–M), ...
```

### Section 1 — What This Means

- **Definition** — 1-2 sentences defining the responsibility
- **Scope** — bullet list: what's included and what's not
- **Why it matters** — 1 sentence on the production consequence

### Section 2 — Real-World Production Application

- How this plays out **day-to-day** in real systems
- **Per-company context** where relevant (each company used it differently)
- **Tradeoffs and real decisions** — not just ideal-scenario advice
- **Litmus tests** — a concrete question that tells you if you're doing it right

### Section 3 — How to Implement

- **Concrete code** — actual implementation patterns with language-tagged code blocks
- **Decision frameworks** — tables or flowcharts (when to use which approach)
- **Checklists** — `- [ ]` items for production readiness
- **Avoid These** — a bullet list of anti-patterns with their consequences

## Cross-Referencing to Case

Every file links to relevant `case/` docs in its header. The link format:

```
> **Related tech docs:** `case/structures-architecture/architecture-patterns.md` (Microservices §1–8), `case/api/apis-and-communication.md` (Third-Party Integrations §49–56)
```

**Rule:** cross-reference the specific **sections** (§N–M) that are relevant, not just the file. This makes `experience/` and `case/` work as a pair — experience answers "how I used it," case answers "what it is."

## Style Rules

- **Action-oriented** — focus on *doing*, not *describing*. Every section has actionable content.
- **Production realism** — tradeoffs and failure modes are as important as best practices. Don't present idealized scenarios.
- **Code-driven** — §3 always includes real code patterns with language tags, not just pseudocode.
- **Company attribution** in header only — the body talks about the *pattern*, not "I did this at X." Companies provide context; the implementation advice is universal.
- **Checklists close every §3** — `- [ ]` items make the advice testable.
- **Avoid These is always the last subsection** — anti-patterns are the capstone, not an afterthought.

## Quick Checklist

```
□ Header block:
     # <Title>
     > Category / Relevant at / Related tech docs
□ §1 What This Means:
     Definition + Scope + Why it matters
□ §2 Real-World Production Application:
     Day-to-day reality + per-company context + tradeoffs + litmus test
□ §3 How to Implement:
     Concrete code + decision frameworks + checklist + Avoid These
□ Cross-references to case/ docs (specific sections, §N–M)
□ Kebab-case filename matching the responsibility
```
