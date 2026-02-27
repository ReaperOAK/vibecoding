# Team Dashboard — Mockup Spec

## Overview
A modern dashboard for teams to monitor project stats, recent activity, and take quick actions.

## Layout
- **Sidebar:** Navigation, workspace switcher
- **Header:** Team name, avatar, notifications
- **Main Panel:**
  - **Stats Overview:** Cards for active projects, hours this week, pending invoices, milestones
  - **Recent Activity Feed:** List of recent actions (project updates, comments, payments)
  - **Quick Actions:** Buttons for new project, log time, create invoice

## Components
- **Stat Card:** Icon, value, label, subtle shadow
- **Activity Item:** Avatar, description, timestamp
- **Button:** Primary (indigo), secondary (white/indigo border)
- **Sidebar:** Collapsible, icons + labels

## States
- Loading (skeletons)
- Empty (no activity)
- Error (fetch failed)

## Responsive
- Mobile: Sidebar collapses to bottom nav, cards stack
- Tablet: Sidebar collapses, grid tightens
- Desktop: Full layout

## Accessibility
- All actions keyboard accessible
- Focus ring on quick actions
- ARIA labels for nav and stats
