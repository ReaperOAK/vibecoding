#!/usr/bin/env python3
"""
 PROJECT BOARD — Global Task Visualizer
================================================
Two-pass global dependency resolution with dual output.
Read-only: NEVER mutates source .md files.

Usage:
    python3 todo_visual.py              # Terminal + HTML output
    python3 todo_visual.py --terminal   # Terminal only
    python3 todo_visual.py --html       # HTML only
    python3 todo_visual.py --list       # List discovered files
    python3 todo_visual.py --json       # Machine-readable JSON
    python3 todo_visual.py --ready      # Actionable tasks (non-blocked, deps met)
    python3 todo_visual.py --ready --json  # Actionable tasks as JSON
"""

from __future__ import annotations

import json
import logging
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

# ─── Logging (never leak local paths into console) ───────────
logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
_log = logging.getLogger("board")

# ─── Configuration ───────────────────────────────────────────
ROOT = Path(__file__).resolve().parent

TODO_GLOBS: list[str] = [
    "*_TODO.md",
    "*_todo.md",
    "*-todo.md",
    "*-TODO.md",
    "TODO/**/*.md",
]

EXCLUDE_PARTS: set[str] = {
    "node_modules", ".git", "dist", "build", ".next",
    "__pycache__", "coverage", ".github", "archive",
}

# Task header: ### IDFC-001: Title  or  #### TODO-WLB001: Title
_TASK_HDR = re.compile(
    r"^(#{2,4})\s+([A-Z][A-Z0-9-]*\d{3,4}):\s*(.+)$",
)

_ID_RE = re.compile(r"[A-Z][A-Z0-9-]*\d{3,4}")

_STATUS_CANON: dict[str, str] = {
    "completed": "completed", "done": "completed", "complete": "completed",
    "✅": "completed", "✅ completed": "completed",
    "not_started": "not_started", "not started": "not_started",
    "pending": "not_started", "todo": "not_started",
    "⬜": "not_started",
    "in_progress": "in_progress", "in progress": "in_progress",
    "wip": "in_progress", "🔄": "in_progress",
    "blocked": "blocked", "⏸️": "blocked", "⏸": "blocked",
    "ready": "ready", "🟢": "ready",
}


# ─── Data Model ──────────────────────────────────────────────
@dataclass
class Task:
    id: str
    title: str
    status: str = "not_started"
    priority: str = "P2"
    owner: str = "unassigned"
    depends_on: list[str] = field(default_factory=list)
    source_file: str = ""
    effort: str = ""


@dataclass
class BoardStats:
    total: int = 0
    completed: int = 0
    in_progress: int = 0
    blocked: int = 0
    not_started: int = 0
    ready: int = 0
    p0_pending: int = 0
    p1_pending: int = 0
    missing_deps: list[tuple[str, str]] = field(default_factory=list)
    files_scanned: int = 0
    files_with_tasks: int = 0


# ═════════════════════════════════════════════════════════════
#  PASS 1 — Discovery & Parsing
# ═════════════════════════════════════════════════════════════

def discover_files(root: Path) -> list[Path]:
    """Find all TODO markdown files, skipping irrelevant directories."""
    found: set[Path] = set()
    for pattern in TODO_GLOBS:
        for p in root.glob(pattern):
            if any(part in EXCLUDE_PARTS for part in p.relative_to(root).parts):
                continue
            if p.is_file():
                found.add(p)
    return sorted(found)


def parse_all(files: list[Path], root: Path) -> dict[str, Task]:
    """Parse every file and merge into a single global task registry."""
    registry: dict[str, Task] = {}
    for path in files:
        try:
            for tid, task in _parse_file(path, root).items():
                if tid in registry:
                    _log.warning(
                        "Duplicate ID %s — keeping version from %s, "
                        "discarding version from %s",
                        tid, registry[tid].source_file, task.source_file,
                    )
                    continue
                registry[tid] = task
        except Exception:
            _log.exception("Failed to parse %s", path.name)
    return registry


# ── Single-file parser ────────────────────────────────────────

def _parse_file(path: Path, root: Path) -> dict[str, Task]:
    content = path.read_text(encoding="utf-8", errors="replace")
    rel = str(path.relative_to(root))
    tasks: dict[str, Task] = {}

    for task_id, raw_title, block in _extract_blocks(content):
        meta = _try_yaml(block) or _parse_legacy(block)
        status = meta.get("status", "") or _status_from_title(raw_title)
        tasks[task_id] = Task(
            id=task_id,
            title=_clean_title(raw_title)[:60],
            status=_normalize_status(status),
            priority=_norm_priority(meta.get("priority", "P2")),
            owner=meta.get("owner", "unassigned").strip(),
            depends_on=_to_dep_list(
                meta.get("depends_on", meta.get("dependencies", [])),
            ),
            source_file=rel,
            effort=meta.get("effort", ""),
        )
    return tasks


