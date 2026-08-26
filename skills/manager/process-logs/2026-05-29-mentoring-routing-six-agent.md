# 2026-05-29 — manager mentoring routing fix

## Original correction

Founder pointed out a manager skill failure: mentoring work collapsed profile, S1 delivery pieces, S2 booking, money facts, and stale "close deal" task language into the wrong GitHub issue shape.

## Mode

Skill patch through six-agent critique loop. Target skill: `/Users/ris/.claude/skills/manager/SKILL.md`.

## Six researcher summaries

1. Target user: founder cannot see what to do next when `track`, `S1`, `S2`, delivery artifacts, and deal status are mixed.
2. Domain/method: mentoring delivery needs a session hierarchy; each session has prep/live/post-delivery, while CRM owns relationship and money.
3. Language: phrases like "close deal", paid amounts, and package counts in delivery issues create wrong operational cues.
4. Source/fidelity: money and package facts must remain in CRM/ledger; GitHub issues may point to CRM slug but must not duplicate amounts.
5. Format: manager needs an explicit mentoring plan shape showing track overview, session issue, delivery children, and CRM owner.
6. Skill/process: add a durable manager rule, templates, title patterns, common mistakes, and anti-patterns.

## Skill changes

- Added "Mentoring source boundaries".
- Added "Mentoring title pattern".
- Added "Mentoring update/create rules".
- Added "Mentoring body template".
- Added mentoring-specific common mistakes and anti-patterns.
- Added a mentoring-specific write-plan example.

## Six critic verdicts

1. Target user: pass after patch; plan now makes S2 issue creation visible.
2. Domain editor: pass; S1 delivery stays under S1 and S2 gets its own issue.
3. Language/meta: one fix needed; "закрыть delivery" sounded like close-deal language.
4. Source/privacy: pass; amounts are banned from delivery issues and routed to CRM/ledger.
5. Format: pass; the new tables are scannable and close to existing skill style.
6. Process/log/git: pass with note that unrelated dirty files in `/Users/ris/.claude` must not be committed.

## Final fix pass

Applied:
- Replaced "закрыть delivery" with "доставить материалы".

Skipped:
- Broad translation of existing English in the old skill. Out of scope for this targeted fix.

## Anti-regression checks

- Checked that mentoring rules mention separate `S<N>` session issues.
- Checked that S1 leftovers stay under S1.
- Checked that S2 calendar booking requires a separate S2 issue.
- Checked that payment amounts, package counts, paid/won, and close-deal language are banned from mentoring delivery tasks.
- Ran `git diff --check -- SKILL.md`: pass.

## KB decision

Skip external KB update. This is a local manager skill rule.

## Git state

Unrelated dirty files exist under `/Users/ris/.claude`; only `skills/manager/SKILL.md` and this process log are in scope.

Final status: complete-after-recheck.

## Follow-up — W-label drift

### Original correction

Founder pointed out a remaining manager drift: Valentin mentoring tasks were not reliably surfaced with the current week tag in manager output.

### Mode

Skill patch through six-agent critique loop. Target skill: `/Users/ris/.claude/skills/manager/SKILL.md`.

### Explorer cycle

- Explorer 1 (`019e74d0-7a6e-7ad2-af4a-dc1689559ff7`, `multi_agent_v1`, skill-pattern, internal): target sections are `W-label rules`, `Mentoring update/create rules`, mentoring write-plan example, and write report; action: patch skill examples and mentoring-specific guard.
- Explorer 2 (`019e74d0-8785-7070-aa41-edf35cd7b776`, `multi_agent_v1`, local source-of-truth, internal): `tasks.md` and W22 files resolve Valentin S2 on `2026-05-29` to `W22`; action: use W22 in examples.
- Explorer 3 (`019e74d0-992e-7633-84d3-fdea158044af`, `multi_agent_v1`, GitHub evidence, internal): live GitHub has `teach-vibecoding#283` open with labels `W20`, `W22`; `teach-vibecoding#314` open with label `W22` and parent `#283`; action: no issue write needed, skill anti-regression only.
- Explorer 4 (`019e74d0-a5ab-76f2-a774-e000a13ddeaa`, `multi_agent_v1`, validation, internal): no formal validator; action: run `git diff --check` and grep guardrails.
- Explorer 5 (`019e74d0-b75d-7d10-8508-5080d3cc063e`, `multi_agent_v1`, process-log, internal): append follow-up in this process log; action: keep role details here and user report short.
- Explorer 6 (`019e74d0-c35a-75a0-a262-9125e45ed255`, `multi_agent_v1`, scope, internal): patch limited to manager `SKILL.md`; action: do not touch AGENTS/CLAUDE or legacy mentoring docs.

