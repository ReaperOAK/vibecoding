# L2: Execution Blocks

## L2-BLK-001: Hook Infrastructure Setup (from L1-CAP-001)
**Depends on:** Nothing
**Description:** Create `.github/hooks/` directory structure, implement core hook scripts, and configure hook file locations in VS Code settings.

### Sub-blocks:
- L2-BLK-001a: Create hook script framework (directory, base scripts, JSON configs)
- L2-BLK-001b: Guardian stop hook (SessionStart + PreToolUse)
- L2-BLK-001c: Scoped git enforcement hook (PreToolUse — block `git add .`)
- L2-BLK-001d: Memory gate enforcement hook (Stop/SubagentStop)
- L2-BLK-001e: Evidence rule enforcement hook (Stop)
- L2-BLK-001f: Destructive command blocking hook (PreToolUse)

---

## L2-BLK-002: Subagent Scoping (from L1-CAP-002)
**Depends on:** Nothing
**Description:** Add `agents` field to CTO and Ticketer. Add `disable-model-invocation` to CTO. Scope which agents can invoke which subagents.

### Sub-blocks:
- L2-BLK-002a: CTO subagent scoping (`agents: [Research, ProductManager, Architect, TODO]`)
- L2-BLK-002b: Ticketer subagent scoping (`agents: [Backend, Frontend, ...]`)
- L2-BLK-002c: Add `disable-model-invocation: true` to CTO

---

## L2-BLK-003: Handoffs Implementation (from L1-CAP-002)
**Depends on:** L2-BLK-002
**Description:** Add `handoffs` field to agents for SDLC stage transitions. Create handoff definitions for common workflows.

### Sub-blocks:
- L2-BLK-003a: CTO→Ticketer handoff (post ticket creation)
- L2-BLK-003b: Cross-stage handoffs for implementing agents (Backend→QA, QA→Security, etc.)
- L2-BLK-003c: Rework handoffs (QA→Backend rework, Security→Backend rework)

---

## L2-BLK-004: Agent Tool Loadout Hardening (from L1-CAP-003)
**Depends on:** Nothing
**Description:** Audit all 15 agent files, remove unauthorized tools from `tools` arrays, ensure each agent has minimum-necessary toolset.

### Sub-blocks:
- L2-BLK-004a: Audit orchestrator agents (CTO, Ticketer, TODO)
- L2-BLK-004b: Audit implementing agents (Backend, Frontend, DevOps, UIDesigner)
- L2-BLK-004c: Audit review agents (QA, Security, CIReviewer, Validator)
- L2-BLK-004d: Audit support agents (Research, ProductManager, Documentation, Architect)

---

## L2-BLK-005: Reference Link Conversion (from L1-CAP-003)
**Depends on:** Nothing
**Description:** Convert all agent "References" sections from plain text to proper Markdown links so VS Code auto-includes referenced instruction content.

---

## L2-BLK-006: Agent-Scoped Hooks (from L1-CAP-003)
**Depends on:** L2-BLK-001
**Description:** Add `hooks` field to individual agents for role-specific validation. Enable `chat.useCustomAgentHooks` setting.

### Sub-blocks:
- L2-BLK-006a: Backend/Frontend PostToolUse lint hook
- L2-BLK-006b: QA/Validator Stop hook (verify test coverage)
- L2-BLK-006c: Ticketer PreToolUse hook (block code file modifications)

---

## L2-BLK-007: Prompt File Enhancement (from L1-CAP-004)
**Depends on:** L2-BLK-002
**Description:** Add `agent`, `tools`, and `model` fields to all 6 prompt files.

---

## L2-BLK-008: Instruction Scoping (from L1-CAP-004)
**Depends on:** Nothing
**Description:** Split always-on instructions into pattern-scoped where applicable. Add new targeted instruction files for specific file types.

---

## L2-BLK-009: Skills Migration (from L1-CAP-005)
**Depends on:** Nothing
**Description:** Convert vibecoding chunks to standard `.github/skills/` format.

---

## L2-BLK-010: MCP Ticket Server (from L1-CAP-006)
**Depends on:** Nothing
**Description:** Create a custom MCP server that wraps `tickets.py` functionality. Exposes `createTicket`, `claimTicket`, `advanceStage`, `getStatus` as typed tools.

---

## L2-BLK-011: VS Code Settings Configuration (from L1-CAP-001 + L1-CAP-003)
**Depends on:** L2-BLK-001
**Description:** Configure VS Code workspace settings for hooks, agent features, tool approval patterns.
