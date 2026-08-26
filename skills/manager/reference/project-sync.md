# Project sync — HQ day plan, time tracking, lifecycle, commits

## ToC
1. [HQ day plan sync (write mode)](#hq-day-plan-sync-write-mode)
2. [Time tracking (write mode)](#time-tracking-write-mode)
3. [Привязка коммитов к задачам](#привязка-коммитов-к-задачам)
4. [Планировочные артефакты (PRD / план / диаграмма)](#планировочные-артефакты-prd--план--диаграмма)
5. [Lifecycle and lane drift](#lifecycle-and-lane-drift)
6. [W-label rules](#w-label-rules)

---

## HQ day plan sync (write mode)

В **write mode** manager **обязан** синхронизировать дневной файл `~/Documents/obsidian/0_hq/tasks/WNN/YYYY-MM-DD.md`, если sync касается работы **сегодня** или founder явно ведёт prep к событию **завтра/послезавтра** из текущей сессии.

**Не ждать** отдельного «обнови day plan» — это часть стандартного `/manager` write sync.

**Алгоритм:**

1. Прочитать `tasks.md` → определить `WNN` и сегодняшний `YYYY-MM-DD.md`.
2. Для каждого touched track/issue добавить или обновить строку в `P0`/`P1` с форматом `**<краткое действие> (`repo#N`, parent `repo#P`).** <1 строка next step>`.
3. Если задача уже в плане — обновить формулировку/next step, не дублировать.
4. Обновить `Обновлено:` timestamp в шапке дневного файла.
5. Если scope явно «не сегодня» — не добавлять в сегодняшний day plan.
6. `tasks.md` **не переписывать** целиком; допустимо только точечно обновить строку в `## Активные треки`, если manager sync меняет канон «что следующий урок / какой open tail» для трека из сессии.

**Анти-паттерны day plan:**
- строка без `repo#N`;
- дубль той же issue в P0 и P1;
- удаление чужих P0 без founder signal — только добавлять/уточнять touched tracks.

---

## Time tracking (write mode)

Владелец детальных записей времени — `~/Documents/obsidian/0_hq/time/log.csv` (формат и словарь activity — `0_hq/time/README.md`). Программный срез по issue зеркалится в Number-поле **«Часы»** Project `ris © corp` / #4 (field id `PVTF_lAHOCisBXs4BCN8OzhVKHhI`), не в body. Body-поле `**Время:**` — legacy: новые не писать, встреченные старые можно удалять при body sync (решение 2026-06-10, `hq#209`).

Если founder в сессии назвал затраченное время — manager **обязан** в том же write sync:

1. Определить самый специфичный issue для этой работы (артефакт/сессия/lesson child, не epic) — обычным search-алгоритмом.
2. Дописать строку в `time/log.csv`: `date,week,issue,track,activity,hours,note`. `date` = день, когда работа была сделана (сверить с календарём/day-файлом: «сегодня» в речи founder'а может означать вчерашний live).
3. Одна строка = один (день × issue × activity); подготовка и проведение — разные строки.
4. Обновить поле «Часы» в Project #4 — суммарный итог по issue из log.csv:
   ```bash
   item=$(gh project item-add 4 --owner serejaris --url https://github.com/serejaris/REPO/issues/N --format json --jq .id)
   gh project item-edit --id "$item" --project-id PVT_kwHOCisBXs4BCN8O --field-id PVTF_lAHOCisBXs4BCN8OzhVKHhI --number HOURS
   ```
   При следующем логе значение пересчитывается из log.csv, не прибавляется на глаз.
5. Если issue для работы нет — сначала стандартный invariant (найти/создать issue с parent + W-label), потом строка времени.
6. В result report показать залогированные строки: `time/log.csv ← 2.5ч проведение → repo#N «title» (Часы=7.5 в ris © corp)`.

В read mode вопросы «сколько времени на X» отвечаются агрегацией из `log.csv` или полем «Часы» с доски, не оценками.

---

## Привязка коммитов к задачам

Founder смотрит «что сделано по коду» через issue, поэтому каждый коммит сессии обязан быть привязан к задаче:

1. **Трейлер в каждом коммите:** `refs <owner>/<repo>#N` (или `closes <owner>/<repo>#N`, если коммит полностью закрывает scope). GitHub при push показывает backlink в timeline issue — работает и cross-repo.
2. **SHA в body:** dated entry в `## Updates` перечисляет короткие SHA touched repos: `(код: dotclaude@9a8ff92, corp-server@6fb5b26)`. Issue без SHA при наличии коммитов в сессии = неполный sync.
3. **Сбор SHA в write mode:** `git log --oneline -10` по каждому touched repo сессии перед записью Updates.
4. Если коммит делается агентом в момент sync — трейлер ставится сразу, body-SHA добавляется в тот же Updates entry.
5. **Артефакт в body/отчёте должен быть закоммичен и запушен ДО ссылки.** Founder читает всё через веб-GitHub: незакоммиченный локальный файл для него не существует. Ссылка в body/отчёте — кликабельный GitHub-URL, не `~/Documents/...`.

---

## Планировочные артефакты (PRD / план / диаграмма)

Issue — источник истины. Правила:

1. **Полный PRD/план живёт прямо в body issue**: контекст, таблица ключевых решений, mermaid-диаграммы (GitHub рендерит их в body), схема данных, MVP-этапы, вне scope, открытые вопросы. Не «ссылка на файл с PRD», а сам PRD.
2. **Локальный md-файл для PRD можно и нужно держать** — рабочая полная копия в репо/vault. При расхождении источник истины — issue.
3. **Ссылка на файл из issue — только кликабельный GitHub-URL на уже закоммиченную и запушенную версию** (`**Source artifact:** https://github.com/<owner>/<repo>/blob/main/...`). Сначала commit+push файла, потом ссылка. Локальный путь `~/...` в issue — мёртвая ссылка для founder'а.
4. Шаблон body для PRD-issue — в `templates/issue-body-templates.md`, секция «PRD issue body template».
5. День-план и `tasks.md` ссылаются на issue (`repo#N`).

---

## Lifecycle and lane drift

Manager checks whether labels/status still match time and delivery reality:

- date passed + `lesson-state:preparing` / `not-started` = `Расхождение lifecycle`;
- live within D-1 and lesson still `Ready` / domain lane `Не начат` = `late prep risk`;
- open post-live/handoff issue without outcome or blocker after the event date = `Расхождение lifecycle`;
- Project #4 lane and domain board lane disagree in a way that changes operator meaning = `Расхождение lane`;
- stale phase label beside current lesson/week = `Расхождение labels`.

Do not auto-close or rewrite lifecycle state unless the exact scope is proven done. In write mode, update labels/status only when the source of truth is clear; otherwise report the drift and next evidence needed.

---

## W-label rules

### Current-week resolution

1. Read `tasks.md` first line under `# Задачи` block — it has `Обновлено: YYYY-MM-DD` and points to the curated current-week index / hot tracks.
2. Compute ISO week number from `current_date` / `date '+%V'`; use it as deterministic fallback whenever `tasks.md` is stale (>7 days) or inconsistent.
3. Map to label format: `W{NN}` (zero-padded only if existing labels are zero-padded — check repo first).

### Датированные mentoring sessions

Для mentoring session issue текущая W-label считается от конкретной даты сессии в body, calendar или Project fields, а не копируется с profile issue, прошлой `S<N>` или примера.

- `Валентин (@xbhsy289) S2 — подготовить и провести сессию` при дате `2026-05-29` в body/calendar получает `W22`.
- Если body/calendar содержит только `DD.MM`, год брать из current session context. Если год неоднозначен — показать `Расхождение недели: дата сессии неоднозначна` и не писать GitHub до уточнения.
- Если sync идёт в другой неделе, показать обе недели: `session week: W22`, `sync week: W23`.
- Если текущая/датированная session issue имеет устаревшую или отсутствующую W-label, вывести `Расхождение недели: <repo#N «title»> — стоит <labels>, по дате нужен W<NN>; действие: добавить W<NN>`.
- Read mode только показывает расхождение. Write mode добавляет scoped W-label по standing authorization.
- Старые `retro:W*` и исторические labels не удалять. Старые `W*` не снимать ради чистоты.

### Multi-week tasks

**Apply BOTH labels.** Task that requires founder action this week AND continues next week gets `W18` AND `W19`.

### Backlog vs future-week

- Deferred more than 1 week without active work → `backlog` (create label if missing)
- Planned for specific future week → `W{NN}` for that week
- Never use `backlog` AND `W{NN}` together — pick one

### Creating W-label on demand

Fast-path: не проверяй существование label отдельным `gh label list`. Сразу `gh issue edit N --add-label "W24"`; только если упало `label not found` — создай label и повтори.

```bash
# W-week label (current/future week)
gh label create "W18" -R "$REPO" \
  --color "0E8A16" \
  --description "Week 18 (Apr 27 - May 3, 2026)"

# backlog label
gh label create "backlog" -R "$REPO" \
  --color "ededed" \
  --description "Deferred — not on current/next week"
```

Color `0E8A16` (dark green) for active weeks, `ededed` (neutral grey) for backlog. Description format: `Week NN (Mon DD - DD, YYYY)`.
