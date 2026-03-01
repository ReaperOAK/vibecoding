---
user-invokable: false
---

# Cross-Cutting Agent Protocols

> **Applies to:** ALL subagents. Every agent MUST follow these protocols in
> addition to their domain-specific instructions. ReaperOAK enforces compliance.

## 1. RUG Discipline (Read → Understand → Generate)

Before ANY action:

1. **READ** — Load required context files. Confirm what you found.
2. **UNDERSTAND** — State the objective, list assumptions, declare confidence.
3. **GENERATE** — Produce output that references context from steps 1-2.

If output references patterns not found in loaded context, it's hallucination.
ReaperOAK rejects and re-delegates.

**Orchestrator rule:** ReaperOAK NEVER implements directly — all implementation
is delegated via `runSubagent`. RUG outputs delegation packets, never code.

## 2. Self-Reflection (After Every Deliverable)

Score 5 dimensions (1-10) before submitting:

| Dimension | Question |
|-----------|----------|
| Correctness | Does it work? Evidence? |
| Completeness | All requirements addressed? |
| Convention | Follows project patterns? |
| Clarity | Readable and maintainable? |
| Impact | No regressions? Minimal blast radius? |

**Gate:** ALL dimensions ≥ 7 to submit. If any < 7, self-iterate (max 3).
After 3 iterations, escalate to ReaperOAK with honest scores.

## 3. Confidence Gates

| Level | Range | Action |
|-------|-------|--------|
| HIGH | 90-100% | Proceed |
| MEDIUM | 70-89% | Proceed with flagged risks |
| LOW | 50-69% | Pause — request review |
| INSUFFICIENT | < 50% | Block — escalate with unknowns |

Confidence must cite evidence. "I think it works" = Medium. "Tests prove it" = High.

## 4. Anti-Laziness

Evidence required for every claim:

- "I read the file" → quote a specific pattern found in it
- "Tests pass" → include test output summary
- "Follows conventions" → name the convention from systemPatterns.md
- "Secure" → reference OWASP category checked

## 5. Context Engineering

Load context by priority:
- **P1 (always):** systemPatterns.md, delegation packet, target files
- **P2 (if relevant):** Related tests, API contracts, types
- **P3 (summarize):** Large files where only structure matters
- **P4 (skip):** Unrelated modules, generated files, vendor code

Build a Context Map before modifying code: primary files, secondary files,
test coverage, patterns to follow, suggested change sequence.

## 6. Cross-Agent Communication (File-Based Handoff)

Agents communicate through **files on disk**, not direct messaging. ReaperOAK
runs agents in dependency phases — each phase writes files that subsequent
phases read.

**As a subagent, you MUST:**
1. **Read upstream artifacts** listed in your delegation prompt BEFORE starting
2. **Align your output** with contracts/schemas from prior phases (don't invent
   your own incompatible versions)
3. **Write clean deliverables** to the paths specified — later agents depend on them

**Example flow:**
- Architect writes `docs/api-contracts.yaml` → Backend reads it to implement routes
- Backend writes `server/src/` → QA Engineer reads it to write tests
- All code written → Security Engineer reads it for threat analysis

If upstream artifacts are missing or inconsistent, **STOP and report** to
ReaperOAK rather than guessing.

## 7. Additional Protocols

| Protocol | Summary |
|----------|---------|
| Autonomy Levels | L1 (Supervised), L2 (Guided), L3 (Autonomous) |
| Governance Audit | Timestamp, agent, action, evidence, confidence per action |
| Handoff Protocol | State, pending actions, blockers, validation evidence |
| Failure Recovery | Capture error → analyze → retry (max 3) → escalate |
| Communication | Direct, evidence-based, no hedging without data |

For detailed protocol definitions, templates, and examples, load chunks from
`.github/vibecoding/chunks/_cross-cutting-protocols/`.

## 8. Agent Event Emission Protocol

