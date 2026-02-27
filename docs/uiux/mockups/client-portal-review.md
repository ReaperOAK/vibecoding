# Client Portal — Deliverable Review Mockup Spec

## Overview
Clients review deliverables, annotate, approve, or request changes.

## Layout
- **Header:** Deliverable name, project, version
- **File Preview:** Image/PDF viewer, zoom, download
- **Feedback Form:** Text input, annotation tools
- **Approval Buttons:** Approve, request changes
- **Version History:** List of previous versions
- **Comments Thread:** Threaded, reply, timestamps

## Components
- **File Viewer:** Supports images, PDFs
- **Annotation Tool:** Highlight, comment
- **Approval Button:** Primary (approve), secondary (request changes)
- **Version Item:** Version number, date, status
- **Comment:** Avatar, text, reply

## States
- No feedback yet (empty)
- Approved, changes requested

## Responsive
- Mobile: Viewer full width, actions below
- Tablet: Two-column
- Desktop: Multi-panel

## Accessibility
- Keyboard annotation
- Focus indicators
- ARIA for file viewer, buttons
