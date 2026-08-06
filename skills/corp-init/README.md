# Corp Init Skill

![Skill illustration](assets/illustration.png)

A skill for initializing or repairing a Personal Corp operating system: HQ files, agent config, daily task plans, GitHub issue workflow, Projects, and corp-* owner routing.

## What It Sets Up

- `AGENTS.md` / `CLAUDE.md` with `Agent Operations Config`
- `tasks.md` as an index plus `tasks/WNN/YYYY-MM-DD.md` day plans
- `okr.md` and `decisions.md`
- GitHub Projects and issue invariants for `manager`
- corp-* owner map and public-surface routing

## Installation

```bash
cp -r skills/corp-init ~/.claude/skills/
```

## Key Rules

- Existing files are patched or extended, never overwritten wholesale.
- Tasks must have GitHub issue pointers before they enter day/week plans.
- `manager` owns GitHub issue writes when available.
- HQ stays short; execution details live in owner repos.

## See Also

- [manager](../manager/) — canonical GitHub issue workflow
- [weekly-planning](../weekly-planning/) — weekly outcomes and day plans
- [weekly-retro](../weekly-retro/) — retrospective and scorecards
- [corp-new](../corp-new/) — register a new corp-* department repo
