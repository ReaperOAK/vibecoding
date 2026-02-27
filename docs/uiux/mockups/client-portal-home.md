# Client Portal — Home Mockup Spec

## Overview
Branded portal home for clients to view project status, deliverables, and invoices.

## Layout
- **Header:** Team logo, brand color background, client name
- **Active Projects:** Cards with milestone progress
- **Recent Deliverables:** List with file previews, review status
- **Pending Approvals:** Badge/count
- **Invoice Summary:** Table or card with outstanding invoices

## Components
- **Project Card:** Name, progress bar, next milestone
- **Deliverable Item:** File icon, name, status
- **Invoice Card:** Amount, due date, status
- **Branding:** Custom logo, primary/accent color, favicon

## States
- No active projects (empty)
- All invoices paid (empty)

## Responsive
- Mobile: Cards stack, bottom nav
- Tablet: Collapsible sidebar
- Desktop: Full layout

## Accessibility
- Color contrast for branding
- Focus indicators
- ARIA for project/deliverable lists
