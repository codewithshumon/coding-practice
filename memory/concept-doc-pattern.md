# Concept-Doc Pattern

> For **conceptual / architectural** topic docs (DSA, architecture, distributed systems, patterns, theory).
> Distinct from the **tool pattern** (`cloud-service-doc-pattern.md`), which is for tools with install/auth/code.
> Established by `case/structures-architecture/backend-systems.md` (Part 1: 7 backend/systems topics).

---

## Table of Contents

- [When to Use This vs the Tool Pattern](#when-to-use-this-vs-the-tool-pattern)
- [The Shared Shell](#the-shared-shell)
- [The 8-Section Concept Body](#the-8-section-concept-body)
- [Critical: Anchor Uniqueness](#critical-anchor-uniqueness)
- [Quick Checklist](#quick-checklist)

---

## When to Use This vs the Tool Pattern

| Content type | Pattern | Key signal |
|---|---|---|
| **Tool / library / CLI** (SDK, CDK, CLI) | **Tool pattern** (`cloud-service-doc-pattern.md`) | Has install, auth, code usage |
| **Concept / architecture / theory** (DSA, Distributed Systems, Clean Architecture) | **This pattern** | Abstract; "install" makes no sense |

The tool template's sections ("Installation & Setup", "Authentication") don't map to abstract concepts — use this 8-section concept template instead, keeping the same structural *shell*.

## The Shared Shell

(Identical to the tool pattern — only the body differs.)

- H1: `# <Category> — Complete Guide`
- Blockquote: series name, Part N, grows-over-time, upcoming topics.
- **Hierarchical TOC**: parent topic (bold) → nested numbered items; all clickable; parent → H1.
- **Continuous numbering** across the whole file (topic A = §1–8, B = §9–16, …).
- **Shared Orientation** hub near the top (one table: each topic → its core question + one-liner).
- **Shared Foundations** appendix + **Quick Reference Card** at the end.
- **File grouping**: related topics sharing themes → ONE combined file; unrelated → separate files.

## The 8-Section Concept Body

| # | Section | What goes in it |
|---|---|---|
| 1 | **What is X?** | Definition bullets + bold **One-liner:** |
| 2 | **Core Concepts** | Key building blocks/terms (table) |
| 3 | **How to Think About It** | Mental model / principles + **Rule of thumb:** |
| 4 | **Common Patterns & Techniques** | Concrete approaches |
| 5 | **When to Apply** | Real-system applicability |
| 6 | **Production Best Practices** | Tight one-line items |
| 7 | **Real-World Examples** | ~3–6: `### Example N — Title` + short code/diagram + `**Why:**` |
| 8 | **Common Pitfalls / Anti-Patterns** | Table: Pitfall / Symptom / Fix |

## Critical: Anchor Uniqueness

When a file holds many topics, each with the **same 8 section names** ("Core Concepts", "Best Practices", …), the auto-generated anchors **collide** — every "Core Concepts" becomes `#core-concepts`.

**Fix:** make every H3 title **descriptive and unique**:
- Embed the topic: `### 18. Consensus, Replication, and Partitioning`
- Use specific phrases: `### 27. Pagination, Rate Limiting, and Caching`
- Spell out **"and"** instead of **"&"** (the `&` becomes a double dash in the slug).

## Quick Checklist

```
□ # <Category> — Complete Guide
□ > Series / Part N / grows over time
□ ## Table of Contents (HIERARCHICAL: parent topics → nested numbered items)
□ ## Shared Orientation (table: topic → core question → one-liner)
□ Per topic (§n–n+7, continuous numbering):
    1. What is X?           (+ One-liner)
    2. Core Concepts        (table)
    3. How to Think About It (+ Rule of thumb)
    4. Common Patterns
    5. When to Apply
    6. Best Practices       (one-liners)
    7. Real-World Examples  (each with Why:)
    8. Pitfalls             (table)
    □ each H3 title UNIQUE (no anchor collisions)
□ ## Shared Foundations
□ ## Quick Reference Card (code block + golden rules)
□ --- + italic closing note
```
