# L3 — GitHub Folder Optimization: Tickets

**Date:** 2026-04-09
**Source L2:** L2-github-optimization.md
**Parse command:** `python3 tickets.py --parse TODO/tasks/`

---

# TASK-GHO-SYS001: Remove applyTo from instruction files

**Type:** infra
**Priority:** critical
**Files:** .github/instructions/core.instructions.md, .github/instructions/sdlc.instructions.md, .github/instructions/ticket-system.instructions.md, .github/instructions/git-protocol.instructions.md, .github/instructions/agent-behavior.instructions.md
**Tags:** p0, context-bloat, instructions, copilot-optimization

## Description

Update YAML frontmatter of 5 instruction files to remove `applyTo: '**'` and ensure keyword-rich `description` fields exist for on-demand discovery. This eliminates ~538 lines of always-loaded context from every Copilot interaction. Each file keeps its existing `name` and `description` fields but removes the `applyTo: '**'` line. Descriptions must include domain-specific keywords so VS Code loads them only when relevant (e.g., "halt gate, boot sequence, memory gate, security baseline" for core).

## Acceptance Criteria

- [ ] Given the 5 instruction files, when I inspect their YAML frontmatter, then none contain `applyTo: '**'`
- [ ] Given a simple user question like "what is 2+2", when Copilot processes it, then zero instruction files are auto-loaded into context
- [ ] Given a user question about "ticket dependencies", when Copilot processes it, then only ticket-system.instructions.md loads via description match

---

# TASK-GHO-SYS002: Consolidate workspace instruction files

**Type:** infra
**Priority:** critical
**Files:** .github/copilot-instructions.md, AGENTS.md, .github/instructions/agent-orchestration.instructions.md
**Tags:** p0, context-bloat, copilot-instructions, agents-md
**Dependencies:** TASK-GHO-SYS001

## Description

Consolidate `copilot-instructions.md` and `AGENTS.md` into a single lean workspace instruction pattern. (1) Trim `.github/copilot-instructions.md` to ≤50 lines containing only project identity, tech stack, and key conventions. (2) Create `.github/instructions/agent-orchestration.instructions.md` with description-based discovery containing the orchestration rules currently in AGENTS.md (boot sequence, tool loadout table, dispatcher contract, evidence rules). (3) Trim `AGENTS.md` to ≤30 lines as a human-readable pointer that references the instruction file for agent details.

## Acceptance Criteria

- [ ] Given `.github/copilot-instructions.md`, when I count its lines, then it has ≤50 lines
- [ ] Given `AGENTS.md`, when I count its lines, then it has ≤30 lines and references agent-orchestration.instructions.md
- [ ] Given `.github/instructions/agent-orchestration.instructions.md`, when I read it, then it contains the boot sequence, tool loadout table, dispatcher contract, and evidence rules previously in AGENTS.md
- [ ] Given the new instruction file, when I inspect its frontmatter, then it uses description-based discovery with no applyTo '**'

---

# TASK-GHO-SYS003: Clean ghost references from catalog

**Type:** infra
**Priority:** high
**Files:** .github/vibecoding/catalog.yml
**Tags:** p1, catalog, ghost-references, hygiene

## Description

Remove all entries from `.github/vibecoding/catalog.yml` that reference files which do not exist on disk. Ghost entries to remove: `.github/agents/_cross-cutting-protocols.md` (under `agent:` key), `.github/VALIDATION-REPORT.md` and `.github/instructions/ARCHITECTURE.instructions.md` (under `general:` key), `.github/instructions/core_governance.instructions.md` and all `.github/governance/*` entries (under `governance:` key). Verify each remaining entry exists on disk after cleanup.

## Acceptance Criteria

- [ ] Given `.github/vibecoding/catalog.yml`, when I check every listed file path, then all referenced files exist on disk
- [ ] Given the catalog, when I search for `_cross-cutting-protocols`, then zero results are found
- [ ] Given the catalog, when I search for `governance` key, then the entire key and its entries are removed
- [ ] Given the catalog, when I search for `VALIDATION-REPORT` or `ARCHITECTURE.instructions`, then zero results are found

---

# TASK-GHO-SYS004: Delete duplicate skills catalog

**Type:** infra
**Priority:** high
**Files:** .github/skills/catalog.yml
**Tags:** p1, catalog, duplicate, cleanup
**Dependencies:** TASK-GHO-SYS003

## Description

Delete `.github/skills/catalog.yml` which is byte-identical to `.github/vibecoding/catalog.yml`. The boot sequence references only `.github/vibecoding/catalog.yml`. Verify no other file references `.github/skills/catalog.yml` before deletion. If references exist, update them to point to `.github/vibecoding/catalog.yml`.

## Acceptance Criteria