def _extract_blocks(content: str) -> list[tuple[str, str, str]]:
    """Yield (task_id, raw_title, content_block) for each task header."""
    lines = content.split("\n")
    results: list[tuple[str, str, str]] = []
    cur_id: str | None = None
    cur_title = ""
    cur_level = 0
    buf: list[str] = []

    for line in lines:
        m = _TASK_HDR.match(line)
        if m:
            if cur_id:
                results.append((cur_id, cur_title, "\n".join(buf)))
            cur_level, cur_id, cur_title = len(m.group(1)), m.group(2), m.group(3).strip()
            buf = []
            continue
        if cur_id is None:
            continue
        # Stop at same-or-higher-level header that isn't a task
        hdr = re.match(r"^(#{1,4})\s+\S", line)
        if hdr and len(hdr.group(1)) <= cur_level:
            results.append((cur_id, cur_title, "\n".join(buf)))
            cur_id = None
            buf = []
            continue
        buf.append(line)

    if cur_id:
        results.append((cur_id, cur_title, "\n".join(buf)))
    return results


# ── YAML frontmatter parser (zero deps) ──────────────────────

def _try_yaml(block: str) -> dict[str, Any] | None:
    m = re.search(r"```ya?ml\s*\n(.*?)```", block, re.DOTALL)
    if not m:
        return None
    return _simple_yaml(m.group(1))


def _simple_yaml(text: str) -> dict[str, Any]:
    """Parse flat key: value YAML subset (strings + bracket-lists)."""
    out: dict[str, Any] = {}
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, val = line.partition(":")
        if not sep:
            continue
        key, val = key.strip(), val.strip()
        if val.startswith("[") and val.endswith("]"):
            out[key] = [i.strip().strip("'\"") for i in val[1:-1].split(",") if i.strip()]
        elif len(val) >= 2 and val[0] in "\"'" and val[-1] == val[0]:
            out[key] = val[1:-1]
        else:
            out[key] = val
    return out


# ── Legacy metadata parser (bold-text / bullet-list) ─────────

def _parse_legacy(block: str) -> dict[str, Any]:
    meta: dict[str, Any] = {}

    # Status
    for pat in (
        r"[-*]\s*(?:✅|⬜|\[.?\])\s*\*\*Status[:\s]*\*\*\s*(.+)",
        r"\*\*Status[:\s]*\*\*\s*(.+)",
    ):
        m = re.search(pat, block, re.I)
        if m:
            meta["status"] = m.group(1).strip().rstrip("*").strip()
            break

    # Priority
    m = re.search(r"\*\*Priority[:\s]*\*\*\s*(P[0-3])", block, re.I)
    if m:
        meta["priority"] = m.group(1)

    # Owner
    m = re.search(r"\*\*Owner[:\s]*\*\*\s*([^\n*]+)", block, re.I)
    if m:
        meta["owner"] = m.group(1).strip()

    # Dependencies
    for pat in (
        r"\*\*Depends?\s*(?:On|_on)?[:\s]*\*\*\s*([^\n]+)",
        r"\*\*Dependencies?[:\s]*\*\*\s*([^\n]+)",
    ):
        m = re.search(pat, block, re.I)
        if m:
            v = m.group(1).strip()
            if v.lower() not in {"none", "n/a", "-", "na", ""}:
                meta["depends_on"] = _ID_RE.findall(v)
            break

    # Effort
    m = re.search(r"\*\*Effort[:\s]*\*\*\s*(\d+h?)", block, re.I)
    if m:
        meta["effort"] = m.group(1)

    return meta


# ── Normalizers ───────────────────────────────────────────────

def _normalize_status(raw: str) -> str:
    if not raw:
        return "not_started"
    low = raw.lower().strip()
    if low in _STATUS_CANON:
        return _STATUS_CANON[low]
    for key, val in _STATUS_CANON.items():
        if key in low:
            return val
    return "not_started"


def _status_from_title(title: str) -> str:
    if "✅" in title or "COMPLETED" in title.upper():
        return "completed"
    if "⬜" in title:
        return "not_started"
    if "🔄" in title:
        return "in_progress"
    if "⏸" in title:
        return "blocked"
    return ""


def _clean_title(title: str) -> str:
    for m in ("✅ COMPLETED", "✅COMPLETED", "COMPLETED", "✅", "⬜", "🔄", "⏸️", "⏸"):
        title = title.replace(m, "")
    return title.strip()


