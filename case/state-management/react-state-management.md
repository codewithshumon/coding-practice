# React State Management — Complete Guide

> **Series:** State Management Documentation — Part 1
> This file holds the **four core React state tools**: Redux Toolkit, Zustand, TanStack Query, and the Context API. More topics (XState, Jotai, Recoil, forms state) will be added as separate files later.

---

## Table of Contents

- [Shared Orientation — Which State Tool, When?](#shared-orientation--which-state-tool-when)
- **Redux Toolkit**
  - [1. What Is Redux Toolkit?](#1-what-is-redux-toolkit)
  - [2. RTK vs Legacy Redux](#2-rtk-vs-legacy-redux)
  - [3. How RTK Manages State](#3-how-rtk-manages-state)
  - [4. The RTK Core API](#4-the-rtk-core-api)
  - [5. When Redux Toolkit Fits](#5-when-redux-toolkit-fits)
  - [6. When Redux Toolkit Is Overkill](#6-when-redux-toolkit-is-overkill)
  - [7. Installing and Setting Up RTK](#7-installing-and-setting-up-rtk)
  - [8. RTK Patterns](#8-rtk-patterns)
  - [9. RTK Production Best Practices](#9-rtk-production-best-practices)
  - [10. RTK Real-World Examples](#10-rtk-real-world-examples)
  - [11. RTK Pitfalls](#11-rtk-pitfalls)
- **Zustand**
  - [12. What Is Zustand?](#12-what-is-zustand)
  - [13. Zustand vs Redux vs Context](#13-zustand-vs-redux-vs-context)
  - [14. How Zustand Works](#14-how-zustand-works)
  - [15. Zustand Core API](#15-zustand-core-api)
  - [16. When to Use Zustand](#16-when-to-use-zustand)
  - [17. When NOT to Use Zustand](#17-when-not-to-use-zustand)
  - [18. Installing and Setting Up Zustand](#18-installing-and-setting-up-zustand)
  - [19. Zustand Patterns](#19-zustand-patterns)
  - [20. Zustand Best Practices](#20-zustand-best-practices)
  - [21. Zustand Real-World Examples](#21-zustand-real-world-examples)
  - [22. Zustand Pitfalls](#22-zustand-pitfalls)
- **TanStack Query**
  - [23. What Is TanStack Query?](#23-what-is-tanstack-query)
  - [24. Server State vs Client State](#24-server-state-vs-client-state)
  - [25. How TanStack Query Works](#25-how-tanstack-query-works)
  - [26. TanStack Query Core API](#26-tanstack-query-core-api)
  - [27. When to Use TanStack Query](#27-when-to-use-tanstack-query)
  - [28. When NOT to Use TanStack Query](#28-when-not-to-use-tanstack-query)
  - [29. Installing and Setting Up TanStack Query](#29-installing-and-setting-up-tanstack-query)
  - [30. TanStack Query Patterns](#30-tanstack-query-patterns)
  - [31. TanStack Query Best Practices](#31-tanstack-query-best-practices)
  - [32. TanStack Query Real-World Examples](#32-tanstack-query-real-world-examples)
  - [33. TanStack Query Pitfalls](#33-tanstack-query-pitfalls)
- **Context API**
  - [34. What Is the Context API?](#34-what-is-the-context-api)
  - [35. Context vs State Libraries](#35-context-vs-state-libraries)
  - [36. How Context Works](#36-how-context-works)
  - [37. Context Core API](#37-context-core-api)
  - [38. When to Use Context](#38-when-to-use-context)
  - [39. When NOT to Use Context](#39-when-not-to-use-context)
  - [40. Setting Up Context](#40-setting-up-context)
  - [41. Context Patterns](#41-context-patterns)
  - [42. Context Best Practices](#42-context-best-practices)
  - [43. Context Real-World Examples](#43-context-real-world-examples)
  - [44. Context Pitfalls](#44-context-pitfalls)
- [Shared Foundations](#shared-foundations)
- [Quick Reference Card](#quick-reference-card)

---

## Shared Orientation — Which State Tool, When?

The single most important idea: **client/UI state** and **server state** are different problems with different tools.

| Tool | State type | Sweet spot | One-liner |
|---|---|---|---|
| **Redux Toolkit** | Client | Large, complex, team-built apps | Predictable, structured, debuggable |
| **Zustand** | Client | Small–medium apps wanting simplicity | Minimal global state, no boilerplate |
| **TanStack Query** | Server | Any app fetching/syncing API data | Cache, refetch, invalidate remote data |
| **Context API** | Client (config) | Low-frequency global values (theme, auth) | Pass values without prop drilling |

**Rule of thumb:** **API/server data → TanStack Query.** For client state, pick by complexity: **Context** (trivial/global config) → **Zustand** (simple/medium) → **Redux Toolkit** (large/complex). Most real apps **combine** TanStack Query (server) with one client-state tool.

**Decision tree:**
- Fetching/mutating API data? → **TanStack Query**
- Theme/locale/current-user/feature flags? → **Context**
- Global UI state, want minimal setup? → **Zustand**
- Complex interdependent client state, large team, need time-travel? → **Redux Toolkit**

---

# Redux Toolkit

## 1. What Is Redux Toolkit?

**Redux Toolkit (RTK)** is the official, opinionated toolset that makes Redux practical. It removes the boilerplate that made legacy Redux painful.

- `configureStore` sets up the store with sane defaults (DevTools, thunk middleware).
- `createSlice` auto-generates action creators and uses **Immer** so you write "mutating" code that's actually immutable.
- `createAsyncThunk` handles async API calls with pending/fulfilled/rejected states.

**One-liner:** RTK is modern Redux — all the predictability, none of the boilerplate.

## 2. RTK vs Legacy Redux

| | Legacy Redux | Redux Toolkit |
|---|---|---|
| Boilerplate | High (action types, creators, switch reducers) | Low (`createSlice` does it all) |
| Immutability | Manual, error-prone | Automatic (Immer) |
| Async | `redux-thunk` by hand | `createAsyncThunk` |
| Store setup | Veratile but verbose | `configureStore` one-liner |
| Server data | Manual | **RTK Query** (bundled) |

**Rule of thumb:** always use RTK — never write legacy Redux by hand today.

## 3. How RTK Manages State

- **Single store** holds the whole app state tree.
- **Unidirectional flow:** component dispatches an action → reducer produces a *new* state → subscribed components re-render via selectors.
- **Immer** lets you write `state.value += 1` inside reducers; it produces an immutable copy underneath.
- **Selectors** let components subscribe to only the slice they need (avoids over-rendering).

**Key point:** state is never mutated in place — every change is a new object, enabling time-travel debugging and predictable renders.

## 4. The RTK Core API

| API | Purpose |
|---|---|
| `configureStore` | Create the store with defaults |
| `createSlice` | Define state + reducers + auto action creators |
| `createAsyncThunk` | Async actions (API calls) with lifecycle states |
| `createSelector` | Memoized derived state (reselect) |
| `useSelector` | Read state in a component |
| `useDispatch` | Dispatch actions in a component |
| `<Provider>` | Makes the store available to the tree |

## 5. When Redux Toolkit Fits

- **Large/complex apps** with lots of interdependent client state.
- **Teams** that benefit from strict structure and conventions.
- Need for **time-travel debugging**, action logging, or replay.
- Heavy **client-side logic** (caching computed results, complex UI flows).

## 6. When Redux Toolkit Is Overkill

- **Small apps** with a few pieces of state (use Zustand/Context).
- App is **mostly server data** with little client state (TanStack Query alone).
- Simple form or toggle state (local `useState` is enough).

## 7. Installing and Setting Up RTK

```bash
npm install @reduxjs/toolkit react-redux
```

```typescript
// store.ts
import { configureStore, createSlice } from "@reduxjs/toolkit";

const counter = createSlice({
  name: "counter",
  initialState: { value: 0 },
  reducers: {
    increment: (state) => { state.value += 1; },   // Immer: looks mutable
  },
});
export const { increment } = counter.actions;

export const store = configureStore({ reducer: { counter: counter.reducer } });
```

```tsx
// Wrap the app once
<Provider store={store}><App /></Provider>

// Use it
const count = useSelector((s) => s.counter.value);
const dispatch = useDispatch();
dispatch(increment());
```

## 8. RTK Patterns

- **Feature-based slices** — one `createSlice` per feature, colocated with its logic.
- **`createAsyncThunk`** for API calls with `pending/fulfilled/rejected`.
- **Normalized state** for collections (store entities by ID in a lookup table).
- **RTK Query** (bundled) for server state — end-to-end data fetching + caching.

## 9. RTK Production Best Practices

1. **One slice per feature** — keep related state and logic together.
2. **Keep state normalized** — collections as `{ [id]: entity }`, not arrays.
3. **Use selectors** (memoized) for derived data, never recompute in components.
4. **Colocate thunks with slices** — feature cohesion.
5. **Keep state minimal** — store raw data, compute derived values via selectors.
6. **Use RTK Query for server data** — don't hand-cache API responses in the store.
7. **Avoid deeply nested state** — flat shapes update and select more easily.

## 10. RTK Real-World Examples

### Example 1 — Async User Fetch
```typescript
export const fetchUser = createAsyncThunk("user/fetch", async (id) => {
  const res = await fetch(`/api/users/${id}`); return res.json();
});
// extraReducers handles pending/fulfilled/rejected
```
**Why:** async lifecycle states handled declaratively — loading/error UI for free.

### Example 2 — Cart State with Immer
```typescript
reducers: {
  addItem: (state, action) => { state.items.push(action.payload); }, // looks mutable
}
```
**Why:** Immer guarantees immutability while keeping code readable.

### Example 3 — Normalized Entities
**Why:** `users: { byId: {}, allIds: [] }` gives O(1) lookups and clean updates vs array scans.

### Example 4 — Memoized Selector
```typescript
const selectExpensive = createSelector([selectItems], items => heavyCompute(items));
```
**Why:** `heavyCompute` only runs when `items` actually changes.

## 11. RTK Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Using Redux for trivial state | Boilerplate for a toggle | Use `useState`/Zustand/Context |
| Non-normalized nested state | Slow updates, hard selects | Normalize by ID |
| Hand-caching server data | Stale/duplicate logic | Use RTK Query / TanStack Query |
| Non-memoized selectors | Recompute every render | Use `createSelector` |
| Mutating outside reducers | Bugs, broken time-travel | Keep all state changes in slices |

---

# Zustand

## 12. What Is Zustand?

**Zustand** is a lightweight, hook-based global state library — no actions, no reducers, no providers, no boilerplate.

- You create a **store** (a hook) that holds state *and* the functions that update it together.
- Components subscribe via the hook, optionally with **selectors** to read only what they need.

**One-liner:** minimal global state with a single hook.

## 13. Zustand vs Redux vs Context

| | Zustand | Redux Toolkit | Context API |
|---|---|---|---|
| Boilerplate | Minimal | Structured/moderate | Low |
| Provider needed | ❌ No | ✅ Yes | ✅ Yes |
| Re-render control | Selectors (granular) | Selectors (granular) | All consumers re-render |
| Best for | Simple–medium | Large/complex | Low-frequency config |

**Rule of thumb:** pick Zustand when you want global state without Redux's ceremony, but more control than Context's re-renders.

## 14. How Zustand Works

- `create()` returns a **hook** bound to a store.
- State and actions live together in one object via `set`/`get`.
- Components subscribe with **selector functions** — only the selected slice triggers a re-render when it changes.

**Key point:** because subscriptions are per-slice, Zustand avoids Context's "any change re-renders everything" problem without Redux's boilerplate.

## 15. Zustand Core API

| API | Purpose |
|---|---|
| `create` | Define the store (returns a hook) |
| `set` / `get` | Update / read state inside the store |
| `subscribe` | Listen to changes outside React |
| selectors | `useStore(s => s.x)` — subscribe to a slice |
| `persist` (middleware) | Sync to localStorage/sessionStorage |
| `devtools` (middleware) | Redux DevTools integration |

## 16. When to Use Zustand

- **Small–medium apps** needing global state.
- Want **simplicity and performance** without providers.
- Dislike Redux boilerplate but need more than local state.
- Need **persisted** state (theme, draft, cart) easily.

## 17. When NOT to Use Zustand

- Very **complex state** needing strict structure/time-travel (Redux fits better).
- **Server/API data** (TanStack Query is purpose-built).
- Truly local component state (just use `useState`).

## 18. Installing and Setting Up Zustand

```bash
npm install zustand
```

```typescript
import { create } from "zustand";

interface BearStore {
  bears: number;
  addBear: () => void;
}
export const useBearStore = create<BearStore>((set) => ({
  bears: 0,
  addBear: () => set((s) => ({ bears: s.bears + 1 })),
}));
```

```tsx
// No Provider needed — use anywhere
const bears = useBearStore((s) => s.bears);   // selector → re-renders only on bears change
const addBear = useBearStore((s) => s.addBear);
```

## 19. Zustand Patterns

- **Selectors** for selective subscription (avoid over-rendering).
- **`persist` middleware** for localStorage-backed state.
- **Slice composition** — combine smaller stores or slices for bigger apps.
- **Async actions** — just call `set` after an `await` inside an action.

## 20. Zustand Best Practices

1. **Always use selectors** — never consume the whole store (`useStore()` re-renders on any change).
2. **Keep state flat** — easier to select and update.
3. **Split stores by domain** — don't dump everything in one global store.
4. **Use middleware** — `persist` for durability, `devtools` for debugging.
5. **Memoize selector results** when deriving complex objects.

## 21. Zustand Real-World Examples

### Example 1 — Persisted Theme Store
```typescript
export const useTheme = create(
  persist((set) => ({ dark: false, toggle: () => set((s) => ({ dark: !s.dark })) }),
          { name: "theme-storage" })
);
```
**Why:** theme survives reloads with one line of middleware.

### Example 2 — Cart Store
```typescript
export const useCart = create((set, get) => ({
  items: [] as Item[],
  add: (i) => set((s) => ({ items: [...s.items, i] })),
  total: () => get().items.reduce((a, b) => a + b.price, 0),
}));
```
**Why:** state + derived getter colocated; no separate reducer layer.

### Example 3 — Selective Subscription
```tsx
const userName = useUserStore((s) => s.name);  // won't re-render if s.email changes
```
**Why:** granular subscriptions = better performance than Context.

## 22. Zustand Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Subscribing to whole store | Over-rendering | Use selectors |
| One giant store | Hard to reason about | Split by domain |
| Missing selectors | Perf issues on growth | Always select slices |
| Treating it as server cache | Stale data | Use TanStack Query |

---

# TanStack Query

## 23. What Is TanStack Query?

**TanStack Query** (formerly React Query) is the standard library for **server state** — fetching, caching, synchronizing, and updating remote data.

- It replaces the `useEffect` + `useState` + manual-cache boilerplate for API calls.
- Handles caching, background refetching, stale-while-revalidate, retries, and invalidation.

**One-liner:** the right tool for API/server data — not for UI/client state.

## 24. Server State vs Client State

| | Client state | Server state |
|---|---|---|
| Owner | Your app | The server |
| Sync model | Synchronous, local | Asynchronous, remote |
| Concerns | UI toggles, form draft | Caching, refetch, invalidation, stale data |
| Tool | Redux / Zustand / Context | **TanStack Query** |

**Rule of thumb:** if the data comes from an API, it belongs in TanStack Query; if it's UI/form/local, use a client-state tool.

## 25. How TanStack Query Works

- You define a **query** (read) or **mutation** (write) function.
- The library caches results keyed by **query keys**, tracks staleness, and refetches in the background.
- Components subscribe to query state (`data`, `isLoading`, `error`) and re-render on changes.
- After a mutation, you **invalidate** affected queries to trigger a refetch.

**Key point:** the cache is the single source of truth for server data — no manual `useState` mirrors of API responses.

## 26. TanStack Query Core API

| API | Purpose |
|---|---|
| `useQuery` | Read/cache server data |
| `useMutation` | Write/change server data |
| `QueryClient` + `<QueryClientProvider>` | App-wide cache setup |
| Query keys | Cache identity (`["users", id]`) |
| `queryClient.invalidateQueries` | Mark queries stale → refetch |
| `useInfiniteQuery` | Pagination/infinite scroll |

## 27. When to Use TanStack Query

- **Any app fetching or syncing API data** — replaces fetch boilerplate.
- Lists, detail pages, dashboards with cached data.
- Mutations that need to refresh related queries.
- Pagination, infinite scroll, optimistic updates.

## 28. When NOT to Use TanStack Query

- **Pure client/UI state** (toggles, form drafts, local UI) — use a client-state tool.
- Truly one-off static data that never changes.

## 29. Installing and Setting Up TanStack Query

```bash
npm install @tanstack/react-query
```

```tsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
const queryClient = new QueryClient();

<QueryClientProvider client={queryClient}><App /></QueryClientProvider>
```

```tsx
import { useQuery } from "@tanstack/react-query";

function Users() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["users"],
    queryFn: () => fetch("/api/users").then((r) => r.json()),
  });
  if (isLoading) return "Loading…";
  return <ul>{data.map((u) => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

## 30. TanStack Query Patterns

- **Structured query keys** — `["users", "list", { page }]` for hierarchical invalidation.
- **Mutation + invalidation** — after a write, invalidate the related read queries.
- **Optimistic updates** — update the cache before the server responds for instant UX.
- **Prefetching** — load data on hover/route-enter before it's needed.
- **`useInfiniteQuery`** — infinite scroll / load-more.

## 31. TanStack Query Best Practices

1. **Use structured, hierarchical query keys** — enables targeted invalidation.
2. **Invalidate after mutations** — keep cache consistent with the server.
3. **Tune `staleTime` / `gcTime`** — don't refetch more than necessary.
4. **Use optimistic updates** for snappy, responsive UX on writes.
5. **Enable React Query Devtools** — inspect cache and query states.
6. **Keep client state out of the query cache** — use Zustand/Redux for UI state.

## 32. TanStack Query Real-World Examples

### Example 1 — Fetch + Cache a List
**Why:** automatic caching, background refetch, dedup of identical queries across components.

### Example 2 — Mutation + Invalidation
```tsx
const mu = useMutation({ mutationFn: addUser, onSuccess: () => queryClient.invalidateQueries({ queryKey: ["users"] }) });
```
**Why:** after adding a user, the list refetches automatically — no manual refetch calls.

### Example 3 — Optimistic Update
```tsx
onMutate: async (newTodo) => {
  await queryClient.cancelQueries({ queryKey: ["todos"] });
  const prev = queryClient.getQueryData(["todos"]);
  queryClient.setQueryData(["todos"], (old) => [...old, newTodo]);
  return { prev };
}
```
**Why:** the UI updates instantly; rolls back if the server rejects.

### Example 4 — Prefetch on Hover
**Why:** prefetch a detail page's data before click → instant navigation.

### Example 5 — Infinite Scroll
```tsx
const { data, fetchNextPage, hasNextPage } = useInfiniteQuery({ ... });
```
**Why:** clean pagination without manual page/offset state.

## 33. TanStack Query Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Weak/random query keys | Cache collisions, wrong data | Structured hierarchical keys |
| No invalidation after mutation | Stale data shown | Invalidate related queries |
| Storing client state in cache | Mixing concerns | Keep UI state separate |
| Over-fetching (low staleTime) | Excessive API calls | Tune staleTime/gcTime |
| Ignoring error/loading states | Broken UX | Always handle isLoading/error |

---

# Context API

## 34. What Is the Context API?

The **Context API** is React's built-in mechanism for **passing data through the component tree without prop drilling**.

- It's like dependency injection for React: a Provider sets a value, any descendant can consume it.
- It ships with React — **no install**, no extra dependency.

**One-liner:** share low-frequency global values (theme, locale, auth) without threading props.

## 35. Context vs State Libraries

| | Context API | Redux / Zustand |
|---|---|---|
| Purpose | Pass values | Manage state |
| Setup | Built-in, providers | External library |
| Re-render behavior | All consumers re-render on value change | Selectors → granular |
| Best for | Low-frequency config | Frequently-changing state |

**Rule of thumb:** Context is for **passing** values, not **managing** high-frequency state. Use a state library when state changes often.

## 36. How Context Works

- `createContext(default)` creates a context.
- A `<Provider value={...}>` supplies the value to its subtree.
- `useContext(MyContext)` reads the nearest provider's value.
- When the provider's `value` changes, **every consumer re-renders**.

**Key point:** because any value change re-renders all consumers, Context is great for low-frequency values and poor for rapidly-changing state.

## 37. Context Core API

| API | Purpose |
|---|---|
| `createContext` | Define a context + default |
| `<Provider value>` | Supply a value to the subtree |
| `useContext` | Read the nearest provider's value |
| `useReducer` (combo) | Add actions/dispatch to context |
| custom `useX` hook | Wrap `useContext` + error guard |

## 38. When to Use Context

- **Low-frequency global values** — theme, locale/i18n, current user, feature flags, routing-ish config.
- Avoiding **prop drilling** for values used deep in the tree.
- Providing **dependencies** (e.g., a configured API client) to components.

## 39. When NOT to Use Context

- **High-frequency changing state** — causes re-render storms (use Zustand/Redux).
- **Complex app state** with many interactions (use Redux/Zustand).
- **Server/API data** (use TanStack Query).

## 40. Setting Up Context

No install — it's built into React:

```tsx
import { createContext, useContext, useState } from "react";

const ThemeContext = createContext<"light" | "dark">("light");

function App() {
  const [theme, setTheme] = useState<"light" | "dark">("light");
  return (
    <ThemeContext.Provider value={theme}>
      <Button />
    </ThemeContext.Provider>
  );
}

function Button() {
  const theme = useContext(ThemeContext);  // reads nearest provider
  return <button className={theme}>Click</button>;
}
```

## 41. Context Patterns

- **Split contexts by concern** — separate Theme, Auth, Locale contexts to limit re-renders.
- **Combine with `useReducer`** — add dispatch/actions to context for local stateful logic.
- **Memoize the provider value** — `useMemo` the value so referential changes don't over-render.
- **Custom `useX` hook** — wrap `useContext` and throw if used outside the provider.

## 42. Context Best Practices

1. **Keep the context value stable** — memoize it (`useMemo`) to avoid needless re-renders.
2. **Split contexts** by change frequency — don't bundle fast- and slow-changing values.
3. **Don't use Context as a full state manager** — it's for passing values.
4. **Colocate provider scope** — wrap only the subtree that needs it, not the whole app unnecessarily.
5. **Add an error guard** in the consumer hook for misuse outside a provider.

## 43. Context Real-World Examples

### Example 1 — Theme Context
**Why:** every component reads theme without prop drilling; one provider toggles dark/light app-wide.

### Example 2 — Auth Context with useReducer
```tsx
const AuthContext = createContext<{ user: User; dispatch: Dispatch }>(...);
// dispatch LOGIN/LOGOUT; consumers read user + dispatch actions
```
**Why:** combines a stable value (auth state) with actions, no external library.

### Example 3 — Feature Flags
**Why:** flags read anywhere in the tree; toggling features without redeploying component props.

### Example 4 — Custom Hook with Guard
```tsx
function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
```
**Why:** clear error if a consumer is placed outside its provider.

## 44. Context Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Changing state in context | Re-render storm | Use Zustand/Redux for frequent state |
| One giant context | Over-rendering unrelated consumers | Split by concern |
| Unmemoized provider value | Consumers re-render every render | `useMemo` the value |
| Using it as a state manager | Performance issues at scale | Reach for Redux/Zustand |
| No provider guard | Silent undefined errors | Throw in the consumer hook |

---

## Shared Foundations

Concepts that recur across **all four tools**:

- **Client state vs server state** — the master distinction. Server data → TanStack Query; UI/local data → Redux/Zustand/Context. Mixing them causes stale data and bugs.
- **Re-render performance** — the central tradeoff. Granular subscriptions (Redux selectors, Zustand selectors) beat Context's all-consumers re-renders for frequent state.
- **Immutability** — Redux depends on it (Immer helps); other tools are more flexible.
- **Selector/memoization discipline** — derive data via selectors/memo, store minimal raw state.
- **Right tool per job** — most apps **combine** TanStack Query (server) with one client tool (Zustand or Redux). Context for global config.
- **Avoid duplication** — never mirror API responses into a client store; let TanStack Query own server state.

## Quick Reference Card

```
STATE TOOL PICKER:
  API / server data?                 → TanStack Query (always)
  Theme / locale / user / flags?     → Context API
  Simple global client state?        → Zustand
  Complex client state + big team?   → Redux Toolkit

COMMON COMBO:  TanStack Query (server)  +  Zustand/Redux (client)  +  Context (config)

PERFORMANCE RULE:
  Context        → all consumers re-render on change (low-freq only)
  Redux/Zustand  → selectors = granular re-renders (fine for frequent state)

GOLDEN RULES:
  ✓ Never mirror API data into a client store — TanStack Query owns server state
  ✓ Use selectors (Redux/Zustand) / memoized values (Context)
  ✓ Keep client state normalized & minimal; derive via selectors
  ✓ Pick the lightest tool that fits — don't use Redux for a toggle
  ✓ Combine tools by concern; don't force one to do everything
```

---

*This file covers the four core React state tools. More topics (XState, Jotai, Recoil, form-state libraries) will be added as separate files in this series over time.*
