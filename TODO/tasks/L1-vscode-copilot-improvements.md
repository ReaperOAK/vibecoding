# L1 Decomposition: VS Code + GitHub Copilot System Improvements (March 2026)

**Project:** vibecoding multi-agent system — 10 targeted improvements  
**Decomposition Level:** L1 (Vision → Capabilities/Epics)  
**Date:** 2026-03-26  
**Author:** TODO Agent  

---

## Context

10 improvement areas were identified from researching the latest VS Code + GitHub Copilot documentation (March 2026). These improvements harden the vibecoding multi-agent system against context pollution, missing enforcement, incomplete handoffs, and cross-tool incompatibility.

---

## L1 Epics

### L1-01: Agent Tool Governance
**Purpose:** Eliminate context pollution and decision paralysis caused by identical 240+ tool kitchen-sink lists across all agent `.agent.md` files. Each agent should have exactly the tools its role authorizes — no more, no less.

**Scope:** `.github/agents/*.agent.md` tool frontmatter, tool set abstractions  
**Priority:** P0 — Critical path, affects all agents  
**Improvement Areas Addressed:** #1 (Fix tools kitchen-sink lists), #2 (Add agents property to CTO/Ticketer)

---

### L1-02: Lifecycle Hook Infrastructure
**Purpose:** Replace LLM-instruction-based policy enforcement with deterministic shell-script hooks fired by VS Code agent lifecycle events. Guardian stop, git policy gating, and auto-sync become code-level guarantees instead of behavioral suggestions.

**Scope:** `.github/hooks/`, `.vscode/settings.json`, hook scripts  
**Priority:** P1  
**Improvement Areas Addressed:** #3 (Create `.github/hooks/` enforcement hooks)

---

### L1-03: Agent Visibility & Scoping
**Purpose:** Prevent non-user-facing agents (dispatched only by Ticketer/CTO) from appearing in user-visible agent pickers. Reduces confusion and prevents inappropriate direct invocation of worker agents.

**Scope:** `user-invocable:` frontmatter across 12 dispatch-only agents  
**Priority:** P1  
**Improvement Areas Addressed:** #4 (Mark non-user-facing agents as `user-invocable: false`)

---

### L1-04: SDLC Handoff Chain Completeness
**Purpose:** Ensure every agent declares `handoffs:` frontmatter so VS Code can automatically chain workflow stages without human re-selection. Complete the post-implementation chain (Backend→QA→Security→CI→Docs→Validator) and rework loops.

**Scope:** `.github/agents/*.agent.md` handoffs frontmatter, dispatcher routing  
**Priority:** P1  
**Improvement Areas Addressed:** #5 (Complete full SDLC handoff chains)

---

### L1-05: Skills & Instructions Standards
**Purpose:** Bring `.github/skills/` SKILL.md files into full conformance with the agentskills.io open standard, enabling interoperability with external agent systems and consistent discovery behavior.

**Scope:** `.github/skills/*/SKILL.md` frontmatter properties  
**Priority:** P2  
**Improvement Areas Addressed:** #6 (Upgrade skills to agentskills.io standard)

---

### L1-06: Cross-Tool Compatibility
**Purpose:** Make the vibecoding system work with Claude-based workflows (CLAUDE.md / `.claude/agents/`), and enhance prompt files with full execution frontmatter (`agent:`, `model:`, `tools:`). Decouples the system from VS Code Copilot exclusivity.

**Scope:** `CLAUDE.md`, `.github/prompts/*.prompt.md` frontmatter  
**Priority:** P2  
**Improvement Areas Addressed:** #7 (CLAUDE.md compatibility), #8 (Enhance prompt files)

---

### L1-07: Developer Experience
**Purpose:** Scaffold the VS Code agent plugin extension that packages the entire vibecoding system (agents, skills, hooks, MCP servers) as an installable .vsix bundle. Enables one-click setup.

**Scope:** `vibecoding-copilot-plugin/` VS Code extension directory  
**Priority:** P3  
**Improvement Areas Addressed:** #9 (Scaffold VS Code agent plugin)

---

### L1-08: Platform Distribution
**Purpose:** Document and implement organization-level sharing of the agent system via GitHub org policy files and `github.copilot.chat.codeGeneration.instructions`. Enables team/enterprise distribution.

**Scope:** Deployment guide, org-level policy documentation  
**Priority:** P3  
**Improvement Areas Addressed:** #10 (Organization-level sharing)
