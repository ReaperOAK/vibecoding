# Agent Boot Protocol

This file is loaded automatically on every agent interaction. It is the
enforcement layer for the multi-agent vibecoding system.

## 1. Session Start (Mandatory)

Before doing ANY work, read these memory bank files in order:

1. `.github/memory-bank/activeContext.md` — current focus and recent changes
2. `.github/memory-bank/progress.md` — what's done, what's pending
3. `.github/memory-bank/systemPatterns.md` — architecture decisions (immutable)
4. `.github/memory-bank/productContext.md` — project vision and objectives

Only read `decisionLog.md` and `riskRegister.md` if the task involves
architecture decisions or security concerns.

## 2. Safety Check (Mandatory)

Read `.github/guardian/STOP_ALL` before executing any file modifications.
If the file contains `STOP`, stop immediately and report to the user.

## 3. Governance & Context Loading (Mandatory)

### Governance Authority

Read `.github/agents/_core_governance.md` — this is the **canonical
governance authority**. It indexes all governance policy files in
`.github/governance/` (lifecycle, worker policy, commit policy, memory,
UI, security, events, context injection, performance monitoring).
No agent may override these rules.

### Domain Chunks

All domain guidance is pre-chunked in `.github/vibecoding/chunks/`.
There are no `.instructions.md` files — chunks are the sole source of truth.

**BEFORE your first action, load your domain chunks:**

1. Read ALL files in `.github/vibecoding/chunks/{YourAgent}.agent/`
   (e.g., Backend → `Backend.agent/`, Frontend → `Frontend.agent/`)
   — typically 2 files, ~8000 tokens. These are your detailed protocols.
2. For task-specific guidance, check `.github/vibecoding/catalog.yml`
   for relevant semantic tags (e.g., `testing:`, `security:`, `governance:`)
3. Read additional chunks listed under those tags as needed

**If you skip chunk loading, you are operating without your protocols.
Your output quality will be lower and ReaperOAK may reject your work.**

## 4. Agent Definitions

Agent roles and permissions are defined in `.github/agents/*.agent.md`.
Each agent file specifies:

- `allowed_read_paths` / `allowed_write_paths` — file access scope
- `forbidden_actions` — hard prohibitions
- `allowed_tools` — tool access whitelist
- `evidence_required` — whether claims need tool output proof

**ReaperOAK is a PURE ORCHESTRATOR.** It NEVER writes code, creates files, or
runs implementation commands. ReaperOAK operates a ticket-driven event loop:
SELECT one READY ticket → LOCK → DELEGATE to implementing agent → run
mandatory post-execution chain (QA → Validator → Documentation → CI Reviewer
→ Commit) → DONE. Each ticket traverses a 9-state machine (READY → LOCKED →
IMPLEMENTING → QA_REVIEW → VALIDATION → DOCUMENTATION → CI_REVIEW → COMMIT → DONE).

When delegating to a subagent, use the delegation packet schema at
`.github/tasks/delegation-packet-schema.json`.

**Worker Pool Model.** Each agent role is backed by an **unbounded elastic
pool** of workers. There is no maxSize cap — pools scale purely based on
ticket backlog (bounded only by system resources). Workers are spawned
dynamically per ticket with unique IDs using the format
`{Role}Worker-{shortUuid}` (e.g., `BackendWorker-a1b2c3`). Each worker
processes EXACTLY ONE ticket — no worker reuse across tickets. Workers are
stateless, ephemeral instances created via `runSubagent` and terminated after
ticket completion. All conflict-free READY tickets are dispatched in parallel.
See `governance/worker_policy.md` for full pool policy.

**Two-Layer Orchestration.** The agent roster is organized into two
concurrent layers that run simultaneously without phase barriers:

- **Strategic Layer** — Research Analyst, Product Manager, Architect,
  Security Engineer (threat modeling only), UIDesigner (conceptual design
  only), DevOps Engineer (infrastructure planning only). This layer produces
  roadmap artifacts: PRDs, ADRs, threat models, design specifications, and
  Strategic Decision Records (SDRs). Its output feeds the ticket pipeline.
- **Execution Layer** — Backend, Frontend Engineer, DevOps Engineer
  (execution), QA Engineer, Security Engineer (execution), Documentation
  Specialist, Validator, CI Reviewer. This layer consumes strategic
  artifacts and processes tickets through the 9-state machine.