def _norm_priority(raw: str) -> str:
    raw = raw.strip().upper()
    return raw if re.match(r"^P[0-3]$", raw) else "P2"


def _to_dep_list(raw: Any) -> list[str]:
    if isinstance(raw, list):
        return [d.strip() for d in raw if d.strip()]
    if isinstance(raw, str):
        if raw.lower() in {"none", "n/a", "-", ""}:
            return []
        return _ID_RE.findall(raw)
    return []


# ═════════════════════════════════════════════════════════════
#  PASS 2 — Global Dependency Resolution
# ═════════════════════════════════════════════════════════════

def resolve(tasks: dict[str, Task]) -> BoardStats:
    """Wire up cross-file deps, auto-block, and compute board stats."""
    stats = BoardStats(total=len(tasks))

    # Build suffix index for fuzzy dep matching (WLB002 → TODO-WLB002)
    suffix_idx: dict[str, str] = {}
    for tid in tasks:
        if tid.startswith("TODO-"):
            suffix_idx[tid[5:]] = tid

    # Normalize short dep IDs to full IDs
    for t in tasks.values():
        t.depends_on = [
            suffix_idx.get(d, d) if d not in tasks else d
            for d in t.depends_on
        ]

    # Detect unresolved deps & auto-block on incomplete deps
    for t in tasks.values():
        for dep in t.depends_on:
            if dep not in tasks:
                stats.missing_deps.append((t.id, dep))
        if t.status not in {"completed", "blocked"}:
            if any(
                dep in tasks and tasks[dep].status != "completed"
                for dep in t.depends_on
            ):
                t.status = "blocked"

    # Tally
    for t in tasks.values():
        match t.status:
            case "completed":
                stats.completed += 1
            case "blocked":
                stats.blocked += 1
            case "in_progress":
                stats.in_progress += 1
            case "ready":
                stats.ready += 1
            case _:
                stats.not_started += 1
        if t.status != "completed":
            if t.priority == "P0":
                stats.p0_pending += 1
            elif t.priority == "P1":
                stats.p1_pending += 1

    return stats


# ═════════════════════════════════════════════════════════════
#  Ready-Task Filter — Actionable tickets for agent assignment
# ═════════════════════════════════════════════════════════════

def get_ready_tasks(tasks: dict[str, Task]) -> list[Task]:
    """Return tasks that are immediately actionable (non-blocked, deps met).

    After resolve() has run, any task whose dependencies are unsatisfied is
    already marked 'blocked'. So ready = status in {not_started, ready} which
    means every dependency is completed (or the task has no deps at all).
    Results are sorted by priority (P0 first) then by ID.
    """
    actionable = [
        t for t in tasks.values()
        if t.status in {"not_started", "ready"}
    ]
    _PRIO_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    actionable.sort(key=lambda t: (_PRIO_ORDER.get(t.priority, 9), t.id))
    return actionable


def render_ready_terminal(ready: list[Task]) -> None:
    """Compact, agent-friendly terminal listing of assignable tasks."""
    if not ready:
        print("No actionable tasks. All tasks are blocked, in-progress, or completed.")
        return
    try:
        from rich import box
        from rich.console import Console
        from rich.table import Table

        c = Console()
        c.print(f"\n[bold green]🟢 READY FOR ASSIGNMENT — {len(ready)} task(s)[/]\n")
        tbl = Table(box=box.SIMPLE, padding=(0, 1))
        tbl.add_column("ID", style="bold cyan", no_wrap=True)
        tbl.add_column("Priority", justify="center")
        tbl.add_column("Title")
        tbl.add_column("Owner")
        tbl.add_column("Effort", justify="right")
        tbl.add_column("File", style="dim")
        _P_STYLE = {"P0": "[bold red]P0[/]", "P1": "[yellow]P1[/]", "P2": "[dim]P2[/]", "P3": "[dim]P3[/]"}
        for t in ready:
            tbl.add_row(
                t.id,
                _P_STYLE.get(t.priority, t.priority),
                t.title[:50],
                t.owner,
                t.effort or "-",
                t.source_file,
            )
        c.print(tbl)
        c.print()
    except ImportError:
        # Plain fallback
        print(f"\nREADY FOR ASSIGNMENT — {len(ready)} task(s)")
        print("-" * 80)
        print(f"{'ID':<16} {'Pri':<4} {'Title':<45} {'Owner':<15}")
        print("-" * 80)
        for t in ready:
            print(f"{t.id:<16} {t.priority:<4} {t.title[:45]:<45} {t.owner:<15}")
        print()


