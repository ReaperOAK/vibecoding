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
If the file contains `HALT_ALL`, stop immediately and report to the user.

## 3. Context Loading

All domain guidance is pre-chunked in `.github/vibecoding/chunks/`.
There are no `.instructions.md` files — chunks are the sole source of truth.

**To load context for a domain:**

1. Check `.github/vibecoding/catalog.yml` for the relevant semantic tag
2. Read only the chunks listed under that tag
3. Each chunk is ≤4000 tokens — load only what the current task needs

**Example:** For accessibility guidance, look up `accessibility:` in
catalog.yml and read the listed chunk files.

## 4. Agent Definitions

Agent roles and permissions are defined in `.github/agents/*.agent.md`.
Each agent file specifies:

- `allowed_read_paths` / `allowed_write_paths` — file access scope
- `forbidden_actions` — hard prohibitions
- `allowed_tools` — tool access whitelist
- `evidence_required` — whether claims need tool output proof

**ReaperOAK is a PURE ORCHESTRATOR.** It NEVER writes code, creates files, or
runs implementation commands. It decomposes tasks and delegates ALL
implementation to subagents via `runSubagent` — in PARALLEL when possible.

When delegating to a subagent, use the delegation packet schema at
`.github/tasks/delegation-packet-schema.json`.

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
