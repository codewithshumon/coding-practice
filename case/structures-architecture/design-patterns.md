# Design Patterns — Complete Guide

> **Series:** Structures & Architecture Documentation — Part 3
> This file covers the **architectural and structural design patterns** used across frontend and backend development: MVC, MVP, MVT, MVVM, and other common patterns (Singleton, Factory, Observer, Strategy, Repository, Adapter, Decorator). Related: `case/structures-architecture/backend-systems.md` (Backend Architecture §9–16, Software Architecture §33–40), `case/structures-architecture/architecture-patterns.md` (Microservices, Event-Driven, etc.), `case/framework/angular/angular.md` (MVVM in practice), `case/framework/django/django.md` (MVT in practice).

---

## Table of Contents

- [Shared Orientation — Architectural vs Behavioral Patterns](#shared-orientation--architectural-vs-behavioral-patterns)
- **Architectural Patterns (MVC, MVP, MVT, MVVM)**
  - [1. What Is MVC?](#1-what-is-mvc)
  - [2. MVC Core Concepts](#2-mvc-core-concepts)
  - [3. How MVC Works](#3-how-mvc-works)
  - [4. Where MVC Is Used](#4-where-mvc-is-used)
  - [5. MVC Examples](#5-mvc-examples)
  - [6. MVC Pitfalls](#6-mvc-pitfalls)
  - [7. What Is MVP?](#7-what-is-mvp)
  - [8. MVP vs MVC](#8-mvp-vs-mvc)
  - [9. How MVP Works](#9-how-mvp-works)
  - [10. Where MVP Is Used](#10-where-mvp-is-used)
  - [11. MVP Examples](#11-mvp-examples)
  - [12. MVP Pitfalls](#12-mvp-pitfalls)
  - [13. What Is MVT?](#13-what-is-mvt)
  - [14. MVT vs MVC](#14-mvt-vs-mvc)
  - [15. How MVT Works](#15-how-mvt-works)
  - [16. Where MVT Is Used](#16-where-mvt-is-used)
  - [17. MVT Examples](#17-mvt-examples)
  - [18. MVT Pitfalls](#18-mvt-pitfalls)
  - [19. What Is MVVM?](#19-what-is-mvvm)
  - [20. MVVM vs MVC/MVP](#20-mvvm-vs-mvcmvp)
  - [21. How MVVM Works](#21-how-mvvm-works)
  - [22. Where MVVM Is Used](#22-where-mvvm-is-used)
  - [23. MVVM Examples](#23-mvvm-examples)
  - [24. MVVM Pitfalls](#24-mvvm-pitfalls)
- **Structural & Behavioral Patterns**
  - [25. Singleton](#25-singleton)
  - [26. Factory & Abstract Factory](#26-factory--abstract-factory)
  - [27. Observer / Pub-Sub](#27-observer--pub-sub)
  - [28. Strategy](#28-strategy)
  - [29. Repository](#29-repository)
  - [30. Adapter / Wrapper](#30-adapter--wrapper)
  - [31. Decorator](#31-decorator)
  - [32. Dependency Injection](#32-dependency-injection)
- [Shared Foundations](#shared-foundations)
- [Quick Reference Card](#quick-reference-card)

---

## Shared Orientation — Architectural vs Behavioral Patterns

Design patterns split into two broad categories:

| Category | What it answers | Examples |
|---|---|---|
| **Architectural** | How is the whole application structured? | MVC, MVP, MVT, MVVM |
| **Structural & Behavioral** | How do individual pieces relate and interact? | Singleton, Factory, Observer, Strategy, Repository, Adapter, Decorator, DI |

**Decision guide:**
- Building a **traditional web app** with clear separation? → **MVC** (backend) or **MVT** (Django)
- Building a **desktop/mobile app** with testable UI logic? → **MVP** or **MVVM**
- Need **two-way binding** between UI and data? → **MVVM** (Angular, WPF, SwiftUI)
- Writing **decoupled, swappable code**? → apply **Repository, Adapter, DI** (structural patterns, regardless of architecture)

**Rule of thumb:** the architectural pattern defines *separation of concerns*; structural patterns define *how you connect pieces within that architecture*. They compose — an MVC app still uses Repository, Adapter, and Factory patterns internally.

---

# Architectural Patterns

## 1. What Is MVC?

**MVC (Model–View–Controller)** separates an application into three interconnected parts: **Model** (data + business logic), **View** (presentation), and **Controller** (input handling + orchestration).

- The **grandparent** of UI architectural patterns — most others (MVP, MVT, MVVM) are MVC variants.
- The core idea: **separate data (Model) from presentation (View)** so each can change independently.

**One-liner:** split the app into Model (what it is), View (what you see), and Controller (what handles input).

## 2. MVC Core Concepts

| Component | Responsibility |
|---|---|
| **Model** | Data, business rules, state. Notifies the View of changes (via Observer pattern). |
| **View** | Renders the Model's data. Observes the Model for changes. |
| **Controller** | Handles user input. Updates the Model. Does NOT update the View directly. |

**Key point:** the Model is independent — it doesn't know about Views or Controllers. The View listens to the Model. The Controller modifies the Model.

## 3. How MVC Works

```
User input → Controller → updates Model → notifies View → re-renders
```

1. User interacts with the View (clicks, types).
2. Controller handles the event, calls methods on the Model.
3. Model updates its state, notifies observers (the View).
4. View reads the updated Model and re-renders.

## 4. Where MVC Is Used

- **Server-side web frameworks** — Ruby on Rails, ASP.NET MVC, Spring MVC, Express (when structured this way)
- **iOS/macOS** — Cocoa MVC (View and Controller are often merged in practice)
- The **conceptual foundation** for MVP, MVT, and MVVM

## 5. MVC Examples

### Example 1 — Express.js (Structured as MVC)

```javascript
// Model (models/order.js)
class Order {
  constructor(id, items) { this.id = id; this.items = items; }
  get total() { return this.items.reduce((s, i) => s + i.price, 0); }
}

// Controller (controllers/orders.js)
class OrdersController {
  constructor(orderService) { this.service = orderService; }
  async index(req, res) {
    const orders = await this.service.findAll();   // business logic
    res.render("orders/list", { orders });         // pass to View
  }
}

// View (views/orders/list.ejs) — template rendering
```

**Why:** the controller orchestrates (fetch data → hand to view); the model holds data + rules; the view renders HTML. Each can be tested independently.

## 6. MVC Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Fat controllers | Business logic in HTTP handlers | Move logic to Model/Service layer |
| Anemic models | Models are just data bags | Put business rules in Models |
| View knows too much | View does data fetching/logic | View only renders; Controller provides data |
| Tight Model-View coupling | Changing UI requires Model changes | Observer pattern decouples |

---

## 7. What Is MVP?

**MVP (Model–View–Presenter)** is a derivative of MVC where the **Presenter** replaces the Controller — it mediates ALL communication between Model and View, which are completely decoupled.

- The **View is passive** — it exposes an interface, and the Presenter tells it exactly what to display.
- The Presenter is **testable** in isolation — you mock the View interface.

**One-liner:** the Presenter is the middleman — the View and Model never talk directly.

## 8. MVP vs MVC

| | MVC | MVP |
|---|---|---|
| View–Model relationship | View observes Model directly | View and Model do NOT interact |
| Middle layer | Controller (handles input) | Presenter (handles input + tells View what to display) |
| Testability | Medium | High (Presenter is UI-framework-free) |
| Best for | Web apps (server-side) | Desktop apps, Android, complex UIs |

**Rule of thumb:** MVP when the View is complex and you want the UI logic **unit-testable without the UI framework**.

## 9. How MVP Works

```
User input → View → Presenter → updates Model → Presenter → tells View to update
```

1. View receives user input, delegates it to the Presenter (via an interface method).
2. Presenter processes, updates the Model.
3. Presenter reads the updated Model, calls methods on the View interface to update the display.
4. The View and Model **never know about each other**.

## 10. Where MVP Is Used

- **Android development** (classic Android architecture pre-Jetpack)
- **Desktop applications** (WinForms, some WPF patterns)
- **GWT (Google Web Toolkit)** applications
- When **testability of UI logic** is the primary concern

## 11. MVP Examples

```python
# View interface — the Presenter depends on this, not a concrete UI
class OrdersView(Protocol):
    def show_orders(self, orders: list[Order]): ...
    def show_error(self, message: str): ...
    def show_loading(self): ...
    def hide_loading(self): ...

# Presenter — framework-free, completely unit-testable
class OrdersPresenter:
    def __init__(self, view: OrdersView, service: OrderService):
        self.view = view
        self.service = service

    async def load_orders(self):
        self.view.show_loading()
        try:
            orders = await self.service.get_all()
            self.view.show_orders(orders)
        except Exception as e:
            self.view.show_error(str(e))
        finally:
            self.view.hide_loading()

# Concrete View (Android Activity, React component, etc.) implements the interface
class AndroidOrdersActivity(OrdersView): ...
class ReactOrdersComponent(OrdersView): ...
```

**Why:** swap `AndroidOrdersActivity` with `ReactOrdersComponent` — zero changes to the Presenter. The Presenter's logic is testable with a mock View.

## 12. MVP Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Bloated Presenter | God Presenter doing everything | Delegate to services/use-cases |
| View doing logic | Logic leaks into the concrete View | Keep View purely display/input handling |
| Not using an interface for View | Presenter tied to a concrete UI framework | Define a View interface (Protocol) |
| Overhead for simple screens | Presenter + interface boilerplate | For simple UIs, MVP may be overkill |

---

## 13. What Is MVT?

**MVT (Model–View–Template)** is Django's architectural pattern — an MVC variant where the **View** (Django's term) acts as the controller/orchestrator, and the **Template** handles presentation.

- In Django's terminology: **Model** = data layer (ORM), **View** = request handler (receives request, fetches data, returns response), **Template** = presentation (HTML with Django Template Language).
- Django's "View" is closer to what other frameworks call a Controller.

**One-liner:** Django's MVC variant — Model (data), View (orchestrator), Template (presentation).

## 14. MVT vs MVC

| | MVC | MVT (Django) |
|---|---|---|
| Controller / View | Controller handles input | View handles input + orchestration |
| View / Template | View renders output | Template renders output |
| Model | Same (data + business logic) | Same (ORM models) |
| Who renders? | The View | The Template (with View providing data) |

**Key point:** in Django's MVT, "View" means "the function that decides *what* to show"; "Template" means "the file that decides *how* to show it."

## 15. How MVT Works

```
HTTP Request → URLconf → View → (reads/writes) Model → renders Template → HTTP Response
```

1. A request arrives; Django's **URLconf** maps it to a **View**.
2. The **View** fetches/persists data via **Models** (ORM).
3. The View returns an HTTP response by **rendering a Template** with the data (a "context").

## 16. Where MVT Is Used

- **Django** and Django REST Framework (where DRF serializers replace templates for JSON APIs).
- Any system built on the Django framework.

## 17. MVT Examples

```python
# Model (models.py) — data + business rules
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_deliverable(self) -> bool:
        return self.status == "paid" and self.items.exists()

# View (views.py) — orchestration: fetch data, pass to template
def order_detail(request, order_id):
    order = get_object_or_404(Order.objects.select_related("customer").prefetch_related("items"), id=order_id)
    return render(request, "orders/detail.html", {"order": order})

# Template (templates/orders/detail.html) — presentation only
<h1>Order #{{ order.id }}</h1>
<p>Customer: {{ order.customer.name }}</p>
<ul>
  {% for item in order.items.all %}
    <li>{{ item.product.name }} — {{ item.quantity }}x</li>
  {% endfor %}
</ul>
```

**Why:** the Model owns data + rules; the View fetches and hands data to the Template; the Template renders HTML. Business logic (`is_deliverable`) lives in the Model, not the View or Template.

## 18. MVT Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Logic in templates | Business rules in `{% if %}` blocks | Move to Model properties/methods |
| Fat views | Views doing too much (validation, business logic, data fetching) | Services layer; views only orchestrate |
| N+1 in templates | Templates triggering extra queries | `select_related`/`prefetch_related` in the View |
| Anemic models | Models are just tables, no behavior | Add properties, methods, managers |

---

## 19. What Is MVVM?

**MVVM (Model–View–ViewModel)** is a pattern where the **ViewModel** exposes Model data and commands to the **View** via **data binding** — the View automatically reflects ViewModel state without explicit View-update code.

- The View **binds** to properties on the ViewModel; when properties change, the View updates automatically.
- The ViewModel transforms Model data into View-ready formats and handles View commands.

**One-liner:** the View binds to the ViewModel; data flows both ways automatically via binding.

## 20. MVVM vs MVC/MVP

| | MVC | MVP | MVVM |
|---|---|---|---|
| View–Logic relationship | View observes Model | Presenter tells View | View binds to ViewModel |
| Coupling | Medium | Low | Low (binding framework handles updates) |
| Data flow | Model → View (push) | Presenter → View (push) | ViewModel ↔ View (two-way binding) |
| Best for | Server-side web | Complex desktop/mobile | Data-binding frameworks (Angular, WPF, SwiftUI) |

**Rule of thumb:** MVVM when the **framework supports data binding** (Angular, WPF, SwiftUI, Android Jetpack) — the binding removes boilerplate Presenter→View update code.

## 21. How MVVM Works

```
View ← (data binding) → ViewModel → Model
  ↑ User input flows to ViewModel via binding
  ↓ ViewModel state changes flow to View via binding
```

1. The View **declares bindings** to ViewModel properties (e.g., `[(ngModel)]="user.name"`).
2. User changes in the View **automatically update** ViewModel properties.
3. ViewModel property changes **automatically update** the View.
4. The ViewModel mediates all data transformation and commands.

## 22. Where MVVM Is Used

- **Angular** (TypeScript, RxJS/Signals, two-way binding via `[(ngModel)]`)
- **WPF / Xamarin / .NET MAUI** (C# / XAML with data binding)
- **SwiftUI / Jetpack Compose** (declarative UI with state binding)
- **Vue.js** (reactive data + template binding — effectively MVVM-inspired)
- **Knockout.js** (the original JavaScript MVVM library)

## 23. MVVM Examples

### Example 1 — Angular Component (MVVM in Practice)

```typescript
// ViewModel: the component class (exposes state + commands)
@Component({
  template: `
    <input [(ngModel)]="searchTerm" (ngModelChange)="onSearch()" />
    <ul>
      <li *ngFor="let r of results">{{ r.name }}</li>
    </ul>
  `,
})
export class SearchComponent {
  searchTerm = signal("");
  results = signal<Result[]>([]);

  constructor(private searchService: SearchService) {}

  onSearch() {
    this.searchService.search(this.searchTerm())
      .subscribe(data => this.results.set(data));
  }
}
```

**Why:** `[(ngModel)]` = two-way binding between input and `searchTerm`. When `searchTerm` changes, the input updates. When the user types, `searchTerm` updates. No manual DOM manipulation — the binding handles it.

### Example 2 — Vue.js (MVVM-Inspired)

```vue
<template>
  <input v-model="searchTerm" @input="onSearch" />
  <li v-for="r in results" :key="r.id">{{ r.name }}</li>
</template>

<script setup>
const searchTerm = ref("");
const results = ref([]);
function onSearch() {
  results.value = await searchService.search(searchTerm.value);
}
</script>
```

**Why:** `v-model` = two-way binding; `ref` = reactive state. Vue re-renders only where `results` is referenced — granular reactivity.

## 24. MVVM Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Bloated ViewModel | ViewModel doing everything (data + presentation + commands) | Extract services, separate commands |
| Over-binding complex expressions | Template logic becomes unreadable | Keep bindings simple; pre-compute in ViewModel |
| Memory leaks from bindings | Observables/subscriptions not cleaned up | Use async pipe / lifecycle hooks to unsubscribe |
| Too many watchers/bindings | Performance degradation | OnPush / computed properties / `trackBy` |

---

# Structural & Behavioral Patterns

## 25. Singleton

Ensure a class has **only one instance** and provide a global access point.

- Use for: database connection pools, configuration objects, logger instances, caches.
- Warning: Singletons introduce global state — use sparingly (DI containers often manage "singleton" lifetime without the pattern itself).

**Example (TypeScript):**
```typescript
class Config {
  private static instance: Config;
  private constructor(private env: Record<string, string>) {}
  static getInstance(): Config {
    if (!Config.instance) Config.instance = new Config(process.env);
    return Config.instance;
  }
  get(key: string): string { return this.env[key]; }
}
```

**Modern alternative:** Dependency Injection containers (NestJS, Angular, Spring) manage singleton lifetimes — you don't manually implement the pattern.

## 26. Factory & Abstract Factory

Create objects **without specifying the exact class** — the factory decides which concrete class to instantiate.

- **Simple Factory:** one method that returns different objects based on input.
- **Abstract Factory:** a family of factories, each creating a family of related objects.

**Where used:** payment gateways (Stripe vs PayPal), cloud providers (AWS vs Azure), database drivers, UI component libraries.

**Example:**
```python
class PaymentGatewayFactory:
    @staticmethod
    def create(provider: str) -> PaymentGateway:
        match provider:
            case "stripe": return StripeAdapter()
            case "paypal": return PayPalAdapter()
            case _: raise ValueError(f"Unknown provider: {provider}")
```

## 27. Observer / Pub-Sub

Define a **one-to-many dependency** — when one object (subject) changes state, all dependents (observers) are notified automatically.

- **Observer:** observers register directly with the subject (tight coupling).
- **Pub/Sub:** publishers and subscribers communicate through an event bus/broker (loose coupling — see Event-Driven in `architecture-patterns.md`).

**Where used:** event handling, reactive state (RxJS, Signals), UI updates on data change, MVC's Model→View notification.

**Example (RxJS):**
```typescript
const subject = new Subject<Order>();
subject.subscribe(order => console.log("Billing:", order));    // observer 1
subject.subscribe(order => console.log("Inventory:", order));  // observer 2
subject.next(newOrder);   // both observers notified
```

## 28. Strategy

Define a **family of interchangeable algorithms** and let the client choose which one to use — without changing the client code.

- Use for: sorting strategies, pricing/discount rules, validation rules, compression algorithms.

**Example:**
```python
class DiscountStrategy(Protocol):
    def apply(self, total: Decimal) -> Decimal: ...

class NoDiscount(DiscountStrategy):
    def apply(self, total): return total

class PercentageDiscount(DiscountStrategy):
    def __init__(self, pct): self.pct = pct
    def apply(self, total): return total * (1 - self.pct)

class OrderService:
    def calculate(self, order, discount: DiscountStrategy):
        return discount.apply(order.subtotal)
```

## 29. Repository

Mediate between the **domain layer and data storage** — the domain works with repositories (interfaces), not with databases directly.

- Use for: abstracting database access, enabling unit testing by mocking repositories, swapping storage backends.
- See `case/structures-architecture/backend-systems.md` §9–16 for detailed layering.

**Example:**
```typescript
interface OrderRepository {
  findById(id: string): Promise<Order>;
  save(order: Order): Promise<void>;
}

class PostgresOrderRepo implements OrderRepository { /* SQL */ }
class InMemoryOrderRepo implements OrderRepository { /* for tests */ }
```

## 30. Adapter / Wrapper

Convert the **interface of a class into another interface** that clients expect — lets incompatible interfaces work together.

- Use for: third-party API integration, legacy system wrappers, normalizing different vendor formats.
- See `case/api/apis-and-communication.md` §49–56 for the full integration pattern.

**Example:** wrapping Stripe's API behind your `PaymentGateway` interface so your business logic never imports Stripe. Swap to PayPal = write a new adapter, zero changes to business code.

## 31. Decorator

Attach **additional responsibilities** to an object dynamically — a flexible alternative to subclassing.

- Use for: logging, caching, auth checks, retry logic, metrics — cross-cutting concerns added without modifying the original class.
- Language-specific: Python `@decorator`, TypeScript decorators, Java annotations.

**Example (Python):**
```python
def with_retry(max_attempts=3):
    def decorator(fn):
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try: return await fn(*args, **kwargs)
                except TransientError:
                    if attempt == max_attempts - 1: raise
                    await asyncio.sleep(2 ** attempt)
        return wrapper
    return decorator

@with_retry(max_attempts=3)
async def call_external_api(): ...
```

## 32. Dependency Injection

Instead of a class creating its own dependencies, they're **provided (injected)** from outside — usually by a DI container.

- Use for: decoupling, testability (inject mocks), swapping implementations.
- Frameworks with built-in DI: Angular, NestJS, Spring Boot, FastAPI (`Depends`).

**Example (NestJS):**
```typescript
@Injectable()
class OrdersService {
  constructor(
    @Inject("IOrderRepo") private repo: OrderRepository,  // injected, not created
    @Inject("IPaymentGateway") private payment: PaymentGateway,
  ) {}
}
```

---

## Shared Foundations

Concepts that recur across **all patterns**:

- **Separation of concerns** — the universal goal. MVC/MVP/MVT/MVVM all split presentation from data; Repository splits domain from storage; Adapter splits your code from vendor code.
- **Program to interfaces, not implementations** — MVP's View interface, Repository pattern, Adapter pattern, and DI all depend on abstractions so concrete implementations can be swapped.
- **Patterns compose, not compete** — a Django app (MVT) uses Repository + Adapter + Factory + Strategy internally. An Angular app (MVVM) uses Service (DI) + Observer (RxJS) + Strategy patterns.
- **Match pattern to complexity** — don't force MVP/MVVM on a simple page; don't use Singleton when DI handles it. Patterns solve problems; if there's no problem, there's no need.

## Quick Reference Card

```
ARCHITECTURAL PATTERN PICKER:
  Server-side web app (Rails, Express, Spring)? → MVC
  Complex UI, testable UI logic?                 → MVP
  Django web app?                                → MVT
  Framework with data binding (Angular, WPF)?    → MVVM
  Simple CRUD, no binding framework?             → MVC (server-side) or minimal pattern

STRUCTURAL/BEHAVIORAL PATTERNS:
  One instance only?                     → Singleton (or DI singleton scope)
  Create objects without knowing class?  → Factory
  Many things react to one change?       → Observer / Pub-Sub
  Swappable algorithm?                   → Strategy
  Isolate data access?                   → Repository
  Incompatible interfaces?               → Adapter
  Add behavior without subclassing?      → Decorator
  Decouple from dependencies?            → Dependency Injection

GOLDEN RULES:
  ✓ Patterns SOLVE problems — don't apply without a problem
  ✓ Depend on abstractions, not concretions
  ✓ Patterns compose; choose per concern
  ✓ Match architectural pattern to framework conventions
  ✓ Testability is the best indicator of a good separation
```
