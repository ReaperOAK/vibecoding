#!/usr/bin/env python3
"""MCP Ticket Server - wraps tickets.py for typed tool access via MCP protocol.

Uses the mcp Python SDK (FastMCP pattern) with stdio transport.
All 7 tools delegate to tickets.py via subprocess.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

TICKETS_PY = str(Path(__file__).resolve().parent.parent.parent.parent / "tickets.py")
WORKSPACE = str(Path(__file__).resolve().parent.parent.parent.parent)

mcp = FastMCP("ticket-server")


def _run_tickets_py(args: list[str]) -> tuple[int, str, str]:
    """Run tickets.py with the given arguments and return (returncode, stdout, stderr)."""
    cmd = [sys.executable, TICKETS_PY] + args
    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=WORKSPACE, timeout=30
    )
    return result.returncode, result.stdout, result.stderr


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
