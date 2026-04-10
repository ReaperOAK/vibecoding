# L1 — GitHub Folder Optimization: Capability Breakdown

**Date:** 2026-04-09
**L0 Vision:** Optimize the `.github/` folder structure for VS Code + GitHub Copilot agent primitives, eliminating context bloat, dead references, duplicate files, and misaligned patterns.

---

## L1.1 — Context Window Optimization

**Owner Domain:** infra (config)
**Priority:** P0 (Critical — 538 lines injected into every interaction regardless of relevance)

Eliminate context window bloat caused by `applyTo: '**'` on 5 instruction files, and consolidate duplicate workspace-level instruction sources (`copilot-instructions.md` + `AGENTS.md`).

- Switch 5 instruction files from `applyTo: '**'` to description-based on-demand discovery so VS Code loads them only when relevant keywords match.
- Consolidate `copilot-instructions.md` as the single lean workspace instruction file (<50 lines). Move orchestration rules from `AGENTS.md` into on-demand instruction files.

**Findings covered:** #1 (applyTo overuse), #2 (duplicate workspace instructions)

---

## L1.2 — Catalog & Reference Hygiene

**Owner Domain:** infra (config)
**Priority:** P1 (High — ghost references cause agent boot failures or wasted context)

Clean dead references from catalog files and eliminate the duplicate catalog.

- Remove references to non-existent files from `.github/vibecoding/catalog.yml`: `_cross-cutting-protocols.md`, `VALIDATION-REPORT.md`, `ARCHITECTURE.instructions.md`, `core_governance.instructions.md`, entire `governance/*` directory.
- Delete `.github/skills/catalog.yml` (identical duplicate of `.github/vibecoding/catalog.yml`).

**Findings covered:** #3 (ghost references), #4 (duplicate catalogs)

---

## L1.3 — Agent File Optimization

**Owner Domain:** infra (config)
**Priority:** P1 (High — 3062 total lines across 15 agents, average 204 lines with heavy duplication)

Trim agent `.agent.md` files to ≤80 lines body by extracting duplicated cross-cutting rules (boot sequence, forbidden actions, tool loadout tables, execution SOP) into shared instruction files that agents reference.

**Findings covered:** #10 (agent files too large)

---

## L1.4 — Tool Configuration Cleanup

**Owner Domain:** infra (config)
**Priority:** P2 (Medium — custom patterns that don't align with Copilot primitives)

Remove or realign tool configuration artifacts that use non-standard patterns:
- Remove `.github/tool-sets/` directory (custom, agents can't resolve `#universal` references).
- Either merge `.github/sandbox/tool-acl.yaml` rules into agent `tools:` frontmatter or document as reference-only.
- Fix hook `toolNames` in `policy-enforcement.json` to match actual VS Code tool names.

**Findings covered:** #5 (tool-sets not a primitive), #6 (tool ACLs unenforced), #7 (hook toolNames mismatch)

---

## L1.5 — Skills & Directory Cleanup

**Owner Domain:** docs / infra
**Priority:** P2-P3 (Medium-Low — improves maintainability but not blocking)

Audit and clean up shallow skill files and unused infrastructure directories:
- Evaluate 20 skill directories; convert shallow stubs (<40 lines with no real procedures) into `.instructions.md` files or flesh out with actionable content.
- Remove empty/stub directories: `.github/observability/`, `.github/tasks/`, `.github/proposals/`.

**Findings covered:** #8 (shallow skills), #9 (unused directories)
