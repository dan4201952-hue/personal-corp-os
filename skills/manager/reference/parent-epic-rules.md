# Parent epic rules — полный свод правил

## ToC
1. [Что считается epic'ом](#что-считается-epicом)
2. [Один epic на issue](#один-epic-на-issue)
3. [Aggregate parent для cross-track issue](#aggregate-parent-для-cross-track-issue)
4. [Project-visible root](#project-visible-root)
5. [Resolve epic — алгоритм при создании / sync issue](#resolve-epic--алгоритм-при-создании--sync-issue)
6. [Нет track-labels](#нет-track-labels)
7. [Проверка перед sync](#проверка-перед-sync)
8. [Смежные задачи / related issues](#смежные-задачи--related-issues)

---

## Что считается epic'ом

- Issue, у которого есть sub-issues (counter `N / M` в шапке)
- Title обычно содержит scope трека: `Кружок #11 — майский поток 2026`, `AI Mindset X26 — программа`, `<сделка> — overview`, `Personal Corp course — delivery v4`
- Epic сам по себе НЕ имеет parent — это корень дерева

---

## Один epic на issue

GitHub поддерживает только один parent через Sub-issues API. Это match: «один трек — одна иерархия». Если кажется, что задача относится к двум трекам — пересмотри scope: вероятно надо разделить на два issue, по одному в каждый трек.

**Не использовать** markdown `Parent: #N`, `Epic: #N`, `Belongs to: #N` в body когда parent установлен через API — это дубликат, который протухает. Parent хранится через GitHub Sub-issues API.

---

## Aggregate parent для cross-track issue

Если issue покрывает 2+ sibling-трека, слоя или deliverable-класса, сначала классифицируй его как aggregate issue. Не привязывай такой issue к первому найденному предметному epic'у, если второй sibling-трек потеряет видимость.

**Признаки aggregate issue:**

- title/body явно содержит несколько sibling-scope: `product + sales`, `strategy + delivery`, `pilot + docs`, `CRM + forecast`, `launch + ops`;
- issue живёт в repo агрегата (`corp-strategy`, `hq`, reporting/forecast/ops repo), а предметные эпики живут в owner repos;
- body говорит про weekly review, close/kill decision, forecast, pipeline, operating review, portfolio snapshot или cross-repo coordination;
- issue обновляет общий индекс, прогноз, heartbeat, dashboard или план, а не один конкретный deliverable.

**Алгоритм:**

1. Найти предметные epic'и для каждого sibling-scope.
2. Найти repo-local aggregate epic: `forecast`, `pipeline`, `portfolio`, `weekly review`, `operating review`, `coordination`, `umbrella`.
3. Если aggregate epic найден — привязать issue к нему и в отчёте писать `parent: aggregate`.
4. Если aggregate epic отсутствует — surface proposal: создать umbrella issue или разделить aggregate issue на отдельные child issue под предметные epic'и.
5. Не писать один и тот же issue child'ом двух epic'ов; GitHub parent остаётся ровно один.

В read/write output явно различай parent type:

- `parent: track` — конкретный предметный трек;
- `parent: aggregate` — forecast/pipeline/portfolio/operating umbrella;
- `parent: runtime` — published/runtime слой;
- `parent: unknown` — parent ещё не найден или требует founder decision.

---

## Project-visible root

Project view группирует работу по видимому root/parent item, а не только по raw `parent_issue_url`. Manager различает:

- **API parent** — прямой parent из GitHub Sub-issues API;
- **visible root** — ближайший parent/track overview/lesson/umbrella issue, который должен быть виден в текущем Project view и по которому founder раскрывает дерево;
- **historical/backlog grandparent** — верхний backlog/strategy parent, который может оставаться вне weekly view, если visible root уже стоит в Project и имеет W-label/status.

**Правило:**

1. Если active/current-week issue не имеет sub-issues и является child delivery/action issue, его API parent или visible root должен быть в `ris © corp` и доменной доске с непустой status lane.
2. Если issue сам является track overview / lesson parent / umbrella (`sub_issues_summary.total > 0`) и уже виден в Project, его backlog/strategy grandparent не обязан попадать в weekly Project. В отчёте писать `parent: historical/backlog`.
3. Если child имеет `parent_issue_url`, но parent item отсутствует в Project view, это `Расхождение Project: parent epic not visible`.
4. Если child-side API показывает `parent: null`, проверь parent `/sub_issues` у вероятного epic. GitHub может читать hierarchy асимметрично; parent `/sub_issues` с child внутри считается proof, но в отчёте помечается как `parent proof: parent sub_issues`.
5. Если Project view фильтрует repo/type так, что parent физически не может появиться, report `Project view limitation` и не перепривязывай child.

---

## Resolve epic — алгоритм при создании / sync issue

1. **Сначала ищи существующий epic** для трека через cross-repo search:
   ```bash
   # Issues с непустым subIssuesSummary.total — кандидаты в epic
   gh search issues --owner serejaris "<track-keyword>" --json repository,number,title,url --limit 20
   # Все кандидаты верифицируй ОДНИМ batched GraphQL-вызовом, не поодиночке:
   gh api graphql -f query='
   query {
     r1: repository(owner:"OWNER1", name:"REPO1") { issue(number:N1) { title subIssuesSummary { total } } }
     r2: repository(owner:"OWNER2", name:"REPO2") { issue(number:N2) { title subIssuesSummary { total } } }
   }' | jq -r '(.data // {}) | to_entries[] | .value.issue | select(. != null) | "\(.title) total=\(.subIssuesSummary.total)"'
   ```
   Рабочий epic обычно имеет `total >= 1`. Новый root issue с ясным track scope и без parent можно предложить/использовать как epic до первого sub-issue, если founder или owner-source подтверждает этот scope.

2. **Канон по доменам:**

   | Track domain | Epic lives in |
   |---|---|
   | Образовательная программа / партнёрство | репо teaching-домена (`teach-vibecoding`, `teach-personal-corp`) |
   | B2B сделка / multi-lane коммерческий трек | `serejaris/crm` (overview-зонт без служебного prefix) |
   | Поток школы | `serejaris/teach-vibecoding` |
   | Продуктовый запуск | репо самого продукта |
   | Research-инициатива | `serejaris/research-corp` |

   Канон роутинга доменов — skill `multi-repo-initiatives` (там же split для потока школы: эпик/программа → `teach-vibecoding`, LMS-публикация → `cohorts` как cross-repo sub-issue).

3. **Если epic'а нет** — manager поднимает в proposal: «нет epic'а для трека X, нужен ли? Если да — создаю в `<repo>` с title `<...>`». **Не создаёт issue без parent'а молча.**

4. **При создании sub_issue** через API:
   ```bash
   CHILD_ID=$(gh api repos/OWNER/REPO/issues/CHILD_NUMBER --jq '.id')
   gh api -X POST repos/EPIC_OWNER/EPIC_REPO/issues/EPIC_NUMBER/sub_issues -F sub_issue_id=$CHILD_ID
   ```

---

## Нет track-labels

Раньше manager создавал labels вида `x26-bloom`, `ai-native-s2`, `<slug>` для cross-repo группировки. **Больше не делаем.**

- Дифференциация трэков идёт через title + epic membership
- Существующие исторические track-labels не удаляем (это история), но и новых не создаём
- Cross-repo навигация по треку = sub_issues epic'а + Project, не label-фильтр

---

## Проверка перед sync

Перед `gh issue edit` / `gh issue create` агент обязан:

```bash
# (1) Если работа с существующим issue — какой у него parent?
gh api repos/OWNER/REPO/issues/N --jq '{parent: .parent_issue_url, sub_summary: .sub_issues_summary}'

# (2) Если parent отсутствует и issue не сам epic — ищи epic, не обходи проверку
```

Surface в proposal явно, какие issue без parent'а и какой epic им предлагается.

---

## Смежные задачи / related issues

`Related` / `Смежные задачи` в body — это только справочные cross-links. Они помогают founder'у увидеть отдельные задачи с общим контекстом, но никогда не создают иерархию.

- Иерархия живёт только в GitHub Sub-issues API (`parent_issue_url`, `sub_issues_summary`).
- Related links подходят для контекстных ссылок, отдельных зависимостей, cross-repo артефактов и исторических задач.
- Current truth живёт в `Status`, `Next`, checklist/scope и `## Updates` основного issue.
- Related block можно удалить без потери владельца, недели, Project placement или дерева Sub-issues.

**Запрещено в related block:** `Parent: #N`, `Epic: #N`, `Belongs to: #N`, ручные списки children/subtasks, status mirror, next-step mirror, W-labels, Project placement, checklist state.

**Persistent body format:**

```markdown
## Related

- repo#N «человекочитаемый заголовок» — краткая причина связи

**Verified:** YYYY-MM-DD by manager
```

Макс. 3 bullet links + одна `Verified` строка. На каждом body sync — перезаписывать из live search, не аппендить бесконечно. Если relevance неочевидна, показывать только в proposal/read-mode report.

**Перед записью body с `Related` — live-verify каждый referenced issue:**

```bash
gh issue view N -R OWNER/REPO --json title,state,url,labels,updatedAt
gh api repos/OWNER/REPO/issues/N --jq '{parent: .parent_issue_url, sub_summary: .sub_issues_summary}'
```

Для active/current-week related refs — также проверить `projectItems`. Если ref missing, closed, parentless, points to another track, has stale W-label, или leaks private/CRM data в public repo — surface `Расхождение related-links` и убрать/доложить до body write.

Для public repos — не копировать private titles, CRM slugs, local paths, personal handles, payment facts, или private URLs. Использовать безопасный public label `private CRM issue — context only`, а точный private pointer хранить в private owner repo/report.
