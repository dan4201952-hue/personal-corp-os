# 2026-06-25 — Project #4 «ris © corp»: триаж сирот + архив Done
## Триггер
Founder: «задачи снова стали сиротами, не могу пользоваться экраном — вывалены все скопом» (Week view, фильтр W26).
## Диагноз
Две независимые причины:
1. **Week view (#7) потеряла табличную группировку** — `groupByFields:[]` (было BOARD по Status, переключили на TABLE → плоская куча). Остаточный след `verticalGroupByFields:[Status]` + `sortByFields:[Status DESC]`. Сохранённый фильтр застрял на `W18`. **Чинится только в UI** — в публичном GraphQL API нет мутации на конфиг view (есть лишь `markFileAsViewed`).
2. **No-status items** (README: «items без Status = ошибка маршрутизации»): 9 в W26, **302 open board-wide** (83 с W-лейблом). Плюс **459 Done** не заархивировано (README: «Done регулярно архивировать»).
## Requests / запросы (воспроизводимо)
```bash
# конфиг views (groupBy/sort/filter)
gh api graphql -f query='{ node(id:"PVT_kwHOCisBXs4BCN8O"){ ...on ProjectV2{ views(first:25){ nodes{ name groupByFields{nodes{...on ProjectV2FieldCommon{name}}} verticalGroupByFields{nodes{...on ProjectV2FieldCommon{name}}} sortByFields{nodes{direction field{...on ProjectV2FieldCommon{name}}}} filter }}}}}'
# все items + Status + Parent issue (пагинация по 100)
gh api graphql -f query=@items.graphql  # fieldValueByName Status/Parent issue + content.parent
# items с labels/status/id для маппинга
gh project item-list 4 --owner serejaris --format json --limit 2000
# проставить Status
gh project item-edit --project-id PVT_kwHOCisBXs4BCN8O --id <ITEM> --field-id PVTSSF_lAHOCisBXs4BCN8Ozg0fml0 --single-select-option-id <OPT>
# архив Done (обратимо: --undo)
gh project item-archive 4 --owner serejaris --id <ITEM>
```
Status option-ids: `Backlog f75ad846 · Ready 08afe404 · In progress 47fc9ee4 · In review 4cc61d42 · Done 98236657`
## Метод
Два workflow (sonnet-агенты, по issue читают `gh issue view ... --json title,body,state,labels,comments,createdAt,updatedAt`):
- `w26-status-triage` — 9 агентов, по 1 issue → Status.
- `orphan-status-sweep` — 9 батч-агентов, ~9 issue каждый, со скидкой на застарелость (только старые W-лейблы + нет свежей активности ⇒ Backlog).
## Решения (83) — распределение
| Status | n |
|---|---|
| Backlog | 56 |
| Ready | 13 |
| In review | 8 |
| In progress | 3 |
| Done | 3 |

<details><summary>Все решения (repo#num · weeks · status · reason)</summary>

| batch | issue | weeks | → status | reason |
|---|---|---|---|---|
| orphan-sweep | hq#144 | W13 | Backlog | Только W13 (март), нет комментариев и активности, скилл board-of-advisors доработка заморо |
| orphan-sweep | hq#145 | W13 | Backlog | Только W13 (март), нет комментариев, метрики аудитории AI Mindset не запускались |
| orphan-sweep | hq#147 | W13 | Backlog | Только W13 (март), нет комментариев, activity log / daily diary не реализован |
| orphan-sweep | teach-vibecoding#193 | W13 | Backlog | Только W13 (март), нет комментариев, сессия 4 с Виктором так и не запланирована через этот |
| orphan-sweep | hq#149 | W13 | Backlog | Только W13 (март), нет комментариев, редакционный план для sereja.tech не сделан |
| orphan-sweep | hq#152 | W13 | Backlog | Только W13 (март), лекция AI Mindset 25 марта прошла, issue не закрыт и не обновлён после  |
| orphan-sweep | hq#153 | W13 | Backlog | Только W13 (март), нет комментариев, упаковка Personal Corp skills формально не закрыта |
| orphan-sweep | cohorts#53 | W13 | Backlog | Только W13 (март), нет комментариев, cron-автоматизация silent risk check не реализована |
| orphan-sweep | hsl-mozg#133 | W13 | Backlog | Только W13 (март), явный лейбл backlog присвоен, алерт по оплатам не реализован |
| orphan-sweep | corp-youtube#2 | W13 | Backlog | Только W13 + retro:W12 лейблы, нет комментариев, последнее обновление W19 (авто-синк) — за |
| orphan-sweep | vibecoding.phd#85 | W13 | Backlog | Только W13 + retro:W12 лейблы, нет комментариев, последнее обновление W19 — reference-only |
| orphan-sweep | vibehack#2 | W13 | Backlog | Только W13 + retro:W12 лейблы, нет комментариев, vibehack-2 так и не спланирован |
| orphan-sweep | teach-vibecoding#205 | W15 | Backlog | Только W15 лейбл, нет комментариев, аутрич на менти не стартовал — застарело |
| orphan-sweep | corp-tg-ris-ai#3 | W15 | Backlog | Только W15 лейбл, нет комментариев, Facebook/Threads перезапуск не начат |
| orphan-sweep | teach-vibecoding#201 | W15 | Backlog | Только W15 + mentee:arkady лейблы, нет комментариев — сессия 2 с Аркадием давно прошла, is |
| orphan-sweep | vibecoding.phd#86 | W20 | Backlog | W20 лейбл, нет комментариев, Кружок S11 уже стартовал и завершился — задача устарела |
| orphan-sweep | crm#17 | W16 | Backlog | Только W16 лейбл, нет комментариев, Михаил Скляренко follow-up не сделан — сделка зависла |
| orphan-sweep | personal-corp#44 | W20 | Backlog | Carry-over с W17 до W20, последний комментарий W20 говорит «финальное решение в W20 close/ |
| orphan-sweep | corp-tg-ris-ai#5 | W18 | Backlog | Только W18-лейбл, нет комментов и прогресса, задача не начата, устарела с мая 2026 |
| orphan-sweep | hq#162 | W18 | Backlog | Только W18-лейбл, стратегический вопрос по cross-repo labels завис без решения, нет активн |
| orphan-sweep | teach-vibecoding#203 | W18,W20 | Backlog | Evergreen профиль менти Тимофея — S3 и S4 не закрыты, нет активности с W20 (май 2026) |
| orphan-sweep | teach-vibecoding#225 | W18 | Backlog | Seed-задача на L3 без комментов и прогресса, только W18-лейбл, статус тела «seed» |
| orphan-sweep | teach-vibecoding#254 | W18 | Backlog | Сессия 3 Тимофея — все чекбоксы пустые, нет комментов, нет активности с W18 (май 2026) |
| orphan-sweep | hq#163 | W18 | Backlog | Только W18, нет комментариев, нет активности с 09.05 — застарела |
| orphan-sweep | teach-vibecoding#258 | W20 | Backlog | Spillover W18→W20, последняя активность 12.06, нет свежей работы в W25-W26 |
| orphan-sweep | hsl-mozg#156 | W20 | Backlog | Spillover W18→W20, ретроспективный TG-опрос так и не отправлен, нет активности с 12.06 |
| orphan-sweep | teach-vibecoding#260 | W20 | Backlog | Smena retreat прошёл в мае, эпик не закрыт, нет активности с 14.05 |
| orphan-sweep | hsl-mozg#158 | W20 | Backlog | Spillover W18→W20, source attribution не реализована, нет активности с 14.05 |
| orphan-sweep | hq#167 | W20 | Backlog | Spillover W18→W20, positioning canon и filter policy не определены, нет активности с 14.05 |
| orphan-sweep | corp-sales#2 | W20 | Backlog | Spillover W18→W20, 4-vector backfill Apr 2026 не завершён, нет активности с 14.05 |
| orphan-sweep | crm#53 | W20 | Backlog | Invoice для Daniel overdue с 26.04, spillover W18→W20, нет действий founder, Daniel до сих |
| orphan-sweep | crm#54 | W20 | Backlog | Спонсорство TestSprite, окно May 11-18 давно прошло, последняя активность 14.05, только ст |
| orphan-sweep | crm#55 | W20 | Backlog | Спонсорство MagicLight, brief от Jason'а так и не пришёл, активность застыла на 14.05, тол |
| orphan-sweep | crm#57 | W20 | Backlog | Наринский / Кружок #11 (старт 14.05) — событие давно прошло, последнее обновление 30.05, н |
| orphan-sweep | teach-vibecoding#261 | W20,W25 | Backlog | Smena acquisition pivot: W25 лейбл добавлен 20.06, но комментариев нет, Smena retreat (9-1 |
| orphan-sweep | corp-content#2 | W20 | Backlog | Контент-пакет Company Brain / AI OS — только W20, активность с 14.05, публикация не случил |
| orphan-sweep | corp-media#3 | W20 | Backlog | Instagram-карусели готовы (PNG 1080×1080, ZIP), но выбор варианта для публикации завис с 7 |
| orphan-sweep | teach-vibecoding#289 | W20 | Backlog | Smena pre-intro видос записан и залит unlisted (09.05), но delivery в чат участников так и |
| orphan-sweep | teach-vibecoding#290 | W20 | Backlog | Страница smena.vibecoding.phd задеплоена, но само видео #2 не записано и не отправлено; Sm |
| orphan-sweep | teach-vibecoding#291 | W20 | Backlog | В теле явно стоит «Status: backlog (W20)», комментариев нет, Smena завершена, обновлений с |
| orphan-sweep | teach-vibecoding#292 | W20 | Backlog | W20 (май), в теле статус «backlog», дедлайн 15.05 прошёл, нет комментариев и активности |
| orphan-sweep | corp-tg-ris-ai#6 | W20 | Backlog | W20 (май), статус «planned — не начато», нет активности с 14 мая, только старый W20-лейбл |
| orphan-sweep | cohorts#58 | W20 | Backlog | W20 feature-request на Zoom-чат в уроках, нет комментариев и реализации, застарело |
| orphan-sweep | crm#58 | W20 | Backlog | W20, большой scope (~8-10ч) на нормализацию CRM-ссылок, нет активности и комментариев с ма |
| orphan-sweep | crm#36 | W20 | Backlog | W20, дедлайн 14.05 прошёл, статус «open» в теле, нет активности с мая |
| orphan-sweep | crm#38 | W20 | Backlog | W20, статус «open» в теле, шаблоны check-in не созданы, нет активности с мая |
| orphan-sweep | crm#44 | W20 | Backlog | Smena pilot завершился (W20, май 2026), дедлайн 14.05 просрочен, нет комментариев и активн |
| orphan-sweep | crm#45 | W20 | Backlog | Smena pilot прошёл, дедлайн 08.05 просрочен, нет комментариев — вопрос об outcome потерял  |
| orphan-sweep | teach-vibecoding#255 | W20 | Backlog | Только W20-лейбл, нет комментариев, updatedAt 12.06 — системное обновление без прогресса,  |
| orphan-sweep | teach-vibecoding#300 | W20 | Backlog | Преза к L4 (11.05) не создана, лайв давно прошёл, нет комментариев — окно доставки упущено |
| orphan-sweep | corp-community#2 | W20 | Backlog | Перенесена в W24 (10.06), но W24 прошла, issue открыт — рубрика так и не запущена |
| orphan-sweep | corp-community#3 | W20 | Backlog | Мини-формат перенесён в W24 (13.06), W24 прошла, issue открыт — рубрика не запущена |
| orphan-sweep | teach-vibecoding#321 | W23 | Backlog | Status: planned, создан 07.06, нет комментариев за 18 дней — сбор артефактов не начат, Кру |
| orphan-sweep | crm#13 | W15 | Backlog | W15 (апрель), последнее обновление 2026-05-09, нет комментариев — трек завис без движения  |
| orphan-sweep | hsl-mozg#226 | W25 | Backlog | Явно помечен POST-MVP, нужен только для будущих потоков. Нет W26-активности и комментариев |
| orphan-sweep | cohorts#84 | W25 | Backlog | Только W25-лейбл, последнее обновление 22.06 (аудит), нет W26-активности и комментариев. |
| orphan-sweep | hsl-mozg#160 | W20 | Done | PR merged в main 2026-05-05, задеплоен в прод (Railway), все тесты зелёные — issue OPEN фо |
| orphan-sweep | teach-vibecoding#306 | W20 | Done | Артефакт index.html для Кружка #11 создан 2026-05-15, секция «Что сделано» описывает завер |
| orphan-sweep | crm#37 | W20 | Done | Профили 5 участников Смены distilled 2026-05-11, артефакт создан (smena-kash-qa-blueprint. |
| orphan-sweep | dotclaude#11 | W25 | In progress | Основная работа выполнена и задокументирована в комментах (2026-06-20, W25), 2 пункта откр |
| orphan-sweep | cohorts#55 | W18,W20 | In review | Фикс задеплоен 2026-05-13 (W20), тело issue обновлено до «fixed, no known runtime blocker» |
| orphan-sweep | hsl-mozg#151 | W18 | In review | Деплой прошёл успешно 2026-04-24, в комментах «Deployment resolved successfully», остались |
| orphan-sweep | hsl-mozg#154 | W18 | In review | Код реализован на ветке codex/personal-corp-lms-access, тесты прошли (8+8 passed), не заде |
| orphan-sweep | teach-vibecoding#231 | W18 | In review | OH-01 опубликован на YouTube, страница задеплоена, URLs верифицированы (200/401) в апреле  |
| orphan-sweep | crm#51 | W20 | In review | Свежий анализ tg-telethon сегодня (W26): тишина 43 дня, сделки нет — ждёт решения founder  |
| orphan-sweep | teach-vibecoding#288 | W20 | In review | Комментарий от 22.06 фиксирует: Олег закрыл тему на фидбек-созвоне, «можно закрывать» — жд |
| orphan-sweep | teach-vibecoding#320 | W23 | In review | Комментарий от 07.06: форма создана, текст для поста готов — «Готово для финального опроса |
| orphan-sweep | teach-vibecoding#348 | W27 | Ready | Запланировано на W27 (лайв 02.07), статус 'planned', задачи не начаты, нет комментариев |
| orphan-sweep | teach-vibecoding#349 | W27 | Ready | Запланировано на W27 (середина недели, 2026-06-30), статус 'planned', нет активности |
| orphan-sweep | teach-vibecoding#350 | W27 | Ready | Запланировано на W27 (в течение недели, 2026-07-02), статус 'planned', нет активности |
| orphan-sweep | teach-vibecoding#351 | W27 | Ready | Запланировано на D+1 после лайва (2026-07-03), статус 'planned', нет активности |
| orphan-sweep | teach-vibecoding#352 | W28 | Ready | Запланировано на W28 (2026-07-03, после L4), статус 'planned', нет активности |
| orphan-sweep | teach-vibecoding#353 | W28 | Ready | Запланировано на W28 (2026-07-04, после ретро), статус 'planned', нет активности |
| orphan-sweep | hsl-mozg#225 | W25 | Ready | MVP сформулирован и уточнён 2026-06-22 (W25), задачи чётко определены, работа не начата |
| w26-triage | teach-vibecoding#346 | W26 | In progress | Коммуникационное окно 22–25.06 активно сегодня, лайв L3 сегодня — задача в процессе выполн |
| w26-triage | vibecoding.phd#91 | W26 | In progress | Issue открыт, дедлайн 24.06 прошёл; агент подготовил драфт и временный FAQ-сабдомен, но ос |
| w26-triage | corp-youtube#33 | W26 | In review | Агент завершил все задачи (research + драфты писем), все [founder] чекбоксы висят — ждёт п |
| w26-triage | teach-vibecoding#345 | W26 | Ready | Issue открыт, все чекбоксы пусты, комментариев нет — работа не начата; body сам говорит "S |
| w26-triage | corp-youtube#34 | W26 | Ready | Issue открыт, нет комментариев и обновлений с момента создания — работа ещё не начата, тол |
| w26-triage | corp-youtube#36 | W26 | Ready | Issue открыт, комментариев нет, обновлений с 21 июня не было — работа не начата |
| w26-triage | corp-content#8 | W26 | Ready | Бриф полностью готов (таймлайн, угол, источники), но дедлайн Пн 22.06 прошёл, пост не опуб |
| w26-triage | corp-content#9 | W26 | Ready | Шаблоны готовы, но запуск ждёт решений founder — работа не начата, активности нет |
| w26-triage | teach-vibecoding#367 | W26 | Ready | Issue открыт, все чеклист-пункты не отмечены, комментариев нет — работа не начата, только  |

</details>
## Архив Done
Критерий: Status=Done **И** issue CLOSED **И** не W26 (W26-Done оставлены для ретро, Done-but-open оставлены). Итог: **434 заархивировано, 0 ошибок** (334 в первом проходе + 100 после сброса GraphQL-лимита). Обратимо через `--undo`.
## Грабли / на улучшение алгоритма
- Bulk `item-edit`/`item-archive` выжигают GraphQL 5000 pts/h; gh маскирует исчерпание ошибкой **`unknown owner type`**. Проверять `gh api rate_limit -q .resources.graphql`, при `remaining:0` ждать `reset` (epoch). → паковать в батчи, ставить паузу/ретрай, либо архивировать реже.
- Агент-эвристика «застарелое ⇒ Backlog» дала 56/83 Backlog — много старых недель (W13–W20) реально мертвы. Стоит ли их вообще держать на доске vs закрывать issue — открытый вопрос для следующего разбора.
- `In review` ставился по «задеплоено, ждёт верификации след. платежа» — проверить, не пора ли часть закрыть (hsl-mozg #151, cohorts #55).
## За founder (UI, API не умеет)
Week → «…» → Group by → Status; сохранить фильтр `W26` (менять еженедельно).
## Связанное
- Память: `project4-orphan-tasks-diagnosis` (ids, команды, rate-limit caveat).
- Машинный лог: `process-logs/triage-decisions.jsonl` (этот прогон = run `2026-06-25-project4-orphan-triage`).
- Сырые транскрипты агентов (полный issue-контент + рассуждение): `subagents/workflows/wf_b810f9a9-cd3` (sweep), `wf_c7c3347a-1f8` (W26) под session-dir.
