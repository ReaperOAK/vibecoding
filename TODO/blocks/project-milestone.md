# Block: Project & Milestone Management

**Block ID:** BLOCK-BE003
**Capability Reference:** TODO-BE003
**Description:** Project creation, milestone tracking, deliverable management, and approval workflow. Enables teams to organize work, set deadlines, and track progress.

## Sub-Blocks

1. **BE003-1: Project & Milestone Models**
   - Define DB schema for projects, milestones, deliverables
   - **Effort:** 0.5 day
   - **Owner:** Backend

2. **BE003-2: CRUD API & UI**
   - Implement tRPC endpoints and frontend forms for project/milestone CRUD
   - **Effort:** 1 day
   - **Owner:** Backend/Frontend

3. **BE003-3: Deliverable Management**
   - Upload, associate, and track deliverables per milestone
   - **Effort:** 0.5 day
   - **Owner:** Backend/Frontend

4. **BE003-4: Approval Workflow**
   - Implement approval/rejection flow for milestones/deliverables
   - **Effort:** 0.5 day
   - **Owner:** Backend/Frontend

5. **BE003-5: Timeline & Progress Tracking**
   - Visualize project timelines, progress bars, and status
   - **Effort:** 0.5 day
   - **Owner:** Frontend

## Dependencies
- BLOCK-DO001 (cloud infra/CI)
- BLOCK-BE008 (auth/RBAC)
- BLOCK-BE001 (multi-tenant core)
- BLOCK-FE002 (UI design system)

---
