---
id: risk-register
version: "1.0"
owner: [Security, Ticketer]
write_access: [Security, Ticketer]
append_only: true
---

# Risk Register

> **Schema Version:** 1.0
> **Owner:** Security Agent
> **Write Access:** Security agent (append), Ticketer (full)
> **Lock Rules:** Only Security agent and Ticketer may write. All other
> subagents have read-only access. No entry may be deleted — only marked as
> mitigated or accepted.
> **Update Protocol:** Append new risks with timestamp, severity, and
> mitigation plan. Update existing risks only to change status or add
> mitigation evidence.

---

## Risk Entry Format

```
### RISK-{number}: {title}
- **Date Identified:** YYYY-MM-DD
- **Identified By:** {agent or human}
- **Severity:** Critical | High | Medium | Low
- **Likelihood:** High | Medium | Low
- **Category:** Security | Operational | Technical | Compliance
- **Description:** What could go wrong
- **Impact:** What happens if it occurs
- **Mitigation:** How to prevent or reduce it
- **Status:** Open | Mitigated | Accepted | Closed
- **Evidence:** Proof of mitigation if applicable
```

---

## Active Risks

### RISK-001: Memory Poisoning via Subagent Hallucination

- **Date Identified:** 2026-02-21
- **Identified By:** Ticketer
- **Severity:** High
- **Likelihood:** Medium
- **Category:** Security
- **Description:** A subagent could write false or contradictory information to
  shared memory bank files, corrupting the system's understanding of the project
- **Impact:** Downstream agents make decisions based on false context, producing
  incorrect code or architecture
- **Mitigation:** `systemPatterns.md` and `decisionLog.md` are write-locked to
  Ticketer only. Subagents can only append to `activeContext.md` and
  `progress.md`. All entries are timestamped and attributed.
- **Status:** Mitigated
- **Evidence:** Lock rules enforced in memory bank file headers

### RISK-002: Prompt Injection in External Content

- **Date Identified:** 2026-02-21
- **Identified By:** Ticketer
- **Severity:** Critical
- **Likelihood:** Medium
- **Category:** Security
- **Description:** Malicious content fetched from external URLs or APIs could
  contain prompt injection patterns that override agent behavior
- **Impact:** Agent executes unintended actions, leaks data, or escalates
  privileges
- **Mitigation:** External content sanitization protocol defined in
  `security.agentic-guardrails.instructions.md`. All external content treated as untrusted.
  Content boundaries enforced via delimiters.
- **Status:** Mitigated
- **Evidence:** Guardrails document created

### RISK-003: Token Runaway / Infinite Loop

- **Date Identified:** 2026-02-21
- **Identified By:** Ticketer
- **Severity:** High
- **Likelihood:** Low
- **Category:** Operational
- **Description:** A subagent enters an infinite retry loop, consuming
  excessive tokens/compute without producing results
- **Impact:** Cost runaway, context window exhaustion, system stall
- **Mitigation:** Maximum retry limit (3) per task. Timeout budgets in
  delegation packets. Loop counter in Plan-Act-Reflect cycle. Ticketer
  monitors iteration count.
- **Status:** Mitigated
- **Evidence:** Orchestration rules define loop detection heuristic

### RISK-004: Unauthorized Privilege Escalation

- **Date Identified:** 2026-02-21
- **Identified By:** Ticketer
- **Severity:** Critical
- **Likelihood:** Low
- **Category:** Security
- **Description:** A subagent attempts to use tools outside its allowed set or
  modify files outside its scope
- **Impact:** Unauthorized code changes, security config modifications,
  production access
- **Mitigation:** Each subagent has explicit `allowed_tools` list and
  `scopeBoundaries`. Tool access enforced at delegation time. Forbidden actions
  list in each agent definition.
- **Status:** Mitigated
- **Evidence:** Subagent files define explicit boundaries

---

## Closed Risks

<!-- Risks that have been resolved or are no longer applicable -->

_None_

### RISK-005: Ticket Resource Path Traversal

