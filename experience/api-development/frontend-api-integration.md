# Integrate Frontend APIs & Services

> **Category:** API Development & Integration
> **Relevant at:** As-Sunnah Foundation
> **Related tech docs:** `case/api/apis-and-communication.md` (REST §1–8, GraphQL §9–16, WebSockets §17–24, SSE §25–32), `case/framework/nextjs/app-router-and-rendering.md` (App Router & rendering §1–56), `case/state-management/react-state-management.md` (TanStack Query §23–33)

---

## 1. What This Means

Integrating frontend APIs means connecting the **frontend application layer** to backend services using the right communication pattern — REST, GraphQL, WebSockets, or SSE — and doing it in a way that's performant, resilient, and maintainable.

**Scope:**
- **REST APIs:** standard CRUD, caching, pagination, optimistic updates
- **GraphQL:** typed queries, avoiding over/under-fetching, fragments, DataLoader
- **WebSockets:** real-time bidirectional (chat, collaboration, live dashboards)
- **SSE:** one-way server push (notifications, live feeds, job progress)
- **Third-party frontend services:** analytics, payment UIs, maps, chat widgets

**Why it matters:** the frontend API layer is where poor backend design becomes visible to users. Slow API responses, missing loading states, and incorrect real-time data degrade UX regardless of how well the backend is built.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**Choosing the right protocol for the data:**
- **Fetching a user profile / product list?** → REST (cached via TanStack Query)
- **Fetching deeply nested, relational data?** → GraphQL (one query instead of 5 REST calls)
- **Chat / real-time collaboration?** → WebSockets (bidirectional, low latency)
- **Live feed of new items / notifications?** → SSE (one-way, auto-reconnect built-in)

**Real decisions:**
- Don't use WebSockets for simple data fetching — it's overkill and makes caching/retries harder
- Don't use GraphQL for a simple CRUD API — REST is simpler and has better HTTP caching
- SSE is perfect for notifications but can't send client→server data — if you need two-way, use WebSockets

**The frontend API layer responsibilities:**
1. **Data fetching** — with caching, background refetching, deduplication (TanStack Query)
2. **Optimistic updates** — update UI before the server confirms (roll back on failure)
3. **Loading / error / empty states** — every data-dependent component handles all three
4. **Real-time sync** — keep UI in sync with server state without polling

**TanStack Query (the standard for server state):**
- Manages cache, staleness, refetch, dedup — replaces manual `useEffect` + `useState` fetch boilerplate
- Mutations + invalidation: after a write, invalidate the relevant read queries to refresh
- Optimistic updates: update the cache immediately, roll back on server error

---

## 3. How to Implement

### REST API Integration with TanStack Query

```tsx
// Fetch + cache a list
export function useUsers() {
  return useQuery({
    queryKey: ["users"],
    queryFn: () => fetch("/api/users").then(r => r.json()),
    staleTime: 60_000,   // serve cached data for 1 minute
  });
}

function UserList() {
  const { data, isLoading, error } = useUsers();

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorBanner error={error} />;
  return <ul>{data.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

### Optimistic Update Pattern

```tsx
const mutation = useMutation({
  mutationFn: (newTodo) => fetch("/api/todos", { method: "POST", body: JSON.stringify(newTodo) }),
  onMutate: async (newTodo) => {
    await queryClient.cancelQueries({ queryKey: ["todos"] });
    const previous = queryClient.getQueryData(["todos"]);
    queryClient.setQueryData(["todos"], old => [...old, { ...newTodo, id: "temp" }]);
    return { previous };   // rollback data
  },
  onError: (err, newTodo, context) => {
    queryClient.setQueryData(["todos"], context.previous);   // rollback
    toast.error("Failed to add todo");
  },
  onSettled: () => queryClient.invalidateQueries({ queryKey: ["todos"] }),  // server truth
});
```

**Why:** the UI updates instantly (feels fast), and if the server rejects, it rolls back seamlessly.

### GraphQL Query

```tsx
export function useUserWithOrders(userId: string) {
  return useQuery({
    queryKey: ["user", userId, "withOrders"],
    queryFn: () => graphqlClient.request(GET_USER_WITH_ORDERS, { userId }),
  });
}

const GET_USER_WITH_ORDERS = gql`
  query GetUser($userId: ID!) {
    user(id: $userId) {
      name email
      orders { id total items { title } }
    }
  }
`;
```

**Why:** one request fetches user + orders + item titles — no 3 REST round-trips.

### WebSocket — Real-Time Bidirectional

```tsx
function useChat(roomId: string) {
  const [messages, setMessages] = useState<Message[]>([]);
  const wsRef = useRef<WebSocket>();

  useEffect(() => {
    const ws = new WebSocket(`wss://api.example.com/chat/${roomId}`);
    ws.onmessage = (event) => setMessages(prev => [...prev, JSON.parse(event.data)]);
    wsRef.current = ws;
    return () => ws.close();
  }, [roomId]);

  const send = (text: string) => wsRef.current?.send(JSON.stringify({ text }));
  return { messages, send };
}
```

### SSE — One-Way Server Push

```tsx
function useLiveFeed() {
  const [events, setEvents] = useState<Event[]>([]);

  useEffect(() => {
    const source = new EventSource("/api/events/stream");
    source.onmessage = (e) => setEvents(prev => [...prev, JSON.parse(e.data)]);
    source.onerror = () => /* auto-reconnect is built into EventSource */;
    return () => source.close();
  }, []);

  return events;
}
```

**Why:** `EventSource` handles auto-reconnect for free — perfect for notifications, feeds, and live dashboards.

### Protocol Decision Framework

```
Fetching data (read)?                          → REST + TanStack Query
Complex nested data, avoiding over-fetching?   → GraphQL
Bidirectional real-time (chat, collab)?        → WebSockets
One-way push (notifications, feeds)?           → SSE
Writing data (mutations)?                      → REST/GraphQL mutation + optimistic update
Page loads fast, fresh data later?             → TanStack Query staleTime + background refetch
```

### Frontend API Checklist

- [ ] Every data fetch handles **loading, error, and empty** states
- [ ] **Optimistic updates** on mutations where UX matters
- [ ] Use **TanStack Query** (or equivalent) — no manual `useEffect` fetch
- [ ] WebSocket connections have **reconnection + heartbeat**
- [ ] SSE with **auto-reconnect** (EventSource handles it)
- [ ] Correct protocol per use case (don't WebSocket everything)
- [ ] API errors surfaced to the user meaningfully
- [ ] Dedup/coalesce identical requests (TanStack Query does this for free)

### Avoid These

- **`useEffect` + `useState` for every API call** — use TanStack Query
- **No loading/error state** — button says "Submit" while the request fails silently
- **WebSockets for simple data fetching** — adds complexity without benefit
- **No reconnection logic** — a silent WebSocket disconnect and the app looks frozen
- **SSE for two-way communication** — it's one-way; use WebSockets
- **Blocking renders on slow API calls** — stream/defer with Suspense
