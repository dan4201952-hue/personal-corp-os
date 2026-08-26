# 2026-05-29 — manager label/project drift fix

## Original correction

Founder reported that label tracking still drifts: Valentin has current-week work but was not visible in the global Ris weekly project. Target skill: `/Users/ris/.claude/skills/manager/SKILL.md`.

## Mode

Full six-agent skill patch. Research source routing: internal + live GitHub. Target artifact is the `manager` skill; user-facing report stays short.

## Explorer cycle

| id | tool | role | prompt scope | source lane | input artifact | verdict | status | output reference | parent action |
|---|---|---|---|---|---|---|---|---|---|
| 019e760a-ffb6-7cf3-893d-3815ec7050e4 | multi_agent_v1 | source routing | owner source and patch points | internal | `SKILL.md` pre-patch | Project placement missing from invariants; live evidence points to `ris © corp` Project #4 | completed | subagent final notification | patched invariant/pre-flight/output |
| 019e760b-0acc-7082-b356-ebbe100eac76 | multi_agent_v1 | live issue evidence | Valentin #283/#314 labels, parent, projectItems | GitHub live | `tasks.md`, `teach-vibecoding#283/#314` | `#283/#314` had W22/parent/domain board but no global weekly board before Project placement fix | completed | subagent final notification | added both to Project #4 |
| 019e760b-14e3-7e21-a3d8-b7f1b7f9c1fa | multi_agent_v1 | GitHub Project commands | Project #4 item-add/status pattern | GitHub live | GitHub Project #4 | Project #4 IDs and `Status=Ready` command pattern verified | completed-after-retry | subagent final notification | used command pattern |
| 019e760b-1fa9-7901-8bea-b2f74ee0931e | multi_agent_v1 | prior-memory pattern | prior Valentin/project drift lessons | memory | memory quick-pass hits | prior mentoring split and projectItems drift are reusable failure class | completed | subagent final notification | patched Project placement rule |
| 019e760b-2a4c-7710-8732-a8bfc536d48e | multi_agent_v1 | skill structure | smallest `manager` patch locations | internal | `SKILL.md` pre-patch | patch points: invariants, pre-flight, standing auth, mentoring check, output tables, mistakes | completed | subagent final notification | applied minimal patch |
| 019e760b-346e-77a0-aee3-2cbe9fc1d054 | multi_agent_v1 | validation/logging | validator/process-log expectations | internal | `/Users/ris/.claude/skills/manager` | no dedicated skill validator; use frontmatter, diff-check, grep gates | completed | subagent final notification | ran validation gates |

## Six researcher rows

| id | tool | role | prompt scope | source lane | input artifact | verdict | status | output reference | parent action |
|---|---|---|---|---|---|---|---|---|---|
| 019e760c-bc09-7211-a33e-e45d787753a3 | multi_agent_v1 | target user researcher | founder visibility failure | internal | `SKILL.md` pre-patch + live drift facts | W-label + parent can still be invisible if absent from `ris © corp`; output must show Project status | completed | subagent final notification | added Project status requirement |
| 019e760c-c6eb-7131-8cb3-8829550cf220 | multi_agent_v1 | domain-method researcher | W-label/parent/domain/global layers | internal | manager rules + GitHub Project model | active issue visibility has four layers: W-label, parent epic, domain board, global Ris weekly board | completed | subagent final notification | added conditional Project invariant |
| 019e760c-d174-7310-8e6b-c888d1f6e663 | multi_agent_v1 | language-output researcher | Russian wording for Project drift | internal | `SKILL.md` output sections | user-facing term is `Расхождение Project`; action is `добавить в Project <name>` | completed | subagent final notification | localized Project drift wording |
| 019e760c-e17d-7151-aca9-a2c1b7db0a75 | multi_agent_v1 | source-fidelity researcher | live verification and privacy boundary | GitHub live + internal | `projectItems`, issue bodies, privacy rules | Project placement must be live-read; do not write money/private CRM/Zoom/payment facts into tasks/Project fields | completed | subagent final notification | added privacy validation and write boundary |
| 019e760c-ec41-7931-8ad2-49cc3a3ffc2c | multi_agent_v1 | format researcher | output table and report slots | internal | `SKILL.md` examples | every active issue row needs adjacent `parent/epic`, `W-label`, and `Project` status | completed | subagent final notification | updated plan/report/table examples |
| 019e760c-fe23-7b03-9be6-9e4e61574ec9 | multi_agent_v1 | process architect researcher | patch points and anti-regression checks | internal | `SKILL.md` structure | add invariant, pre-flight, standing authorization, read-mode `projectItems`, mentoring weekly check, examples, grep | completed | subagent final notification | added validation gates |

## Implementation changes

- Added `Project placement` as the fourth manager invariant.
- Added pre-flight `projectItems` resolution for domain board + `ris © corp` Project #4.
- Extended standing authorization to scoped Project placement writes.
- Added `Расхождение Project` to read mode and mentoring weekly checks.
- Updated write-plan/read-mode/report examples to show `Project`.
- Added common mistake and anti-pattern for treating W-label as enough.
- Fixed live drift: added `teach-vibecoding#283` and `teach-vibecoding#314` to Project #4 `ris © corp`, both `Status=Ready`.

