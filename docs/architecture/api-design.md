# FreelanceFlow API Design (tRPC)

## API Domains (Routers)
- **auth**: signup, login, logout, invite, client access
- **tenants**: create, update, branding, settings
- **users**: CRUD, roles, team management
- **clients**: CRUD, contacts, search
- **projects**: CRUD, milestones, deliverables
- **time**: log, update, timers, reports
- **invoices**: CRUD, line items, payments
- **files**: upload, presigned URL, parse, metadata
- **notifications**: subscribe, mark read, preferences

## Middleware Stack
- Auth (JWT/session)
- Tenant context (from JWT)
- Rate limiting
- Input validation (zod)

## Real-Time Patterns
- Notifications: SSE or Socket.io subscription per user/tenant
- File upload: webhook triggers parsing, notification

## RBAC & Permissions
- Roles: admin, member, client
- Permission matrix enforced in routers
- Client portal: separate router, limited scope

## Example tRPC Router (projects)
- listProjects
- getProjectById
- createProject
- updateProject
- deleteProject
- listMilestones
- addMilestone
- ...

## Error Handling
- Standardized error objects
- Sentry integration for error reporting

## API Versioning
- Versioned routers if breaking changes
