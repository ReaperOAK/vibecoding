# TASK-SYS-001: Create hook infrastructure directory and base configuration

**Type:** infra
**Priority:** critical
**Files:** .github/hooks/policy-enforcement.json, .github/hooks/scripts/README.md
**Tags:** hooks, infrastructure, P0

## Description
Create the `.github/hooks/` directory structure and base hook configuration file. This is the foundation for all deterministic policy enforcement, replacing instructional rules with shell-script-backed policy gates. Includes the hook scripts directory and a README documenting the hook architecture.

## Acceptance Criteria
- [ ] `.github/hooks/` directory exists with a valid JSON hook config (`policy-enforcement.json`)
- [ ] `.github/hooks/scripts/` directory exists with a README explaining hook architecture
- [ ] VS Code recognizes the hooks directory when `chat.hookFilesLocations` includes `.github/hooks`

---

# TASK-SYS-002: Implement guardian stop hook (SessionStart + PreToolUse)

**Type:** infra
**Priority:** critical
**Dependencies:** TASK-SYS-001
**Files:** .github/hooks/scripts/check-guardian-stop.sh, .github/hooks/policy-enforcement.json
**Tags:** hooks, guardian, safety, P0

## Description
Implement a shell-script hook that reads `.github/guardian/STOP_ALL` and blocks all agent activity when it contains "STOP". Fires on SessionStart (block session initialization) and PreToolUse (block all tool invocations). Replaces the instruction-based "Read STOP_ALL — if STOP: halt" rule with deterministic enforcement.

## Acceptance Criteria
- [ ] Given `.github/guardian/STOP_ALL` contains "STOP", when any agent starts a session, then the SessionStart hook blocks
- [ ] Given `.github/guardian/STOP_ALL` does not contain "STOP", when an agent starts, then the hook allows continuation
- [ ] Given the hook fires on PreToolUse, when STOP_ALL is active, then all tool invocations receive `permissionDecision: "deny"`

---

# TASK-SYS-003: Implement scoped git enforcement hook (PreToolUse)

**Type:** infra
**Priority:** critical
**Dependencies:** TASK-SYS-001
**Files:** .github/hooks/scripts/block-git-add-all.sh, .github/hooks/policy-enforcement.json
**Tags:** hooks, git-safety, P0

## Description
Implement a PreToolUse hook that blocks dangerous git commands: `git add .`, `git add -A`, `git add --all`, wildcard staging, and `git push --force`. Replaces the instruction-based "PROHIBITED: git add ." rule with deterministic enforcement.

## Acceptance Criteria
- [ ] Given a terminal command contains `git add .`, `git add -A`, or `git add --all`, when PreToolUse fires, then it returns `permissionDecision: "deny"` with reason
- [ ] Given a terminal command contains `git add specific-file.ts`, when PreToolUse fires, then it allows
- [ ] Given a terminal command contains `git push --force`, when PreToolUse fires, then it returns `permissionDecision: "ask"` requiring manual approval

---

# TASK-SYS-004: Implement memory gate enforcement hook (SubagentStop)

**Type:** infra
**Priority:** critical
**Dependencies:** TASK-SYS-001
**Files:** .github/hooks/scripts/verify-memory-gate.sh, .github/hooks/policy-enforcement.json
**Tags:** hooks, memory, P0

## Description
Implement a SubagentStop hook that verifies agents have written to `.github/memory-bank/activeContext.md` before being allowed to complete. Replaces the instruction-based "Before DONE, write to memory bank" rule with deterministic enforcement.

## Acceptance Criteria
- [ ] Given a subagent completes work, when SubagentStop fires, then it checks `.github/memory-bank/activeContext.md` for a recent entry
- [ ] Given no recent memory entry exists, when the hook evaluates, then it blocks completion with guidance
- [ ] Given a valid memory entry exists, when the hook evaluates, then it allows the stop to proceed

---

# TASK-SYS-005: Implement evidence rule enforcement hook (Stop)

**Type:** infra
**Priority:** high
**Dependencies:** TASK-SYS-001
**Files:** .github/hooks/scripts/verify-evidence.sh, .github/hooks/policy-enforcement.json
**Tags:** hooks, evidence, P1

## Description
Implement a Stop hook that verifies agent output summaries contain required evidence (artifact paths, test results, confidence level) before allowing session end. Replaces instruction-based evidence requirements with shell-script validation.

## Acceptance Criteria
- [ ] Given an agent session is ending, when the Stop hook fires, then it verifies artifact paths exist in the agent output summary
- [ ] Given the summary is missing or has no artifact paths, when evaluated, then the hook blocks with guidance
- [ ] Given evidence is present and valid (artifact paths, confidence, test results), when evaluated, then the hook allows session end

---

# TASK-SYS-006: Implement destructive command blocking hook (PreToolUse)

**Type:** infra
**Priority:** high
**Dependencies:** TASK-SYS-001
**Files:** .github/hooks/scripts/block-destructive-ops.sh, .github/hooks/policy-enforcement.json
**Tags:** hooks, safety, P1

## Description
Implement a PreToolUse hook that blocks destructive terminal commands: `rm -rf`, `DROP TABLE`, `DELETE FROM`, `git reset --hard`, and similar dangerous operations. Enforces the forbidden actions rules deterministically.

## Acceptance Criteria
- [ ] Given a terminal command contains `rm -rf`, `DROP TABLE`, `DELETE FROM`, or `git reset --hard`, when PreToolUse fires, then it returns `permissionDecision: "deny"`
- [ ] Given a terminal command is safe (e.g., `npm test`), when PreToolUse fires, then it allows
- [ ] Given a command requires human approval (e.g., database migration), when PreToolUse fires, then it returns `permissionDecision: "ask"`

---

# TASK-SYS-007: Configure VS Code workspace settings for hooks and agent features

**Type:** infra
**Priority:** critical
**Dependencies:** TASK-SYS-001
**Files:** .vscode/settings.json
**Tags:** vscode, configuration, P0

## Description
Configure VS Code workspace settings to enable the hooks system, custom agent hooks, instruction file locations, agent file locations, and prompt file locations. This is the settings glue that activates all hook-based enforcement.

## Acceptance Criteria
- [ ] Given settings.json is updated, when VS Code loads, then `chat.hookFilesLocations` includes `.github/hooks`
- [ ] Given settings are applied, then `chat.useCustomAgentHooks` is `true`
- [ ] Given settings are applied, then `chat.instructionsFilesLocations`, `chat.agentFilesLocations`, and `chat.promptFilesLocations` are correctly configured
