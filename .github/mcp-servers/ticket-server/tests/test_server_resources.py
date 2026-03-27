from __future__ import annotations

import importlib.util
import json
import sys
import types
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[4]
SERVER_PATH = ROOT / ".github/mcp-servers/ticket-server/server.py"


class FakeFastMCP:
    def __init__(self, name: str) -> None:
        self.name = name
        self.resource_handlers: dict[str, object] = {}
        self.tool_handlers: dict[str, object] = {}
        self.prompt_handlers: dict[str, object] = {}

    def resource(self, uri: str):
        def decorator(func):
            self.resource_handlers[uri] = func
            return func

        return decorator

    def tool(self, name: str):
        def decorator(func):
            self.tool_handlers[name] = func
            return func

        return decorator

    def prompt(self, name: str, description: str):
        def decorator(func):
            self.prompt_handlers[name] = {
                "description": description,
                "handler": func,
            }
            return func

        return decorator

    def run(self, transport: str) -> None:
        self.transport = transport


def load_server_module() -> types.ModuleType:
    mcp_module = types.ModuleType("mcp")
    server_module = types.ModuleType("mcp.server")
    fastmcp_module = types.ModuleType("mcp.server.fastmcp")
    fastmcp_module.FastMCP = FakeFastMCP

    sys.modules["mcp"] = mcp_module
    sys.modules["mcp.server"] = server_module
    sys.modules["mcp.server.fastmcp"] = fastmcp_module

    spec = importlib.util.spec_from_file_location("ticket_server", SERVER_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("Failed to load ticket server module spec")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TicketServerResourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = load_server_module()

    def test_resource_uris_are_registered(self) -> None:
        resource_handlers = self.server.mcp.resource_handlers

        self.assertIn("ticket://READY", resource_handlers)
        self.assertIn("ticket://DONE", resource_handlers)
        self.assertIn("ticket://{ticket_id}", resource_handlers)
        self.assertIn("prompts://list", resource_handlers)

    def test_ready_resource_returns_ready_ticket_summaries(self) -> None:
        raw_payload = self.server.read_ready_tickets()
        payload = json.loads(raw_payload)

        self.assertIsInstance(payload, list)
        self.assertGreaterEqual(len(payload), 1)
        for entry in payload:
            self.assertEqual({"id", "title", "type", "priority"}, set(entry))
            self.assertIsInstance(entry["id"], str)
            self.assertTrue(entry["id"])

    def test_done_resource_returns_completion_timestamps(self) -> None:
        raw_payload = self.server.read_done_tickets()
        payload = json.loads(raw_payload)

        self.assertIsInstance(payload, list)
        self.assertGreaterEqual(len(payload), 7)
        for entry in payload:
            self.assertEqual(
                {"id", "title", "type", "priority", "completed_at"},
                set(entry),
            )
            self.assertTrue(entry["completed_at"])

    def test_valid_ticket_resource_returns_full_ticket_document(self) -> None:
        expected_ticket = json.loads(
            (ROOT / "tickets/TASK-VIB-008.json").read_text(encoding="utf-8")
        )

        raw_payload = self.server.read_ticket("TASK-VIB-008")
        payload = json.loads(raw_payload)

        self.assertEqual(expected_ticket, payload)

    def test_invalid_ticket_resource_raises_file_not_found(self) -> None:
        with self.assertRaises(FileNotFoundError):
            self.server.read_ticket("TASK-VIB-404")

    def test_traversal_ticket_ids_raise_file_not_found(self) -> None:
        traversal_payloads = [
            "../ticket-state/READY/TASK-VIB-009",
            "..\\ticket-state\\READY\\TASK-VIB-009",
            "TASK-VIB-009/../../ticket-state/READY/TASK-VIB-009",
        ]

        for payload in traversal_payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(FileNotFoundError):
                    self.server.read_ticket(payload)

    def test_separator_bearing_ticket_ids_raise_file_not_found(self) -> None:
        malformed_ids = [
            "TASK/VIB-009",
            "TASK-VIB-009/extra",
            "TASK-VIB-009\\extra",
            "TASK VIB 009",
            "TASK-VIB-009.json",
        ]

        for ticket_id in malformed_ids:
            with self.subTest(ticket_id=ticket_id):
                with self.assertRaises(FileNotFoundError):
                    self.server.read_ticket(ticket_id)

    def test_completed_at_prefers_top_level_completed_at(self) -> None:
        completed_at = self.server._completed_at(
            {
                "completed_at": "2026-03-27T00:00:00+00:00",
                "history": [
                    {"event": "STAGE_COMPLETED", "to_stage": "DONE", "timestamp": "stale"}
                ],
            }
        )

        self.assertEqual("2026-03-27T00:00:00+00:00", completed_at)

    def test_completed_at_falls_back_to_done_history(self) -> None:
        completed_at = self.server._completed_at(
            {
                "history": [
                    {"event": "CREATED", "timestamp": "2026-03-26T00:00:00+00:00"},
                    {
                        "event": "STAGE_COMPLETED",
                        "to_stage": "DONE",
                        "timestamp": "2026-03-27T01:00:00+00:00",
                    },
                ]
            }
        )

        self.assertEqual("2026-03-27T01:00:00+00:00", completed_at)

    def test_completed_at_returns_none_without_done_history(self) -> None:
        completed_at = self.server._completed_at(
            {
                "history": [
                    {
                        "event": "STAGE_COMPLETED",
                        "to_stage": "QA",
                        "timestamp": "2026-03-27T01:00:00+00:00",
                    }
                ]
            }
        )

        self.assertIsNone(completed_at)

    def test_status_tool_parses_json_output(self) -> None:
        with mock.patch.object(
            self.server,
            "_run_tickets_py",
            return_value=(0, "{\"tickets\": 3}", ""),
        ):
            payload = json.loads(self.server.get_status(format="json"))

        self.assertEqual({"tickets": 3}, payload)

    def test_status_tool_falls_back_when_json_is_invalid(self) -> None:
        with mock.patch.object(
            self.server,
            "_run_tickets_py",
            return_value=(0, "not-json", ""),
        ):
            payload = json.loads(self.server.get_status(format="json"))

        self.assertEqual(False, payload["success"])
        self.assertEqual("not-json", payload["output"])

    def test_sync_and_integrity_tools_report_success_flag(self) -> None:
        with mock.patch.object(self.server, "_run_tickets_py", return_value=(0, "ok", "")):
            sync_payload = json.loads(self.server.sync_tickets())
            validate_payload = json.loads(self.server.validate_integrity())

        self.assertTrue(sync_payload["success"])
        self.assertEqual("ok", sync_payload["output"])
        self.assertIsNone(sync_payload["errors"])
        self.assertTrue(validate_payload["success"])

    def test_claim_advance_release_and_rework_tools_wrap_subprocess_result(self) -> None:
        with mock.patch.object(self.server, "_run_tickets_py", return_value=(0, "done", "")):
            claim_payload = json.loads(
                self.server.claim_ticket("TASK-VIB-009", "QA", "pop-os", "reaperoak")
            )
            advance_payload = json.loads(self.server.advance_ticket("TASK-VIB-009", "QA"))
            release_payload = json.loads(self.server.release_ticket("TASK-VIB-009"))
            rework_payload = json.loads(
                self.server.rework_ticket("TASK-VIB-009", "QA", "reason")
            )

        self.assertTrue(claim_payload["success"])
        self.assertEqual("done", claim_payload["message"])
        self.assertTrue(advance_payload["success"])
        self.assertTrue(release_payload["success"])
        self.assertTrue(rework_payload["success"])

    def test_process_ticket_valid_id(self) -> None:
        prompt_text = self.server.process_ticket_prompt("TASK-VIB-001")

        self.assertIn("TASK-VIB-001", prompt_text)
        self.assertIn("Description", prompt_text)
        self.assertIn("Acceptance Criteria", prompt_text)
        self.assertIn("File Paths In Scope", prompt_text)

    def test_process_ticket_invalid_id(self) -> None:
        prompt_text = self.server.process_ticket_prompt("TASK-VIB-999")

        self.assertIn("Ticket TASK-VIB-999 not found", prompt_text)

    def test_ticket_status_success(self) -> None:
        status_json = json.dumps(
            {
                "stage_counts": {
                    "READY": 2,
                    "BACKEND": 1,
                    "DONE": 3,
                },
                "total_tickets": 6,
            }
        )
        with mock.patch.object(self.server, "_run_tickets_py", return_value=(0, status_json, "")):
            dashboard = self.server.ticket_status_prompt()

        self.assertIn("| Stage | Count | Status |", dashboard)
        self.assertIn("| READY | 2 |", dashboard)
        self.assertIn("Total tickets: 6", dashboard)

    def test_ticket_status_subprocess_error(self) -> None:
        with mock.patch.object(
            self.server,
            "_run_tickets_py",
            return_value=(1, "", "boom"),
        ):
            dashboard = self.server.ticket_status_prompt()

        self.assertIn("Failed to fetch ticket status", dashboard)

    def test_prompts_list(self) -> None:
        payload = json.loads(self.server.read_prompts_list())
        prompt_names = {entry["name"] for entry in payload}

        self.assertEqual({"process-ticket", "ticket-status"}, prompt_names)

    def test_json_parse_error(self) -> None:
        with mock.patch.object(self.server, "_run_tickets_py", return_value=(0, "not-json", "")):
            dashboard = self.server.ticket_status_prompt()

        self.assertIn("Invalid status format", dashboard)


if __name__ == "__main__":
    unittest.main()
