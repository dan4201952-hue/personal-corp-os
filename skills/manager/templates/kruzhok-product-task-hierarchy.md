# Kruzhok product task hierarchy

Use this template when manager touches tasks for `Кружок`, `Circle`, a stream
number, lesson delivery, запуск/воронка, bot/funnel work, or student-facing
publication for the product.

The hierarchy uses the same shape as mentoring:

```text
трек потока -> issue урока -> подзадачи артефактов доставки
трек потока -> lane запуска и воронки -> подзадачи запуска и воронки
```

## Source Boundaries

| Layer | Owner | What belongs there |
|---|---|---|
| Product canon | `~/Documents/obsidian/0_hq/products/kruzhok/` | offer, status, dates, source-of-truth routing |
| Public entry / acquisition | `vibecoding.phd`, `live-sereja-tech`, `corp-tg-ris-ai`, `corp-vibecoders` | public CTA, source code, destination, posts, live links |
| Bot / funnel | `hsl-mozg` | экран бота, бронь, оплата, follow-up, source attribution |
| Lesson source | `teach-vibecoding` | teacher-facing lesson source, deck source, handouts, messages |
| Runtime / publication | `cohorts` | LMS-страница, доступ, `video_id`, production smoke |
| CRM / cash | `crm`, cash — `corp-sales/CLAUDE.md` § Live cash truth | people, deals, follow-up, факт оплаты |

HQ names the route and current canon. Execution tasks live in the owner repo of
the artifact.

## Hierarchy

### Track Overview / Epic

Root issue for one stream or product launch.

Title pattern:

```text
Кружок #<N> — <stream/product scope>
```

Example:

```text
Кружок #11 — майский поток 2026
```

The epic body is a router: status, next lesson or launch milestone, source
boundaries, and acceptance that active children are attached through the
GitHub Sub-issues API.

### Запуск и воронка

First-level child of the track epic. Use one lane запуска и воронки when the work
is about launch, traffic, public surfaces, source codes, bot/funnel, or
conversion across multiple posts/screens.

The lane title starts with the product/stream, not with a service prefix. Its
type and owner live in labels, Projects, parent tree, and body fields.

Title pattern:

```text
Кружок #<N> — запуск и воронка: <scope запуска/конверсии>
```

Typical children:

- `Кружок #<N> — пост запуска в Telegram`
- `Кружок #<N> — CTA для YouTube/лайва`
- `Кружок #<N> — исходники и маршрут бота`
- `Кружок #<N> — E2E-проверка брони и оплаты`

### Lesson Issue

First-level child of the track epic. This is the Kruzhok equivalent of a
mentoring session issue by hierarchy shape only. For Kruzhok, use `lesson` and
`L<N>`; reserve `session` and `S<N>` for mentoring.

Title pattern:

```text
Кружок #<N> L<M> — <lesson topic>
```

Examples:

```text
Кружок #11 L3 — GitHub/деплой: от прототипа до живого ИИ-сервиса
Кружок #11 L4 — финальный урок, тема уточняется
```

The lesson issue is a lifecycle parent. Its title must name the topic so `L3`
and `L4` do not become interchangeable status containers. The body owns
lesson-level state: prep, live fact, post-live delivery, runtime/publication
status, next student-facing step, and current blockers.

### Lesson Children

Second-level children under the exact lesson issue. These tasks must not be
placed directly under the stream epic when they belong to one lesson.

Typical children:

- `Кружок #<N> L<M> — презентация`
- `Кружок #<N> L<M> — сообщения и домашка`
- `Кружок #<N> L<M> — провести лайв`
- `Кружок #<N> L<M> — запись и video_id`
- `Кружок #<N> L<M> — транскрипт и заметки источника`
- `Кружок #<N> L<M> — LMS/runtime-страница`
- `Кружок #<N> L<M> — пост в канал после лайва`

## Lesson Body Template