## Critic pass

| id | tool | role | prompt scope | source lane | input artifact | verdict | status | output reference | parent action |
|---|---|---|---|---|---|---|---|---|---|
| 019e760e-d415-7db0-b91a-470bffd66ab6 | multi_agent_v1 | target user critic | original Valentin visibility failure | internal | patched `SKILL.md` | 8/10; patch prevents original failure; report example and log evidence needed fixes | completed | subagent final notification | added Project to report rows; added evidence block |
| 019e760e-de9f-7b22-80bd-a037fe2585d4 | multi_agent_v1 | domain editor critic | Project invariant and standing auth | internal | patched `SKILL.md` | 8/10; Project invariant needed active/current-week guard; standing authorization too broad | completed | subagent final notification | narrowed invariant and Project write boundary |
| 019e760e-e99d-74f0-97d8-a71791201ca9 | multi_agent_v1 | language/meta critic | Russian wording and output labels | internal | patched `SKILL.md` | 7/10; new lines mixed English/Russian and needed `ris © corp` consistency | completed | subagent final notification | localized new lines and backticked `ris © corp` |
| 019e760e-f5e5-7e33-a1e1-d22f61b11480 | multi_agent_v1 | source/privacy critic | privacy and live evidence | GitHub live + internal | patched `SKILL.md` + log | 8/10; no privacy leak; log needed live evidence and Project-write privacy gate | completed | subagent final notification | added evidence and privacy validation |
| 019e760f-003a-7d60-8568-718885f6cb2a | multi_agent_v1 | format critic | examples/table/report format | internal | patched `SKILL.md` | 8/10; read table passed; report rows and new issue Project style needed fixes | completed | subagent final notification | updated report rows and mentoring new-issue bracket |
| 019e760f-0c94-7902-9de5-08a9c36553d9 | multi_agent_v1 | process/log/git critic | six-agent evidence and git/validation | internal | patched `SKILL.md` + log | 6/10; critic rows missing; validation gate wording stale; intended git changes only | completed | subagent final notification | added evidence-contract rows and corrected validation record |

## Narrow re-critique

| id | tool | role | prompt scope | source lane | input artifact | verdict | status | output reference | parent action |
|---|---|---|---|---|---|---|---|---|---|
| 019e7611-4c39-70d2-bbc5-93bd13fc42a3 | multi_agent_v1 | language/format re-critic | Project placement additions after final fix | internal | final `SKILL.md` | PASS; no blocking fixes; original visibility failure closed | completed | subagent final notification | no file change |
| 019e7611-3fb3-71b1-bee8-d063e3df0f2f | multi_agent_v1 | process/log re-critic | process-log evidence contract after final fix | internal | final log draft | FAIL; rows needed source lane/status/output reference/scope | completed | subagent final notification | added complete evidence-contract rows |
| 019e7613-00ea-7092-8bb8-502880588a86 | multi_agent_v1 | final process/log re-critic | evidence rows after final log fix | internal | final process log | PASS; explorer/researcher/critic/re-critic rows satisfy evidence contract; validation and live state match | completed-after-retry | subagent final notification | no file change |

## Final fix pass

Applied:
- Kept `ris © corp` explicit as current global weekly Project.
- Added `Project: неизвестен` fallback when Project cannot be resolved.
- Ensured examples include `Project` in plan, report, and table output.
- Narrowed Project invariant to active/current-week issues.
- Narrowed standing authorization for global Project writes to live-read missing placement in current weekly/day plan.
- Added real critic rows with ids, roles, verdicts, and parent actions.

Skipped:
- Broad rewrite of old English sections in the skill. Out of scope.

## Validation

- Explorer live evidence reported before fix: `teach-vibecoding#283/#314` had `W22` and correct parent/domain board, absent from `ris © corp`.
- Live GitHub after fix: both issues are in Project #4 `ris © corp`, `Status=Ready`.
- Skill validation commands run after patch:
  - `git -C /Users/ris/.claude diff --check -- skills/manager/SKILL.md skills/manager/process-logs/2026-05-29-label-drift-six-agent.md`
  - frontmatter parse for `name: manager`
  - grep gate for `Project placement`, `projectItems`, `Расхождение Project`, `global Ris`, and read-mode `Project` column.
- Live evidence command:
  - `gh project item-list 4 --owner serejaris --format json --limit 1000 | jq -r '.items[] | select((.content.url // "") | test("teach-vibecoding/issues/(283|314)$")) | {title,status,labels,repo:.repository,url:.content.url}'`
- Live evidence after fix:
  - `teach-vibecoding#283`: Project `ris © corp`, Status `Ready`, labels `W20`, `W22`.
  - `teach-vibecoding#314`: Project `ris © corp`, Status `Ready`, labels `W22`.
- Privacy validation:
  - Sensitive grep ran for `api_key|token|secret|password|passcode|payment|paid|ledger|Zoom`; matches are existing policy/prohibition text or safe issue content references, not new leaked secrets.

## KB decision

Skip external KB update. This is a local manager operational rule.

Final status: complete-after-recheck.