Every agent MUST emit structured events during ticket execution. ReaperOAK is
the SOLE consumer and router of all events. Agents must NOT directly call or
communicate with each other — ALL inter-agent communication flows through
ReaperOAK's event loop.

### Event Types

| Event Type | When Emitted | Payload |
|-----------|-------------|---------|
| `TASK_STARTED` | Agent begins work on assigned ticket | ticket_id, agent_name, timestamp |
| `TASK_COMPLETED` | Agent finishes with evidence | ticket_id, agent_name, timestamp, evidence (artifact paths, test results, confidence) |
| `TASK_FAILED` | Agent cannot complete | ticket_id, agent_name, timestamp, error_details, suggested_action |
| `NEEDS_INPUT_FROM` | Agent needs output from another agent type | ticket_id, agent_name, target_agent, context, question |
| `BLOCKED_BY` | Agent is blocked by external dependency | ticket_id, agent_name, blocker_description, blocker_type |
| `PROGRESS_UPDATE` | Periodic status during long tasks | ticket_id, agent_name, timestamp, percent_complete, current_step |
| `REQUEST_RESEARCH` | Need research before proceeding | ticket_id, agent_name, research_question |
| `REQUIRES_UI_DESIGN` | UI artifacts needed before Frontend work | ticket_id, agent_name, feature_name, ui_requirements |
| `ESCALATE_TO_PM` | Scope or requirements unclear | ticket_id, agent_name, ambiguity_description |
| `REQUIRES_STRATEGIC_INPUT` | Execution agent needs strategic decision | ticket_id, agent_name, question, suggested_reviewer |

### 8.1 Worker Pool Events

These events are emitted by the elastic worker pool subsystem and consumed by
ReaperOAK's continuous scheduler. Workers are dynamically spawned per ticket
with unique IDs (`{Role}Worker-{shortUuid}`) and terminated after completion.
Pools are **unbounded** — they scale elastically based on ticket backlog with
no artificial upper limit (bounded only by system resources).
See `governance/worker_policy.md` for the full pool policy.

| Event Type | When Emitted | Payload |
|-----------|-------------|--------|
| `WORKER_FREE` | Worker completes ticket and is released | worker_id, pool_role, timestamp, freed_capacity |
| `WORKER_ASSIGNED` | Worker assigned to ticket | worker_id, pool_role, ticket_id, timestamp |
| `WORKER_SPAWNED` | New worker dynamically created for a ticket | worker_id, pool_role, ticket_id, timestamp |
| `WORKER_TERMINATED` | Worker removed from pool (completed, failed, violation, or idle timeout) | worker_id, pool_role, reason, timestamp |
| `POOL_SCALED_UP` | Elastic pool expanded due to backlog growth | pool_role, old_count, new_count, trigger |
| `POOL_SCALED_DOWN` | Elastic pool contracted due to idle workers | pool_role, old_count, new_count, reason |

### Event Payload Format

Emit events as structured markdown in your output:

```
**Event:** TASK_COMPLETED
**Ticket:** TDSA-BE001
**Agent:** Backend
**Timestamp:** 2026-02-27T14:30:00Z
**Details:** Implementation complete. Files created: server/auth.ts, server/auth.test.ts
**Evidence:** All 5 acceptance criteria verified. Confidence: HIGH
**Artifacts:** server/auth.ts, server/auth.test.ts
```

### Emission Rules

1. Every agent MUST emit `TASK_STARTED` at the beginning and either
   `TASK_COMPLETED` or `TASK_FAILED` at the end of every ticket execution.
2. Blocking events (`NEEDS_INPUT_FROM`, `BLOCKED_BY`, `REQUEST_RESEARCH`,
   `REQUIRES_UI_DESIGN`, `ESCALATE_TO_PM`) pause the current ticket.
   ReaperOAK handles routing the request to the appropriate agent and
   passing resolution artifacts back.
3. `PROGRESS_UPDATE` should be emitted periodically during tasks with
   effort > 30 min to provide visibility into long-running work.
