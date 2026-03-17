# TASK-SYS-008: Add subagent scoping to CTO agent

**Type:** architecture
**Priority:** critical
**Files:** .github/agents/CTO.agent.md
**Tags:** agents, orchestration, P0

## Description
Add `agents` field to CTO agent frontmatter to scope which subagents CTO can invoke: Research, ProductManager, Architect, TODO only. Add `disable-model-invocation: true` to prevent CTO from being invoked as a subagent by other agents (it's a top-level orchestrator only).

## Acceptance Criteria
- [ ] Given CTO.agent.md is updated, when the `agents` field is present, then it contains exactly `['Research', 'ProductManager', 'Architect', 'TODO']`
- [ ] Given CTO.agent.md has `disable-model-invocation: true`, when any other agent tries to invoke CTO as subagent, then VS Code blocks it
- [ ] Given CTO is invoked, when it attempts to call Backend or Frontend as subagent, then VS Code prevents the invocation

---

# TASK-SYS-009: Add subagent scoping to Ticketer agent

**Type:** architecture
**Priority:** critical
**Files:** .github/agents/Ticketer.agent.md
**Tags:** agents, orchestration, P0

## Description
Add `agents` field to Ticketer agent frontmatter to scope which subagents Ticketer can invoke: all implementing and review agents (Backend, Frontend, DevOps, UIDesigner, QA, Security, CIReviewer, Documentation, Validator, TODO). Ticketer must NOT be able to invoke CTO, Research, PM, or Architect.

## Acceptance Criteria
- [ ] Given Ticketer.agent.md is updated, when the `agents` field is present, then it lists `['Backend', 'Frontend', 'DevOps', 'UIDesigner', 'QA', 'Security', 'CIReviewer', 'Documentation', 'Validator', 'TODO']`
- [ ] Given Ticketer is invoked, when it attempts to call CTO or Research as subagent, then VS Code blocks the invocation
- [ ] Given the agents field is enforced, when Ticketer dispatches a Backend agent, then it succeeds

---

# TASK-SYS-010: Add CTO to Ticketer handoff

**Type:** architecture
**Priority:** critical
**Dependencies:** TASK-SYS-008
**Files:** .github/agents/CTO.agent.md
**Tags:** handoffs, orchestration, P0

## Description
Add `handoffs` field to CTO agent frontmatter with a handoff that transitions to Ticketer after ticket decomposition is complete. This replaces the manual instruction "Run continue.prompt.md to begin Ticketer execution" with a native VS Code handoff button.

## Acceptance Criteria
- [ ] Given CTO.agent.md includes a `handoffs` field, when CTO completes ticket decomposition, then an "Execute Ticket Backlog" handoff button appears
- [ ] Given the handoff is defined, when clicked, then it invokes the Ticketer agent with prompt "Scan READY tickets and begin dispatching workers"
- [ ] Given `send: true`, when the button appears, then clicking it auto-submits without requiring user editing

---

# TASK-SYS-011: Add SDLC stage handoffs to implementing agents

**Type:** architecture
**Priority:** high
**Dependencies:** TASK-SYS-009
**Files:** .github/agents/Backend.agent.md, .github/agents/Frontend.agent.md, .github/agents/DevOps.agent.md, .github/agents/Architect.agent.md, .github/agents/Research.agent.md
**Tags:** handoffs, sdlc, P1

## Description
Add `handoffs` field to all implementing agents for SDLC stage transitions. Each agent gets a handoff to the next stage in the pipeline (Backend→QA, QA→Security, Security→CI, CI→Docs, Docs→Validation). This creates a native workflow chain.

## Acceptance Criteria
- [ ] Given Backend.agent.md includes `handoffs`, when Backend completes, then a "Run QA" handoff button appears pointing to QA agent
- [ ] Given each agent has handoffs, then the full chain is: implementing→QA→Security→CI→Docs→Validation
- [ ] Given handoff prompts include ticket ID context, when clicked, then the next agent receives the ticket ID

---

# TASK-SYS-012: Add rework handoffs to review agents

**Type:** architecture
**Priority:** high
**Dependencies:** TASK-SYS-011
**Files:** .github/agents/QA.agent.md, .github/agents/Security.agent.md, .github/agents/Validator.agent.md, .github/agents/CIReviewer.agent.md
**Tags:** handoffs, rework, P1

## Description
Add rework handoffs to all review agents. When a review agent rejects a ticket, a "Rework" handoff button appears that routes back to the original implementing agent with rejection evidence.

## Acceptance Criteria
- [ ] Given QA.agent.md includes rework handoffs, when QA rejects a ticket, then a "Rework: Return to Implementation" handoff button appears
- [ ] Given the rework handoff is defined, when clicked, then it routes back to the implementing agent with rejection evidence in the prompt
- [ ] Given all review agents have rework handoffs, then rejection-initiated rework is a one-click operation
