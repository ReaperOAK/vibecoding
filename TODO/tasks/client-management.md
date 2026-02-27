# Client Management (CRM-lite) — L3 Actionable Tasks

## FF-BE002-001: Define Client & Contact Models in DB

**Status:** READY
**Priority:** P1
**Owner:** Backend
**Depends On:** FF-BE001-001
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Add client, contact, and organization tables to Prisma schema
2. Run DB migration and verify schema
3. Document model relationships

**File Paths:**
- prisma/schema.prisma
- prisma/migrations/
- docs/db/client-model.md

**Acceptance Criteria:**
- [ ] Client, contact, organization tables created
- [ ] Migration runs without errors
- [ ] Model relationships documented
- [ ] All code and docs committed

**Description:**
Define and implement DB models for clients, contacts, and organizations. Ensure relationships are documented and schema is migrated.

---

## FF-BE002-002: Implement Client/Contact CRUD API (tRPC)

**Status:** READY
**Priority:** P1
**Owner:** Backend
**Depends On:** FF-BE002-001
**Effort:** 2h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Implement tRPC endpoints for client/contact CRUD
2. Add input validation and error handling
3. Write unit tests for API endpoints

**File Paths:**
- app/api/clients/
- app/api/contacts/
- tests/api/clients.test.ts

**Acceptance Criteria:**
- [ ] CRUD endpoints implemented and tested
- [ ] Input validation and error handling in place
- [ ] Unit tests cover all endpoints
- [ ] All code and tests committed

**Description:**
Implement tRPC API endpoints for client and contact CRUD. Ensure endpoints are validated, tested, and robust.

---

## FF-FE002-003: Build Client/Contact Management UI

**Status:** READY
**Priority:** P1
**Owner:** Frontend Engineer
**Depends On:** FF-BE002-002, FF-FE002-001
**Effort:** 2h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Build frontend forms and tables for client/contact CRUD
2. Integrate with tRPC endpoints
3. Add validation and error display

**File Paths:**
- app/clients/
- app/contacts/
- app/components/clients/

**Acceptance Criteria:**
- [ ] UI for client/contact CRUD implemented
- [ ] Integration with tRPC API
- [ ] Validation and error handling in UI
- [ ] All code committed

**Description:**
Build frontend UI for managing clients and contacts. Integrate with backend API and ensure robust validation.

---

## FF-BE002-004: Implement Search, Tagging, and Notes for Clients

**Status:** READY
**Priority:** P2
**Owner:** Backend, Frontend
**Depends On:** FF-BE002-002, FF-FE002-003
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Add search, tagging, and notes fields to client model
2. Implement API and UI for these features
3. Test search, tagging, and notes flows

**File Paths:**
- prisma/schema.prisma
- app/api/clients/
- app/clients/

**Acceptance Criteria:**
- [ ] Search, tagging, notes fields in DB and API
- [ ] UI for managing tags and notes
- [ ] All flows tested
- [ ] All code committed

**Description:**
Add search, tagging, and notes features to client management. Implement both backend and frontend support.

---

## FF-BE002-005: Client Onboarding & CSV Import

**Status:** READY
**Priority:** P2
**Owner:** Backend, Frontend
**Depends On:** FF-BE002-002, FF-FE002-003
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Implement onboarding flow for new clients
2. Add CSV import for bulk client creation
3. Test onboarding and import flows

**File Paths:**
- app/clients/import.tsx
- app/api/clients/import.ts

**Acceptance Criteria:**
- [ ] Onboarding flow for new clients
- [ ] CSV import functional and validated
- [ ] All flows tested
- [ ] All code committed

**Description:**
Enable onboarding and CSV import for clients. Ensure flows are robust and validated on both backend and frontend.

---
