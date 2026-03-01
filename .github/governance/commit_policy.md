<!-- GOVERNANCE_VERSION: 9.1.0 -->

# Commit Policy

> **Governance Version:** 9.1.0
> **Source:** Extracted from ReaperOAK.agent.md §12, §22
> **Scope:** Per-ticket atomic commit enforcement, scoped git rules, and
> pre-commit scope validation.

---

## 1. Per-Ticket Commit Enforcement

One commit per ticket. No exceptions.

### Commit Rules

- Commit message format: `[TICKET-ID] description`
- CHANGELOG MUST be updated in the same commit
- No squash commits across tickets
- No multi-ticket commits
- All changed files MUST be included in the commit

### Commit Execution

ReaperOAK performs the commit at the COMMIT state (after CI_REVIEW passes):

```bash
git add <changed-files>
git commit -m "[TICKET-ID] <description>"
```

### Failure Handling

- Commit fails → retry once with corrected parameters
- Second failure → escalate to user
- Wrong commit format → ticket returns to REWORK (rework_count++)
- No commit → ticket cannot reach DONE

---

## 2. Scoped Git Enforcement

Strengthens per-ticket commit enforcement with explicit scoping rules
that prevent unscoped staging operations and validate commit scope against
ticket declarations.

### Hard Rules

- **NEVER** use `git add .`
- **NEVER** use `git add -A`
- **NEVER** use `git add --all`
- **ALWAYS** list files explicitly: `git add path/to/file1 path/to/file2 ...`
- Files staged **MUST** match the ticket's declared `file_paths` in its L3
  task spec

### DRIFT-002 Trigger

Any use of `git add .`, `git add -A`, or `git add --all` emits:

```yaml
event: PROTOCOL_VIOLATION
violation: DRIFT-002
invariant: INV-3
details: "Unscoped staging operation detected"
severity: HIGH
auto_repair: true
```

The ComplianceWorker rejects the commit and re-stages with the explicit
file list from the ticket's `file_paths`.

---

## 3. Pre-Commit Scope Validation

Runs at COMMIT state before `git commit`:

```
function validateCommitScope(ticket):
  staged_files = git diff --cached --name-only
  declared_files = ticket.file_paths
  CHANGELOG_path = "CHANGELOG.md"  # Always allowed

  extra_files = staged_files - declared_files - {CHANGELOG_path}
  missing_files = declared_files - staged_files

  if extra_files is not empty:
    emit PROTOCOL_VIOLATION(DRIFT-002, ticket, "Extra files: {extra_files}")
    return REJECT → REWORK

  if missing_files is not empty:
    emit PROTOCOL_VIOLATION(DRIFT-002, ticket, "Missing files: {missing_files}")
    return REJECT → REWORK

  return PASS
```

---

## 4. Commit Command Template

The ONLY acceptable commit format:

```bash
git add path/to/file1.ts path/to/file2.ts CHANGELOG.md
git commit -m "[TICKET-ID] description"
```

Any deviation from explicit file listing triggers DRIFT-002.

---

## 5. Integration with Lifecycle

The commit stage is the 8th state in the 9-state machine (see
`lifecycle.md`). A ticket transitions from CI_REVIEW → COMMIT only when:

1. CI Reviewer emits PASS (lint, types, complexity all pass)
2. Memory gate passes (see `memory_policy.md`)
3. Pre-commit scope validation passes (this document, §3)

Failure at any of these gates blocks the transition and routes the ticket
to REWORK or flags for human attention.

---

## 6. Prohibited Patterns

| Pattern | Violation | Consequence |
|---------|-----------|-------------|
| `git add .` | DRIFT-002 | Block commit, re-stage explicitly |
| `git add -A` | DRIFT-002 | Block commit, re-stage explicitly |
| `git add --all` | DRIFT-002 | Block commit, re-stage explicitly |
| Multi-ticket commit | INV-2 violation | Reject, split into per-ticket commits |
| Missing CHANGELOG update | Commit rule violation | Reject, require CHANGELOG entry |
| Commit without ticket ID prefix | Format violation | Reject, re-format message |
| Staging files outside ticket scope | DRIFT-002 | Reject, remove extra files |
| Missing declared files from staging | DRIFT-002 | Reject, add missing files |

---

## 7. Class B (Background) Commit Policy

Background workers spawned by the Operational Concurrency Floor use a
distinct commit format. Full specification: `governance/concurrency_floor.md` §7.

### BG Commit Format

```bash
git add path/to/report.md
git commit -m "[BG-<TYPE>] description"
```

Example: `[BG-SEC-AUDIT] OWASP gap analysis for auth module`

### BG Commit Rules

| Rule | Enforcement |
|------|-------------|
| Format: `[BG-<TYPE>]` prefix | Reject commits without valid BG prefix |
| Scoped git only (no `git add .`) | DRIFT-002 applies to Class B equally |
| Small, scoped changes | Never mass-refactor |
| Blocked if Class A modifies same files | Class A has file priority |
| CHANGELOG entry optional for BG | Reports/proposals don't require CHANGELOG |

### BG Commit Validation

```
function validateBGCommit(bg_ticket):
  staged = git diff --cached --name-only
  classA_files = union(active_classA_worker.touched_files)
  overlap = intersection(staged, classA_files)
  if overlap is not empty:
    return REJECT  # Class A has file priority
  return PASS
```