Some agents span both layers with different capabilities per layer: Security
Engineer operates strategically for threat modeling and executionally for
SBOM/scans; DevOps Engineer operates strategically for capacity planning and
executionally for CI/CD and IaC.

**Strategy Evolution.** Strategic Decision Records (SDRs) enable mid-execution
strategy changes without halting unaffected work. SDR lifecycle:
PROPOSED → APPROVED → APPLIED → ARCHIVED. Only strategic-layer agents may
propose SDRs. Each approved SDR increments the roadmap minor version
(v1.0 → v1.1 → v1.2). SDRs that affect in-flight tickets trigger
re-prioritization but do NOT halt execution unless explicitly flagged as
blocking. Rejected SDRs are archived with a rejection reason.

**TODO Agent** is invokable only by ReaperOAK. No other agent may delegate
to it or invoke it directly. TODO Agent is a progressive refinement
decomposition engine with **3 operating modes**:

- **Strategic Mode** (L0→L1): Decomposes project vision into capabilities
- **Planning Mode** (L1→L2): Expands one capability into execution blocks
- **Execution Planning Mode** (L2→L3): Expands one block into actionable tasks

TODO Agent operates in one of 3 modes per invocation. ReaperOAK selects
the appropriate mode based on the current decomposition layer.

**TODO Agent invocation:** For any multi-step feature request, ReaperOAK
MUST first invoke the TODO Agent in Strategic Mode (L0→L1) to identify
capabilities, then progressively refine through Planning Mode (L1→L2) and
Execution Planning Mode (L2→L3) before entering the BUILD phase. Each L3
task is a "ticket" in the ticket-driven model, entering the 9-state machine
at READY.

**TODO Agent never initiates strategic decisions.** If strategic input is
needed during decomposition (unclear scope, missing architecture decision,
conflicting requirements), TODO emits `REQUIRES_STRATEGIC_INPUT` with the
specific question and waits for ReaperOAK to route the request to the
appropriate strategic-layer agent. After resolution, ReaperOAK passes the
answer back to TODO Agent to continue decomposition.

**TODO directory structure:**

- `TODO/vision.md` — L0 vision statement + L1 capabilities list
- `TODO/capabilities.md` — L1 capability details with status
- `TODO/blocks/` — L2 execution blocks per capability
- `TODO/tasks/` — L3 actionable tasks per block
- `TODO/micro/` — L4 micro-tasks (optional, only when triggered)

**Validator Agent** is an independent compliance reviewer with special
authority to **reject task completion**. It verifies Definition of Done
compliance, SDLC stage adherence, quality gates, and pattern conformance.
The Validator cannot implement code — it only reads artifacts and writes
validation reports. Its rejection blocks advancement past QA_REVIEW.

**Validator Agent invocation:** Validator is invoked as part of the mandatory
post-execution chain at the QA_REVIEW state of every ticket. No agent may
self-validate.

## 5. Human Approval Required

Never execute these without explicit user confirmation:

- Database drops, mass deletions, force pushes
- Production deployments or merges to main
- New external dependency introduction
- Schema migrations that alter or drop columns
- Any operation with irreversible data loss potential

## 6. Memory Updates

Update memory bank files when:

- Focus shifts → append to `activeContext.md`
- Milestone completes → append to `progress.md`
- Significant trade-off made → append to `decisionLog.md` (ReaperOAK only)
- New threat identified → append to `riskRegister.md`

All updates are append-only. Never delete existing entries.

### OIP Memory Enforcement (§24 of ReaperOAK.agent.md)

Every ticket MUST have a memory bank entry before reaching COMMIT state.
Required format in `activeContext.md`:

```
### [TICKET-ID] — Summary
- **Artifacts:** file1.ts, file2.ts
- **Decisions:** Chose X over Y because Z
- **Timestamp:** 2026-02-28T15:00:00Z
```

Missing entries trigger DRIFT-003 violation and ComplianceWorker auto-repair.
Write the entry yourself to avoid violations.

## 7. Loop Prevention

If you notice yourself:
- Making the same tool call more than 3 times with identical parameters
- Editing the same file back and forth
- Retrying the same failed approach

Stop. Re-read the task objective. Try a different approach or escalate.

## 8. Cross-Cutting Protocols (ALL Agents)

### RUG Discipline (Read → Understand → Generate)

Before ANY action:
1. **READ** — Load required context files. Confirm what you found.
2. **UNDERSTAND** — State the objective, list assumptions, declare confidence.
3. **GENERATE** — Produce output that references context from steps 1-2.

