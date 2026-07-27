# Apply Rendering Strategies

> **Category:** Application Development
> **Relevant at:** As-Sunnah Foundation
> **Related tech docs:** `case/framework/nextjs/app-router-and-rendering.md` (Rendering Strategies Part B §57–96), `case/web/web-quality.md` (Core Web Vitals §1–8, SEO §17–24)

---

## 1. What This Means

Rendering strategies control **when and how** a page's HTML is produced. Choosing the right strategy per page — SSR, SSG, ISR, Streaming, or PPR — directly affects performance, SEO, and user experience.

**Scope:**
- **SSR (Server-Side Rendering):** fresh HTML on every request — dynamic, SEO-friendly, per-request cost
- **SSG (Static Site Generation):** build-time HTML served from CDN — fastest, cheapest, fixed content
- **ISR (Incremental Static Regeneration):** SSG that refreshes periodically or on-demand — static speed + fresh data
- **Streaming:** HTML chunks sent progressively — faster perceived load via Suspense boundaries
- **PPR (Partial Prerendering):** static shell + streamed dynamic holes — best of both (experimental)

**Why it matters:** the wrong rendering strategy produces either stale content (SSG for fast-changing data), slow pages (SSR without streaming), or wasted compute (SSR for static content). The strategy is a **per-page decision**, not a per-app one.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**Matching strategy to content:**
- **Marketing pages, docs, blog?** → SSG (build once, CDN-fast)
- **Product catalog with hourly price updates?** → ISR (static speed, periodic refresh)
- **User dashboard with live data?** → SSR + Streaming (fresh, fast TTFB)
- **E-commerce product detail?** → ISR (mostly static, on-demand refresh after edit)
- **Mostly static page with a personalized widget?** → PPR (static shell cached, dynamic widget streamed)

**The Core Web Vitals connection:**
- SSR without streaming → bad **LCP** (user waits for all data)
- Streaming with Suspense → good **LCP** (shell arrives fast, details fill in)
- SSG/ISR from CDN → best **LCP** (edges near users)
- Layout shifts from late-loading content → bad **CLS** (reserve space)

**Real decision flow for a new page:**
1. Does the content change per user or per request? → SSR/Streaming
2. Does it change periodically but not per-request? → ISR
3. Does it rarely change? → SSG
4. Is it mostly static with small dynamic parts? → PPR (experimental)
5. Is there a slow data source blocking the page? → Add Streaming/Suspense

---

## 3. How to Implement

### SSR — Dynamic, Per-Request Rendering

```tsx
// No explicit config needed — dynamic APIs (cookies, headers, searchParams)
// make the page dynamically rendered
export default async function Dashboard() {
  const data = await fetchUserData();   // fresh per request
  return <UserView data={data} />;
}
```

### SSG — Build-Time, CDN-Served

```tsx
// Use generateStaticParams for dynamic routes
export async function generateStaticParams() {
  const posts = await fetch("/api/posts").then(r => r.json());
  return posts.map(p => ({ id: p.id }));
}

export default function Post({ params }) {
  // rendered at build time, served from CDN
  return <PostView params={params} />;
}
```

### ISR — Static + Background Refresh

```tsx
// Revalidate every 60 seconds — stale-while-revalidate
export const revalidate = 60;

export default async function Product({ params }) {
  const product = await fetch(`/api/products/${params.id}`).then(r => r.json());
  return <ProductView product={product} />;
}
```

**On-demand revalidation** (after a CMS edit or mutation):
```tsx
import { revalidateTag } from "next/cache";

export async function updateProduct() {
  await db.product.update(...);
  revalidateTag("products");   // instantly refresh all tagged pages
}
```

### Streaming — Progressive, Suspense-Boundary-Based

```tsx
import { Suspense } from "react";

export default function Page() {
  return (
    <div>
      <Header />                           {/* sent immediately */}
      <Suspense fallback={<Skeleton />}>
        <SlowDataSection />                {/* streamed when ready */}
      </Suspense>
    </div>
  );
}
```

**Why:** the user sees the shell (Header + Skeleton) immediately. The slow section fills in without blocking — better LCP and perceived performance.

### PPR — Static Shell + Dynamic Holes (experimental)

```tsx
// next.config.js: experimental.ppr = true

// The entire page is a static shell except:
<Suspense fallback={<Skeleton />}>
  <DynamicUserWidget />                    {/* streamed fresh per request */}
</Suspense>
```

### Strategy Picker

| Content pattern | Strategy | Config |
|---|---|---|
| Never changes | SSG | Default |
| Changes periodically | ISR | `export const revalidate = N` |
| Per-request fresh | SSR | Use dynamic APIs |
| Slow data on any page | + Streaming | Wrap in `<Suspense>` |
| Mostly static, small dynamic hole | PPR | `experimental.ppr = true` |

### Avoid These

- **SSR for static content** — wasted server compute on every request
- **SSG for fast-changing data** — pages serve stale content
- **No Suspense boundaries** — the whole page waits for the slowest data
- **Too-short ISR intervals** — effectively turns ISR into SSR (undermines the benefit)
- **PPR in production** without tracking experimental stability
- **Forgetting to reserve space** for streamed/late-loading content (CLS penalty)