def render_ready_json(ready: list[Task]) -> None:
    """Machine-readable JSON list of assignable tasks."""
    out = {
        "ready_count": len(ready),
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "priority": t.priority,
                "owner": t.owner,
                "effort": t.effort,
                "depends_on": t.depends_on,
                "source_file": t.source_file,
            }
            for t in ready
        ],
    }
    print(json.dumps(out, indent=2))


# ═════════════════════════════════════════════════════════════
#  Terminal Output (rich → plain fallback)
# ═════════════════════════════════════════════════════════════

def render_terminal(tasks: dict[str, Task], stats: BoardStats) -> None:
    try:
        _render_rich(tasks, stats)
    except ImportError:
        _render_plain(tasks, stats)


def _render_rich(tasks: dict[str, Task], stats: BoardStats) -> None:
    from rich import box
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    c = Console()
    pct = f"{stats.completed / stats.total * 100:.1f}" if stats.total else "0.0"

    # Banner
    c.print()
    c.print(Panel.fit(
        f"[bold cyan] PROJECT BOARD[/]\n"
        f"[dim]{stats.total} tasks · {stats.files_with_tasks} files · {pct}% done[/]",
        border_style="cyan",
    ))

    # Summary
    tbl = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
    tbl.add_column("Metric", style="bold")
    tbl.add_column("Value", justify="right")
    tbl.add_row("✅ Completed", f"[green]{stats.completed}[/]")
    tbl.add_row("� Ready", f"[green]{stats.ready}[/]")
    tbl.add_row("�🔵 Not Started", f"[blue]{stats.not_started}[/]")
    tbl.add_row("🔄 In Progress", f"[yellow]{stats.in_progress}[/]")
    tbl.add_row("🔴 Blocked", f"[red]{stats.blocked}[/]")
    tbl.add_row("🔴 P0 Pending", f"[bold red]{stats.p0_pending}[/]")
    tbl.add_row("🟠 P1 Pending", f"[bold yellow]{stats.p1_pending}[/]")
    c.print(tbl)

    # P0 table
    p0 = sorted(
        (t for t in tasks.values() if t.priority == "P0" and t.status != "completed"),
        key=lambda x: x.id,
    )
    if p0:
        c.print(f"\n[bold red]🔴 P0 CRITICAL — {len(p0)} pending[/]")
        pt = Table(box=box.SIMPLE, padding=(0, 1))
        pt.add_column("ID", style="bold red", no_wrap=True)
        pt.add_column("Title")
        pt.add_column("Status", justify="center")
        pt.add_column("Owner")
        pt.add_column("File", style="dim")
        _SS = {
            "blocked": "[red]BLOCKED[/]", "not_started": "[yellow]TODO[/]",
            "in_progress": "[cyan]WIP[/]", "ready": "[green]READY[/]",
        }
        for t in p0:
            pt.add_row(t.id, t.title[:45], _SS.get(t.status, t.status), t.owner, t.source_file)
        c.print(pt)

    # Blocked detail
    blocked = sorted(
        (t for t in tasks.values() if t.status == "blocked"),
        key=lambda x: x.id,
    )
    if blocked:
        c.print(f"\n[bold yellow]⏸ BLOCKED — {len(blocked)} tasks[/]")
        for t in blocked:
            blockers = [d for d in t.depends_on if d in tasks and tasks[d].status != "completed"]
            ext = [f"{d}?" for d in t.depends_on if d not in tasks]
            c.print(f"  [dim]{t.id}[/] ← {', '.join(blockers + ext)}")

    # Missing deps
    if stats.missing_deps:
        c.print(f"\n[bold magenta]⚠ UNRESOLVED DEPS — {len(stats.missing_deps)}[/]")
        for tid, did in stats.missing_deps[:15]:
            c.print(f"  [dim]{tid}[/] → [bold]{did}[/] (not found)")
        if len(stats.missing_deps) > 15:
            c.print(f"  [dim]… +{len(stats.missing_deps) - 15} more[/]")

    # Per-file breakdown
    files: dict[str, dict[str, int]] = {}
    for t in tasks.values():
        files.setdefault(t.source_file, {"total": 0, "done": 0})
        files[t.source_file]["total"] += 1
        if t.status == "completed":
            files[t.source_file]["done"] += 1
    ft = Table(title="Per-File Progress", box=box.ROUNDED)
    ft.add_column("File", style="cyan")
    ft.add_column("Done", justify="right")
    ft.add_column("Total", justify="right")
    ft.add_column("%", justify="right")
    for f, cnts in sorted(files.items()):
        p = cnts["done"] / cnts["total"] * 100 if cnts["total"] else 0
        sty = "green" if p == 100 else "yellow" if p > 50 else "red"
        ft.add_row(f, str(cnts["done"]), str(cnts["total"]), f"[{sty}]{p:.0f}%[/]")
    c.print()
    c.print(ft)
    c.print()


