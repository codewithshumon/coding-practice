# Frontend Interview — Questions & Answers

> Built from your own `case/` study notes and `experience/` playbooks.
> Your headline stack: **React, Next.js 13+ (App Router), TypeScript, TanStack Query, Playwright/Cypress** (As-Sunnah Foundation), with full-stack breadth (NestJS, FastAPI, Django, AWS) from Codixel, Impressive Security, Eicra Soft, and MVI Solutions.

**How to use this file:** Answers are written the way you'd say them out loud. The ⭐ marks the questions most likely to be asked. The last section has the numbers you must memorize.

---

## Table of Contents

1. [About You / Intro Questions](#1-about-you--intro-questions)
2. [React Core & Server Components](#2-react-core--server-components)
3. [Next.js App Router & Rendering Strategies](#3-nextjs-app-router--rendering-strategies)
4. [State Management](#4-state-management)
5. [API Integration & Data Fetching](#5-api-integration--data-fetching)
6. [Performance & Core Web Vitals](#6-performance--core-web-vitals)
7. [Frontend Security](#7-frontend-security)
8. [Accessibility (WCAG) & SEO](#8-accessibility-wcag--seo)
9. [Testing & Code Quality](#9-testing--code-quality)
10. [TypeScript & JavaScript Essentials](#10-typescript--javascript-essentials)
11. [Frameworks Beyond React (Angular, patterns)](#11-frameworks-beyond-react-angular-patterns)
12. [Behavioral / Experience Questions](#12-behavioral--experience-questions)
13. [Numbers & Facts Cheat Sheet](#13-numbers--facts-cheat-sheet)

---

## 1. About You / Intro Questions

### Q1. ⭐ Tell me about yourself.

> "I'm a frontend-focused engineer whose core stack is **React, Next.js with the App Router, and TypeScript**. At As-Sunnah Foundation I owned rendering-strategy decisions per page — SSG, ISR, SSR with streaming — built with Server Components by default and small interactive Client Component islands. I also owned Core Web Vitals, accessibility, frontend security, and the test suites.
>
> Before that I built full-stack systems: a high-throughput financial events platform at Codixel on AWS, travel-booking and payment integrations at Impressive Security with NestJS, a multi-tenant B2B eCommerce SaaS at Eicra Soft with ERP connectors, and Django maintenance at MVI Solutions. That backend breadth makes me a better frontend developer — I understand API contracts, caching, and security from both sides of the wire."

### Q2. ⭐ Walk me through a recent project you're proud of.

Use the As-Sunnah Foundation Next.js work:

> "At As-Sunnah Foundation I worked on a content-heavy Next.js App Router site where performance and SEO directly drive reach. The key decisions I owned:
> - **Per-page rendering strategy** — marketing and content pages were static (SSG) or ISR with a `revalidate` window; personalized or live pages used SSR with Streaming and Suspense boundaries.
> - **Server Components by default** — data fetching happened server-side with zero client JS; interactivity like buttons and forms were small `'use client'` islands.
> - **Server Actions for mutations** — forms worked even without JavaScript, with `revalidatePath`/`revalidateTag` refreshing the UI after writes.
> - **Quality metrics** — image dimensions to prevent layout shift, preloaded hero images for LCP, lazy-loaded routes, and accessibility to WCAG AA.
>
> The litmus test I used: open the Network tab — if every component ships a JS bundle, the server/client boundary is too high."

### Q3. Why do you like React / what makes a good frontend developer?

> "React's server/client boundary model in the App Router lets me ship the minimum JavaScript necessary. But what makes a good frontend developer is thinking in **user-centric quality**: performance measured on real users (Core Web Vitals), accessibility as a requirement not a feature, and semantic HTML as the foundation that benefits screen readers, search engines, and speed at the same time."

---

## 2. React Core & Server Components

### Q4. ⭐ What are React Server Components (RSC)?

> "Server Components render **exclusively on the server and ship zero client-side JavaScript**. They can be `async`, so they can `await` data directly — fetch from a database or API — without `useEffect`. They **cannot** use hooks, state, effects, event handlers, or browser APIs. The server sends a serialized payload (not component code) to the browser, and Client Components hydrate as interactive islands. In the Next.js App Router, **components are Server Components by default**."

### Q5. ⭐ What are Client Components and when do you use them?

> "Client Components are opted into with the `'use client'` directive. They support hooks, state, effects, event handlers, refs, and browser APIs like `window` and `localStorage`. Key detail people miss: **Client Components are still server-rendered initially** — the server pre-renders their HTML for fast first paint and SEO, then React hydrates them in the browser. `'use client'` enables hydration, not client-only rendering.
>
> I use them for: interactivity (buttons, inputs), browser APIs, and client-only libraries like charts or rich text editors. Best practice is to **push `'use client'` as deep in the tree as possible**, because everything a client component imports counts toward the client bundle."

### Q6. ⭐ What are hydration and hydration mismatches?

> "Hydration is React attaching event handlers and state to server-rendered HTML so it becomes interactive. A hydration mismatch happens when the server-rendered HTML and the client's first render disagree — classic causes are reading `window`/`localStorage` or the current time during render. I prevent them by keeping first renders deterministic and moving browser-dependent logic into `useEffect`."

### Q7. How do you decide the server/client boundary in a page?

> "Default to Server Components and carve out **client islands** for interactivity. Example: a blog post page is one Server Component that fetches the post; the Like button inside it is a small Client Component receiving serializable props. Rules I follow:
> - Pass server-fetched data down as **serializable props** (strings, numbers, arrays, plain objects) — never re-fetch on the client what the server already fetched.
> - Keep heavy libraries server-side when possible.
> - Code-split large client components with `dynamic()`.
>
> The Network tab is the litmus test — if everything ships JS, the boundary is wrong."

### Q8. ⭐ What are Server Actions?

> "Server Actions are async functions that run **on the server**, invoked directly from components — marked with `'use server'`. They collapse the form → fetch → API route → mutation → refetch chain into one function. Used with `<form action={createPost}>` they give **progressive enhancement — the form works without JavaScript**. After a mutation I call `revalidatePath` or `revalidateTag` to refresh the affected UI.
>
> Rules: they must be async, return serializable data, **validate input server-side** (never trust the client), and check authorization. I use Server Actions for form mutations and Route Handlers for public HTTP endpoints and webhooks."

### Q9. What are Route Handlers in Next.js?

> "`route.ts` files that define API endpoints using the web-standard `Request`/`Response` objects — the App Router replacement for `pages/api`. You export named HTTP methods (GET, POST, etc.), and they can run on the **Edge or Node.js runtime**. I use them for REST endpoints for non-React clients, webhook receivers like Stripe, and streaming responses like SSE or AI token streams. For form mutations inside my own app, I prefer Server Actions."

### Q10. What is Next.js Middleware and when would you use it?

> "Middleware runs **before a request completes, at the edge** — defined in `middleware.ts` with a `matcher` limiting which paths it runs on. I use it for auth gating (redirect to `/login` if no session cookie on `/dashboard/:path*`), i18n rewrites, and A/B testing. Rules: keep it minimal and fast since it runs on every matched request — **no database queries or heavy work**, and always set a `matcher` so it doesn't run on static assets."

### Q11. Explain the key React hooks you use daily.

> - `useState` — local UI state.
> - `useEffect` — synchronizing with external systems; **not** for data fetching (that's TanStack Query or server components).
> - `useReducer` — complex state transitions paired with Context.
> - `useMemo` — memoizing expensive derivations (and Context provider values to prevent over-rendering).
> - `useRef` — mutable values that don't trigger re-renders, and DOM access.
> - Custom hooks — extracting reusable logic like a `useChat` WebSocket hook."

---

## 3. Next.js App Router & Rendering Strategies

### Q12. ⭐ Explain SSR vs SSG vs ISR vs Streaming — and when you'd use each.

> "**Rendering is a per-page decision, not a per-app decision.**
>
> - **SSG** — HTML generated at **build time**, served from a CDN. Fastest and cheapest, zero per-request compute. For marketing pages, docs, blogs — content known at build time.
> - **SSR** — HTML rendered on the server **per request**. For personalized, per-user, or always-fresh data: dashboards, authenticated views.
> - **ISR** — static pages **regenerated in the background** on an interval (`export const revalidate = 60`) or on demand (`revalidateTag`/`revalidatePath`). Static speed with fresh data. For catalogs, blogs with CMS updates — I'd use on-demand revalidation after a CMS edit.
> - **Streaming** — the server sends the shell immediately and streams slow sections wrapped in `<Suspense>` as they resolve. Improves TTFB and perceived performance. For pages where one slow query shouldn't block the whole page.
>
> There's also **PPR (Partial Prerendering)** — a static prerendered shell with streamed dynamic 'holes' — but it's still **experimental**, so I'd evaluate stability before production."

### Q13. ⭐ How does ISR's stale-while-revalidate work exactly?

> "First request serves the static page. Once the page is older than its `revalidate` window, the next request still gets the **stale page immediately** while regeneration runs **in the background**; subsequent requests get the fresh version. So users never wait for a rebuild. Pitfalls: too-long windows serve stale data, too-short windows effectively become SSR. And after mutations like a CMS edit, on-demand `revalidateTag` beats waiting for the window."

### Q14. ⭐ How do the App Router file conventions work?

> "Folder structure equals URL structure. The conventions:
> - `page.tsx` — the route UI, makes the route public
> - `layout.tsx` — shared wrapper that **nests and persists** across navigations
> - `loading.tsx` — Suspense fallback (it *is* Suspense under the hood)
> - `error.tsx` — error boundary per route
> - `not-found.tsx` — 404 UI
> - `route.ts` — API endpoint (Route Handler)
> - `[param]` dynamic segments, `(group)` route groups that organize without affecting the URL, `@slot` parallel routes, `[...slug]` catch-all.
>
> I add `loading.tsx`/`error.tsx` for every meaningful route and colocate non-route files next to the feature."

### Q15. How does rendering strategy affect Core Web Vitals?

> "Directly. **SSG/ISR served from CDN gives the best LCP. SSR without streaming hurts LCP and TTFB** because the server waits for all data before sending anything. **Streaming with Suspense** sends the shell early → good LCP. Heavy hydration hurts **INP** — the fix is less client JS, smaller islands. **CLS** comes from late-loading content without reserved space — always set image/video dimensions and reserve space for ads and dynamic content."

### Q16. What's the difference between the App Router and the old Pages Router? What about React Router?

> "The App Router (Next.js 13+) is file-system based with **Server Components by default**, nested layouts, and built-in loading/error states. The Pages Router is the legacy model. Mixing both in one app causes double-routing problems.
>
> **React Router** is the client-side router for React apps *outside* Next.js — Vite SPAs. With v6.4+ the data router (`createBrowserRouter`) adds **loaders and actions**, which are like client-oriented Server Actions. Best practices there: lazy-load route components, use `<Link>` never `<a>`, per-route loading/error states. For an SPA where SEO matters, I'd reach for Next.js instead since client-only rendering is poor for SEO."

---

## 4. State Management

### Q17. ⭐ How do you decide which state management tool to use?

> "The master distinction is **client state vs server state — they're different problems with different tools**:
> - **API/server data → TanStack Query.** It handles caching, background refetching, retries, and invalidation. Never mirror API responses into a client store.
> - **Theme, locale, current user, feature flags → Context API.** Low-frequency config values.
> - **Minimal global UI state for small–medium apps → Zustand.**
> - **Complex interdependent client state in a large-team app → Redux Toolkit**, when you need structure, time-travel debugging, and action logging.
>
> Most real apps **combine** them: TanStack Query for server state + Zustand or Redux for client state + Context for config. And the golden rule: don't use Redux for a toggle — pick the lightest tool that fits."

### Q18. ⭐ Explain TanStack Query in depth.

> "TanStack Query is the standard library for **server state** — fetching, caching, synchronizing, and updating remote data. It replaces the `useEffect` + `useState` + manual-cache boilerplate.
>
> Key concepts:
> - **Query keys** — the cache is keyed hierarchically, like `['users', 'list', { page }]`, which lets you invalidate a whole group: `invalidateQueries(['users'])`.
> - **staleTime** — how long data is considered fresh (e.g. `staleTime: 60_000`); stale data triggers background refetch while the user sees cached data instantly.
> - **Mutations + invalidation** — after a write, invalidate affected queries so reads refresh.
> - **Optimistic updates** — in `onMutate`: cancel outgoing queries, snapshot previous cache with `getQueryData`, write the optimistic value with `setQueryData`, and **roll back in `onError`** using the snapshot.
> - **Prefetching** on hover or route-enter, and `useInfiniteQuery` for infinite scroll.
>
> Pitfalls I avoid: weak/random query keys (cache collisions), forgetting invalidation (stale UI), storing client state in the query cache, and over-fetching with too-low staleTime."

### Q19. Compare Redux Toolkit, Zustand, and Context.

> "**Redux Toolkit** — single store, unidirectional flow, `createSlice` auto-generates actions and uses **Immer** so 'mutating' code produces immutable updates. `createAsyncThunk` handles pending/fulfilled/rejected. Best for large apps and teams needing predictability and time-travel debugging. Always normalize state as `{ [id]: entity }` for O(1) lookups, and use `createSelector` for memoized derived state.
>
> **Zustand** — a hook-based store with **no providers, no actions, no boilerplate**. State and updates live together via `set`/`get`. **Always subscribe with selectors** (`useStore(s => s.x)`) — subscribing to the whole store re-renders on any change. `persist` middleware gives you localStorage in one line; `devtools` plugs into Redux DevTools.
>
> **Context** — built-in, zero install, for **low-frequency** values (theme, auth, locale). The catch: **every consumer re-renders when the value changes**, so I memoize the provider value with `useMemo` and split contexts by concern. High-frequency state in Context causes re-render storms."

### Q20. What's the biggest state management anti-pattern?

> "**Mirroring server data into client state.** If you copy API responses into Redux/Zustand, you're hand-building a cache — stale data, manual refetch triggers, sync bugs. That's TanStack Query's job. The client store should hold only what the server doesn't know: UI toggles, form drafts, selections."

---

## 5. API Integration & Data Fetching

### Q21. ⭐ How do you choose between REST, GraphQL, WebSockets, and SSE?

> "By interaction model, not habit:
> - **REST** — CRUD, public APIs, widest compatibility, HTTP-cacheable. Default.
> - **GraphQL** — complex relational data where REST causes over/under-fetching; one request fetches user + orders + order items that would take 3+ REST round-trips. Multiple clients needing different shapes.
> - **WebSockets** — **bidirectional** real-time: chat, collaborative editing, presence. Needs an HTTP upgrade handshake, then full-duplex frames.
> - **SSE** — **one-way server→client push** over plain HTTP: notifications, live feeds, progress updates. `EventSource` has **built-in auto-reconnect with `Last-Event-ID`**, and it passes proxies easily. Gotchas: HTTP/1.1 limits concurrent streams per browser (use HTTP/2), and proxy buffering needs disabling.
>
> Common mistake: using WebSockets for one-way push — SSE is simpler and purpose-built for that."

### Q22. ⭐ How do you handle WebSocket reliability on the frontend?

> "Three things: **heartbeat ping/pong** to drop dead connections, **client reconnection with exponential backoff**, and **authenticating during the handshake** (token on connect). On the server side, scaling needs a pub/sub broker like Redis because sockets are per-server. And I always design the UI for connection loss — queued messages and a connection indicator."

### Q23. What does your frontend API layer look like?

> "It has four responsibilities:
> 1. **Data fetching with caching and dedup** — TanStack Query with structured keys and tuned `staleTime`.
> 2. **Optimistic updates with rollback** on failure.
> 3. **Loading/error/empty states on every data-dependent component** — no silent failures.
> 4. **Real-time sync without polling** where it matters.
>
> Anti-patterns I avoid: `useEffect` + `useState` for every call, blocking renders on slow APIs (stream/defer with Suspense instead), and WebSockets for simple fetching where caching and retries are actually harder."

### Q24. How do you integrate third-party frontend services (analytics, payment UIs, maps, chat widgets)?

> "Treat them as **unreliable and slow — isolate them so they can't break my core page**. I lazy-load them, handle their failures gracefully (the page works if the widget doesn't), and keep their integration behind a thin wrapper so swapping vendors doesn't touch business components. Same principle as the backend adapter pattern."

### Q25. REST best practices you expect from an API you consume?

> "Nouns not verbs (`/orders`, not `/getOrders`), correct status codes (never 200 for errors), **versioning from day one** (`/v1/`), pagination on every list — **cursor over offset** for large data, and idempotency keys on writes so retries are safe. Consistent error shapes like `{ data, error, meta }`. When I work backend-side I hold APIs to the same standard — I've built and maintained versioned APIs at Codixel and Eicra."

---

## 6. Performance & Core Web Vitals

### Q26. ⭐ What are the Core Web Vitals and their thresholds?

> "Three user-centric metrics from Google, measured on **real users** (Chrome UX Report, p75):
> - **LCP (Largest Contentful Paint)** — loading; when the largest visible element renders. **Good ≤ 2.5s.**
> - **INP (Interaction to Next Paint)** — interactivity; tracks every click/tap/keypress latency. **Good ≤ 200ms.** It **replaced FID in 2024**.
> - **CLS (Cumulative Layout Shift)** — visual stability. **Good ≤ 0.1.**
>
> 'Needs improvement' bands: LCP ≤ 4s, INP ≤ 500ms, CLS ≤ 0.25. Core Web Vitals are a **Google ranking signal**, and the trap I always call out: a good Lighthouse lab score with poor real-user experience — measure CrUX/RUM, not just the lab."

### Q27. ⭐ How do you optimize each vital?

> "**LCP** — minimize server response, optimize/resize the hero image (webp/avif), and **preload the hero**: `<link rel="preload" as="image" fetchPriority="high">`. SSG/ISR from CDN gives the best LCP; streaming the shell early helps SSR.
>
> **INP** — ship less JavaScript: Server Components by default, small client islands, route-level `dynamic()` lazy loading, tree-shaking (`import { debounce } from 'lodash-es'`, never the whole library). Break long tasks with `scheduler.yield()`.
>
> **CLS** — **always set width/height on images and videos** (`<img src="/hero.webp" width={1200} height={600}>`), reserve space for ads and late-loading content, beware font swaps."

### Q28. ⭐ Tell me about a performance problem you solved.

Backend-flavored but impressive — deliver it as full-stack breadth:

> "My go-to debugging rule is **measure first, never guess**. On one system, an endpoint sat at **3.2s p95**. I profiled instead of guessing: distributed tracing showed **82% of the request time was in the database**, cache lookup was only 3%. The query filtered by status and date range over tenants with >10,000 orders and had no matching index. I added a composite index on `(tenant_id, status, created_at)` and p95 dropped from **3200ms to 4ms**. The lesson generalizes to frontend too — trace where time actually goes, optimize the dominant stage, and verify with before/after numbers.
>
> Other examples from the same playbook: eliminating an N+1 that fired **101 queries down to 2** with `prefetch_related`, and caching expensive report aggregations with a TTL, which **cut DB load ~90%**."

### Q29. How do bundle size and rendering connect to user experience?

> "They compound: **smaller bundle → faster load (LCP) and snappier interaction (INP); streaming → faster LCP; semantic HTML → better SEO and accessibility; image dimensions → zero CLS** — high Core Web Vitals → better search ranking → more users. That's why I treat performance, accessibility, and SEO as one discipline, not three."

### Q30. What caching layers affect a frontend app?

> "Nearest to farthest from the user: **Browser cache → CDN edge → application in-memory → distributed cache like Redis → database cache**. Done right, most requests never reach the origin. On the HTTP side that's `Cache-Control` headers and ETags; static assets on **S3 + CloudFront** is the classic pattern. The hard part is never storing data — it's **invalidating** it correctly, which is why everything gets a TTL and mutations trigger explicit revalidation (`revalidateTag` on the Next.js side)."

---

## 7. Frontend Security

### Q31. ⭐ How do you handle authentication securely in a React/Next.js app?

> "**OAuth 2.0 Authorization Code flow with PKCE** — never the deprecated Implicit flow. The PKCE verifier lives in `sessionStorage`, the challenge goes in the request.
>
> For tokens, I keep the **access token in an HttpOnly, Secure, SameSite cookie** — `localStorage` is readable by any XSS script. Short-lived access tokens (e.g., `Max-Age=3600`) plus **refresh-token rotation**, revoked on logout."

### Q32. ⭐ Where do you store JWTs and why?

> "HttpOnly cookie, not localStorage — **localStorage tokens are stealable by XSS**. Also worth knowing: a JWT's payload is **base64-encoded, not encrypted** — anyone can read it, so no secrets in claims. Always set `exp`, prefer **RS256** (asymmetric — services verify with a public key) over sharing one HS256 secret everywhere, and validate signature, expiry, issuer, and audience."

### Q33. ⭐ How do you prevent XSS and CSRF?

> "**XSS** — React escapes by default, so the danger is `dangerouslySetInnerHTML` and similar raw HTML injection: that content goes through **DOMPurify** first. Defense in depth with a **Content-Security-Policy** (`default-src 'self'; script-src 'self'; object-src 'none'`) so even a successful injection can't load external scripts — plus HSTS and `X-Content-Type-Options` via `next.config.js` headers.
>
> **CSRF** — `SameSite` cookies plus a **double-submit token** (`X-CSRF-Token` header matching a cookie value)."

### Q34. Is hiding a button real authorization?

> "No — **hiding the button is UX, not security**. The client is presentation; **the server is the authority**. I enforce authorization per request in Server Components and Server Actions (e.g., `getCurrentUser()` and `notFound()` gating in the admin page), and on the API with scope checks. Also: `NEXT_PUBLIC_` env vars are public by definition — **no secrets in client code, ever** — and dependencies get audited (`npm audit`)."

### Q35. What is CORS and how do you handle it?

> "CORS is the browser's cross-origin policy — it's configured on the **server**, restricting which origins may call the API. The cardinal sin is `Access-Control-Allow-Origin: *` combined with credentials, which is a real security hole. I allow-list explicit origins. When I've owned the API side (Impressive Security), I set CORS deliberately at the gateway/middleware — which makes debugging it from the frontend much faster."

---

## 8. Accessibility (WCAG) & SEO

### Q36. ⭐ What are the WCAG basics you apply?

> "Target **WCAG 2.1 AA**. The **POUR principles**: Perceivable (alt text, captions, contrast), Operable (keyboard navigation, no traps, visible focus), Understandable (predictable behavior, clear errors), Robust (semantic HTML that works with assistive tech).
>
> In practice: **native elements over div hacks** — a real `<button type="submit">` is focusable, keyboard-activatable, and screen-reader-aware; `<div onClick>` is none of those. Color contrast **≥ 4.5:1 for normal text, 3:1 for large text**. Meaningful alt text (empty alt for decorative images). I test with keyboard only plus a screen reader (NVDA/VoiceOver), because **automated tools like axe and Lighthouse only catch ~30%** of issues."

### Q37. Why does accessibility matter?

> "Roughly **15–20% of people have a disability**, it's legally required in many markets (ADA, Section 508, the European Accessibility Act), and it overlaps with SEO and quality — semantic HTML and alt text serve screen readers *and* crawlers."

### Q38. ⭐ How do you approach SEO as a frontend developer?

> "Search engines work in four steps: **crawl → index → rank → serve** — if a bot can't crawl or index the page, it doesn't exist. My checklist:
> - **Technical**: crawlable pages, sitemap, `robots.txt`, HTTPS, canonical URLs (`<link rel="canonical">` consolidates duplicate variants like `?color=blue`), mobile-friendly, and Core Web Vitals as a ranking signal.
> - **On-page**: unique descriptive title tags and meta descriptions, **one h1 with hierarchical headings**, semantic HTML, keyword placement, alt text.
> - **Rendering**: SSR/SSG/ISR so content exists in HTML — client-only rendering is invisible to crawlers.
>
> Next.js metadata API handles most of this, and I verify with Search Console."

---

## 9. Testing & Code Quality

### Q39. ⭐ Describe your testing strategy for frontend code.

> "**Test pyramid** — lots of fast unit tests for business logic, integration tests for how components talk to APIs/state, and a thin layer of E2E for critical flows.
>
> - Unit + integration run in CI in ~2 minutes and **block PR merges**; E2E (Playwright/Cypress, ~10 minutes) runs on merge to main.
> - Every production bug gets a **regression test**.
> - **Flaky tests get fixed immediately** — flakiness erodes trust in the whole suite; quarantine if needed.
> - Test business logic, edge cases, error paths, and critical flows like checkout — not getters, framework internals, or coverage for its own sake. **90% coverage with bugs still shipping** means you're testing the wrong things.
>
> With Playwright I write TypeScript specs — `page.goto`, `fill`, `expect(locator).toBeVisible()` — robust role/`data-testid` selectors, never brittle CSS, and I let auto-waiting work instead of fixed sleeps."

### Q40. What do you look for in code review?

> "Review is a quality gate, not a rubber stamp. Automated checks (lint, format, `tsc --noEmit`, tests) handle the mechanical stuff; humans focus on **correctness, design, maintainability, security, and tests**. Feedback explains *why* and suggests alternatives — that's how juniors learn standards. A merge is a commitment to maintain that code forever. I keep PRs small and reviewable; 1000-line PRs can't actually be reviewed."

### Q41. How do you keep code quality high day to day?

> "Write for the next reader — code is read far more often than it's written. Small focused functions, honest names (`fetchActiveUsers`, not `getData`), guard clauses over deep nesting, dependencies injected so code is testable, comments that explain **why** not what. Clarity first, performance second — and the boy-scout rule plus a dedicated fraction of each sprint (around 20%) for paying down debt before it compounds."

---

## 10. TypeScript & JavaScript Essentials

### Q42. ⭐ Why TypeScript for frontend work?

> "Type safety catches a whole class of bugs at compile time instead of in production, makes refactoring safe in a growing codebase, and types double as documentation. It's non-negotiable in my stack — I run `tsc --noEmit` as a CI gate. I've also used it heavily backend-side with Node/NestJS at Eicra and Impressive Security."

### Q43. Explain the event loop briefly.

> "JavaScript is **single-threaded with an asynchronous event loop**. Sync code runs to completion; async callbacks/timers/promises wait in queues and run when the stack clears. That's why **CPU-bound work blocks everything** — long tasks freeze interaction (this is literally what INP punishes), so I break up long tasks and keep heavy computation off the main thread."

### Q44. Common async pitfalls you avoid?

> "Unawaited promises and floating error handling; `Promise.all` failing fast when I wanted partial success (`allSettled`); race conditions from stale responses — with TanStack Query's cache and cancellation this mostly disappears; and sequential awaits that should be parallel."

---

## 11. Frameworks Beyond React (Angular, Patterns)

### Q45. How does React compare to Angular and Vue?

> "**React** is a flexible UI library — I bring my own routing/state/tooling. **Angular** is an opinionated, TypeScript-first full platform: dependency injection, RxJS reactivity, routing, forms, HTTP out of the box — a steep learning curve, great for large enterprise teams that want conventions enforced. **Vue** is a progressive framework in between, with gentle adoption and granular reactivity. I pick by team and problem: enterprise SPA with enforced structure → Angular; flexible app of any size → React; gradual adoption → Vue."

### Q46. What do you know about Angular's performance model? (if asked)

> "Angular is **zone-based change detection** by default, so the wins are: **`OnPush`** change detection (skip CD unless inputs/references change), **Signals** (v16+) for fine-grained reactivity, **`trackBy` with `*ngFor`** to avoid re-rendering whole lists, **lazy-loaded routes** (`loadComponent`/`loadChildren`), AOT compilation, and unsubscribing observables — the `async` pipe auto-unsubscribes, or `takeUntilDestroyed()`. RxJS leaks from missing unsubs are the classic memory bug."

### Q47. Explain MVVM and where you've seen it.

> "Model–View–ViewModel: the ViewModel exposes model data via **data binding**, so the view updates automatically without explicit update code — **two-way binding**. It's the model behind Angular's `[(ngModel)]`, Vue's `v-model` (Knockout.js was the original JS MVVM library), WPF, SwiftUI. Compared to MVP, where a Presenter explicitly tells a passive View what to render, MVVM lets the binding framework do it — less boilerplate when the framework supports it. Pitfalls I know to avoid: bloated ViewModels, complex binding expressions, and **subscription leaks**."

### Q48. Which design patterns do you actually use in frontend work?

> "- **Observer/Pub-Sub** — RxJS, event handling, React's state→render notification.
> - **Adapter** — wrapping third-party services (Stripe behind a `PaymentGateway` interface) so vendors can swap without touching business code.
> - **Strategy** — interchangeable algorithms: validation rules, pricing rules.
> - **Factory** — creating the right component/service per input.
> - **Dependency Injection** — decoupling and testability; built into Angular and NestJS.
> - **Repository** — the data-access layer behind interfaces so tests mock it.
>
> The rule: patterns compose, match them to the actual complexity — don't force MVVM or a repository layer onto a simple page."

---

## 12. Behavioral / Experience Questions

> These are grounded in your real experience docs. Deliver in STAR flow: Situation → Task → Action → Result.

### Q49. ⭐ Tell me about working with designers or PMs.

> "I collaborate **contract-first and early**. With backend, we agree the API contract (`POST /api/v1/orders` request/response) before either side builds — **I mock it immediately** and keep building while they implement. With designers, I've pushed back constructively with alternatives — e.g., 'that animation is GPU-heavy on mobile; here's a lighter version with the same feel,' or 'this layout needs 3 API calls — we can pre-fetch to keep it snappy.' With QA I coordinate on critical paths like checkout, payment, and login using feature flags and staging."

### Q50. ⭐ Tell me about a time you handled a production issue.

> "My rule is **two phases: mitigate first, diagnose second** — don't debug while users suffer.
>
> One incident: alerts fired on error rate > 5%. We were paged, and within minutes executed the rollback (blue/green redeploy) — service restored before diagnosis even started. Root cause via 5-Whys: a new query lacked an index, so DB queries hit 30-second timeouts; why did it ship? No query review in the PR; why? No DB-migration check in CI. So the fix had three parts — the code fix, a regression test, and a systemic change: an `EXPLAIN ANALYZE` check in CI. **Fix the system, not the person** — blameless postmortems."

### Q51. Tell me about debugging something difficult.

> "I follow a hypothesis-driven method: **define → decompose → hypothesize → investigate → verify → fix → learn**. Define precisely — what/when/where/how much/expected behavior; if you can't state the problem clearly, you don't understand it yet. Form specific, testable hypotheses instead of shotgun debugging. Example: an endpoint at 3.2s p95 affecting ~200 users/hour — hypothesis 'missing composite index for the status + date filter', confirmed with `EXPLAIN ANALYZE`, fixed (3200ms → 4ms), verified no regressions. Also caught a race condition that way — concurrent updates deadlocking — fixed with a row lock. The difference between senior and junior isn't just knowledge, it's approach."

### Q52. ⭐ Tell me about working on a distributed/async team.

> "At Eicra Soft I worked async with US-based Solutions Architects. The discipline that made it work: **written-first** — specs reviewed async before code, self-contained PR descriptions (What/Why/How/Testing/**before-after UI screenshots**), reviewing the other timezone's PRs first thing in my morning, and flagging blockers **before** end-of-day — a vague question costs a full day in round trips, so I batch questions with context and what I've already tried."

### Q53. Tell me about mentoring or knowledge sharing.

> "I treat code review as teaching — instead of 'wrong, use a repository,' explaining *why* the repository pattern helps and offering to pair. Pair programming with driver/navigator swaps every 20–30 minutes, narrating my thinking so the process transfers. Short 15-minute walkthroughs of documented patterns and public Slack Q&A so answers compound. And psychological safety: normalizing not-knowing, separating the person from the mistake, sharing my own."

### Q54. Tell me about a technical decision you owned.

> "I record decisions as **ADRs — Architecture Decision Records** — context, decision, consequences, and the alternatives I rejected. Example from my notes: choosing event-driven messaging between order and billing via SQS with DLQs, having rejected synchronous calls for their coupling. I also keep a **tech-debt register** and protect roughly **20% of every sprint** to pay it down, and I invest in DX — fast CI, one-command local setup, automated lint/format — because feedback in minutes instead of 20 changes everything."

### Q55. Tell me about handling legacy code.

> "At MVI Solutions I maintained old, undocumented codebases. My method: **understand → add characterization tests that pin current behavior** (even the quirky parts — a test documenting '3 × 10 + 5 mystery fee' is documentation) → change in small steps → test each → deploy incrementally. **Extend, don't rewrite** — new opt-in code paths alongside unchanged legacy behavior; big-bang rewrites are the anti-pattern. Security-critical upgrades (known CVEs, `npm audit`/`pip-audit`) jump the queue. Most professional engineering is maintenance, not greenfield."

### Q56. How do you gather and act on user feedback?

> "Both directions. Reactive: Sentry for client-side JS errors, alerts on error rate > 1% or p99 > 2s, and a triage framework — P0 data loss/security → fix now; P1 broken core feature → this sprint; P2 workaround exists → next sprint; P3 cosmetic → backlog. Proactive: behavioral analytics (Mixpanel/Amplitude) — drop-off funnels and **rage clicks** told us a form needed inline validation and auto-save; RUM tracks real-user Core Web Vitals. Feature rollouts go 1% → 10% → 50% → 100% with automated rollback."

### Q57. How do you communicate with clients or non-technical stakeholders?

> "A trust stack: reliability, transparency, competence, empathy. Working demos over slide decks — a 10-minute clickable demo beats 30 minutes of slides, and I let the client drive it. For bad news there's a formula: say it early, state the impact, own it, present the plan, explain how recurrence is prevented. Translate jargon ('we'll add caching' → 'pages will load faster because we stop repeating expensive work'), and under-promise, over-deliver."

### Q58. Why should we hire you / what's your biggest strength?

> "I combine **frontend depth with full-stack context**. On the frontend I own the modern Next.js stack end-to-end — rendering strategy, state, performance, accessibility, security, testing. And because I've built the backend side too — versioned APIs, caching layers, queues, AWS — I don't throw issues over a wall; I understand the whole request path, from browser cache through CDN to database, and I debug with measurement instead of guesses."

### Q59. What's a weakness? (honest, with progress)

> Pick one that fits the material, e.g.:

> "I've historically leaned toward backend-measurable problems because metrics there are crisp — so I've deliberately pushed myself to bring the same measurement discipline to frontend quality: real-user Core Web Vitals, accessibility audits, and analytics-driven UX fixes instead of shipping what 'feels fast.'"

### Q60. Do you have questions for us? (ask these)

> - "How do you measure frontend quality — do you track Core Web Vitals on real users, and who owns them?"
> - "What's the server/client boundary philosophy — Server Components by default, or is the codebase mostly client-side?"
> - "How much of the API contract does the frontend team shape, and is there contract mocking in the workflow?"
> - "What does the test pyramid actually look like here — do E2E tests gate merges or run post-merge?"
> - "How do design and frontend collaborate — design system, shared component library?"

---

## 13. Numbers & Facts Cheat Sheet

Memorize these — interviewers probe for exact values:

| Fact | Value |
|---|---|
| LCP good / needs improvement | ≤ 2.5s / ≤ 4s |
| INP good / needs improvement | ≤ 200ms / ≤ 500ms (**replaced FID in 2024**, p75 of all interactions) |
| CLS good / needs improvement | ≤ 0.1 / ≤ 0.25 |
| WCAG contrast (AA) | 4.5:1 normal text, 3:1 large text |
| WCAG target | 2.1 AA |
| People with disabilities | ~15–20% |
| Automated a11y coverage (axe/Lighthouse) | ~30% — rest is manual |
| App Router introduced | Next.js 13 |
| Angular standalone / Signals | v14+ / v16+ |
| React Router data router (loaders/actions) | v6.4+ |
| ISR example | `export const revalidate = 60` (stale-while-revalidate) |
| TanStack Query staleTime example | 60_000 (1 min) |
| JWT structure | header.payload.signature — **base64, NOT encrypted** |
| Token cookie example | HttpOnly, Secure, SameSite, Max-Age=3600 |
| OAuth for SPAs/browser | Authorization Code + **PKCE** (Implicit is deprecated) |
| CSP example | `default-src 'self'; script-src 'self'; object-src 'none'` |
| Perf war stories | index fix 3200ms→4ms p95; N+1 101→2 queries; cache cut DB load ~90% |
| CI timing | unit+integration ~2 min (blocks merge), E2E ~10 min (on merge) |
| Codixel platform | "hundreds of events daily", single-digit-ms APIs |
| PPR status | experimental |

---

*Sources: `case/` study notes (react-state-management, web-quality, app-router-and-rendering, angular, apis-and-communication, security-and-auth, caching, design-patterns, media-processing, aws, cloud-platforms) and `experience/` playbooks (all five companies). Good luck — you know this material.*
