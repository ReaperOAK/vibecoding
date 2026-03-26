---
name: Ticket System
description: File-based ticket state machine. Quick reference for ticket operations, stage directories, and tickets.py commands.
user-invocable: false
---

# Ticket System Quick Reference

## State = Directory
Ticket state determined by directory under `ticket-state/`:
READY → ARCHITECT/RESEARCH/BACKEND/... → QA → SECURITY → CI → DOCS → VALIDATION → DONE

## tickets.py Commands
| Command | Purpose |
|---------|---------|
| `--sync` | Resolve deps, move unblocked to READY |
| `--status` | Dashboard view |
| `--claim <id> <agent> <machine> <operator>` | Claim ticket |
| `--advance <id> <agent>` | Move to next stage |
| `--rework <id> <agent> <reason>` | Send back for rework |

## References
- [ticket-system.instructions.md](../../instructions/ticket-system.instructions.md)