def _render_plain(tasks: dict[str, Task], stats: BoardStats) -> None:
    pct = f"{stats.completed / stats.total * 100:.1f}" if stats.total else "0.0"
    print(f"\n{'=' * 52}")
    print(f"   PROJECT BOARD  ({stats.total} tasks, {pct}% done)")
    print(f"{'=' * 52}")
    print(f"  ✅ Completed   {stats.completed}")
    print(f"  📋 Not Started {stats.not_started}")
    print(f"  🔄 In Progress {stats.in_progress}")
    print(f"  🔴 Blocked     {stats.blocked}")
    print(f"  🔴 P0 Pending  {stats.p0_pending}")
    print(f"  🟠 P1 Pending  {stats.p1_pending}")
    print(f"{'-' * 52}")

    p0 = [t for t in tasks.values() if t.priority == "P0" and t.status != "completed"]
    if p0:
        print(f"\n  P0 CRITICAL ({len(p0)}):")
        for t in sorted(p0, key=lambda x: x.id):
            print(f"    {t.id}: {t.title[:40]}  [{t.status}]  @{t.owner}")

    if stats.missing_deps:
        print(f"\n  UNRESOLVED DEPS ({len(stats.missing_deps)}):")
        for tid, did in stats.missing_deps[:15]:
            print(f"    {tid} → {did}")
    print()


# ═════════════════════════════════════════════════════════════
#  HTML / Mermaid Output
# ═════════════════════════════════════════════════════════════

def generate_html(tasks: dict[str, Task], stats: BoardStats) -> str:
    mermaid = _build_mermaid(tasks)
    rows = _build_rows(tasks)
    pct = f"{stats.completed / stats.total * 100:.1f}" if stats.total else "0.0"

    html = _HTML_TEMPLATE
    replacements = {
        "%%TOTAL%%": str(stats.total),
        "%%COMPLETED%%": str(stats.completed),
        "%%IN_PROGRESS%%": str(stats.in_progress),
        "%%BLOCKED%%": str(stats.blocked),
        "%%NOT_STARTED%%": str(stats.not_started),
        "%%P0%%": str(stats.p0_pending),
        "%%P1%%": str(stats.p1_pending),
        "%%PROGRESS%%": pct,
        "%%MISSING%%": str(len(stats.missing_deps)),
        "%%MERMAID%%": mermaid,
        "%%ROWS%%": rows,
    }
    for k, v in replacements.items():
        html = html.replace(k, v)
    return html


def _safe_node(raw: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "_", raw)


def _build_mermaid(tasks: dict[str, Task]) -> str:
    lines = ["graph TD"]

    # Group by source file into subgraphs
    by_file: dict[str, list[Task]] = {}
    for t in tasks.values():
        by_file.setdefault(t.source_file, []).append(t)

    for fp, ftasks in sorted(by_file.items()):
        label = Path(fp).stem.replace("_", " ").replace("-", " ").title()
        sg = _safe_node(fp)
        lines.append(f'    subgraph {sg}["{label}"]')
        for t in sorted(ftasks, key=lambda x: x.id):
            safe_t = (
                t.title
                .replace('"', "'")
                .replace("<", "‹")
                .replace(">", "›")
                .replace("&", "+")
            )
            icon = {"P0": "🔴", "P1": "🟠", "P2": "🟢", "P3": "⚪"}.get(t.priority, "")
            nid = _safe_node(t.id)
            lines.append(f'        {nid}["{icon} {t.id}<br/>{safe_t}"]:::{t.status}')
        lines.append("    end")

    lines.append("")

    # Dependency edges
    seen_ext: set[str] = set()
    for t in tasks.values():
        for dep in t.depends_on:
            src, dst = _safe_node(dep), _safe_node(t.id)
            if dep in tasks:
                lines.append(f"    {src} --> {dst}")
            elif dep not in seen_ext:
                lines.append(f'    {src}["{dep} ❓"]:::missing')
                lines.append(f"    {src} -.-> {dst}")
                seen_ext.add(dep)
            else:
                lines.append(f"    {src} -.-> {dst}")

    # Class definitions
    lines.append("")
    lines.append('    classDef completed fill:#dcfce7,stroke:#166534,stroke-width:2px,color:#14532d')
    lines.append('    classDef not_started fill:#dbeafe,stroke:#1e40af,stroke-width:2px,color:#1e3a8a')
    lines.append('    classDef in_progress fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#92400e')
    lines.append('    classDef blocked fill:#fee2e2,stroke:#991b1b,stroke-width:2px,color:#7f1d1d')
    lines.append('    classDef ready fill:#d1fae5,stroke:#059669,stroke-width:2px,color:#065f46')
    lines.append('    classDef missing fill:#f3f4f6,stroke:#6b7280,stroke-width:1px,stroke-dasharray:5,color:#374151')
    return "\n".join(lines)


