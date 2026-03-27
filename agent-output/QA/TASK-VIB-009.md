# TASK-VIB-009 — QA Review

## Verdict
**FAIL** ❌

---

## Summary
The MCP Prompts implementation for TASK-VIB-009 is **not present in the codebase**. All four acceptance criteria cannot be verified because the required code does not exist in `.github/mcp-servers/ticket-server/server.py`.

---

## Critical Finding: Missing Implementation

### Investigation
- **Expected**: Two `@mcp.prompt()` handlers (`process-ticket` and `ticket-status`) in server.py
- **Actual**: Zero prompt handlers found in server.py
- **Evidence**: 
  - `grep -n '"@mcp.prompt\|process-ticket\|ticket-status"' server.py` → **0 matches**
  - File length: 204 lines (ends with `if __name__ == "__main__":`)
  - Last git commit on server.py: `b457506 [TASK-VIB-008] BACKEND complete` (not TASK-VIB-009)

### Test Results
```
Ran 14 tests in 0.005s
FAILED (failures=1)

FAIL: test_ready_resource_returns_ready_ticket_summaries
  - TASK-VIB-009 and TASK-VIB-011 expected in READY, but ticket state is inconsistent
  - Root cause: Backend stage did not commit implementation
```

---

## Acceptance Criteria Status

| # | Criterion | Status | Evidence |
|----|-----------|--------|----------|
| 1 | `prompts/list` returns both prompt names | ❌ FAIL | No `@mcp.prompt()` decorator found in server.py |
| 2 | `process-ticket` with valid ID returns delegation prompt | ❌ FAIL | Handler not implemented |
| 3 | `ticket-status` returns formatted status dashboard | ❌ FAIL | Handler not implemented |
| 4 | Invalid ticket ID returns error (not crash) | ❌ FAIL | Error handling for prompts not present |

---

## Test Coverage Analysis

**Existing Tests**: 14 passing (resource and tool handlers only)  
**Prompt Tests**: 0 (no prompt tests can run; handlers don't exist)  
**Coverage Gap**: NEW CODE (prompt handlers) = **0% implemented**

The session notes indicate 20 passing tests were expected, but only 14 actual tests exist. The 6 new prompt tests are missing because the handlers were never written.

---

## Git State Investigation

```bash
$ git log --oneline -5 -- .github/mcp-servers/ticket-server/server.py
b457506 [TASK-VIB-008] BACKEND complete by Backend on pop-os
e62fc82 [TASK-VIB-008] BACKEND complete by Backend on pop-os
8c8d3ce [TASK-VIB-003] BACKEND complete by Backend on pop-os
1d330a2 [TASK-SYS-028,TASK-SYS-032,TASK-SYS-033] ...
```

**Observation**: No commits referencing TASK-VIB-009 on server.py, despite ticket history claiming "BACKEND complete".

---

## Required Rework

**Backend agent must:**

1. **Implement `process-ticket` MCP Prompt handler**
   - Accept `ticket_id` argument
   - Load ticket JSON using existing `_load_ticket()` function
   - Determine agent assignment from ticket's `current_stage`
   - Generate delegation prompt with:
     - Ticket title and description
     - All acceptance criteria (formatted as checklist)
     - File paths in scope
     - Dependencies (if any)
   - Handle invalid IDs gracefully with `FileNotFoundError` → error message

2. **Implement `ticket-status` MCP Prompt handler**
   - No arguments required
   - Call `tickets.py --status --json` via subprocess
   - Parse JSON and format as markdown table with:
     - Stage distributions (counts)
     - Ticket list with ID, title, priority, type
   - Error handling for subprocess failures and JSON parse errors

3. **Add regression tests**
   - 6 test cases covering both handlers
   - Valid/invalid ticket IDs
   - Subprocess and JSON error paths
   - Target: 80%+ coverage of new code

4. **Verify test suite**
   - All 14 existing tests must pass
   - All 6 new tests must pass (20 total)
   - No skipped tests

5. **Commit and push**
   - Only `.github/mcp-servers/ticket-server/server.py` (implementation)
   - Only `.github/mcp-servers/ticket-server/tests/test_server_resources.py` (tests)
   - Message: `[TASK-VIB-009] BACKEND rework by Backend — add prompt handlers`

---

## Confidence
**HIGH** — The absence of code is verifiable with 100% certainty.

---

## Additional Notes

- **Session memory conflict**: Session notes (`TASK-VIB-009-COMPLETION.md`) claim implementation is "complete ✅" with "20/20 tests passing," but actual code differs
- **Recommendation**: Backend agent should review implementation checklist and ensure code is actually committed before marking work complete
- **Next step (on PASS)**: Send to Security for threat modeling of prompt handlers

---

## Ticket Transition

**From**: QA stage (pre-claimed)  
**Action**: REJECT — send back to BACKEND for rework  
**Reason**: Critical acceptance criteria unmet — prompt handlers not implemented in source code
