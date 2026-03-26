---
name: Git Protocol
description: Dispatcher-claim protocol, scoped git rules, commit format, lease mechanism. Quick reference for git-based distributed locking.
user-invocable: false
---

# Git Protocol Quick Reference

## Scoped Git (Non-Negotiable)
- **PROHIBITED**: `git add .`, `git add -A`, `git add --all`
- **REQUIRED**: Explicit file-by-file staging only
- **REQUIRED**: Commit message starts with `[TICKET-ID]`

## Two-Commit Protocol
1. **CLAIM** (Ticketer): `[TICKET-ID] CLAIM by AGENT on MACHINE (OPERATOR)`
2. **WORK** (Subagent): `[TICKET-ID] STAGE complete by AGENT on MACHINE`

## Lease
- Default: 30 minutes
- Expired lease → ticket reclaimable

## References
- [git-protocol.instructions.md](../../instructions/git-protocol.instructions.md)
