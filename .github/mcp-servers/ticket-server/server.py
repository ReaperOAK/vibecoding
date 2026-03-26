#!/usr/bin/env python3
"""MCP Ticket Server - wraps tickets.py for typed tool access via MCP protocol."""

import json
import subprocess
import sys
import os

TICKETS_PY = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'tickets.py')
WORKSPACE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')

TOOLS = {
    "syncTickets": {
        "description": "Sync ticket state: release expired claims, evaluate deps, move unblocked to READY",
        "inputSchema": {"type": "object", "properties": {}, "required": []}
    },
    "getStatus": {
        "description": "Get dashboard view of all tickets",
        "inputSchema": {
            "type": "object",
            "properties": {"format": {"type": "string", "enum": ["json", "text"], "default": "text"}},
            "required": []
        }
    },
    "claimTicket": {
        "description": "Claim a READY ticket for an agent",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ticketId": {"type": "string"}, "agent": {"type": "string"},
                "machine": {"type": "string"}, "operator": {"type": "string"}
            },
            "required": ["ticketId", "agent", "machine", "operator"]
        }
    },
    "advanceTicket": {
        "description": "Advance a ticket to the next SDLC stage",
        "inputSchema": {
            "type": "object",
            "properties": {"ticketId": {"type": "string"}, "agent": {"type": "string"}},
            "required": ["ticketId", "agent"]
        }
    },
    "releaseTicket": {
        "description": "Release a stale claim on a ticket",
        "inputSchema": {
            "type": "object",
            "properties": {"ticketId": {"type": "string"}},
            "required": ["ticketId"]
        }
    },
    "reworkTicket": {
        "description": "Send a ticket back for rework with rejection reason",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ticketId": {"type": "string"}, "agent": {"type": "string"},
                "reason": {"type": "string"}
            },
            "required": ["ticketId", "agent", "reason"]
        }
    },
    "validateIntegrity": {
        "description": "Run full integrity check on ticket state",
        "inputSchema": {"type": "object", "properties": {}, "required": []}
    }
}


def run_tickets_py(args):
    cmd = [sys.executable, TICKETS_PY] + args
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=WORKSPACE, timeout=30)
    return result.returncode, result.stdout, result.stderr


def handle_tool_call(name, arguments):
    if name == "syncTickets":
        rc, out, err = run_tickets_py(["--sync"])
        return {"success": rc == 0, "output": out.strip(), "errors": err.strip() if err else None}
    elif name == "getStatus":
        fmt = arguments.get("format", "text")
        args = ["--status"] + (["--json"] if fmt == "json" else [])
        rc, out, err = run_tickets_py(args)
        if fmt == "json" and rc == 0:
            try:
                return json.loads(out)
            except json.JSONDecodeError:
                return {"success": False, "output": out.strip()}
        return {"success": rc == 0, "output": out.strip()}
    elif name == "claimTicket":
        rc, out, err = run_tickets_py(["--claim", arguments["ticketId"], arguments["agent"], arguments["machine"], arguments["operator"]])
        return {"success": rc == 0, "message": out.strip()}
    elif name == "advanceTicket":
        rc, out, err = run_tickets_py(["--advance", arguments["ticketId"], arguments["agent"]])
        return {"success": rc == 0, "message": out.strip()}
    elif name == "releaseTicket":
        rc, out, err = run_tickets_py(["--release", arguments["ticketId"]])
        return {"success": rc == 0, "message": out.strip()}
    elif name == "reworkTicket":
        rc, out, err = run_tickets_py(["--rework", arguments["ticketId"], arguments["agent"], arguments["reason"]])
        return {"success": rc == 0, "message": out.strip()}
    elif name == "validateIntegrity":
        rc, out, err = run_tickets_py(["--validate"])
        return {"success": rc == 0, "output": out.strip()}
    else:
        return {"error": f"Unknown tool: {name}"}


def handle_message(msg):
    method = msg.get("method")
    msg_id = msg.get("id")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {"listChanged": False}}, "serverInfo": {"name": "ticket-server", "version": "1.0.0"}}}
    elif method == "notifications/initialized":
        return None
    elif method == "tools/list":
        tool_list = [{"name": n, "description": s["description"], "inputSchema": s["inputSchema"]} for n, s in TOOLS.items()]
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": tool_list}}
    elif method == "tools/call":
        params = msg.get("params", {})
        result = handle_tool_call(params.get("name"), params.get("arguments", {}))
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}], "isError": "error" in result}}
    else:
        return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        response = handle_message(msg)
        if response is not None:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
