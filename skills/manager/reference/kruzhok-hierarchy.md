# Kruzhok product hierarchy — полный свод правил

## ToC
1. [Иерархия Кружка](#иерархия-кружка)
2. [Kruzhok title pattern](#kruzhok-title-pattern)
3. [Kruzhok update/create rules](#kruzhok-updatecreate-rules)
4. [Pre-sync checklist](#pre-sync-checklist)
5. [Kruzhok read/write output](#kruzhok-readwrite-output)

---

## Иерархия Кружка

Для задач по `Кружку`, `Circle`, номеру потока, уроку, запуску/воронке, bot/funnel или student-facing publication сначала загрузить `templates/kruzhok-product-task-hierarchy.md`.

Структура Кружка повторяет mentoring. Корневой epic = поток/продуктовый track. Первый уровень = lane запуска/воронки и отдельные lesson issues. Второй уровень = артефакты конкретного запуска/воронки или урока: презентация, сообщения, запись, транскрипт, LMS/runtime, пост после лайва.

---

## Kruzhok title pattern

Полный шаблон и body-структура живут в `templates/kruzhok-product-task-hierarchy.md`. Короткая формула:

| Тип issue | Title pattern | Пример |
|---|---|---|
| Track epic | `Кружок #<N> — <stream/product scope>` | `Кружок #11 — майский поток 2026` |
| Lane запуска и воронки | `Кружок #<N> — запуск и воронка: <scope запуска/конверсии>` | `Кружок #12 — запуск и воронка: предзапуск` |
| Lesson issue | `Кружок #<N> L<M> — <lesson topic>` | `Кружок #11 L3 — GitHub/деплой: от прототипа до живого ИИ-сервиса` |
| Lesson child | `Кружок #<N> L<M> — <artifact/action>` | `Кружок #11 L3 — пост в канал после лайва` |

Lesson issue — lifecycle object урока. Его title обязан содержать тему, иначе `L<N>` начинает выглядеть как взаимозаменяемый контейнер статуса. Если тема не подтверждена, title явно пишет `тема уточняется`. Дата, время, дедлайн и W-label живут в body, labels, Project fields или календаре.

Если работа относится к конкретному уроку, manager сначала ищет/создаёт lesson issue и только потом создаёт/обновляет child task под ним. Нельзя класть презентацию, сообщения, запись, транскрипт или LMS-задачу прямо под epic, если есть или нужен lesson parent.

Для Кружка говорить `lesson` / `L<N>`. Термины `session` / `S<N>` остаются за mentoring.

---

## Kruzhok update/create rules

| Ситуация | Действие |
|---|---|
| Найден только stream epic, а работа относится к конкретному уроку | Найти или создать `Кружок #<N> L<M> — ...`; stream epic обновлять только короткой строкой состояния. |
| Презентация, сообщения, запись, транскрипт, LMS/runtime или post-live send относятся к уроку | Оставить/создать child issue под точным `L<M>` lesson issue. |
| Работа относится к исходникам, маршруту бота, брони/оплате, тексту после оплаты, атрибуции или cash | Использовать lane запуска/воронки и owner repo `hsl-mozg` / `corp-sales` / HQ; не смешивать с lesson delivery. |
| Lesson source готов, но LMS/runtime или student smoke не проверены | Статус lesson issue = `delivery pending` или `blocked`, не `done`. |
| Live прошёл, но LMS/runtime/channel proof открыт | Lesson issue остаётся open с `lesson-state:delivered`; конкретный хвост остаётся child issue. |
| Live прошёл, runtime/comms/proof закрыты, активных хвостов нет | Lesson issue закрывается как historical delivered с `lesson-state:processed`. |
| Тема будущего урока не подтверждена | Lesson issue остаётся planned/open с `тема уточняется` в title/body. Дата будущего урока пишется в body/Project/calendar. |
| Есть старые flat issues под stream epic | В плане показать proposed tree и reparent только те issue, где parent однозначен; массовый rename/close делать отдельным sync. |

---

## Pre-sync checklist

Перед любым Kruzhok sync manager обязан показать:

- `Track overview`: stream epic + W-label + Project.
- `Lane запуска/воронки`: если работа про продажи/маркетинг/funnel.
- `Lesson issue`: точный `L<N>` для live/delivery work.
- `Lesson lifecycle`: planned / current / open tail / historical delivered; старые L1/L2 не должны выглядеть активными, если delivery proof уже есть.
- `Delivery children`: запись/video_id, транскрипт/заметки источника, deck, messages, LMS/runtime, пост после лайва grouped under the exact lesson.
- `Расхождение недели`: missing/stale W-label by lesson date or active delivery work.
- `Расхождение Project`: active/current-week issue missing domain Project, missing `ris © corp`, or present in a Project with empty status lane.

---

## Kruzhok read/write output

Kruzhok read/write output must include:

```text
Дерево трека:
- <root epic>
  - <lane запуска/воронки или legacy lane запуска/воронки>
  - <historical lesson L1 with topic>
    - <delivery artifact child>
  - <active/open-tail lesson L3 with topic>
    - <delivery artifact child>
- <planned lesson L4 with topic уточняется when needed>
  - <трекер состояния доставки, if still needed>

Прямые дочерние задачи эпика без классификации:
- <repo#N> «title» — почему оставлено flat / next classification action
```

---

## Common mistakes (Kruzhok-specific)

| Mistake | Fix |
|---|---|
| Mixing Kruzhok stream epic, lesson work and delivery artifacts in one flat list | Mirror mentoring: stream epic routes; each lesson gets its own issue; deck/messages/recording/transcript/LMS live under that lesson. |
| Артефакты урока Кружка лежат под lane запуска/воронки | Lane запуска/воронки owns source, bot, booking, payment, CTA and conversion surfaces. Lesson deck, homework, recording, transcript, LMS and post-live message belong under the exact lesson issue. |
| Creating a Kruzhok artifact issue without lesson parent | Find/create `Кружок #<N> L<M> — ...` first, then link artifact issue as a child through Sub-issues API. |
| Naming a Kruzhok lesson parent without the lesson topic | Use `Кружок #<N> L<M> — <topic>`; action/status/date lives in body, labels, calendar, and Project fields. |
| Leaving completed L1/L2 lesson parents open after delivery proof exists | Close the lesson parent as historical delivered, or name the exact open delivery tail as child. |
