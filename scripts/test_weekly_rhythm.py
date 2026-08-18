#!/usr/bin/env python3
"""Behavior checks for the public weekly-rhythm skill bundle."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
SCRIPT = ROOT / "skills" / "weekly-planning" / "scripts" / "living_week.py"
SPEC = importlib.util.spec_from_file_location("living_week", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    with tempfile.TemporaryDirectory() as temp:
        workspace = Path(temp)
        w34 = MODULE.week_context(date(2026, 8, 18), workspace, "reports")
        w35 = MODULE.week_context(date(2026, 8, 24), workspace, "reports")
        w53 = MODULE.week_context(date(2027, 1, 1), workspace, "reports")
        require(w34["week_label"] == "W34", "18 Aug 2026 must resolve to W34")
        require(w35["week_label"] == "W35", "24 Aug 2026 must resolve to W35")
        require(w53["week_label"] == "W53", "1 Jan 2027 must resolve to ISO W53")
        require(len(w34["days"]) == 7, "context must contain the full ISO week")
        require(
            w34["habit_storage_key"] == "personal-corp.plan.W34.wealth.v1",
            "habit state must use a week-scoped key",
        )

        html = MODULE.render(w34)
        require(html.count("<!-- daily:updated -->") == 1, "updated marker missing")
        require(html.count("<!-- daily:kanban -->") == 1, "kanban marker missing")
        require(html.count("<!-- daily:day-slice -->") == 1, "compat marker missing")
        require(html.count('data-day="2026-08-') == 7, "render must contain seven days")
        require(html.count("data-habit=") == 14, "render must contain fourteen habits")
        private_home = "/" + "Users/"
        private_prefix = "corp" + "-"
        require(private_home not in html and private_prefix not in html, "private paths leaked")

    print("OK: weekly rhythm W34/W35/W53, seven days, 14 habits, public boundary")


if __name__ == "__main__":
    main()
