# 2026-05-30 — manager related tasks + HQ drift

run_id: manager-related-tasks-hq-drift-2026-05-30
started_at: 2026-05-30 11:24 ART
mode: skill-patch + artifact patch
source_routing: internal
target_skill_path: /Users/ris/.claude/skills/manager/SKILL.md
hq_owner_paths:
- /Users/ris/Documents/obsidian/0_hq/tasks/W22/2026-05-30.md
- /Users/ris/Documents/obsidian/0_hq/tasks/W22/README.md

## Original request

Founder confirmed HQ Drift Sentinel findings as real drift and asked to update manager so tasks can show related tasks/links without duplication. User explicitly linked:
- /Users/ris/.claude/skills/manager/SKILL.md
- /Users/ris/.agents/skills/six-agent-critique-loop/SKILL.md

## Failure label

Related task links were not governed: manager could either hide useful connected issues or duplicate hierarchy in markdown. HQ task drift also allowed a day-plan line to lag behind GitHub/CRM source truth.

## Explorer cycle

| id | tool | role | source lane | verdict | parent action |
|---|---|---|---|---|---|
| 019e794d-cb59-7571-ba3e-8a59b7b10f55 | multi_agent_v1 explorer | skill/pattern discovery | internal | add Related rule near Parent epic rules and templates | applied in manager skill |
| 019e794d-db41-7800-8937-094808655f90 | multi_agent_v1 explorer | hierarchy source-of-truth | internal | hierarchy stays GitHub Sub-issues API; Related is context only | applied |
| 019e794d-fb8c-76b2-877c-871e93d00449 | multi_agent_v1 explorer | HQ wording | internal | Sportmaster daily wording stale after crm#27 docs state | applied in HQ day/week files |
| 019e794e-0c09-7a70-8abc-8ddefd721bd1 | multi_agent_v1 explorer | duplication risk | internal | Related must be replaced from live search, no task statuses/checklists | applied |
| 019e794e-1b71-7223-bde3-090e9fe9869e | multi_agent_v1 explorer | validation lane | internal | add grep gates for parent markdown, Sub-issues API, Related/HQ drift | used in validation |
| 019e794e-2bcd-7653-ab57-0c3ac5732bdc | multi_agent_v1 explorer | process-log/gate | internal | durable log fields and completion gates listed | this log |

## Researcher cycle

| id | role | source lane | verdict | parent action |
|---|---|---|---|---|
| 019e794f-6a62-7440-a043-f08d626ec3fb | target user | internal | founder needs readable repo#N title refs, parent/project visibility, no bare issue numbers | issue-ref and output rules retained |
| 019e794f-780a-7e21-979b-e6e9c703dc91 | domain/method | internal | four layers: Sub-issues, W-label, Projects, body | reinforced in Related and Project gates |
| 019e794f-88e0-7ba1-8ffa-2c157cb1ce53 | language | internal | avoid hierarchy wording inside Related; each link gets one reason | wording patched |
| 019e794f-a397-7013-bad5-7907613780d9 | source/fidelity | internal | live-verify Related refs and remove stale/private refs before body write | added live verification and public safety rule |
| 019e794f-b18a-7602-82b0-11460a7bc7e8 | format | internal | optional Related block, max 3 bullets plus verification, replace wholesale | applied |
| 019e794f-c293-7bf3-b94c-7ab71866abfc | process architect | internal | patch Sources, Pre-flight, Update/Create, Common mistakes | applied |

## Synthesis matrix

| failure | desired behavior | manager section | validation gate |
|---|---|---|---|
| Related links become duplicate hierarchy | Related is context only; parent remains Sub-issues API | Parent epic rules; Related issues | no allowed markdown Parent/Epic fields |
| Related block becomes mini-board | max 3 refs, no status/checklists, replace from live search | Search; body templates; Common mistakes | rg Related + template review |
| Stale related refs leak old state | live-read title/state/labels/parent/project before body write | Related issues | related-links gate |
| HQ plan drifts from issue truth | active task rows require repo#N; missing issue = drift | Sources; Pre-flight | rg Расхождение HQ tasks |
| Project drift overclaimed | projectItems/item status required before claiming fixed | Project evidence commands; HQ files | downgraded HQ wording |

