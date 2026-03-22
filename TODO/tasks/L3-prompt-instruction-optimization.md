# TASK-SYS-020: Add agent field to all prompt files

**Type:** architecture
**Priority:** high
**Files:** .github/prompts/start.prompt.md, .github/prompts/continue.prompt.md, .github/prompts/stop.prompt.md, .github/prompts/takeover.prompt.md, .github/prompts/figma-to-code.prompt.md, .github/prompts/expensify.prompt.md
**Tags:** prompts, routing, P1

## Description
Add `agent` field to all 6 prompt file frontmatters so that invoking a prompt automatically selects the correct agent. `/start` routes to CTO, `/continue` routes to Ticketer, `/stop` routes to Ticketer, etc. Eliminates manual agent switching.

## Acceptance Criteria
- [ ] Given start.prompt.md has `agent: 'CTO'` in frontmatter, when /start is invoked, then the CTO agent is automatically selected
- [ ] Given continue.prompt.md has `agent: 'Ticketer'`, when /continue is invoked, then the Ticketer agent is automatically selected
- [ ] Given stop.prompt.md has `agent: 'Ticketer'`, when /stop is invoked, then the correct agent handles the stop
- [ ] Given each prompt file routes to the correct agent, then no manual agent switching is needed

---

# TASK-SYS-021: Add tools field to prompt files

**Type:** architecture
**Priority:** medium
**Dependencies:** TASK-SYS-020
**Files:** .github/prompts/start.prompt.md, .github/prompts/continue.prompt.md, .github/prompts/figma-to-code.prompt.md
**Tags:** prompts, tools, P2

## Description
Add `tools` field to prompt files to scope tool availability per workflow. The start prompt prioritizes research/planning tools, the figma-to-code prompt prioritizes Figma MCP tools, etc.

## Acceptance Criteria
- [ ] Given start.prompt.md specifies tools, when CTO runs via /start, then only CTO-appropriate tools are available
- [ ] Given figma-to-code.prompt.md specifies tools, when invoked, then Figma MCP tools are prioritized
- [ ] Given prompt file tools take precedence over agent defaults, when both are present, then the prompt file tools win

---

# TASK-SYS-022: Create pattern-scoped instruction for Python files

**Type:** architecture
**Priority:** medium
**Files:** .github/instructions/python.instructions.md
**Tags:** instructions, scoping, P2

## Description
Create a new instruction file scoped to `applyTo: '**/*.py'` with Python-specific conventions for the ticket system code (tickets.py). Only loaded when agents work on Python files, reducing context bloat for non-Python work.

## Acceptance Criteria
- [ ] Given a new instruction file with applyTo `**/*.py`, when an agent works on tickets.py, then Python-specific rules are loaded
- [ ] Given the file is scoped to .py, when an agent works on .md or .ts files, then this instruction is NOT loaded
- [ ] Given Python rules exist, then they include conventions for the ticket system Python code

---

# TASK-SYS-023: Create pattern-scoped instruction for agent definition files

**Type:** architecture
**Priority:** medium
**Files:** .github/instructions/agent-definitions.instructions.md
**Tags:** instructions, scoping, P2

## Description
Create a new instruction file scoped to `applyTo: '.github/agents/**'` with meta-rules for writing agent definition files (required frontmatter fields, tool loadout structure, reference link format). Only loaded when agents modify agent definitions.

## Acceptance Criteria
- [ ] Given a new instruction file with applyTo `.github/agents/**`, when an agent modifies agent definitions, then meta-rules are loaded
- [ ] Given the instruction includes frontmatter schema documentation, when agents write new agents, then they follow the correct structure
- [ ] Given the scoping is correct, when agents work on non-agent files, then this instruction is NOT loaded

---

# TASK-SYS-024: Review and optimize git-protocol instruction scoping

**Type:** research
**Priority:** medium
**Files:** .github/instructions/git-protocol.instructions.md
**Tags:** instructions, scoping, P2

## Description
Review git-protocol.instructions.md and determine if any portion can be split into a scoped sub-instruction. Currently uses `applyTo: '**'` which loads for every file context. Evaluate whether the commit format and lease mechanism sections could be scoped to `.github/**` while keeping the core git safety rules universal.

## Acceptance Criteria
- [ ] Given git-protocol.instructions.md is reviewed, when evaluated, then a decision is documented on whether to keep universal or split
- [ ] Given splitting is chosen, when implemented, then core git safety rules remain universal and protocol-specific rules are scoped
- [ ] Given the instruction is reviewed, when complete, then a brief ADR documents the rationale
