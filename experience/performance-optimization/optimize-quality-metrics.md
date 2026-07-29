# Optimize for Quality Metrics

> **Category:** Performance & Optimization
> **Relevant at:** As-Sunnah Foundation
> **Related tech docs:** `case/web/web-quality.md` (Core Web Vitals §1–8, WCAG §9–16, SEO §17–24), `case/framework/nextjs/app-router-and-rendering.md` (Rendering Strategies §57–96)

---

## 1. What This Means

Optimizing for quality metrics means tuning the **frontend** for measurable user-experience and discoverability outcomes — **Core Web Vitals** (LCP/INP/CLS), **SEO**, **accessibility (WCAG)**, **bundle size**, and **rendering performance**.

**Scope:**
- **Core Web Vitals** — LCP (loading), INP (interactivity), CLS (visual stability) — Google's real-user metrics
- **SEO** — crawlability, semantic structure, meta, technical SEO
- **Accessibility (WCAG)** — semantic HTML, keyboard nav, contrast, screen-reader support
- **Bundle size** — shipping less JavaScript to the browser
- **Rendering performance** — SSR/SSG/Streaming choices, avoiding layout thrash

**Why it matters:** these aren't separate concerns — they reinforce each other. Fast pages (CWV) rank higher (SEO); semantic HTML helps both accessibility and crawlers; smaller bundles improve INP and LCP. A page that's fast, accessible, and discoverable wins on all axes.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**How the metrics connect:**
```
Smaller bundle  → faster load (LCP) + snappier interaction (INP)
  + Streaming (Suspense) → faster LCP (shell arrives early)
  + Semantic HTML        → better SEO + accessibility
  + Image dimensions     → no CLS (no layout shift)
  = High CWV scores → better SEO ranking → more users
```

**Real-world optimizations:**
- **LCP:** preload the hero image, optimize image format/size, reduce server response time
- **INP:** reduce JS work on interaction, split long tasks, code-split heavy components
- **CLS:** always set image/video dimensions, reserve space for ads/dynamic content
- **Bundle size:** tree-shake, lazy-load routes, avoid importing entire libraries
- **SEO:** semantic headings, unique title/meta, canonical URLs, sitemap, crawlable content
- **Accessibility:** native elements over divs, keyboard navigation, color contrast ≥ 4.5:1

**The measurement reality:**
- **CWV = real users** (Chrome UX Report), not just lab (Lighthouse) — both matter
- **Accessibility** — automated tools (axe, Lighthouse) catch ~30%; manual screen-reader/keyboard testing catches the rest
- **SEO** — verified via Search Console (indexing, CWV, manual actions)

---

## 3. How to Implement

### Core Web Vitals — LCP / INP / CLS

```tsx
// LCP: preload the hero image so it loads immediately
<head>
  <link rel="preload" as="image" href="/hero.webp" fetchPriority="high" />
</head>

// CLS: always set dimensions — the browser reserves space before load
<img src="/hero.webp" width={1200} height={600} alt="..." />
// (No dimensions → image loads late → content shifts → CLS penalty)

// INP: break long tasks so interactions stay responsive
// Heavy synchronous work blocks interaction; split it
async function processItems(items) {
  for (const item of items) {
    doWork(item);
    await scheduler.yield();   // let the event loop handle interactions
  }
}

// LCP via Streaming: send the shell fast, defer slow data
<Suspense fallback={<Skeleton />}>
  <SlowDataSection />   {/* streamed in, doesn't block the shell */}
</Suspense>
```

### Bundle Size

```tsx
// Lazy-load routes — don't ship everything upfront
const Settings = dynamic(() => import("./Settings"), {
  loading: () => <Skeleton />,
});

// Avoid importing entire libraries — import what you use
import { debounce } from "lodash-es";   // tree-shakeable, not `import _ from "lodash"`
```

### SEO — Semantic + Technical

```tsx
// Semantic structure helps crawlers AND screen readers
<article>
  <h1>Q3 Earnings Report</h1>           {/* one h1, hierarchical headings */}
  <section>
    <h2>Revenue</h2>
    <p>...</p>
  </section>
</article>

// Unique title + meta per page (Next.js metadata API)
export const metadata = {
  title: "Q3 Earnings Report — Acme",
  description: "Acme's Q3 revenue reached $2.4B...",
};
// Canonical to avoid duplicate-content penalty
<link rel="canonical" href="https://site.com/reports/q3" />
```

### Accessibility (WCAG AA)

```tsx
// Native elements — keyboard-accessible + screen-reader-aware for free
<button type="submit">Submit</button>   // not <div onClick={...}>

// Alt text on meaningful images (also helps SEO)
<img src="chart.png" alt="Q3 revenue: $2.4B, up 15% from Q2" />

// Visible focus indicators (CSS) — keyboard users need to see where they are
// Color contrast ≥ 4.5:1 (normal text), ≥ 3:1 (large text)
```

### Quality Metrics Checklist

- [ ] **CWV measured on real users** (CrUX/RUM), not just lab (Lighthouse)
- [ ] **LCP ≤ 2.5s** — preload hero, optimize images, reduce server time
- [ ] **INP ≤ 200ms** — split long tasks, reduce JS, code-split
- [ ] **CLS ≤ 0.1** — image dimensions, reserve space for dynamic content
- [ ] **Bundle size** tracked — lazy-load routes, tree-shake, audit deps
- [ ] **Semantic HTML** — proper headings, landmarks, native elements
- [ ] **WCAG AA** — keyboard nav, contrast ≥ 4.5:1, alt text, focus visible
- [ ] **SEO basics** — unique title/meta, canonical, sitemap, crawlable
- [ ] **Accessibility tested** with a screen reader + keyboard (not just automated)
- [ ] **Rendering strategy** chosen per page (SSG/ISR/SSR/Streaming)

### Avoid These

- **Only measuring lab (Lighthouse)** — good lab score, poor real UX
- **No image dimensions** — CLS when images load late
- **Late-loading ads/fonts** without reserved space — layout shift
- **Oversized images** — bad LCP; serve appropriate sizes/formats (webp/avif)
- **Divs as buttons** — keyboard-inaccessible, no screen-reader role
- **Low contrast** — unreadable for low-vision users
- **Shipping entire libraries** — bloated bundle hurts LCP and INP
- **Generic alt text** ("image") — meaningless to screen readers and crawlers
