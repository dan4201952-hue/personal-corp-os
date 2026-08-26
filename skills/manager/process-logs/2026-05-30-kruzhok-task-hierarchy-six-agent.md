# 2026-05-30 — Kruzhok task hierarchy

## Original Correction

User asked to align Kruzhok tasks and add a manager skill product template. The
required hierarchy mirrors mentoring: track epic, lesson issues as first-level
children, and recording/transcript/deck/messages/LMS as children of the exact
lesson.

## Mode

Skill patch + GitHub issue alignment through six-agent critique loop.

Target skill:
- `/Users/ris/.claude/skills/manager/SKILL.md`
- `/Users/ris/.claude/skills/manager/templates/kruzhok-product-task-hierarchy.md`

Research source routing: internal.

## Explorer Cycle

| id | tool | role | source lane | verdict | parent action |
|---|---|---|---|---|---|
| 019e78f2-9784-7d71-8b8c-e056ae261401 | multi_agent_v1 | skill-pattern | manager skill files | Create `templates/kruzhok-product-task-hierarchy.md`; link from `SKILL.md`. | Applied. |
| 019e78f2-a978-7001-bb71-150462320c78 | multi_agent_v1 | GitHub hierarchy | `hq#170` and related issues | Root epic exists; `#308` orphan; `#310/#312` active under root. | Used for sync plan. |
| 019e78f2-b918-7c62-a942-19ef9e5eac23 | multi_agent_v1 | product-domain | HQ product/funnel files | Owner boundaries: HQ canon, `hsl-mozg` funnel, `teach-vibecoding` lesson source, `cohorts` runtime, `corp-sales` cash. | Added to template. |
| 019e78f2-c873-7570-a768-2c1506ab9be1 | multi_agent_v1 | lesson-source | `teach-vibecoding` stream paths | Lesson parent should own source/live/post-live/runtime state; children are surfaces. | Added checklist/gates. |
| 019e78f2-d694-7393-aa48-4262e4cab501 | multi_agent_v1 | GitHub ops | Sub-issues API | Use REST numeric `.id` and `replace_parent=true` for reparenting. | Used in GitHub sync. |
| 019e78f2-e46b-7c93-b033-3ab822e55c4e | multi_agent_v1 | process-log | manager process logs | Use strict table schema in `process-logs/`. | This log created. |

## Researchers

| id | tool | role | verdict | parent action |
|---|---|---|---|---|
| 019e78f4-e42d-73b3-8840-e82481750521 | multi_agent_v1 | target user | Template needs owner, freshness, weekly visibility, and done gates. | Hardened rules. |
| 019e78f4-f3bd-73a3-9de7-3e193d6349ed | multi_agent_v1 | domain method | HQ routes; owner repos hold execution facts. | Added owner boundaries. |
| 019e78f5-1397-7431-b1a1-153964355d0f | multi_agent_v1 | language | Use `lesson/L<N>` for Kruzhok and reserve `session/S<N>` for mentoring. | Added title rule. |
| 019e78f5-2246-76c3-9731-82c0d0b21b59 | multi_agent_v1 | source fidelity | Do not mark done from adjacent proof; LMS, video, Telegram, cash, funnel have separate gates. | Added gates. |
| 019e78f5-30cd-7a63-af56-54dd2198475a | multi_agent_v1 | format hierarchy | Manager output should show a tree and gaps. | Added output tree shape. |
| 019e78f5-3e61-7d71-97d0-3c82100dbce0 | multi_agent_v1 | process architect | Add Kruzhok source boundaries, title pattern, update rules, validation gate. | Applied in `SKILL.md` and template. |

## Implementation Changes

- Added `templates/kruzhok-product-task-hierarchy.md`.
- Updated `SKILL.md` with Kruzhok hook, title pattern, update/create rules, output tree shape, common mistakes, and `epic` root domain.
- Created lesson parents under `hq#170`: `teach-vibecoding#315` L1, `teach-vibecoding#316` L3, `teach-vibecoding#317` L4.
- Reframed `teach-vibecoding#308` as L2 lesson parent, attached under `hq#170`, removed stale `lesson-state:not-started`.
- Reparented existing artifacts:
  - L1: `hq#176`, `hq#177`, `hq#178`, `teach-vibecoding#302` under `teach-vibecoding#315`.
  - L2: `teach-vibecoding#303` under `teach-vibecoding#308`.
  - L3: `teach-vibecoding#304`, `teach-vibecoding#312` under `teach-vibecoding#316`.
  - L4: `teach-vibecoding#305` under `teach-vibecoding#317`.
- Renamed lesson artifact issues to include `L1/L3/L4`.
- Replaced raw Zoom share URL in `teach-vibecoding#308` bot comment with safe evidence text.

## Critic Pass

| id | tool | role | verdict | parent action |
|---|---|---|---|---|
| 019e78fa-a86d-7610-a869-d4039c68ac8e | multi_agent_v1 | target-user critic | Request mostly satisfied; fix titles, stale labels, root title duplication, old flat children. | Applied title/label/template fixes; left generic old children for separate cleanup. |
| 019e78fa-b906-75a0-a20e-bf4c5d134cb7 | multi_agent_v1 | domain critic | Tree improved; stale labels/gates and generic direct children remain. | Fixed label/title drift; kept generic cleanup explicit. |
| 019e78fa-c9e2-76f3-a06f-c5d2e8313ef5 | multi_agent_v1 | language critic | Use `launch/funnel`, avoid lesson artifacts as `content`, add `epic` domain. | Applied. |
| 019e78fa-dcaa-73e1-9e10-bafc15e15b02 | multi_agent_v1 | source-fidelity critic | `#308` body clean but old comment had raw Zoom URL. | Replaced comment body with safe evidence. |
| 019e78fa-ed02-75d1-9fa7-afbfe9397291 | multi_agent_v1 | format critic | Add tree output and legacy direct children block. | Applied. |
| 019e78fb-01e7-7921-b0e2-7a71edd0ee39 | multi_agent_v1 | process critic | Need log, parent evidence, dirty worktree note. | Applied here and verified. |

## Validation

- `tasks.md` read before GitHub writes; current week W22 from 2026-05-30.
- Parent evidence checked through GitHub Sub-issues API:
  - `teach-vibecoding#315/#308/#316/#317` parent = `hq#170`.
  - `teach-vibecoding#312/#304` parent = `teach-vibecoding#316`.
  - `teach-vibecoding#303` parent = `teach-vibecoding#308`.
  - `hq#176` parent = `teach-vibecoding#315`.
- `teach-vibecoding#308` labels after fix: `type:lesson`, `lesson-state:processed`, `program:cohort`, `W21`.
- `teach-vibecoding#308` raw Zoom URL removed from body and old bot comment.
- Dirty worktree note: `/Users/ris/.claude` had pre-existing `M skills/manager/SKILL.md` and untracked `skills/manager/process-logs/2026-05-29-label-drift-six-agent.md`; this run added the template and this process log.

Final status: complete-after-recheck.
