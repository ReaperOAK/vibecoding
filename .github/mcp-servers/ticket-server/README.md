# MCP Ticket Server

last_reviewed: 2026-03-27

## Overview

The ticket server exposes ticket operations over MCP tools, resources, and
prompts. Tools wrap `tickets.py` actions, resources provide direct read access
to structured ticket data, and prompts generate delegation content for agents.

## MCP Resources

The server exposes three MCP resource URIs:

1. `ticket://READY`
2. `ticket://DONE`
3. `ticket://{ticket-id}`

### Resource: `ticket://READY`

Returns a JSON array of READY ticket summaries.

Example response:

```json
[
  {
    "id": "TASK-VIB-012",
    "title": "Example Ready Ticket",
    "type": "backend",
    "priority": "high"
  }
]
```

Example usage (pseudo-code):

```python
ready_json = mcp_client.resources.read("ticket://READY")
ready_tickets = json.loads(ready_json)
```

### Resource: `ticket://DONE`

Returns a JSON array of completed ticket summaries with completion timestamps.

Example response:

```json
[
  {
    "id": "TASK-VIB-001",
    "title": "Completed Ticket",
    "type": "infra",
    "priority": "medium",
    "completed_at": "2026-03-26T12:03:21+00:00"
  }
]
```

Example usage (pseudo-code):

```python
done_json = mcp_client.resources.read("ticket://DONE")
done_tickets = json.loads(done_json)
```

### Resource: `ticket://{ticket-id}`

Returns the full ticket JSON object for a specific ticket ID.

URI format:

- `ticket://{ticket-id}` where `{ticket-id}` follows `TASK-[A-Z]+-\d{3}`
- Example: `ticket://TASK-VIB-008`

Example response:

```json
{
  "ticket_id": "TASK-VIB-008",
  "title": "Add MCP Resources to Ticket Server",
  "stage": "DOCS",
  "type": "backend",
  "priority": "high"
}
```

Example usage (pseudo-code):

```python
ticket_json = mcp_client.resources.read("ticket://TASK-VIB-008")
ticket = json.loads(ticket_json)
```

## MCP Prompts

The server exposes two MCP prompt templates via the MCP Prompts API.
Use `mcp_client.prompts.get(name, arguments)` to call them.

A metadata resource is also available at `prompts://list`.

### Prompt: `process-ticket`

Generates a complete agent delegation prompt from ticket metadata.

**Arguments:**

| Argument | Type | Required | Description |
| --- | --- | --- | --- |
| `ticket_id` | string | Yes | Ticket ID matching `TASK-[A-Z]+-NNN` |

**Returns:** A Markdown delegation prompt containing:

- Ticket ID and title
- Full description
- Acceptance criteria list
- File paths in scope
- Current stage and suggested agent

**Example usage (pseudo-code):**

```python
delegation = mcp_client.prompts.get(
    "process-ticket", {"ticket_id": "TASK-VIB-009"}
)
```

**Example output:**

```markdown
# Ticket Delegation Prompt

## Ticket
- ID: TASK-VIB-009
- Title: Add MCP Prompts to Ticket Server

## Description
The MCP ticket server should expose canned prompt templates ...

## Acceptance Criteria
- Given the updated server.py, When a MCP client calls `prompts/list`, ...

## File Paths In Scope
- .github/mcp-servers/ticket-server/server.py

## Stage
- Current stage: DOCS

## Agent Assignment Hint
- Suggested agent: Documentation
```

**Error responses:**

| Condition | Response |
| --- | --- |
| Invalid or missing ticket ID | `Ticket {id} not found` |
| Ticket file unreadable or malformed | `Failed to read ticket metadata` |

### Prompt: `ticket-status`

Generates a formatted Markdown dashboard of all ticket stages and counts.

**Arguments:** None

**Returns:** A Markdown table showing per-stage ticket counts and a total
summary line.

**Example usage (pseudo-code):**

```python
dashboard = mcp_client.prompts.get("ticket-status")
```

**Example output:**

```markdown
# Ticket Status Dashboard

| Stage | Count | Status |
| --- | ---: | --- |
| READY | 2 | Has tickets |
| BACKEND | 1 | Has tickets |
| DONE | 7 | Has tickets |
...

Total tickets: 10 (READY: 2, BACKEND: 1, ...)
```

**Error responses:**

| Condition | Response |
| --- | --- |
| `tickets.py` subprocess fails | `Failed to fetch ticket status` |
| Ticket system not found or uninitialized | `Ticket system not initialized` |
| Status JSON is malformed | `Invalid status format` |

### Resource: `prompts://list`

Returns metadata for all available prompt templates as a JSON array.

**Example response:**

```json
[
  {
    "name": "process-ticket",
    "description": "Generate delegation prompt for given ticket",
    "arguments": [
      {"name": "ticket_id", "type": "string", "required": true}
    ]
  },
  {
    "name": "ticket-status",
    "description": "Generate ticket status dashboard",
    "arguments": []
  }
]
```

## Security

Resources validate ticket IDs with regex allowlist and canonical path containment to prevent directory traversal.

## Error Handling

Invalid ticket IDs return FileNotFoundError with consistent message format.
The same not-found message is used for malformed IDs, containment failures,
and missing ticket files.

## API Notes

- Resource responses are JSON strings that can be parsed into an object or array.
- `ticket://READY` and `ticket://DONE` return arrays.
- `ticket://{ticket-id}` returns a single JSON object.