4. `TASK_COMPLETED` MUST include evidence — artifact paths, test results,
   and confidence level. Events without evidence are rejected.

### No Direct Agent Communication

Agents must NOT call each other directly. ALL inter-agent communication is
routed through ReaperOAK. This ensures:

- Single point of coordination and audit trail
- No circular dependencies between agents
- ReaperOAK maintains full visibility of system state
- Every interaction is logged for observability

## 9. Anti-One-Shot Guardrails

Hard rules preventing agents from attempting complex work in a single pass
or exceeding ticket scope. These guardrails enforce iterative, evidence-based
delivery.

### Scope Enforcement

- Agent must ONLY respond to the assigned ticket ID
- If output references unrelated tickets → ReaperOAK REJECTS
- If implementation exceeds ticket scope (modifies files not in the ticket's
  write_paths) → Validator REJECTS at QA_REVIEW
- If agent attempts to implement multiple tickets in one response → force
  stop and re-delegate

### Mandatory Iteration Pattern (for tasks with effort > 30 min)

Agents MUST demonstrate iteration rather than attempting one-shot delivery:

1. **Pass 1 — Draft implementation:** Write the initial implementation
   addressing all acceptance criteria
2. **Pass 2 — Self-review:** Check output against acceptance criteria using
   the Self-Reflection protocol (§2). Score all 5 dimensions.
3. **Pass 3 — Fix gaps:** Address any gaps, low scores, or missing criteria
   found during self-review
4. **Pass 4 — Final check:** Confirm all criteria are met, run quality
   scores, verify file scope compliance

**Minimum:** 2 iterations for any task with effort > 30 min. The
Self-Reflection scores (§2) serve as the evidence of iteration.

### Pre-Submission Scope Checks

Before submitting `TASK_COMPLETED`:

1. Compare files modified against the ticket's listed write_paths
2. If any file outside scope was modified → undo the change and report
3. Verify that output references only the assigned ticket ID
4. Confirm all acceptance criteria from the ticket are addressed

### Anti-Batch Detection

ReaperOAK enforces single-ticket focus through these checks:

- Does agent output contain multiple ticket IDs? → REJECT
- Does agent output modify files belonging to other tickets? → REJECT
- Does output exceed expected size for a single ticket? → flag for review
- Does agent output include self-reflection evidence? → required for
  acceptance of `TASK_COMPLETED` events

## 10. Strategic Event Types

These events are emitted only by **strategic-layer agents** (Research Analyst,
Product Manager, Architect, Security Engineer in strategic mode, UIDesigner,
DevOps Engineer in planning mode). Execution-layer agents MUST NOT emit
these events.

| Event Type | When Emitted | Payload |
|-----------|-------------|--------|
| `SDR_PROPOSED` | Strategic agent proposes strategy change | sdr_id, proposer, impact_assessment |
| `SDR_APPROVED` | ReaperOAK approves SDR | sdr_id, approver, affected_tickets |
| `SDR_APPLIED` | SDR changes applied to roadmap | sdr_id, roadmap_version_before, roadmap_version_after |
| `STRATEGIC_REVIEW_REQUIRED` | Execution agent detects strategic issue | ticket_id, issue_description, suggested_reviewer |
| `ARCHITECTURE_RISK_DETECTED` | Architect identifies structural risk | risk_id, severity, affected_components |
| `SCOPE_CONFLICT_DETECTED` | PM identifies scope conflict | conflict_description, affected_tickets |

> **Note:** Strategic events pause the continuous scheduling loop for the
> affected tickets only. Unaffected tickets continue normal execution.

## 11. Operational Integrity Protocol (OIP) — All Agents

> **Canonical Definition:** `.github/agents/ReaperOAK.agent.md` §19
> **Governance Authority:** `.github/agents/_core_governance.md`
> **Governance Policies:** `.github/governance/` (9 policy files)
> **OIP Version:** 1.0.0

The OIP is the self-healing governance layer for Light Supervision Mode.
These rules apply to ALL agents — not just ReaperOAK.

