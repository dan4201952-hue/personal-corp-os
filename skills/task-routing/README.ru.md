# Скилл Task Routing

![Иллюстрация скилла](assets/illustration.png)

Скилл Claude Code для маршрутизации issues в правильный репозиторий через конфиг из CLAUDE.md. Часть фреймворка Personal Corp.

## Проблема

В мульти-репо сетапе issues создаются не там — задачи по боту в стратегическом репо, личные ops-задачи в публичных репо, дубликаты по проектам.

## Решение

Читает routing config из AGENTS.md / CLAUDE.md (созданный или отремонтированный `corp-init`) и матчит ключевые слова задачи с правильным целевым репозиторием.

## Установка

```bash
cp -r skills/task-routing ~/.claude/skills/
```

## Как работает

1. Читает routing patterns из CLAUDE.md
2. Матчит описание задачи → целевой репо
3. Проверяет дубликаты в целевом репо и едином проекте
4. Проверяет наличие W-label (никогда не создаёт — это работа `weekly-planning`)
5. Создаёт issue в правильном репо

## Часть фреймворка Personal Corp

```
corp-init → task-routing → weekly-planning / weekly-retro
     ↑               ↑              ↑
 (настройка)   (ежедневная)    (недельный цикл)
```

## Связанные скиллы

- [corp-init](../corp-init/) — создаёт или ремонтирует routing конфиг
- [weekly-planning](../weekly-planning/) — создаёт W-labels и приоритизирует
- [weekly-retro](../weekly-retro/) — создаёт бэклог из ретро
