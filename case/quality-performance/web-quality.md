# Performance & Quality — Complete Guide

> **Series:** Web Quality Documentation — Part 1
> This file covers the three core **web quality disciplines**: Core Web Vitals (user-centric performance), WCAG (accessibility), and SEO (search visibility). Related: `framework/nextjs/app-router-and-rendering.md` covers rendering strategies that directly affect these metrics; `structures-architecture/backend-systems.md` §41–56 covers backend-side performance and system optimization. More topics (Lighthouse, A11y auditing, SEO tooling) will be added later.

---

## Table of Contents

- [Shared Orientation — The Three Pillars of Web Quality](#shared-orientation--the-three-pillars-of-web-quality)
- **Core Web Vitals**
  - [1. What Are Core Web Vitals?](#1-what-are-core-web-vitals)
  - [2. CWV vs Raw Performance Metrics](#2-cwv-vs-raw-performance-metrics)
  - [3. LCP, INP, and CLS](#3-lcp-inp-and-cls)
  - [4. Core Web Vital Thresholds](#4-core-web-vital-thresholds)
  - [5. When Core Web Vitals Matter](#5-when-core-web-vitals-matter)
  - [6. Core Web Vitals Best Practices](#6-core-web-vitals-best-practices)
  - [7. Core Web Vitals Examples](#7-core-web-vitals-examples)
  - [8. Core Web Vitals Pitfalls](#8-core-web-vitals-pitfalls)
- **WCAG (Accessibility)**
  - [9. What Is WCAG?](#9-what-is-wcag)
  - [10. WCAG vs Other Accessibility Standards](#10-wcag-vs-other-accessibility-standards)
  - [11. The POUR Principles](#11-the-pour-principles)
  - [12. WCAG Conformance Levels](#12-wcag-conformance-levels)
  - [13. When Accessibility Matters](#13-when-accessibility-matters)
  - [14. WCAG Best Practices](#14-wcag-best-practices)
  - [15. WCAG Real-World Examples](#15-wcag-real-world-examples)
  - [16. WCAG Pitfalls](#16-wcag-pitfalls)
- **SEO**
  - [17. What Is SEO?](#17-what-is-seo)
  - [18. SEO vs Paid Search vs Social](#18-seo-vs-paid-search-vs-social)
  - [19. How Search Engines Work](#19-how-search-engines-work)
  - [20. Core SEO Techniques](#20-core-seo-techniques)
  - [21. When SEO Matters](#21-when-seo-matters)
  - [22. SEO Best Practices](#22-seo-best-practices)
  - [23. SEO Real-World Examples](#23-seo-real-world-examples)
  - [24. SEO Pitfalls](#24-seo-pitfalls)
- [Shared Foundations](#shared-foundations)
- [Quick Reference Card](#quick-reference-card)

---

## Shared Orientation — The Three Pillars of Web Quality

These three disciplines answer different quality questions, and they reinforce each other:

| Pillar | Question | One-liner |
|---|---|---|
| **Core Web Vitals** | Is the experience *fast and stable*? | Google's user-centric performance metrics |
| **WCAG (Accessibility)** | Can *everyone* use it? | International web accessibility standards |
| **SEO** | Can search engines *find and rank* it? | Visibility in search results |

**How they reinforce each other:**
- **CWVs (performance) boosts SEO** — Google uses CWVs as a ranking signal. A fast, stable page ranks higher.
- **Accessibility aids SEO** — semantic HTML, alt text, and proper structure help both screen readers and search bots.
- **All three converge on the same goal:** a fast, inclusive, discoverable web experience.

**Rule of thumb:** you can't have good SEO without good performance; you can't claim a quality product without accessibility. These aren't optional add-ons — they are web quality.

---

# Core Web Vitals

## 1. What Are Core Web Vitals?

**Core Web Vitals (CWV)** are Google's standardized set of **user-centric metrics** measuring real-world web experience: **loading speed** (LCP), **interactivity** (INP), and **visual stability** (CLS).

**One-liner:** Google's three user-centric metrics for real web quality.

## 2. CWV vs Raw Performance Metrics

| | Core Web Vitals | Raw metrics (load time, TTFB) |
|---|---|---|
| Focus | User experience | Technical speed |
| Examples | LCP, INP, CLS | Load time, TTFB, requests |
| Measured | Real users (Chrome UX Report) | Lab, synthetic |

**Key point:** CWV measures **what users actually experience**, not just what a profiler shows. A fast server with poor layout shift still fails.

## 3. LCP, INP, and CLS

| Metric | Measures | Good threshold |
|---|---|---|
| **LCP** (Largest Contentful Paint) | Loading — when the largest visible element appears | ≤ 2.5s |
| **INP** (Interaction to Next Paint) | Interactivity — responsiveness to user actions | ≤ 200ms |
| **CLS** (Cumulative Layout Shift) | Visual stability — how much things move around | ≤ 0.1 |

**LCP** (replaced FID in 2024): tracks the largest piece of content (hero image, text block) becoming visible.
**INP** (replaced FID): tracks the **latency of every interaction** (clicks, taps, keypresses) and uses the p75 worst.
**CLS**: tracks unexpected layout shifts (ads loading late, images without dimensions).

## 4. Core Web Vital Thresholds

| Rating | LCP | INP | CLS |
|---|---|---|---|
| **Good** | ≤ 2.5s | ≤ 200ms | ≤ 0.1 |
| **Needs improvement** | ≤ 4s | ≤ 500ms | ≤ 0.25 |
| **Poor** | > 4s | > 500ms | > 0.25 |

**Key point:** these are **real-user** thresholds from the Chrome UX Report, not synthetic lab measurements. Both matter, but CWV = real users.

## 5. When Core Web Vitals Matter

- **SEO** — Google uses CWVs as a **ranking signal**. Poor CWVs hurt search visibility.
- **User experience + conversion** — slow/shaky pages lose users and sales.
- **Responsive, image-heavy pages** — where LCP and CLS are common issues.

## 6. Core Web Vitals Best Practices

1. **Optimize LCP** — minimize server response, optimize images (format/size), preload the hero.
2. **Optimize INP** — reduce JS work on interaction, avoid long tasks, split heavy code.
3. **Eliminate CLS** — always include **width/height** on images/videos; reserve space for ads/dynamic content.
4. **Measure real user data** (CrUX, RUM), not just lab (Lighthouse).
5. **Monitor continuously** — changes to rendering/fetching can silently degrade CWVs.

## 7. Core Web Vitals Examples

### Example 1 — LCP Win: Preload Hero Image
**Why:** `link rel="preload"` on the hero image makes it start loading immediately — often the biggest LCP gain.

### Example 2 — CLS Fix: Image Dimensions
```html
<!-- Bad: image loads late, pushes content -->
<img src="hero.jpg">
<!-- Good: space reserved, no shift -->
<img src="hero.jpg" width="1200" height="600">
```
**Why:** the browser reserves space before the image loads — zero layout shift.

### Example 3 — INP Win: Break a Long Task
**Why:** split a 200ms JS function into smaller async pieces — interaction latency stays under the INP threshold.

## 8. Core Web Vitals Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Only measuring lab (Lighthouse) | Good lab score, poor real UX | Add real-user monitoring |
| No image dimensions | CLS when images load | Always set width/height |
| Late-loading ads/fonts | CLS surprise | Reserve space |
| Oversized images | Bad LCP | Optimize + serve appropriate sizes |
| Ignoring INP | Good LCP, sluggish feel | Reduce JS, split long tasks |

---

# WCAG (Accessibility)

## 9. What Is WCAG?

**WCAG (Web Content Accessibility Guidelines)** are internationally recognized standards for making web content accessible to people with disabilities — covering **perceivable, operable, understandable, and robust** principles.

**One-liner:** the global standard for web accessibility.

## 10. WCAG vs Other Accessibility Standards

| | WCAG | Section 508 (US) | ADA |
|---|---|---|---|
| Scope | Global web standard | US federal procurement | US anti-discrimination law |
| Technical | Detailed success criteria | References WCAG | Legal, not technical |

**Rule of thumb:** **WCAG 2.1 AA** is the common compliance target — it satisfies most legal and practical requirements globally.

## 11. The POUR Principles

| Principle | What it means | Examples |
|---|---|---|
| **Perceivable** | Users must be able to *sense* the content | Text alternatives (alt), captions, color contrast |
| **Operable** | Users must be able to *use* the interface | Keyboard navigation, enough time, focus order |
| **Understandable** | Users must be able to *comprehend* the info and UI | Readable text, predictable behavior, error suggestions |
| **Robust** | Content must work with *assistive tech* | Valid semantic HTML, ARIA where needed |

**Key point:** POUR is the organizing framework — every WCAG success criterion maps to one of these principles.

## 12. WCAG Conformance Levels

| Level | What it means | Example |
|---|---|---|
| **A** | Minimum | No keyboard traps, alt text for images |
| **AA** | Standard (the common target) | Color contrast ≥ 4.5:1, focus visible |
| **AAA** | Strictest | Sign language for audio, contrast ≥ 7:1 |

**Rule of thumb:** target **AA** for broad compliance; AAA is aspirational for most sites.

## 13. When Accessibility Matters

- **Legal compliance** — many jurisdictions require WCAG AA (ADA, Section 508, EAA).
- **Broadest audience** — ~15-20% of people have a disability.
- **Universal good practices** — keyboard nav, semantic HTML, and clear text help everyone.
- SEO bonus — semantic structure aids both screen readers and search crawlers.

## 14. WCAG Best Practices

1. **Semantic HTML** — use native elements (`button`, `a`, `input`) over generic `div`+hacks.
2. **Keyboard accessibility** — every interactive element navigable by keyboard.
3. **Color contrast** — AA minimum: 4.5:1 for normal text, 3:1 for large text.
4. **Alt text** for all meaningful images.
5. **Focus indicators** — always visible.
6. **Test with screen readers** (NVDA, VoiceOver) and keyboard only.
7. **Automated checks** (axe, Lighthouse) catch ~30%; manual testing catches the rest.

## 15. WCAG Real-World Examples

### Example 1 — Accessible Button
```html
<!-- Bad: div click doesn't work for keyboard/screen readers -->
<div onClick={handler}>Submit</div>
<!-- Good: native button works for everyone -->
<button type="submit">Submit</button>
```
**Why:** a `button` is focusable, keyboard-activatable, and screen-reader-aware — for free.

### Example 2 — Image with Alt Text
```html
<img src="chart.png" alt="Quarterly revenue: $2.4M in Q1, up 15% from Q4">
```
**Why:** screen readers convey the chart's meaning; search engines index the alt text.

## 16. WCAG Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Divs as buttons | Keyboard-inaccessible, no screen-reader role | Use native elements |
| No focus indicators | Keyboard users lost | Visible focus outline |
| Low contrast | Unreadable for low-vision | 4.5:1 minimum |
| Missing or generic alt text | "image" or empty alt on meaningful images | Descriptive alt on meaningful; empty on decorative |
| Relying only on color | Colorblind users miss info | Add icons/labels alongside color |

---

# SEO

## 17. What Is SEO?

**SEO (Search Engine Optimization)** is the set of practices to improve a website's **visibility and ranking** in search engine results — through **technical, on-page, and off-page** optimizations.

**One-liner:** make your site findable in search results.

## 18. SEO vs Paid Search vs Social

| | SEO | Paid (PPC) | Social |
|---|---|---|---|
| Cost | Time/effort (organic) | Pay per click | Time/effort |
| Duration | Long-term, compounding | Stops when payment stops | Ephemeral |
| Traffic type | Intent-based (searching) | Intent-based (searching) | Interest-based (browsing) |

**Rule of thumb:** SEO = **organic, sustainable, intent-driven** traffic — free after the effort. The three main types: **Technical SEO** (site structure, speed), **On-Page SEO** (content, keywords, meta), and **Off-Page SEO** (backlinks, authority).

## 19. How Search Engines Work

1. **Crawl** — bots follow links and discover pages.
2. **Index** — pages are parsed and stored.
3. **Rank** — indexed pages are scored (relevance + authority + UX signals).
4. **Serve** — results are returned for a query.

**Key point:** if a bot can't crawl or index your page, it doesn't exist to the search engine. Technical SEO is the foundation for everything else.

## 20. Core SEO Techniques

| Category | Techniques |
|---|---|
| **Technical** | `robots.txt`, sitemaps, canonical URLs, HTTPS, Core Web Vitals, mobile-friendly |
| **On-Page** | Title tags, meta descriptions, heading hierarchy, semantic HTML, keyword placement, alt text |
| **Off-Page** | Quality backlinks, citations, social signals |
| **Content** | Quality, relevance, freshness, E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) |

## 21. When SEO Matters

- Any site wanting **organic search traffic**.
- **Content-driven** sites (blogs, docs, e-commerce).
- Pages with **public, indexable** content.

## 22. SEO Best Practices

1. **Technical SEO first** — crawlable, fast, mobile-friendly, HTTPS.
2. **Semantic HTML** — proper headings, landmarks, meaningful structure.
3. **Descriptive, unique** title tags and meta descriptions.
4. **Optimize images** — format, size, alt text.
5. **Canonical URLs** to consolidate duplicate content.
6. **Monitor in Search Console** — check indexing, CWVs, and manual actions.

## 23. SEO Real-World Examples

### Example 1 — A Crawlable Page
```html
<title>Widget Pro - Best Widgets for Developers</title>
<meta name="description" content="Widget Pro offers durable..." />
<h1>Widget Pro</h1>
<img src="widget.jpg" alt="Widget Pro model X in matte black" />
```
**Why:** search bots can find, parse, and understand this page — title + h1 + alt text = a well-signaled page.

### Example 2 — Canonical Avoids Duplicate
```html
<link rel="canonical" href="https://site.com/product" />
```
**Why:** `site.com/product?color=blue` tells the bot it's the same page — no duplicate penalty.

## 24. SEO Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Blocked by robots.txt | Not indexed | Allow crawling |
| No sitemap | Crawled slowly/missed pages | Submit sitemap |
| Duplicate content | Split rankings | Canonical URLs |
| Doorway/cloaking tactics | Penalties, de-indexing | Don't manipulate — build quality |
| Slow/broken mobile | Poor ranking | Mobile-first, optimize CWVs |

---

## Shared Foundations

Concepts that recur across **all three quality disciplines**:

- **Quality is user-centric** — CWVs measure real user experience; WCAG ensures all users; SEO optimizes for real searchers. None are about gaming tools or benchmarks.
- **Semantic HTML benefits all three** — proper structure improves accessibility (screen readers), SEO (crawlers), and indirectly performance (lighter markup).
- **Performance and SEO are tightly linked** — Core Web Vitals are a Google ranking signal; better CWVs → better rankings → more users who benefit from WCAG.
- **Measurement is essential** — you can't improve what you don't measure: CWVs (CrUX/Lighthouse), WCAG (axe/screen readers), SEO (Search Console/Analytics).
- **They compound** — a fast (CWV), accessible (WCAG), crawlable (SEO) page wins on all three axes simultaneously.

## Quick Reference Card

```
THREE PILLARS:
  Core Web Vitals → is it fast and stable?  (LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1)
  WCAG            → can everyone use it?     (Target AA: POUR principles)
  SEO             → can they find it?        (Crawlable, relevant, authoritative)

HOW THEY REINFORCE:
  Fast (CWVs)    → ranks higher (SEO)
  Accessible     → semantic HTML → ranks higher (SEO)
  Findable (SEO) → more users → more value from CWVs + accessibility efforts

CWV QUICK FIXES:
  LCP → optimize images, preload hero, reduce server time
  INP → reduce JS, split long tasks, avoid expensive event handlers
  CLS → image dimensions, reserve space for dynamic content

WCAG QUICK FIXES (AA):
  ✓ Semantic HTML (natives over divs)  ✓ Keyboard accessible
  ✓ Color contrast ≥ 4.5:1           ✓ Alt text on images
  ✓ Visible focus indicators          ✓ Test with a screen reader

SEO QUICK FIXES:
  ✓ Crawlable (robots.txt + sitemap)  ✓ Semantic HTML (headings, alt)
  ✓ Unique title + meta description   ✓ Canonical URLs
  ✓ Fast + mobile-friendly (CWVs)     ✓ Monitor Search Console
```

---

*This file covers the three web-quality pillars. More topics (Lighthouse deep-dive, accessibility auditing, SEO tooling, Core Web Vital monitoring) will be added as separate files in this series over time.*
