# Cloud-Service Doc Pattern

> Established by `case/cloud-service/aws.md` (AWS SDK doc — Part 1).
> Apply this structure to every new tech-topic doc in the series (AWS CDK, Lambda, DynamoDB, GCP, Azure, etc.).

---

## Table of Contents

- [The 7-Part Skeleton](#the-7-part-skeleton)
- [The 11-Section Body Template](#the-11-section-body-template)
- [Style Rules](#style-rules)
- [Anchor Gotcha](#anchor-gotcha)
- [Quick Template Checklist](#quick-template-checklist)

---

## The 7-Part Skeleton

Every doc must contain, in order:

1. **File & title**
   - Path: `case/cloud-service/<topic>.md` (lowercase filename).
   - H1: `# <Topic> — Complete Guide` (em-dash, "Complete Guide").
   - Blockquote (`>`) right after: series name, Part number, "file grows over time," upcoming topic names.

2. **Table of Contents — HIERARCHICAL, not flat**
   - `## Table of Contents`
   - Top-level bullet = bold **Topic Name** (parent).
   - Nested bullets = the numbered sections, each a clickable anchor link.
   - Parent links to the H1.
   - **Why hierarchical:** future topics (CDK, Lambda…) sit beside the first as siblings; items nest under their own topic.

3. **Fixed 11-section body** (numbered, see below).

4. **Quick Reference Card** — fenced code block: ASCII summary + ✓ checklist.

5. **Horizontal rule** `---`.

6. **Closing italic note** — "More sections/topics will be added over time."

7. **File grouping (IMPORTANT):** closely-related tools that **share concepts** (auth, regions, signing) go in **ONE combined file** with multiple parent topics in the TOC + a shared comparison hub at top. **Unrelated topics** get **separate files**. The AWS **SDK + CDK + CLI** trio is combined in `case/cloud-service/aws.md` (SDK=§1–11, CDK=§12–22, CLI=§23–33). Each tool gets a **distinct §2** comparing against its OWN alternatives so comparisons don't repeat.

**Generalizes beyond AWS (frontend libraries, etc.):** keep the 11-section *shape*, but swap §4 → **"Core API"** (table of hooks/functions) and §8 → **"Common Patterns"** (idioms). Exemplar: `case/state-management/react-state-management.md` (Redux Toolkit / Zustand / TanStack Query / Context API).

**Whole frameworks** (`case/framework/{django,fastapi,spring-boot,nestjs,expressjs}`): swap §4 → **"Core Concepts & Features"** (framework building blocks table), §8 → **"Project Structure & Configuration"**. Each framework = ONE comprehensive 11-section doc (unlike Next.js, which decomposes into many sub-topics because its App Router has distinct primitives).

**Databases** (`case/database/databases.md`): swap §4 → **"Data Model & Key Features"**, §8 → **"Connection & Authentication"**. A technique topic in the batch (e.g., Database Optimization) uses §7 → "Tools & Setup", §8 → "Measurement & Profiling". Keep the 11-section shape uniform; adapt §4/§7/§8 to the domain.

---

## The 11-Section Body Template

| # | Section | What goes in it |
|---|---|---|
| 1 | `## 1. What is X?` | Definition bullets + bold **One-liner:** summary. |
| 2 | `## 2. X vs alternatives` | Comparison table (Tool / Purpose / When It Runs / Example) + **Rule of thumb:** line. |
| 3 | `## 3. How Does It Work?` | Numbered step-by-step lifecycle; end with **Key point:** note. |
| 4 | `## 4. Available variants` | Table (Language-or-type / Name / Install) + short Notes. |
| 5 | `## 5. Where Should You Use It?` | Bullet list of use cases. |
| 6 | `## 6. Where NOT to Use It?` | Bullet list; each ends with `→ redirect to correct tool`. |
| 7 | `## 7. Installation & Setup` | bash install + code usage for TWO languages (Python + Node.js); close with `**Pattern:**` tip. |
| 8 | `## 8. Authentication / Config` | Numbered **priority chain** (first match wins) + **Golden rules:** bullets. |
| 9 | `## 9. Production Best Practices` | Numbered list (10–14 items), each ONE tight line. |
| 10 | `## 10. Real-World Examples` | ~6 examples: `### Example N — Title (stack)` + fenced code + `**Why:**` line. |
| 11 | `## 11. Common Pitfalls` | Table: Pitfall / Symptom / Fix. |

---

## Style Rules

- **Short but complete** — every point tight yet self-explanatory.
- Em-dash (`—`) in headings and "Rule of thumb"/"Key point" lines.
- Tables for comparisons and pitfalls.
- Dual-language code coverage (Python + Node.js) for setup and examples.
- Bold inline key terms; `❌` / `✅` / `✓` markers where they add clarity.
- Every example ends with a `**Why:**` line.

## Anchor Gotcha

GitHub-style anchors are auto-generated from heading text: lowercase, spaces→`-`, punctuation stripped/converted to `-`.
- `# AWS SDK — Complete Guide` → `#aws-sdk--complete-guide` (note the **double** dash from the em-dash).
- Always verify TOC links match the generated slug.

## Input-vs-Ask Mismatch Rule

If a pasted input describes tool **A** but the user asks about tool **B**:
- Document what they asked for (**B**).
- Add a short comparison section so the two aren't confused.
- (Example: CDK was pasted → SDK doc was written, with a "SDK vs CDK vs CLI" section.)

---

## Quick Template Checklist

```
□ # <Topic> — Complete Guide
□ > Series / Part N / grows over time
□ ## Table of Contents  (HIERARCHICAL: parent topic → nested numbered items)
□ §1  What is X?           (+ One-liner)
□ §2  X vs alternatives     (table + Rule of thumb)
□ §3  How Does It Work?     (steps + Key point)
□ §4  Available variants    (table + Notes)
□ §5  Where to use it
□ §6  Where NOT to use it   (→ redirects)
□ §7  Installation & Setup  (Python + Node.js, + Pattern tip)
□ §8  Auth / Config         (priority chain + Golden rules)
□ §9  Production Best Practices (10–14 one-liners)
□ §10 Real-World Examples   (~6, each with Why:)
□ §11 Common Pitfalls       (table)
□ ## Quick Reference Card   (code block + ✓ checklist)
□ --- + italic closing note
```