```markdown
Урок <M> потока Кружка #<N>.

**Status:** <planned / prep / held / delivery pending / delivered / blocked>
**Freshness:** <planned / current open tail / historical delivered / stale active-looking>
**Active work:** <repo#N or none>
**Next:** <one concrete next action>
**Дата лайва:** <YYYY-MM-DD HH:MM TZ or exact blocker>
**Teacher source:** `<teach-vibecoding path>`
**Runtime target:** `<cohorts path or LMS URL>`

## Scope
- prep: lesson source, agenda, prompts, deck
- live: conduct lesson and capture recording
- post-live: transcript/summary, homework, channel message
- runtime: LMS-страница, `video_id`, доступ, production smoke

## Delivery checklist
- [ ] Lesson source ready
- [ ] Deck / visual support ready
- [ ] Student messages / homework ready
- [ ] Live held or exact blocker recorded
- [ ] Recording / transcript status recorded
- [ ] LMS/runtime bundle validated
- [ ] Student-facing URL smoke passed
- [ ] Channel/group post sent or ready-to-send copy recorded

## Updates

- **YYYY-MM-DD:** <what changed>
```

## Plan Output Shape

Manager plans and read-mode reports for Kruzhok must show the tree, not a flat
list:

```text
Кружок #11 · hq#170 «Кружок #11 — майский поток 2026»
- Lane запуска и воронки <repo#N> «Кружок #11 — запуск и воронка: предзапуск» [deadline: 2026-05-14 in body; parent: hq#170 ✓; W-label: W20 ✓; Project: Кружок ✓; ris © corp ✓; status: Done]
  - <repo#A> «Кружок #11 — пост запуска в Telegram» [parent: lane ✓; W-label: W20 ✓; Project: Кружок ✓; status: Done]
  - <repo#B> «Кружок #11 — исходники и маршрут бота» [parent: lane ✓; W-label: W20 ✓; Project: Кружок ✓; status: Done]
- historical delivered L1 <repo#N> «Кружок #11 L1 — от промпта до продукта» [live date in body; parent: hq#170 ✓; W-label: W20 ✓; Project: Кружок ✓; status: Done]
  - <repo#A> «Кружок #11 L1 — лендинг урока 1» [parent: L1 ✓; W-label: W20 ✓; Project: Кружок ✓; status: Done]
- open tail L3 <repo#N> «Кружок #11 L3 — GitHub/деплой: от прототипа до живого ИИ-сервиса» [live date in body; parent: hq#170 ✓; W-label: W22 ✓; Project: Кружок ✓; ris © corp ✓; status: In progress]
  - <repo#A> «Кружок #11 L3 — презентация» [parent: L3 ✓; W-label: W22 ✓; Project: Кружок ✓; status: Done]
  - <repo#B> «Кружок #11 L3 — LMS/runtime-страница» [parent: L3 ✓; W-label: W22 ✓; Project: Кружок ✓; status: In progress]
  - <repo#C> «Кружок #11 L3 — пост в канал после лайва» [parent: L3 ✓; W-label: W22 ✓; Project: Кружок ✓; status: In progress]
- planned L4 <repo#N> «Кружок #11 L4 — финальный урок, тема и дата уточняются» [parent: hq#170 ✓; W-label: W23?; Project: Кружок ✓; status: Backlog/Ready]
- Трекер состояния доставки <repo#N> «Кружок #11 — состояние доставки уроков» [parent: hq#170 ✓; W-label: W22 ✓; Project: Кружок ✓; status: In progress]

Прямые дочерние задачи эпика без классификации:
- <repo#N> «Кружок #11 — старый продуктовый хвост» [parent: hq#170 ✓; W-label: backlog; Project: Кружок ?; status: Backlog] — старый или шумный child; следующее действие: классифицировать по owner evidence
```

Each surfaced issue line includes lifecycle class, parent status, W-label, and
Project placement. Active/current-week issues must be present in the domain
Project and in `ris © corp` when they are in the weekly/day plan; if the Project
has status lanes, the status value must be set. Missing Project, missing global
Project, or null status for active work is `Расхождение Project`.

