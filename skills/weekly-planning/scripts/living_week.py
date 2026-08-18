#!/usr/bin/env python3
"""Resolve an ISO week and create a public-safe living weekly plan."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE = SKILL_DIR / "assets" / "living-week-plan.html"
WEEKDAYS_RU = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")
MONTHS_RU = (
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
)


def parse_date(value: str | None) -> date:
    return date.fromisoformat(value) if value else date.today()


def week_context(today: date, workspace: Path, reports_dir: str) -> dict[str, object]:
    iso_year, week, weekday = today.isocalendar()
    start = today - timedelta(days=weekday - 1)
    end = start + timedelta(days=6)
    label = f"W{week}"
    days = [start + timedelta(days=offset) for offset in range(7)]
    return {
        "today": today.isoformat(),
        "iso_year": iso_year,
        "week": week,
        "week_label": label,
        "week_start": start.isoformat(),
        "week_end": end.isoformat(),
        "week_range": f"{start.day}–{end.day} {MONTHS_RU[end.month - 1]} {end.year}",
        "days": [item.isoformat() for item in days],
        "plan_file": str(workspace / reports_dir / f"{label}-plan.html"),
        "outcomes_file": str(workspace / reports_dir / f"{label}-outcomes.md"),
        "habit_storage_key": f"personal-corp.plan.{label}.wealth.v1",
    }


def render(context: dict[str, object]) -> str:
    html = TEMPLATE.read_text(encoding="utf-8")
    replacements = {
        "{{WEEK_LABEL}}": str(context["week_label"]),
        "{{WEEK_RANGE}}": str(context["week_range"]),
        "{{UPDATED_AT}}": datetime.now().astimezone().isoformat(timespec="minutes"),
        "{{HABIT_STORAGE_KEY}}": str(context["habit_storage_key"]),
    }
    for index, day_value in enumerate(context["days"], start=1):
        day = date.fromisoformat(str(day_value))
        replacements[f"{{{{DAY_{index}_ISO}}}}"] = day.isoformat()
        replacements[f"{{{{DAY_{index}_LABEL}}}}"] = f"{WEEKDAYS_RU[index - 1]} {day:%d.%m}"
    for token, value in replacements.items():
        html = html.replace(token, value)
    return html


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("command", choices=("context", "create"))
    result.add_argument("--date", help="Local date as YYYY-MM-DD")
    result.add_argument("--workspace", default=".")
    result.add_argument("--reports-dir", default="reports")
    result.add_argument("--force", action="store_true")
    result.add_argument("--json", action="store_true")
    return result


def main() -> int:
    args = parser().parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    context = week_context(parse_date(args.date), workspace, args.reports_dir)
    if args.command == "context":
        if args.json:
            print(json.dumps(context, ensure_ascii=False, indent=2))
        else:
            print(f"{context['week_label']} {context['week_start']}..{context['week_end']}")
            print(context["plan_file"])
        return 0

    output = Path(str(context["plan_file"]))
    if output.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing plan: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(context), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
