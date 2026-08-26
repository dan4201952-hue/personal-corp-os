# 2026-06-17 — корневой фикс повторяющихся падений manager (gh обходит --jq на errors)

Follow-up к `hq#210` (2026-06-10 оптимизация запросов). Симптом founder'а: «на чистом контексте 1 из 3 вызовов — ошибка». В транскриптах два паттерна:
- `gh search issues --state all` → `invalid argument "all"` (валидны только open/closed);
- GraphQL-ответ → Python-инлайн `d['data']` → `KeyError: 'data'`.

## Корневая причина (верифицирована live)

Когда в ответе GraphQL есть массив `errors` (хоть один упавший alias, хоть тотальный провал запроса), **`gh api graphql` полностью игнорирует флаг `--jq`**: валит сырой JSON-body в stdout + короткую ошибку в stderr, exit 1. Guard `(.data // {})` внутри `--jq` при этом не выполняется — флаг обойдён.

- Тотальный провал → body = `{"errors":[...]}` без ключа `data`. Любой downstream `d['data']` (Python) → `KeyError: 'data'`.
- Partial провал → body = `{"data":{...},"errors":[...]}` сырой, downstream получает не то, что ждал.

Прошлая правка пыталась лечить это guard'ом `(.data // {})` *внутри* `--jq` — бесполезно, т.к. `--jq` обходится.

## Что верифицировано

| Случай | `--jq` (старое) | `| jq -r` (новое) |
|---|---|---|
| успех | ✓ | ✓ |
| partial error | сырой JSON, --jq обойдён | живые alias'ы, exit 0 |
| total error | сырой JSON без data → KeyError downstream | пусто, exit 0, без краша |

`gh search issues` без `--state` возвращает open+closed одним вызовом (62+10 на W25); GraphQL `is:issue` без `state:` — то же одним alias. Два вызова/два alias на open+closed = лишний расход REST-лимита 30/мин.

## Патч

- search-algorithm.md: убран хардкод `--state open`; оба статуса = опустить квалификатор (один вызов / один alias); все `gh api graphql ... --jq` → `... | jq -r '(.data // {}) | ...'`; добавлен CRITICAL-блок про обход `--jq`; запрет Python-инлайна `d['data']`.
- parent-epic-rules.md: per-candidate REST-loop (`для каждого gh api repos/.../issues/N`) → один batched GraphQL `subIssuesSummary`, через `| jq -r`.
- modes-read-write.md: read-mode step 2/4 — multi-key и per-match чтение → batched GraphQL, без per-issue `gh issue view`.

Финальный прогон: 7/7 команд скилла exit 0, форс тотального провала через `| jq -r` → пусто без краша, `--state all` остаётся невалидным (документировано как запрет).
