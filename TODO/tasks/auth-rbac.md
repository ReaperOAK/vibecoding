# Authentication & Authorization (RBAC) — L3 Actionable Tasks

## FF-BE008-001: Integrate NextAuth.js v5 for Authentication

**Status:** READY
**Priority:** P0
**Owner:** Backend
**Depends On:** FF-DO001-001, FF-DO001-002
**Effort:** 2h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Install and configure NextAuth.js v5 (Auth.js)
2. Set up email and social login providers
3. Configure JWT/session management

**File Paths:**
- app/api/auth/[...nextauth].ts
- prisma/schema.prisma
- .env

**Acceptance Criteria:**
- [ ] NextAuth.js v5 installed and configured
- [ ] Email/social login functional
- [ ] JWT/session management working
- [ ] Auth API routes tested
- [ ] Secrets managed via .env

**Description:**
Integrate NextAuth.js v5 for secure authentication, supporting email and social login. Ensure JWT/session management is robust and secrets are handled securely.

---

## FF-BE008-002: Define Roles & Permission Matrix (RBAC)

**Status:** READY
**Priority:** P1
**Owner:** Backend
**Depends On:** FF-BE008-001
**Effort:** 2h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Define roles (admin, member, client) in DB and code
2. Implement permission matrix for all routes
3. Enforce RBAC in API and UI

**File Paths:**
- prisma/schema.prisma
- app/api/middleware/role.ts
- app/context/permissions.ts

**Acceptance Criteria:**
- [ ] Roles defined in DB and code
- [ ] Permission matrix covers all routes
- [ ] RBAC enforced in API and UI
- [ ] Tests for role enforcement
- [ ] Documentation updated

**Description:**
Define and enforce a robust RBAC system with roles and permissions. Ensure all routes and UI respect the permission matrix.

---

## FF-BE008-003: Secure Session & Token Handling

**Status:** READY
**Priority:** P1
**Owner:** Backend
**Depends On:** FF-BE008-001
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Implement secure session storage
2. Add token rotation and logout logic
3. Test session expiration and invalidation

**File Paths:**
- app/api/auth/[...nextauth].ts
- app/utils/session.ts

**Acceptance Criteria:**
- [ ] Sessions stored securely
- [ ] Token rotation implemented
- [ ] Logout and expiration tested
- [ ] No session leakage or reuse
- [ ] All code committed

**Description:**
Ensure secure session and token handling, including rotation and logout. Test for session expiration and invalidation.

---

## FF-BE008-004: Add Protected Routes & Middleware

**Status:** READY
**Priority:** P1
**Owner:** Backend
**Depends On:** FF-BE008-002, FF-BE008-003
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Add middleware for route protection (API, UI)
2. Extract tenant context from JWT/session
3. Test protected routes for all roles

**File Paths:**
- app/api/middleware/auth.ts
- app/api/middleware/tenant.ts

**Acceptance Criteria:**
- [ ] Middleware protects all sensitive routes
- [ ] Tenant context extracted and enforced
- [ ] All roles tested for access
- [ ] No unauthorized access possible
- [ ] Middleware code committed

**Description:**
Add middleware to protect all sensitive routes and enforce tenant context. Test for correct access by all roles.

---

## FF-BE008-005: Implement User Invitation & Onboarding Flow

**Status:** READY
**Priority:** P1
**Owner:** Backend
**Depends On:** FF-BE008-001
**Effort:** 2h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Implement invite flow for new users
2. Add onboarding screens and password reset
3. Test onboarding for all roles

**File Paths:**
- app/api/auth/invite.ts
- app/onboarding/
- app/api/auth/reset-password.ts

**Acceptance Criteria:**
- [ ] Invite flow functional for all roles
- [ ] Onboarding screens implemented
- [ ] Password reset works
- [ ] All flows tested
- [ ] UI and API code committed

**Description:**
Implement user invitation and onboarding, including password reset. Ensure onboarding is smooth for all user roles.

---
