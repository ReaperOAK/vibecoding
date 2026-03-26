# TASK-SYS-030 — ARCHITECT Complete

## Summary
Set `user-invocable: false` on 8 dispatch-only agents: Backend, Frontend, QA, Security, CIReviewer, Documentation, Validator, TODO.

## Artifacts Modified
- .github/agents/Backend.agent.md
- .github/agents/Frontend.agent.md
- .github/agents/QA.agent.md
- .github/agents/Security.agent.md
- .github/agents/CIReviewer.agent.md
- .github/agents/Documentation.agent.md
- .github/agents/Validator.agent.md
- .github/agents/TODO.agent.md

## Evidence
All 8 files now have `user-invocable: false` in frontmatter. CTO, Ticketer, Research, ProductManager, Architect, UIDesigner, DevOps remain `user-invocable: true`.

## Confidence: HIGH