### Six researcher summaries

1. Target user (`019e74d1-e594-7e73-8e3b-9762c8f49b78`): founder-facing output must surface week mismatch and concrete action.
2. Domain/method (`019e74d1-f09b-7bd0-a832-6c4a260575ce`): W-rollover belongs to active work items: track overview, exact `S<N>` session, and delivery children.
3. Language (`019e74d1-ffb4-71b1-bb55-7944838b9d10`): use Russian term `Расхождение недели`; keep `W22` as technical token.
4. Source/fidelity (`019e74d2-0cdf-7dd1-a3e4-f10310f3b235`): verify `tasks.md`, actual GitHub labels, parent epic, and keep money facts in CRM/ledger.
5. Format/output (`019e74d2-17ec-7fd3-ab88-f615a3da16fa`): mentoring plan and reports must show W-label status, including missing/drift cases.
6. Process architect (`019e74d2-2250-7123-91dd-b41dd6133189`): add dated mentoring sessions rule, checklist, common mistake, and anti-regression grep.

### Skill changes

- Added `Dated mentoring sessions` under `W-label rules`.
- Added mentoring weekly check before mentoring sync.
- Added common mistake for copying W-label from profile/S1/example to a new session.
- Updated mentoring write-plan example with `2026-05-29` and `W22`.
- Updated result/read-mode examples to show W-label status and missing-label drift.

### Six critic verdicts

1. Target user (`019e74d3-dcd8-70a1-86d3-e9671ae7c37b`): 8/10. Fix applied: read-mode now computes and surfaces mentoring week drift; log no longer pending.
2. Domain editor (`019e74d3-eb1a-74f1-ba3b-a8bd143eba72`): 8/10. Fix applied: standing authorization no longer allows closing by observed outcome alone; W-label source uses deterministic date/week fallback.
3. Language/title/meta (`019e74d3-f95c-7af3-834f-fedd93fda3a3`): 6/10. Fixes applied in scoped areas: `Treck` typo, founder-facing examples for body updates, Russian labels for `Расхождение недели` and `Проверка трека`. Broad translation of legacy skill text skipped as separate hygiene work.
4. Source/fidelity/privacy (`019e74d4-04d3-7f53-bb3e-e74a999997c7`): 7/10. Fix applied: Valentin example now uses placeholders instead of inaccurate live issue numbers; commercial terms removed from GitHub example and routed to CRM slug.
5. Format/output (`019e74d4-10a9-7022-aca4-7ca7a08c004c`): 8/10. Fix applied: generic plan/report/read examples expose W-label state per issue, including skipped issue and per-issue W-label mini-list.
6. Process/log/git (`019e74d4-24a7-7cd3-b8c4-4e0e4d7bb3ea`): 7/10. Fix applied: critic verdicts and validation results recorded; commit scope remains limited to `skills/manager/SKILL.md` and this process log.

### Final fix pass

Applied:
- Added read-mode W-label drift check for mentoring matches.
- Clarified current-week resolution and `DD.MM` year inference.
- Tightened write boundary: W-label write requires `tasks.md` pre-flight, live issue read, and parent check.
- Removed comment-first and commercial-term examples from generic write plan.
- Changed Valentin example to placeholders and explicit `2026-05-29` / `W22`.
- Added per-issue W-label state to write report, skipped issue output, and read-mode health check.

Skipped:
- Broad translation of all legacy English in `manager/SKILL.md`; out of scope for this targeted drift fix.

### Validation results

- `git -C /Users/ris/.claude diff --check -- skills/manager/SKILL.md skills/manager/process-logs/2026-05-29-mentoring-routing-six-agent.md`: pass.
- `rg -n "Датированные mentoring sessions|Расхождение недели|2026-05-29|W22|Copying W-label|Read mode ничего не пишет|Проверка трека" /Users/ris/.claude/skills/manager/SKILL.md`: pass.
- `ruby -e 'require "psych"; p Psych.load_file(ARGV[0]).fetch("name")' /Users/ris/.claude/skills/manager/SKILL.md`: pass (`manager`).
- Live evidence rechecked: `teach-vibecoding#283` labels `W20`, `W22`; `teach-vibecoding#314` label `W22`.

### KB decision

Skip external KB update. This is a local manager skill rule.

### Git state

Unrelated dirty files exist under `/Users/ris/.claude`; commit scope is only `skills/manager/SKILL.md` and `skills/manager/process-logs/2026-05-29-mentoring-routing-six-agent.md`.

Final status: complete-after-recheck.
