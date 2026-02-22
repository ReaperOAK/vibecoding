Debug the specified issue following a structured investigation protocol.

## Debug Protocol

### 1. REPRODUCE
- Confirm the error state exists with tool output evidence
- Capture exact error messages, stack traces, and reproduction steps
- Document the expected vs actual behavior

### 2. ISOLATE
- Narrow to the smallest reproducing scope using binary search
- Check recent changes: `git log --oneline -20` and `git diff`
- Compare working vs broken state
- Identify the exact file, function, and line causing the issue

### 3. DIAGNOSE
- Apply the 5-Why technique to find root cause (not symptoms):
  1. Why does this error occur?
  2. Why does that condition exist?
  3. Why was that the state?
  4. (Continue until root cause found)
- Distinguish correlation from causation
- Check if this is a known pattern or anti-pattern

### 4. FIX
- Write regression test BEFORE fixing (prove the bug exists)
- Apply minimal correct fix at root cause
- Prefer targeted fix over broad refactor
- Document what changed and why

### 5. VERIFY
- Original error no longer reproduces
- Regression test passes
- No new errors introduced
- Related functionality still works
- Run broader test suite if available

## Output Format

```markdown
## Bug Report: [Title]

### Reproduction
[Steps to reproduce, error output]

### Root Cause
[5-Why analysis result]

### Fix Applied
[Files modified, what changed, why]

### Verification
[Test results, evidence fix works]

### Prevention
[How to prevent similar issues]
```
