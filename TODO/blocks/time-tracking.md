# Block: Time Tracking

**Block ID:** BLOCK-BE004
**Capability Reference:** TODO-BE004
**Description:** Timesheet entry, timers, reporting, and export. Allows users to log time, run timers, and generate reports for billing and productivity.

## Sub-Blocks

1. **BE004-1: Time Entry Model & DB**
   - Define DB schema for time entries, timer states
   - **Effort:** 0.5 day
   - **Owner:** Backend

2. **BE004-2: Time Tracking API & UI**
   - Implement tRPC endpoints and frontend for time entry, timer, and editing
   - **Effort:** 1 day
   - **Owner:** Backend/Frontend

3. **BE004-3: Reporting & Export**
   - Generate reports, CSV export for billing/productivity
   - **Effort:** 0.5 day
   - **Owner:** Backend/Frontend

4. **BE004-4: Timesheet Validation & Approval**
   - Add validation, approval, and lock for submitted timesheets
   - **Effort:** 0.5 day
   - **Owner:** Backend/Frontend

5. **BE004-5: Timer UX Enhancements**
   - Improve timer UX (notifications, idle detection, reminders)
   - **Effort:** 0.5 day
   - **Owner:** Frontend

## Dependencies
- BLOCK-DO001 (cloud infra/CI)
- BLOCK-BE008 (auth/RBAC)
- BLOCK-BE001 (multi-tenant core)
- BLOCK-FE002 (UI design system)

---
