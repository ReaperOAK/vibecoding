# Vibecoding System Upgrade — Complete Ticket Map

## Dependency Graph

```
SYS001 (Hook Infrastructure)
├── SYS002 (Guardian Stop Hook)
├── SYS003 (Scoped Git Hook)
├── SYS004 (Memory Gate Hook)
├── SYS005 (Evidence Rule Hook)
├── SYS006 (Destructive Command Hook)
└── SYS007 (VS Code Settings)
    ├── SYS018 (Agent-Scoped Lint Hook)
    └── SYS019 (Ticketer Scope Guard Hook)

SYS008 (CTO Subagent Scoping) ─── independent
├── SYS010 (CTO→Ticketer Handoff)
    └── SYS011 (SDLC Stage Handoffs)
        └── SYS012 (Rework Handoffs)

SYS009 (Ticketer Subagent Scoping) ─── independent

ARC013-016 (Tool Loadout Audit) ─── independent (4 parallel tasks)

ARC017 (Reference Link Conversion) ─── independent

SYS020 (Prompt File Agent Field) ─── independent
└── SYS021 (Prompt File Tools Field)

SYS022, SYS023, SYS024 (Instruction Scoping) ─── independent

SYS025 (Skills Directory)
└── SYS026 (Skills Migration)

SYS027 (MCP Server Design)
└── SYS028 (MCP Server Implementation)

SYS029 (Tool Sets) ─── independent
```

## Execution Priority Order

### Wave 1 — P0 Foundation (No Dependencies)
| Ticket | Title | Effort |
|--------|-------|--------|
| SYS001 | Hook infrastructure setup | S |
| SYS008 | CTO subagent scoping | S |
| SYS009 | Ticketer subagent scoping | S |
| ARC017 | Convert references to Markdown links | S |

### Wave 2 — P0 Enforcement (Depends on SYS001)
| Ticket | Title | Effort |
|--------|-------|--------|
| SYS002 | Guardian stop hook | S |
| SYS003 | Scoped git enforcement hook | S |
| SYS004 | Memory gate enforcement hook | M |
| SYS007 | VS Code settings configuration | S |
| SYS010 | CTO→Ticketer handoff | S |

### Wave 3 — P1 Hardening (Parallel)
| Ticket | Title | Effort |
|--------|-------|--------|
| SYS005 | Evidence rule hook | M |
| SYS006 | Destructive command hook | S |
| SYS011 | SDLC stage handoffs | M |
| ARC013 | Audit CTO tool loadout | S |
| ARC014 | Audit Ticketer tool loadout | S |
| ARC015 | Audit implementing agent tools | M |
| ARC016 | Audit review agent tools | M |
| SYS020 | Prompt file agent routing | S |

### Wave 4 — P1 Polish (Dependencies from Wave 2-3)
| Ticket | Title | Effort |
|--------|-------|--------|
| SYS012 | Rework handoffs | S |
| SYS018 | Agent-scoped lint hook | S |
| SYS019 | Ticketer scope guard hook | S |
| SYS021 | Prompt file tools field | S |

### Wave 5 — P2 Optimization (Independent)
| Ticket | Title | Effort |
|--------|-------|--------|
| SYS022 | Python instruction scoping | S |
| SYS023 | Agent definition instruction | S |
| SYS024 | Git protocol instruction scoping | S |
| SYS025 | Skills directory setup | M |
| SYS029 | Tool sets creation | S |

### Wave 6 — P2-P3 Future (Dependencies from Wave 5)
| Ticket | Title | Effort |
|--------|-------|--------|
| SYS026 | Skills migration | M |
| SYS027 | MCP ticket server design | M |
| SYS028 | MCP ticket server implementation | L |

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total L3 tickets | 29 |
| P0 (Critical) | 8 |
| P1 (High) | 12 |
| P2 (Medium) | 7 |
| P3 (Low) | 2 |
| XS effort | 0 |
| S effort | 17 |
| M effort | 10 |
| L effort | 2 |
| Max parallel in Wave 1 | 4 |
| Max parallel in Wave 3 | 8 |
