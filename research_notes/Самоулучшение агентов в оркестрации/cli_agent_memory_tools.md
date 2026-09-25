# Cross-session learning for terminal coding agents: built-in memory, lesson files, reflection commands and hooks (state as of 2026-09-25)

Legend used throughout:
- **[P]** means verified in a primary source fetched in this session (official docs, a repo README, source code or a changelog; accessed 2026-09-25).
- **[S]** means seen only in a web-search result snippet. The page itself was not opened, so treat it as weaker evidence.
- Dates are publication or release dates. Claude Code, Codex and Gemini CLI version dates come from npm publish timestamps ([registry.npmjs.org/@anthropic-ai/claude-code](https://registry.npmjs.org/@anthropic-ai/claude-code), [@openai/codex](https://registry.npmjs.org/@openai/codex), [@google/gemini-cli](https://registry.npmjs.org/@google/gemini-cli)) [P].
- Anything older than 2025 is labelled "background".

## KQ1. Built-in cross-session learning features per product (2026): what is captured automatically vs manually, where it is stored, how bloat is controlled

### Takeaway
By late 2026 the three big terminal CLIs each have first-party auto-memory, and each takes a different stance:
- **Claude Code**: auto memory, always on by default. It records user preferences, corrections and project context, not debugging or process fixes.
- **Codex CLI**: an opt-in two-phase background pipeline whose extraction prompt explicitly targets "fewer tool calls and fewer reasoning tokens". It learns only from interactive, root, non-ephemeral sessions.
- **Gemini CLI**: experimental Auto Memory. It mines idle sessions into patches and SKILL.md drafts that wait in a human-reviewed inbox.

Other products:
- **Copilot Memory** is the only built-in memory with published A/B evidence and automatic expiry (28 days unused). It is designed for autonomous cloud agents.
- **Cursor** removed its Memories feature (late 2025). **Devin** is deprecating Knowledge in favour of Skills.
- **Aider, OpenCode, Roo, Kiro, Amp and Factory** rely on manually maintained rule or instruction files.

### Cited Findings

#### Claude Code (Anthropic)

**Two memory systems** [P] ([docs: memory](https://code.claude.com/docs/en/memory)):
- CLAUDE.md files are "instructions you write"; auto memory is "notes Claude writes itself based on your corrections and preferences".
- Both load at the start of every conversation "as context, not enforced configuration". To block actions reliably, the docs point to PreToolUse hooks.

**CLAUDE.md hierarchy** [P] ([docs: memory](https://code.claude.com/docs/en/memory)):
- Load order: managed policy (`/etc/claude-code/CLAUDE.md`, or a `claudeMd` key in managed settings), then user `~/.claude/CLAUDE.md`, then project `./CLAUDE.md` or `./.claude/CLAUDE.md`, then local `./CLAUDE.local.md` (gitignored).
- Files are concatenated root-to-cwd. Subdirectory CLAUDE.md files load on demand when Claude reads files there.
- `@path` imports recurse to a maximum depth of four hops. Block-level HTML comments are stripped before injection, so human-only notes cost no tokens.

**Rules and when to add to CLAUDE.md** [P] ([docs: memory](https://code.claude.com/docs/en/memory)):
- `.claude/rules/*.md` holds modular rules. Rules with a `paths:` glob frontmatter load only when Claude reads matching files. User-level rules live in `~/.claude/rules/`. `.claude/rules` was added in v2.0.64 (2025-12-10) [P] ([CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md)).
- Official guidance on when to add a lesson: "Claude makes the same mistake a second time", a code review catches something Claude should have known, or you type the same correction as last session.
- Multi-step procedures should move to a skill or a path-scoped rule instead of CLAUDE.md.
- Size target: "under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence." Files over 4 MiB are skipped.

**AGENTS.md support** [P] ([docs: memory](https://code.claude.com/docs/en/memory); [CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md)):
- Native AGENTS.md reading arrived in v2.1.277 (2026-09-18).
- By default AGENTS.md is read only when no CLAUDE.md or CLAUDE.local.md exists on the path. The `claude-md-and-agents-md` setting reads both.
- `/import [codex|gemini|cursor]` (v2.1.213+) copies other agents' instruction files, MCP servers, commands, subagents and skills into Claude Code.

**The '#' quick-memory shortcut was removed** [P] ([CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md)):
- v2.0.70 (2025-12-15): "Removed # shortcut for quick memory entry (tell Claude to edit your CLAUDE.md instead)".
- Today, "remember X" saves to auto memory. "Add this to CLAUDE.md" edits CLAUDE.md [P] ([docs: memory](https://code.claude.com/docs/en/memory)).

**Auto memory: history** [P] ([CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md), dates via npm):

| Version | Date | Change |
|---|---|---|
| v2.1.59 | 2026-02-25 | Introduced: "Claude automatically saves useful context to auto-memory. Manage with /memory" |
| v2.1.63 | 2026-02-28 | Shared across git worktrees |
| v2.1.74 | 2026-03-11 | `autoMemoryDirectory` setting |
| v2.1.83 | 2026-03-24 | 25KB cap added |
| v2.1.186 | 2026-06-22 | Agent is reminded to compact the index |
| v2.1.210 | 2026-07-14 | Over-limit writes return an explicit error |
| v2.1.214 | 2026-07-18 | `modified` ISO timestamp in frontmatter |

**Auto memory: what it captures** [P] ([docs: memory](https://code.claude.com/docs/en/memory)):
- Four typed note kinds: `user` (role, preferences), `feedback` ("corrections you give Claude and approaches you confirm"), `project` (ongoing work and decisions not derivable from code or git) and `reference` (where external info lives).
- Explicit exclusion: "Claude skips anything it can derive from the codebase, such as architecture, file paths, or debugging fixes."
- It "doesn't save something every session". Claude decides what is useful.

**Auto memory: storage and bloat control** [P] ([docs: memory](https://code.claude.com/docs/en/memory)):
- Storage is `~/.claude/projects/<project>/memory/`, holding a `MEMORY.md` index (one line per memory) plus topic files. It is machine-local, not synced across machines or cloud.
- Only the first 200 lines or 25KB of MEMORY.md load at session start. Topic files are read on demand.
- Near the limit, Claude Code "reminds Claude to shorten it: keep one line per entry, move detail into topic files, and merge or drop stale entries". Over the limit, the write succeeds but an error tells Claude to rewrite the index.
- Memory files are excluded from the transcript retention sweep. There is no automatic expiry: they stay until edited or deleted.
- Review gate: none before write (auto-apply). The user audits later via `/memory` (browse, edit, toggle) or plain file edits.
- UI shows "Saved N memories" or "Recalled N memories".

**Auto memory: toggles** [P] ([docs: memory](https://code.claude.com/docs/en/memory)):
- On by default. Turn off with `autoMemoryEnabled: false` per user or project, or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.

**`/doctor` trim check** [P] ([docs: memory](https://code.claude.com/docs/en/memory); [CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md)):
- v2.1.206 (2026-07-09) proposes trimming checked-in CLAUDE.md files.
- It cuts content derivable from code (layouts, dependency lists, architecture overviews) and keeps pitfalls, rationale and non-default conventions. This is a built-in anti-bloat pass.

**Subagent memory** [P] ([docs: sub-agents](https://code.claude.com/docs/en/sub-agents); [CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md)):
- A `memory:` frontmatter field (`user`, `project` or `local`) was added in v2.1.33 (2026-02-06).
- Locations: `~/.claude/agent-memory/<name>/`, `.claude/agent-memory/<name>/` (can be committed to VCS) or `.claude/agent-memory-local/<name>/`.
- The subagent's system prompt gets the first 200 lines or 25KB of its own MEMORY.md, instructions to curate it, and Read/Write/Edit tools.
- `project` is the recommended default scope. The docs suggest prompting it to "check your memory for patterns you've seen before" and, after the task, to "save what you learned".
- It is part of auto memory: disabling auto memory disables it. The main conversation's auto memory is not loaded into subagents.

**`/insights`** [P] ([docs: costs](https://code.claude.com/docs/en/costs); [docs: commands](https://code.claude.com/docs/en/commands)):
- Generates an HTML report of recent sessions on this machine. It covers what you work on, "friction points such as misunderstood requests or buggy code", and suggestions.
- It analyzes up to 200 unseen sessions per run and "skips very short ones".
- Output goes to `~/.claude/usage-data/report.html` plus timestamped copies, deleted after `cleanupPeriodDays` (30 days by default).
- It consumes plan or API tokens and is not available in cloud sessions.
- It was announced in early February 2026 by Anthropic's Thariq Shihipar [S] ([zolkos.com, 2026-02-03](https://www.zolkos.com/2026/02/03/deep-dive-how-claude-codes-insights-command-works.html)). It is not listed as "Added" in the CHANGELOG. Fixes appear from v2.1.101 (2026-04-10) [P].
- Report sections reportedly include "Where Things Go Wrong" and "Suggested CLAUDE.md Additions" with copy buttons [S] ([pasqualepillitteri.it](https://pasqualepillitteri.it/en/news/408/claude-code-insights-command-workflow)).
- v2.1.281 (2026-09-23) added an auto-mode recommendation estimating how many permission prompts auto mode could have handled [P] ([CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md)).

**Hooks relevant to learning capture** [P] ([docs: hooks](https://code.claude.com/docs/en/hooks); [CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md)):

| Hook or feature | Added | Notes |
|---|---|---|
| `Stop` / `SubagentStop` split | v1.0.41 | |
| `PreCompact` | v1.0.48, 2025-07-10 | Matcher `manual` or `auto`. Can block compaction since v2.1.105, 2026-04-13 |
| `SessionEnd` | v1.0.85, 2025-08-19 | Reasons: clear, resume, logout, prompt_input_exit, other. Timeout extendable via `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` since v2.1.74 |
| `PostCompact` | v2.1.76, 2026-03-14 | |
| `last_assistant_message` in Stop/SubagentStop input | v2.1.47, 2026-02-18 | |
| Stop/SubagentStop may return `hookSpecificOutput.additionalContext` to keep the turn going | v2.1.163, 2026-06-04 | |

- All hooks receive `transcript_path`. The transcript is written asynchronously, so it may lag the current turn.
- `additionalContext`, `systemMessage` and stdout are capped at 10,000 characters.
- **Agent-type hooks** (`type: "agent"`, experimental) spawn a subagent with Read/Grep/Glob for up to 50 turns and return `{ok: true|false}`. They are usable, for example, as a Stop-time verifier or reflector.

**Skill-creator evals** [P] ([anthropics/skills skill-creator SKILL.md](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md); date of the eval features not verified):
- Each test case is run twice in the same turn: a with-skill subagent and a baseline without the skill.
- `total_tokens` and `duration_ms` are captured per run into `timing.json`.
- A `benchmark.json`/`benchmark.md` aggregates pass_rate, time and tokens "with mean ± stddev and the delta".
- Test prompts live in `evals/evals.json`, with results per `iteration-N/`. A separate description optimizer improves triggering.

#### Codex CLI (OpenAI)

**Memories: rollout and defaults**:
- A built-in memory preview shipped on 16 April 2026. v0.128 is referenced as shipping the native Memories system [S] ([codex.danielvaughan.com, 2026-04-18](https://codex.danielvaughan.com/2026/04/18/codex-built-in-memory-system-deep-dive/)). npm dates v0.128.0 to 2026-04-30 [P].
- Memories are off by default [S] ([developers.openai.com/codex/memories](https://developers.openai.com/codex/memories.md); [mem0 blog](https://mem0.ai/blog/how-memory-works-in-codex-cli)).
- Config surface in the official schema [P] ([config.schema.json](https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json)):
  - feature flags `features.memories`, `features.memory_tool`, `features.external_agent_memory_import`;
  - a `[memories]` table with `generate_memories`, `use_memories`, `extract_model`, `consolidation_model`, `max_rollout_age_days`, `max_rollouts_per_startup`, `min_rollout_idle_hours` (">12h recommended"), `max_unused_days`, `max_raw_memories_for_consolidation`, `min_rate_limit_remaining_percent` and `disable_on_external_context` (marks threads with external context as "polluted");
  - `version` v1/v2 (v1 is the default).

**Memories: pipeline** [P] ([codex-rs/memories/README.md](https://raw.githubusercontent.com/openai/codex/main/codex-rs/memories/README.md)):
- **Trigger**: a root session start, only if the session is not ephemeral, the feature is enabled, the session is not a sub-agent, and the state DB is available. It runs asynchronously in the background.
- **Phase 1** (per thread): picks rollouts "from allowed interactive session sources", within the age window and idle long enough. A model extracts `raw_memory`, `rollout_summary` and `rollout_slug`. Secrets are redacted. Results are stored in the state DB.
- **Phase 2** (global consolidation): a single lock. It selects stage-1 outputs, dropping those unused beyond `max_unused_days` and ranking by `usage_count` and recency. It syncs `raw_memories.md` and `rollout_summaries/` into `~/.codex/memories` (a git-baselined dir). It writes `phase2_workspace_diff.md`. If anything changed, it runs an internal consolidation sub-agent "with no approvals, no network, and local write access only" that updates `MEMORY.md`, `memory_summary.md` and `skills/`.
- **Forgetting** is diff-driven: deleted inputs lead to removal of only the memory they supported [P] ([consolidation.md](https://raw.githubusercontent.com/openai/codex/main/codex-rs/memories/write/templates/memories/consolidation.md)).

**Memories: what Phase 1 targets (process efficiency)** [P] ([stage_one_system.md](https://raw.githubusercontent.com/openai/codex/main/codex-rs/memories/write/templates/memories/stage_one_system.md)):
- Stated goals: help future agents "solve similar tasks with fewer tool calls and fewer reasoning tokens, reuse proven workflows and verification checklists, avoid known landmines and failure modes".
- It extracts "Tool usage lessons: correct commands, flags, environment assumptions" and "Common failure patterns: build/test errors and the proven fix".
- It classifies rollout outcome; `fail` includes "stuck loop, tool misuse, or user dissatisfaction".
- It weights user corrections, interruptions and redo requests as the strongest preference evidence.

**Memories: headless limitation and access**:
- Memories are not generated from `codex exec` sessions, only interactive ones [S] ([search summary citing Codex memory sources; see also openai/codex discussion #12567](https://github.com/openai/codex/discussions/12567)). This is consistent with the primary README's "allowed interactive session sources" [P].
- Memory tools `memories.list/search/read` exist [S] ([codex.danielvaughan.com, 2026-05-01](https://codex.danielvaughan.com/2026/05/01/codex-cli-memories-persistent-context-session-memory-ecosystem/)).
- Default idle before eligibility is "six hours" [S] ([search summary](https://github.com/openai/codex/discussions/12567)). The schema text recommends >12h [P]. Treat the exact default as unverified.
- Guidance: team-wide standards belong in AGENTS.md or requirements.toml, not memories [S] ([codex.danielvaughan.com](https://codex.danielvaughan.com/2026/05/01/codex-cli-memories-persistent-context-session-memory-ecosystem/)).

**AGENTS.md in Codex** [P] ([config.schema.json](https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json)):
- `project_doc_max_bytes` defaults to 32768: "Maximum total bytes of project instruction content".
- `project_doc_fallback_filenames` lists fallbacks when AGENTS.md is missing.
- The AGENTS.md docs moved to developers.openai.com/codex/guides/agents-md (not fetched; only the pointer is verified [P] via [docs/agents_md.md](https://raw.githubusercontent.com/openai/codex/main/docs/agents_md.md)).
- The schema has a `skills` config keyed by SKILL.md path [P].

#### Gemini CLI (Google)

**GEMINI.md hierarchy** [P] ([docs/cli/gemini-md.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/gemini-md.md)):
- Global `~/.gemini/GEMINI.md`, then workspace and parent dirs, then "just-in-time" GEMINI.md discovered when a tool touches a directory.
- `@file.md` imports. `/memory show` and `/memory reload` commands.
- `context.fileName` can list `["AGENTS.md", "CONTEXT.md", "GEMINI.md"]`.

**Explicit memory** [P] ([docs/tools/memory.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/tools/memory.md); [tutorial](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/tutorials/memory-management.md)):
- The agent "edits Markdown memory files directly". It routes shared project instructions to repo GEMINI.md, private project notes to a per-project private memory folder, and cross-project prefs to `~/.gemini/GEMINI.md`.
- The page no longer describes a `save_memory` tool. v0.40.0 (2026-04-28) "transitioned to a prompt-driven, four-tier memory management system" [P] ([changelog](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/changelogs/index.md)).

**Auto Memory (experimental, off by default)** [P] ([docs/cli/auto-memory.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/auto-memory.md)):
- Enable with `experimental.autoMemory: true`.
- A background extraction agent, on a preview Gemini Flash model, runs at session startup. It scans `~/.gemini/tmp/<project>/chats/` for sessions idle ≥3 hours with ≥10 user messages. It ignores "active, trivial, and sub-agent sessions".
- It uses a lock file and a processed-state file.
- It drafts memory updates as unified-diff `.patch` files and procedures as `SKILL.md` drafts, "defaults to creating no artifacts unless the evidence is strong", and "cannot directly edit active memory files, settings, credentials, or project GEMINI.md files".
- Review happens in `/memory inbox`: promote skills to user or workspace, apply or reject patches. Nothing is applied automatically.
- Stated use cases include "Codify hard-won fixes for project-specific landmines" and "repeated verification commands".
- Timeline [P] ([changelog](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/changelogs/index.md)): `/memory` inbox for extracted skills in v0.39.0 (2026-04-23); Auto Memory Inbox with canonical-patch contract in v0.42.0 (2026-05-12).
- Gemini CLI also has a built-in `skill-creator` skill (per changelog [P]).

#### Aider (feature background, pre-2025; docs current)

**No auto-learning** [P] ([conventions docs](https://raw.githubusercontent.com/Aider-AI/aider/main/aider/website/docs/usage/conventions.md); [repo map docs](https://raw.githubusercontent.com/Aider-AI/aider/main/aider/website/docs/repomap.md)):
- Conventions are a hand-written `CONVENTIONS.md` loaded read-only via `/read` or `--read`, or always via `read:` in `.aider.conf.yml`. It is cached when prompt caching is enabled.
- There is a community conventions repo.
- The repo map is a graph-ranked symbol map fitted to a token budget (`--map-tokens`, default 1k). It is a per-run context aid, not memory.

#### OpenCode

**Manual AGENTS.md; no built-in auto-memory in the rules doc** [P] ([rules.mdx](https://raw.githubusercontent.com/sst/opencode/master/packages/web/src/content/docs/rules.mdx); fetched from the `master` branch, and the default branch may differ):
- `AGENTS.md` is created or improved in place by `/init`. Global rules live in `~/.config/opencode/AGENTS.md`.
- Claude Code fallbacks: `CLAUDE.md`, `~/.claude/CLAUDE.md`, `~/.claude/skills/`.

#### Amp (Sourcegraph → Amp)

**AGENTS.md; memory is thread-based** [S] ([ampcode.com/news/AGENTS.md](https://ampcode.com/news/AGENTS.md)):
- Uses `AGENTS.md`, falling back to `CLAUDE.md`. Files are read from cwd, parents up to $HOME, subtrees and `/etc/ampcode/AGENTS.md`.
- A third-party guide describes "persistent threads as living memory" and headless mode [S] ([verdent.ai](https://www.verdent.ai/guides/agents/amp-coding-agent)).
- No auto-learning feature was verified.

#### Grok CLIs (two different products)

**superagent-ai/grok-cli (community)** [P] ([README](https://raw.githubusercontent.com/superagent-ai/grok-cli/main/README.md)):
- A community project, "not affiliated with ... xAI".
- Headless: `--prompt`/`-p`, `--format json`, `--max-tool-rounds`, `--batch-api`.
- Skills in `.agents/skills/<name>/SKILL.md` (project) or `~/.agents/skills/` (user). Custom sub-agents via `subAgents` in `~/.grok/user-settings.json`. MCP config in `.grok/settings.json`.
- The README describes no memory or instruction-file learning feature. AGENTS.md is not mentioned in the README.

**xAI "Grok Build" (`grok`, official)**:
- Launched as early beta on 2026-05-14, expanded on 2026-05-25, and reached v1.0 on 2026-08-07; Apache-2.0 [S] ([buildfastwithai](https://www.buildfastwithai.com/blogs/grok-build-xai-cli-ai-agents-2026); [x.ai/news/grok-build-cli](https://x.ai/news/grok-build-cli)).
- The official README confirms a Rust TUI, headless use, ACP embedding, and docs for "MCP servers, skills, plugins, hooks, headless mode, sandboxing" at x.ai/cli. The code includes ports of codex and opencode code [P] ([xai-org/grok-build README](https://raw.githubusercontent.com/xai-org/grok-build/main/README.md)).
- Loads conventions from AGENTS.md and compatible formats; `-p` headless supports session continuation and turn limits [S] ([docs.x.ai/build/overview](https://docs.x.ai/build/overview)).
- Portable skills in `.grok/skills/` [S] ([awesome-grok-build](https://github.com/yuuichieguchi/awesome-grok-build)).
- No built-in auto-memory was verified.

#### GitHub Copilot (coding agent, CLI, code review)

**Copilot Memory** (public preview) [P] ([github/docs: copilot-memory.md](https://raw.githubusercontent.com/github/docs/main/content/copilot/concepts/agents/copilot-memory.md)):
- Stores repository-level facts (conventions, architecture decisions, build commands) and user-level preferences.
- Used by the Copilot cloud/coding agent, Copilot code review (repo facts only) and Copilot CLI. Knowledge is shared across these surfaces.
- Repository facts are "stored with citations pointing to the code". Before use, citations are "check[ed] ... against the current branch ... Only validated facts are used."
- Facts are created only from actions by users with write access. Repo owners can review and delete them.
- Retention: "any stored fact or preference that goes unused is automatically deleted after 28 days", and the timer may reset on validated use.
- On by default for individual plans. On org and enterprise plans, an admin policy is required first.

**Custom instructions**:
- Supports AGENTS.md (nested), `.github/copilot-instructions.md`, `.github/instructions/**.instructions.md`, CLAUDE.md and GEMINI.md, with `@path` includes. The CLI combines all instruction files [S] ([docs.github.com: CLI custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)).
- AGENTS.md support for the coding agent came on 2025-08-28 [S] ([GitHub changelog](https://github.blog/changelog/2025-08-28-copilot-coding-agent-now-supports-agents-md-custom-instructions/)).

**Evidence**: with memories, the coding agent's PR merge rate was 90% vs 83% without (+7 points), and code review positive feedback was 77% vs 75%, "p-value <0.00001" [S] ([GitHub blog, 2026-01-15](https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/)).

#### Cursor

**Memories were added then removed** [S] ([localskills.sh](https://localskills.sh/blog/cursor-memories-guide); [Cursor forum "Are my memories gone?"](https://forum.cursor.com/t/are-my-memories-gone/144057)):
- Memories were auto-extracted from chats and introduced mid-2025. They were removed starting in v2.1.x (late 2025), and users were advised to export memories into Rules.
- Rules (`.cursor/rules` .mdc, legacy `.cursorrules`) are now the only built-in persistence.
- Claude Code `/init` can import `.cursor/rules` [P] ([docs: memory](https://code.claude.com/docs/en/memory)).

#### Windsurf (Cascade)

**Auto-generated memories** [S] ([docs.windsurf.com: Cascade Memories](https://docs.windsurf.com/windsurf/cascade/memories)):
- Cascade "can automatically generate and store memories" it deems useful, or you can ask it to "create a memory of …".
- They don't consume credits and are stored locally in `~/.codeium/windsurf/memories/`.
- They are workspace-scoped, not committed to the repo, and retrieved when Cascade believes they are relevant.
- Managed in the Memories panel. No automatic pruning was documented in the snippet.

#### Cline

**Rules** [P] ([docs: cline-rules](https://raw.githubusercontent.com/cline/cline/main/docs/customization/cline-rules.mdx)):
- Workspace rules in `.clinerules/` or `.cline/rules/`. Global rules in `~/.cline/rules` or `~/Documents/Cline/Rules`.
- Also reads `AGENTS.md` and `~/.agents/AGENTS.md`, plus `.cursorrules` and `.windsurfrules`.
- Per-rule toggles. Conditional rules via YAML frontmatter scope loading to matching files, to save tokens.
- `/newrule` creates a rule interactively.

**Memory Bank** [P] ([docs: memory-bank](https://raw.githubusercontent.com/cline/cline/main/docs/best-practices/memory-bank.mdx)):
- A documentation methodology, not a feature: custom instructions in `.clinerules/memory-bank.md` plus six files under `memory-bank/` (projectbrief, productContext, activeContext, systemPatterns, techContext, progress).
- Cline must read these files at the start of every task [S] ([DeepWiki](https://deepwiki.com/cline/prompts/3.1-memory-bank-system)).

**Self-improving Cline** [P] ([cline/prompts self-improving-cline.md](https://raw.githubusercontent.com/cline/prompts/main/workflows/self-improving-cline.md)):
- A manual workflow `/self-improving-cline.md`. It first checks whether the task "involve[d] user feedback ... OR multiple non-trivial steps".
- It asks permission, lists active workspace and global rules, and proposes focused `.clinerules` edits for user approval.
- The earlier variant fired "before using the attempt_completion tool" [S] ([Cline blog](https://cline.bot/blog/double-clicking-on-toggleable-clinerules-self-improving-cline)).

#### Roo Code

**Manual rules only** [P] ([docs: custom instructions](https://raw.githubusercontent.com/RooCodeInc/Roo-Code-Docs/main/docs/features/custom-instructions.md)):
- Global `~/.roo/rules/` and `~/.roo/rules-{modeSlug}/`. Workspace `.roo/rules/` (preferred) or `.roorules`. Mode-specific `.roo/rules-{modeSlug}/`.
- Workspace rules win on conflict.
- No built-in auto-memory in the doc. Memory banks are community add-ons, for example GreatScottyMac's [S] ([cascade-memory-bank](https://github.com/GreatScottyMac/cascade-memory-bank), Windsurf variant).

#### Kiro (AWS)

**Steering files** [S] ([kiro.dev/docs/steering](https://kiro.dev/docs/steering/); [kiro.dev/cli](https://kiro.dev/cli/)):
- `.kiro/steering/*.md`, with foundation files `product.md`, `tech.md` and `structure.md`. All steering files load automatically in kiro-cli.
- Open issues report steering not applied in CLI [S] ([issue #4351](https://github.com/kirodotdev/Kiro/issues/4351)), and a request to auto-load steering, skills and agents at session start [S] ([issue #6755](https://github.com/kirodotdev/Kiro/issues/6755)).
- No auto-memory was verified.

#### Devin (Cognition)

**Knowledge and Playbooks** [S] ([docs.devin.ai: Knowledge](https://docs.devin.ai/product-guides/knowledge)):
- Devin "will automatically suggest Knowledge to remember based on your feedback in chat". Users can edit, dismiss or ask Devin to regenerate a suggestion. This is a human review gate.
- Playbooks are for recurring tasks.
- "Knowledge is deprecated ... Existing Knowledge is being migrated to Skills in Plugins automatically." The deprecation date was not visible.

#### Augment Code (IDE agent + Auggie CLI)

**Memories and Memory Review**:
- Memories "automatically update as you work with the Agent and persist across conversations" [S] ([Augment blog](https://www.augmentcode.com/blog/meet-augment-agent)).
- Memory Review (2025-09-08) lets users "review, edit, and curate memories as they're created" [S] ([changelog](https://www.augmentcode.com/changelog/memory-review)).
- Augment's own guide warns "uncurated memory degrades agent performance ... stale assumptions ... apply wrong approaches with apparent confidence". It recommends AGENTS.md or workspace rules for every-task issues and memory for learned-during-work items [S] ([Augment guide](https://www.augmentcode.com/guides/agent-memory-vs-context-engineering)).
- Auggie CLI: "conversation history and task state persist across terminal sessions"; `--print` for automation; `.augment/commands/` [S] ([docs](https://docs.augmentcode.com/cli/overview)).

#### Factory (Droid)

**Recipe, not feature** [S] ([docs.factory.ai: memory management](https://docs.factory.ai/guides/power-user/memory-management)):
- Put memory preferences in `~/.factory/AGENTS.md` or project AGENTS.md, pointing to a `memories.md`.
- Capture learnings "when a command fails, a user corrects you, or a better approach is discovered".
- Suggests building a `/remember` command or skill. No auto-memory was verified.

#### Anthropic API (for Agent SDK / custom agents)

**Memory tool and context editing** [P] ([anthropic.com/news/context-management, 2025-09-29](https://www.anthropic.com/news/context-management)):
- Memory tool: "store and consult information outside the context window through a file-based system ... a dedicated memory directory ... that persists across conversations". It "operates entirely client-side", so developers own the storage.
- Context editing "automatically clears stale tool calls and results".
- Evidence: memory tool plus context editing gave +39% over baseline on an internal agentic-search eval; context editing alone +29%. In a 100-turn web-search eval, context editing "reduc[ed] token consumption by 84%".
- Anthropic's context-engineering post (2025-09-29) names "structured note-taking, or agentic memory" (for example a NOTES.md) as a core long-horizon technique [P] ([anthropic.com/engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

### Inferences
- **Claude Code auto memory is the wrong tool for process lessons from orchestrated runs.** It deliberately skips "debugging fixes" and code-derivable content and privileges user corrections. A headless hand gets no human corrections, so expect little to be saved (inference from [P] docs).
- **Codex memories are the closest built-in match to the user's goal** (fewer tool calls, landmines, verification checklists). But they are user-global (`~/.codex/memories`), not repo-committed, and they are not generated from `codex exec` rollouts. They cannot be the path by which lessons reach target repos.
- **Gemini Auto Memory is the only built-in design with a mandatory human review inbox and patch/skill output.** Its eligibility rules (≥10 user messages, idle 3h) exclude one-shot headless runs.
- **Copilot Memory's design is the most transferable pattern for bloat and staleness control**: citations to code, validated before use; unused-for-28-days expiry; write-access gating.
- **Product churn is high.** Cursor removed auto memories; Devin is folding Knowledge into Skills; Claude Code removed '#'; Gemini replaced its memory tool with prompt-driven file edits. The shared direction is to converge on plain Markdown files (AGENTS.md or CLAUDE.md, MEMORY.md) plus SKILL.md. A durable orchestrator design should write lessons into those portable formats rather than into any vendor store.

### Gaps
- No quantitative evaluation found for Claude Code auto memory, Codex memories, Gemini Auto Memory, Windsurf or Augment memories.
- The exact launch release of `/insights` is not in the CHANGELOG; the date is snippet-based.
- Codex official memories doc (developers.openai.com) and the AGENTS.md guide could not be fetched (host blocked). The default idle hours (6 vs the ">12h recommended" text) and EEA availability are unverified.
- Grok Build's memory and instruction-file behaviour is known only from snippets. Which Grok CLI the user's Orca workers run (superagent-ai/grok-cli vs xAI Grok Build) determines what is available.
- Devin Knowledge deprecation date, Kiro steering inclusion modes, Amp memory specifics, and the current status of Roo Code were not verified.
- Search budget was exhausted before verifying an academic study on AGENTS.md effectiveness and cost (academic, out of scope anyway).

## KQ2. Community tools and recipes for capturing lessons (2025–2026)

### Takeaway
Community tools split into four families:
- **Correction-queue → reviewed CLAUDE.md/AGENTS.md edits**: claude-reflect, claude-reflect-system, Cline's self-improving workflow.
- **Diary → periodic reflection**: claude-diary, MindStudio learnings.md, /insights-driven loops.
- **Always-on observation of tool calls → scored atomic lessons or skills**: ECC continuous-learning v2 "instincts", Continuous-Claude's daemon, Letta skill learning.
- **Retrieval memory stores via hooks or MCP**: claude-mem, Basic Memory, OpenMemory/Mem0, Serena memories.

Only the third family systematically mines tool-level process inefficiencies. Only Letta publishes benchmark evidence.

### Cited Findings

#### claude-reflect (Bayram Annakov)
- Source: [README](https://raw.githubusercontent.com/BayramAnnakov/claude-reflect/main/README.md) [P]. Date not shown. It references Claude Code issues #14061 and #15369, so it was active in late 2025 to 2026.
- **Capture** (automatic, via hooks): `capture_learning.py` runs on every prompt. Regex detects corrections ("no, use X", "don't use Y", "actually…"), positive feedback, and an explicit "remember:" marker. Confidence is 0.60–0.95.
- Other hooks: a session-start reminder, a PreCompact backup of the queue, and a post-commit reminder to run /reflect.
- **Apply** (manual): `/reflect` runs a semantic AI filter, then a human table of Apply, Edit or Skip.
- **Targets**: `~/.claude/CLAUDE.md`, `./CLAUDE.md`, subdirectory CLAUDE.md files, `.claude/commands/*.md` (routes skill-related corrections back into the skill file), and **`AGENTS.md` if it exists** ("works with Codex, Cursor, Aider, Jules, Zed, Factory").
- **Process signal**: `/reflect --include-tool-errors`; scripts `extract_tool_errors.py` and `extract_tool_rejections.py`; `/reflect --scan-history` mines past sessions.
- **Consolidation**: duplicate detection before add (merge, replace or skip); `/reflect --dedupe` semantic consolidation; `--review` shows "confidence scores and decay status".
- `/reflect-skills` finds repeating intents across sessions (for example "Found 2 potential skills from analyzing 68 sessions") and drafts commands for approval.
- Tip: set `cleanupPeriodDays` high, because it depends on session transcripts that are deleted after 30 days by default.

#### claude-reflect-system (haddock-development)
- Source: [README](https://raw.githubusercontent.com/haddock-development/claude-reflect-system/master/README.md) [P].
- Skill-centric. `/reflect` analyzes the current session and classifies signals: HIGH = corrections leading to a "Critical Corrections" section; MEDIUM = approvals leading to "Best Practices"; LOW = observations leading to "Considerations".
- It edits skill files with a timestamped backup, YAML validation, rollback and a git commit.
- `/reflect-on` enables auto-reflection at session end via a **Stop hook**. Manual review is recommended first.
- The README's own claims ("Battle-Tested", "Forever learned") are marketing. It shows no measurements.

#### claude-diary (Lance Martin; blog 2025-12-01)
- Sources: [README](https://raw.githubusercontent.com/rlancemartin/claude-diary/main/README.md) [P]; [blog post source](https://raw.githubusercontent.com/rlancemartin/rlancemartin.github.io/master/_posts/2025-12-01-claude_diary.md) [P].
- `/diary` is written from in-context session content (Martin found parsing JSONL "required dozens of bash tool calls"). It is run manually or automatically via a **PreCompact hook** (matcher `auto`). Entries go to `~/.claude/memory/diary/YYYY-MM-DD-session-N.md`.
- `/reflect` reads unprocessed entries (tracked in `processed.log`). It treats "2+ occurrences = pattern, 3+ = strong pattern" and scans for "violations of existing CLAUDE.md rules (highest priority)". It writes one-line bullets to `~/.claude/CLAUDE.md` and saves the analysis to `~/.claude/memory/reflections/`.
- Reflection is kept manual so updates can be reviewed.
- Inspiration: Cat Wu said some Anthropic staff create diary entries from sessions and reflect on them. The approach is also linked to Generative Agents and ACE (academic, pointer only).
- Evidence is anecdotal after a month: PR-review feedback, git conventions, testing order, and "token efficiency, biasing toward single-agent delegation".

#### claude-mem (Alex Newman / thedotmack)
- Source: [README](https://raw.githubusercontent.com/thedotmack/claude-mem/main/README.md) [P]. Apache-2.0.
- Hooks: SessionStart, UserPromptSubmit, PostToolUse, Stop and SessionEnd. It captures "tool usage observations", compresses them with AI, and injects context into future sessions.
- Storage: a local worker service with an HTTP API and web viewer, SQLite with FTS5, and a Chroma vector DB.
- 3-layer MCP search: `search` (~50–100 tokens/result), then `timeline`, then `get_observations` (~500–1,000 tokens/result). The README claims "~10x token savings" from filtering first; this is a vendor claim with no methodology shown.
- Installers for Claude Code, OpenCode, Antigravity and a "Grok Bot" via chat-log watching.
- Now defaults to a hosted "CMEM Pro" observer after browser sign-in. It is skippable with `--provider`, `CLAUDE_MEM_ONLINE_OPTIN=false`, or in CI/non-interactive shells.
- `<private>` tags exclude content from storage.
- Maturity: 46.1K then 65.8K stars (June 2026) [S] ([augmentcode.com/learn](https://www.augmentcode.com/learn/claude-mem-65k-stars)); 94.6k per [skillsllm](https://skillsllm.com/skill/claude-mem) [S]; v12.3.8, 106 contributors, 244 releases as of April 2026 [S].
- Nature: an episodic context store (what was done), not a lesson distiller.

#### everything-claude-code (ECC) "continuous-learning" (Affaan Mustafa)
- Sources: [v2 SKILL.md](https://raw.githubusercontent.com/affaan-m/everything-claude-code/main/skills/continuous-learning-v2/SKILL.md) [P]; [v1 SKILL.md](https://raw.githubusercontent.com/affaan-m/everything-claude-code/main/skills/continuous-learning/SKILL.md) [P].
- **v1**: a Stop hook extracts patterns (error_resolution, user_corrections, workarounds, debugging_techniques) from sessions with 10+ messages into `~/.claude/skills/learned/`. `auto_approve: false` by default. Deprecated 2026-04-28.
- **v2.1 "instincts"**:
  - PreToolUse and PostToolUse hooks record every prompt and tool call to `observations.jsonl`. The rationale: "Skills are probabilistic—they fire ~50-80% of the time. v2 uses hooks for observation (100% reliable)".
  - An optional background observer (Haiku, every 5 minutes after ≥20 observations; `observer.enabled: false` by default) creates atomic YAML "instincts". Each has one trigger and one action, confidence 0.3–0.9, a domain tag and evidence. Examples: `grep-before-edit.yaml (0.6) [global]`.
  - Instincts are project-scoped by git-remote hash. They are promoted to global when the same instinct appears in 2+ projects with average confidence ≥0.8.
  - Confidence rises with repeated observation and falls on user correction, long non-observation or contradiction.
  - `/evolve` clusters instincts into skills, commands or agents. `/prune` deletes expired pending instincts. `/instinct-export` and `/instinct-import` share them.
  - Storage lives outside `~/.claude` (`$XDG_DATA_HOME/ecc-homunculus`) so Claude Code's sensitive-path guard does not block background writes.
- Maturity: the README advertises 68 agents and 292 skills; the star count is only a badge [P] ([README](https://raw.githubusercontent.com/affaan-m/everything-claude-code/main/README.md)).
- It was inspired by the community project "Homunculus".

#### Continuous-Claude (parcadei; v1, v2 and v3 URLs serve the same README)
- Source: [README](https://raw.githubusercontent.com/parcadei/Continuous-Claude-v3/main/README.md) [P]. Examples are dated 2026-01-08.
- Mantra: "Compound, don't compact."
- Memory: PostgreSQL + pgvector. When a session's heartbeat is stale for more than 5 minutes, a daemon "spawns headless Claude (Sonnet)" that "analyzes thinking blocks from session" and extracts learnings into `archival_memory` with BGE embeddings.
- A memory-awareness hook surfaces "MEMORY MATCH" results on each prompt.
- Explicit `store_learning.py --type WORKING_SOLUTION --confidence high`.
- Continuity: an in-session ledger `thoughts/ledgers/CONTINUITY_<topic>.md` and between-session YAML handoffs `thoughts/shared/handoffs/<session>/` (`/handoff`, "resume work").
- Scale: 109 skills, 32 agents and 30 hooks, so it is heavy.

#### learnings.md loops (MindStudio blog series; dates not visible) [S]
- Sources: [self-learning skill learnings.md](https://www.mindstudio.ai/blog/self-learning-claude-code-skill-learnings-md/), [learnings loop](https://www.mindstudio.ai/blog/how-to-build-learnings-loop-claude-code-skills), [binary evals](https://www.mindstudio.ai/blog/self-improving-ai-skills-binary-evals-claude-code), [wrap-up skill](https://www.mindstudio.ai/blog/self-learning-ai-skill-system-learnings-md-wrap-up).
- A per-skill `learnings.md` is read at the start of each run and updated after it, with notes on "what worked, what didn't".
- Variant: binary evals in `eval.json` score each output, and the skill updates learnings from the scores.
- Warning: an uncurated file with "hundreds of entries" buries signal, so add a periodic consolidation step.
- Variant: a dedicated "wrap-up" skill so updating doesn't depend on memory.

#### "Self-improving CLAUDE.md" prompts [S]
- Source: [dev.to, Aviad Rozenhek](https://dev.to/aviadr1/self-improving-ai-one-prompt-that-makes-claude-learn-from-every-mistake-16ek).
- After a mistake, one prompt makes Claude reflect, abstract the general pattern and write it down. The file carries "meta-rules about how to write rules" to keep additions consistent.

#### /insights-driven loops [S]
- Sources: [chatwithgpt substack](https://chatwithgpt.substack.com/p/the-self-improving-loop-how-claude), [dev.to CLI tool](https://dev.to/yahav10/i-built-a-cli-that-turns-claude-codes-insights-report-into-actionable-skills-rules-and-workflows-377), [HN](https://news.ycombinator.com/item?id=47350947).
- Practitioners run `/insights` periodically and paste its "Suggested CLAUDE.md Additions". One community CLI converts the report into skills, rules and workflows.

#### Letta Code (Letta, creators of MemGPT)
- Source: [README](https://raw.githubusercontent.com/letta-ai/letta-code/main/README.md) [P].
- Agents are persistent identities. They "programmatically rewrite their context": system-prompt learning via memory blocks, plus skill learning.
- MemFS tracks all context in git, and it can sync to a GitHub repo (`/memory-repository set`).
- Skills come from `~/.letta` (global), `.agents/skills` (project) and agent-scoped MemFS. `/skill-creator` is included.
- Headless: `letta -p --agent <id> ...`.
- "Sleep-time compute" is now called "dreaming". Cloud backend is the default; local is possible.
- **Evidence** [S] ([Letta blog: Skill Learning](https://www.letta.com/blog/skill-learning/)):
  - Two-stage process: reflection on a trajectory, then skills learned "using the baseline agent's trajectory and textual feedback from the verifier".
  - Terminal-Bench: "21.1% relative (9% absolute) increase ... while also reducing costs by 15.7%". Terminal-Bench 2.0: "36.8% relative (15.7% absolute)".
  - Setup: Sonnet 4.5 on 89 tasks. Blog date not verified.

#### Serena (Oraios)
- Source: [README](https://raw.githubusercontent.com/oraios/serena/main/README.md) [P].
- A code-intelligence MCP server with a simple "memory management" system for knowledge "shared across sessions, users and projects". Users often combine it with AGENTS.md, and it "can easily be disabled".
- Details of the memory format were not in the README.

#### Basic Memory (Basic Machines)
- Source: [README](https://raw.githubusercontent.com/basicmachines-co/basic-memory/main/README.md) [P].
- An MCP server over local Markdown files with a knowledge graph (observations and wikilinks) and semantic/hybrid search. Works with Claude, Codex and Cursor.
- An optional paid cloud and "Teams" shared workspace.
- A general knowledge store, not coding-lesson specific.

#### OpenMemory MCP / Mem0 [S]
- Sources: [mem0.ai/openmemory](https://mem0.ai/openmemory); [intro post](https://mem0.ai/blog/introducing-openmemory-mcp).
- A local-first MCP memory layer for Cursor, Claude and Windsurf, with a hosted "Mem0 Platform MCP" alternative.
- A reported issue says OpenMemory MCP was not working with Claude Code [S] ([mem0 issue #3400](https://github.com/mem0ai/mem0/issues/3400)).
- Similar cross-agent MCP stores: Memorix [S] ([AVIDS2/memorix](https://github.com/AVIDS2/memorix)) and Hindsight for Codex [S] ([hindsight.vectorize.io](https://hindsight.vectorize.io/sdks/integrations/codex)).

#### Out-of-scope pointers (one line each)
- Beads, an issue-graph "memory" for agents [S] ([Yegge](https://steve-yegge.medium.com/introducing-beads-a-coding-agent-memory-system-637d7d92514a)).
- Ralph loop, Gas Town, BMAD, Every's compound engineering, claude-flow and agent teams are covered by other researchers.
- Academic: ACE, the generator/reflector/curator pattern ([arXiv 2510.04618](https://arxiv.org/pdf/2510.04618)); [SkillLearnBench (2604.20087)](https://arxiv.org/abs/2604.20087); ["Do Agent Optimizers Compound?" on Terminal-Bench 2.0 (2607.14004)](https://arxiv.org/pdf/2607.14004).
- Observability: [Claude Code OpenTelemetry](https://code.claude.com/docs/en/monitoring-usage).

### Inferences
- **Best fit for mining process inefficiencies from traces**: ECC v2 (tool-call observation plus confidence and decay), claude-reflect with `--include-tool-errors` and tool rejections, and Continuous-Claude's daemon (thinking-block mining).
- **Best fit for pushing lessons into worker instruction files**: claude-reflect (multi-target sync including AGENTS.md and skill files).
- **Closest published analogue of the user's verifier-driven pipeline**: Letta's verifier-feedback skill learning. It is the only one with a benchmark delta and a cost reduction.
- **Retrieval stores (claude-mem, Basic Memory, OpenMemory) add infrastructure and token cost at read time.** They mostly preserve episodic context, not distilled rules, so they address "remember what happened" rather than "stop repeating the mistake".
- **Several popular tools are Claude-Code-hook-bound** (claude-reflect, claude-reflect-system, claude-diary, ECC, Continuous-Claude). They don't observe Codex or Grok hands unless those tools' transcripts are parsed separately.

### Gaps
- Star counts for claude-reflect, claude-reflect-system, claude-diary, ECC and Continuous-Claude were not verified; GitHub pages and the API are blocked.
- No independent evaluation found for any community tool except Letta's own benchmark.
- MindStudio post dates were not visible.
- Serena memory internals (file layout, scope) were not checked beyond the README.
- Whether OpenMemory's Claude Code issue is resolved is unknown.

## KQ3. Comparative mechanism matrix: trigger, storage, review gate, consolidation, scope, evidence (emphasis on process inefficiencies)

### Takeaway
The mechanisms differ most on two axes:
- **Who reviews**: auto-apply (Claude auto memory, Codex memories, Windsurf, ECC ≥0.7 confidence) vs an inbox or human gate (Gemini Auto Memory, claude-reflect, Devin, Augment Memory Review, Cline).
- **Whether they forget**: time or usage expiry (Copilot 28 days, Codex `max_unused_days`, ECC decay) vs grow-until-trimmed (CLAUDE.md, learnings.md, Memory Bank).

Only Codex memories, ECC v2, claude-reflect (tool errors), Continuous-Claude, /insights, Gemini Auto Memory and Letta explicitly target process inefficiencies. These are wasted or failed tool calls, stuck loops, wrong commands, and verification checklists.

### Cited Findings

| Mechanism | Trigger | Storage | Review gate | Consolidation / pruning | Scope | Process-inefficiency capture | Evidence | Source |
|---|---|---|---|---|---|---|---|---|
| Claude Code CLAUDE.md, rules, imports | Manual edits; "add this to CLAUDE.md"; `/init`; `/import` | Repo files and `~/.claude` | Human (diff/PR) | Manual; `/doctor` trim (v2.1.206); 200-line guidance | Org, user, project, local, path | Only if written by hand | None quantified | [P] [memory](https://code.claude.com/docs/en/memory) |
| Claude Code auto memory | Automatic (model decides); "remember X" | `~/.claude/projects/<p>/memory/` (machine-local) | None pre-write; audit via `/memory` | 200-line/25KB index; reminders; merge or drop stale; no expiry | Per repo (shared across worktrees) | Weak: skips "debugging fixes" | None found | [P] [memory](https://code.claude.com/docs/en/memory) |
| Claude Code subagent `memory` | Agent's own prompt, or asked to save | `~/.claude/agent-memory` or `.claude/agent-memory` (VCS-able) | None | Same 200-line/25KB curation | Agent role × user or project | Depends on the agent prompt | None found | [P] [sub-agents](https://code.claude.com/docs/en/sub-agents) |
| Claude Code `/insights` | Manual command | `~/.claude/usage-data/report.html` | Human reads, copies rules | n/a (a report; 30-day retention) | User × machine, ≤200 new sessions | Friction: misunderstood requests, buggy code | Anecdotal blogs | [P] [costs](https://code.claude.com/docs/en/costs) |
| Claude Code hooks (Stop, SubagentStop, SessionEnd, PreCompact; agent-type) | Deterministic lifecycle events | Whatever the hook writes | Configurable | Script-defined | Any | Yes, if the hook parses `transcript_path` | n/a | [P] [hooks](https://code.claude.com/docs/en/hooks) |
| skill-creator evals | Manual | `<skill>-workspace/iteration-N/` | Human plus benchmark | Iterations | Skill | Measures tokens and time per run | Yields pass_rate, time, token deltas | [P] [skill-creator](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md) |
| Codex memories | Automatic at root-session start (background) | `~/.codex/memories` (git-baselined) plus state DB | None (consolidator agent auto-writes) | `max_unused_days`; usage ranking; diff-driven forgetting | User-global | Strong: "fewer tool calls and fewer reasoning tokens", tool lessons, failure patterns | None found | [P] [README](https://raw.githubusercontent.com/openai/codex/main/codex-rs/memories/README.md) |
| Gemini CLI Auto Memory | Automatic background at startup, over idle sessions | Project memory dir inbox leading to private or global memory and skills | **Human inbox** (`/memory inbox`) | "No artifacts unless evidence strong"; patch dry-run | Project-private, global, skills | Landmines, verification commands, procedures leading to skills | None found | [P] [auto-memory](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/auto-memory.md) |
| Copilot Memory | Automatic during agent work | GitHub-hosted | None pre-write; owners can delete | Citation validation before use; 28-day unused expiry | Repo facts, user prefs | Facts only | **+7 pts merge rate; +2 pts review feedback** | [P] [docs](https://raw.githubusercontent.com/github/docs/main/content/copilot/concepts/agents/copilot-memory.md); [S] [blog](https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/) |
| Windsurf memories | Automatic, or on request | `~/.codeium/windsurf/memories/` | None | Not documented | Workspace | Facts and preferences | None | [S] [docs](https://docs.windsurf.com/windsurf/cascade/memories) |
| Cursor Memories | (Removed in 2.1.x) | | | | | | | [S] [forum](https://forum.cursor.com/t/are-my-memories-gone/144057) |
| Devin Knowledge suggestions | Automatic suggestion from chat feedback | Devin cloud (migrating to Skills) | **Human** edit, save or dismiss | n/a | Org | Feedback-derived | None | [S] [docs](https://docs.devin.ai/product-guides/knowledge) |
| Augment Memories + Review | Automatic | Augment | **Human review** (since 2025-09-08) | Curation by user | Workspace | Corrected patterns | Vendor warning that uncurated memory hurts | [S] [changelog](https://www.augmentcode.com/changelog/memory-review) |
| Cline self-improving workflow | Manual `/self-improving-cline.md` | `.clinerules` | **Human** approval | Focused edits | Workspace, global | Multi-step and feedback tasks | None | [P] [prompt](https://raw.githubusercontent.com/cline/prompts/main/workflows/self-improving-cline.md) |
| claude-reflect | Hook capture (auto) plus `/reflect` (manual) | CLAUDE.md files, AGENTS.md, skill files | **Human** Apply/Edit/Skip | Dedupe, `--dedupe`, decay status | Global, project, skill | Tool errors and rejections (flag) | None | [P] [README](https://raw.githubusercontent.com/BayramAnnakov/claude-reflect/main/README.md) |
| claude-reflect-system | Manual, or Stop hook (auto mode) | Skill files plus git commit | Human (manual mode) | Backups, rollback | Skill | Corrections and approvals | None | [P] [README](https://raw.githubusercontent.com/haddock-development/claude-reflect-system/master/README.md) |
| claude-diary | `/diary` manual or PreCompact auto; `/reflect` manual | `~/.claude/memory/diary`, then `~/.claude/CLAUDE.md` | Human (reflect kept manual) | `processed.log`; 2+ = pattern | User-global | Rule violations; token-efficiency preferences | Anecdotal | [P] [post](https://raw.githubusercontent.com/rlancemartin/rlancemartin.github.io/master/_posts/2025-12-01-claude_diary.md) |
| ECC continuous-learning v2 | PreToolUse/PostToolUse hooks (every call) plus background observer | `$XDG_DATA_HOME/ecc-homunculus` | Auto (≥0.7 "auto-approved"); `/evolve` manual | Confidence decay; `/prune`; promote at 2+ projects and ≥0.8 | Project, then global | **Strong**: tool workflows ("grep-before-edit") | None | [P] [SKILL.md](https://raw.githubusercontent.com/affaan-m/everything-claude-code/main/skills/continuous-learning-v2/SKILL.md) |
| Continuous-Claude | Daemon on stale heartbeat (auto) | Postgres + pgvector | None | Not documented | Cross-session | Thinking-block mining; WORKING_SOLUTION type | None | [P] [README](https://raw.githubusercontent.com/parcadei/Continuous-Claude-v3/main/README.md) |
| claude-mem | Hooks (auto) | SQLite + Chroma (+ optional cloud) | None | Not documented | Project | Tool observations (episodic) | "~10x token savings" (vendor claim) | [P] [README](https://raw.githubusercontent.com/thedotmack/claude-mem/main/README.md) |
| learnings.md loop | Skill start and end (in-prompt) | Per-skill file | Optional binary evals | Periodic cleanup step recommended | Skill | What worked or failed per run | None | [S] [MindStudio](https://www.mindstudio.ai/blog/how-to-build-learnings-loop-claude-code-skills) |
| Letta skill learning | Reflection after task, using verifier feedback | Agent MemFS (git) | Not stated | Not stated | Agent | Trajectory-level | **+21.1% rel TB, −15.7% cost; +36.8% rel TB2.0** | [S] [Letta](https://www.letta.com/blog/skill-learning/) |
| Anthropic memory tool + context editing | Model tool calls (API) | Developer-owned dir | Developer-defined | Context editing clears stale tool results | Agent | Developer-defined | **+39% / +29%; −84% tokens** | [P] [news](https://www.anthropic.com/news/context-management) |

### Inferences
- **Hooks give 100% capture, but lesson extraction is still an LLM judgment.** Tools that separate capture (deterministic hooks or rollout files) from distillation (a separate agent or consolidator) most resemble a fresh-context verifier. Examples: ECC's Haiku observer, the Codex Phase-2 sub-agent with no network, Gemini's extraction agent writing only to an inbox, and Continuous-Claude's headless Sonnet. This directly addresses the baseline gap "the orchestrator grades itself".
- **Expiry and validation are the main anti-bloat levers seen in production systems** (Copilot 28 days plus citation validation; Codex usage ranking plus `max_unused_days`). Rule files have none. Their only defences are size budgets: 200 lines, 25KB, Codex 32 KiB, hook `additionalContext` 10k chars.
- **The evidence base is thin and vendor-produced.** Copilot, Letta and Anthropic each report positive deltas on their own evals. No product reports a measured reduction in recurrence of a specific mistake class, which is the metric the user lacks.

### Gaps
- No source reports recurrence-rate reduction per lesson, or token or time savings per lesson, for any CLI-agent memory mechanism.
- Consolidation behaviour is undocumented for Windsurf, Continuous-Claude and claude-mem.

## KQ4. Which mechanisms work for headless / non-interactive runs launched by an orchestrator (claude -p, codex exec, gemini -p, grok -p) vs which assume an interactive human session

### Takeaway
Instruction files (CLAUDE.md, AGENTS.md, GEMINI.md, rules, skills) load in headless runs of every CLI checked, so they are the reliable injection path.

Automatic learning is mostly interactive-only:
- Codex skips `exec` rollouts.
- Gemini Auto Memory requires ≥10 user messages and 3h idle.
- Claude's `--bare` (recommended for scripts and slated to become the `-p` default) disables auto memory, hooks and CLAUDE.md.
- Correction-detectors need a human correcting.

The robust pattern for an orchestrator is to capture from its own pipeline journal and the hands' transcript files, distill offline, and write back into AGENTS.md or skills.

### Cited Findings

**Claude Code `-p`** [P] ([docs: headless](https://code.claude.com/docs/en/headless); [CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md)):
- Without `--bare`, `claude -p` "loads the same context an interactive session would". That includes CLAUDE.md, auto memory, hooks from `.claude/settings.json`, and skills, even in untrusted folders.
- `--bare` (v2.1.81, 2026-03-20) skips hooks, skills, plugins, MCP, **auto memory and CLAUDE.md**. The docs call it "the recommended mode for scripted and SDK calls, and will become the default for `-p` in a future release".
- On SIGTERM, `-p` "runs `SessionEnd` hooks and exits".
- User-invoked skills work in `-p` by including `/skill-name` in the prompt.
- Instructions that must reach the system-prompt level in automation: use `--append-system-prompt` [P] ([docs: memory](https://code.claude.com/docs/en/memory)).
- `InstructionsLoaded` hooks can log which CLAUDE.md and rules actually loaded [P] ([docs: memory](https://code.claude.com/docs/en/memory)).

**Claude Code `/insights`**: an interactive report over local sessions, "not available in cloud sessions" [P] ([docs: commands](https://code.claude.com/docs/en/commands)). It "skips very short ones" [P] ([docs: costs](https://code.claude.com/docs/en/costs)).

**Codex**:
- The memory pipeline runs only for non-ephemeral, non-sub-agent root sessions from "allowed interactive session sources" [P] ([README](https://raw.githubusercontent.com/openai/codex/main/codex-rs/memories/README.md)).
- "Codex doesn't save memories from exec sessions" [S] ([discussion #12567 and related](https://github.com/openai/codex/discussions/12567)).
- The pipeline also skips when rate-limit remaining is below `min_rate_limit_remaining_percent` [P] ([schema](https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json)).

**Gemini CLI Auto Memory**: needs sessions with ≥10 user messages, idle ≥3h, not sub-agent; review is an interactive `/memory inbox` [P] ([docs](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/auto-memory.md)).

**Copilot Memory**: designed for the asynchronous cloud coding agent and the CLI. Memories are created and used without a human in the loop, and validated against citations [P] ([docs](https://raw.githubusercontent.com/github/docs/main/content/copilot/concepts/agents/copilot-memory.md)).

**Grok**:
- superagent-ai grok-cli: headless `--prompt` with JSON output; skills load from `.agents/skills` [P] ([README](https://raw.githubusercontent.com/superagent-ai/grok-cli/main/README.md)).
- Grok Build: `-p` headless with session continuation; AGENTS.md loading [S] ([docs.x.ai](https://docs.x.ai/build/overview)).

**Letta Code**: headless `letta -p --agent <id>`. Memory is bound to a persistent agent ID, not a session [P] ([README](https://raw.githubusercontent.com/letta-ai/letta-code/main/README.md)).

**Community tools**:
- claude-reflect: capture uses a UserPromptSubmit regex on human corrections; apply via interactive `/reflect` review [P] ([README](https://raw.githubusercontent.com/BayramAnnakov/claude-reflect/main/README.md)).
- claude-diary: PreCompact-auto diary, manual `/reflect` [P] ([README](https://raw.githubusercontent.com/rlancemartin/claude-diary/main/README.md)).
- ECC v2: capture via tool hooks [P] ([SKILL.md](https://raw.githubusercontent.com/affaan-m/everything-claude-code/main/skills/continuous-learning-v2/SKILL.md)).
- claude-mem: the installer completes non-interactively in CI shells [P] ([README](https://raw.githubusercontent.com/thedotmack/claude-mem/main/README.md)).

### Inferences

**Headless-compatible as-is:**
- Instruction files and skills in all CLIs.
- Claude Code hooks, subagent `memory` and auto memory in non-bare `-p`.
- ECC v2 observation hooks and claude-mem hooks in non-bare `claude -p`.
- Copilot Memory and Letta agent memory.
- Offline miners run by the orchestrator over transcript files: `~/.claude/projects/*.jsonl`, Codex rollouts, Gemini `~/.gemini/tmp/<project>/chats/`. Examples: claude-reflect `--scan-history`, a Codex-Phase-1-style extraction prompt reused as a standalone distiller, /insights-style reports.

**Interactive-assuming:**
- Codex memories generation, Gemini Auto Memory eligibility and inbox, /insights (human reads HTML).
- Correction-regex capture (claude-reflect, claude-reflect-system), since no human corrections occur in headless runs.
- Cline and Devin human-approval flows.

**Fragility for orchestrators:**
- If Anthropic makes `--bare` the `-p` default, hook- and auto-memory-based capture in Claude hands silently stops. Orchestrators should pass explicit flags and verify loading via `InstructionsLoaded` or `system/init`.
- The baseline's Codex hands run through the codex-companion plugin with `--resume`/`--fresh`. Whether those threads count as "interactive session sources" for Codex memories is unknown. Do not rely on Codex memories for them.

### Gaps
- Whether `/insights` can be invoked in `-p` mode, or includes `-p` transcripts, is not documented.
- Whether the Codex memory read path (`use_memories` injection) applies to `codex exec` runs was not verified. The session sources codex-companion uses (exec vs app-server) were not checked.
- Grok Build's hook events and memory behaviour in `-p` mode were not verified.

## KQ5. Mapping onto the user's baseline ("fable-ruki-agenty": head writes specs → Codex/Grok hands → forwarder journal → fresh verifier → incidents.md loop)

### Takeaway
The baseline already has several of the strongest pieces the community reinvents:
- deterministic capture points (the per-issue journal);
- an independent verifier (Letta-style verifier feedback);
- a "2+ occurrences → rule" threshold, the same as Claude docs' "same mistake a second time", claude-diary's "2+ = pattern" and ECC's promotion rule;
- issue-first edits (a claude-reflect-style human gate).

It lacks:
- a distiller separate from the orchestrator;
- expiry and validation (Copilot, Codex);
- measurement (skill-creator-style with/without benchmarks; per-run tokens and time);
- a write-back channel into the hands' own AGENTS.md or skills.

### Cited Findings
- **Baseline facts** [P] ([local SKILL.md](/home/user/personal-corp-os/skills/fable-ruki-agenty/SKILL.md)):
  - Codex hands run via the `codex` plugin runtime codex-companion, with `--model gpt-5.5` explicitly, and `--resume` (same thread) for reworks 1–2 or `--fresh` for a new executor.
  - Orca Grok workers get context "only as text" (Orca doesn't carry session history).
  - The journal records dispatch payload, executor digest, verifier verdicts per DoD item, rework N and blocked.
  - The incident journal lives at `.claude/skills/fable-ruki-agenty/incidents.md`. "2+ open entries of one class → skill edit (issue-first)", and new observations live in the journal before becoming rules.
  - Subagents write full reports to `<scratchpad>/reports/<agent>.md` and return a digest of ≤15 lines.
- **Claude Code's official rule for promoting a lesson** is "Claude makes the same mistake a second time" [P] ([docs: memory](https://code.claude.com/docs/en/memory)). This matches the baseline's 2+ threshold.
- **Measurement primitives available off the shelf**:
  - skill-creator runs with-skill vs baseline in parallel, logging `total_tokens` and `duration_ms` per run, aggregated as mean ± stddev and delta [P] ([skill-creator](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md)).
  - Copilot measured memory with an A/B on merge rate [S] ([GitHub blog](https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/)).
- **Write-back channels into hands**:
  - Codex reads AGENTS.md with a 32 KiB total budget [P] ([schema](https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json)).
  - Claude Code reads AGENTS.md natively since v2.1.277 [P] ([docs: memory](https://code.claude.com/docs/en/memory)).
  - Gemini can be configured to read AGENTS.md [P] ([gemini-md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/gemini-md.md)).
  - OpenCode and Cline read AGENTS.md [P] ([opencode rules](https://raw.githubusercontent.com/sst/opencode/master/packages/web/src/content/docs/rules.mdx); [cline rules](https://raw.githubusercontent.com/cline/cline/main/docs/customization/cline-rules.mdx)).
  - Copilot, Amp and Grok Build read AGENTS.md [S].
  - superagent grok-cli and Letta load project skills from `.agents/skills/` [P].
  - claude-reflect already syncs approved learnings to AGENTS.md and skill files [P] ([README](https://raw.githubusercontent.com/BayramAnnakov/claude-reflect/main/README.md)).
- **Process-lesson taxonomy to reuse**: the Codex Phase-1 prompt categories (tool usage lessons, failure patterns plus proven fix, verification checklists, outcome = fail for "stuck loop, tool misuse") [P] ([stage_one_system.md](https://raw.githubusercontent.com/openai/codex/main/codex-rs/memories/write/templates/memories/stage_one_system.md)).

### Inferences

**Per approach: how it differs from or plugs into the baseline**
- **Claude Code auto memory**: differs in that it is per-machine, automatic and unreviewed, and preference-oriented. It would capture little from headless hands. Plug-in: leave it on for the orchestrator (head) session only, or disable it to avoid unreviewed drift in the head's behaviour.
- **Claude subagent `memory: project`**: a candidate for giving the fresh verifier or scout roles a committed, role-scoped memory (`.claude/agent-memory/<role>/`) of recurring DoD failure modes. This must be balanced against "fresh context" independence; memory biases the verifier.
- **Claude hooks (SubagentStop / SessionEnd / agent-type)**: a deterministic place to append a structured "run record" per dispatched subagent (tokens, duration, tool-error count from `transcript_path`, `last_assistant_message`). This closes the "no per-task token or time accounting" gap for Claude-side agents.
- **Codex memories**: user-global and interactive-only. They are not a channel for spec-driven `exec`/companion runs. The Phase-1 prompt is still a ready-made template for an offline "lesson distiller" the forwarder could run over Codex rollout files after each closed or blocked issue.
- **Gemini Auto Memory**: its inbox of patches and SKILL.md drafts with human apply is the closest built-in analogue of "issue-first skill edit". Copying its contract (drafts only, target allowlist, dry-run patches, "no artifacts unless evidence strong") would upgrade incidents.md → skill edits.
- **Copilot Memory**: borrow two ideas. (a) Each lesson carries a citation (issue number, commit or file:line) and is re-validated before injection. (b) Lessons unused or unconfirmed for N pipelines expire. Together these give the missing "check that a fix reduced recurrence" signal: after a fix commit, count new incidents of that class over the next K pipelines; if zero, close; if more, reopen.
- **claude-reflect**: its multi-target sync (CLAUDE.md, AGENTS.md, skill files) with human Apply/Edit/Skip maps directly onto the missing path for lessons to reach target-repo AGENTS.md. Its correction-regex capture is useless for headless hands, but `--scan-history --include-tool-errors` over transcripts is not.
- **claude-diary**: the diary maps to the per-issue journal, which already exists and is richer. Its reflect step adds "scan for violations of existing rules (highest priority)". This is a cheap recurrence check the orchestrator could run over journals at pipeline start.
- **ECC v2 instincts**: atomic trigger→action lessons with confidence, decay and project→global promotion (2+ projects, ≥0.8) are a more granular alternative to incidents.md classes. The observer hooks only see Claude Code tool calls, not Codex or Grok hands.
- **Continuous-Claude**: the daemon-on-session-end reflection by a separate headless model equals a "separate grader". It is heavy (Postgres, 109 skills), but the pattern of spawning a cheap headless distiller after each run is directly reusable.
- **Letta skill learning**: the strongest evidence that verifier textual feedback plus trajectory reflection yields reusable skills (+9–15.7 absolute on Terminal-Bench variants, −15.7% cost). It maps one-to-one onto the baseline's verifier verdicts and rework lists as inputs.
- **learnings.md and self-improving prompts**: per-skill lesson files with a wrap-up step and periodic consolidation are a lightweight way to give each hand-role (Codex coder, Grok scout, verifier) its own lessons file injected by pointer in the dispatch envelope.
- **/insights**: useful for the human weekly retro on the head's own Claude Code sessions (friction and CLAUDE.md suggestions). It is not a pipeline component.
- **Retrieval stores** (claude-mem, Basic Memory, OpenMemory, Serena): low fit. They add infrastructure and read-time tokens. The baseline's principle "context only as text in the spec" argues for distilled rules, not retrieval.

**Suggested pipeline shape (synthesis, not sourced)**
1. **Capture**: the forwarder writes one machine-readable run record per dispatch next to the issue journal. Fields: channel, model, tokens, wall-time, tool-error count, rework count, verifier failures per DoD item, "noticed, didn't touch" items.
2. **Distill**: a separate fresh-context distiller (not the orchestrator) runs a Codex-Phase-1-style prompt over the record, the journal and the transcript. It proposes candidate lessons as patches, citing issue and commit, typed as either a spec-writing lesson (→ skill) or a hand lesson (→ target repo AGENTS.md or `.agents/skills`).
3. **Gate**: an issue-first human or orchestrator review, like Gemini's inbox or claude-reflect's Apply/Edit/Skip.
4. **Expire and verify**: each lesson has a citation and a recurrence counter. It is closed only when K subsequent pipelines show no recurrence, and expired if never triggered.
5. **Measure**: a skill-creator-style with/without benchmark on a small fixed set of replayable issues to catch regressions in tokens, time and pass rate.

### Gaps
- It is unknown which session source codex-companion uses and whether its rollouts are accessible and parseable for offline distillation. This needs a local check.
- Which Grok CLI the Orca workers run determines whether AGENTS.md, `.agents/skills` or `.grok/skills` is the correct write-back target.
- No source validates that injecting orchestrator-distilled lessons into AGENTS.md improves hand performance. The only positive evidence is vendor-run: Copilot +7 points merge rate, Letta +9–15.7 absolute on Terminal-Bench, Anthropic +39%.
