# Technologies, Libraries, Packages & Tools

## Core Languages & Web Standards

- **React 19+** — JavaScript library for building component-based, declarative user interfaces with the latest features and concurrent rendering capabilities.
- **Next.js 15+** — React meta-framework providing App Router, file-based routing, server-side rendering, static generation, and full-stack capabilities.
- **TypeScript** — Strongly typed superset of JavaScript that adds static type checking, interfaces, and generics for safer, more maintainable code.
- **JavaScript (ES6+)** — Core scripting language for the web, using modern ECMAScript features such as arrow functions, destructuring, modules, async/await, and more.
- **HTML5** — Latest version of the HyperText Markup Language providing semantic elements, native form validation, multimedia APIs, and improved document structure.
- **CSS3** — Latest CSS specification offering flexbox, grid, animations, custom properties (variables), media queries, and advanced selectors for modern web styling.

## Styling Solutions

- **Tailwind CSS** — Utility-first CSS framework that composes designs directly in markup using pre-defined utility classes, promoting rapid UI development and consistent design.
- **Material UI (MUI)** — Comprehensive React component library implementing Google's Material Design principles with a rich set of pre-built, customizable UI components.
- **CSS Modules** — Approach that locally scopes CSS class names by default per component/file, eliminating global namespace collisions.
- **Sass/SCSS** — CSS preprocessor extending CSS with variables, nested rules, mixins, functions, and inheritance for more expressive and maintainable stylesheets.
- **Styled Components** — CSS-in-JS library that lets you write actual CSS syntax inside JavaScript/TypeScript, creating React components with co-located, dynamic styles.
- **Emotion** — High-performance CSS-in-JS library offering both a styled-component API and a css-prop approach with powerful composition and theming capabilities.
- **shadcn/ui** — Modern component collection and code distribution platform that integrates by copying source code directly into your project, giving full control over component implementation.

## State Management & Data Fetching

- **Redux Toolkit** — Official, opinionated toolset for Redux state management providing simplified store setup, reducer logic, and immutable update patterns with built-in best practices.
- **Zustand** — Lightweight, minimalistic state management library for React with a simple hook-based API, no boilerplate, and no provider wrapping required.
- **TanStack Query** — Powerful data-fetching and server-state management library handling caching, background refetching, pagination, and mutations for REST and GraphQL APIs (formerly React Query).
- **Context API** — React's built-in mechanism for passing data through the component tree without prop drilling, suitable for global state like themes, auth, or locale.

## APIs & Communication

- **REST APIs** — Representational State Transfer architectural style using standard HTTP methods (GET, POST, PUT, DELETE) for structured client-server communication.
- **GraphQL APIs** — Query language and runtime that lets clients request exactly the data they need from a typed schema, reducing over-fetching and under-fetching.
- **WebSockets** — Protocol providing full-duplex, persistent communication channels over a single TCP connection for real-time bidirectional data flow.
- **Server-Sent Events (SSE)** — Standard allowing servers to push real-time updates to browsers over HTTP, ideal for one-way streaming like notifications or live feeds.

## Authentication & Security

- **OAuth** — Open standard for access delegation, enabling third-party applications to obtain limited access to user accounts without exposing credentials.
- **JWT (JSON Web Tokens)** — Compact, URL-safe token format for securely transmitting claims between parties, commonly used for stateless authentication and authorization.

## Next.js Architecture Features

- **Next.js App Router** — File-system-based routing system (introduced in Next.js 13+) using `app/` directory with layouts, loading states, error boundaries, and nested routing.
- **React Server Components** — Components that render exclusively on the server, shipping zero client-side JavaScript, reducing bundle size and improving performance.
- **Client Components** — Traditional interactive React components rendered in the browser, enabling event handlers, hooks, state, effects, and browser APIs.
- **Server Actions** — Server-side async functions that can be called directly from Client Components, handling form submissions and data mutations without a separate API route.
- **Route Handlers** — Custom request handlers defined in the App Router (`route.ts` files) replacing API Routes, supporting Web-standard Request/Response objects.
- **Middleware** — Code that executes before a request is completed, enabling request rewriting, redirects, header modification, and authentication checks at the edge.
- **React Router** — Client-side routing library for React applications (used outside or alongside Next.js) enabling declarative, component-based routing with dynamic segments.

## Rendering Strategies

- **SSR (Server-Side Rendering)** — Technique of rendering React components into HTML on the server per incoming request, improving initial load performance and SEO.
- **SSG (Static Site Generation)** — Process of pre-rendering pages into static HTML at build time, serving them instantly from a CDN with minimal server overhead.
- **ISR (Incremental Static Regeneration)** — Strategy that allows updating static pages after build time on a per-page basis, re-generating pages in the background when new data arrives.
- **Streaming** — Progressive rendering approach that sends HTML chunks to the browser as they become ready, enabling faster Time-to-First-Byte and improved perceived performance.
- **PPR (Partial Prerendering)** — Experimental Next.js feature combining static and dynamic content within the same page, prerendering static shell while streaming dynamic content.

## Performance & Quality

- **Core Web Vitals** — Google's standardized set of user-centric metrics (LCP, INP, CLS) measuring loading, interactivity, and visual stability for real-world web performance.
- **WCAG (Web Content Accessibility Guidelines)** — Internationally recognized standards for making web content accessible to people with disabilities, covering perceivable, operable, understandable, and robust principles.
- **SEO (Search Engine Optimization)** — Practices and techniques to improve a website's visibility and ranking in search engine results through technical, on-page, and content optimizations.

## Development & DevOps Tools

- **Git** — Distributed version control system for tracking source code changes, enabling collaborative development, branching, merging, and history management.
- **CI/CD Pipelines** — Automated workflows for Continuous Integration (automated build/test on commit) and Continuous Deployment/Delivery (automated release to environments).
- **Docker** — Containerization platform that packages applications and their dependencies into lightweight, portable containers for consistent deployment across environments.
- **Cloud Deployment Platforms** — Services and infrastructure (such as Vercel, AWS, Google Cloud, Azure) for hosting, scaling, and managing web applications in the cloud.

## AI-Assisted Development Tools

- **GitHub Copilot** — AI-powered code completion and generation tool that integrates with IDEs, suggesting whole lines and functions based on context and comments.
- **Cursor** — AI-first code editor that deeply integrates large language models into the development workflow for code generation, explanation, and refactoring.
- **ChatGPT** — OpenAI's conversational AI model used for generating code, debugging, explaining concepts, and assisting with software development tasks.
- **Claude Code** — Anthropic's AI-powered CLI coding assistant that helps with codebase exploration, editing, debugging, and software engineering tasks directly in the terminal.
