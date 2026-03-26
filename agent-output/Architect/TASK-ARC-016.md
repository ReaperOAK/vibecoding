# TASK-ARC-016 — Tighten Review Agent Tool Loadouts

## Summary
Tightened tool arrays for QA, Security, CIReviewer, and Validator agents to role-appropriate minimal sets.

## Artifacts
- `.github/agents/QA.agent.md` — tools: `[vscode, execute, read, search, browser, 'github/*', 'playwright/*']`
- `.github/agents/Security.agent.md` — tools: `[vscode, execute, read, search, browser, 'github/*']`
- `.github/agents/CIReviewer.agent.md` — tools: `[vscode, execute, read, search, 'github/*']`
- `.github/agents/Validator.agent.md` — tools: `[vscode, execute, read, search, browser, 'github/*', 'playwright/*']`

## Decisions
- QA/Validator get playwright/* for test execution and browser for inspection
- Security gets browser for scanning but not playwright
- CIReviewer gets minimal set (lint/type checks only)
- All get github/* for git operations and read/search for codebase analysis

## Confidence: HIGH