- [ ] Given the `.github/skills/` directory, when I list its contents, then `catalog.yml` does not exist
- [ ] Given a grep for `skills/catalog.yml` across the entire repo, when I check results, then zero references remain
- [ ] Given the boot sequence, when agents load catalog, then `.github/vibecoding/catalog.yml` is the only catalog path used

---

# TASK-GHO-SYS005: Extract shared agent rules into instruction file

**Type:** infra
**Priority:** high
**Files:** .github/instructions/agent-shared.instructions.md
**Tags:** p1, agent-optimization, dry, shared-rules
**Dependencies:** TASK-GHO-SYS002

## Description

Create `.github/instructions/agent-shared.instructions.md` containing cross-cutting rules duplicated across all 15 agent files. Extract: (1) Boot Sequence (steps 1-6, identical in all agents), (2) Forbidden Actions (git add rules, force push, deploy restrictions — identical across agents), (3) Execution SOP (6-step plan-read-navigate-edit-validate-log procedure), (4) Tool Loadout reference table (universal tools table). Use `applyTo: '.github/agents/**'` so it loads only when working on agent definitions. Target ≤120 lines.

## Acceptance Criteria

- [ ] Given `.github/instructions/agent-shared.instructions.md`, when I read it, then it contains boot sequence, forbidden actions, execution SOP, and universal tool loadout
- [ ] Given the file frontmatter, when I inspect it, then `applyTo` targets `.github/agents/**` only
- [ ] Given the file line count, when I count lines, then it is ≤120 lines
- [ ] Given any agent file, when I look for boot sequence text, then it references agent-shared.instructions.md instead of duplicating the steps

---

# TASK-GHO-SYS006: Trim agent files to 80 lines

**Type:** infra
**Priority:** high
**Files:** .github/agents/Architect.agent.md, .github/agents/Backend.agent.md, .github/agents/CIReviewer.agent.md, .github/agents/CTO.agent.md, .github/agents/DevOps.agent.md, .github/agents/Documentation.agent.md, .github/agents/Frontend.agent.md, .github/agents/ProductManager.agent.md, .github/agents/QA.agent.md, .github/agents/Research.agent.md, .github/agents/Security.agent.md, .github/agents/TODO.agent.md, .github/agents/Ticketer.agent.md, .github/agents/UIDesigner.agent.md, .github/agents/Validator.agent.md
**Tags:** p1, agent-optimization, context-reduction, dry
**Dependencies:** TASK-GHO-SYS005

## Description

Update all 15 agent `.agent.md` files to remove duplicated cross-cutting sections (boot sequence, forbidden actions, execution SOP, universal tool loadout table) and replace with a single reference line to `agent-shared.instructions.md`. Each agent file should retain ONLY: (1) role description, (2) stage ownership, (3) scope (included/excluded), (4) role-specific tools, (5) role-specific rules, (6) evidence requirements unique to the role. Target ≤80 lines body per agent file. Current average is 204 lines; target reduction is ~60%.

## Acceptance Criteria

- [ ] Given any agent `.agent.md` file, when I count its body lines excluding frontmatter, then it is ≤80 lines
- [ ] Given any agent file, when I search for Boot Sequence sections, then none contain the full 6-step boot sequence
- [ ] Given any agent file, when I search for Forbidden Actions, then the section contains only role-specific prohibitions
- [ ] Given all 15 agent files combined, when I sum their line counts, then total is ≤1500 lines down from 3062

---

# TASK-GHO-SYS007: Remove tool-sets directory

**Type:** infra
**Priority:** medium
**Files:** .github/tool-sets/universal.jsonc, .github/tool-sets/code-editing.jsonc, .github/tool-sets/research.jsonc
**Tags:** p2, cleanup, tool-sets, dead-config

## Description

Delete `.github/tool-sets/` directory containing `universal.jsonc`, `code-editing.jsonc`, and `research.jsonc`. These files define custom tool groupings using `#shorthand` references that VS Code and Copilot cannot resolve — they are dead configuration. Before deletion, grep the codebase for any `#universal`, `#research`, or `#code-editing` references and remove them from any files that contain them.

## Acceptance Criteria

- [ ] Given the `.github/` directory, when I list its contents, then `tool-sets/` does not exist
- [ ] Given a grep for `#universal` or `tool-sets` across the repo, when I check results, then zero references remain
- [ ] Given agent files, when I inspect their frontmatter, then no `tool-sets:` property references `#universal`, `#research`, or `#code-editing`

---

# TASK-GHO-SYS008: Resolve tool-acl enforcement

**Type:** infra
**Priority:** medium
**Files:** .github/sandbox/tool-acl.yaml
**Tags:** p2, tool-acl, sandbox, enforcement

## Description

`.github/sandbox/tool-acl.yaml` defines per-agent tool ACLs but has no enforcement mechanism. Resolution: (1) Review the ACL rules and determine which are already enforced by agent file tool loadout sections. (2) For rules not covered, either add them to agent `tools:` frontmatter if VS Code supports it or convert the file to a reference document. (3) Delete the `sandbox/` directory after migration. Document the decision.

