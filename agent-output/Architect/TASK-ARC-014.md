# TASK-ARC-014 — Tighten Ticketer Tool Loadout

## Summary
Tightened Ticketer agent tools from 16-item full toolset to minimal dispatcher set: `[agent, execute, read, 'github/*']`.

## Artifacts
- `.github/agents/Ticketer.agent.md` — tools array reduced

## Decisions
- Kept `agent` (dispatch subagents), `execute` (run tickets.py), `read` (read ticket state), `github/*` (git operations)
- Removed: vscode, edit, search, web, browser, figma, forgeos, tavily, upstash, markitdown, playwright, mermaid, todo

## Confidence: HIGH
