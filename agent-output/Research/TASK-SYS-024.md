# TASK-SYS-024 — RESEARCH Complete

## Decision: Keep git-protocol.instructions.md Universal (applyTo: '**')

### Analysis

The git-protocol instruction contains 8 sections:
1. Dispatcher-Claim / Worker-Work Protocol
2. Commit 1 — CLAIM
3. Commit 2 — WORK
4. Scoped Git Rules (Hard)
5. Commit Message Format
6. Lease Mechanism
7. Failure Recovery
8. Summary Handoff Protocol

### Evaluation

**Could be scoped to `.github/**`**: Sections 2, 3, 5, 6 (commit format, lease details)
**Must remain universal**: Sections 1, 4, 7, 8 (git safety rules apply to ALL file operations)

### Decision: Do NOT Split

**Rationale:**
1. **Section 4 (Scoped Git Rules)** blocks `git add .` everywhere — this MUST remain universal
2. **Section 1 (Dispatcher-Claim)** constrains ALL agents regardless of what files they modify
3. **Splitting creates risk**: If an agent modifies code files outside `.github/`, the commit format and protocol rules wouldn't load
4. **Token cost is acceptable**: The file is ~100 lines — the context cost of loading it universally is minimal compared to the risk of missing critical git safety rules
5. **All other instruction files already use `applyTo: '**'`** — splitting one creates inconsistency

### Recommendation
Keep `applyTo: '**'` unchanged. The git safety rules (no `git add .`, scoped staging, commit format) must be loaded for every file context.

## Artifacts
- This research document (no code changes)

## Confidence: HIGH