## Acceptance Criteria

- [ ] Given the `.github/sandbox/` directory, when I check its contents, then `tool-acl.yaml` is either migrated or converted to a reference doc
- [ ] Given the tool ACL rules, when I compare with agent file tool loadout sections, then all enforceable rules are documented in agent files
- [ ] Given the resolution, when I read the output, then a clear decision is documented about enforcement approach

---

# TASK-GHO-SYS009: Fix hook toolNames to match VS Code

**Type:** infra
**Priority:** medium
**Files:** .github/hooks/policy-enforcement.json
**Tags:** p2, hooks, toolNames, copilot-compatibility

## Description

Update `toolNames` arrays in `.github/hooks/policy-enforcement.json` to use actual VS Code tool IDs. Currently the block-git-add-all hook lists `["run_in_terminal", "execute/runInTerminal"]`. Verify `run_in_terminal` is the correct VS Code tool ID and remove any namespaced tool IDs that do not correspond to actual tools. Check all hooks in the file and verify every `toolNames` entry matches a real tool.

## Acceptance Criteria

- [ ] Given `.github/hooks/policy-enforcement.json`, when I inspect all `toolNames` arrays, then every entry matches an actual VS Code Copilot tool ID
- [ ] Given the block-git-add-all hook, when I trigger a git add . command, then the hook fires and blocks it
- [ ] Given all hooks, when I inspect the file, then no invalid or namespaced tool IDs remain unless they are verified valid

---

# TASK-GHO-DOC001: Audit and consolidate shallow skills

**Type:** docs
**Priority:** medium
**Files:** .github/skills/a11y/SKILL.md, .github/skills/agent-protocols/SKILL.md, .github/skills/ai-safety/SKILL.md, .github/skills/architecture/SKILL.md, .github/skills/boot-sequence/SKILL.md, .github/skills/ci-cd/SKILL.md, .github/skills/containerization/SKILL.md, .github/skills/cto-playbook/SKILL.md, .github/skills/design/SKILL.md, .github/skills/git-protocol/SKILL.md, .github/skills/implementation/SKILL.md, .github/skills/orchestration/SKILL.md, .github/skills/performance/SKILL.md, .github/skills/planning/SKILL.md, .github/skills/qa/SKILL.md, .github/skills/sdlc/SKILL.md, .github/skills/sdlc-lifecycle/SKILL.md, .github/skills/security/SKILL.md, .github/skills/testing/SKILL.md, .github/skills/ticket-system/SKILL.md, .github/vibecoding/catalog.yml
**Tags:** p2, skills, documentation, consolidation

## Description

Audit all 20 skill directories under `.github/skills/`. For each skill: (1) count lines in SKILL.md, (2) check for real procedures, scripts, templates, or checklists. Skills with less than 40 lines and no actionable procedures should be converted to `.instructions.md` files under `.github/instructions/` with proper description-based discovery frontmatter. Skills with real workflows over 40 lines with procedures should be kept. Update `.github/vibecoding/catalog.yml` to reflect any moves. Document the audit results.

## Acceptance Criteria

- [ ] Given the skills audit, when I review it, then each of the 20 skills has a documented disposition (keep or convert or merge)
- [ ] Given skills converted to instructions, when I check their new `.instructions.md` files, then they have proper description-based frontmatter
- [ ] Given the catalog, when I verify references, then all entries point to files that exist on disk
- [ ] Given remaining skill directories, when I count SKILL.md lines, then all are over 40 lines with actionable procedures

---

# TASK-GHO-SYS010: Remove unused infrastructure directories

**Type:** infra
**Priority:** low
**Files:** .github/observability/agent-trace-schema.json, .github/tasks/claim-schema.json, .github/tasks/definition-of-done-template.md, .github/tasks/delegation-packet-schema.json, .github/tasks/initialization-checklist-template.md, .github/tasks/merge-protocol.md, .github/proposals/.gitkeep
**Tags:** p3, cleanup, unused-directories, hygiene

## Description

Delete empty or stub-only infrastructure directories that serve no functional purpose: (1) `.github/observability/` contains only `agent-trace-schema.json` with no consumers, (2) `.github/tasks/` contains template files not connected to any workflow, (3) `.github/proposals/` contains only `.gitkeep`. Before deletion, verify no file in the repo references these directories. If `agent-trace-schema.json` has potential value, relocate to `.github/docs/schemas/` or document intent.

## Acceptance Criteria

- [ ] Given the `.github/` directory, when I list its contents, then `observability/`, `tasks/`, and `proposals/` do not exist
- [ ] Given a grep for `observability` or `tasks/claim-schema` across the repo, when I check results, then zero functional references remain
- [ ] Given any valuable content like schemas, when I check, then it has been relocated to an appropriate location before deletion
