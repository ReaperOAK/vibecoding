# TASK-ARC-013: Audit and tighten CTO tool loadout

**Type:** architecture
**Priority:** high
**Files:** .github/agents/CTO.agent.md
**Tags:** tools, audit, P1

## Description
Audit the CTO agent tool array and remove tools not needed for its discovery/research/delegation role. CTO does not implement code, so should not have code-modification tools beyond what's needed for reading. Replace individual tool listings with tool set references where possible.

## Acceptance Criteria
- [ ] Given CTO.agent.md tools array is reviewed, when compared to role needs, then only discovery/research/delegation tools remain
- [ ] Given CTO does not implement code, when tools are audited, then unnecessary code-modification tools are removed
- [ ] Given tool sets are available, when applicable, then individual tool listings are replaced with tool set references

---

# TASK-ARC-014: Audit and tighten Ticketer tool loadout

**Type:** architecture
**Priority:** high
**Files:** .github/agents/Ticketer.agent.md
**Tags:** tools, audit, P1

## Description
Audit the Ticketer agent tool array and reduce to minimum necessary for its stateless dispatcher role. Ticketer needs only: agent (subagent dispatch), execute (ticket commands), github (git operations), memory (state), sequentialthinking (planning). Remove all code reading/editing tools.

## Acceptance Criteria
- [ ] Given Ticketer is a dumb dispatcher, when its tools are audited, then it has ONLY dispatch-essential tools
- [ ] Given Ticketer must never read code, when tools are reviewed, then code reading/search/edit tools are absent
- [ ] Given the tool list is minimal, when Ticketer runs, then decision paralysis from 240+ tools is eliminated

---

# TASK-ARC-015: Audit and tighten implementing agent tool loadouts

**Type:** architecture
**Priority:** high
**Files:** .github/agents/Backend.agent.md, .github/agents/Frontend.agent.md, .github/agents/DevOps.agent.md, .github/agents/UIDesigner.agent.md
**Tags:** tools, audit, P1

## Description
Audit all implementing agent tool arrays and ensure each has only role-specific tools plus universal tools. Backend should not have Figma tools, Frontend should not have DB tools, etc. Each agent should have less than 30 tools total.

## Acceptance Criteria
- [ ] Given each implementing agent has a defined role, when tools are audited, then they contain only role-specific plus universal tools
- [ ] Given Backend needs DB tools but not Figma, when Backend tools are listed, then Figma MCP tools are absent
- [ ] Given Frontend needs UI tools but not DB, when Frontend tools are listed, then MongoDB tools are absent
- [ ] Given all agents are reviewed, then each implementing agent has fewer than 30 tools

---

# TASK-ARC-016: Audit and tighten review agent tool loadouts

**Type:** architecture
**Priority:** high
**Files:** .github/agents/QA.agent.md, .github/agents/Security.agent.md, .github/agents/CIReviewer.agent.md, .github/agents/Validator.agent.md
**Tags:** tools, audit, P1

## Description
Audit all review agent tool arrays and ensure each has only role-specific tools. QA needs testing tools, Security needs security scanning, CIReviewer needs only universal tools, Validator needs verification tools.

## Acceptance Criteria
- [ ] Given QA needs testing tools, when audited, then it has playwright/browser tools but not MongoDB or Terraform
- [ ] Given Security needs security scanning, when audited, then it has Sentry but not Stitch
- [ ] Given CIReviewer only needs universal tools, when audited, then no role-specific tools are present
- [ ] Given all review agents are reviewed, then each has a minimal, role-appropriate tool set

---

# TASK-ARC-017: Convert all agent reference sections to Markdown links

**Type:** architecture
**Priority:** high
**Files:** .github/agents/CTO.agent.md, .github/agents/Ticketer.agent.md, .github/agents/Backend.agent.md, .github/agents/Frontend.agent.md, .github/agents/QA.agent.md, .github/agents/Security.agent.md, .github/agents/Architect.agent.md, .github/agents/Research.agent.md, .github/agents/ProductManager.agent.md, .github/agents/Documentation.agent.md, .github/agents/DevOps.agent.md, .github/agents/UIDesigner.agent.md, .github/agents/CIReviewer.agent.md, .github/agents/Validator.agent.md, .github/agents/TODO.agent.md
**Tags:** agents, references, P1

## Description
Convert all agent "References" sections from plain text paths to proper Markdown links. When chat.includeReferencedInstructions is enabled, VS Code auto-includes linked instruction content, eliminating the need for agents to manually read referenced files during boot sequence.

## Acceptance Criteria
- [ ] Given each agent has a References section, when converted, then each reference is a proper Markdown link
- [ ] Given chat.includeReferencedInstructions is enabled, when an agent is invoked, then referenced instruction content is automatically included
- [ ] Given all 15 agents are updated, when any agent is invoked, then its referenced instructions are auto-loaded without boot sequence reads

---

# TASK-SYS-018: Add agent-scoped PostToolUse lint hook to implementing agents

**Type:** infra
**Priority:** high
**Dependencies:** TASK-SYS-007
**Files:** .github/agents/Backend.agent.md, .github/agents/Frontend.agent.md, .github/hooks/scripts/lint-changed-files.sh
**Tags:** hooks, linting, P1

## Description
Add agent-scoped hooks.PostToolUse entries to Backend and Frontend agent frontmatter that auto-run linting on modified files after every edit. This ensures code quality without relying on the agent to remember to lint.

## Acceptance Criteria
- [ ] Given Backend.agent.md includes a hooks.PostToolUse entry, when a file is edited, then the lint script runs on the modified file
- [ ] Given linting fails, when the hook returns, then lint errors are included as additional context
- [ ] Given chat.useCustomAgentHooks is true, when the hook is defined in frontmatter, then it activates only for that agent

---

# TASK-SYS-019: Add agent-scoped PreToolUse hook to Ticketer to block code modifications

**Type:** infra
**Priority:** high
**Dependencies:** TASK-SYS-007
**Files:** .github/agents/Ticketer.agent.md, .github/hooks/scripts/ticketer-scope-guard.sh
**Tags:** hooks, scope-enforcement, P1

## Description
Add an agent-scoped PreToolUse hook to Ticketer that blocks any attempt to edit code files. Only ticket JSON files in tickets/ and ticket-state/ are allowed.

## Acceptance Criteria
- [ ] Given Ticketer has a PreToolUse hook, when it attempts to edit a code file, then the hook denies with reason "Ticketer is a dispatcher, not an implementer"
- [ ] Given the file being edited is a .json in tickets/ or ticket-state/, then the hook allows
- [ ] Given the hook is agent-scoped, when other agents run, then this hook does NOT fire
