# Next.js App Router & Rendering — Complete Guide

> **Series:** Next.js / Frontend Documentation — Part 1
> This file holds the **App Router building blocks** (routing, components, actions, handlers, middleware) and the **rendering strategies** (SSR, SSG, ISR, Streaming, PPR). More topics (data fetching, caching, deployment) will be added as separate files later.

---

## Table of Contents

- [Shared Orientation — The Next.js Mental Model](#shared-orientation--the-nextjs-mental-model)
- **Part A — App Router Building Blocks**
  - [1. What Is the Next.js App Router?](#1-what-is-the-nextjs-app-router)
  - [2. App Router File Conventions](#2-app-router-file-conventions)
  - [3. How App Router Routing Works](#3-how-app-router-routing-works)
  - [4. App Router Patterns](#4-app-router-patterns)
  - [5. When to Use the App Router](#5-when-to-use-the-app-router)
  - [6. App Router Best Practices](#6-app-router-best-practices)
  - [7. App Router Examples](#7-app-router-examples)
  - [8. App Router Pitfalls](#8-app-router-pitfalls)
  - [9. What Are React Server Components?](#9-what-are-react-server-components)
  - [10. The Server Component Model](#10-the-server-component-model)
  - [11. How Server Components Work](#11-how-server-components-work)
  - [12. Server Component Patterns](#12-server-component-patterns)
  - [13. When to Use Server Components](#13-when-to-use-server-components)
  - [14. Server Component Best Practices](#14-server-component-best-practices)
  - [15. Server Component Examples](#15-server-component-examples)
  - [16. Server Component Pitfalls](#16-server-component-pitfalls)
  - [17. What Are Client Components?](#17-what-are-client-components)
  - [18. The Client Component Model](#18-the-client-component-model)
  - [19. How Client Components Work](#19-how-client-components-work)
  - [20. Client Component Patterns](#20-client-component-patterns)
  - [21. When to Use Client Components](#21-when-to-use-client-components)
  - [22. Client Component Best Practices](#22-client-component-best-practices)
  - [23. Client Component Examples](#23-client-component-examples)
  - [24. Client Component Pitfalls](#24-client-component-pitfalls)
  - [25. What Are Server Actions?](#25-what-are-server-actions)
  - [26. The Server Action Model](#26-the-server-action-model)
  - [27. How Server Actions Work](#27-how-server-actions-work)
  - [28. Server Action Patterns](#28-server-action-patterns)
  - [29. When to Use Server Actions](#29-when-to-use-server-actions)
  - [30. Server Action Best Practices](#30-server-action-best-practices)
  - [31. Server Action Examples](#31-server-action-examples)
  - [32. Server Action Pitfalls](#32-server-action-pitfalls)
  - [33. What Are Route Handlers?](#33-what-are-route-handlers)
  - [34. The Route Handler Model](#34-the-route-handler-model)
  - [35. How Route Handlers Work](#35-how-route-handlers-work)
  - [36. Route Handler Patterns](#36-route-handler-patterns)
  - [37. When to Use Route Handlers](#37-when-to-use-route-handlers)
  - [38. Route Handler Best Practices](#38-route-handler-best-practices)
  - [39. Route Handler Examples](#39-route-handler-examples)
  - [40. Route Handler Pitfalls](#40-route-handler-pitfalls)
  - [41. What Is Next.js Middleware?](#41-what-is-nextjs-middleware)
  - [42. The Middleware Model](#42-the-middleware-model)
  - [43. How Middleware Works](#43-how-middleware-works)
  - [44. Middleware Patterns](#44-middleware-patterns)
  - [45. When to Use Middleware](#45-when-to-use-middleware)
  - [46. Middleware Best Practices](#46-middleware-best-practices)
  - [47. Middleware Examples](#47-middleware-examples)
  - [48. Middleware Pitfalls](#48-middleware-pitfalls)
  - [49. What Is React Router?](#49-what-is-react-router)
  - [50. React Router Core Concepts](#50-react-router-core-concepts)
  - [51. How React Router Works](#51-how-react-router-works)
  - [52. React Router Patterns](#52-react-router-patterns)
  - [53. When to Use React Router](#53-when-to-use-react-router)
  - [54. React Router Best Practices](#54-react-router-best-practices)
  - [55. React Router Examples](#55-react-router-examples)
  - [56. React Router Pitfalls](#56-react-router-pitfalls)
- **Part B — Rendering Strategies**
  - [57. What Is Server-Side Rendering?](#57-what-is-server-side-rendering)
  - [58. How SSR Differs From Other Strategies](#58-how-ssr-differs-from-other-strategies)
  - [59. How SSR Works](#59-how-ssr-works)
  - [60. SSR Patterns](#60-ssr-patterns)
  - [61. When to Use SSR](#61-when-to-use-ssr)
  - [62. SSR Best Practices](#62-ssr-best-practices)
  - [63. SSR Examples](#63-ssr-examples)
  - [64. SSR Pitfalls](#64-ssr-pitfalls)
  - [65. What Is Static Site Generation?](#65-what-is-static-site-generation)
  - [66. SSG vs Other Rendering Strategies](#66-ssg-vs-other-rendering-strategies)
  - [67. How SSG Works](#67-how-ssg-works)
  - [68. SSG Patterns](#68-ssg-patterns)
  - [69. When to Use SSG](#69-when-to-use-ssg)
  - [70. SSG Best Practices](#70-ssg-best-practices)
  - [71. SSG Examples](#71-ssg-examples)
  - [72. SSG Pitfalls](#72-ssg-pitfalls)
  - [73. What Is Incremental Static Regeneration?](#73-what-is-incremental-static-regeneration)
  - [74. ISR vs SSG vs SSR](#74-isr-vs-ssg-vs-ssr)
  - [75. How ISR Works](#75-how-isr-works)
  - [76. ISR Patterns](#76-isr-patterns)
  - [77. When to Use ISR](#77-when-to-use-isr)
  - [78. ISR Best Practices](#78-isr-best-practices)
  - [79. ISR Examples](#79-isr-examples)
  - [80. ISR Pitfalls](#80-isr-pitfalls)
  - [81. What Is Streaming?](#81-what-is-streaming)
  - [82. Streaming vs Traditional SSR](#82-streaming-vs-traditional-ssr)
  - [83. How Streaming Works](#83-how-streaming-works)
  - [84. Streaming Patterns](#84-streaming-patterns)
  - [85. When to Use Streaming](#85-when-to-use-streaming)
  - [86. Streaming Best Practices](#86-streaming-best-practices)
  - [87. Streaming Examples](#87-streaming-examples)
  - [88. Streaming Pitfalls](#88-streaming-pitfalls)
  - [89. What Is Partial Prerendering?](#89-what-is-partial-prerendering)
  - [90. PPR vs Other Strategies](#90-ppr-vs-other-strategies)
  - [91. How PPR Works](#91-how-ppr-works)
  - [92. PPR Patterns](#92-ppr-patterns)
  - [93. When to Use PPR](#93-when-to-use-ppr)
  - [94. PPR Best Practices](#94-ppr-best-practices)
  - [95. PPR Examples](#95-ppr-examples)
  - [96. PPR Pitfalls](#96-ppr-pitfalls)
- [Shared Foundations](#shared-foundations)
- [Quick Reference Card](#quick-reference-card)

---

## Shared Orientation — The Next.js Mental Model

The App Router rests on two big ideas: an **explicit server/client boundary** and a **per-route rendering choice**. This file covers both halves.

| Group | What it answers | Topics |
|---|---|---|
| **Part A — Building Blocks** | How do I structure routes, components, and server/client code? | App Router, Server Components, Client Components, Server Actions, Route Handlers, Middleware, React Router |
| **Part B — Rendering Strategies** | When and how does each page render? | SSR, SSG, ISR, Streaming, PPR |

**Rule of thumb:** **Part A** defines *structure* (files, components, boundaries); **Part B** defines *timing* (when HTML is produced). A real page combines them — e.g., a Server Component (Part A) fetched during ISR (Part B) and streamed behind Suspense (Part B).

**The server/client boundary (core mental model):** in the App Router, components are **server by default**; you opt into the client only where interactivity is needed (`'use client'`). Most data fetching and rendering happens on the server; the browser receives HTML + a small interactive island.

---

# Part A — App Router Building Blocks

## 1. What Is the Next.js App Router?

The **App Router** is Next.js's file-system router (introduced in Next.js 13). You define routes by creating **files and folders** in the `app/` directory — no router configuration.

- Folder structure **= URL structure** (`app/dashboard/settings` → `/dashboard/settings`).
- Special files (`page`, `layout`, `loading`, `error`) hook into the route lifecycle.
- It replaces the older `pages/` router as the modern default.

**One-liner:** define routes by creating files in `app/`, not by configuring a router.

## 2. App Router File Conventions

| File | Role |
|---|---|
| `page.tsx` | Route UI (makes the route public) |
| `layout.tsx` | Shared wrapper around nested pages |
| `loading.tsx` | Loading UI (Suspense fallback) |
| `error.tsx` | Error boundary for the route |
| `not-found.tsx` | 404 UI |
| `template.tsx` | Like layout but re-mounts on navigation |
| `route.ts` | API endpoint (Route Handler) |
| `[param]` / `(...)` / `@slot` | Dynamic / grouped / parallel segments |

**Key point:** the URL is derived from the folder tree; special filenames add lifecycle hooks.

## 3. How App Router Routing Works

- Each **folder** is a route segment; each **`page.tsx`** makes that segment navigable.
- **Layouts nest** — a parent layout wraps all child pages/layouts.
- **Dynamic segments** (`[id]`) inject URL params; **route groups** `(...)` organize without affecting the URL.
- **Parallel routes** (`@slot`) render multiple layouts in one view; **intercepting routes** handle modals/overlays.

**Rule of thumb:** think in a tree of layouts wrapping pages, with the URL mapping to folder depth.

## 4. App Router Patterns

- **Nested layouts** for shared chrome (nav, sidebar, footer).
- **Route groups** `(marketing)` / `(app)` to organize without URL impact.
- **Dynamic routes** `[id]` / catch-all `[...slug]` for parameterized pages.
- **Colocation** — keep component files alongside routes without making them routes.
- **Parallel + intercepting routes** for modals and dashboards.

## 5. When to Use the App Router

- Any **new Next.js 13+ app** — it's the modern default.
- When you want **server components, streaming, layouts, and nested routing** out of the box.
- When you need fine-grained **loading/error** states per route.

## 6. App Router Best Practices

1. **Use layouts** for shared UI instead of repeating it per page.
2. **Add `loading.tsx` / `error.tsx`** per meaningful route for good UX.
3. **Keep components server by default** — opt into client only where needed.
4. **Colocate** non-route files to keep folders clean.
5. **Prefer Server Actions** over hand-written API routes for form mutations.

## 7. App Router Examples

### Example 1 — Nested Layout + Page
```
app/
  layout.tsx          ← root layout (nav + footer)
  dashboard/
    layout.tsx        ← dashboard sidebar
    page.tsx          ← /dashboard
    settings/page.tsx ← /dashboard/settings
```
**Why:** shared chrome lives in layouts; pages stay focused on content.

### Example 2 — Dynamic Route
```tsx
// app/posts/[id]/page.tsx
export default function Post({ params }: { params: { id: string } }) {
  return <h1>Post {params.id}</h1>;
}
```
**Why:** one file handles all `/posts/:id` URLs.

## 8. App Router Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Mixing `app/` and `pages/` | Confusion, double routing | Migrate fully to `app/` |
| Over-nesting layouts | Rigid, slow re-renders | Flatten where possible |
| Careless client/server boundary | Bloated client bundles | Keep `'use client'` low in the tree |
| Missing loading/error files | Poor UX on slow/failing routes | Add per-route fallbacks |

---

## 9. What Are React Server Components?

**React Server Components (RSC)** render **exclusively on the server** and ship **zero client-side JavaScript** to the browser.

- They can access databases, filesystem, and secrets directly (server-only).
- They **cannot** use hooks, state, effects, or browser APIs.
- They're the **default** in the App Router.

**One-liner:** server-rendered components with no JS cost to the browser.

## 10. The Server Component Model

| Can do | Cannot do |
|---|---|
| Fetch data directly (async) | Use `useState`/`useEffect` |
| Access backend resources | Handle DOM/browser events |
| Keep heavy deps server-side | Use context the same way as client |
| Pass serializable props to Client Components | Hold client-side state |

**Key point:** RSC run on every request/render on the server; their output is serialized React tree, not shipped JS.

## 11. How Server Components Work

1. Server renders the component tree (RSC can be `async` and `await` data).
2. The result is a **serialized payload** sent to the browser — not component code.
3. Client Components are rendered as "islands" within the server tree.
4. The browser hydrates only the interactive (client) parts.

**Rule of thumb:** data fetching + rendering = server; interaction = client island.

## 12. Server Component Patterns

- **Fetch data directly** in an `async` server component (no `useEffect`).
- **Keep heavy libraries server-side** (they never reach the bundle).
- **Pass serializable props** (strings, numbers, arrays, plain objects) to Client Components.
- **Compose** server components around small client components.

## 13. When to Use Server Components

- **Data fetching** and rendering from DB/API/filesystem.
- **Static or read-only** content.
- Anything **not needing interactivity**.

## 14. Server Component Best Practices

1. **Server by default** — opt into client only where interactivity is required.
2. **Push `'use client'` as low as possible** in the tree.
3. **Fetch data in server components**, pass results down as props.
4. **Keep non-serializable logic** out of props crossing the boundary.

## 15. Server Component Examples

### Example 1 — Direct Data Fetch
```tsx
// app/users/page.tsx  (Server Component — default)
export default async function Users() {
  const users = await db.user.findMany();
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```
**Why:** no client fetch, no loading state boilerplate, zero JS shipped.

### Example 2 — Server Wrapping Client
```tsx
<ServerList data={await fetch()} />  {/* passes serializable data */}
  <ClientLikeButton id={item.id} />  {/* interactive island */}
```
**Why:** heavy data stays server-side; only the button ships JS.

## 16. Server Component Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Using hooks in server components | Runtime error | Move to a Client Component |
| Passing non-serializable props | Serialization error | Pass plain/serializable data |
| Marking everything client | Bloated bundles | Default to server |
| Duplicating fetch on client | Redundant requests | Fetch once on server |

---

## 17. What Are Client Components?

**Client Components** render in the browser and support **interactivity** — hooks, state, effects, and event handlers. You opt in with the `'use client'` directive.

**One-liner:** the interactive counterpart to RSC, opted in via `'use client'`.

## 18. The Client Component Model

- Declared with `'use client'` at the top of the file.
- Can use `useState`, `useEffect`, event handlers, refs, browser APIs.
- Are **hydrated** in the browser (server sends initial HTML, then JS takes over).
- Everything they import counts toward the **client bundle**.

## 19. How Client Components Work

1. The directive marks the file (and its imports) as client code.
2. On first request, the server **pre-renders their HTML** (for fast first paint + SEO).
3. In the browser, React **hydrates** the HTML, attaching interactivity.
4. From then on they behave like classic React components.

**Key point:** Client Components are still server-rendered initially — `'use client'` enables hydration, not client-only rendering.

## 20. Client Component Patterns

- **Interactive widgets** (buttons, toggles, modals, forms with state).
- **Client-only logic** (browser APIs, animations, third-party client libs).
- **Interleave** — a server component renders data, a small client component handles interaction.

## 21. When to Use Client Components

- **Interactivity** — state, effects, event handlers.
- **Browser APIs** (window, localStorage, IntersectionObserver).
- **Client-only libraries** (charts, rich text editors).

## 22. Client Component Best Practices

1. **Minimize client JS** — keep the boundary as low as possible.
2. **Push `'use client'` down the tree**, not at the root.
3. **Pass server-fetched data as props** rather than re-fetching on the client.
4. **Code-split** large client components with `dynamic()` / lazy loading.

## 23. Client Component Examples

### Example 1 — Interactive Counter
```tsx
"use client";
import { useState } from "react";
export default function Counter() {
  const [n, setN] = useState(0);
  return <button onClick={() => setN(n + 1)}>{n}</button>;
}
```
**Why:** needs state + an event handler — classic client component.

### Example 2 — Receiving Server Data
```tsx
"use client";
export default function Filter({ products }: { products: Product[] }) {
  const [q, setQ] = useState("");
  // filter client-side; data came from server as props
}
```
**Why:** server fetched the list; client only handles the interactive filter.

## 24. Client Component Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Marking the whole tree client | Huge bundle, slow | Push `'use client'` lower |
| Re-fetching data already on server | Redundant requests | Pass as props |
| Hydration mismatches | React warnings | Avoid `window`/time-dependent first render |
| Importing server-only code | Bundle bloat/errors | Keep server deps in server components |

---

## 25. What Are Server Actions?

**Server Actions** are async functions that run **on the server** but can be **called directly from Client Components** (e.g., form submissions) — without writing a separate API endpoint.

**One-liner:** server-side mutations invoked from the client, no API route required.

## 26. The Server Action Model

- Marked with `'use server'` (file-level or function-level).
- Always `async`; return **serializable** data.
- Work natively with `<form action={...}>` for **progressive enhancement** (works without JS).
- Often paired with `revalidatePath`/`revalidateTag` to refresh cached data.

## 27. How Server Actions Work

1. Client calls the action (form submit or direct call).
2. Next.js sends a secure request to the server running that function.
3. The function performs the mutation (DB write, API call).
4. It returns serializable data and/or triggers cache revalidation.
5. The UI updates without a manual refetch.

**Key point:** Server Actions collapse the "form → fetch → API route → mutation → refetch" chain into one function.

## 28. Server Action Patterns

- **Form actions** — `<form action={createPost}>` (works without JS).
- **`useFormState` / `useFormStatus`** — handle pending state + validation feedback.
- **`revalidatePath` / `revalidateTag`** — refresh data after a mutation.
- **`useFormStatus`** for submit-button loading states.

## 29. When to Use Server Actions

- **Form submissions** and data mutations.
- Any **client → server write** that doesn't need a public HTTP API.
- When you want **progressive enhancement** (works without JS).

## 30. Server Action Best Practices

1. **Validate input** server-side (never trust client data).
2. **Revalidate** cached data after writes (`revalidatePath`/`revalidateTag`).
3. **Return serializable** results only.
4. **Authorize** the action (check the user/session).
5. Prefer Server Actions over Route Handlers for **form mutations**.

## 31. Server Action Examples

### Example 1 — Form Mutation + Revalidation
```tsx
// app/actions.ts
"use server";
import { revalidatePath } from "next/cache";
export async function createPost(formData: FormData) {
  await db.post.create({ title: formData.get("title") });
  revalidatePath("/posts");
}
// app/posts/new/page.tsx  (Server Component)
<form action={createPost}><input name="title" /><button>Add</button></form>
```
**Why:** no API route, no client fetch, works without JS, auto-refreshes the list.

## 32. Server Action Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| No input validation | Security holes | Validate server-side |
| Forgetting to revalidate | Stale UI | Call `revalidatePath`/`revalidateTag` |
| Returning non-serializable data | Errors | Return plain data |
| Using for public APIs | Wrong tool | Use Route Handlers for HTTP APIs |

---

## 33. What Are Route Handlers?

**Route Handlers** are `route.ts` files that define **API endpoints** using Web-standard `Request`/`Response` objects — the App Router's replacement for the old API Routes.

**One-liner:** build HTTP API endpoints in the App Router with Web Request/Response.

## 34. The Route Handler Model

- Defined in `route.ts` (or `route.tsx`) inside a route segment.
- Export named HTTP methods: `GET`, `POST`, `PUT`, `DELETE`, etc.
- Each receives a standard Web `Request` and returns a `Response`.
- Run on the server; can be **edge** or **Node.js** runtime.

## 35. How Route Handlers Work

1. A request hits `app/<segment>/route.ts`.
2. The matching method handler (`GET`/`POST`/…) runs.
3. It reads the `Request` (body, headers, search params), does work, returns a `Response`.
4. Supports **streaming** responses and **caching** via standard headers.

**Key point:** full control over the HTTP contract — status codes, headers, streaming, content types.

## 36. Route Handler Patterns

- **REST endpoints** for non-React clients / mobile.
- **Webhook receivers** (Stripe, GitHub, etc.).
- **Streaming responses** (SSE, AI token streams).
- **CORS + auth** at the HTTP layer.

## 37. When to Use Route Handlers

- You need a **real HTTP API** (webhooks, third-party integrations, mobile clients).
- You're **streaming** responses (SSE, LLM token streams).
- A non-React client must call you over HTTP.

## 38. Route Handler Best Practices

1. **Prefer Server Actions for form mutations**; Route Handlers for HTTP APIs.
2. **Set correct status codes + headers** (CORS, content-type, caching).
3. **Validate + authorize** every request.
4. **Stream** large/AI responses instead of buffering.
5. Choose **edge runtime** for latency-sensitive, lightweight handlers.

## 39. Route Handler Examples

### Example 1 — GET Endpoint
```ts
// app/api/users/route.ts
export async function GET() {
  const users = await db.user.findMany();
  return Response.json(users);
}
```
**Why:** clean Web-standard API for any HTTP client.

### Example 2 — Webhook Receiver
```ts
export async function POST(req: Request) {
  const event = await req.json();
  // verify signature, handle event
  return new Response("ok");
}
```
**Why:** ideal for third-party webhook integrations.

## 40. Route Handler Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Using where Server Actions suffice | Unnecessary HTTP layer | Use Server Actions for forms |
| Ignoring caching headers | Missed perf wins | Set Cache-Control / revalidate |
| No auth/validation | Security holes | Authorize + validate |
| Heavy logic on edge runtime | Limits/errors | Use Node.js runtime if needed |

---

## 41. What Is Next.js Middleware?

**Middleware** is code that runs **before a request is completed**, at the **edge**, to rewrite, redirect, modify headers, or run auth checks.

**One-liner:** edge-level pre-request logic (auth gating, redirects, i18n).

## 42. The Middleware Model

- Defined in `middleware.ts` at the project root (or `src/`).
- Runs **before routing** — sees the request before a route is chosen.
- Executes on the **edge runtime** (fast, globally distributed).
- Uses a `matcher` config to limit which paths it runs on.

## 43. How Middleware Works

1. Request arrives at the edge.
2. Middleware inspects it (cookies, headers, URL, geo).
3. It can **rewrite** the URL, **redirect**, set **headers**, or **continue**.
4. The (possibly rewritten) request proceeds to routing.

**Key point:** Middleware is for **cross-cutting request concerns**, not business logic — keep it fast.

## 44. Middleware Patterns

- **Auth checks** → redirect to `/login` if unauthenticated.
- **i18n** → rewrite to a locale-prefixed route based on headers/cookies.
- **A/B testing / feature flags** → rewrite to variants.
- **Header injection** → add request/response headers.

## 45. When to Use Middleware

- **Authentication/authorization** gating.
- **Locale/i18n routing**.
- **Redirects** and URL rewrites.
- Edge-level **feature flagging**.

## 46. Middleware Best Practices

1. **Keep it minimal and fast** — it runs on every matched request.
2. **Limit the `matcher`** to only the paths that need it.
3. **Don't do heavy work** (no DB queries if avoidable).
4. Use it for **routing concerns**, not data fetching.

## 47. Middleware Examples

### Example 1 — Auth Redirect
```ts
// middleware.ts
export function middleware(req: NextRequest) {
  if (!req.cookies.get("session")) return NextResponse.redirect(new URL("/login", req.url));
}
export const config = { matcher: ["/dashboard/:path*"] };
```
**Why:** gates `/dashboard/*` at the edge before rendering.

## 48. Middleware Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Running on every route | Slow global overhead | Scope the `matcher` |
| Heavy logic inside | Edge limits/latency | Move to route handlers/actions |
| Data fetching in middleware | Unsupported/slow | Fetch in components/handlers |
| Forgetting matcher config | Runs on static assets | Configure matcher carefully |

---

## 49. What Is React Router?

**React Router** is a **client-side** declarative routing library for React apps **outside Next.js** (e.g., Vite, CRA). It maps URLs to components in the browser.

**One-liner:** client-side routing with dynamic segments for SPAs (non-Next.js).

## 50. React Router Core Concepts

| Concept | Role |
|---|---|
| `<Routes>` / `<Route>` | Define the URL → component mapping |
| `<Link>` | Client-side navigation (no full reload) |
| Dynamic segments | `:id` URL params |
| Nested routes | Outlet-based layout nesting |
| Loaders / Actions | Data fetching + mutations (data router) |

## 51. How React Router Works

- The router listens to the browser's URL (History API).
- On navigation, it matches the URL to `<Route>`s and renders the right component — **without a full page reload**.
- The **data router** (`createBrowserRouter`) adds `loader`s (fetch on navigation) and `action`s (mutations), similar to Server Actions but client/edge-oriented.

## 52. React Router Patterns

- **Nested routes** with `<Outlet>` for shared layouts.
- **Dynamic params** (`/post/:id`).
- **Loaders + actions** for data (v6.4+ data API).
- **Protected routes** via loader/guard wrappers.
- **Lazy loading** route components.

## 53. When to Use React Router

- **SPA routing** in Vite/CRA/remix-free apps.
- Client-side navigation without a framework like Next.js.

## 54. React Router Best Practices

1. Use the **data router** (`createBrowserRouter`) with loaders/actions.
2. **Lazy-load** route components for smaller initial bundles.
3. Use `<Link>` (never `<a>`) for in-app navigation.
4. Handle **loading/error** states per route.

## 55. React Router Examples

### Example 1 — Nested Routes with Params
```tsx
<Routes>
  <Route path="/" element={<Layout />}>
    <Route index element={<Home />} />
    <Route path="post/:id" element={<Post />} />
  </Route>
</Routes>
```
**Why:** one config maps URLs to components with a shared layout.

## 56. React Router Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Using `<a>` for navigation | Full page reloads | Use `<Link>` |
| Not lazy-loading routes | Big initial bundle | `lazy` / dynamic imports |
| Client-only (no SSR) | Poor SEO | Add SSR or use Next.js |
| Ignoring loaders | Manual fetch boilerplate | Use the data router API |

---

# Part B — Rendering Strategies

## 57. What Is Server-Side Rendering?

**SSR** renders HTML **on the server per request**, sending fully-formed HTML to the browser for fast first paint and SEO, then hydrating it.

**One-liner:** fresh server-rendered HTML on every request.

## 58. How SSR Differs From Other Strategies

| Strategy | When rendered | Freshness | Cost |
|---|---|---|---|
| **SSR** | Per request | Always fresh | Per-request compute |
| SSG | Build time | Static until rebuild | ~Zero per request |
| ISR | Build + periodic | Periodically fresh | Low |
| Streaming | Per request, chunked | Fresh, progressive | Per-request |

**Rule of thumb:** use SSR when content must be **fresh per request** and SEO matters.

## 59. How SSR Works

1. A request arrives.
2. The server renders the React tree to HTML (fetching data as needed).
3. HTML is sent to the browser (fast first paint + indexable).
4. React **hydrates** the HTML, attaching interactivity.

**Key point:** trade per-request server compute for fresh, SEO-friendly HTML.

## 60. SSR Patterns

- **Dynamic data pages** (user dashboards, real-time feeds).
- **Personalized content** (per-user).
- **App Router dynamic rendering** (opt out of static via dynamic APIs).

## 61. When to Use SSR

- Per-request **dynamic/personalized** data.
- Pages needing **SEO** that can't be static.
- Authenticated, user-specific views.

## 62. SSR Best Practices

1. **Cache** where you can (don't render fresh needlessly).
2. **Keep server logic fast** — slow renders hurt TTFB.
3. **Defer slow parts** with Streaming/Suspense.
4. **Hydrate efficiently** to avoid INP issues.

## 63. SSR Examples

### Example 1 — Dynamic Dashboard
**Why:** each user sees their own fresh data on every load; SEO-friendly and up-to-date.

## 64. SSR Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| SSR for static content | Wasted compute | Use SSG/ISR |
| Slow server renders | High TTFB | Optimize queries, add streaming |
| Heavy hydration | Poor INP | Reduce client JS, split islands |

---

## 65. What Is Static Site Generation?

**SSG** pre-renders pages to static HTML **at build time**, served from a CDN — the fastest and cheapest strategy.

**One-liner:** build once, serve fast static HTML forever (until rebuild).

## 66. SSG vs Other Rendering Strategies

| | SSG | SSR | ISR |
|---|---|---|---|
| Render time | Build | Request | Build + periodic |
| Freshness | Static | Live | Periodic |
| Speed | Fastest | Slower | Fast |
| Best for | Stable content | Dynamic content | Periodically updated |

## 67. How SSG Works

1. At build, Next.js renders each page to static HTML.
2. HTML + assets are deployed to a CDN.
3. Requests are served static — **zero per-request compute**.

**Key point:** content is fixed until the next build (or via ISR).

## 68. SSG Patterns

- **Marketing/landing pages**, docs, blogs.
- Public content that changes rarely.
- Pages with data known at build time.

## 69. When to Use SSG

- **Static/public** content that changes infrequently.
- Maximum **performance** and minimal **cost**.

## 70. SSG Best Practices

1. Use for **stable** content.
2. Pair with **ISR** when freshness is needed.
3. Watch **build times** for very large sites.

## 71. SSG Examples

### Example 1 — Marketing Site
**Why:** instant CDN-served pages, perfect Lighthouse scores, near-zero hosting cost.

## 72. SSG Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| SSG for fast-changing data | Stale content | Use ISR/SSR |
| Huge site → long builds | Slow deploys | Use ISR for on-demand pages |

---

## 73. What Is Incremental Static Regeneration?

**ISR** generates static pages at build, then **regenerates them in the background** — on a time interval or on-demand — giving static speed with fresh data.

**One-liner:** static speed + fresh data via background regeneration.

## 74. ISR vs SSG vs SSR

| | SSG | ISR | SSR |
|---|---|---|---|
| Speed | Fastest | Fast | Slower |
| Freshness | Build-only | Periodic/on-demand | Per-request |
| Cost | Lowest | Low | Per-request |
| Best for | Static | Periodically updated | Always-fresh |

## 75. How ISR Works

1. First request serves the **static** page (fast).
2. If stale (past `revalidate`), the **stale page** is served while regeneration runs **in the background** (stale-while-revalidate).
3. Subsequent requests get the **regenerated** page.
4. Can also be triggered **on-demand** via `revalidateTag`/`revalidatePath`.

**Key point:** users always get a fast response; freshness happens behind the scenes.

## 76. ISR Patterns

- **E-commerce catalogs** (prices/stock updated periodically).
- **Blogs/CMS** content.
- **Dashboards** with near-real-time data.

## 77. When to Use ISR

- Mostly-static content that **updates periodically**.
- You want **static performance** without stale data.

## 78. ISR Best Practices

1. Set **sensible `revalidate` windows** (match how stale is acceptable).
2. Use **on-demand revalidation** (`revalidateTag`) for instant updates after mutations.
3. Don't set `revalidate` so low it becomes SSR.

## 79. ISR Examples

### Example 1 — Product Page
```tsx
export const revalidate = 60; // regenerate at most once per 60s
export default async function Product({ params }) {
  const p = await fetch(`/api/products/${params.id}`).then(r => r.json());
  return <ProductView product={p} />;
}
```
**Why:** CDN-fast, refreshes within a minute.

### Example 2 — On-Demand Revalidation
**Why:** after an admin edits a product, call `revalidateTag("products")` to update instantly.

## 80. ISR Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Too-long revalidate | Stale data | Shorten or use on-demand |
| Too-short revalidate | Effectively SSR | Lengthen the window |
| Ignoring stale window | Confusing UX | Understand stale-while-revalidate |

---

## 81. What Is Streaming?

**Streaming** sends HTML to the browser **in chunks as it's ready**, instead of waiting for the whole page — improving Time-to-First-Byte and perceived performance.

**One-liner:** stream HTML progressively so users see content sooner.

## 82. Streaming vs Traditional SSR

| | Traditional SSR | Streaming |
|---|---|---|
| Delivery | All at once | Chunked, progressive |
| TTFB | Waits for all data | Fast (sends shell first) |
| Slow data | Blocks whole page | Deferred behind Suspense |
| UX | Blank → all | Shell → fills in |

## 83. How Streaming Works

1. The server sends the **static/fast shell** immediately.
2. Slow components are wrapped in **`<Suspense>`** with fallback UI.
3. As each suspended part resolves, its HTML is **streamed in** and swapped.
4. The user sees content progressively instead of staring at a blank screen.

**Key point:** Streaming turns "wait for everything" into "show what's ready."

## 84. Streaming Patterns

- Wrap **slow data sections** in `<Suspense fallback={...}>`.
- Use `loading.tsx` (which is Suspense under the hood) per route.
- Stream around expensive queries/API calls.

## 85. When to Use Streaming

- Pages with **slow data fetches**.
- Improving **perceived performance** (TTFB, LCP).

## 86. Streaming Best Practices

1. **Use `<Suspense>` liberally** around slow parts.
2. **Stream the fast shell first**, defer the slow bits.
3. Provide **meaningful fallbacks** (skeletons), not blank space.
4. Combine with RSC for server-side streaming.

## 87. Streaming Examples

### Example 1 — Page with a Slow Section
```tsx
export default function Page() {
  return (
    <>
      <Header />              {/* sent immediately */}
      <Suspense fallback={<Skeleton />}>
        <SlowDashboard />     {/* streamed when ready */}
      </Suspense>
    </>
  );
}
```
**Why:** users see the header instantly; the dashboard fills in without blocking.

## 88. Streaming Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| No Suspense boundaries | Whole page waits | Wrap slow parts |
| Poor fallbacks | Janky/blank flashes | Use skeleton loaders |
| Everything suspended | Nothing shows early | Stream the shell first |

---

## 89. What Is Partial Prerendering?

**PPR** (experimental) combines a **static prerendered shell** with **streamed dynamic content** — the best of SSG (fast cached shell) and Streaming (fresh dynamic parts).

**One-liner:** prerender the static shell, stream in only the dynamic bits.

## 90. PPR vs Other Strategies

| | PPR | SSG | SSR | Streaming |
|---|---|---|---|---|
| Shell | Static (cached) | Static | Dynamic | Dynamic |
| Dynamic parts | Streamed | None | All | All |
| Speed | Fast (cached shell) | Fastest | Slower | Progressive |

## 91. How PPR Works

1. At build, the **static shell** of a page is prerendered and cached.
2. **Dynamic regions** (marked by Suspense) are left as "holes."
3. On request, the cached shell is served instantly; dynamic holes are **streamed in**.
4. Result: near-instant static delivery + fresh dynamic content.

**Key point:** PPR splits each page into "static (cacheable)" and "dynamic (streamed)" automatically based on Suspense boundaries.

## 92. PPR Patterns

- Mark dynamic parts with `<Suspense>`; the rest becomes the static shell.
- Pages that are **mostly static with small dynamic regions** (e.g., a personalized banner on an otherwise static page).

## 93. When to Use PPR

- Pages that are **mostly static** with small **dynamic** sections.
- You want **SSG-like speed** with some per-request personalization.
- (Currently **experimental** — evaluate stability before production.)

## 94. PPR Best Practices

1. **Maximize the static shell**; isolate only true dynamic parts.
2. Use **Suspense** to define dynamic holes.
3. **Monitor experimental status** — APIs may change.
4. Keep dynamic regions small for the best speedup.

## 95. PPR Examples

### Example 1 — Mostly-Static Page with a Dynamic User Widget
**Why:** header/nav/footer are prerendered & cached (instant); only the "Welcome, {user}" widget streams in fresh.

## 96. PPR Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Experimental instability | Breaking changes | Track Next.js releases |
| Too much marked dynamic | Defeats PPR's benefit | Keep dynamic regions minimal |
| Misunderstanding holes | Unexpected caching | Learn the Suspense-based boundary |

---

## Shared Foundations

Concepts that recur across **all App Router topics**:

- **The server/client boundary** — the central mental model. Server by default; opt into client (`'use client'`) only for interactivity. Push the boundary as low as possible.
- **Rendering is a per-route choice** — static (SSG), periodic (ISR), per-request (SSR), or progressive (Streaming/PPR). Pick per page, not per app.
- **Caching & revalidation** — the data layer (`fetch` caching, `revalidatePath`/`revalidateTag`) ties mutations to refreshed UI.
- **Hydration** — server HTML + client JS = interactivity; minimize client JS to keep hydration fast (Core Web Vitals).
- **Progressive enhancement** — Server Actions and form actions work even without JS.
- **Performance budgets** — Core Web Vitals (**LCP**, **INP**, **CLS**) drive most rendering/component decisions.

## Quick Reference Card

```
TWO HALVES:
  Part A — Building Blocks  → structure (files, components, boundaries)
  Part B — Rendering        → timing (when HTML is produced)

COMPONENT MODEL (Part A):
  Server by default → opt into client ('use client') only for interactivity
  Push 'use client' as LOW in the tree as possible
  Server Components: data fetch, zero JS, no hooks
  Client Components: state, effects, events, hydration

MUTATIONS & APIs (Part A):
  Form mutations?      → Server Actions ('use server')
  Real HTTP API?       → Route Handlers (route.ts)
  Cross-cutting edge?  → Middleware (auth, i18n, redirects)

RENDERING PICKER (Part B):
  Static, rarely changes?        → SSG
  Static, updates periodically?  → ISR
  Fresh per request / SEO?       → SSR
  Slow data, better perceived?   → Streaming (Suspense)
  Mostly static + small dynamic? → PPR (experimental)

NON-NEXT.JS ROUTING: React Router (client-side, Vite/CRA)

GOLDEN RULES:
  ✓ Server components by default; minimal client islands
  ✓ Revalidate cache after mutations
  ✓ Wrap slow parts in Suspense to stream
  ✓ Use loading.tsx / error.tsx per route
  ✓ Track Core Web Vitals (LCP, INP, CLS)
```

---

*This file covers the App Router building blocks and rendering strategies. More Next.js topics (data fetching & caching, deployment, optimizations) will be added as separate files in this series over time.*
