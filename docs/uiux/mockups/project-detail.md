# Project Detail View — Mockup Spec

## Overview
Detailed project page with milestones, deliverables, time tracking, and team info.

## Layout
- **Header:** Project name, client, status badge, progress bar
- **Milestones:** Timeline or kanban board
- **Deliverables:** List with file previews, status
- **Time Tracking:** Summary card (hours, budget, chart)
- **Team Members:** Avatars, roles
- **Activity/Comments:** Threaded, with reply

## Components
- **Progress Bar:** Shows % complete
- **Milestone Card:** Title, due date, status
- **File Preview:** Thumbnail, download, version
- **Comment Thread:** Avatar, text, timestamp, reply

## States
- Loading (skeletons)
- Empty (no deliverables)
- Error (fetch failed)

## Responsive
- Mobile: Sections stack, kanban → list
- Tablet: Two-column
- Desktop: Multi-panel

## Accessibility
- All controls labeled
- Focus indicators on interactive elements
- ARIA for timeline, comments
