# L1 — Vibecoding System Improvements: Capability Breakdown

**Date:** 2026-03-26  
**L0 Vision:** Upgrade the vibecoding multi-agent SDLC system to leverage the latest VS Code/GitHub Copilot platform APIs, fix critical infrastructure bugs, and improve agent governance quality and cost efficiency.

---

## L1.1 — Infrastructure Integrity

**Owner Domain:** infra  
**Priority:** P0 (Critical — blocks all agents from loading catalog context and blocks automated policy enforcement)

Restore foundational infrastructure correctness:
- Create `.github/vibecoding/` directory and canonical `catalog.yml` so the boot sequence path referenced by all instruction files actually exists and agents can load context chunks.
- Enable all governance hooks in `policy-enforcement.json` and `auto-sync.json` so the STOP_ALL guardian check, `git add .` blocking, destructive-op blocking, and evidence verification are actually enforced at runtime rather than silently skipped.

**Items covered:** #1 (catalog path bug), #2 (governance hooks disabled)

---

## L1.2 — MCP Server Core Transport

**Owner Domain:** backend  
**Priority:** P0 (Critical — MCP server cannot receive any calls without a transport layer)

Implement proper JSON-RPC/stdio transport in the ticket MCP server so it is a functioning MCP server. The tool schema definitions are already correct; they just need to be wrapped with the `mcp` Python SDK (FastMCP pattern) and exposed via stdio transport per the MCP protocol specification.

**Items covered:** #3 (MCP server missing transport)

---

## L1.3 — Agent Governance Configuration

**Owner Domain:** infra (config)  
**Priority:** P1 (High — improves cost efficiency and security boundary enforcement)

Harden the agent configuration layer:
- Wire `.github/tool-sets/` definitions to agent frontmatter so `#universal`, `#research`, and `#code-editing` shorthand reduces tool sprawl and context exhaustion.
- Add `agents: [...]` property to coordinator agents (Ticketer, CTO) to explicitly restrict which subagents they can invoke.
- Verify and set `user-invocable: false` on all worker agents that should not be directly user-invocable.
- Downgrade review-chain agents (CIReviewer, QA, Validator, Documentation) from the most expensive model to a model array using `claude-3-7-sonnet` / `claude-3-5-sonnet` fallback.

**Items covered:** #4 (tool-sets not wired), #5 (coordinator agents missing agents property), #6 (worker agents missing user-invocable), #7 (all agents use expensive model)

---

## L1.4 — MCP Server Feature Enhancements

**Owner Domain:** backend  
**Priority:** P2 (High — requires L1.2 transport to be functional first)

Extend the MCP ticket server with MCP Resources and Prompts capabilities:
- **Resources:** Expose `ticket://READY`, `ticket://{ticket-id}`, and `ticket://DONE` as structured MCP Resources so agents and tools can read ticket state without calling a tool.
- **Prompts:** Expose `process-ticket` and `ticket-status` canned prompt templates so Ticketer can generate delegation prompts programmatically via the MCP Prompts API.

**Items covered:** #8 (MCP Resources), #9 (MCP Prompts)

---

## L1.5 — Extension Platform

**Owner Domain:** backend (TypeScript/VS Code extension)  
**Priority:** P3 (Medium — enhances observability and developer experience)

Upgrade the VS Code extension from basic scaffold to a full platform component:
- Register the MCP ticket server as an **MCP App** via `vscode.lm.registerMcpServerDefinitionProvider` so the server is available workspace-wide without manual `.vscode/mcp.json` editing.
- Add a `@vibecoding` **chat participant** with `/status`, `/sync`, and `/next` slash commands for interactive ticket management from the chat panel.
- Add a **TreeView provider** under `contributes.views` showing tickets grouped by stage (READY / IN-PROGRESS / DONE) for visual ticket state feedback.

**Items covered:** #10 (MCP App), #11 (chat participant), #12 (TreeView)

---

## Dependency Graph (L1)

```
L1.1 Infrastructure Integrity ──┐
L1.2 MCP Server Core Transport ─┤─▶ L1.3 Agent Governance Config
                                │        (can proceed independently)
                                └──▶ L1.4 MCP Server Enhancements
                                         └──▶ L1.5 Extension Platform
```

All L1.3–L1.5 capabilities are unblocked once L1.1 and L1.2 are complete, but L1.3 has no hard technical dependency on L1.1 or L1.2 — it is sequenced by priority to ensure infrastructure is stable first.
