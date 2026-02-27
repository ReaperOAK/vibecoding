# Block: Invoicing & Stripe Integration

**Block ID:** BLOCK-BE005
**Capability Reference:** TODO-BE005
**Description:** Invoice generation, Stripe billing, usage-based pricing, and payment status tracking. Automates billing and payment collection for freelance teams.

## Sub-Blocks

1. **BE005-1: Invoice & Payment Models**
   - Define DB schema for invoices, line items, payments
   - **Effort:** 0.5 day
   - **Owner:** Backend

2. **BE005-2: Invoice CRUD API & UI**
   - Implement tRPC endpoints and frontend for invoice CRUD
   - **Effort:** 1 day
   - **Owner:** Backend/Frontend

3. **BE005-3: Stripe Integration**
   - Integrate Stripe SDK, webhooks, and usage-based billing
   - **Effort:** 1 day
   - **Owner:** Backend

4. **BE005-4: Payment Status & Reconciliation**
   - Track payment status, handle failed payments, and reconciliation
   - **Effort:** 0.5 day
   - **Owner:** Backend

5. **BE005-5: Invoice Delivery & Client View**
   - Email invoices, client portal view, and payment links
   - **Effort:** 0.5 day
   - **Owner:** Backend/Frontend

## Dependencies
- BLOCK-DO001 (cloud infra/CI)
- BLOCK-BE008 (auth/RBAC)
- BLOCK-BE001 (multi-tenant core)
- BLOCK-FE002 (UI design system)

---
