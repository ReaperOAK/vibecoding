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

## 6. Additional Protocols

| Protocol | Summary |
|----------|---------|
| Autonomy Levels | L1 (Supervised), L2 (Guided), L3 (Autonomous) |
| Governance Audit | Timestamp, agent, action, evidence, confidence per action |
| Handoff Protocol | State, pending actions, blockers, validation evidence |
| Failure Recovery | Capture error → analyze → retry (max 3) → escalate |
| Communication | Direct, evidence-based, no hedging without data |

For detailed protocol definitions, templates, and examples, load chunks from
`.github/vibecoding/chunks/_cross-cutting-protocols/`.
