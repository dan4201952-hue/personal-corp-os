# 2026-06-10 — оптимизация GitHub-запросов manager

Issue: `hq#210`. Анализ трёх прогонов из транскриптов: тяжёлый sync = ~105 gh-вызовов (22× search REST 30/мин → троттлинг; 2-3 round-trip на issue; повторные field-list/label list; 4× item-list).

Патч:
- реестр констант project/field/option ids (self-updating таблица);
- канон чтения = batched GraphQL (issue-state: parent+labels+projectItems+status пачкой; верифицирован live на hq#210);
- батч-поиск через GraphQL search() с alias'ами (user:serejaris), вне лимита 30/мин;
- snapshot Project #4 в /tmp/manager-proj4.json один раз за прогон, --limit 1000;
- label fast-path (--add-label сразу, create по ошибке);
- правило параллелизма независимых чтений;
- body-шаблоны вынесены в templates/issue-body-templates.md (998 → 939 строк).

Ожидание: тяжёлый sync ~105 → ~15-20 вызовов, без троттлинга.
