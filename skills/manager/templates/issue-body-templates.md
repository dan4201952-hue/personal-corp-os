# Manager — body templates

Источник: вынесено из SKILL.md 2026-06-10 (`hq#210`). Читать перед `gh issue create` / `gh issue edit --body-file`.

## Issue body template (when creating new)

Before using any template in a public repo, replace private absolute paths, CRM slugs, personal handles, payment facts, raw Telegram/Zoom URLs, and local-only evidence with safe public pointers. If no safe public pointer exists, write the exact private pointer only in the private owner repo or internal report.

```markdown
<one-line context: what changed/what was made>

**Source artifact:** <absolute path or URL>
**Date:** <YYYY-MM-DD>
**Track:** <link to opp/contact card if commercial or mentoring — `[[crm-slug]]`>

## Что сделано
<2-4 bullets — what's the actual progress>

## Next step
<one line — what closes this issue>

## Related

- repo#N «человекочитаемый заголовок» — краткая причина связи

**Verified:** <YYYY-MM-DD> by manager

Omit the whole `Related` block when there are no verified context links.

---
Synced by manager from session <YYYY-MM-DD>.
```

### Mentoring body template

Для mentoring session issue использовать короткий delivery-шаблон без денег:

```markdown
Сессия <N> для [[crm-slug]].

**Status:** <planned / held / delivery pending / delivered>
**Next:** <одно конкретное действие по prep или delivery>
**CRM:** [[crm-slug]]
**Дата сессии:** <YYYY-MM-DD HH:MM TZ или exact blocker>

## Scope
- prep / agenda
- факт проведения
- post-session delivery: recording, transcript, workbook, LMS/runtime, student link

## Related

- repo#N «человекочитаемый заголовок» — краткая причина связи

**Verified:** <YYYY-MM-DD> by manager

Omit the whole `Related` block when there are no verified context links.

## Delivery checklist
- [ ] Recording/video status
- [ ] Транскрипт и заметки источника
- [ ] Workbook/summary
- [ ] LMS/runtime link
- [ ] Link sent to student

## Updates

- **YYYY-MM-DD:** <что изменилось по session delivery>
```

Запрещено в этом шаблоне: суммы, цены, paid/won, остаток пакета, «закрыть сделку». Эти факты живут в CRM/ledger.

## PRD issue body template

Для планировочного issue (PRD / план системы / mini-PRD при weekly planning) полный текст живёт в body — issue является источником истины. Локальная полная копия файла в репо нужна и остаётся; `Source artifact` указывает на неё кликабельным GitHub-URL **после commit+push**.

```markdown
<one-line: что за система и зачем>

**Status:** prd-draft / prd-accepted / in-build
**Next:** <одно действие — обычно «приёмка PRD founder'ом» или первый MVP-slice>
**Source artifact:** https://github.com/<owner>/<repo>/blob/main/<path>.md (закоммиченная копия PRD)
**Date:** <YYYY-MM-DD>
**Track:** <домен/потребитель>

---

# <Название> — PRD

## Контекст
<1 абзац: кто потребитель, какую боль закрывает>

## Что уже есть (разведка)
<таблица: Источник/Компонент | Покрытие | Пробел — с фактами и датой разведки>

## Ключевые решения
<таблица: Вопрос | Решение | Обоснование>

## Архитектура
<mermaid-блок — GitHub рендерит его прямо в body issue>

## Схема данных
<если есть>

## MVP-этапы
<нумерованный список slice'ов>

## Вне scope
<что сознательно не делаем + указатели на смежные треки>

## Открытые вопросы
<нумерованные, self-contained — каждый читается без back-reference>

---

## Related

- repo#N «человекочитаемый заголовок» — краткая причина связи

**Verified:** <YYYY-MM-DD> by manager

## Updates

- **YYYY-MM-DD:** <разведка/решения этого синка>
```

Правила: mermaid вставлять как есть (рендерится в GitHub issues); локальные пути — только как системные указатели (DB, cwd автоматизаций), deliverable-ссылки — кликабельные GitHub-URL после commit+push.

## Body update template (default)

When updating issue body via `gh issue edit --body-file`:

```markdown
<one-line context: what changed/what was made — same as before, refresh if scope changed>

**Status:** <active / blocked / pending external / done — only "done" if founder said so>
**Next:** <one-line next concrete step — refresh on each sync>

Before writing, remove any old `## Related` block from `[... rest of original body content ...]`; then insert at most one fresh verified block when useful.

## Updates

- **YYYY-MM-DD:** <2-4 bullets of progress / decisions / shifts in this sync>
- **YYYY-MM-DD:** <previous sync entry, kept>
- ...

## Related

- repo#N «человекочитаемый заголовок» — краткая причина связи

**Verified:** <YYYY-MM-DD> by manager

Omit the whole `Related` block when there are no verified context links.
```

Newest update at top of `## Updates` section, oldest at bottom (or vice versa — pick once per issue and stay consistent within it).

## Comment template (fallback only)

Use when comment is genuinely ephemeral / chronological context (see "Comment is fallback" rule).

```markdown
**YYYY-MM-DD:** <one-line note that doesn't fit body — e.g. "external blocker until X", "transient state observation">
```

Keep comments short. If a comment grows beyond 4 lines — it belongs in body.
