# Branded Client Portal — L3 Actionable Tasks

## FF-FE001-001: Set Up Portal Shell & Routing

**Status:** READY
**Priority:** P1
**Owner:** Frontend Engineer
**Depends On:** FF-BE001-001, FF-FE002-001
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Set up client portal routes and layout in Next.js
2. Implement authentication and access control
3. Test portal shell and routing

**File Paths:**
- app/portal/
- app/portal/layout.tsx
- app/portal/_middleware.ts

**Acceptance Criteria:**
- [ ] Portal routes and layout implemented
- [ ] Authentication and access control functional
- [ ] Portal shell tested
- [ ] All code committed

**Description:**
Set up the foundational shell and routing for the branded client portal. Ensure authentication and access control are in place.

---

## FF-FE001-002: Build Deliverable Review & Feedback UI

**Status:** READY
**Priority:** P1
**Owner:** Frontend Engineer
**Depends On:** FF-FE001-001
**Effort:** 2h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Build UI for clients to review deliverables
2. Implement feedback and comment features
3. Test deliverable review and feedback flows

**File Paths:**
- app/portal/deliverables.tsx
- app/components/portal/feedback.tsx

**Acceptance Criteria:**
- [ ] Deliverable review UI implemented
- [ ] Feedback and comment features functional
- [ ] All flows tested
- [ ] All code committed

**Description:**
Build UI for clients to review deliverables and leave feedback. Ensure robust and user-friendly experience.

---

## FF-FE001-003: Implement Milestone Approval Workflow

**Status:** READY
**Priority:** P2
**Owner:** Frontend Engineer
**Depends On:** FF-FE001-002
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Implement approval/rejection UI for milestones
2. Track and display milestone status
3. Test approval workflow

**File Paths:**
- app/portal/milestones.tsx
- app/components/portal/milestone-status.tsx

**Acceptance Criteria:**
- [ ] Approval/rejection UI implemented
- [ ] Milestone status tracked and displayed
- [ ] All flows tested
- [ ] All code committed

**Description:**
Implement milestone approval workflow in the client portal. Provide clear status tracking and user-friendly UI.

---

## FF-FE001-004: Support Client Branding & Customization

**Status:** READY
**Priority:** P2
**Owner:** Frontend Engineer, UIDesigner
**Depends On:** FF-FE001-001
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Add support for per-client branding (logo, theme)
2. Implement customization options in portal
3. Test branding and customization flows

**File Paths:**
- app/portal/branding.tsx
- app/components/portal/branding.tsx

**Acceptance Criteria:**
- [ ] Per-client branding and theme supported
- [ ] Customization options functional
- [ ] All flows tested
- [ ] All code committed

**Description:**
Support per-client branding and customization in the portal. Ensure clients can personalize their experience.

---

## FF-FE001-005: Enforce Secure Access & Permissions

**Status:** READY
**Priority:** P1
**Owner:** Backend, Frontend
**Depends On:** FF-FE001-001
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Enforce RBAC and secure client-only views
2. Test access control for all portal routes
3. Audit for unauthorized access

**File Paths:**
- app/portal/_middleware.ts
- app/api/auth/

**Acceptance Criteria:**
- [ ] RBAC enforced for all portal routes
- [ ] Secure client-only views implemented
- [ ] No unauthorized access possible
- [ ] All code committed

**Description:**
Enforce secure access and permissions for the client portal. Ensure only authorized clients can access portal features.

---
