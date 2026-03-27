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
    """Enforce strict ticket ID format for resource reads."""
    if not TICKET_ID_PATTERN.fullmatch(ticket_id):
        raise FileNotFoundError(f"Ticket '{ticket_id}' not found")


def _load_ticket(ticket_id: str) -> dict[str, Any]:
    """Load a ticket JSON document by ticket ID."""
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


@mcp.resource("ticket://READY")
def read_ready_tickets() -> str:
    """Return JSON summaries for all READY tickets."""
    ready_tickets = [_ready_ticket_summary(ticket) for ticket in _load_stage_tickets("READY")]
    return json.dumps(ready_tickets, indent=2)


@mcp.resource("ticket://DONE")
def read_done_tickets() -> str:
    """Return JSON summaries for all completed tickets."""
    done_tickets = [_done_ticket_summary(ticket) for ticket in _load_stage_tickets("DONE")]
    return json.dumps(done_tickets, indent=2)


@mcp.resource("ticket://{ticket_id}")
def read_ticket(ticket_id: str) -> str:
    """Return the full ticket JSON for a specific ticket ID."""
    return json.dumps(_load_ticket(ticket_id), indent=2)


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
