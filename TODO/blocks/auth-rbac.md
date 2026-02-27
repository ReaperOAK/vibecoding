# Block: Authentication & Authorization (RBAC)

**Block ID:** BLOCK-BE008
**Capability Reference:** TODO-BE008
**Description:** Implement secure login, role-based access control, and permissions management for all user types (admin, team member, client). Foundation for all protected features.

## Sub-Blocks

1. **BE008-1: Auth Provider Integration**
   - Integrate NextAuth.js v5 (Auth.js) for email/social login
   - Configure JWT/session management
   - **Effort:** 1 day
   - **Owner:** Backend

2. **BE008-2: Role & Permission Model**
   - Define roles (admin, member, client) and permission matrix
   - Enforce RBAC in API and UI
   - **Effort:** 1 day
   - **Owner:** Backend

3. **BE008-3: Secure Session & Token Handling**
   - Implement secure session storage, token rotation, and logout
   - **Effort:** 0.5 day
   - **Owner:** Backend

4. **BE008-4: Protected Routes & Middleware**
   - Add middleware for route protection (API, UI)
   - Tenant context extraction from JWT
   - **Effort:** 0.5 day
   - **Owner:** Backend

5. **BE008-5: User Invitation & Onboarding**
   - Implement invite flow, onboarding, and password reset
   - **Effort:** 1 day
   - **Owner:** Backend

## Dependencies
- BLOCK-DO001 (cloud infra/CI)

---
