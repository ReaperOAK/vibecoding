Update the memory bank files in `.github/memory-bank/` to reflect the current session's work.

Follow this protocol:

1. **Read ALL memory bank files first** — even if you think some don't need updates:
   - `.github/memory-bank/productContext.md`
   - `.github/memory-bank/systemPatterns.md`
   - `.github/memory-bank/activeContext.md`
   - `.github/memory-bank/progress.md`
   - `.github/memory-bank/decisionLog.md`
   - `.github/memory-bank/riskRegister.md`

2. **Update `activeContext.md`** — Append a new entry with:
   - Current timestamp (ISO-8601)
   - Attribution to "Claude Code"
   - Current focus description
   - Recent changes summary
   - Next steps

3. **Update `progress.md`** — If any milestones were completed or new work started:
   - Move completed items with evidence
   - Add new in-progress items
   - Update pending backlog

4. **Update `decisionLog.md`** — If any significant decisions were made:
   - Append new decision entry with full rationale
   - Never delete existing entries

5. **Update `riskRegister.md`** — If any new risks were identified:
   - Append new risk entry
   - Update status of existing risks if mitigated

**Rules:**
- `systemPatterns.md` and `decisionLog.md` are APPEND-ONLY — never delete or overwrite
- All entries must include timestamps and attribution
- Provide a summary of what was updated after completing
