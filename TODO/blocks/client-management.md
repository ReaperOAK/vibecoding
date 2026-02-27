# Block: Client Management (CRM-lite)

**Block ID:** BLOCK-BE002
**Capability Reference:** TODO-BE002
**Description:** CRUD for clients, contacts, and organizations. Includes search, tagging, notes, and basic CRM features tailored for freelance teams.

## Sub-Blocks

1. **BE002-1: Client & Contact Models**
   - Define DB schema for clients, contacts, organizations
   - **Effort:** 0.5 day
   - **Owner:** Backend

2. **BE002-2: CRUD API & UI**
   - Implement tRPC endpoints and frontend forms for client/contact CRUD
   - **Effort:** 1 day
   - **Owner:** Backend/Frontend

3. **BE002-3: Search, Tagging, Notes**
   - Add search, tagging, and notes features to client records
   - **Effort:** 0.5 day
   - **Owner:** Backend/Frontend

4. **BE002-4: Tenant-Aware Access**
   - Enforce tenant isolation for all client data
   - **Effort:** 0.5 day
   - **Owner:** Backend

5. **BE002-5: Client Onboarding & Import**
   - UI/API for onboarding new clients, CSV import
   - **Effort:** 0.5 day
   - **Owner:** Backend/Frontend

## Dependencies
- BLOCK-DO001 (cloud infra/CI)
- BLOCK-BE008 (auth/RBAC)
- BLOCK-BE001 (multi-tenant core)
- BLOCK-FE002 (UI design system)

---
