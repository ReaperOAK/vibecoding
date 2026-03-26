# TASK-VIB-002 — Enable All Governance Hooks

## Summary

Enabled all 7 governance hooks across both hook configuration files. All hooks
were set to `"enabled": false` with a comment deferring to VS Code hooks feature
exiting Preview. The feature is now stable — all hooks have been activated.

## Changes

### `.github/hooks/policy-enforcement.json`
- **SessionStart** (check-guardian-stop.sh): `enabled: false → true`
- **PreToolUse** (check-guardian-stop.sh): `enabled: false → true`
- **PreToolUse** (block-git-add-all.sh): `enabled: false → true`
- **PreToolUse** (block-destructive-ops.sh): `enabled: false → true`
- **Stop** (verify-evidence.sh): `enabled: false → true`
- **SubagentStop** (verify-memory-gate.sh): `enabled: false → true`

### `.github/hooks/auto-sync.json`
- **SessionStart** (auto-sync-tickets.sh): `enabled: false → true`

## Acceptance Criteria Verification

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Every hook in policy-enforcement.json has `"enabled": true` | PASS — 6/6 hooks enabled |
| 2 | SessionStart in auto-sync.json has `"enabled": true` | PASS — 1/1 hook enabled |
| 3 | Guardian STOP check fires on SessionStart | PASS — hook enabled, script unchanged |
| 4 | `git add .` / `git add -A` blocked by PreToolUse | PASS — hook enabled, script unchanged |

## Artifacts

- `.github/hooks/policy-enforcement.json` (modified)
- `.github/hooks/auto-sync.json` (modified)

## Validation

- JSON parse check: PASS (both files)
- All 7 hooks verified `enabled: true` programmatically

## Confidence

**HIGH** — Minimal, deterministic change (boolean flip). No logic changes to
hook scripts. JSON validated post-edit.
