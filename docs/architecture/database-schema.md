# FreelanceFlow Database Schema

## Core Tables & Relationships

- **tenants** (1) ⟶ (N) **users**
- **users** (N) ⟷ (N) **team_memberships** (role, tenant_id)
- **clients** (1) ⟶ (N) **client_contacts**
- **tenants** (1) ⟶ (N) **clients**
- **projects** (1) ⟶ (N) **milestones**
- **projects** (1) ⟶ (N) **deliverables**
- **projects** (1) ⟶ (N) **time_entries**
- **projects** (1) ⟶ (N) **invoices**
- **invoices** (1) ⟶ (N) **invoice_line_items**
- **invoices** (1) ⟶ (N) **payments**
- **projects** (1) ⟶ (N) **files**
- **files** (1) ⟶ (1) **document_metadata**
- **users** (1) ⟶ (N) **notifications**

## Table List
- tenants (id, name, branding, ...)
- users (id, email, name, ...)
- team_memberships (id, user_id, tenant_id, role)
- clients (id, tenant_id, name, ...)
- client_contacts (id, client_id, name, email, ...)
- projects (id, tenant_id, client_id, name, ...)
- milestones (id, project_id, name, due_date, ...)
- deliverables (id, project_id, milestone_id, file_id, ...)
- time_entries (id, project_id, user_id, start, end, ...)
- invoices (id, project_id, client_id, status, ...)
- invoice_line_items (id, invoice_id, description, amount, ...)
- payments (id, invoice_id, amount, status, ...)
- files (id, project_id, tenant_id, url, ...)
- document_metadata (id, file_id, type, parsed_text, ...)
- notifications (id, user_id, type, data, read, ...)

## Multi-Tenancy
- Every table has `tenant_id` (except tenants itself)
- RLS policies restrict access by tenant
- Key indexes: (tenant_id), (user_id), (project_id), (client_id), (invoice_id)

## ERD (Entity Relationship Description)
- One tenant has many users, clients, and projects
- Users belong to tenants via team_memberships (role: admin, member, client)
- Projects belong to tenants and clients
- Projects have milestones, deliverables, time entries, invoices, files
- Invoices have line items and payments
- Files have document metadata
- Notifications are per user
