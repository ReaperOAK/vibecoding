# L1: Capability Breakdown

## L1-CAP-001: Deterministic Policy Enforcement via Hooks
**Priority:** P0 — Critical
**Impact:** HIGH — Converts "please follow" rules into "will be blocked" enforcement
**Description:** Implement the VS Code hooks system (`.github/hooks/`) to deterministically enforce guardian stop, scoped git rules, tool ACLs, memory gate, and evidence requirements. Replaces instruction-only enforcement with shell-script-backed policy gates.

## L1-CAP-002: Native Agent Orchestration (Subagents + Handoffs)
**Priority:** P0 — Critical
**Impact:** HIGH — Enables structured delegation and workflow chaining
**Description:** Add `agents` field to CTO and Ticketer for subagent scoping. Add `handoffs` field for SDLC stage transitions. Replace manual `continue.prompt.md` chaining with native VS Code handoff buttons. Add `disable-model-invocation` to prevent CTO from being invoked as subagent.

## L1-CAP-003: Agent Definition Hardening
**Priority:** P1 — High
**Impact:** HIGH — Tightens tool access controls and eliminates redundant context
**Description:** Audit and tighten `tools` arrays per agent (currently near-identical across agents). Convert references to Markdown links for auto-inclusion. Add agent-scoped hooks for per-role validation. Add `argument-hint` for user-invocable agents.

## L1-CAP-004: Prompt File & Instruction Optimization
**Priority:** P1 — High
**Impact:** MEDIUM — Reduces context bloat and improves routing
**Description:** Add `agent` field to prompt files (routing `/start` → CTO, `/continue` → Ticketer). Add `tools` field to prompt files. Split always-on instructions into pattern-scoped where applicable.

## L1-CAP-005: Skills System Migration
**Priority:** P2 — Medium
**Impact:** MEDIUM — Standardizes context chunks for portability
**Description:** Convert `.github/vibecoding/chunks/` to standard `.github/skills/` format with `SKILL.md` files. Makes chunks discoverable, portable across VS Code/CLI/GitHub coding agent.

## L1-CAP-006: MCP Infrastructure Improvement
**Priority:** P2 — Medium
**Impact:** MEDIUM — Better tool management and sandboxing
**Description:** Evaluate and create a custom `tickets.py` MCP server to replace CLI-based ticket management. Enable MCP sandboxing for worker agents. Create MCP resources for agent output sharing.
