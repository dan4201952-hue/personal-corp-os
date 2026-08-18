# Weekly Planning Skill

![Skill illustration](assets/illustration.png)

A Claude Code and Codex skill for structured weekly planning. It turns retro findings and backlog into prioritized outcomes, then renders a living full-week view that the local daily skill can refresh.

## Problem

Weekly planning without structure leads to reactive work, missed priorities, and tasks landing in wrong repos.

## Solution

8-step process: collect tasks → map calendar → group by Area → Eisenhower split → choose outcomes → create issues → add to board → build the living weekly plan.

- **Outcomes, not tasks** — "By Friday, X is true" format
- **Delegation matrix** — founder judgment vs agent execution
- **Correct routing** — issues land in the repo where work happens
- **Config-driven** — reads repos, routing, project ID from CLAUDE.md
- **Full ISO week** — closed past days, highlighted today, and future plan stay visible together
- **Area Explorer** — one kanban source, filtered views, Area goals, and Area-colored cards
- **Private browser habits** — Wealth checkboxes persist under a week-scoped localStorage key

## Installation

```bash
cp -r skills/weekly-planning ~/.claude/skills/
```

## Prerequisites

Run `corp-doctor` first to generate or repair the config block in AGENTS.md / CLAUDE.md, or add manually:

```markdown
## Agent Operations Config
repos:
  - owner/repo-1
  - owner/repo-2
project_id: N
owner: your-github-handle
routing:
  - pattern: "backend, bugs"
    repo: owner/backend-repo
```

## Process

| Step | What happens |
|------|-------------|
| 1. Collect | Scan retro backlog, open issues, calendar, user input |
| 2. Calendar | Map fixed events, deadlines, commitments |
| 3. Group | Organize by surface (product, sales, content, etc.) |
| 4. Eisenhower | Split by urgency/importance + founder vs agent |
| 5. Outcomes | Define measurable results for the week |
| 6. Issues | Create in correct repos with W{NN} label |
| 7. Board | Add all to unified GitHub Project |
| 8. Living plan | Resolve W{NN}, render seven days, Area views, clocks, and Wealth habits |

## Part of Personal Corp Framework

```
corp-doctor → weekly-retro → weekly-planning → local daily refreshes → repeat
```

## See Also

- [corp-doctor](../corp-doctor/) — workspace setup and health repair
- [weekly-retro](../weekly-retro/) — structured weekly retrospective
