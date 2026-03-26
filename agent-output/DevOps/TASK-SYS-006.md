# TASK-SYS-006 — DEVOPS Complete

## Summary
Created PreToolUse hook `block-destructive-ops.sh` that blocks catastrophic commands (rm -rf, DROP TABLE, git reset --hard, etc.) and prompts approval for risky commands (DELETE FROM, docker rm, etc.). Registered in policy-enforcement.json.

## Artifacts
- .github/hooks/scripts/block-destructive-ops.sh (new)
- .github/hooks/policy-enforcement.json (updated)

## Evidence
Two-tier approach: deny patterns (exit 1) for catastrophic ops, ask patterns (exit 2) for risky ops. Covers rm -rf, git force push, DROP/TRUNCATE/DELETE SQL, docker prune.

## Confidence: HIGH
