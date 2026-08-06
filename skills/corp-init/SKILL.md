---
name: corp-init
description: >-
  Use when initializing or repairing a Personal Corp / founder-operator
  business operating system: HQ vault, AGENTS.md/CLAUDE.md config, tasks index
  and daily plans, OKR, decisions, corp-* owner repo map, GitHub Projects,
  manager invariants, or when user says "corp init", "init corp",
  "настрой corp", "инициализируй HQ", "обнови операционку бизнеса".
  Replaces the older project-init skill.
---

# Corp Init

Разовая или ремонтная настройка операционной системы Personal Corp: короткий HQ layer, GitHub issues как task truth, `manager` как workflow для задач, дневные планы в `tasks/WNN/YYYY-MM-DD.md`, corp-* owner map и проверяемые источники фактов.

Skill не создаёт "проект с нуля вслепую". Сначала он определяет, есть ли уже HQ/corp контур, затем аккуратно дополняет недостающее.

## Phase 0 — Scope Menu

Первое действие — показать меню и дождаться явного выбора:

```text
Что настраиваем?

1. HQ files — AGENTS.md/CLAUDE.md, tasks index, daily tasks dir, okr.md, decisions.md
2. GitHub operating layer — owner, Projects, issue invariants, labels, parent epic rules
3. Corp owner map — corp-* repos, product repos, public surfaces, source-of-truth routing
4. Repair/audit existing setup — найти расхождения и предложить patch

"всё" = 1 + 2 + 3
```

До ответа пользователя не запускать проверки и не создавать файлы.

## Phase 1 — Verify Existing

Сначала читать, затем спрашивать. Если выбран repair/audit, только читать и показывать diff-план.

### HQ files

```bash
pwd
for d in 0_hq .; do [ -f "$d/AGENTS.md" ] || [ -f "$d/CLAUDE.md" ] && echo "agent dir: $d"; done
find . -maxdepth 3 \( -name AGENTS.md -o -name CLAUDE.md -o -name tasks.md -o -name okr.md -o -name decisions.md \) -print
find ./tasks -maxdepth 2 -type f 2>/dev/null | sort | tail -30
grep -R "Agent Operations Config" -n AGENTS.md CLAUDE.md 0_hq/AGENTS.md 0_hq/CLAUDE.md 2>/dev/null
head -40 tasks.md 2>/dev/null || head -40 0_hq/tasks.md 2>/dev/null
head -30 okr.md 2>/dev/null || head -30 0_hq/okr.md 2>/dev/null
```

Detect:
- primary agent file: prefer `AGENTS.md`; support `CLAUDE.md`; if both regular files exist with divergent content, ask which is primary.
- tasks mode: current mode is `tasks.md` as index plus `tasks/WNN/YYYY-MM-DD.md` day files.
- stale OKR: dated period in the past, "протух", or missing source pointers.
- archive risk: `_archive/` is read-only history; do not create working files there.

### GitHub operating layer

Run preflight before any write:

```bash
gh api user --jq '.login'
gh project list --owner <owner> --limit 50
gh search issues --owner <owner> --state open --json repository,number,title,labels,updatedAt --limit 50
```

If a `manager` skill/config exists, treat it as canonical for:
- W-label convention
- parent epic requirement
- Project placement
- standing write authorization
- day plan sync

Do not use generic GitHub issue helpers when `manager` is available.

### Corp owner map

Check for source-of-truth routing before inventing it:

```bash
find ~/Documents/GitHub -maxdepth 1 -type d -name 'corp-*' | sort
grep -R "Корпоративные отделы\\|Публичные поверхности\\|Где живёт правда\\|Продукты" -n AGENTS.md 0_hq/AGENTS.md 2>/dev/null
```

For each domain, identify:
- owner repo or owner file
- what facts live there
- what must only be linked from HQ
- public surface, if relevant

## Phase 2 — Interview Only Gaps

One question at a time. Do not ask about facts already present in HQ or owner repos.

### HQ questions

Ask only if missing:
- "Где живёт короткий HQ layer? По умолчанию `0_hq/`."
- "Primary agent file: `AGENTS.md`, `CLAUDE.md`, or both with one symlink?"
- "Нужны дневные планы? По умолчанию `tasks.md` index + `tasks/WNN/YYYY-MM-DD.md`."

### GitHub questions

Ask only if missing or ambiguous:
- "GitHub owner for corp operations?"
- "Какая weekly/global Project board является active work board? Нужны номер и человекочитаемое имя."
- "Какие domain Project boards существуют?"
- "Есть ли standing authorization для `manager` writes, или спрашивать каждый раз?"

### Corp routing questions

Ask in owner-map form:
- "Какие 5-10 owner repos реально участвуют в weekly operations?"
- "Какие факты живут только в HQ, а какие в owner repo?"
- "Какие публичные поверхности надо отслеживать: сайт, лендинг, бот, YouTube, Telegram, live pages?"

