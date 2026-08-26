# 2026-05-30 — Kruzhok task hierarchy recheck 2

## Intake

- Trigger: founder correction after first alignment: stale L1/L2 state remains visible; lesson epic title must include the topic.
- Mode: full six-agent critique loop.
- Target skill: `/Users/ris/.claude/skills/manager/SKILL.md`.
- Target template: `/Users/ris/.claude/skills/manager/templates/kruzhok-product-task-hierarchy.md`.
- Target live issues: `hq#170`, `teach-vibecoding#315/#308/#316/#317`, and stale/artifact children `#302/#304/#312`.
- Required source: `0_hq/tasks.md` before any GitHub writes.

## Explorer Cycle

| Agent | Lane | Verdict | Parent action |
|---|---|---|---|
| Locke `019e7904-c9fe-7350-aa60-eda4a0ebeb59` | source-of-truth | `tasks.md` says L3 held 2026-05-28; active tail is `teach-vibecoding#312`; L1/L2 must not look active | update root and lesson statuses |
| Franklin `019e7904-dd2b-7131-97de-ef10efbc08c0` | runtime/publication | L1/L2 delivery proof is strong; L3 lacks authenticated runtime/Telegram proof | keep L3 open |
| Bernoulli `019e7904-efbb-7951-b857-42a65d48da51` | GitHub tree | `hq#170` has correct lesson parents, but L1/L3/L4 labels/statuses drift | label and lifecycle cleanup |
| Linnaeus `019e7905-01d0-7971-a98c-8237d21c1a7b` | skill consistency | add dated lesson lifecycle classes and stale-active anti-pattern | patch manager/template |
| Sartre `019e7905-19ea-7e63-9c25-403c89632e49` | GitHub operations | safe scoped edits are titles, labels, bodies, closing only completed scope | execute scoped writes |
| Goodall `019e7905-2bc6-7442-a640-52e821640998` | process evidence | add sibling process log with explorer/researcher/critic/final gates | this file |

## Researcher Cycle

| Agent | Role | Verdict | Parent action |
|---|---|---|---|
| Erdos `019e7907-c846-7092-8eb2-03cc24fc6840` | target user | first screen must show one active tail: L3 -> `#312`; L1/L2 history; L4 planned | lifecycle grouping |
| Laplace `019e7907-de30-7271-8531-6824b359933b` | domain/method | hierarchy is `hq#170 -> lesson parent -> delivery children`; title must include topic | title rule |
| Popper `019e7907-f6d7-7ab0-a795-72fc59cada22` | language | parent titles lacking topic cause L3/L4 confusion | rename lesson parents |
| Plato `019e7908-1516-7100-ac9b-3cd4e81b70d5` | source fidelity | L1/L2 safely delivered; L3 not safely closed; L4 has numbering/topic conflict | conservative close/open |
| Tesla `019e7908-28d0-7152-9468-99d80c50fe49` | format/hierarchy | report tree by historical/current/planned buckets | output shape patch |
| Mencius `019e7908-3a32-7170-b90d-9b7ce6342aa3` | process architect | add Project placement status-lane validation for active current-week issues | Project rule patch |

## Implementation

- Patched `SKILL.md` with topic-required Kruzhok lesson titles, lifecycle checks, and Project status-lane validation.
- Patched `templates/kruzhok-product-task-hierarchy.md` with lesson lifecycle classes and stale-active anti-patterns.
- Planned GitHub writes:
  - retitle lesson parents with topics;
  - close L1 parent/artifact only where delivery proof exists;
  - keep L3 open with active tail `#312`;
  - keep L4 planned with `topic TBD / date TBD`;
  - update `hq#170` body to show current tail and historical lessons.

## Critic Cycle

| Agent | Role | Verdict | Parent action |
|---|---|---|---|
| Ampere `019e790f-64f5-7732-8adf-f963818c62d4` | user readability | lesson tree now reads correctly, but active Project status lanes are empty | logged Project drift; GraphQL limit blocked status edit |
| Gauss `019e790f-65cd-7e62-87e8-0bc2caa3aa35` | lifecycle | L1/L2 consistent; L3 semantic label correct; L4 evidence conflict needs decision | kept L4 planned/TBD because `tasks.md` says next live not checked and source has numbering conflict |
| Helmholtz `019e790f-6696-7d30-9280-98e4ab62e00f` | title language | hard title requirement passed; L4 title risk too close to L3 | changed L4 title to explicit `topic TBD / финальный урок` |
| Wegener `019e790f-6754-76f2-b23f-d05e0d320d3a` | source fidelity | pass; L3 not overclaimed, L4 not delivered, L1/L2 supported | no issue body change required beyond L4 conflict wording |
| Bacon `019e790f-680b-7b31-bcfa-b4da924fcea5` | hierarchy | lesson artifacts are no longer direct children; legacy direct children still create tree noise | root body names legacy direct children and current L3 tail |
| Euler `019e790f-691e-7a01-bff4-3f2a531ce56c` | process validation | critic rows/final status missing | filled this section and final status |

## Final Fix Pass

- `teach-vibecoding#317` title changed to `product: Кружок #11 L4 — topic TBD / финальный урок (date TBD)`.
- `teach-vibecoding#317` body now says topic/date are not verified in the 2026-05-30 task snapshot.
- `teach-vibecoding#305` closed as legacy/superseded preview artifact.
- `hq#170` body updated to reflect L4 `topic TBD`, closed legacy preview, and L3 as the only current post-live tail.
- Project status lane drift remains for `teach-vibecoding#316/#312/#317`: they are present in `ris © corp`, but GraphQL rate limit blocked `project item-edit` before status could be filled.

## Validation Gates

- `tasks.md` read before `gh` writes: done.
- `git diff --check` on touched manager files.
- frontmatter parse: `name == manager`.
- grep gates: `Kruzhok product hierarchy`, `Kruzhok update/create rules`, `Дерево трека`, `Project placement`, `Расхождение Project`, `lesson topic`, `Lesson Lifecycle Classes`.
- live GitHub check: root -> lesson -> artifact tree and lesson parent titles include topics.
- active tail check: only L3/`#312` remains current after L1/L2 cleanup.

## Final Status

complete-after-recheck for skill/template and issue descriptions.

Known follow-up: set Project status lanes for active/planned issues after GraphQL rate limit reset:

- `teach-vibecoding#316`: `ris © corp=In progress`; domain Project status should show active/delivered tail, not Todo.
- `teach-vibecoding#312`: `ris © corp=In progress` or ready lane; domain Project status should show active tail.
- `teach-vibecoding#317`: planned/backlog status or Done only after L4 source/date reconciliation.
