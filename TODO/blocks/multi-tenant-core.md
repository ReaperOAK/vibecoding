# Block: Multi-Tenant Core & Team Isolation

**Block ID:** BLOCK-BE001
**Capability Reference:** TODO-BE001
**Description:** Implement tenant isolation, workspace boundaries, and secure data partitioning. All data access and workflows must be tenant-aware.

## Sub-Blocks

1. **BE001-1: Tenant Model & DB Partitioning**
   - Add tenant_id to all tables, enforce RLS in PostgreSQL/Prisma
   - **Effort:** 1 day
   - **Owner:** Backend

2. **BE001-2: Tenant Context Middleware**
   - Middleware to extract tenant from JWT/session, inject into API
   - **Effort:** 0.5 day
   - **Owner:** Backend

3. **BE001-3: Workspace Switching & Onboarding**
   - UI/API for switching workspaces, onboarding new tenants
   - **Effort:** 0.5 day
   - **Owner:** Backend/Frontend

4. **BE001-4: Tenant-Aware API & File Access**
   - Ensure all API/file flows are tenant-scoped
   - **Effort:** 1 day
   - **Owner:** Backend

5. **BE001-5: Tenant Branding & Settings**
   - Support per-tenant branding, settings, and preferences
   - **Effort:** 1 day
   - **Owner:** Backend/Frontend

## Dependencies
- BLOCK-DO001 (cloud infra/CI)
- BLOCK-BE008 (auth/RBAC)

---