- **Date Identified:** 2026-03-27
- **Identified By:** Security
- **Severity:** High
- **Likelihood:** Medium
- **Category:** Security
- **Description:** The MCP ticket resource reads `ticket://{ticket_id}` by joining the caller-controlled `ticket_id` directly into `tickets/{ticket_id}.json` without validating path separators or canonical path containment.
- **Impact:** A caller can read JSON files outside the intended `tickets/` directory, including ticket-state documents that expose stage and operational metadata.
- **Mitigation:** Validate ticket IDs against a strict allowlist, resolve the candidate path, verify it stays under the canonical `tickets/` directory, and add traversal regression tests.
- **Status:** Open
- **Evidence:** `agent-output/Security/TASK-VIB-008.md` documents a successful read of `../ticket-state/READY/TASK-VIB-009` through the resource handler.

### RISK-005: Ticket Resource Path Traversal
- **Date Identified:** 2026-03-27
- **Identified By:** Security
- **Severity:** High
- **Likelihood:** Medium
- **Category:** Security
- **Description:** ticket://{ticket_id} can escape tickets/ through relative paths.
- **Impact:** callers can read ticket-state JSON outside the intended resource boundary.
- **Mitigation:** allowlist IDs, enforce canonical containment, add regression tests.
- **Status:** Open
- **Evidence:** agent-output/Security/TASK-VIB-008.md

### RISK-006: TASK-VIB-009 Backend Work Not Committed
- **Date Identified:** 2026-03-27T06:57:31.963845+00:00
- **Identified By:** QA
- **Severity:** High
- **Likelihood:** Already occurred
- **Category:** Process/Quality
- **Description:** Backend agent claimed completion but did not commit prompt handler implementation to server.py.
- **Impact:** Ticket incorrectly advanced through CI/QA pipeline; rework required.
- **Mitigation:** Backend agent must verify commits exist before marking stage complete.
- **Status:** Open (REWORK in progress)
- **Evidence:** agent-output/QA/TASK-VIB-009.md

### RISK-007: Transitive Lodash Advisory in Extension Toolchain
- **Date Identified:** 2026-04-09
- **Identified By:** Security
- **Severity:** High
- **Likelihood:** Medium
- **Category:** Security
- **Description:** `npm audit --audit-level=high` in `extension/` reports a high-severity transitive lodash advisory (GHSA-r5fr-rjxr-66jc / CWE-94) in the development dependency graph.
- **Impact:** Potential code-injection exposure in affected tooling contexts if vulnerable code paths are invoked.
- **Mitigation:** Update/override transitive dependency chain to a patched lodash version in a dedicated dependency-hardening ticket; rerun audit to verify zero high/critical findings.
- **Status:** Open
- **Evidence:** Security stage audit output during TASK-VIB-012 review (2026-04-09).

### [TASK-VIB-010] Dependency Risk Escalation
- **Timestamp:** 2026-04-09T16:34:30Z
- **Agent:** Security
- **Risk:** High severity vulnerable component in extension dependency graph
- **Details:** npm audit reports lodash GHSA-r5fr-rjxr-66jc (CWE-94, CVSS 8.1) and brace-expansion GHSA-f886-m6hf-6m8v (CWE-400)
- **Severity:** HIGH
- **Recommended Fix:** Upgrade/override transitive dependencies to patched versions and re-run npm audit with zero high/critical findings

### RISK-008: Orchestration Boot Path Drift
- **Date Identified:** 2026-04-10
- **Identified By:** Security
- **Severity:** Low
- **Likelihood:** Medium
- **Category:** Operational
- **Description:** `.github/instructions/agent-orchestration.instructions.md` references `.github/vibecoding/chunks/` in required boot sequence, but that path is not present in the current repository layout.
- **Impact:** Agents can be forced into ambiguous boot-sequence behavior (strict-fail vs implicit skip), reducing governance consistency and audit repeatability.
- **Mitigation:** Update the boot-sequence step to point to existing chunk/reference sources used by the current catalog and skills layout.
- **Status:** Accepted
- **Evidence:** `agent-output/Security/TASK-GHO-SYS002.md` SARIF finding `SEC-ORCH-001`.
