# Search algorithm — поиск и project evidence

## ToC
1. [Pre-flight (HARD PRECONDITION)](#pre-flight-hard-precondition)
2. [Реестр констант (Project IDs)](#реестр-констант-project-ids)
3. [Search for existing issues](#search-for-existing-issues)
4. [Batched GraphQL search](#batched-graphql-search)
5. [Project evidence commands — batched GraphQL issue state](#project-evidence-commands--batched-graphql-issue-state)
6. [Active session → Project status In progress](#active-session--project-status-in-progress)
7. [False-positive surface](#false-positive-surface)

---

## Pre-flight (HARD PRECONDITION)

**Pre-flight MUST run before any `gh search`, `gh issue`, or other GH command.** No exceptions. Skipping pre-flight = skill violation.

**Keep pre-flight silent and minimal.** Do not dump tasks.md content, full git status, or label catalogues into chat. Read what you need internally, surface only what changes the proposal.

**Output budget for pre-flight: 0 lines.** All findings go into the proposal, not into a separate investigation dump.

**Алгоритм:**

1. **Read `~/Documents/obsidian/0_hq/tasks.md` FIRST.** Curated index of current-week priorities + active tracks + repo pointers. Without it, search is shotgun (4+ random keywords) instead of targeted.
   - For "today", current-week, HQ plan, or drift questions, also read the linked daily file `tasks/WNN/YYYY-MM-DD.md` and the current `tasks/WNN/README.md`.
   - Active task rows in `tasks.md` / `tasks/WNN/YYYY-MM-DD.md` must have human-readable GitHub issue refs (`repo#N`). If a task has no issue ref, report `Расхождение HQ tasks`.
2. Определи GitHub Project-доски из `tasks.md` и track index. Один раз за запуск сними snapshot:
   ```bash
   gh project item-list 4 --owner serejaris --format json --limit 1000 > /tmp/manager-proj4.json
   jq -r '.items[] | select(.content.number==N and (.content.repository|endswith("REPO"))) | .status' /tmp/manager-proj4.json
   ```
   `--limit 1000` обязателен: на доске 300+ items, дефолтный лимит вернёт неполный срез. Это специальное исключение только для pre-flight snapshot Project #4; для доменных Project evidence используй issue-scoped GraphQL `projectItems`.
3. **HQ task drift guard.** Если current day/week plan содержит active задачу без `repo#N` → вывести `Расхождение HQ tasks: <строка> — нет GitHub issue`. Read mode: только докладывать. Write mode: найти существующий или создать issue, затем обновить дневной план.
4. Check git status of CRM/relevant repo (silently). If specific artifacts referenced in session are uncommitted, mention only those by name in proposal.
5. Compute current ISO week if `tasks.md` "Обновлено" is stale.
6. Независимые gh-чтения запускай параллельно — несколько Bash-вызовов в одном сообщении. Последовательно — только когда вход одного зависит от выхода другого.

**Red flag: skipping tasks.md**

Если собираешься запустить `gh search issues` без предварительного чтения `tasks.md` — STOP. Ты делаешь shotgun search вместо targeted по Project/track index.

---

## Реестр констант (Project IDs)

Известные ID использовать напрямую. `gh project list` / `gh project field-list` дёргать только для доски, которой нет в таблице.

| Project | number | project-id | известные поля |
|---|---|---|---|
| `ris © corp` | 4 | `PVT_kwHOCisBXs4BCN8O` | Status `PVTSSF_lAHOCisBXs4BCN8Ozg0fml0` (Backlog = `f75ad846`, Ready = `08afe404`, In progress = `47fc9ee4`, In review = `4cc61d42`, Done = `98236657`); Часы `PVTF_lAHOCisBXs4BCN8OzhVKHhI` |
| `Менторство 1-на-1` | 14 | `PVT_kwHOCisBXs4BQrb1` | field-list при первом write → дописать |
| `Кружок Вайбкодинга` | 28 | `PVT_kwHOCisBXs4BR41f` | Status `PVTSSF_lAHOCisBXs4BR41fzg_lQzE` (Todo = `f75ad846`, In Progress = `47fc9ee4`, Done = `98236657`) |
| `Colder — корпоративное обучение` | 31 | `PVT_kwHOCisBXs4BT5Hs` | field-list при первом write → дописать |
| `Personal Corp` | 34 | `PVT_kwHOCisBXs4BVZDi` | Status `PVTSSF_lAHOCisBXs4BVZDizhQ1LDQ` (Todo = `f75ad846`, In Progress = `47fc9ee4`, Done = `98236657`) |
| `Школа Вайбкодинга` | 5 | `PVT_kwHOCisBXs4BDKxF` | field-list при первом write → дописать |
| `Personal Corp Course Launch` | 10 | `PVT_kwHOCisBXs4BP8bu` | Status `PVTSSF_lAHOCisBXs4BP8buzg-NMEM` (Todo = `f75ad846`, In Progress = `47fc9ee4`, Done = `98236657`) |

---

## Search for existing issues

For each artifact or query subject, search by **multiple keys** to avoid missing matches. For simple unambiguous tracks (clear single-keyword like `Sportmaster`) one query is enough — escalate to multi-key only when first query returns 0 or 5+ matches:

```bash
gh search issues --owner serejaris <key> --json repository,number,title,labels,state,updatedAt
```

**КРИТИЧНО: `--state` принимает только `open` или `closed`. Значение `all` невалидно и вызывает ошибку.** Чтобы охватить оба статуса — НЕ передавай `--state` вообще: один вызов без флага возвращает и open, и closed одновременно. Никогда не делай два запроса (open + closed) — это лишний расход скудного REST-лимита (30/мин).

```bash
# REST: один вызов без --state — оба статуса сразу
gh search issues --owner serejaris LABEL_OR_KEY --json repository,number,title,labels,state,updatedAt
```

```bash
# GraphQL: один alias без state: qualifier — оба статуса сразу
gh api graphql -f query='
query {
  results: search(query:"user:serejaris is:issue LABEL_OR_KEY", type:ISSUE, first:40){ nodes { ... on Issue { number title state repository{nameWithOwner} labels(first:10){nodes{name}} updatedAt } } }
}' | jq -r '(.data // {}) | (.results.nodes // [])[] | select(.number != null)
  | "\(.state) \(.repository.nameWithOwner)#\(.number) \(.title) [\([(.labels.nodes // [])[].name]|join(","))]"'
```

**Keys to try (per artifact/subject):**
- Person name + slug (Russian + English): `"Roman Kiselev"`, `kuimov`, `Куимов`
- Company / track: `Sportmaster`, `Smena`, `Кружок`
- Telegram handle if mentioned: `Roma_Bookin`, `NikitaKuimov`
- Filename slug from CRM artifact: `kuimov-nikita`, `2026-Q2-sportmaster-strategy`

**Match acceptance criterion:** issue title or body references the same person/company/track AND scope of work overlaps. If 2+ candidates match — pick the most specific one as primary. Distinct scopes become `Related` context, not comments by default.

---

## Batched GraphQL search

Батч при 3+ ключах — один вызов вместо N:

```bash
gh api graphql -f query='
query {
  s1: search(query:"user:serejaris is:issue Sportmaster", type:ISSUE, first:20){ nodes { ... on Issue { number title state url repository{nameWithOwner} labels(first:10){nodes{name}} updatedAt } } }
  s2: search(query:"user:serejaris is:issue Куимов", type:ISSUE, first:20){ nodes { ... on Issue { number title state url repository{nameWithOwner} labels(first:10){nodes{name}} } } }
}' | jq -r '(.data // {}) | to_entries[] | .key as $k | (.value.nodes // [])[] | select(.number != null)
  | "\($k) \(.state) \(.repository.nameWithOwner)#\(.number) \(.title) [\([(.labels.nodes // [])[].name]|join(","))]"'
```

**CRITICAL — pipe в отдельный `jq`, НЕ флаг `--jq`.** Это главная причина повторяющихся падений скилла:

- Когда в ответе GraphQL есть массив `errors` (хоть один упавший alias, хоть тотальный провал запроса), `gh api graphql` **полностью игнорирует флаг `--jq`** и валит сырой JSON-body в stdout + короткую ошибку в stderr, exit 1. Guard `(.data // {})` внутри `--jq` при этом **не выполняется** — флаг обойдён.
- Поэтому всегда `gh api graphql -f query='...' | jq -r '(.data // {}) | ...'`. Тогда сырой body (с `data` или только с `errors`) идёт из stdout в `jq`, guard `(.data // {})` срабатывает на теле: живые alias'ы печатаются, упавшие игнорируются, тотальный провал → пустой вывод без краша. Ошибка gh остаётся видимой в stderr для отладки.
- **Никогда не парсить ответ Python-инлайном (`python3 -c "d['data']..."`)** — при тотальном провале body = `{"errors":[...]}` без ключа `data` → `KeyError: 'data'`. Если Python неизбежен — только `d.get('data', {})`, не `d['data']`.

**Обязательные guard'ы в jq-выражении (без них батч падает на `cannot iterate over: null`):**
- **`(.data // {})`** — ПЕРВЫМ. На теле без ключа `data` (только `errors`) `.data` = `null`, `to_entries[]` падает. `// {}` гарантирует пустой объект;
- `(.value.nodes // [])` и `(.labels.nodes // [])` — alias или поле может вернуть `null`;
- `select(.number != null)` — отбрасывает пустые объекты `{}` от не-Issue нод;
- `is:issue` в каждой query-строке — отсекает PR.

**Partial errors:** при `| jq` упавший alias просто отсутствует в выводе, живые печатаются. Не ретраить весь батч вслепую — при нужде прочитать `.errors` отдельным проходом (`... | jq '.errors'`), починить/выкинуть упавший alias.

**Почему батч важен:** `gh search issues` — REST Search API с лимитом **30 запросов/мин**; multi-key прогон на 15-20 поисков упирается в троттлинг. GraphQL `search()` считается против общего GraphQL-лимита (5000 очков/час) и батчится. Qualifier владельца в GraphQL-запросе — `user:serejaris`, не `--owner`.

---

## Project evidence commands — batched GraphQL issue state

When reporting or fixing Project placement, prose is not evidence. Use live reads.

**Канон чтения — batched GraphQL.** Один вызов на пачку issues (до ~20 через alias'ы) возвращает state, labels, parent и projectItems со status lane.

**Project API discipline:**
- `gh project item-list` разрешён только когда skill явно называет конкретный pre-flight snapshot, например Project #4.
- Для всех остальных Project read сначала используй batched GraphQL по issue и читай `projectItems`.
- Перед `gh project item-edit` докажи live GraphQL-read: issue exists, Project item exists, current status lane, target Project and lane.
- Если GraphQL/API rate limit блокирует proof, останови Project sync и напиши `Project lane pending: rate limit`.

**Red flag:** если собираешься выполнить `gh project item-list <domain-project>` до batched GraphQL issue-state read — STOP.

Пример:

```bash
gh api graphql -f query='
query {
  i1: repository(owner:"serejaris", name:"crm") { issue(number:27) { ...IssueState } }
  i2: repository(owner:"serejaris", name:"teach-vibecoding") { issue(number:313) { ...IssueState } }
}
fragment IssueState on Issue {
  number title state url
  labels(first:20){nodes{name}}
  parent { number title repository { nameWithOwner } }
  projectItems(first:10){nodes{ id project { number title } fieldValueByName(name:"Status"){ ... on ProjectV2ItemFieldSingleSelectValue { name } } }}
}' | jq -r '(.data // {}) | to_entries[] | .value.issue | select(. != null)
  | "\(.number) \(.title) [\([(.labels.nodes // [])[].name]|join(","))] parent=\(.parent.repository.nameWithOwner // "—")#\(.parent.number // "") projects=\([(.projectItems.nodes // [])[] | "\(.project.title):\(.fieldValueByName.name // "пусто")"]|join(" | "))"'
```

Пайп `| jq -r`, не флаг `--jq` (см. CRITICAL выше — при `errors` в ответе gh обходит `--jq`). `parent` здесь = API parent из Sub-issues; `projectItems[].fieldValueByName.name` = status lane. Ответ лежит в `.data.<alias>.issue` (не забыть уровень `.issue` в jq).

**Списки children эпика — REST:**

```bash
gh api repos/PARENT_OWNER/PARENT_REPO/issues/PARENT_N/sub_issues --jq '.[] | {number, title, repository_url}'
```

**Точечный fallback (один issue):** `gh issue view N -R OWNER/REPO --json projectItems` — `projectItems[].status` is an object; read `.status.name`, not `.status`.

**Project drift rules:**
- Present in Project + empty Status field = `Расхождение Project`
- In write mode, set the resolved lane when unambiguous
- If GraphQL/rate limit blocks status edit, report `Расхождение Project: placement ok, status lane pending` and do not claim full repair

---

## Active session → Project status `In progress`

В **write mode**, если founder в текущей сессии реально работает с issue, manager **обязан** выставить status `In progress` на всех touched primary/child issues в:

- глобальном weekly Project `ris © corp` / Project `#4` — lane **`In progress`** (`optionId` обычно `47fc9ee4`);
- доменной доске трека, если issue там уже лежит — lane **`In progress`** / **`In Progress`** (имя зависит от board; не оставлять `Ready`/`Todo`/пусто).

**Правила:**

1. Трогаем только issues, которые manager обновил или создал в этом sync, плюс их visible parent lesson/session issue, если parent тоже в текущем day plan.
2. Не переводить в `In progress` исторические/backlog issues без работы в сессии.
3. Не понижать `Done` / `In review` без явного founder signal.
4. Если item ещё не в Project — сначала `gh project item-add`, потом `gh project item-edit` на status.
5. Parent lesson/session issue тоже переводить в `In progress`, если child активен сегодня.

**Команды (пример для `ris © corp`):**

```bash
# 1) item id — из live GraphQL `projectItems.nodes[].id` или из `gh project item-add ... --format json`
# 2) field/option ids — из реестра констант выше или `gh project field-list` для неизвестной доски
gh project item-edit \
  --id PVTI_... \
  --project-id PVT_kwHOCisBXs4BCN8O \
  --field-id PVTSSF_lAHOCisBXs4BCN8Ozg0fml0 \
  --single-select-option-id 47fc9ee4
```

Для доменной доски (например Colvir / `Colder — корпоративное обучение`, Project `#31`) сначала прочитай `gh project field-list 31 --owner serejaris` — имена lane могут отличаться.

---

## False-positive surface (read AND write mode)

Search by W-label or generic terms can return issues that **share a label but aren't on this track**.

**Rule:** if a search match's title/body has no overlap with the queried track besides W-label or other generic label — it's a false positive. Drop it from results, surface in report under `IGNORED (false positives)` so founder can confirm.

```
IGNORED (false positives):
- crm#1 — surfaced via W18 label match, but track = legal/monotributo (unrelated to Sportmaster)
```

Don't silently filter — show what was filtered and why, in case founder spots a real link manager missed.
