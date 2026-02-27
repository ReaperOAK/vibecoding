# FreelanceFlow System Architecture

## 1. Technology Stack Selection

**Frontend:** Next.js 15 (App Router), TypeScript, React 19, TailwindCSS v4, shadcn/ui
- *Rationale:* Modern, composable UI, SSR/SSG, best-in-class DX, rapid iteration, strong ecosystem.

**Backend:** Next.js API routes + tRPC (preferred for type safety, monorepo simplicity). Optionally, a separate Node.js/Express service for heavy async jobs.
- *Rationale:* Unified stack, type-safe API, easy SSR, scalable for MVP and beyond.

**Database:** PostgreSQL (multi-tenant, shared DB, tenant_id column), Prisma ORM
- *Rationale:* Mature, scalable, strong RLS support, easy migrations, fits SaaS needs.

**Auth:** NextAuth.js v5 (Auth.js), JWT + session
- *Rationale:* Secure, flexible, supports social/email, integrates with Next.js.

**Real-time:** SSE (for notifications) or Socket.io (for chat/live updates)
- *Rationale:* Real-time UX, scalable, fits notification and collaboration needs.

**File Storage:** S3-compatible (Cloudflare R2 or AWS S3)
- *Rationale:* Cost-effective, scalable, easy integration, supports presigned URLs.

**Document Parsing:** pdf-parse, mammoth.js, tesseract.js (OCR)
- *Rationale:* Covers PDF, DOCX, image OCR for deliverables.

**Payment:** Stripe SDK + webhooks
- *Rationale:* Industry standard, usage-based billing, secure, global.

**Deployment:** Docker (local dev), Vercel (frontend), containerized backend (cloud)
- *Rationale:* Fast local onboarding, scalable prod, CI/CD ready.

**Monitoring:** Sentry (errors), OpenTelemetry (traces)
- *Rationale:* Proactive error and performance monitoring.

**Testing:** Vitest (unit), Playwright (E2E), Storybook + Chromatic (visual)
- *Rationale:* Modern, fast, covers all test types.

---

## 2. Multi-Tenant Architecture
- Shared PostgreSQL DB, all tables have `tenant_id` column
- Row-Level Security (RLS) enforced in DB and Prisma
- Tenant context middleware (extracts tenant from JWT claims)
- Subdomain-based (team.myapp.com) or path-based (/t/team) routing
- All API, file, and notification flows are tenant-aware

---

## 3. Component Boundaries & Project Structure
See [Project Structure](#project-structure) below. Clear separation of app (frontend), server (backend logic), db (schema/migrations), components (UI), and shared lib/types/hooks.

---

## 4. Well-Architected Pillars
- **Operational Excellence:** CI/CD, health checks, error monitoring, automated tests
- **Security:** RLS, JWT, RBAC, S3 ACLs, Stripe PCI compliance
- **Reliability:** Managed DB, container orchestration, health checks, retries
- **Performance:** SSR/SSG, CDN, indexed queries, async jobs
- **Cost:** Cloudflare R2, serverless, usage-based billing
- **Sustainability:** Automated scaling, efficient resource use

---

## 5. ADRs (Architecture Decision Records)
- **Monorepo, modular monolith** for MVP and scale-up
- **tRPC** for type-safe API, not REST
- **Shared DB with RLS** for multi-tenancy
- **Presigned S3 uploads** for file pipeline
- **Stripe for billing** (no homegrown billing logic)
- **SSE/Socket.io** for real-time
- **Prisma ORM** for DB access

---

## 6. Implementation DAG (High-Level)
1. Multi-tenant core
2. Auth & RBAC
3. Client management
4. Project/milestone management
5. Time tracking
6. Invoicing & Stripe
7. File uploads & parsing
8. Real-time notifications
9. Client portal
10. Monitoring & CI/CD

---

## 7. Project Structure
See below for detailed structure.
