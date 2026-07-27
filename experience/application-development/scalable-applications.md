# Design & Develop Scalable Applications

> **Category:** Application Development
> **Relevant at:** Impressive Security (Node.js/NestJS), Eicra Soft (Node.js/TypeScript & Python/FastAPI), MVI Solutions (Python/Django/DRF), As-Sunnah Foundation (React/Next.js/TypeScript)
> **Related tech docs:** `case/structures-architecture/backend-systems.md` (Backend Architecture §9–16, Software Architecture §33–40), `case/structures-architecture/architecture-patterns.md` (Microservices §1–8), `case/framework/nextjs/app-router-and-rendering.md` (App Router & rendering §1–56)

---

## 1. What This Means

Designing and developing scalable applications means building software that **stays fast, secure, and maintainable** as users, data, and complexity grow — using the right architecture and framework for the job.

**Scope:**
- Writing clean, modular code following **SOLID principles**
- Structuring applications with **layered/clean architecture** (separation of concerns)
- Choosing the right framework for the domain (NestJS for enterprise Node.js, FastAPI for async Python APIs, Django for full-stack web apps, React/Next.js for modern frontends)
- Ensuring the system can **scale horizontally** (stateless services, database read replicas, caching) and **scale in complexity** (modular code, clear boundaries)

**Why it matters:** applications that aren't built for scale become slow, fragile, and impossible to change. The architecture decisions made early determine how far a system can grow before requiring a rewrite.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**Backend (NestJS / FastAPI / Django):**
- Designing the **layer structure first**: controllers/views → services/use-cases → repositories/data-access → domain models.
- **No business logic in controllers or ORM queries.** Controllers parse HTTP and delegate; services orchestrate; the domain enforces invariants.
- Following **SOLID** in practice: each class/module has one reason to change; depend on abstractions (interfaces), not concretions.
- **Database-per-service** in microservices (no shared DB), async communication via messaging (SQS, EventBridge) instead of chatty sync calls.
- Using **Django REST Framework** for robust APIs with serializers, viewsets, and authentication classes on top of Django's ORM.

**Frontend (React / Next.js):**
- **Server components by default** — keep heavy work (DB queries, data fetching) on the server; opt into client components only for interactivity.
- Building with **reusable, composable components** — design systems and shared UI packages reduce duplication.
- **TypeScript** everywhere for type safety, better refactoring, and self-documenting code.

**Across the stack:** the same patterns apply regardless of language — **separate concerns, invert dependencies, keep things stateless, cache aggressively.**

---

## 3. How to Implement

### Backend — NestJS / Node.js

```
Controller → Service → Repository → Domain
```

```typescript
// Controller: HTTP concerns only
@Controller("orders")
export class OrdersController {
  constructor(private readonly ordersService: OrdersService) {}

  @Post()
  async create(@Body() dto: CreateOrderDto) {
    return this.ordersService.create(dto);   // delegates
  }
}

// Service: business logic, depends on abstractions
@Injectable()
export class OrdersService {
  constructor(
    @Inject("IOrderRepository") private readonly repo: IOrderRepository,
    @Inject("IPaymentGateway") private readonly payment: IPaymentGateway,
  ) {}
  async create(dto: CreateOrderDto) {
    const order = Order.create(dto);  // domain object enforces invariants
    await this.repo.save(order);
    return order;
  }
}
```

**Key pattern:** `IOrderRepository` is an interface — the concrete implementation (Postgres, etc.) lives behind it. Same for `IPaymentGateway`. Swap implementations without touching business logic.

### Backend — Python / FastAPI + Django

**FastAPI (microservices):**
```python
# Dependency injection keeps things testable
@router.post("/orders")
async def create_order(dto: CreateOrderDto, repo: Annotated[OrderRepo, Depends(get_repo)]):
    order = Order.create(dto)
    await repo.save(order)
    return order
```

**Django + DRF:**
```python
# Business logic in services, not in views/serializers
class OrderService:
    def create_order(self, dto: CreateOrderDTO) -> Order:
        order = Order.objects.create(customer=dto.customer, ...)
        self.payment_gateway.charge(order.total)
        return order

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    def perform_create(self, serializer):
        OrderService().create_order(serializer.validated_data)
```

### Frontend — React / Next.js

- **Server Component** (default) for data fetching, zero client JS.
- **Client Component** (`"use client"`) only for interactivity.
- Push `"use client"` as low in the tree as possible — don't mark the whole page.

```tsx
// Server Component: fetches data, no JS shipped
export default async function Dashboard() {
  const data = await db.analytics.findMany();
  return (
    <div>
      <ServerChart data={data} />          {/* server-rendered */}
      <ClientDateFilter />                 {/* interactive island */}
    </div>
  );
}
```

### Cross-Framework Checklist

- [ ] Business logic is in services/domain, not in controllers or ORM calls
- [ ] Dependencies point inward (framework → use-case → domain)
- [ ] Services are stateless; any state lives in Redis/DB
- [ ] External services (payments, email) sit behind interfaces/adapters
- [ ] TypeScript / type hints enforce the contracts
- [ ] Code is organized by feature/domain, not by technical layer alone

### Avoid These

- **Anemic domain:** putting all logic in services while domain objects are empty bags of data
- **Fat controllers:** HTTP handlers that do everything (validation, business logic, DB calls)
- **Leaky abstractions:** domain code importing framework classes or ORM models
- **Shared databases between microservices:** the fastest way to build a distributed monolith
- **Deep `"use client"` wrapping:** marking entire pages as client defeats the purpose of RSC
