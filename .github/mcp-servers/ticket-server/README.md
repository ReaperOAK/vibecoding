# MCP Ticket Server

last_reviewed: 2026-03-27

## Overview

The ticket server exposes ticket operations over MCP tools and resources.
Tools wrap `tickets.py` actions, while resources provide direct read access to
structured ticket data.

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
