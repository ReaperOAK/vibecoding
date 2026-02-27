# Project & Milestone Management — L3 Actionable Tasks

## FF-BE003-001: Define Project, Milestone & Deliverable Models

**Status:** READY
**Priority:** P1
**Owner:** Backend
**Depends On:** FF-BE001-001
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Add project, milestone, and deliverable tables to Prisma schema
2. Run DB migration and verify schema
3. Document model relationships

**File Paths:**
- prisma/schema.prisma
- prisma/migrations/
- docs/db/project-model.md

**Acceptance Criteria:**
- [ ] Project, milestone, deliverable tables created
- [ ] Migration runs without errors
- [ ] Model relationships documented
- [ ] All code and docs committed

**Description:**
Define and implement DB models for projects, milestones, and deliverables. Ensure relationships are documented and schema is migrated.

---

## FF-BE003-002: Implement Project/Milestone CRUD API (tRPC)

**Status:** READY
**Priority:** P1
**Owner:** Backend
**Depends On:** FF-BE003-001
**Effort:** 2h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Implement tRPC endpoints for project/milestone CRUD
2. Add input validation and error handling
3. Write unit tests for API endpoints

**File Paths:**
- app/api/projects/
- app/api/milestones/
- tests/api/projects.test.ts

**Acceptance Criteria:**
- [ ] CRUD endpoints implemented and tested
- [ ] Input validation and error handling in place
- [ ] Unit tests cover all endpoints
- [ ] All code and tests committed

**Description:**
Implement tRPC API endpoints for project and milestone CRUD. Ensure endpoints are validated, tested, and robust.

---

## FF-FE003-003: Build Project/Milestone Management UI

**Status:** READY
**Priority:** P1
**Owner:** Frontend Engineer
**Depends On:** FF-BE003-002, FF-FE002-001
**Effort:** 2h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Build frontend forms and tables for project/milestone CRUD
2. Integrate with tRPC endpoints
3. Add validation and error display

**File Paths:**
- app/projects/
- app/milestones/
- app/components/projects/

**Acceptance Criteria:**
- [ ] UI for project/milestone CRUD implemented
- [ ] Integration with tRPC API
- [ ] Validation and error handling in UI
- [ ] All code committed

**Description:**
Build frontend UI for managing projects and milestones. Integrate with backend API and ensure robust validation.

---

## FF-BE003-004: Implement Deliverable Management (Upload, Associate, Track)

**Status:** READY
**Priority:** P2
**Owner:** Backend, Frontend
**Depends On:** FF-BE003-002, FF-FE003-003
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Implement file upload and association with milestones
2. Track deliverable status and history
3. Test deliverable management flows

**File Paths:**
- app/api/deliverables/
- app/deliverables/

**Acceptance Criteria:**
- [ ] File upload and association functional
- [ ] Deliverable status tracked
- [ ] All flows tested
- [ ] All code committed

**Description:**
Enable file upload and association with milestones. Track deliverable status and provide management UI.

---

## FF-BE003-005: Implement Approval Workflow for Milestones/Deliverables

**Status:** READY
**Priority:** P2
**Owner:** Backend, Frontend
**Depends On:** FF-BE003-004
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Implement approval/rejection flow for milestones/deliverables
2. Add UI for approval actions and status
3. Test approval workflow

**File Paths:**
- app/api/milestones/approval.ts
- app/milestones/approval.tsx

**Acceptance Criteria:**
- [ ] Approval/rejection flow implemented
- [ ] UI for approval actions and status
- [ ] All flows tested
- [ ] All code committed

**Description:**
Implement approval workflow for milestones and deliverables. Provide UI for approval actions and status tracking.

---

## FF-FE003-006: Visualize Project Timelines & Progress

**Status:** READY
**Priority:** P2
**Owner:** Frontend Engineer
**Depends On:** FF-BE003-003
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Build timeline and progress bar components
2. Integrate with project/milestone data
3. Test timeline and progress visualization

**File Paths:**
- app/projects/timeline.tsx
- app/components/projects/progress.tsx

**Acceptance Criteria:**
- [ ] Timeline and progress bar components implemented
- [ ] Data integration verified
- [ ] All code committed

**Description:**
Visualize project timelines and progress with dedicated UI components. Integrate with project and milestone data.

---
