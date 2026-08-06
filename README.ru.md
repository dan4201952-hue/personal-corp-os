# Personal Corp OS

[![en](https://img.shields.io/badge/lang-en-blue.svg)](README.md)
[![ru](https://img.shields.io/badge/lang-ru-green.svg)](README.ru.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Validate](https://github.com/serejaris/personal-corp-os/actions/workflows/validate.yml/badge.svg)](https://github.com/serejaris/personal-corp-os/actions/workflows/validate.yml)

> Personal Corp — способ управлять личной компанией через AI-агентов: задачи вне головы, отделы вместо памяти одного человека, недельное ретро вместо «когда-нибудь разберусь».

Здесь лежит всё, что для этого нужно: рассказ, как система устроена, шаблоны штаба и отдела, и открытые скиллы для [Claude Code](https://docs.anthropic.com/en/docs/claude-code) и Codex.

От [Ris](https://t.me/ris_ai) — пишу про AI-разработку и вайбкодинг.

English version: [README.md](README.md).

## Проблема: вы бутылочное горлышко

Не потому что мало работаете. Потому что стратегия, память, координация, исполнение и приёмка лежат в одной куче — у вас в голове. Пока это так, пропускная способность отдела равна вашей.

Найм не расшивает горлышко: человек забирает работу, но не контекст, и вы продолжаете объяснять. ИИ сам по себе тоже не расшивает: агент без контекста — тот же новый сотрудник, только он ещё и не помнит вчера.

Дело не в силе модели. Дело в том, что контекст не выходит из головы.

## Главная идея: представление задаёт папка

Правила лежат в каждой папке. Запускаете агента из штаба — он видит карту всей системы. Запускаете из отдела — видит свой домен, свои задачи и свои скиллы. Модель одна и та же, представление разное, потому что его задаёт папка, а не длинный промпт.

Отсюда всё остальное: чтобы это работало, контекст должен выйти из головы в файлы, а файлы — лечь по папкам с правилами.

## Четыре слоя и кто где живёт

| Слой | Кто действует | Что здесь лежит |
|---|---|---|
| Управления | Человек | Цель, приоритеты, лимиты, право сказать «годится» |
| **Правды** | Человек пишет, агент читает | Правила, память, индексы, источник правды |
| **Операционный** | Агент исполняет, человек принимает | Задачи, очередь, статусы, прогоны, отделы |
| Наблюдения | Агент собирает, человек смотрит | Дашборды, метрики, блокеры |

Субагент живёт только в операционном слое: он не пишет правду о системе и не принимает результат.

Тест для любого файла: **это правда о системе или это результат работы?** Правда лежит в папке с самого начала. Результат создаёт скилл, когда ему есть что записать. Поэтому в шаблонах нет пустых файлов под будущие отчёты, решения и словари.

## Маршрут: как опыт становится капиталом

```mermaid
graph LR
    A["Задача<br/>владелец + критерии"] --> B["Исполнение<br/>человек или агент"]
    B --> C["Приёмка<br/>годится или нет"]
    C --> D["Паттерн<br/>что сработало"]
    D --> E["Память отдела<br/>правила и решения"]
    E --> F["Приоритет<br/>следующая неделя"]
    F --> A
    style A fill:#8b5cf6,color:#fff
    style C fill:#f59e0b,color:#fff
    style E fill:#10b981,color:#fff
```

**1. Описание задачи.** Мысль становится задачей, когда у неё есть владелец, критерии готовности и место, где она лежит. До этого она живёт в вас. После — её может взять и человек, и агент.

**2. Накопление опыта в отделах.** Артефакты и решения оседают в отделе — отдельной папке своего домена. В следующий раз агент читает не вас, а отдел.

**3. Ретро с агентом.** Раз в неделю вы вместе смотрите, что сработало, и поднимаете это в правила. То, что вы поправили дважды, становится строкой правил и больше не требует вашего участия.

## Недельный ритм

Три звена по отдельности — список возможностей. Ритм превращает их в систему.

```mermaid
graph LR
    R["ретро<br/>что сработало"] --> P["планирование<br/>приоритеты недели"]
    P --> T["задачи<br/>по отделам"]
    T --> E["исполнение<br/>след возвращается в задачу"]
    E --> R
    style R fill:#f59e0b,color:#fff
    style P fill:#3b82f6,color:#fff
    style T fill:#8b5cf6,color:#fff
    style E fill:#10b981,color:#fff
```

Ритм отвечает на вопрос, который обычно остаётся без ответа: когда именно опыт превращается в правило. Ответ: на ретро, раз в неделю, а не «когда-нибудь потом».

Одно и то же слово даёт разный результат в зависимости от папки: «ретро» в отделе — срез этого отдела, «ретро» в штабе — срез всей системы. Правила папки сильнее общих.

## Три уровня задач

Начинайте с первого. Переходите дальше, только когда предыдущий начал мешать.

| Уровень | Как выглядит | Когда пора |
|---|---|---|
| 1 | Один `tasks.md` — задачи на сегодня в одном месте | Всегда, это старт |
| 2 | День, длительные задачи и история разложены по файлам | Когда контекст задач приходится помнить головой |
| 3 | Состояние длительных задач в GitHub Issues, день — короткий список со ссылками | Когда появляются несколько репозиториев или совместная работа |

## Шаблоны

| Шаблон | Что это |
|---|---|
| [`templates/hq`](./templates/hq/) | Штаб — точка входа агента и карта системы |
| [`templates/department`](./templates/department/) | Отдел — папка одного домена со своими задачами и скиллами |

Отделы лежат **рядом со штабом, не внутри него**. Каждый файл шаблона открывается строкой «зачем он здесь и к какому слою относится».

## Первый шаг: 30 минут сегодня

1. Скопируйте [`templates/hq`](./templates/hq/) к себе и заполните `me.md`.
2. Откройте агента из этой папки и попросите прочитать `AGENTS.md`.
3. Заведите первый отдел из [`templates/department`](./templates/department/) рядом со штабом и положите в него одну реальную задачу.
4. Поставьте плагин (см. [Установка](#установка)) — он приносит скиллы недельного ритма.
5. В конце недели запустите ретро, в начале следующей — планирование.

После двух таких недель у отдела появляется собственная память, и часть решений перестаёт проходить через вас.

## Шесть скиллов маршрута

| Скилл | Звено маршрута | Что делает |
|-------|----------------|------------|
| [corp-init](./skills/corp-init/) | Контур | Настройка или ремонт HQ, GitHub issue workflow, corp-* owner map и agent config |
| [corp-new](./skills/corp-new/) | Отдел | Регистрация приватного corp-* репозитория отдела и HQ-записи после подтверждения |
| [task-routing](./skills/task-routing/) | Задача | Маршрутизация issues в правильный репозиторий через конфиг |
| [manager](./skills/manager/) | Исполнение | Синк работы сессии в GitHub Issues и cross-repo запросы по задачам |
| [weekly-retro](./skills/weekly-retro/) | Паттерн в память | Структурированное ретро: сбор данных, интервью с основателем, фиксация в issues |
| [weekly-planning](./skills/weekly-planning/) | Приоритет | Ретро и бэклог — приоритизированные outcomes с матрицей Эйзенхауэра |

## Куда это ведёт

| Стадия | Как думаете | Где горлышко |
|--------|-------------|--------------|
| Вайбкодер | «Я и AI» | Контекст в голове |
| Оператор | «Я направляю агентов» | Координация вручную |
| CEO | «Я управляю системой» | Горлышка нет, система работает |

Ваша работа сжимается до трёх действий: задать цель, выбрать следующий ход, принять результат.

Словарь терминов — [CONTEXT.md](CONTEXT.md). Принятые архитектурные решения — [docs/adr/](docs/adr/).

## Установка

### Claude Code

В терминале:

```bash
claude plugin marketplace add serejaris/personal-corp-os
claude plugin install personal-corp-os@personal-corp-os
claude plugin details personal-corp-os
```

В Claude Code Desktop или interactive `/plugin` flow:

1. Откройте **Plugins** или `/plugin`.
2. Добавьте marketplace: `serejaris/personal-corp-os`.
3. Установите `personal-corp-os`.

### Codex

В репозитории есть Codex manifest: [.codex-plugin/plugin.json](.codex-plugin/plugin.json).
Добавьте marketplace из GitHub, затем установите плагин:

```bash
codex plugin marketplace add serejaris/personal-corp-os
codex plugin add personal-corp-os@personal-corp-os
```

После установки откройте новый Codex thread и проверьте:

```text
Use Personal Corp skills to plan my week.
```

### Переход с personal-corp-skills

До 06.08.2026 репозиторий назывался `personal-corp-skills`. Старые ссылки GitHub перенаправляет сам. Плагин переименован вместе с репозиторием, поэтому в Claude Code удалите установленный плагин `personal-corp-skills` через `/plugin` и поставьте новый по инструкции выше.

### Один скилл

Используйте этот вариант, если нужна одна папка скилла:

> Install this skill: `https://github.com/serejaris/personal-corp-os/tree/main/skills/cc-analytics`

Замените `cc-analytics` на имя любого скилла из таблицы ниже.


## Все скиллы
| Скилл | Что делает |
|-------|-----------|
| [art-director](./skills/art-director/) | Итеративный поиск визуального стиля с промптами, журналом процесса, ассетами и графами решений |
| [product-data-audit](./skills/product-data-audit/) | Глубокий аудит продукта/бизнеса — интерактивный HTML-отчёт на 12 секций |
| [cc-analytics](./skills/cc-analytics/) | HTML-отчёты статистики использования Claude Code |
| [ceo-council](./skills/ceo-council/) | Параллельные субагенты в роли C-level экспертов для стратегического анализа |
| [claude-md-writer](./skills/claude-md-writer/) | Создание и рефакторинг CLAUDE.md по best practices |
| [corp-new](./skills/corp-new/) | Добавление приватного corp-* репозитория отдела и HQ-записи после подтверждения |
| [safe-public-release](./skills/safe-public-release/) | Provenance, лицензии, security allowlist, approval и fresh-clone проверка публичных артефактов |
| [design-minimal](./skills/design-minimal/) | Одна HTML-страница в минимальном стиле для дашбордов, брифов, раздаток и отчётов |
| [gh-issues](./skills/gh-issues/) | Управление GitHub Issues через CLI с хранением контекста сессий |
| [meeting-copilot](./skills/meeting-copilot/) | Live dashboard для встреч: подготовка, обновление из транскрипта, закрытие с решениями и follow-up |
| [readme-generator](./skills/readme-generator/) | Человеко-ориентированные README с правильной структурой |
| [manager](./skills/manager/) | Двусторонний мост между текущей сессией и GitHub Issues |
| [idea](./skills/idea/) | Захват одной озвученной идеи в папку-с-провенансом, дедуп по индексу, опциональное зеркало в GitHub Project |
| [pm-prioritize](./skills/pm-prioritize/) | Ранжирование бэклогов через RICE, ICE, MoSCoW или Kano |
| [pm-prd](./skills/pm-prd/) | Генерация структурированного PRD с шаблонами под тип продукта |
| [pm-user-stories](./skills/pm-user-stories/) | Разбивка Epic на User Stories с INVEST и Story Map |
| [pm-competitive](./skills/pm-competitive/) | Конкурентный анализ: SWOT, feature-матрица, дифференциация |
| [pm-feedback](./skills/pm-feedback/) | Классификация фидбека, кластеризация тем, ранжирование болей |
| [pm-brainstorm](./skills/pm-brainstorm/) | Структурированный продуктовый брейншторм с SCAMPER |
| [pm-metrics](./skills/pm-metrics/) | Ревью продуктовых метрик, воронка/retention, OKR alignment |
| [pm-roadmap](./skills/pm-roadmap/) | Обновление roadmap Now/Next/Later с атрибуцией задержек |
| [html-draft](./skills/html-draft/) | Одна HTML-диаграмма в стиле плоского инженерного чертежа — архитектура, потоки, spec sheets |
| [parallel-design-variants](./skills/parallel-design-variants/) | Параллельный design bake-off: N разных направлений через субагентов, галерея, голосование, потом микс победителей |
| [fable-ruki-agenty](./skills/fable-ruki-agenty/) | Ручной режим оркестрации: Fable пишет самодостаточные спеки в тела GH issues и раздаёт готовые задачи субагентам на Sonnet; сам код не пишет |
| [grill-me](./skills/grill-me/) | Безжалостное интервью по плану, по одному вопросу за раз, до общего понимания; каждая развилка — явное решение с рекомендацией |
| [to-prd](./skills/to-prd/) | Синтез обсуждения в `PRD.md` в папке проекта — без интервью; швы для тестов; цепочка после grill-me |
| [to-issues](./skills/to-issues/) | Разбивка PRD/спеки на `tasks/NN-slug.md` — вертикальные tracer-bullet срезы, критерии приёмки и зависимости |
| [tg-bot-ops](./skills/tg-bot-ops/) | Переиспользуемый операционный плейбук для Telegram-ботов и Telegram-to-agent gateways |

### Дизайн и медиа

| Скилл | Когда использовать |
|-------|--------------------|
| [art-director](./skills/art-director/) | Итеративный art direction, поиск визуального стиля, ветки генерации и графы решений |
| [design-minimal](./skills/design-minimal/) | Читаемые standalone HTML-страницы: дашборды, брифы, раздатки, операционные карты, отчёты |
| [html-draft](./skills/html-draft/) | Технические диаграммы в стиле плоского инженерного чертежа: архитектура, system flows, spec sheets |
| [parallel-design-variants](./skills/parallel-design-variants/) | Несколько по-настоящему разных дизайн-направлений на выбор — редизайн, hero, лендинг, обложка; лайв-bake-off с голосованием |

### Продуктовые скиллы

| Скилл | Когда использовать |
|-------|--------------------|
| [pm-feedback](./skills/pm-feedback/) | Отзывы, NPS или саппорт-тикеты — нужна кластеризация тем и ранжирование болей |
| [pm-competitive](./skills/pm-competitive/) | Вход в категорию, fundraising или дифференциация перед PRD |
| [pm-brainstorm](./skills/pm-brainstorm/) | Структурированная дивергенция перед квартальным планированием |
| [pm-prioritize](./skills/pm-prioritize/) | Бэклог слишком большой — RICE, ICE, MoSCoW или Kano |
| [pm-prd](./skills/pm-prd/) | Top-требованиям нужен PRD для ревью и разработки |
| [pm-user-stories](./skills/pm-user-stories/) | PRD или Epic готов к разбивке на User Stories |
| [pm-metrics](./skills/pm-metrics/) | Еженедельный/месячный обзор метрик, A/B, pacing OKR |
| [pm-roadmap](./skills/pm-roadmap/) | Закрытие спринта или стейкхолдер-ревью — обновить roadmap |

```mermaid
graph LR
    pmFeedback[pm-feedback] --> pmPrioritize[pm-prioritize]
    pmCompetitive[pm-competitive] --> pmPrioritize
    pmBrainstorm[pm-brainstorm] --> pmPrioritize
    pmPrioritize --> pmPrd[pm-prd]
    pmPrd --> pmUserStories[pm-user-stories]
    pmMetrics[pm-metrics] --> pmRoadmap[pm-roadmap]
    pmRoadmap --> pmPrioritize
```

### Telegram

| Скилл | Когда использовать |
|-------|--------------------|
| [tg-bot-ops](./skills/tg-bot-ops/) | Инциденты Telegram-ботов и Telegram-to-agent gateways, webhook/polling diagnostics, безопасный restart, Bot API smoke tests, delivery в forum topics |


## Other

### [Statusline](./statusline/)
Кастомный статусбар с отображением затрат, использования контекста и git-ветки с цветовой индикацией.

## Архивные скиллы

Архивные скиллы сохраняются для справки и не входят в активный набор скиллов
плагина.

| Скилл | Примечание |
|-------|------------|
| [paperclip-api](./archive/skills/paperclip-api/) | Исторический helper для Paperclip API; сохранён для справки |

## Ручная установка

Скиллы — обычные папки. Копируйте всю папку скилла, чтобы не потерять optional
references и examples:

```bash
cp -r skills/<name> ~/.claude/skills/
```

## Автор

- Telegram: [@ris_ai](https://t.me/ris_ai) — AI-разработка и вайбкодинг
- YouTube: [@serejaris](https://www.youtube.com/@serejaris)
- [vibecoding.phd](https://vibecoding.phd)

## Лицензия

MIT

## Безопасность

Секреты, утечки приватных данных и exploitable behavior отправляйте приватно.
См. [SECURITY.md](SECURITY.md).
