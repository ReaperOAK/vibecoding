# TASK-SYS-025: Create skills directory and migrate first chunk

**Type:** infra
**Priority:** medium
**Files:** .github/skills/boot-sequence/SKILL.md
**Tags:** skills, migration, P2

## Description
Create the `.github/skills/` directory structure and migrate the first vibecoding chunk (boot-sequence) to the standard skills format. Each skill gets a `SKILL.md` file with proper frontmatter (name, description, user-invocable). This establishes the pattern for migrating all chunks.

## Acceptance Criteria
- [ ] Given .github/skills/ directory is created, when VS Code scans for skills, then the directory is recognized
- [ ] Given the boot-sequence skill is created, when any agent is invoked, then the boot sequence can be loaded as a skill
- [ ] Given the SKILL.md frontmatter is valid, when examined, then it includes name, description, and optionally user-invocable

---

# TASK-SYS-026: Migrate remaining vibecoding chunks to skills format

**Type:** infra
**Priority:** medium
**Dependencies:** TASK-SYS-025
**Files:** .github/skills/, .github/vibecoding/chunks/
**Tags:** skills, migration, P2

## Description
Convert all remaining vibecoding chunk directories to standard `.github/skills/` format with SKILL.md files. Makes chunks discoverable and portable across VS Code, CLI, and GitHub coding agent.

## Acceptance Criteria
- [ ] Given all chunk directories are enumerated, when migrated, then each has a corresponding .github/skills/<name>/SKILL.md
- [ ] Given skills use the standard format, when VS Code loads them, then they appear in the skills listing
- [ ] Given the old chunks still exist, when migration is verified, then the old chunks can be deprecated

---

# TASK-SYS-027: Design MCP ticket server architecture

**Type:** research
**Priority:** medium
**Files:** docs/adr/mcp-ticket-server.md
**Tags:** mcp, architecture, P2

## Description
Research and design an MCP server that wraps tickets.py functionality. Document the architecture decision including transport choice (stdio vs HTTP), implementation language, tool definitions (createTicket, claimTicket, advanceStage, getStatus, syncTickets), and sandboxing configuration.

## Acceptance Criteria
- [ ] Given the research is complete, when the ADR is written, then it documents trade-offs of MCP server vs CLI for ticket management
- [ ] Given the architecture is defined, when reviewed, then it specifies all ticket management tools with typed schemas
- [ ] Given the decision is made, when documented, then it includes transport choice, implementation language, and sandboxing config

---

# TASK-SYS-028: Implement MCP ticket server

**Type:** infra
**Priority:** low
**Dependencies:** TASK-SYS-027
**Files:** .github/mcp-servers/ticket-server/, .vscode/mcp.json
**Tags:** mcp, infrastructure, P3

## Description
Implement the MCP ticket server designed in TASK-SYS-027. Wraps tickets.py as typed MCP tools with sandboxing. Configure in .vscode/mcp.json for VS Code auto-discovery.

## Acceptance Criteria
- [ ] Given the MCP server is implemented, when started, then it exposes all ticket management tools via MCP protocol
- [ ] Given the server is configured in .vscode/mcp.json, when VS Code starts, then agents can invoke ticket tools directly
- [ ] Given the server wraps tickets.py, when tools are called, then they produce identical results to CLI invocation
- [ ] Given sandboxing is enabled, when the server runs, then it can only access tickets/ and ticket-state/

---

# TASK-SYS-029: Create tool sets for common tool groupings

**Type:** architecture
**Priority:** medium
**Files:** .github/tool-sets/universal.jsonc, .github/tool-sets/code-editing.jsonc, .github/tool-sets/research.jsonc
**Tags:** tools, toolsets, P2

## Description
Create reusable tool set definitions that group commonly-used tools. A `#universal` set for tools every agent needs (memory, serena, execute, vscode, tavily, github, sequentialthinking), a `#code-editing` set for implementing agents, and a `#research` set for research/planning agents. Reduces duplication across agent files.

## Acceptance Criteria
- [ ] Given a universal.jsonc tool set is created, when agents reference #universal, then all universal tools are included
- [ ] Given a code-editing.jsonc tool set exists, when implementing agents reference it, then all code editing tools are included
- [ ] Given tool sets reduce duplication, when agent files are updated, then individual tool listings are replaced with tool set references
