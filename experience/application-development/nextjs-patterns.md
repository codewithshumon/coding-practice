# Implement Next.js Patterns

> **Category:** Application Development
> **Relevant at:** As-Sunnah Foundation
> **Related tech docs:** `case/framework/nextjs/app-router-and-rendering.md` (full App Router reference §1–56), `case/state-management/react-state-management.md` (state management §1–44), `case/web/web-quality.md` (Core Web Vitals, WCAG, SEO §1–24)

---

## 1. What This Means

Implementing Next.js patterns means building applications using the **App Router ecosystem** correctly — knowing when to use each primitive (Server Components, Client Components, Server Actions, Route Handlers, Middleware, React Router) and how they compose.

**Scope:**
- The **App Router** replaces the old Pages Router — file-system routing in `app/` with layouts, loading states, and error boundaries
- **Server Components** are the default — they render on the server, ship zero client JS
- **Client Components** (`"use client"`) enable interactivity where needed
- **Server Actions** replace custom API routes for form submissions and mutations
- **Route Handlers** (`route.ts`) are the escape hatch for real HTTP APIs
- **Middleware** runs at the edge before routing
- **React Router** is the client-side alternative for non-Next.js SPAs

**Why it matters:** Next.js 13+ fundamentally changed the React mental model. Misusing the server/client boundary (e.g., marking entire pages as client) produces slow, bloated apps that defeat the purpose of the framework.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**Choosing the right primitive:**
- **Fetching data / rendering server-only content?** → Server Component (default)
- **Interactivity (state, effects, events)?** → Client Component (`"use client"`)
- **Form submission / data mutation?** → Server Action (`"use server"`)
- **REST API / webhook / streaming?** → Route Handler (`route.ts`)
- **Auth gating / i18n / redirects?** → Middleware

**The server/client boundary is the core decision:**
```
┌─ Server Component (default) ────────────────────┐
│  fetch data, render, zero client JS              │
│  ┌─ Client Component ("use client") ──────────┐ │
│  │  interactive island (state, hooks, events) │ │
│  │  receives server data as serialized props  │ │
│  └────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

**Real tradeoffs:**
- Server Actions reduce boilerplate but couple mutations to the Next.js runtime
- Route Handlers are more portable but require manual fetch/serialization
- Client Components give interactivity but ship JavaScript
- Middleware is fast (edge) but limited — no heavy work

**The litmus test:** open the Network tab — if every component ships a JS bundle, the boundary is too high. Only interactive pieces should ship client code.

---

## 3. How to Implement

### App Router File Structure

```
app/
├── layout.tsx          # root layout (shared chrome)
├── page.tsx            # home page
├── dashboard/
│   ├── layout.tsx      # dashboard sidebar wrapper
│   ├── page.tsx        # /dashboard
│   ├── loading.tsx     # loading skeleton
│   ├── error.tsx       # error boundary
│   └── settings/
│       └── page.tsx    # /dashboard/settings
├── api/
│   └── webhooks/
│       └── route.ts    # POST endpoint for third-party webhooks
└── middleware.ts       # edge: auth gating, locale redirects
```

### Server Component — Fetch Data

```tsx
// app/posts/page.tsx  (server component by default)
export default async function Posts() {
  const posts = await db.post.findMany();   // runs on the server
  return (
    <ul>
      {posts.map(p => (
        <li key={p.id}>
          <h2>{p.title}</h2>
          <LikeButton postId={p.id} />     {/* client island */}
        </li>
      ))}
    </ul>
  );
}
```

**Why:** the data fetch runs on the server — no `useEffect`, no loading state boilerplate, zero JS for the list HTML.

### Client Component — Interactive Island

```tsx
"use client";
import { useState } from "react";

export function LikeButton({ postId }: { postId: string }) {
  const [liked, setLiked] = useState(false);
  return (
    <button onClick={() => setLiked(!liked)}>
      {liked ? "❤️" : "🤍"}
    </button>
  );
}
```

**Why:** `"use client"` is pushed as deep as possible — only the button ships JS, not the entire post list.

### Server Action — Form Mutation

```tsx
// app/actions.ts
"use server";
import { revalidatePath } from "next/cache";

export async function createPost(formData: FormData) {
  await db.post.create({ title: formData.get("title") });
  revalidatePath("/posts");          // refresh the list
}

// Component
<form action={createPost}>
  <input name="title" />
  <button type="submit">Create</button>
</form>
```

**Why:** no API route, no client fetch, works without JavaScript (progressive enhancement).

### Route Handler — Webhook Receiver

```ts
// app/api/stripe/route.ts
export async function POST(req: Request) {
  const sig = req.headers.get("stripe-signature") as string;
  const event = stripe.webhooks.constructEvent(await req.text(), sig, secret);
  // handle event
  return Response.json({ received: true });
}
```

**Why:** when a real HTTP endpoint is needed (third-party webhooks), Route Handlers provide full control.

### Middleware — Auth Gating

```ts
// middleware.ts
export function middleware(req: NextRequest) {
  if (!req.cookies.get("session")) {
    return NextResponse.redirect(new URL("/login", req.url));
  }
}
export const config = { matcher: ["/dashboard/:path*"] };
```

**Why:** runs at the edge before routing — fast, global, scoped by path.

### Decision Framework

| I need to… | Use |
|---|---|
| Fetch data and render it | Server Component |
| Add interactivity | Client Component (push low) |
| Handle a form submission | Server Action |
| Expose a public HTTP endpoint | Route Handler |
| Gate/protect routes at the edge | Middleware |
| Build a non-Next.js SPA | React Router |

### Avoid These

- **`"use client"` at the root** — makes the entire app a client-side bundle
- **Re-fetching server data on the client** — pass as serialized props
- **Using Route Handlers for form mutations** — Server Actions are cleaner and support progressive enhancement
- **Non-serializable props** crossing the server→client boundary
- **Missing loading/error boundaries** — every meaningful route should have them