### 11.1 OIP Event Types

All agents must recognize and respond to these OIP-specific events:

| Event | Emitter | Payload | Agent Response |
|-------|---------|---------|---------------|
| `PROTOCOL_VIOLATION` | OIP Drift Detector | ticket_id, violation_id (DRIFT-001 to DRIFT-009), invariant_id, severity, auto_repair | If you caused the violation, expect REWORK or ComplianceWorker intervention |
| `INSTRUCTION_MISALIGNMENT` | Governance Integrity Check | file_path, expected_version, actual_version | Governance file version ≠ system GOVERNANCE_VERSION — report to ReaperOAK |
| `GOVERNANCE_DRIFT` | Governance Integrity Check | drift_type, file_path, details | Duplication, oversized file, or policy misalignment detected |
| `REPAIR_COMPLETED` | ComplianceWorker | ticket_id, violation_id, repair_action | Resume normal ticket processing after repair |
| `REPAIR_FAILED` | ComplianceWorker | ticket_id, violation_id, failure_reason | Expect escalation to human or re-delegation |

### 11.2 Scoped Git Rules (ALL Agents)

When any agent creates a commit or suggests git commands:

**FORBIDDEN:**
- `git add .`
- `git add -A`
- `git add --all`
- Any wildcard or glob pattern in `git add`

**REQUIRED:**
- `git add path/to/file1 path/to/file2 ...` — explicit file listing only
- Files staged MUST match the ticket's declared `file_paths`
- CHANGELOG.md is always an allowed addition

Violation of these rules triggers DRIFT-002 (UNSCOPED_COMMIT).

### 11.3 Memory Bank Entry (ALL Implementing Agents)

Before a ticket can reach COMMIT, the implementing agent MUST ensure a
memory bank entry exists in `.github/memory-bank/activeContext.md`.

**Required format:**
```
### [TICKET-ID] — {summary}
- **Artifacts:** {comma-separated file paths}
- **Decisions:** {key decisions made}
- **Timestamp:** {ISO8601}
```

If you complete a ticket and forget the memory entry, a ComplianceWorker
will be spawned to generate it — but this counts as a DRIFT-003 violation.
Write it yourself to avoid the violation.

### 11.4 Evidence Requirements (ALL Implementing Agents)

Every `TASK_COMPLETED` event MUST include:
- **Artifact paths:** files created or modified
- **Test results:** test output or "N/A" with justification
- **Confidence level:** HIGH (90-100%) | MEDIUM (70-89%) | LOW (50-69%)

Missing evidence triggers DRIFT-007 (UNVERIFIED_EVIDENCE) and returns the
ticket to IMPLEMENTING.

### 11.5 Single-Ticket Scope (ALL Agents)

Your output MUST reference ONLY your assigned ticket ID. If your response
contains references to other ticket IDs (pattern: `[A-Z]+-[A-Z]+\d{3}`
excluding your assigned ticket), you will be:
1. Immediately terminated (WORKER_TERMINATED)
2. A fresh worker spawned for REWORK
3. This is a HARD KILL — no warning, no retry within the same instance

### 11.6 ComplianceWorker Protocol

ComplianceWorkers are specialized repair agents:
- Spawned on PROTOCOL_VIOLATION with `auto_repair: true`
- Perform exactly ONE repair action per spawn
- Emit REPAIR_COMPLETED or REPAIR_FAILED
- Terminate after single action
- Do NOT run the full 9-state lifecycle
- Only repair the specific missing artifact or state

### 11.7 Health Sweep Awareness

All agents should be aware that ReaperOAK runs a continuous health sweep
that checks for:
1. Orphan tickets (stalled > 45 min)
2. Expired locks (> 30 min)
3. Missing memory entries (last 3 DONE tickets)
4. Incomplete post-chain audit trails
5. Scope drift (modified files ≠ declared paths)

If the health sweep detects an issue with your ticket, you may be terminated
and your ticket re-queued. This is normal OIP behavior, not an error.
