# L2 — GitHub Folder Optimization: Execution Blocks

**Date:** 2026-04-09
**Source:** L1-github-optimization.md

---

## From L1.1 — Context Window Optimization

### BLOCK 1.1 — Remove `applyTo: '**'` from Instruction Files (P0)

Update the YAML frontmatter of 5 instruction files (core, sdlc, ticket-system, git-protocol, agent-behavior) to remove `applyTo: '**'` and add keyword-rich `description` fields. This switches them from always-loaded to on-demand discovery by VS Code.

- **Deliverable:** 5 instruction files with `applyTo` removed and `description` added with relevant keywords
- **Files:** `.github/instructions/core.instructions.md`, `.github/instructions/sdlc.instructions.md`, `.github/instructions/ticket-system.instructions.md`, `.github/instructions/git-protocol.instructions.md`, `.github/instructions/agent-behavior.instructions.md`
- **Effort:** S
- **L3 tickets:** TASK-GHO-SYS001

### BLOCK 1.2 — Consolidate Workspace Instructions (P0)

Trim `copilot-instructions.md` to <50 lines as the single lean workspace instruction file. Move orchestration rules from `AGENTS.md` into a new on-demand instruction file `agent-orchestration.instructions.md`. Update `AGENTS.md` to be a minimal pointer to the instruction file.

- **Deliverable:** `copilot-instructions.md` ≤50 lines; new `agent-orchestration.instructions.md` with moved rules; `AGENTS.md` trimmed to pointer-only
- **Files:** `.github/copilot-instructions.md`, `AGENTS.md`, `.github/instructions/agent-orchestration.instructions.md`
- **Effort:** M
- **L3 tickets:** TASK-GHO-SYS002
- **Dependencies:** TASK-GHO-SYS001 (instruction files must use description-based discovery before moving rules into them)

---

## From L1.2 — Catalog & Reference Hygiene

### BLOCK 2.1 — Clean Ghost References from Catalog (P1)

Remove all entries in `.github/vibecoding/catalog.yml` that reference non-existent files: `_cross-cutting-protocols.md`, `VALIDATION-REPORT.md`, `ARCHITECTURE.instructions.md`, `core_governance.instructions.md`, and the entire `governance` key.

- **Deliverable:** `catalog.yml` contains only references to files that actually exist on disk
- **Files:** `.github/vibecoding/catalog.yml`
- **Effort:** XS
- **L3 tickets:** TASK-GHO-SYS003

### BLOCK 2.2 — Delete Duplicate Catalog (P1)

Remove `.github/skills/catalog.yml` since it is byte-identical to `.github/vibecoding/catalog.yml`. The boot sequence references only `.github/vibecoding/catalog.yml`.

- **Deliverable:** `.github/skills/catalog.yml` deleted; no remaining references to it
- **Files:** `.github/skills/catalog.yml` (delete)
- **Effort:** XS
- **L3 tickets:** TASK-GHO-SYS004
- **Dependencies:** TASK-GHO-SYS003 (clean the canonical copy first, then delete the duplicate)

---

## From L1.3 — Agent File Optimization

### BLOCK 3.1 — Extract Shared Agent Rules (P1)

Create a new `.github/instructions/agent-shared.instructions.md` file containing the duplicated cross-cutting content: boot sequence, forbidden actions, execution SOP, tool loadout reference table. Use `applyTo: '.github/agents/**'` so it loads only when agent files are in context.

- **Deliverable:** New shared instruction file with extracted cross-cutting rules; ≤120 lines
- **Files:** `.github/instructions/agent-shared.instructions.md`
- **Effort:** M
- **L3 tickets:** TASK-GHO-SYS005
- **Dependencies:** TASK-GHO-SYS002 (workspace instructions consolidated first so we know what shared rules to extract)

### BLOCK 3.2 — Trim Agent Files (P1)

Update all 15 agent `.agent.md` files to remove duplicated boot sequence, forbidden actions, execution SOP, and tool loadout table. Replace with a reference to `agent-shared.instructions.md`. Target ≤80 lines body per agent.

