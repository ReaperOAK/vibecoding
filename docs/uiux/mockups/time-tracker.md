# Time Tracker — Mockup Spec

## Overview
Track time, view weekly timesheets, and analyze reports.

## Layout
- **Active Timer:** Project/task selector, start/stop, elapsed time
- **Weekly Timesheet:** Grid view (days x projects/tasks)
- **Daily Log:** List of entries
- **Report Charts:** Bar/pie charts by project, team member

## Components
- **Timer:** Large display, start/stop button
- **Timesheet Cell:** Editable, shows hours
- **Log Entry:** Project, task, duration, notes
- **Chart:** Visual summary

## States
- Timer running, stopped
- No entries (empty)

## Responsive
- Mobile: Timer sticky at top, grid scrolls
- Tablet: Grid tightens
- Desktop: Full grid, charts side

## Accessibility
- Keyboard start/stop
- Focus indicators
- ARIA for grid, charts