## Lesson Lifecycle Classes

| Class | GitHub state | Labels | Close condition |
|---|---|---|---|
| historical delivered | closed | `type:lesson`, `program:cohort`, `lesson-state:processed`, week label | live happened, runtime/comms/proof are recorded, and no active tail remains |
| open tail | open | `type:lesson`, `program:cohort`, `lesson-state:delivered`, week label | live happened, but LMS/runtime/channel/proof still has active work |
| current | open | `type:lesson`, `program:cohort`, `lesson-state:preparing` or `lesson-state:delivered`, week label | work is actually in the current W-plan |
| planned | open | `type:lesson`, `program:cohort`, `lesson-state:not-started` or `lesson-state:preparing`, future week label when known | topic/owner are confirmed; otherwise keep `тема уточняется` in title/body; date lives in body/calendar/Project fields |

Historical lessons must not look like active work. If L1/L2 already happened and
delivery proof exists, close the lesson parent or mark the only remaining child
as an explicit open tail.

## Durable Rules

- One stream/product launch has one root epic.
- Запуск и воронка is a first-level lane under the root epic.
- Each lesson is a first-level child under the root epic.
- Each lesson parent title includes the topic, not only `провести / доставить урок`.
- Visible titles do not use service prefixes such as `product:`, `content:`,
  `infra:`, `ops:`, or `epic:`. Type/routing lives in labels, parent tree,
  body fields, and Project placement.
- Visible titles do not include dates, times, deadlines, or W-labels. Put them
  in labels, Project fields, body fields, calendar, or CRM.
- Visible titles are Russian. Keep English only for product names, brands,
  repos, commands, APIs, labels, and stable technical tokens such as `GitHub`,
  `Telegram`, `YouTube`, `LMS`, `OpenClaw`, `Personal Corp`, `LLM`, `PRD`,
  `E2E`, and `video_id`.
- Presentation, messages, recording, transcript, LMS, and post-live tasks are
  children of the exact lesson issue.
- A lesson child task must not be attached to the lane запуска и воронки only because it
  contains public copy.
- A lesson issue must not be collapsed into the root epic body.
- A lane запуска и воронки must not own lesson delivery artifacts.
- A task with a concrete artifact lives in the owner repo for that artifact.
- Active/current-week issues keep manager invariants: W-label, exactly one
  parent through Sub-issues API, and Project placement.
- Create lesson parent skeletons ahead of time only when the lesson is part of
  the committed stream plan. Create artifact children when the work enters the
  current/next week or a concrete artifact appears.
- Runtime/publication is not done until `video_id` or exact blocker is recorded,
  bundle validation passes, and student-facing URL smoke passes.
- A passed live is not a delivered lesson until the active delivery tail is
  either closed with proof or shown as the exact open child.
- Funnel/cash status needs owner evidence from `hsl-mozg`, `crm`, or
  `corp-sales`; do not infer payment or attribution from views alone.

## Anti-Patterns

- Root epic with 20 flat children where lessons, запуск/воронка, backlog, and
  artifact tasks are mixed.
- `Кружок #11 L3 — презентация` attached directly under the epic when
  a L3 lesson issue exists or should exist.
- `Кружок #11 multi-channel promo` used as parent for L1/L2/L3 lesson
  deck or recording tasks.
- Closing delivery because teacher source exists while LMS/runtime is not
  verified.
- Leaving passed L1/L2 lesson parents open after delivery proof exists; this
  makes old lessons look like current work.
- Naming a lesson parent `провести и доставить урок` without the topic; topic is
  required in the title.
- Creating a new lesson artifact issue without first finding or creating the
  exact lesson parent issue.
- English action phrases in visible titles: `launch/funnel`, `delivery track`,
  `post-live channel post`, `topic TBD`, `date TBD`, `workshop prep`,
  `handoff`, `rollout package`.