- **Deliverable:** All 15 agent files ≤80 lines body; cross-cutting rules replaced with reference to shared file
- **Files:** All 15 `.github/agents/*.agent.md`
- **Effort:** L
- **L3 tickets:** TASK-GHO-SYS006
- **Dependencies:** TASK-GHO-SYS005 (shared instruction file must exist before removing rules from agents)

---

## From L1.4 — Tool Configuration Cleanup

### BLOCK 4.1 — Remove tool-sets Directory (P2)

Delete `.github/tool-sets/` directory and its 3 files (`universal.jsonc`, `code-editing.jsonc`, `research.jsonc`). These use a custom `#shorthand` pattern that agents cannot resolve. Tool groupings are already documented in agent files.

- **Deliverable:** `.github/tool-sets/` deleted; no remaining `#universal`/`#research`/`#code-editing` references in codebase
- **Files:** `.github/tool-sets/` (delete directory)
- **Effort:** XS
- **L3 tickets:** TASK-GHO-SYS007

### BLOCK 4.2 — Resolve tool-acl.yaml (P2)

Move enforceable rules from `.github/sandbox/tool-acl.yaml` into agent file `tools:` frontmatter sections (where supported) or convert to a reference document. Remove the `sandbox/` directory if empty after.

- **Deliverable:** Tool ACL rules merged into agent files or documented as reference; `sandbox/` cleaned
- **Files:** `.github/sandbox/tool-acl.yaml`, `.github/agents/*.agent.md`
- **Effort:** S
- **L3 tickets:** TASK-GHO-SYS008

### BLOCK 4.3 — Fix Hook toolNames (P2)

Verify and update `toolNames` arrays in `.github/hooks/policy-enforcement.json` to match actual VS Code tool names. Currently has `execute/runInTerminal` which should be `run_in_terminal`.

- **Deliverable:** All `toolNames` entries match actual VS Code tool IDs; hooks fire correctly
- **Files:** `.github/hooks/policy-enforcement.json`
- **Effort:** XS
- **L3 tickets:** TASK-GHO-SYS009

---

## From L1.5 — Skills & Directory Cleanup

### BLOCK 5.1 — Audit and Consolidate Skills (P2)

Evaluate all 20 skill directories. For skills with <40 lines and no actionable procedures, convert to `.instructions.md` files. For skills with real workflows, keep as-is.

- **Deliverable:** Shallow skills converted to instruction files or fleshed out; skill directory count reduced
- **Files:** `.github/skills/*/SKILL.md`, `.github/instructions/*.instructions.md`
- **Effort:** L
- **L3 tickets:** TASK-GHO-DOC001

### BLOCK 5.2 — Remove Unused Directories (P3)

Delete empty/stub infrastructure directories: `.github/observability/` (contains only `agent-trace-schema.json`), `.github/tasks/` (contains templates only), `.github/proposals/` (contains only `.gitkeep`).

- **Deliverable:** Empty/stub directories removed; any valuable content relocated
- **Files:** `.github/observability/`, `.github/tasks/`, `.github/proposals/` (delete)
- **Effort:** XS
- **L3 tickets:** TASK-GHO-SYS010

---

## Dependency Graph

```
TASK-GHO-SYS001 (applyTo removal)
    └── TASK-GHO-SYS002 (consolidate workspace instructions)
         └── TASK-GHO-SYS005 (extract shared agent rules)
              └── TASK-GHO-SYS006 (trim agent files)

TASK-GHO-SYS003 (clean ghost refs)
    └── TASK-GHO-SYS004 (delete duplicate catalog)

TASK-GHO-SYS007 (remove tool-sets)     — independent
TASK-GHO-SYS008 (resolve tool-acl)     — independent
TASK-GHO-SYS009 (fix hook toolNames)   — independent
TASK-GHO-DOC001 (audit skills)         — independent
TASK-GHO-SYS010 (remove unused dirs)   — independent
```
