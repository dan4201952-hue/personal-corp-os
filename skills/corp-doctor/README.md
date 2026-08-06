# Corp Doctor

One entry point for every operation on a Personal Corp loop: diagnose, repair, add a department, or route a task.

The skill opens with a menu and waits for an explicit choice, so it never rebuilds a working setup blindly.

| Menu item | What happens |
|---|---|
| Diagnose | Read-only pass over the HQ, the operations layer, and the departments; returns a table of mismatches |
| Repair | Closes the mismatches found, one agreed change at a time |
| New department | Read-only preflight, dry-run summary, then a private corp-* repo and one row in the HQ map |
| Route a task | Finds the owning department by the routing map, checks duplicates, creates the issue |
| Build from scratch | HQ, agent rules, level-one task file, the first department, and the weekly rhythm |

Replaces the earlier `corp-init`, `corp-new`, and `task-routing` skills.

Русская версия: [README.ru.md](README.ru.md)
