# 2026-05-30 — Kruzhok title prefix removal recheck

## Intake

- Trigger: founder correction: visible `product:`, `epic:`, `content:`, `infra:`, `ops:` prefixes make GitHub tasks harder to scan.
- Mode: full six-agent critique loop.
- Target skill: `/Users/ris/.claude/skills/manager/SKILL.md`.
- Target template: `/Users/ris/.claude/skills/manager/templates/kruzhok-product-task-hierarchy.md`.
- Target live issue titles: visible Kruzhok #11 lesson/tree titles and directly visible Kruzhok support children.
- Source routing: internal.

## Explorer Cycle

| Agent | Lane | Verdict | Parent action |
|---|---|---|---|
| Russell `019e793a-2c81-71e1-9fc4-1cc9fb9f8182` | skill/template scope | rule should change globally in manager; live rename should be narrow for Kruzhok | patch manager/title convention and Kruzhok template |
| Feynman `019e793a-2cf5-7ce0-a79d-e0657a21550c` | GitHub surface | remove prefixes from visible Kruzhok titles; preserve product/lesson/topic/status | rename targeted issues |
| Hubble `019e793a-2d7e-7b10-ba0f-f24187a1d804` | process/validation | `tasks.md` was read before `gh`; log path and validation commands identified | use this log and gates |

## Researcher Cycle

| Agent | Role | Verdict | Parent action |
|---|---|---|---|
| Rawls `019e793c-7f2e-7013-a675-09b692998c51` | target user | visible domain prefixes hurt scanning; titles should start with object | make `{object} — {action}` the visible formula |
| Darwin `019e793c-7fd7-7af2-80c4-fbd7cc3c5eb9` | domain method | type/routing must move to metadata: labels, parent tree, body, Projects | strengthen non-title metadata rule |
| Planck `019e793c-804b-7d92-aef7-64213f238d69` | language | first token should be recognizable object: `Кружок #11 L3`, `Валентин S2`, `Sportmaster` | rewrite examples |
| Hilbert `019e793c-80d1-7743-ad84-29c0217bc59f` | source fidelity | removing prefixes is safe only if object/date/LN and parent/project remain | add anti-regression checks |
| Jason `019e793c-81a4-7760-ba4f-cc052e70d3f9` | format/tree | tree should render without prefix noise | patch output shape and live titles |
| Euclid `019e793c-8313-7b11-ad20-1b1bb9358a0e` | process architect | accept old prefixes as legacy input; canonical output is unprefixed | document legacy alias behavior |

## Implementation Plan

- Patch manager title convention: canonical visible title has no domain prefix.
- Patch Kruzhok title patterns and examples: no `epic:`, `product:`, `content:`, `infra:`, `ops:`.
- Keep parent/W-label/Project/type/lifecycle checks as metadata contract.
- Rename live visible Kruzhok issue titles only; do not bulk-rename unrelated historical tracks.

## Validation Gates

- `git diff --check` on touched manager files.
- frontmatter parse: `name == manager`.
- `rg -n "^(.*` patterns?` not used; grep for `(epic|product|content|infra|ops): Кружок` in active skill/template should return no title examples.
- Live GitHub title check for `hq#170`, `teach-vibecoding#315/#308/#316/#317/#302/#303/#304/#305/#306/#310/#312`.
- Six critic rows after implementation.

## Critic Cycle

| Agent | Role | Verdict | Parent action |
|---|---|---|---|
| Curie `019e7942-139b-76b2-aac7-96bc6fc2822e` | target user | blocker: visible tree still had `product:` and nested `infra:` / `ops:` children | removed prefixes from `hq#3` and `hsl-mozg#159/#125/#133/#151` |
| Godel `019e7942-1463-7350-9e9c-55afafcd7905` | domain method | blocker: stale `mentoring:` and `ops:` creation examples remained | patched mentoring/session and missing-epic examples |
| Maxwell `019e7942-14df-7be1-b4f7-677839db24cb` | language/title | partial pass; stale examples and active title polish remained | patched manager examples and renamed active titles |
| Nietzsche `019e7942-15e8-7e80-a55d-c2d7d9fd7dfc` | source fidelity | blocker: active current titles still had `content:`, `handoff:`, `product:`, `ops:` | renamed active Colvir/PC/Kruzhok/mentoring titles; body fidelity on Colvir S5 left out of scope |
| Newton `019e7942-16e1-7a01-830f-dad1c6ed7db4` | format/tree | pass on tree render | no action |
| Hypatia `019e7942-17e1-7370-95fe-98611a24aec3` | process/log | blocker: process log incomplete and stale generic examples remained | filled critic/final rows; patched generic examples |

## Final Fix Pass

- Patched manager stale examples:
  - epic examples no longer teach `epic:` or `ops:` as canonical visible prefixes.
  - mentoring session creation examples now use `<person> S<N> — ...`.
  - missing-epic proposal now uses `<X> — overview`.
  - Sportmaster/Smena output examples no longer use lower-case prefix titles.
- Patched Kruzhok template title examples and output shape to be prefix-free.
- Patched secondary GitHub issue skill `/Users/ris/.codex/skills/gh-issues/skill.md` so it no longer teaches `ops:`, `content:`, or `feat:` as canonical visible title prefixes.
- Renamed visible GitHub titles across current Kruzhok #11 tree and active manager-renamed issues so titles start with the recognizable object.
- Preserved metadata contract: W-label, parent tree, type/lifecycle labels, Projects, and body fields carry machine routing.
- Skipped body rewrite for `teach-colder-vibecoding#4`: critic identified stale body details, but the current user request is title prefix removal; changing delivery/source body would be a separate manager sync.

## Final Status

complete-after-recheck.

Final checks:

- `tasks.md` was read before GitHub writes.
- `git diff --check` passed for touched manager files.
- frontmatter check passed: `name == manager`.
- active manager/template grep has no canonical Kruzhok title examples with `product: Кружок`, `epic: Кружок`, `content: Кружок`, `infra: Кружок`, or `ops: Кружок`.
- live title check passed for current visible Kruzhok and active manager-renamed issues listed in this run.
- secondary `gh-issues` skill grep now contains old prefixes only in the new anti-pattern row.