If your output references patterns not found in loaded context, it's
hallucination. ReaperOAK will reject and re-delegate.

### Upstream Artifact Reading (Cross-Agent Communication)

Agents communicate through **files on disk**. ReaperOAK runs agents in
dependency phases — each phase writes files that subsequent phases read.

**You MUST:**
1. Read **upstream artifacts** listed in your delegation prompt BEFORE starting
2. Align your output with contracts/schemas from prior phases — don't invent
   your own incompatible versions
3. Write clean deliverables to the paths specified — later agents depend on them

If upstream artifacts are missing or inconsistent, **STOP and report** to
ReaperOAK rather than guessing.

### Evidence & Confidence

Every claim needs evidence:
- "I read the file" → quote a specific pattern found in it
- "Tests pass" → include test output
- "Follows conventions" → name the convention from systemPatterns.md

Confidence levels: HIGH (90-100%, proceed) | MEDIUM (70-89%, flag risks) |
LOW (50-69%, pause for review) | INSUFFICIENT (<50%, block and escalate).

### Task-Level SDLC Compliance (Ticket Lifecycle)

Every ticket traverses a mandatory 9-state machine:

```
READY → LOCKED → IMPLEMENTING → QA_REVIEW → VALIDATION → DOCUMENTATION → CI_REVIEW → COMMIT → DONE
```

**Rules:**
- No state may be skipped. Guard conditions enforce every transition.
- At IMPLEMENTING, the assigned agent works on the ticket and emits
  `TASK_COMPLETED` or `TASK_FAILED` when done.
- At QA_REVIEW, the mandatory post-execution chain runs: QA Engineer reviews
  test coverage → Validator checks Definition of Done compliance → if both
  pass, ticket advances to VALIDATION.
- At DOCUMENTATION, Documentation Specialist updates relevant docs.
- At CI_REVIEW, CI Reviewer checks lint/type/complexity.
- At COMMIT, ReaperOAK enforces `git commit` → ticket advances to DONE.
- If any chain member rejects, the ticket enters REWORK → re-delegated to
  the implementing agent. Max 3 rework iterations before escalation.
- Agents must emit structured events (`TASK_STARTED`, `TASK_COMPLETED`,
  `TASK_FAILED`, `NEEDS_INPUT_FROM`, `BLOCKED_BY`) at state transitions
  — see `_cross-cutting-protocols.md` §8.
- Agents must follow the anti-one-shot guardrails
  — see `_cross-cutting-protocols.md` §9.

**References:**
- Definition of Done template: `.github/tasks/definition-of-done-template.md`
- Initialization checklist: `.github/tasks/initialization-checklist-template.md`
- Cross-cutting protocols: `.github/agents/_cross-cutting-protocols.md`

## 9. Operational Integrity Protocol (OIP)

> **Canonical Definition:** `.github/agents/ReaperOAK.agent.md` §19
> **Governance Authority:** `.github/agents/_core_governance.md`
> **Cross-Cutting Rules:** `.github/agents/_cross-cutting-protocols.md` §11
> **Governance Policies:** `.github/governance/` (9 policy files)

The OIP is the self-healing governance layer for Light Supervision Mode
(Model B). It applies to ALL agents. Key rules:

### Scoped Git (INV-3)
- NEVER use `git add .`, `git add -A`, or `git add --all`
- ALWAYS list files explicitly in `git add`
- Violation triggers DRIFT-002

### Memory Gate (INV-4)
- Every ticket MUST have a memory entry before COMMIT
- 5 required fields: ticket_id, summary, artifacts, decisions, timestamp
- Violation triggers DRIFT-003

### Single-Ticket Scope (INV-8)
- Workers operate ONLY on their assigned ticket
- Referencing other ticket IDs → immediate termination
- This is a HARD KILL — no warning

### Evidence (INV-6)
- TASK_COMPLETED must include: artifact paths, test results, confidence level
- Missing evidence → DRIFT-007 → return to IMPLEMENTING

### ComplianceWorker
- Auto-spawned on PROTOCOL_VIOLATION with `auto_repair: true`
- Performs targeted single-action repair
- Only blocks the affected ticket — all other tickets continue

### Health Sweep
- 5 checks every scheduling interval
- Auto-corrects: stalled tickets, expired locks, missing memory, incomplete chains, scope drift

For the full OIP specification, read `.github/agents/ReaperOAK.agent.md` §19.
