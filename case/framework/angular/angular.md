# Angular — Complete Guide

> **Series:** Framework Documentation
> Angular — the opinionated, TypeScript-first frontend framework (Google-maintained, enterprise-grade). Related: `case/framework/nestjs/nestjs.md` (the backend counterpart — same patterns, server-side), `case/state-management/react-state-management.md` (Redux — Angular's state management inspiration), `case/structures-architecture/design-patterns.md` (MVC/MVVM §1–16), `case/api/apis-and-communication.md` (REST §1–8).

---

## Table of Contents

- [1. What Is Angular?](#1-what-is-angular)
- [2. Angular vs React vs Vue](#2-angular-vs-react-vs-vue)
- [3. How Angular Works](#3-how-angular-works)
- [4. Core Concepts and Features](#4-core-concepts-and-features)
- [5. Where to Use Angular](#5-where-to-use-angular)
- [6. Where NOT to Use Angular](#6-where-not-to-use-angular)
- [7. Installation and Setup](#7-installation-and-setup)
- [8. Project Structure and Configuration](#8-project-structure-and-configuration)
- [9. Angular Production Best Practices](#9-angular-production-best-practices)
- [10. Angular Real-World Examples](#10-angular-real-world-examples)
- [11. Angular Pitfalls](#11-angular-pitfalls)

---

## 1. What Is Angular?

**Angular** (2+) is a **TypeScript-first, opinionated, component-based** frontend framework built by Google — providing a complete platform with **dependency injection, two-way data binding, RxJS reactivity, routing, forms, HTTP client, and testing utilities** out of the box.

- **"Batteries included"** — Angular ships with everything needed for a large-scale SPA: router, forms, HTTP, animations, i18n, PWA support.
- **TypeScript-first** — every Angular app is TypeScript; the ecosystem assumes strong typing.
- **RxJS (Reactive Extensions)** — async data flows are modeled as observable streams, not promises.
- Note: **AngularJS (1.x)** is a completely different framework — this file covers Angular 2+.

**One-liner:** the opinionated, enterprise-grade TypeScript frontend framework — everything you need, structured by default.

## 2. Angular vs React vs Vue

| | Angular | React | Vue |
|---|---|---|---|
| Philosophy | Opinionated full framework | Flexible UI library | Progressive framework |
| Language | TypeScript (first-class) | JavaScript/TS (optional) | JavaScript/TS (optional) |
| Architecture | MVC/MVVM, DI, services | Component + hooks | Component + reactivity |
| State management | RxJS + NgRx / Signals | External (Redux, Zustand) | Pinia / Vuex |
| Learning curve | Steep (many concepts) | Moderate | Gentle |
| Best for | Enterprise/team-built SPAs | Flexible apps of any size | Small–medium apps, gradual adoption |

**Rule of thumb:** Angular for **large, enterprise SPAs with teams that benefit from structure and convention**; React for **flexibility and ecosystem breadth**; Vue for **simplicity and progressive adoption**.

## 3. How Angular Works

- **Component tree** — the UI is a hierarchy of components, each with a template (HTML), class (logic), and styles (CSS).
- **Modules (NgModules)** group related components, services, and pipes into cohesive blocks (standalone components increasingly replace them in modern Angular).
- **Dependency injection (DI)** — services are registered in an injector and injected into components/other services via constructor parameters.
- **Change detection** — Angular's zone-based system detects when data changes and updates the DOM accordingly (supplemented by `OnPush` strategy for performance).
- **RxJS** — HTTP requests, routing params, form changes, and inter-component communication flow through observable streams.

## 4. Core Concepts and Features

| Concept | What it is |
|---|---|
| **Components** | `@Component` decorator — template + class + styles = a reusable UI piece |
| **Templates** | HTML with Angular-specific syntax: `*ngIf`, `*ngFor`, `[property]`, `(event)`, `[(ngModel)]` |
| **Services / DI** | `@Injectable` classes with business logic; injected via constructor |
| **Modules** | `@NgModule` groups components/services; `Standalone Components` (v14+) remove the need |
| **Routing** | `@angular/router` — lazy-loaded route config, guards, resolvers |
| **Forms** | Template-driven (simple) and Reactive (complex, testable) |
| **HttpClient** | `@angular/common/http` — typed HTTP requests returning observables |
| **Pipes** | Transform data in templates (`date`, `currency`, `async` for observables) |
| **Directives** | Attribute (`ngClass`, `ngStyle`) and structural (`*ngIf`, `*ngFor`) |
| **RxJS** | Observables, operators (`map`, `switchMap`, `debounceTime`), Subjects |
| **Signals** (v16+) | Fine-grained reactivity — a simpler alternative to RxJS for local state |
| **Angular CLI** | Scaffold, build, test, and deploy from the terminal |

## 5. Where to Use Angular

- **Enterprise dashboards and admin panels** — the structure scales with large teams.
- **Large SPAs** needing strong conventions and consistency.
- **Teams that want everything included** — router, forms, HTTP, i18n built in.
- **TypeScript-mandatory** organizations.
- **Progressive Web Apps (PWAs)** — Angular has first-class PWA support (`@angular/pwa`).

## 6. Where NOT to Use Angular

- **Small/static sites** — the framework overhead exceeds the payoff.
- **Teams wanting flexibility** — Angular is opinionated; React/Vue give more freedom.
- **Rapid prototyping** — the setup and boilerplate are heavier than React or Vue.
- **Server-rendered / SEO-critical** — use Angular Universal (SSR) or consider Next.js/Nuxt.
- **Teams without TypeScript/RxJS experience** — the learning curve is real.

## 7. Installation and Setup

```bash
npm install -g @angular/cli
ng new my-app --standalone --routing --style=scss
cd my-app && ng serve          # http://localhost:4200
```

```typescript
// app.component.ts — a minimal standalone component
import { Component } from "@angular/core";

@Component({
  selector: "app-root",
  standalone: true,
  template: `<h1>Hello {{ name }}</h1>
             <button (click)="toggle()">Toggle</button>`,
})
export class AppComponent {
  name = "Angular";
  toggle() { this.name = this.name === "Angular" ? "World" : "Angular"; }
}
```

## 8. Project Structure and Configuration

```
src/
├── main.ts                    # bootstrap (platform, root component)
├── app/
│   ├── app.component.ts       # root component
│   ├── app.routes.ts          # route configuration
│   ├── features/              # feature modules or standalone component folders
│   │   ├── orders/
│   │   │   ├── orders.component.ts      # logic + metadata
│   │   │   ├── orders.component.html    # template
│   │   │   ├── orders.component.scss    # scoped styles
│   │   │   └── orders.service.ts        # @Injectable business logic
│   │   └── users/ ...
│   ├── shared/                # shared components, pipes, directives
│   ├── core/                  # singleton services (auth, logging, guards)
│   └── models/                # TypeScript interfaces/types
├── environments/              # per-environment config
└── angular.json               # CLI configuration (build, serve, test)
```

- **Standalone components** (recommended since v14) eliminate NgModules.
- **Feature-based organization** — each domain (orders, users) is a self-contained folder.
- **Shared feature modules** for reusable UI; **Core module** for app-wide singletons.

## 9. Angular Production Best Practices

1. **Use standalone components** — NgModules are legacy; standalone reduces boilerplate.
2. **Lazy-load routes** — `loadComponent` / `loadChildren` to split bundles by route.
3. **`OnPush` change detection** — skip change detection unless inputs/references change (big perf win).
4. **Unsubscribe from observables** — use `async` pipe (auto-unsubscribes) or `takeUntilDestroyed()` (v16+).
5. **Reactive forms** for complex forms — more testable, more predictable than template-driven.
6. **State management** — NgRx (Redux pattern) for complex global state; Signals for local/medium state.
7. **Keep templates simple** — logic in the component class, not in the template.
8. **Use `trackBy`** with `*ngFor` to avoid re-rendering entire lists.
9. **AOT compilation** (default in production builds) — faster rendering, smaller bundles.
10. **Barrel exports** (`index.ts` re-exporting a folder's public API) for clean imports.

## 10. Angular Real-World Examples

### Example 1 — Reactive Form + Service

```typescript
// orders.service.ts
@Injectable({ providedIn: "root" })
export class OrdersService {
  constructor(private http: HttpClient) {}
  getOrders(): Observable<Order[]> {
    return this.http.get<Order[]>("/api/orders");
  }
  create(dto: CreateOrderDto): Observable<Order> {
    return this.http.post<Order>("/api/orders", dto);
  }
}

// orders.component.ts
@Component({
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, AsyncPipe],
  template: `
    <form [formGroup]="form" (ngSubmit)="submit()">
      <input formControlName="customerId" />
      <button type="submit" [disabled]="form.invalid">Create</button>
    </form>
    <ul>
      <li *ngFor="let o of orders$ | async; trackBy: trackById">
        {{ o.id }} — {{ o.total | currency }}
      </li>
    </ul>
  `,
})
export class OrdersComponent {
  private service = inject(OrdersService);
  orders$ = this.service.getOrders();

  form = new FormGroup({
    customerId: new FormControl("", Validators.required),
  });

  submit() {
    this.service.create(this.form.value).subscribe(() => {
      this.orders$ = this.service.getOrders();   // refresh
      this.form.reset();
    });
  }

  trackById(_: number, item: Order) { return item.id; }
}
```

**Why:** form + data fetch + mutation in one cohesive component — services handle HTTP, components handle UI. `async` pipe auto-unsubscribes.

### Example 2 — Lazy-Loaded Route

```typescript
// app.routes.ts
export const routes: Routes = [
  { path: "orders", loadComponent: () =>
      import("./features/orders/orders.component").then(m => m.OrdersComponent) },
];
```

**Why:** the orders bundle loads only when the user navigates to `/orders` — smaller initial download.

### Example 3 — `OnPush` + Signals (Modern Reactivity)

```typescript
@Component({
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,   // big perf win
  template: `<p>{{ count() }}</p>
             <button (click)="inc()">+</button>`,
})
export class CounterComponent {
  count = signal(0);
  inc() { this.count.update(n => n + 1); }
}
```

**Why:** Signals give fine-grained reactivity; `OnPush` skips change detection except on signal updates — both fast.

### Example 4 — Interceptor for Auth Headers

```typescript
// auth.interceptor.ts
@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = localStorage.getItem("token");   // (better: HttpOnly cookie)
    if (token) {
      req = req.clone({ setHeaders: { Authorization: `Bearer ${token}` } });
    }
    return next.handle(req);
  }
}
```

**Why:** every HTTP request automatically carries the auth token — no per-call boilerplate.

## 11. Angular Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Default change detection everywhere | Slow, excessive DOM updates | `OnPush` + Signals / async pipe |
| Unsubscribed observables | Memory leaks, zombie logic | `async` pipe / `takeUntilDestroyed()` |
| Huge NgModule splitting | Slow initial load | Lazy-load routes + standalone components |
| Logic in templates | Hard to test, hard to read | Move logic to component class |
| Not using `trackBy` with `*ngFor` | Full list re-render on change | `trackBy: trackById` |
| Tight coupling to RxJS everywhere | Complexity for simple state | Use Signals (v16+) for local state |
| Direct DOM manipulation | Bypasses Angular's abstraction | Use Renderer2 / template bindings |
| No barrel files | Deep import paths (`../.../../../../service`) | `index.ts` re-exports |
