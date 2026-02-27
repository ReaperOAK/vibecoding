# Multi-Tenant Core & Team Isolation — L3 Actionable Tasks

## FF-BE001-001: Implement Tenant Model & DB Partitioning

**Status:** READY
**Priority:** P1
**Owner:** Backend
**Depends On:** FF-BE008-001
**Effort:** 2h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Add tenant_id to all relevant tables in Prisma schema
2. Enforce RLS in PostgreSQL and Prisma
3. Migrate DB and test tenant isolation

**File Paths:**
- prisma/schema.prisma
- prisma/migrations/

**Acceptance Criteria:**
- [ ] tenant_id present on all tables
- [ ] RLS policies enforced in DB and Prisma
- [ ] Migration runs without errors
- [ ] Tenant isolation verified by tests
- [ ] All code committed

**Description:**
Implement tenant-aware DB schema and enforce row-level security for all data access. Ensure strict tenant isolation.

---

## FF-BE001-002: Build Tenant Context Middleware

**Status:** READY
**Priority:** P1
**Owner:** Backend
**Depends On:** FF-BE001-001
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Create middleware to extract tenant from JWT/session
2. Inject tenant context into all API requests
3. Test middleware for all routes

**File Paths:**
- app/api/middleware/tenant.ts
- app/context/tenant.ts

**Acceptance Criteria:**
- [ ] Middleware extracts tenant from JWT/session
- [ ] Tenant context injected into API
- [ ] All routes tested for tenant context
- [ ] Middleware code committed

**Description:**
Build middleware to extract and inject tenant context for all API requests. Ensure all routes are tenant-aware.

---

## FF-BE001-003: Workspace Switching & Onboarding (UI/API)

**Status:** READY
**Priority:** P2
**Owner:** Backend, Frontend
**Depends On:** FF-BE001-002
**Effort:** 2h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Implement UI/API for switching workspaces
2. Add onboarding flow for new tenants
3. Test switching and onboarding

**File Paths:**
- app/onboarding/
- app/api/tenants/

**Acceptance Criteria:**
- [ ] Workspace switching functional in UI/API
- [ ] Onboarding flow for new tenants
- [ ] All flows tested
- [ ] UI and API code committed

**Description:**
Enable workspace switching and onboarding for new tenants. Ensure seamless experience for team admins and members.

---

## FF-BE001-004: Ensure Tenant-Aware API & File Access

**Status:** READY
**Priority:** P1
**Owner:** Backend
**Depends On:** FF-BE001-002
**Effort:** 2h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Audit all API endpoints for tenant scoping
2. Enforce tenant checks on file uploads/downloads
3. Add tests for tenant-aware access

**File Paths:**
- app/api/
- app/api/files/

**Acceptance Criteria:**
- [ ] All API endpoints enforce tenant scoping
- [ ] File access restricted by tenant
- [ ] Tests cover tenant-aware access
- [ ] All code committed

**Description:**
Ensure all API and file flows are tenant-scoped. Add tests to verify strict tenant-aware access.

---

## FF-BE001-005: Implement Tenant Branding & Settings

**Status:** READY
**Priority:** P2
**Owner:** Backend, Frontend
**Depends On:** FF-BE001-003
**Effort:** 2h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Add per-tenant branding (logo, colors) and settings
2. Implement UI for branding/settings management
3. Test branding/settings flows

**File Paths:**
- app/settings/branding.tsx
- app/api/tenants/settings.ts

**Acceptance Criteria:**
- [ ] Per-tenant branding/settings stored in DB
- [ ] UI for managing branding/settings
- [ ] All flows tested
- [ ] UI and API code committed

**Description:**
Support per-tenant branding and settings. Provide UI for admins to manage branding and preferences.

---
