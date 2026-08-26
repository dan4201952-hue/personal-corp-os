# Issue authoring — titles, body templates, update/create decisions

## ToC
1. [Issue title convention](#issue-title-convention)
2. [Assignee — по умолчанию founder](#assignee--по-умолчанию-founder)
3. [Критерий готовности (definition of done) — body обязан быть проверяемым](#критерий-готовности-definition-of-done--body-обязан-быть-проверяемым)
4. [Update vs create decision](#update-vs-create-decision)
5. [Mentoring update/create rules](#mentoring-updatecreate-rules)
6. [Comment vs body update](#comment-vs-body-update)
7. [Body update mechanics](#body-update-mechanics)
8. [Mentoring source boundaries](#mentoring-source-boundaries)

---

## Issue title convention

Per `serejaris/hq#163`. **Видимые служебные prefixes (`product:`, `epic:`, `content:`, `infra:`, `ops:` и т.п.) больше не пишутся в title.** Тип задачи живёт в labels, parent tree, Projects и body.

Title language: заголовок пишется на русском. Английский — только для собственных имён и технических токенов. Action-часть всегда русская: `подготовить`, `провести`, `доставить`, `проверить`, `обновить`, `закрыть хвост`, `собрать`.

### Formula

```
{object} — {action}
```

| Сегмент | Что | Примеры |
|---|---|---|
| **`{object}`** | Конкретный субъект задачи | `Sportmaster`, `Personal Corp L3`, `Кружок #11 L3`, `Валентин S2`, `@ris_ai`, `tg-telethon` |
| **`{action}`** | Глагол + краткий scope без даты, времени, дедлайна и W-label | `подготовить бриф`, `обработать ответ + intake + слот` |

### Правила

1. **Без служебного prefix в title**
2. **`{object}` — узнаваемый объект в начале** (`Кружок #11 L3`, `Sportmaster`, `Валентин S2`)
3. **`em-dash (—)` разделитель** между object и action
4. **Без дат, времени, дедлайнов и W-label в title** — это metadata: labels, Project fields, body, календарь или CRM
5. **Без эмодзи в title**
6. **Старый prefix принимать как legacy alias** при поиске/чтении, но новые и переименованные titles писать без prefix

### Product / runtime fix title pattern

| Ситуация | Title pattern | Пример |
|---|---|---|
| Бот / funnel / runtime feature | `<product or surface> — <исправленное пользовательское поведение>` | `Бот @vibecod3rs — статус повторной заявки без сброса очереди` |
| Manual production case | Использовать как evidence в body, не как основной title | В body: `Julia 174676528 вручную добавлена через Bot API` |
| Ops discovery / runbook | `<system> — <операционная возможность или runbook>` | `Railway ops — контейнерные one-off команды через ssh` |

Если title можно понять только зная скриншот, имя человека или историю debugging-сессии — title слишком ситуативный. Детали → в `## Что сделано`, `Evidence`, `Updates`; title → через продуктовый результат.

### Mentoring title pattern

| Тип issue | Title pattern | Пример |
|---|---|---|
| Track overview | `<person> — трек менторинга` | `Валентин (@xbhsy289) — трек менторинга` |
| Session issue | `<person> S<N> — подготовить / провести / доставить материалы` | `Валентин (@xbhsy289) S2 — подготовить и провести сессию` |
| Delivery child | `<person> S<N> — <artifact/action>` | `Валентин (@xbhsy289) S1 — LMS-страница и ссылка на запись` |

### Anti-patterns

- ❌ `Sprint 2 pre-record — setup warp/claude...` — нет узнаваемого объекта
- ❌ `🔥 Sportmaster: КП` — эмодзи в title
- ❌ `prep к 27.04 встрече по Спортмастеру` — глагол в начале вместо существительного, дата в title
- ❌ `ops: всё про Smena retreat` — служебный prefix и слишком общий action
- ❌ `Smena → расхождение opp ⚠️ overdue 21.04` — стрелка вместо em-dash, эмодзи, дата в title
- ❌ `Кружок #13 — post-payment сообщения (W26)` — W-label в title

### Примеры правильных titles

- `Sportmaster — подготовить бриф и финал бюджета`
- `Максим (@urapapa) — обработать ответ + intake + слот`
- `Валентин (@xbhsy289) S2 — подготовить и провести сессию`
- `Personal Corp L3 — подготовить лайв`
- `@ris_ai — пост перекличка апреля 2026`
- `tg-telethon — синк полного покрытия без отставания`

### Where does type metadata live

| Metadata | Где |
|---|---|
| Work type | labels such as `type:lesson`, `area:content`, `area:ops`, `area:infra`, lifecycle labels |
| Track hierarchy | GitHub Sub-issues parent tree |
| Weekly visibility | W-label + Project placement |
| Dates, time, deadlines | body fields, Project fields, calendar, CRM |
| Owner/source | repo, Project, body fields such as `Source`, `Teacher source`, `Runtime target` |
| Root/epic status | sub-issues summary + body; no visible `epic:` prefix required |

### When migrating existing issues

Если в session manager касается issue со старым title — **не переименовывать** автоматически. Только если founder явно попросил bulk-rename.

---

## Assignee — по умолчанию founder

Когда manager в write mode **создаёт** issue или **трогает** активный issue без assignee — по умолчанию назначает founder'а: `@me`. `@me` резолвится в аутентифицированный gh-аккаунт (`serejaris`) — логин не хардкодить.

| Ситуация | Assignee |
|---|---|
| Новый issue, создаёт manager | `@me` (founder) по умолчанию |
| Активный touched issue без assignee | добавить `@me` |
| Issue уже назначен на кого-то (team-член, подрядчик) | **НЕ перетирать** — оставить как есть |
| Founder явно назвал другого исполнителя | назначить названного, не `@me` |
| Team / hiring / trial issue с владельцем-человеком (`corp-team`, эксперт-подрядчик типа Ивана) | владелец задачи, не founder по умолчанию |

Команды:
- create: `gh issue create ... --assignee @me`
- existing: `gh issue edit <N> -R <owner>/<repo> --add-assignee @me`

Read mode assignee не трогает (ничего не пишет в GitHub). Назначение assignee покрыто standing write authorization — отдельно «подтверди» не спрашивать.

---

## Критерий готовности (definition of done) — body обязан быть проверяемым

Когда manager **создаёт** issue или **оформляет** существующий, body **обязан** содержать проверяемые критерии готовности.

**Обязательный минимум:**

1. **Конкретный scope-чеклист `- [ ]`** — что именно входит в задачу, по пунктам, каждый формулируется так, что по нему видно «сделано / не сделано».
2. **Явное «считается done, когда…»** — условие закрытия, привязанное к проверяемому артефакту/поведению.
3. **Указатель на источник** — откуда взялся scope: секция скилла-источника, отчёт research-corp, CRM slug `[[…]]`, родительский epic, транскрипт встречи.

**ЗАПРЕЩЕНЫ расплывчатые однострочники без конкретики.** Issue, тело которого нельзя сверить с реальностью = **malformed**.

- ❌ `Внедрить правила по отчёту X` — непонятно какие правила, в какой файл, и когда считается готовым.
- ✅ scope-чеклист `- [ ]` конкретных правил + «done, когда правила закодированы в `<skill>/SKILL.md` § …» + ссылка на отчёт-источник.

Если manager трогает уже существующий расплывчатый issue (body — однострочник без DoD), он в том же sync **дописывает** конкретный scope-чеклист + acceptance + указатель на источник. Это часть стандартного write-синка по standing authorization.

---

## Update vs create decision

**Default: update issue body, NOT add comment.** Body = single source of truth, readable as one document.

| Situation | Action |
|---|---|
| Existing issue covers same scope, same track | **Edit body** — refresh "Status:", "Next:", dated line в `## Updates`. Проверь W-label текущая И parent epic привязан. |
| Existing issue scope is narrower but session expanded scope | Edit body существующего + создай новый follow-up issue с расширенным scope. Новый issue идёт child'ом того же epic'а. |
| Multiple existing issues match different aspects (parent epic + sub-issue) | Edit body наиболее специфичного child'а; epic трогаем только если его body нужно обновить. |
| Existing issue covers 2+ sibling scopes or belongs to forecast/pipeline/operating review | Treat as aggregate issue. Find repo-local aggregate epic first; if none exists, propose umbrella issue or split. |
| Existing child has parent API but appears flat in Project view | Do not reparent first. Verify parent Project placement + parent status lane. Add/fix the parent Project item before changing hierarchy. |
| Found related issue with same subject but different scope | Keep it as `Related` context only. Update/create a separate primary issue for the new standalone action. |
| No existing issue matches, but track is in `tasks.md` | Создать новый issue. Сначала resolve parent epic (см. parent-epic-rules.md). Если epic есть — link через sub_issues API. Если нет — surface в proposal. |
| No existing issue, no track in `tasks.md`, fresh artifact | Ask founder which repo + какой epic before creating |

---

## Mentoring update/create rules

| Ситуация | Действие |
|---|---|
| Найден только профильный track issue, а работа относится к конкретной сессии | Не превращать профиль в session task. Создать или найти `S<N>` issue и обновлять его. |
| У `S1` есть незакрытые delivery-части | Оставить их child/sub-issues под `S1`. Не переносить в `S2`. |
| В календаре появилась `S2`, а issue под `S2` нет | Создать `<person> S2 — подготовить и провести сессию` как child профильного mentoring issue; дату записать в body/calendar. |
| Founder подтвердил, что материалы сессии отданы студенту | Считать session delivery завершённой: обновить session issue до `delivered`, закрыть только тот issue, scope которого полностью покрыт доставкой, зафиксировать следующий active step отдельным issue. |
| После доставленной сессии следующий шаг = новый слот | Найти или создать child issue `<person> S<N+1> — забронировать следующую встречу`. |
| Существующий issue говорит «закрыть сделку», но CRM/ledger уже показывают оплаченный пакет | Считать это stale sales issue: предложить закрыть/переименовать только после проверки scope; delivery вести в session issue. Не создавать новую delivery-задачу с формулировкой «закрыть сделку». |
| Нужно упомянуть деньги, цену, остаток пакета или paid/won | Не писать это в GitHub task body. Обновить CRM/ledger, в issue оставить ссылку `[[crm-slug]]` и delivery next step. |

Перед любым mentoring sync manager обязан ответить на четыре вопроса: какой track overview, какая session issue, какие delivery children, где CRM/ledger owner для денег.

**Pre-sync weekly check:**

- `Track overview`: issue + title + parent/epic status + W-label.
- `Session issue`: точный `S<N>` issue для текущего календарного слота + parent OK + session date + expected W-label.
- `Delivery children`: хвосты сгруппированы по `S<N>`; старые `S1` хвосты получают новую W-label только если работа по ним реально продолжается сейчас.
- `Project placement`: активные `Track overview`, текущий `S<N>` issue и активные delivery children проверены через `projectItems`: доменная Project-доска (`Менторство 1-на-1`) + `ris © corp` / Project `#4`, если они входят в текущий weekly/day plan.
- `Расхождение недели`: `нет` или список issue, где labels не совпадают с датой/текущей неделей, с конкретным действием `добавить W<NN>` / `создать W<NN>`.
- `Расхождение Project`: `нет` или список issue, где W-label есть, parent OK, но нужный Project отсутствует; действие `добавить в Project <name>`.

**Read mode ничего не пишет в GitHub** — только показывает расхождение и следующее действие. Write mode добавляет scoped W-label по standing authorization только после `tasks.md` pre-flight, live issue read и parent check, если repo/issue/parent однозначны.

---

## Comment vs body update

**Default: edit body.** Comments stack chronologically and become unreadable through 5+ entries.

Use a comment ONLY when:
- The note is genuinely chronological and ephemeral (e.g. "blocked by external party until 05.05") — would clutter body
- Founder explicitly asked for a comment ("прокомментируй там")
- Body update would lose distinct meaningful history (rare — usually history goes into "## Updates" section in body)
- **Work-record после реальной работы по issue (Iron invariant 6)** — обязательный timeline-комментарий «что сделано в этой сессии» + `refs`/SHA. Один такой комментарий на сессию × issue.

**Anti-pattern signal:** if you're about to write the third comment on an issue with same kind of body-level progress update — that's two too many. Edit body instead.

---

## Body update mechanics

**НЕ загружать generic `github-issues`/`gh-issues` skill для этой операции.** Manager сам владеет read-modify-write паттерном: `gh issue view` → локальный body-файл → `gh issue edit --body-file`, с обновлением `Status` / `Next` / `## Updates`.

Если нужны команды — использовать стандартный `gh` CLI напрямую по правилам этого manager skill (не «вообще никак», а через CLI без переключения на generic skill).

Шаблоны body — новый issue, mentoring session, body update (default), comment (fallback) — живут в `templates/issue-body-templates.md`. Прочитать этот файл перед `gh issue create` или `gh issue edit --body-file`.

---

## Mentoring source boundaries

Manager всегда разводит четыре слоя:

| Слой | Где живёт | Что туда писать |
|---|---|---|
| Relationship / пакет / деньги | `crm/20_People/*`, `crm/30_Opportunities/*`, ledger/sales DB | оплата, сумма, остаток пакета, сделка, close/won/lost, договорённости |
| Track overview | профильный mentoring issue в teaching repo | короткий указатель на CRM slug, список сессий и текущее состояние доставки без сумм |
| Session issue | отдельный issue на каждую сессию `S1`, `S2`, ... | подготовка, факт проведения, чеклист доставки после сессии |
| Delivery sub-issues | children конкретной session issue | запись, транскрипт, workbook, LMS/runtime, ссылка студенту, follow-up |

Жёсткое правило: task/issue про delivery сессии не должен содержать цены, суммы, paid/won формулировки, «закрыть сделку» или ledger facts. Достаточно ссылки `[[crm-slug]]` и фразы «денежный статус см. в CRM/ledger».
