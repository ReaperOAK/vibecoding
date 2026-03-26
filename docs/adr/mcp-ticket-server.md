# ADR: MCP Ticket Server Architecture

## Status
Proposed

## Context
`tickets.py` provides CLI-based ticket management. Agents currently invoke it via shell commands (`python3 tickets.py --claim`, `--advance`, etc.). An MCP server wrapping this functionality would provide typed tool interfaces, better error handling, and eliminate shell invocation overhead.

## Decision

### Transport: stdio
- **Chosen**: stdio (standard input/output)
- **Rationale**: VS Code MCP support uses stdio transport. No HTTP server management needed. Simple process lifecycle — starts with agent session, stops when session ends.
- **Rejected alternative**: HTTP/SSE — adds deployment complexity, port management, no benefit for local single-user operation.

### Implementation Language: Python
- **Chosen**: Python (same as tickets.py)
- **Rationale**: Direct import of tickets.py functions. No serialization boundary. Single dependency chain.
- **Rejected alternative**: TypeScript — would require subprocess calls to tickets.py, losing direct access.

### Tool Definitions

| Tool | Input Schema | Output |
|------|-------------|--------|
| `syncTickets` | `{}` | `{ moved: string[], blocked: { id, blockers }[] }` |
| `getStatus` | `{ format?: "json" \| "text" }` | `{ stages: Record<string, Ticket[]>, claims: Claim[] }` |
| `claimTicket` | `{ ticketId: string, agent: string, machine: string, operator: string }` | `{ success: boolean, message: string }` |
| `advanceTicket` | `{ ticketId: string, agent: string }` | `{ success: boolean, from: string, to: string }` |
| `releaseTicket` | `{ ticketId: string }` | `{ success: boolean }` |
| `reworkTicket` | `{ ticketId: string, agent: string, reason: string }` | `{ success: boolean }` |
| `validateIntegrity` | `{}` | `{ valid: boolean, issues: string[] }` |

### Sandboxing Configuration

```json
{
  "mcpServers": {
    "tickets": {
      "command": "python3",
      "args": [".github/mcp/ticket-server.py"],
      "cwd": "${workspaceFolder}",
      "env": {}
    }
  }
}
```

### File Structure

```
.github/mcp/
├── ticket-server.py    # MCP server wrapping tickets.py
└── README.md           # Usage documentation
```

## Consequences

**Positive:**
- Typed tool interfaces replace fragile shell command parsing
- Better error reporting (structured JSON vs stderr text)
- Discoverable tools in VS Code MCP panel

**Negative:**
- Additional maintenance surface
- Requires MCP SDK dependency (mcp-python)

**Risks:**
- MCP protocol may evolve — pin SDK version
- tickets.py refactoring must keep MCP server in sync

## References
- [Model Context Protocol Specification](https://modelcontextprotocol.io/specification)
- VS Code MCP integration docs
- tickets.py source
