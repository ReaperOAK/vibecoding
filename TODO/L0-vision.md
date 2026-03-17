# L0: Vision — Vibecoding System Upgrade

## Strategic Vision

Upgrade the multi-agent vibecoding system from **instruction-dependent enforcement** to **deterministic enforcement** by adopting VS Code's native agent infrastructure: hooks, handoffs, agent-scoped tools, skills, subagent orchestration, and MCP tool scoping.

## Current State

- 15 agent definitions relying on prose-based rules ("PROHIBITED", "REQUIRED")
- No hooks infrastructure — zero deterministic enforcement
- No handoffs — manual workflow chaining via `continue.prompt.md`
- No `agents` field — no subagent scoping on any agent
- No skills — using custom `.github/vibecoding/chunks/` instead of standard format
- No agent-scoped hooks — policy violations depend on LLM compliance
- Prompt files missing `agent` and `tools` fields
- Instruction files all use `applyTo: '**'` — no conditional scoping
- References in agent files are plain text, not Markdown links

## Target State

- Deterministic policy enforcement via hooks (guardian stop, git safety, scope enforcement, memory gate)
- Native handoffs replacing manual prompt file chaining
- `agents` field restricting CTO→{Research,PM,Architect,TODO} and Ticketer→{workers}
- Agent-scoped hooks for per-role validation
- Standard `.github/skills/` replacing vibecoding chunks
- Prompt files routing to correct agents via `agent` field
- Pattern-scoped instructions reducing context bloat
- MCP tool scoping via `tools` field enforcement
