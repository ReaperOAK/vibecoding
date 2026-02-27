# Invoicing & Stripe Integration — L3 Actionable Tasks

## FF-BE005-001: Define Invoice, Line Item & Payment Models

**Status:** READY
**Priority:** P1
**Owner:** Backend
**Depends On:** FF-BE001-001
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Add invoice, line item, and payment tables to Prisma schema
2. Run DB migration and verify schema
3. Document model relationships

**File Paths:**
- prisma/schema.prisma
- prisma/migrations/
- docs/db/invoice-model.md

**Acceptance Criteria:**
- [ ] Invoice, line item, payment tables created
- [ ] Migration runs without errors
- [ ] Model relationships documented
- [ ] All code and docs committed

**Description:**
Define and implement DB models for invoices, line items, and payments. Ensure relationships are documented and schema is migrated.

---

## FF-BE005-002: Implement Invoice CRUD API (tRPC)

**Status:** READY
**Priority:** P1
**Owner:** Backend
**Depends On:** FF-BE005-001
**Effort:** 2h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Implement tRPC endpoints for invoice CRUD
2. Add input validation and error handling
3. Write unit tests for API endpoints

**File Paths:**
- app/api/invoices/
- tests/api/invoices.test.ts

**Acceptance Criteria:**
- [ ] CRUD endpoints implemented and tested
- [ ] Input validation and error handling in place
- [ ] Unit tests cover all endpoints
- [ ] All code and tests committed

**Description:**
Implement tRPC API endpoints for invoice CRUD. Ensure endpoints are validated, tested, and robust.

---

## FF-BE005-003: Integrate Stripe SDK & Webhooks

**Status:** READY
**Priority:** P1
**Owner:** Backend
**Depends On:** FF-BE005-002
**Effort:** 2h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Integrate Stripe SDK for payments
2. Implement webhooks for payment events
3. Add usage-based billing logic

**File Paths:**
- app/api/invoices/stripe.ts
- app/api/webhooks/stripe.ts

**Acceptance Criteria:**
- [ ] Stripe SDK integrated for payments
- [ ] Webhooks handle payment events
- [ ] Usage-based billing logic implemented
- [ ] All code committed

**Description:**
Integrate Stripe SDK and webhooks for payment processing. Implement usage-based billing logic for invoices.

---

## FF-BE005-004: Track Payment Status & Reconciliation

**Status:** READY
**Priority:** P2
**Owner:** Backend
**Depends On:** FF-BE005-003
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Track payment status for all invoices
2. Handle failed payments and reconciliation
3. Add admin UI for payment status

**File Paths:**
- app/api/invoices/status.ts
- app/admin/invoices/

**Acceptance Criteria:**
- [ ] Payment status tracked for all invoices
- [ ] Failed payments handled and reconciled
- [ ] Admin UI for payment status
- [ ] All code committed

**Description:**
Track payment status and handle reconciliation for invoices. Provide admin UI for payment status management.

---

## FF-FE005-005: Implement Invoice Delivery & Client View

**Status:** READY
**Priority:** P2
**Owner:** Frontend Engineer
**Depends On:** FF-BE005-002
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Implement email delivery of invoices
2. Build client portal view for invoices and payment links
3. Test invoice delivery and client view

**File Paths:**
- app/clients/invoices.tsx
- app/api/invoices/email.ts

**Acceptance Criteria:**
- [ ] Invoices emailed to clients
- [ ] Client portal view for invoices/payment
- [ ] All flows tested
- [ ] All code committed

**Description:**
Enable invoice delivery via email and provide client portal view for invoices and payments. Ensure robust and user-friendly experience.

---
