#!/usr/bin/env python3
"""MCP Ticket Server - wraps tickets.py for typed tool access via MCP protocol.

Uses the mcp Python SDK (FastMCP pattern) with stdio transport.
All 7 tools delegate to tickets.py via subprocess.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

WORKSPACE_PATH = Path(__file__).resolve().parent.parent.parent.parent
TICKETS_PY = str(WORKSPACE_PATH / "tickets.py")
WORKSPACE = str(WORKSPACE_PATH)
TICKET_STATE_DIR = WORKSPACE_PATH / "ticket-state"
TICKETS_DIR = WORKSPACE_PATH / "tickets"
TICKET_ID_PATTERN = re.compile(r"TASK-[A-Z]+-\d{3}")
STAGE_AGENT_HINTS = {
    "READY": "Ticketer",
    "RESEARCH": "Research",
    "PM": "ProductManager",
    "ARCHITECT": "Architect",
    "DEVOPS": "DevOps",
    "BACKEND": "Backend",
    "UIDESIGNER": "UIDesigner",
    "FRONTEND": "Frontend",
    "QA": "QA",
    "SECURITY": "Security",
    "CI": "CIReviewer",
    "DOCS": "Documentation",
    "VALIDATION": "Validator",
    "DONE": "Ticketer",
}
STAGE_ORDER = [
    "READY",
    "RESEARCH",
    "PM",
    "ARCHITECT",
    "DEVOPS",
    "BACKEND",
    "UIDESIGNER",
    "FRONTEND",
    "QA",
    "SECURITY",
    "CI",
    "DOCS",
    "VALIDATION",
    "DONE",
]

mcp = FastMCP("ticket-server")


def _run_tickets_py(args: list[str]) -> tuple[int, str, str]:
    """Run tickets.py with the given arguments and return (returncode, stdout, stderr)."""
    cmd = [sys.executable, TICKETS_PY] + args
    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=WORKSPACE, timeout=30
    )
    return result.returncode, result.stdout, result.stderr


def _read_json_file(file_path: Path) -> dict[str, Any]:
    """Read and parse a JSON file from disk."""
    with file_path.open("r", encoding="utf-8") as file_handle:
        return json.load(file_handle)


def _validate_ticket_id(ticket_id: str) -> None:
    """Validate ticket ID against a strict regex allowlist.

    Args:
        ticket_id: Ticket identifier, for example ``TASK-VIB-008``.

    Raises:
        FileNotFoundError: If the ID does not match ``TASK-[A-Z]+-\d{3}``.

    Security:
        First defense against path traversal. Rejects malformed IDs before any
        filesystem path is constructed.
    """
    if not TICKET_ID_PATTERN.fullmatch(ticket_id):
        raise FileNotFoundError(f"Ticket '{ticket_id}' not found")


def _load_ticket(ticket_id: str) -> dict[str, Any]:
    """Load a ticket JSON document by ticket ID.

    Args:
        ticket_id: Ticket identifier in allowlisted format.

    Returns:
        Parsed ticket JSON document.

    Raises:
        FileNotFoundError: If ID validation fails, canonical containment fails,
            or the target ticket file does not exist.

    Security:
        Defense-in-depth path containment check with ``Path.resolve()`` and
        ``relative_to()`` ensures resolved paths remain inside ``tickets/``.
    """
    _validate_ticket_id(ticket_id)
    tickets_dir = TICKETS_DIR.resolve()
    ticket_path = (TICKETS_DIR / f"{ticket_id}.json").resolve()

    # Defense-in-depth: ensure the final path stays under tickets/.
    try:
        ticket_path.relative_to(tickets_dir)
    except ValueError as exc:
        raise FileNotFoundError(f"Ticket '{ticket_id}' not found") from exc

    if not ticket_path.exists():
        raise FileNotFoundError(f"Ticket '{ticket_id}' not found")
    return _read_json_file(ticket_path)


def _load_stage_tickets(stage: str) -> list[dict[str, Any]]:
    """Load all ticket JSON documents for a stage directory."""
    stage_dir = TICKET_STATE_DIR / stage
    if not stage_dir.exists():
        return []
    return [_read_json_file(ticket_path) for ticket_path in sorted(stage_dir.glob("*.json"))]


def _ready_ticket_summary(ticket: dict[str, Any]) -> dict[str, Any]:
    """Create the READY ticket summary shape exposed by the resource."""
    return {
        "id": ticket.get("ticket_id"),
        "title": ticket.get("title"),
        "type": ticket.get("type"),
        "priority": ticket.get("priority"),
    }


def _completed_at(ticket: dict[str, Any]) -> str | None:
    """Extract the completion timestamp for DONE tickets."""
    completed_at = ticket.get("completed_at")
    if isinstance(completed_at, str) and completed_at:
        return completed_at

    history = ticket.get("history")
    if not isinstance(history, list):
        return None

    for event in reversed(history):
        if not isinstance(event, dict):
            continue
        if event.get("event") == "STAGE_COMPLETED" and event.get("to_stage") == "DONE":
            timestamp = event.get("timestamp")
            if isinstance(timestamp, str) and timestamp:
                return timestamp
    return None


def _done_ticket_summary(ticket: dict[str, Any]) -> dict[str, Any]:
    """Create the DONE ticket summary shape exposed by the resource."""
    return {
        "id": ticket.get("ticket_id"),
        "title": ticket.get("title"),
        "type": ticket.get("type"),
        "priority": ticket.get("priority"),
        "completed_at": _completed_at(ticket),
    }


def _string_list(value: Any) -> list[str]:
    """Normalize arbitrary list-like metadata to a list of non-empty strings."""
    if not isinstance(value, list):
        return []
    return [entry.strip() for entry in value if isinstance(entry, str) and entry.strip()]


def _ticket_stage(ticket: dict[str, Any]) -> str:
    """Resolve current stage from ticket metadata."""
    stage = ticket.get("current_stage") or ticket.get("stage")
    if isinstance(stage, str) and stage.strip():
        return stage.strip().upper()
    return "BACKEND"


def _agent_hint(ticket: dict[str, Any], stage: str) -> str:
    """Resolve assignment hint from ticket metadata or stage mapping."""
    assigned_agent = ticket.get("assigned_agent")
    if isinstance(assigned_agent, str) and assigned_agent.strip():
        return assigned_agent.strip()
    return STAGE_AGENT_HINTS.get(stage, "Backend")


def _format_process_ticket_prompt(ticket: dict[str, Any]) -> str:
    """Build a markdown delegation prompt for one ticket.

    Args:
        ticket: Parsed ticket JSON document.

    Returns:
        Markdown string containing ticket ID, title, description,
        acceptance criteria, file scope, stage, and agent assignment hint.
    """
    ticket_id = str(ticket.get("ticket_id", "UNKNOWN"))
    title = str(ticket.get("title", "Untitled ticket"))
    description = str(ticket.get("description", "No description provided.")).strip()
    criteria = _string_list(ticket.get("acceptance_criteria"))
    file_paths = _string_list(ticket.get("file_paths"))
    stage = _ticket_stage(ticket)
    agent = _agent_hint(ticket, stage)

    criteria_lines = "\n".join(f"- {criterion}" for criterion in criteria) or "- None"
    paths_lines = "\n".join(f"- {file_path}" for file_path in file_paths) or "- None"

    return (
        "# Ticket Delegation Prompt\n\n"
        f"## Ticket\n- ID: {ticket_id}\n- Title: {title}\n\n"
        f"## Description\n{description}\n\n"
        f"## Acceptance Criteria\n{criteria_lines}\n\n"
        f"## File Paths In Scope\n{paths_lines}\n\n"
        f"## Stage\n- Current stage: {stage}\n\n"
        f"## Agent Assignment Hint\n- Suggested agent: {agent}\n"
    )


def _extract_stage_counts(status_payload: dict[str, Any]) -> dict[str, int]:
    """Extract stage counts from tickets.py status JSON output.

    Args:
        status_payload: Parsed JSON object returned by
            ``tickets.py --status --json``.

    Returns:
        Mapping of uppercase stage name to non-negative ticket count.

    Raises:
        ValueError: If the payload contains neither ``stage_counts`` nor
            ``stages`` data in a recognisable format.
    """
    stage_counts = status_payload.get("stage_counts")
    if isinstance(stage_counts, dict):
        counts: dict[str, int] = {}
        for stage, count in stage_counts.items():
            if isinstance(stage, str) and isinstance(count, int):
                counts[stage.upper()] = max(0, count)
        if counts:
            return counts

    stages_payload = status_payload.get("stages")
    if isinstance(stages_payload, dict):
        counts = {}
        for stage, entries in stages_payload.items():
            if isinstance(stage, str) and isinstance(entries, list):
                counts[stage.upper()] = len(entries)
        if counts:
            return counts

    raise ValueError("Missing stage count data")


def _format_ticket_status_prompt(status_payload: dict[str, Any]) -> str:
    """Render stage counts and totals as a Markdown dashboard.

    Args:
        status_payload: Parsed JSON object returned by
            ``tickets.py --status --json``.

    Returns:
        Markdown string with a stage count table and a total summary line.

    Raises:
        ValueError: Propagated from :func:`_extract_stage_counts` when count
            data cannot be extracted.
    """
    stage_counts = _extract_stage_counts(status_payload)
    total_tickets = status_payload.get("total_tickets")
    if not isinstance(total_tickets, int):
        total_tickets = sum(stage_counts.values())

    lines = [
        "# Ticket Status Dashboard",
        "",
        "| Stage | Count | Status |",
        "| --- | ---: | --- |",
    ]
    for stage in STAGE_ORDER:
        count = stage_counts.get(stage, 0)
        status_text = "Has tickets" if count > 0 else "Empty"
        lines.append(f"| {stage} | {count} | {status_text} |")

    stage_summary = ", ".join(
        f"{stage}: {stage_counts.get(stage, 0)}" for stage in STAGE_ORDER
    )
    lines.extend(["", f"Total tickets: {total_tickets} ({stage_summary})"])
    return "\n".join(lines)


@mcp.resource("ticket://READY")
def read_ready_tickets() -> str:
    """Return JSON summaries for all READY tickets.

    Returns:
        JSON array string with summary objects:
        ``[{"id": str, "title": str, "type": str, "priority": str}]``.
    """
    ready_tickets = [_ready_ticket_summary(ticket) for ticket in _load_stage_tickets("READY")]
    return json.dumps(ready_tickets, indent=2)


@mcp.resource("ticket://DONE")
def read_done_tickets() -> str:
    """Return JSON summaries for all completed tickets.

    Returns:
        JSON array string with completion metadata:
        ``[{"id": str, "title": str, "type": str, "priority": str,
        "completed_at": str | null}]``.
    """
    done_tickets = [_done_ticket_summary(ticket) for ticket in _load_stage_tickets("DONE")]
    return json.dumps(done_tickets, indent=2)


@mcp.resource("ticket://{ticket_id}")
def read_ticket(ticket_id: str) -> str:
    """Return the full ticket JSON for a specific ticket ID.

    Args:
        ticket_id: Ticket identifier from the URI template
            ``ticket://{ticket_id}``.

    Returns:
        Pretty-printed JSON string containing the full ticket document.

    Raises:
        FileNotFoundError: For invalid IDs, containment failures, or missing
            ticket files. Error message format is consistent with normal
            not-found behavior.
    """
    return json.dumps(_load_ticket(ticket_id), indent=2)


@mcp.resource("prompts://list")
def read_prompts_list() -> str:
    """Return prompt metadata exposed by this server."""
    prompts = [
        {
            "name": "process-ticket",
            "description": "Generate delegation prompt for given ticket",
            "arguments": [
                {
                    "name": "ticket_id",
                    "type": "string",
                    "required": True,
                }
            ],
        },
        {
            "name": "ticket-status",
            "description": "Generate ticket status dashboard",
            "arguments": [],
        },
    ]
    return json.dumps(prompts, indent=2)


@mcp.prompt(name="process-ticket", description="Generate delegation prompt for given ticket")
def process_ticket_prompt(ticket_id: str) -> str:
    """Generate a delegation prompt from ticket metadata.

    Args:
        ticket_id: Ticket identifier in ``TASK-[A-Z]+-\\d{3}`` format.

    Returns:
        Markdown delegation prompt with ticket title, description,
        acceptance criteria, file scope, stage, and agent assignment hint.
        Returns an error string when the ticket cannot be found or read.
    """
    try:
        ticket = _load_ticket(ticket_id)
    except FileNotFoundError:
        return f"Ticket {ticket_id} not found"
    except (json.JSONDecodeError, OSError):
        return "Failed to read ticket metadata"

    return _format_process_ticket_prompt(ticket)


@mcp.prompt(name="ticket-status", description="Generate ticket status dashboard")
def ticket_status_prompt() -> str:
    """Generate a status dashboard for all ticket stages.

    Returns:
        Markdown table summarising per-stage ticket counts and a total
        summary line. Returns an error string when ``tickets.py`` cannot
        be reached or returns malformed output.
    """
    rc, out, err = _run_tickets_py(["--status", "--json"])
    if rc != 0:
        error_text = f"{out}\n{err}".lower()
        if "no such file" in error_text or "not initialized" in error_text:
            return "Ticket system not initialized"
        return "Failed to fetch ticket status"

    try:
        status_payload = json.loads(out)
    except json.JSONDecodeError:
        return "Invalid status format"

    if not isinstance(status_payload, dict):
        return "Invalid status format"

    try:
        return _format_ticket_status_prompt(status_payload)
    except ValueError:
        return "Invalid status format"


@mcp.tool(name="syncTickets")
def sync_tickets() -> str:
    """Sync ticket state: release expired claims, evaluate deps, move unblocked to READY."""
    rc, out, err = _run_tickets_py(["--sync"])
    return json.dumps({
        "success": rc == 0,
        "output": out.strip(),
        "errors": err.strip() if err.strip() else None,
    })


@mcp.tool(name="getStatus")
def get_status(format: str = "text") -> str:
    """Get dashboard view of all tickets. Use format='json' for structured output."""
    args = ["--status"] + (["--json"] if format == "json" else [])
    rc, out, err = _run_tickets_py(args)
    if format == "json" and rc == 0:
        try:
            parsed = json.loads(out)
            return json.dumps(parsed, indent=2)
        except json.JSONDecodeError:
            return json.dumps({"success": False, "output": out.strip()})
    return json.dumps({"success": rc == 0, "output": out.strip()})


@mcp.tool(name="claimTicket")
def claim_ticket(ticketId: str, agent: str, machine: str, operator: str) -> str:
    """Claim a READY ticket for an agent."""
    rc, out, err = _run_tickets_py(
        ["--claim", ticketId, agent, machine, operator]
    )
    return json.dumps({"success": rc == 0, "message": out.strip()})


@mcp.tool(name="advanceTicket")
def advance_ticket(ticketId: str, agent: str) -> str:
    """Advance a ticket to the next SDLC stage."""
    rc, out, err = _run_tickets_py(["--advance", ticketId, agent])
    return json.dumps({"success": rc == 0, "message": out.strip()})


@mcp.tool(name="releaseTicket")
def release_ticket(ticketId: str) -> str:
    """Release a stale claim on a ticket."""
    rc, out, err = _run_tickets_py(["--release", ticketId])
    return json.dumps({"success": rc == 0, "message": out.strip()})


@mcp.tool(name="reworkTicket")
def rework_ticket(ticketId: str, agent: str, reason: str) -> str:
    """Send a ticket back for rework with rejection reason."""
    rc, out, err = _run_tickets_py(
        ["--rework", ticketId, agent, reason]
    )
    return json.dumps({"success": rc == 0, "message": out.strip()})


@mcp.tool(name="validateIntegrity")
def validate_integrity() -> str:
    """Run full integrity check on ticket state."""
    rc, out, err = _run_tickets_py(["--validate"])
    return json.dumps({
        "success": rc == 0,
        "output": out.strip(),
    })


if __name__ == "__main__":
    mcp.run(transport="stdio")
