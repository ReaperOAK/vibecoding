---
name: init
description: This prompt initializes the legacy repository takeover process, guiding the system through structured reconstruction before resuming normal autonomous execution.
---
We are entering LEGACY REPOSITORY TAKEOVER MODE.

This repository was not built under the autonomous orchestration system.
It may contain:
- Incomplete features
- No tickets
- No roadmap
- Partial docs
- Architectural drift
- Inconsistent patterns
- Broken tests
- Missing validation
- Technical debt
- Untracked requirements

You must NOT begin implementing features immediately.

You must perform structured reconstruction.

---

# PHASE 1 — CHAOS DIAGNOSIS (Parallel Discovery)

Spawn multiple agents in parallel:

Research:
- Analyze folder structure.
- Identify main modules.
- Detect frameworks, languages, build system.
- Identify entry points.
- Identify dependency graph.
- Identify unreferenced files.
- Detect unused dependencies.
- Summarize current capabilities.

Architect:
- Reverse-engineer system architecture.
- Identify architectural style.
- Identify violations of clean boundaries.
- Detect circular dependencies.
- Detect missing abstraction layers.
- Detect scaling risks.
- Detect missing infra components.

QA:
- Detect test presence.
- Detect coverage gaps.
- Detect missing test harness.
- Detect failing tests (if runnable).
- Identify critical untested flows.

Security:
- Scan for obvious vulnerabilities.
- Detect exposed secrets.
- Detect unsafe patterns.
- Detect missing auth flows.
- Identify insecure configs.

Documentation:
- Scan README.
- Compare docs vs code.
- Detect outdated docs.
- Detect missing setup steps.
- Detect mismatches.

DevOps:
- Detect CI/CD.
- Detect Docker presence.
- Detect deployment configs.
- Detect environment variable usage.
- Detect missing staging config.

Run at least 10 agents in parallel.
If fewer than 10 discovery tasks exist, spawn background audits.

No implementation allowed in this phase.

Deliver:
- CHAOS_REPORT.md
- ARCHITECTURE_RECONSTRUCTION.md
- GAP_ANALYSIS.md
- TECH_DEBT_REPORT.md
- SECURITY_AUDIT_SUMMARY.md

---

# PHASE 2 — RECONSTRUCT INTENT

If no PRD exists:

ProductManager must:
- Infer product intent from code.
- Identify user flows.
- Identify features implemented.
- Identify half-built features.
- Identify missing features implied by code.
- Generate RECONSTRUCTED_PRD.md

Research must:
- Compare inferred product to market alternatives.
- Identify obvious missing features.
- Identify improvement opportunities.

Architect must:
- Draft TARGET_ARCHITECTURE.md
- Compare current vs target architecture.
- Identify refactor zones.

Do NOT modify code yet.

---

# PHASE 3 — TICKET GENERATION

TODO.agent must:

1. Convert gap analysis into:
   - Stabilization tickets
   - Refactor tickets
   - Missing feature tickets
   - Infra tickets
   - Security tickets
   - Documentation tickets

2. Create dependency graph.
3. Mark blockers.
4. Estimate impact.
5. Prioritize stabilization over new features.
6. Create structured task files.

Tickets must be granular.
One change per ticket.
Beginner-friendly clarity.

No implementation yet.

---

# PHASE 4 — STABILIZATION FIRST

Before feature work:

Execute in parallel:
- Critical bug fixes
- Broken build fixes
- Security patches
- Failing tests repair
- CI setup
- Missing lint rules

Each ticket must:
- Follow full SDLC
- Trigger QA
- Trigger Validator
- Trigger Documentation
- Commit atomically

Parallel execution allowed if no file conflict.

Maintain minimum 10 active workers.
Use background agents if backlog low.

---

# PHASE 5 — CONTROLLED DEVELOPMENT RESUMPTION

Only after:

- Build passes
- Critical tests exist
- CI exists
- Architecture doc exists
- PRD reconstructed

Then continue normal autonomous execution:
- Ticket by ticket
- Parallelized
- Full SDLC loop
- Strict commit rules
- Memory updates
- Observability updates

---

# SPECIAL RULES FOR LEGACY MODE

1. Do NOT mass-refactor blindly.
2. Do NOT rewrite entire modules without architectural justification.
3. Do NOT delete files without dependency analysis.
4. Do NOT auto-format entire codebase.
5. Avoid sweeping changes.
6. Prefer incremental stabilization.
7. Maintain compatibility unless explicitly approved.
8. Generate migration tickets instead of silent rewrites.

---

# CONFLICT HANDLING

If major architectural inconsistency found:

Emit:
ARCHITECTURE_REWRITE_REQUIRED

Pause affected tickets only.
Produce refactor roadmap.
Resume after plan approved.

---

# DELIVERABLES

1. Chaos report
2. Reconstructed PRD
3. Target architecture
4. Gap analysis
5. Ticket tree
6. Stabilization completion
7. Updated README
8. Clean CI pipeline
9. Security baseline
10. Resume normal orchestration

System must transition from:

Unstructured vibecoded chaos

to

Governed, ticket-driven, production-grade engineering system.

Do not skip reconstruction.
Do not jump to coding.
Stabilize first.
Then build.