def _build_rows(tasks: dict[str, Task]) -> str:
    badges = {
        "completed": '<span class="badge done">✅ Done</span>',
        "not_started": '<span class="badge todo">📋 Todo</span>',
        "in_progress": '<span class="badge wip">🔄 WIP</span>',
        "blocked": '<span class="badge blocked">🔴 Blocked</span>',
        "ready": '<span class="badge ready">🟢 Ready</span>',
    }
    pri_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    rows: list[str] = []
    for t in sorted(tasks.values(), key=lambda x: (pri_order.get(x.priority, 9), x.id)):
        badge = badges.get(t.status, t.status)
        deps = ", ".join(t.depends_on) or "—"
        rows.append(
            f"<tr data-priority='{t.priority}' data-status='{t.status}'>"
            f"<td><b>{t.id}</b></td><td>{t.title}</td><td>{t.priority}</td>"
            f"<td>{badge}</td><td>{t.owner}</td><td>{deps}</td>"
            f"<td class='file'>{t.source_file}</td></tr>"
        )
    return "\n            ".join(rows)


# ─── HTML Template ────────────────────────────────────────────

_HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title> Project Board</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:#0f172a;color:#e2e8f0;min-height:100vh}
header{background:#1e293b;border-bottom:1px solid #334155;padding:14px 24px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100;flex-wrap:wrap;gap:10px}
header h1{font-size:1.4rem;color:#38bdf8;white-space:nowrap}
.stats-bar{display:flex;gap:20px;align-items:center;flex-wrap:wrap}
.stat{text-align:center;min-width:48px}
.stat-value{font-size:1.4rem;font-weight:bold}
.stat-label{font-size:.7rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px}
.controls{display:flex;gap:6px}
.controls button{background:#334155;color:#e2e8f0;border:1px solid #475569;border-radius:6px;padding:5px 11px;cursor:pointer;font-size:1rem;transition:background .15s}
.controls button:hover{background:#475569}
.tabs{display:flex;border-bottom:1px solid #334155;background:#1e293b}
.tab{padding:11px 22px;cursor:pointer;border-bottom:2px solid transparent;color:#94a3b8;font-size:.9rem;user-select:none;transition:color .15s}
.tab.active{color:#38bdf8;border-bottom-color:#38bdf8}
.tab:hover{color:#e2e8f0}
#graph-container{overflow:hidden;height:calc(100vh - 130px);position:relative;cursor:grab;display:block}
#graph-container:active{cursor:grabbing}
#graph-inner{transform-origin:0 0;padding:40px;display:inline-block;min-width:100%}
#task-table-container{display:none;padding:0}
#filter-bar{padding:10px 16px;background:#1e293b;display:flex;gap:8px;flex-wrap:wrap;border-bottom:1px solid #334155;align-items:center}
.filter-btn{background:#334155;color:#e2e8f0;border:1px solid #475569;border-radius:20px;padding:4px 14px;cursor:pointer;font-size:.8rem;transition:all .15s}
.filter-btn.active{background:#38bdf8;color:#0f172a;border-color:#38bdf8}
.filter-btn:hover{border-color:#38bdf8}
.table-scroll{overflow-x:auto;max-height:calc(100vh - 185px);overflow-y:auto}
table{width:100%;border-collapse:collapse;font-size:.83rem}
th{background:#1e293b;padding:9px 12px;text-align:left;position:sticky;top:0;border-bottom:2px solid #38bdf8;color:#38bdf8;z-index:2;cursor:pointer}
th:hover{color:#22d3ee}
td{padding:7px 12px;border-bottom:1px solid #1e293b}
tr:hover td{background:rgba(56,189,248,.06)}
.badge{padding:2px 8px;border-radius:4px;font-size:.73rem;font-weight:600;white-space:nowrap}
.badge.done{background:#166534;color:#dcfce7}
.badge.ready{background:#1e40af;color:#dbeafe}
.badge.wip{background:#d97706;color:#fef3c7}
.badge.blocked{background:#991b1b;color:#fee2e2}
.file{color:#64748b;font-size:.73rem}
.progress-bar{width:180px;height:7px;background:#334155;border-radius:4px;overflow:hidden}
.progress-fill{height:100%;background:linear-gradient(90deg,#38bdf8,#22d3ee);border-radius:4px}
.search-box{background:#334155;border:1px solid #475569;border-radius:6px;padding:5px 12px;color:#e2e8f0;font-size:.85rem;width:220px;outline:none;transition:border-color .15s}
.search-box:focus{border-color:#38bdf8}
.search-box::placeholder{color:#64748b}
footer{background:#1e293b;border-top:1px solid #334155;padding:8px 24px;text-align:center;font-size:.7rem;color:#64748b}
@media(max-width:768px){header{flex-direction:column;gap:8px}.stats-bar{gap:10px}.search-box{width:100%}}
</style>
</head>
<body>
<header>
  <h1> Board</h1>
  <div class="stats-bar">
    <div class="stat"><div class="stat-value" style="color:#22c55e">%%COMPLETED%%</div><div class="stat-label">Done</div></div>
    <div class="stat"><div class="stat-value" style="color:#eab308">%%IN_PROGRESS%%</div><div class="stat-label">WIP</div></div>
    <div class="stat"><div class="stat-value" style="color:#ef4444">%%BLOCKED%%</div><div class="stat-label">Blocked</div></div>
    <div class="stat"><div class="stat-value" style="color:#3b82f6">%%NOT_STARTED%%</div><div class="stat-label">Todo</div></div>
    <div class="stat">
      <div class="stat-value">%%PROGRESS%%%</div>
      <div class="progress-bar"><div class="progress-fill" style="width:%%PROGRESS%%%;max-width:100%"></div></div>
    </div>
  </div>
  <div class="controls">
    <button onclick="zoomIn()" title="Zoom In">+</button>
    <button onclick="zoomOut()" title="Zoom Out">&minus;</button>
    <button onclick="resetView()" title="Reset View">&#x27F2;</button>
    <button onclick="fitView()" title="Fit to Screen">&#x2B1C;</button>
  </div>
</header>
<div class="tabs">
  <div class="tab active" onclick="showView('graph')">&#x1F4CA; Dependency Graph</div>
  <div class="tab" onclick="showView('table')">&#x1F4CB; Task List (%%TOTAL%%)</div>
</div>
<div id="graph-container">
  <div id="graph-inner">
    <pre class="mermaid">
%%MERMAID%%
    </pre>
  </div>
</div>
<div id="task-table-container">
  <div id="filter-bar">
    <input class="search-box" type="text" placeholder="Search tasks..." oninput="filterTable()">
    <button class="filter-btn active" data-filter="all" onclick="setFilter(this)">All (%%TOTAL%%)</button>
    <button class="filter-btn" data-filter="P0" onclick="setFilter(this)">P0 (%%P0%%)</button>
    <button class="filter-btn" data-filter="P1" onclick="setFilter(this)">P1 (%%P1%%)</button>
    <button class="filter-btn" data-filter="blocked" onclick="setFilter(this)">Blocked (%%BLOCKED%%)</button>
    <button class="filter-btn" data-filter="completed" onclick="setFilter(this)">Done (%%COMPLETED%%)</button>
  </div>
  <div class="table-scroll">
    <table>
      <thead><tr>
        <th onclick="sortTable(0)">ID</th>
        <th onclick="sortTable(1)">Title</th>
        <th onclick="sortTable(2)">Priority</th>
        <th onclick="sortTable(3)">Status</th>
        <th onclick="sortTable(4)">Owner</th>
        <th>Deps</th>
        <th onclick="sortTable(6)">File</th>
      </tr></thead>
      <tbody>
            %%ROWS%%
      </tbody>
    </table>
  </div>
</div>
<footer> Project Board &middot; Read-only snapshot &middot; Source files are never modified</footer>
<script>
mermaid.initialize({startOnLoad:true,theme:'dark',flowchart:{useMaxWidth:false,htmlLabels:true,curve:'basis',padding:15},securityLevel:'loose',maxTextSize:500000});

function showView(v){
  var g=document.getElementById('graph-container'),t=document.getElementById('task-table-container'),tabs=document.querySelectorAll('.tab');
  if(v==='graph'){g.style.display='block';t.style.display='none';tabs[0].classList.add('active');tabs[1].classList.remove('active')}
  else{g.style.display='none';t.style.display='block';tabs[0].classList.remove('active');tabs[1].classList.add('active')}
}

var container=document.getElementById('graph-container'),inner=document.getElementById('graph-inner');
var scale=1,tx=0,ty=0,drag=false,sx,sy;
function upd(){inner.style.transform='translate('+tx+'px,'+ty+'px) scale('+scale+')'}
function zoomIn(){scale=Math.min(scale*1.25,6);upd()}
function zoomOut(){scale=Math.max(scale/1.25,.05);upd()}
function resetView(){scale=1;tx=0;ty=0;upd()}
function fitView(){var svg=inner.querySelector('svg');if(!svg)return;var r=svg.getBoundingClientRect();scale=Math.min(container.clientWidth/(r.width||1),container.clientHeight/(r.height||1),.95);tx=10;ty=10;upd()}
container.addEventListener('wheel',function(e){e.preventDefault();scale=Math.max(.05,Math.min(6,scale*(e.deltaY>0?.88:1.12)));upd()},{passive:false});
container.addEventListener('mousedown',function(e){drag=true;sx=e.clientX-tx;sy=e.clientY-ty});
container.addEventListener('mousemove',function(e){if(!drag)return;tx=e.clientX-sx;ty=e.clientY-sy;upd()});
container.addEventListener('mouseup',function(){drag=false});
container.addEventListener('mouseleave',function(){drag=false});
document.addEventListener('keydown',function(e){if(e.target.tagName==='INPUT')return;if(e.key==='+'||e.key==='=')zoomIn();if(e.key==='-')zoomOut();if(e.key==='0')resetView()});
setTimeout(fitView,1500);

var activeFilter='all';
function setFilter(btn){
  document.querySelectorAll('.filter-btn').forEach(function(b){b.classList.remove('active')});
  btn.classList.add('active');activeFilter=btn.dataset.filter;filterTable();
}
function filterTable(){
  var q=(document.querySelector('.search-box')||{}).value||'';q=q.toLowerCase();
  document.querySelectorAll('tbody tr').forEach(function(tr){
    var mf=activeFilter==='all'||(activeFilter==='blocked'?tr.dataset.status==='blocked':activeFilter==='completed'?tr.dataset.status==='completed':tr.dataset.priority===activeFilter);
    var ms=!q||tr.textContent.toLowerCase().indexOf(q)!==-1;
    tr.style.display=(mf&&ms)?'':'none';
  });
}
var sortDir={};
function sortTable(col){
  var tbody=document.querySelector('tbody'),rows=Array.from(tbody.querySelectorAll('tr'));
  sortDir[col]=!sortDir[col];var dir=sortDir[col]?1:-1;
  rows.sort(function(a,b){var av=a.children[col].textContent.trim(),bv=b.children[col].textContent.trim();return av<bv?-dir:av>bv?dir:0});
  rows.forEach(function(r){tbody.appendChild(r)});
}
</script>
</body>
</html>
"""


# ═════════════════════════════════════════════════════════════
#  CLI Entry Point
# ═════════════════════════════════════════════════════════════

def main() -> None:
    args = set(sys.argv[1:])

    if args & {"-h", "--help", "help"}:
        print(__doc__)
        return

    files = discover_files(ROOT)

    if args & {"--list", "-l"}:
        print(f"Found {len(files)} TODO files:")
        for f in files:
            print(f"   {f.relative_to(ROOT)}")
        return

    # ── Pass 1: Parse ──
    tasks = parse_all(files, ROOT)
    if not tasks:
        print("No structured tasks found in any TODO file.")
        return

    # ── Pass 2: Resolve ──
    stats = resolve(tasks)
    stats.files_scanned = len(files)
    stats.files_with_tasks = len({t.source_file for t in tasks.values()})

    # ── Ready-task filter (--ready) ──
    if "--ready" in args:
        ready = get_ready_tasks(tasks)
        if "--json" in args:
            render_ready_json(ready)
        else:
            render_ready_terminal(ready)
        return

    # ── JSON dump ──
    if "--json" in args:
        out = {
            "tasks": {tid: asdict(t) for tid, t in tasks.items()},
            "stats": asdict(stats),
        }
        print(json.dumps(out, indent=2, default=str))
        return

    # ── Outputs ──
    want_terminal = "--html" not in args
    want_html = "--terminal" not in args

    if want_terminal:
        render_terminal(tasks, stats)

    if want_html:
        html = generate_html(tasks, stats)
        out_path = ROOT / "index.html"
        out_path.write_text(html, encoding="utf-8")
        size = out_path.stat().st_size
        msg = f"Board written to index.html ({size:,} bytes)"
        try:
            from rich.console import Console
            Console().print(f"[green]{msg}[/]")
        except ImportError:
            print(msg)


if __name__ == "__main__":
    main()
