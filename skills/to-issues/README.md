# To Issues

Splits a plan, spec, or `PRD.md` into independent task files — **tracer bullet** slices: each task goes end-to-end through every layer instead of covering "just the backend". The agent proposes the split, agrees granularity and dependencies with you, then writes markdown into `tasks/`.

**When to call it:** you have a `PRD.md` (or another spec) and need grab-and-go tasks for agents or developers without GitHub Issues.

**What you get:** `tasks/01-slug.md`, `tasks/02-slug.md`, … with *What to build* blocks, an **Acceptance criteria** checklist, and **Depends on** links to other `tasks/…` or `none`.

**Chain:** [grill-me](../grill-me/) → [to-prd](../to-prd/) → **to-issues**.

Русская версия: [README.ru.md](README.ru.md)