## Skill changes

- Added daily plan source layer and HQ task drift guard.
- Added Project evidence commands and status-lane caveat.
- Added Related issues rule: context-only, max 3 refs, live-verified, public-safe.
- Added optional Related blocks in body templates after core task content.
- Added anti-patterns for related-as-match, manual Related task lists, duplicated hierarchy, and HQ tasks without issue refs.

## HQ artifact changes

- /Users/ris/Documents/obsidian/0_hq/tasks/W22/2026-05-30.md
  - Sportmaster strategy next step updated from stale Roman/email check to Anna/IP docs package.
  - Valentin S2 send added as teach-vibecoding#314 with needs_confirmation.
  - Project repair wording downgraded to placement-only until projectItems/status evidence exists.
- /Users/ris/Documents/obsidian/0_hq/tasks/W22/README.md
  - Same Sportmaster/Valentin drift reflected in W22 context.
  - Project visibility wording downgraded to placement/status-lane caveat.

## Critic cycle

| id | role | verdict | parent action |
|---|---|---|---|
| 019e7951-ca39-7420-b6ca-a1929b0adb69 | target user | Related looked mandatory; HQ guard conflicted with tasks read-only; Project fallback needed | Related optional, HQ guard clarified, existing Project unknown rule retained |
| 019e7951-dbb5-7fd0-b3f1-790533a8f523 | domain/process | Related should not trigger W/Project fixes unless primary; current-week Project wording too broad | patched |
| 019e7951-f60d-7351-8b55-0c510deae363 | language | issue-ref format conflict, English placeholders, hierarchy-like words, typo | patched |
| 019e7952-056c-7cf2-bda3-dde444e92b97 | source/privacy | public repo path/CRM leak risk; duplicate Related block risk | public safety note + remove old Related before insert |
| 019e7952-14a2-7771-8043-051c923367ac | format | Related block placement and max-lines ambiguity | moved after core content; clarified max bullets |
| 019e7952-2656-7d73-9a06-847cd27bff03 | process/log/git | Project gate overclaimed in HQ files; no archive edits; diff check passed | HQ wording downgraded; Project evidence commands added |

## Final fix pass

Applied:
- Optional Related block with omit rule.
- Safe public-repo pointer rule.
- Related refs remove/report unless primary/touched.
- Project drift wording downgraded in HQ task files.
- Issue-ref format unified to `repo#N «title»`.
- `Workinging epics` fixed.

Skipped:
- Full Project status-lane repair. This run was scoped to read-only drift update + skill patch; live Project mutation was not required.

## Validation

Commands run:

```bash
rg -n "HQ task drift|Расхождение HQ tasks|Related issues|## Related|Смежные задачи|related-links|Project evidence commands|projectItems|status lane pending" /Users/ris/.claude/skills/manager/SKILL.md
rg -n '(Parent|Epic|Belongs to):[[:space:]]*#' /Users/ris/.claude/skills/manager --glob '*.md' | rg -v 'Не использовать|Markdown|Дубликат|дубликат|Anti-pattern|Запрещено|Forbidden|body не содержит' || true
rg -n 'human title|why related|Workinging|prep к встрече|Project-дрифт 30.05 исправлен|Project visibility 30.05|исправлена Project-видимость' /Users/ris/.claude/skills/manager/SKILL.md /Users/ris/Documents/obsidian/0_hq/tasks/W22/2026-05-30.md /Users/ris/Documents/obsidian/0_hq/tasks/W22/README.md || true
git -C /Users/ris/Documents/obsidian/0_hq diff --check
git -C /Users/ris/.claude diff --check
```

Results:
- Related/HQ drift rules found.
- No allowed markdown `Parent: #N` / `Epic: #N` / `Belongs to: #N` fields found.
- No stale wording grep hits after final fix pass.
- `git diff --check` passed for `0_hq` and `.claude`.
- No `_archive/` paths edited.

Skill validator: no dedicated local validator found for this skill; grep and diff-check gates used.
KB decision: skip. This is a manager skill rule, not a KB concept.
Commit: no commit requested.

## Final status

complete-after-recheck
