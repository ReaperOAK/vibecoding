# Time Tracking — L3 Actionable Tasks

## FF-BE004-001: Define Time Entry Model & DB Schema

**Status:** READY
**Priority:** P1
**Owner:** Backend
**Depends On:** FF-BE001-001
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Add time entry and timer state tables to Prisma schema
2. Run DB migration and verify schema
3. Document model relationships

**File Paths:**
- prisma/schema.prisma
- prisma/migrations/
- docs/db/time-entry-model.md

**Acceptance Criteria:**
- [ ] Time entry and timer state tables created
- [ ] Migration runs without errors
- [ ] Model relationships documented
- [ ] All code and docs committed

**Description:**
Define and implement DB models for time entries and timer states. Ensure relationships are documented and schema is migrated.

---

## FF-BE004-002: Implement Time Tracking API (tRPC)

**Status:** READY
**Priority:** P1
**Owner:** Backend
**Depends On:** FF-BE004-001
**Effort:** 2h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Implement tRPC endpoints for time entry, timer, and editing
2. Add input validation and error handling
3. Write unit tests for API endpoints

**File Paths:**
- app/api/time/
- tests/api/time.test.ts

**Acceptance Criteria:**
- [ ] Time tracking endpoints implemented and tested
- [ ] Input validation and error handling in place
- [ ] Unit tests cover all endpoints
- [ ] All code and tests committed

**Description:**
Implement tRPC API endpoints for time tracking. Ensure endpoints are validated, tested, and robust.

---

## FF-FE004-003: Build Time Tracking UI (Entry, Timer, Edit)

**Status:** READY
**Priority:** P1
**Owner:** Frontend Engineer
**Depends On:** FF-BE004-002, FF-FE002-001
**Effort:** 2h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Build frontend for time entry, timer, and editing
2. Integrate with tRPC endpoints
3. Add validation and error display

**File Paths:**
- app/time/
- app/components/time/

**Acceptance Criteria:**
- [ ] UI for time entry, timer, and editing implemented
- [ ] Integration with tRPC API
- [ ] Validation and error handling in UI
- [ ] All code committed

**Description:**
Build frontend UI for time tracking, including entry, timer, and editing. Integrate with backend API and ensure robust validation.

---

## FF-BE004-004: Implement Reporting & Export (CSV)

**Status:** READY
**Priority:** P2
**Owner:** Backend, Frontend
**Depends On:** FF-BE004-002, FF-FE004-003
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Generate reports for billing and productivity
2. Implement CSV export for time entries
3. Test reporting and export flows

**File Paths:**
- app/api/time/report.ts
- app/time/report.tsx

**Acceptance Criteria:**
- [ ] Reports generated for billing/productivity
- [ ] CSV export functional
- [ ] All flows tested
- [ ] All code committed

**Description:**
Enable reporting and CSV export for time tracking. Provide both backend and frontend support for these features.

---

## FF-BE004-005: Add Timesheet Validation & Approval

**Status:** READY
**Priority:** P2
**Owner:** Backend, Frontend
**Depends On:** FF-BE004-004
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Add validation and approval logic for submitted timesheets
2. Implement lock for approved timesheets
3. Test validation and approval flows

**File Paths:**
- app/api/time/approval.ts
- app/time/approval.tsx

**Acceptance Criteria:**
- [ ] Timesheet validation and approval implemented
- [ ] Lock for approved timesheets
- [ ] All flows tested
- [ ] All code committed

**Description:**
Add validation and approval for timesheets. Ensure approved timesheets are locked and flows are robust.

---

## FF-FE004-006: Enhance Timer UX (Notifications, Idle Detection)

**Status:** READY
**Priority:** P2
**Owner:** Frontend Engineer
**Depends On:** FF-FE004-003
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Add notifications for timer events
2. Implement idle detection and reminders
3. Test timer UX enhancements

**File Paths:**
- app/time/timer.tsx
- app/components/time/timer.tsx

**Acceptance Criteria:**
- [ ] Notifications for timer events implemented
- [ ] Idle detection and reminders functional
- [ ] All enhancements tested
- [ ] All code committed

**Description:**
Enhance timer UX with notifications, idle detection, and reminders. Ensure robust and user-friendly timer experience.

---