### OKR questions

If `okr.md` missing or stale, ask:
- period and North Star
- 1-3 Objectives
- 2-4 KRs per Objective
- source pointer per KR: file path, DB query, GitHub issue, dashboard, API
- guard rails
- review cadence

KR without source pointer is a stop condition.

## Phase 3 — Write

Use `apply_patch` for manual file edits. Never overwrite an existing file. Append or patch the smallest section.

### HQ file layout

Create missing structure:

```bash
mkdir -p <hq>/tasks/W{NN} <hq>/retros
touch <hq>/decisions.md
```

`tasks.md` template:

```markdown
# Задачи

Обновлено: <YYYY-MM-DD>
Текущий день: [tasks/WNN/YYYY-MM-DD.md](tasks/WNN/YYYY-MM-DD.md)
Текущая неделя: [tasks/WNN/README.md](tasks/WNN/README.md)

`tasks.md` — входной индекс. Рабочие задачи живут в `tasks/`: неделя -> день.

## Как читать

1. Открыть сегодняшний файл.
2. Если нужен контекст недели — открыть недельный README.
3. Если нужно проверить источник правды — сверить с GitHub-задачами через `manager`.

## Правило

Сюда и в дневные файлы писать только задачи со связанной GitHub-задачей.
```

Day file template:

```markdown
# YYYY-MM-DD · <weekday>

Обновлено: YYYY-MM-DD

## Правило дня

<one sentence>

## P0

1. **<task> (`repo#N`).** <next action>

## P1
```

### Agent Operations Config

Append this block to the primary agent file when missing:

~~~markdown
## Agent Operations Config

### Канонические файлы

```yaml
canonical:
  tasks_index: <hq>/tasks.md
  tasks_dir: <hq>/tasks/
  okr: <hq>/okr.md
  decisions: <hq>/decisions.md
```

### Cadence

- Weekly retro: воскресенье/понедельник через `weekly-retro`
- OKR review: Phase 1.5 каждого retro + end-of-period review
- Monthly snapshot: конец месяца через owner repo for money/sales
~~~

If the project uses `CLAUDE.md`, keep the same content there. If both files are desired, create a symlink only after explicit user approval.

### Corp owner map

Add or repair owner-map sections in the agent file:
- current products and owner files
- money/cash source
- bot/funnel/payment source
- task source and issue rule
- people/CRM source
- public surfaces
- corp-* departments

Keep HQ short. Store execution details in owner repos and link to them.

### GitHub operating layer

If using `manager`, encode these invariants in the setup:
- every active issue has W-label
- every non-epic issue has exactly one parent epic
- active/current-week issues have Project placement and non-empty lane
- real work gets a work-record comment
- day plan sync writes to `tasks/WNN/YYYY-MM-DD.md`
- `tasks.md` is an index; do not bulk mutate it

Do not create legacy `retro:W00` bootstrap labels. Create concrete `WNN` labels only when needed by the current workflow. Do not create track labels for every initiative; use title + parent epic membership.

### OKR

Only write `okr.md` from user-provided objectives and source pointers. If period is stale, preserve old content under `## История` or mark it stale; do not silently replace.

## Phase 4 — Verify

Run the smallest useful checks:

```bash
test -f <hq>/tasks.md
test -d <hq>/tasks
test -f <hq>/decisions.md
grep -n "Agent Operations Config" <hq>/AGENTS.md <hq>/CLAUDE.md 2>/dev/null
grep -n "tasks_index\\|tasks_dir" <hq>/AGENTS.md <hq>/CLAUDE.md 2>/dev/null
find <hq>/tasks -maxdepth 2 -type f | sort | tail -20
```

For GitHub setup, verify live state:

```bash
gh project list --owner <owner> --limit 50
gh search issues --owner <owner> --label "W{NN}" --state open --json repository,number,title,labels --limit 50
```

Report:
- created/changed files
- detected existing canon
- unresolved gaps
- next skill to run (`manager`, `weekly-planning`, or `weekly-retro`)

## Stop Conditions

- no explicit Phase 0 scope
- both `AGENTS.md` and `CLAUDE.md` are different regular files and no primary is chosen
- writing inside `_archive/`
- creating a task without a GitHub issue pointer
- KR without source-of-truth pointer
- unknown GitHub owner or Project but user requested GitHub writes
- no suitable parent epic for a new active issue
- public repo privacy risk
- attempt to overwrite existing files wholesale

## Related Skills

- `manager` — canonical GitHub issue workflow and day-plan sync
- `weekly-planning` — writes weekly outcomes and day plans
- `weekly-retro` — closes the loop and fills outcomes scorecards
- `corp-new` — registers a new private corp-* department repo after approval
