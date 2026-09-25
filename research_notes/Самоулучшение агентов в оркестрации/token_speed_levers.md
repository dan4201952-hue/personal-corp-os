# Token / speed / cost levers for orchestrated CLI coding agents (Claude Code, Codex CLI, Grok CLI) — research notes

Legend and access notes (read first):
- **[P]** = verified in a primary source fetched in this session (2026-09-25): anthropic.com, code.claude.com, platform.claude.com, raw.githubusercontent.com (vendor repos, OpenAI cookbook, Codex source), registry.npmjs.org, pypi.org.
- **[P-code]** = verified in a tool's source code or config schema (not prose docs); interpretation of code is mine and flagged.
- **[R]** = recalled from prior knowledge, **NOT verified this session**. The session-wide WebSearch budget was already exhausted (200/200) before my first query, and the hosts (manus.im, openai.com, vercel.com, cursor.com, arxiv.org, humanlayer.dev, trychroma.com) are blocked. Treat [R] items as leads to verify, not facts.
- No finding below comes from a search snippet (WebSearch returned nothing).
- "Baseline" = the `fable-ruki-agenty` skill (`/home/user/personal-corp-os/skills/fable-ruki-agenty/SKILL.md`, read in full): Fable orchestrator writes specs into GitHub issues and does not read code or call Bash. Claude subagents act as forwarders. Codex (gpt-5.5, via the OpenAI `codex` Claude Code plugin) does coding, review and verification. Grok CLI workers in Orca terminals do scouting. There is a per-issue journal, a fresh-context verifier, and an acceptance ladder (2 reworks → fresh executor → blocked). Sonnet/Haiku are banned "for any role" (founder decision, 04.07.2026).
- The current landscape at the time of writing (Sept 2026), verified: Claude Fable 5.1, Opus 5.5 (released 2026-09-22), Sonnet 5, Haiku 4.5. Claude Code v2.1.282 (2026-09-24). Codex CLI 0.157.0 (2026-09-25). OpenAI's cookbook mentions GPT-5.4 and the GPT-5.6 Luna/Terra/Sol tiers. Sources: [Anthropic newsroom](https://www.anthropic.com/news), [npm @anthropic-ai/claude-code](https://registry.npmjs.org/@anthropic-ai/claude-code), [npm @openai/codex](https://registry.npmjs.org/@openai/codex), [OpenAI cookbook: cost & quality](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/agent_optimization/optimizing_agents_for_cost_and_quality.ipynb).

---

## Q0 — Objective: ranked list of levers, applied to the baseline

### Takeaway
In current, dated, published measurements, these levers give the most savings, in order:
1. **Prompt-cache discipline.** Agent loops cost 2.7–5.3× less.
2. **A "cheap first, escalate on failure" effort policy.** When a test signal exists, the pass rate stays the same or rises at about 55–60% of the cost.
3. **Time awareness plus budgets.** Wall time drops 33–69%.
4. **Context-lifecycle hygiene at task boundaries.** Long runs cost 32–39% less.

The lever most specific to this baseline is to stop spending frontier-model tokens on LLM "forwarder" subagents. OpenAI's `codex-rescue` forwarder is pinned to `model: sonnet` in its definition. This conflicts with the founder's Sonnet ban, which may be silently violated or overridden. Such forwarders can be replaced by deterministic scripts or tools.

Caution: an orchestrator/worker split only pays for bulk, independent work. On one dependent chain, the coordinator model alone at lower effort was cheaper in every case Anthropic measured.

### Cited Findings (evidence behind the ranking; details in Q1–Q5)
- Prompt caching was "the largest lever by a wide margin". It cut agent-loop cost by a factor of 2.7–5.3 on Anthropic's benchmarks and cut a triage agent's bill by 83%, or 88% with input trimming [P] — [Anthropic: Optimizing for cost and intelligence (live doc, measurements Aug–Sep 2026)](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)
- Re-running failures at higher effort was tested with Opus 5.5 on a SWE-bench Pro subset. Running everything at `low` and re-running the 13% of failures at `high` gave about 97% pass at about $0.17 per task. Running everything at `high` gave 95.3% at $0.29. Two conditions apply: a failure signal is required, and wall-clock doubles on failures [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)
- Adding a "time matters" instruction plus an elapsed-time system message on each turn gave 33–69% less time and 28–54% lower cost per task. Scores changed by +0.2 to −1.9 points, and some confidence intervals fell beyond the pre-set margins (Fable 5.1 at `high`; DRACO, HLE and an internal physics set) [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)
- On a long run, pruning at task boundaries saved 39% and compaction saved 32%. On a short 20-issue run, context editing cost 74% more [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)
- On single dependent chains, orchestration does not pay: "When the work is one dependent chain, or fits in a single context… In every such case measured, the coordinator's model alone at lower effort came out ahead" [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)
- OpenAI's Claude Code plugin defines the `codex:codex-rescue` subagent with `model: sonnet` and `tools: Bash`. It preloads two skills (`codex-cli-runtime` ≈3.1 KB, `gpt-5-4-prompting` ≈3.6 KB). It is told to make exactly one Bash call to `codex-companion.mjs task`, and it may "tighten the user's request into a better Codex prompt" [P] — [openai/codex-plugin-cc codex-rescue.md](https://raw.githubusercontent.com/openai/codex-plugin-cc/main/plugins/codex/agents/codex-rescue.md) (plugin v1.0.6, fetched 2026-09-25)
- In Claude Code, a subagent's `model` frontmatter takes precedence over `CLAUDE_CODE_SUBAGENT_MODEL`. Only `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` overrides it. `/tasks` shows which model each subagent actually ran on [P] — [Claude Code docs: subagents](https://code.claude.com/docs/en/sub-agents)
- Anthropic list prices per MTok (input/output, cache read): Fable 5.1 $10/$50 (cache read $0.25); Opus 5.5 $4/$20 (cache read $0.20); Sonnet 5 $2/$10. On Max plans Fable draws on "50% of weekly limits"; on Pro it uses "Usage credits" [P] — [anthropic.com/pricing](https://www.anthropic.com/pricing) (fetched 2026-09-25)

### Inferences — ranked levers for this baseline
The ranking is my synthesis. It weighs expected savings on the scarcest resource (Fable quota, then wall time), strength of evidence, and ease of adoption.

1. **Cache discipline for every long-lived agent (orchestrator first).**
   - *Mechanism:* the prefix-match KV cache re-bills repeated context at 0.1× input (0.05× on Opus 5.5, 0.025× on Fable 5.1).
   - *Claude Code / orchestrator:*
     - Pick model and effort once per session; do not use `/model` mid-session. `opusplan` toggles, a skill's `model:` frontmatter and automatic fallbacks all count as model switches.
     - Do not connect or disconnect MCP servers or plugins mid-session.
     - Compact only at issue boundaries.
     - Watch the `Prompt cache (main)` line in `/usage` (v2.1.251+).
     - Set `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL=1h` (or `experimental.cacheTtl: 1h` per agent) for forwarders that sit idle while Codex runs. Subagents get a 5-minute TTL even on a subscription.
   - *Codex:* keep AGENTS.md and tool sets stable, and `--resume` the same thread for reworks.
   - *Evidence:* 2.7–5.3× cheaper loops. The production median cache-read share is 84% and the top decile is ≥94% (Q2).
   - *Risk:* caching fights context editing and compaction; every rewrite is a cache miss.
2. **De-LLM the plumbing (forwarders, journal posts, closes).**
   - *Mechanism:* each forwarder is a whole subagent session (fresh prefix, separate cache, CLAUDE.md reload, reasoning) that does one Bash call.
   - *Apply:*
     - (a) Replace the gh/orca/codex forwarders with deterministic scripts exposed as a tool that is not Bash (a small MCP server or plugin command) or as hooks. This keeps the "Fable never calls Bash" rule.
     - (b) If you keep LLM forwarders, pin them to `model: opus` (Opus 5.5 is not banned) with `effort: low`, `omitClaudeMd: true` (v2.1.271+), a small `maxTurns` and a 1h cache TTL.
     - (c) Verify the forwarder's actual model with `/tasks`. As shipped, `codex-rescue` asks for Sonnet.
   - *Savings:* not measured. By inference, it removes several subagent sessions per issue (dispatch, one journal post per phase, verifier dispatch, close).
   - *Also fixes:* "empty prompt at spawn" and "lost report" incidents, which are LLM-forwarder failure modes.
   - *Hypothesis to check:* a foreground `--wait` Bash call is subject to Claude Code's Bash timeouts (2 min default, 10 min maximum). A Codex run longer than that could kill the forwarder's call and "lose" the report (Q4.5).
3. **Build the effort ladder into the acceptance ladder.**
   - *Codex:* first attempt at `--effort medium` (`low` for mechanical tasks). Rework 1 in the same thread with the verifier diff. Rework 2 at `high`. Fresh executor at `high`/`xhigh`.
   - *Evidence:* Anthropic's "low then re-run failures at high" result (same pass rate at about 58% of the cost). OpenAI recommends `medium` as the all-round Codex setting.
   - *Scouts:* Grok on a non-reasoning model for pure retrieval.
   - *Orchestrator:* Fable effort can change without a cache miss on Fable 5.1 (Claude Code v2.1.260+).
   - *Risk:* low effort can hide "I'm stuck" signals; sweep per workload.
4. **Deterministic-first verification.**
   - The script (not an LLM) runs each DoD command and posts raw output. An LLM verifier runs only on DoD items that cannot be expressed as a command, at low effort, and may answer "unverifiable".
   - During reworks, use sampled test subsets (C-compiler `--fast` 1–10%); run the full suite at acceptance.
   - *Evidence:* code graders are "fast, cheap, objective". QA cost about 8% of a $124 harness run. The Claude Code `/goal` checker is a "small fast model".
   - *Risk:* a checker that passes bad work lets failures through. The baseline's "the check must be able to fail" rule already mitigates this.
5. **Time boxes, watchdogs and a clock.**
   - Wrap each Grok/Codex worker in `timeout` plus a heartbeat on its NDJSON event stream: no event for N seconds → kill and respawn with a narrower spec. Forbid broad globs in scout prompts; use `rg --files -g … <abs root>`. Set `--max-tool-rounds` for headless Grok.
   - Add the two-sentence "time matters" instruction to worker prompts. If the workers are Claude-based, inject elapsed time.
   - *Evidence:* −33–69% time with the clock; Claude Code's own Glob timeout is 20 s.
   - *Risk:* premature wrap-up (score −1–2 points on some sets).
6. **Context lifecycle at issue boundaries.**
   - Orchestrator: compact or `/clear` between issues with custom compaction instructions (queue state, open forks). GitHub issues already act as the handoff document.
   - Codex: `--fresh` per issue, `--resume` for reworks, and `model_post_turn_compact_threshold_percent` (turn-end compaction) around 50–60 so compaction happens at natural breaks.
   - Avoid API context editing on short runs.
   - *Evidence:* −32% to −39% on long runs; +74% for context editing on short runs.
7. **Tool-output hygiene.**
   - Cap and filter outputs: Codex `tool_output_token_limit` about 10k with head+tail truncation (OpenAI guidance), Claude Code PreToolUse hooks that filter test output, RTK-style command proxies.
   - Scouts return `file:line` lists rather than dumps (already a baseline rule).
   - *Evidence:* RTK claims "up to 90% of bash output"; it states this is not the bill. Anthropic's data-file test was 12× cheaper and 25/25 correct instead of 6/25.
   - *Risk:* truncation can hide the failing line.
8. **Model routing inside the allowed set.**
   - Fable only for specs and fork resolution. Opus 5.5 (`medium`) for any Claude-side helper. Codex mini/spark for mechanical operations; the plugin supports `--model gpt-5.4-mini` and `spark`. Grok non-reasoning for scouting.
   - *Evidence:* Opus 5.5 at default matched Fable 5.1 at default on a SWE-bench Pro subset at about one fifth of the cost per solved task.
   - *Risk:* each model has its own cache; hard-tail tasks.
9. **Prompt audit of the skill and the dispatch envelope, and self-contained specs.**
   - Remove "verify twice"-style rules from executor prompts where a separate verifier exists. Keep AGENTS.md small (Codex caps it at 32 KiB). Do not ask Codex for status updates or preambles mid-run.
   - *Evidence:* stale prompts cost +36% per ticket; removing "verify twice" cut cost by one third; Claude Code's brevity-limit prompt cost 3% on an eval.
10. **Git-worktree parallelism, only for file-disjoint bulk.**
    - *Evidence:* 2.3 h instead of 15–20 h wall time with 25 workers, but only for work larger than one context window.
    - *Costs:* tokens rise. Claude Code worktrees do not share each other's caches, and each needs dependencies installed.
    - *Risks:* resource headroom matters (up to 6 percentage points of success), and subscription 5-hour windows drain faster.
11. **Navigation aids for scouts.**
    - Give scouts a precomputed repo map or symbol index (Aider `--map-tokens` about 1k, ctags/ast-grep, Serena LSP, or a semantic index) so they do not glob-walk.
    - *Evidence:* moderate and mostly vendor-run. Claude Context reported −39% tokens and −36% tool calls at equal F1 on 30 SWE-bench instances with GPT-4o-mini.
12. **Tool Search / code mode / programmatic tool calling.**
    - Claude Code already defers MCP tools by default. This matters only if worker sessions carry large MCP catalogs.
    - *Evidence:* −85% of definition tokens; −45% run cost at 502 tools; PTC −37% tokens.
13. **Batch or flex for offline steps.**
    - Use for the weekly retro over the incident journal, re-grading and summaries: 50% off (Anthropic Batch, OpenAI Batch/Flex, Grok CLI `--batch-api`).
    - Not applicable to interactive worker loops.
14. **Subscription vs API placement.**
    - Keep interactive loops on subscriptions. On a subscription the main conversation gets a 1h cache TTL, which drops to 5 min once usage credits are drawn.
    - Watch that `claude -p` / SDK runs bill Fable to usage credits without asking.
    - Use API plus Batch for unattended bulk.
    - Quotas change often.

**Do-not list:**
- API context editing on short runs (+74% cost).
- Lowering `max_tokens` to save money: cost per solved task stays about the same.
- Global brevity limits in system prompts (−3% on an eval).
- An advisor pairing without measuring the consult rate.
- Adding orchestration layers for one dependent chain.

### Gaps
- There is no public measurement of a Claude-subagent-forwarder → Codex pipeline's overhead per issue; the savings from lever 2 are inferred, not measured.
- I could not verify which model the baseline's forwarders actually run on. The plugin frontmatter says `sonnet`, and the founder bans Sonnet. The user's `availableModels` or `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` settings are unknown.
- Most Anthropic measurements are API-priced. How subscription quotas weight cache reads versus uncached input for Claude Code, and weight cached tokens for Codex/ChatGPT plans, is not documented in any source I could reach.

---

## Q1 — Context management

### Takeaway
Context is the core constraint. Claude Code's docs state that "performance degrades as it fills". The measured winners are:
- Fresh, isolated contexts for verbose side-work (subagents), paying roughly 4–15× more total tokens for multi-agent setups.
- Deliberate compaction or pruning at natural task boundaries rather than automatic mid-task compaction.
- Short always-loaded instructions (Claude Code: under 200 lines; Codex: 32 KiB cap), with the rest delivered on demand via skills.
- Structured handoff files (progress file, git log, feature list, ExecPlans).

API context editing is a context-window tool, not a savings lever: in Anthropic's 2026 run it cost 74% more on a short run. Context-rot evidence is real but mostly qualitative for 2026 frontier models. Newer models (Opus 4.5+) removed the "context anxiety" that made resets necessary for Sonnet 4.5.

### Cited Findings

#### 1.1 Subagent context isolation and its overhead
- **Mechanism (Anthropic, 2025-09-29):** each subagent "might explore extensively, using tens of thousands of tokens or more, but returns only a condensed, distilled summary of its work (often 1,000–2,000 tokens)" [P] — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- **Token overhead, measured (Anthropic, 2025-06-13):** agents use about 4× more tokens than chat, and multi-agent systems about 15× more. Token usage alone explains 80% of BrowseComp performance variance (three factors explain 95%). A lead Opus 4 with Sonnet 4 subagents outperformed single-agent Opus 4 by 90.2% on an internal research eval [P] — [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- **Agent teams in Claude Code:** "approximately 7x more tokens than standard sessions when teammates run in plan mode". Guidance: keep teams small and spawn prompts focused, and shut teammates down when done. Agent teams became a research preview in v2.1.32 (2026-02-05) [P] — [Claude Code docs: costs](https://code.claude.com/docs/en/costs); [Claude Code CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md) with dates from [npm](https://registry.npmjs.org/@anthropic-ai/claude-code)
- **What a non-fork Claude Code subagent loads** [P] — [Claude Code docs: subagents](https://code.claude.com/docs/en/sub-agents):
  - its own system prompt, the task message and the full CLAUDE.md hierarchy;
  - a git-status snapshot and any preloaded skills.
  - Explore and Plan skip CLAUDE.md and git status "to keep research fast and inexpensive". `omitClaudeMd: true` (v2.1.271, 2026-09-14) lets custom subagents skip it too.
  - "Latency matters. A subagent that isn't a fork starts fresh and may need time to gather context."
  - Default concurrency limit: 20 running subagents (v2.1.217+).
- **Cache cost of subagents** [P] — [Claude Code docs: prompt caching](https://code.claude.com/docs/en/prompt-caching); [Claude Code docs: subagents](https://code.claude.com/docs/en/sub-agents):
  - A subagent's first request does not read the parent's cache (different prefix).
  - Subagents get a 5-minute TTL even on a subscription unless configured otherwise.
  - A **fork** (`/subtask`, v2.1.212+) inherits the parent's prefix, reads the parent's cache and is therefore "cheaper than spawning a fresh subagent for tasks that need the same context".
- **Model routing of subagents in Claude Code; this changed in 2026** [P] — [Claude Code docs: subagents](https://code.claude.com/docs/en/sub-agents); [CHANGELOG v2.0.17](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md):
  - The Haiku-powered Explore subagent arrived in v2.0.17 (2025-10-15).
  - Since v2.1.198 (2026-07-01), Explore inherits the main model, capped at Opus.
  - `CLAUDE_CODE_SUBAGENT_MODEL` sets the default; `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` overrides even frontmatter.
- **Anthropic's 2026 cost guide on subagents:** subagents are for "self-contained bulky steps"; "skip when the deciding model needs the intermediate context to judge well". The subagent "starts a fresh prefix with no cache shared with the parent" [P] — [claude-api skill cost-optimization reference (bundled with Claude Code 2.1.282)](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence) (same measurements are in the live guide)
- **Illustrative example (not a measurement):** a research subagent read 6,100 tokens of files; the main context received a 420-token result [P] — [Claude Code docs: context window simulation](https://code.claude.com/docs/en/context-window)
- **Practitioner view:** "Subagents are not about playing house and anthropomorphizing roles… Subagents are about context control" (HumanLayer, Aug 2025; anecdotal) [P] — [HumanLayer ACE-FCA](https://raw.githubusercontent.com/humanlayer/advanced-context-engineering-for-coding-agents/main/ace-fca.md)

#### 1.2 Compaction, auto-compact, "frequent intentional compaction", resets
- **Claude Code auto-compact defaults (Sept 2026)** [P] — [Claude Code docs: model config](https://code.claude.com/docs/en/model-config); [Claude Code docs: env vars](https://code.claude.com/docs/en/env-vars):
  - 1M-window models (Sonnet 5, Fable, Opus 4.7+ on the Anthropic API) compact "at about 967K tokens by default", i.e., late.
  - Sonnet 4.6 / Opus 4.6 without extended context compact at the 200K boundary.
  - The window is configurable from 100K to 1M via `/autocompact 500k`, `--autocompact`, or `CLAUDE_CODE_AUTO_COMPACT_WINDOW`.
  - `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` can only lower the trigger percentage, and it applies to subagents too.
- **Compaction cost mechanics in Claude Code** [P] — [Claude Code docs: prompt caching](https://code.claude.com/docs/en/prompt-caching); [Claude Code docs: costs](https://code.claude.com/docs/en/costs):
  - The summarization request reuses the cached prefix, so "a mid-session /compact costs a fraction of what the context size suggests".
  - After a break longer than the cache TTL, it re-processes the full history uncached.
  - Recommendation: "run /compact at a natural break in your work… instead of waiting for auto-compaction to trigger mid-task". `/clear` "costs nothing".
  - `/compact <focus>` and a "Compact instructions" section in CLAUDE.md steer what survives.
- **Anthropic's measurement of compaction timing (Aug 2026)** [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence):
  - A mid-session effort change plus an added tool rewrote 39,000 and 60,000 cached tokens: $0.95/session versus $0.81 with no changes.
  - The same changes on the first request after compaction cost $0.75. On the request that triggered compaction they cost $0.92, because the summarization pass re-processed 81K tokens at the write price.
  - Accuracy was within noise in all arms.
- **Claude Code "resume from summary":** when resuming a large session after a long break, Claude Code offers to run `/compact` immediately. The history is replaced with the summary, the most recent exchanges and up to five recently read files [P] — [Claude Code docs: sessions](https://code.claude.com/docs/en/sessions)
- **Claude Code thrashing guard:** if a file or tool output immediately refills the window several times after compaction, Claude Code stops with "Autocompact is thrashing". The fix is to compact with a focus that drops the large output or to move the large-file work to a subagent [P] — [Claude Code docs: troubleshooting](https://code.claude.com/docs/en/troubleshooting)
- **Codex CLI compaction controls (config schema, main branch, fetched 2026-09-25)** [P-code] — [openai/codex config.schema.json](https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json):
  - `model_auto_compact_token_limit`, "token usage threshold triggering auto-compaction".
  - `model_auto_compact_token_limit_scope`, either `total` or `body_after_prefix`.
  - `model_post_turn_compact_threshold_percent`: "Percentage of the usable context window that triggers compaction after a final response… Omitted or zero disables turn-end compaction". This is effectively a built-in "intentional compaction at turn end".
  - `compact_prompt` and `experimental_compact_prompt_file`.
  - The compaction code keeps `COMPACT_USER_MESSAGE_MAX_TOKENS = 20_000`, which I read as the budget for retained recent user messages (my interpretation of the code) [P-code] — [codex compact.rs](https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/src/compact.rs)
- **OpenAI guidance** [P] — [Codex Prompting Guide (cookbook, updated 2026-02-25)](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/gpt-5/codex_prompting_guide.ipynb); [GPT-5.2 prompting guide (2025-12-11)](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/gpt-5/gpt-5-2_prompting_guide.ipynb):
  - Codex models have "first-class compaction support".
  - For `/responses/compact`: "Compact after major milestones (e.g., tool-heavy phases), not every turn" and "Keep prompts functionally identical when resuming to avoid behavior drift".
- **OpenAI on the cache/compaction tension:** "when you drop, summarize or compact earlier turns in a conversation, you'll break the cache… context engineering and prompt caching are inherently at odds". The Responses API supports `context_management=[{"type":"compaction","compact_threshold":100000}]` [P] — [OpenAI cookbook: Prompt Caching 201 (2026-02-18)](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/Prompt_Caching_201.ipynb)
- **"Frequent intentional compaction"** (Dex Horthy / HumanLayer, Aug 2025; case studies, anecdotal) [P] — [HumanLayer ACE-FCA](https://raw.githubusercontent.com/humanlayer/advanced-context-engineering-for-coding-agents/main/ace-fca.md):
  - Design the whole workflow around context and keep utilization "in the 40%–60% range". Use research → plan → implement phases, each compacted into files (e.g., `progress.md`).
  - Case studies: a bug fix in the 300k-LOC Rust BAML codebase got a PR approved; 35k LOC were shipped with a collaborator.
- **Context resets vs compaction** [P] — [Harness design for long-running application development (Prithvi Rajasekaran, 2026-03-24)](https://www.anthropic.com/engineering/harness-design-long-running-apps); [Scaling Managed Agents (2026-04-08)](https://www.anthropic.com/engineering/managed-agents):
  - Sonnet 4.5 showed "context anxiety" (wrapping up prematurely near its perceived limit) strongly enough that "compaction alone wasn't sufficient", so context resets with structured handoffs "became essential". Resets add "orchestration complexity, token overhead, and latency".
  - "Opus 4.5 largely removed that behavior", so resets were dropped. Managed Agents calls them "dead weight".
- **Long-running harness** [P] — [Effective harnesses for long-running agents (Justin Young, 2025-11-26)](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): "compaction isn't sufficient" for multi-window builds. Opus 4.5 given only a high-level prompt tended to one-shot the task and run out of context mid-feature.

#### 1.3 Context editing and the memory tool (Anthropic API)
- **Launch claims (2025-09-29):** combining the memory tool and context editing improved performance 39% over baseline on an internal agentic-search eval; context editing alone gave 29%. In a 100-turn web-search eval, context editing let workflows complete that would otherwise exhaust context "while reducing token consumption by 84%" (internal eval; methodology not published) [P] — [Anthropic: Managing context on the Claude Developer Platform](https://www.anthropic.com/news/context-management)
- **Later, contradicting cost measurement (2026)** [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence):
  - "Context editing, a token-hygiene lever, cost more than it saved in the run measured". It cost +74% on the 20-issue run and changed nothing on the long run.
  - A client-side prune (replace stale tool results with one-line extracts at each task boundary) saved 39%. It kept 89% cache reads on the first request after a boundary and 81% between boundaries.
  - "If you use context editing, clear in a few large batches."
- **API mechanics** [P] — [Anthropic docs: context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing); claude-api skill reference:
  - Strategies `clear_tool_uses_20250919` (optionally clearing tool inputs) and `clear_thinking_20251015`, under beta `context-management-2025-06-27`.
  - Tool-result clearing invalidates the cache from the point it clears; use `clear_at_least` so each invalidation is worth it.
  - The memory tool type is `memory_20250818`; it is client-side file storage.
- **Server-side compaction:** a separate feature (skill reference: beta `compact-2026-01-12`, default trigger 150K tokens). The live docs now describe on-demand and threshold compaction under beta header `compact-2026-09-04` [P] — [Anthropic docs: compaction](https://platform.claude.com/docs/en/build-with-claude/compaction). *Renamed/extended during 2026.*
- **Real-world regression from thinking-clearing (Mar–Apr 2026):** a Claude Code change used `clear_thinking_20251015` to drop old thinking after 1h idle. A bug made it clear on every turn, which caused "forgetfulness, repetition, and odd tool choices" and cache misses. Anthropic believes this drove the reports of "usage limits draining faster". It was fixed on 2026-04-10 [P] — [An update on recent Claude Code quality reports (2026-04-23)](https://www.anthropic.com/engineering/april-23-postmortem)
- **Managed Agents view:** "irreversible decisions to selectively retain or discard context can lead to failures". Anthropic explores storing context as an object outside the window [P] — [Scaling Managed Agents (2026-04-08)](https://www.anthropic.com/engineering/managed-agents)

#### 1.4 Context-rot limits
- **Anthropic (2025-09-29):**
  - "as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases… this characteristic emerges across all models". There is an "attention budget" (n² pairwise relationships).
  - Guiding principle: "find the smallest set of high-signal tokens".
  - Even larger windows "will be subject to context pollution and information relevance concerns" [P] — [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- **Claude Code best practices (current):** "LLM performance degrades as context fills… Claude may start 'forgetting' earlier instructions or making more mistakes. The context window is the most important resource to manage" [P] — [Claude Code docs: best practices](https://code.claude.com/docs/en/best-practices)
- **Chroma "Context Rot" (research repo):** "model performance varies significantly as input length changes, even on simple tasks". Experiments: a NIAH extension with semantic needles and haystack variations, LongMemEval, and repeated words [P] — [chroma-core/context-rot README](https://raw.githubusercontent.com/chroma-core/context-rot/master/README.md); technical report at [research.trychroma.com/context-rot](https://research.trychroma.com/context-rot)
  - [R] The report (Kelly Hong et al., 2025-07-14) evaluated 18 LLMs (GPT-4.1, Claude 4, Gemini 2.5, Qwen3). Shuffled haystacks scored better than coherent ones, and full ~113K-token LongMemEval prompts scored markedly worse than focused ~300-token ones.
- **Newer frontier models hold longer sessions**, at least per the vendor: Claude Code says of Fable, "Size up larger tasks… It holds long sessions without losing the thread" (vendor guidance, not a measurement) [P] — [Claude Code docs: model config](https://code.claude.com/docs/en/model-config). The Opus 4.5+ removal of "context anxiety" is in 1.2.

#### 1.5 Short CLAUDE.md / AGENTS.md; progressive disclosure via skills
- **Claude Code sizing guidance** [P] — [Claude Code docs: memory](https://code.claude.com/docs/en/memory); [Claude Code docs: costs](https://code.claude.com/docs/en/costs):
  - "target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence."
  - Move multi-step procedures to skills or path-scoped rules; "Aim to keep CLAUDE.md under 200 lines by including only essentials".
  - Auto memory loads only the first 200 lines or 25 KB.
- **Context cost by feature** [P] — [Claude Code docs: features overview](https://code.claude.com/docs/en/features-overview):
  - Skills: "Low (descriptions every request)", full content only when used.
  - Hooks: "Zero unless the hook returns output".
  - Illustrative startup sizes: system prompt ~4,200 tokens, project CLAUDE.md ~1,800, skill descriptions ~450, deferred MCP tool names ~120 [P] — [Claude Code docs: context window](https://code.claude.com/docs/en/context-window)
- **Agent Skills progressive disclosure (Anthropic, 2025-10-16; open standard 2025-12-18):** metadata first, the SKILL.md body when relevant, extra files only as needed. "sorting a list via token generation is far more expensive than simply running a sorting algorithm"; scripts run without being loaded into context [P] — [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- **Codex AGENTS.md:** `project_doc_max_bytes` defaults to 32,768 bytes of project instructions in total [P-code] — [codex config.schema.json](https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json). AGENTS.md files are merged root-to-leaf and injected as user-role messages [P] — [Codex Prompting Guide](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/gpt-5/codex_prompting_guide.ipynb)
- **Stale or over-prescriptive instructions cost money and accuracy (Anthropic, measured Aug 2026)** [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence):
  - Prompts written for Opus 4.8 cost 36% more per ticket on Opus 5 with no accuracy change.
  - Removing "verify twice" cut cost per ticket by a third, and removing "be maximally thorough" almost as much.
  - A retired thinking setting, contradictory rules and a hand-rolled scratchpad each cost 7–11 accuracy points.
  - Setup: 44-ticket support-desk set, deterministic grading.
- **Brevity instructions can hurt (Anthropic, Apr 2026):** a Claude Code system-prompt line ("keep text between tool calls to ≤25 words… final responses to ≤100 words") showed a 3% drop on one eval for Opus 4.6 and 4.7 and was reverted [P] — [Claude Code quality postmortem](https://www.anthropic.com/engineering/april-23-postmortem)
- **ETH Zurich AGENTBench harness exists:** it evaluates coding agents with repository context set to `NONE`, `LLM`-generated, or `HUMAN`-written AGENTS.md/CLAUDE.md, and analyzes "traces and costs" [P] — [eth-sri/agentbench README](https://raw.githubusercontent.com/eth-sri/agentbench/main/README.md)
  - [R] Paper result (Feb 2026, not verified): LLM-generated context files slightly reduced success (~−3%) and raised cost by over 20%; human-written ones helped modestly (~+4%).
- [R] Vercel, Jan 2026, not verified: a compressed ~8 KB docs index in AGENTS.md reached 100% on their Next.js agent evals, versus skills at ~53% by default (the skill often not invoked) and ~79% with explicit instructions — [Vercel blog](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals). This is a counterpoint: on-demand skills can fail to trigger.
- [R] HumanLayer, Nov 2025, not verified: frontier models follow ~150–200 instructions reasonably; recommends CLAUDE.md under 300 lines (theirs under 60) — [HumanLayer blog](https://www.humanlayer.dev/blog/writing-a-good-claude-md)

#### 1.6 Handoff documents between sessions
- **Anthropic long-running harness (2025-11-26)** [P] — [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents):
  - An initializer agent writes `init.sh`, `claude-progress.txt`, an initial commit, and a feature list (200+ features marked "failing").
  - Every coding session starts by reading the progress file and git log and running a basic test. It ends with a commit and a progress update.
  - This "saves Claude some tokens in every session since it doesn't have to figure out how to test the code".
- **Harness design (2026-03-24):** a structured handoff artifact must carry "enough state for the next agent to pick up the work cleanly". Agents communicated via files, one writing and another reading and responding [P] — [Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- **OpenAI ExecPlans (article dated 2025-10-07):** PLANS.md "living documents", fully self-contained so "a novice" could succeed. The team says a similar PLANS.md "enabled Codex to work for more than seven hours from a single prompt" (anecdote) [P] — [OpenAI cookbook: Using PLANS.md](https://raw.githubusercontent.com/openai/openai-cookbook/main/articles/codex_exec_plans.md)
- **OpenAI "Iterating Development Workflows with Codex" (2026-08-03):** AGENTS.md prompts make Codex capture per-phase context files (`harness/context/phase-<NN>-…-context.md`) for later reuse, and a skill automates the process [P] — [OpenAI cookbook](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/codex/iterating-development-workflows-with-codex.md)
- **Claude Code best practices:** when you've "corrected Claude more than twice on the same issue… Run /clear and start fresh with a more specific prompt… A clean session with a better prompt almost always outperforms a long session with accumulated corrections". Write a self-contained spec, then "start a fresh session to execute it" [P] — [Claude Code docs: best practices](https://code.claude.com/docs/en/best-practices)

### Inferences
- **The acceptance ladder already matches vendor guidance.** Two reworks, then a fresh executor, mirrors Claude Code's "corrected more than twice → /clear and restart". Making the fresh executor also a higher-effort executor gives the measured "escalate on failure" economics (Q2.5).
- **The scratchpad-report protocol is the right shape.** Full report in a file plus a ≤15-line digest matches Anthropic's "subagent output to filesystem + lightweight references" and "condensed 1,000–2,000-token summaries".
- **Fable, the orchestrator, runs a single long session:**
  - With 1M-window models, Claude Code will not auto-compact until about 967K tokens. Given context-rot evidence and the cache-rewrite cost of compaction, an explicit window (e.g., `/autocompact 300k`) plus manual `/compact <keep queue, decisions, open forks>` at issue boundaries is likely better than waiting for auto-compaction.
  - The optimal threshold is unmeasured; HumanLayer's 40–60% is anecdotal.
- **Codex workers:** `model_post_turn_compact_threshold_percent` is the closest built-in equivalent of "frequent intentional compaction at natural breaks". Combining it with `--fresh` per issue limits both rot and cache waste.
- **Avoid API context editing** (not used in the baseline anyway) and prefer boundary pruning if a custom harness is built.
- **Instruction files:**
  - The 290-line, ~37 KB SKILL.md is loaded only when invoked (`disable-model-invocation: true`) but then sits in Fable's prefix for the whole session. It is cached, so cost is modest; the adherence and over-obedience risk ("verify twice"-style rules) matters more than its tokens. An audit against Fable 5.1 (`/claude-api prompt-audit`) is a cheap, measured-positive step.
  - Codex executors read the repo's AGENTS.md on every run; keep it far below the 32 KiB cap.

### Gaps
- No 2026 public measurement quantifies context rot for Fable 5.1, Opus 5.5 or GPT-5.5 at specific fill levels. The Chroma study (2025) predates them.
- There is no measured comparison of compaction thresholds (e.g., 30% vs 60% vs 95%) for coding agents; HumanLayer's 40–60% is practitioner advice.
- The ETH AGENTBench numbers and Vercel's skills-vs-AGENTS.md eval could not be verified (blocked hosts).
- [R-leads] Amp's "handoff instead of compaction" (ampcode.com, late 2025) could not be verified.

---

## Q2 — Caching and pricing

### Takeaway
Caching is the single largest lever on every vendor. The recipe:
- stable prefixes, append-only history;
- no mid-session model, effort or tool changes;
- a TTL matched to wait gaps;
- `prompt_cache_key` on OpenAI.

Batch/flex gives a stacked 50% off, but only for work no one waits on. For routing and effort, compare **cost per solved task**, never per-token price:
- a stronger model at low effort often beats a weaker model at default;
- "low effort + re-run failures at high" was the cheapest measured coding policy;
- effort defaults keep changing (Claude Code: high→medium→reverted→Opus 5.5 default medium).

### Cited Findings

#### 2.1 Prompt caching hit-rate practices
- **Magnitude (Anthropic, measured Aug 2026)** [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence):
  - Caching cut agent-loop cost by 2.7–5.3×. The benchmark runs read 79–90% of input from cache.
  - Over 14 days of first-party API traffic ending 2026-08-23, agent loops read a median 84% of input from cache; the top 10% of harnesses read ≥94%. "Deep in a task, a well-built loop pays full price on under 1% of its input."
  - "A 40-turn task sends its first turn 40 times", so cost grows about with the square of turn count.
- **Anthropic on Opus 5.5 (2026-09-22):** "Cache reads (which make up the majority of agentic and coding work costs)" are $0.20/M, down from $0.50 on Opus 5 [P] — [Introducing Claude Opus 5.5](https://www.anthropic.com/news/claude-opus-5-5)
- **Multipliers:**
  - Cache read about 0.1× input (0.025× on Fable 5.1, 0.05× on Opus 5.5). Writes 1.25× for the 5-minute TTL and 2× for the 1-hour TTL.
  - The minimum cacheable prefix is 512 tokens on Opus 5/Fable and 4,096 on Opus 4.6/4.5/Haiku 4.5.
  - A cache read refreshes the timer, and generation time counts against the TTL [P] — [claude-api skill: prompt-caching reference](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) (bundled in Claude Code 2.1.282); prices [P] — [anthropic.com/pricing](https://www.anthropic.com/pricing)
- **TTL choice (measured)** [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence):
  - Use 1h when more than about 1 in 20 gaps fall between 5 and 60 minutes and gaps over an hour are rare.
  - With no pauses, 5-min was 15% cheaper than 1h on Sonnet 5 and 15–18% cheaper on Opus 5.5.
  - On Fable 5.1, keep-alive requests are usually cheaper than the 1h TTL: resend the previous request with `max_tokens: 0` within 4 minutes of the previous request's start.
- **Claude Code specifics** [P] — [Claude Code docs: prompt caching](https://code.claude.com/docs/en/prompt-caching):
  - **TTL:**
    - On a subscription within included usage, the main conversation gets a 1-hour TTL. Subagents, workflows, teammates, forks and compaction get 5 minutes.
    - Once usage credits are drawn, the main conversation drops to 5 minutes. On an API key it is 5 minutes by default.
    - Controls: `promptCacheTtl`, `subagentPromptCacheTtl` and the corresponding env vars (v2.1.242+, 2026-08-24).
  - **Invalidators:**
    - switching models, including `opusplan` plan-mode toggles, a skill `model:` frontmatter and automatic safety fallbacks;
    - changing effort, except on Opus 5.5/Fable 5.1 via API key or subscription since v2.1.260 (2026-09-03);
    - the first enabling of fast mode;
    - MCP connect/disconnect when tools are in the prefix;
    - compaction (by design), many images, and Claude Code upgrades.
  - **Cache-safe:** file edits, CLAUDE.md edits (which don't apply until `/clear`/`/compact`/restart), permission-mode and output-style changes, skills and commands, `/recap`, `/rewind`, and spawning subagents.
  - **Scope:** "effectively scoped to one machine and directory". Worktrees of the same repo "build different prefixes and miss each other's cache". Parallel sessions in the same directory share it. The Agent SDK can suppress per-machine sections to share across machines.
  - **Monitoring:** `/usage` shows the `Prompt cache (main)` hit share and misses (v2.1.251+). The likely cause of the last miss is shown in v2.1.260+.
- **OpenAI** [P] — [Prompt Caching 201 (OpenAI cookbook, 2026-02-18)](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/Prompt_Caching_201.ipynb):
  - Caching reduces TTFT "by up to 80%" and input cost "by up to 90%". It is automatic from 1,024 tokens, in 128-token increments; extended caching lasts 24 h.
  - `prompt_cache_key` improves routing stickiness: "one of our coding customers saw an improved hit rate from 60% to 87%". Keep each prefix+key combination under about 15 RPM.
  - Use `allowed_tools` to restrict tools without changing the tools array.
  - In the author's test over 2,300 runs, TTFT was 7% faster at 1,024 tokens and 67% faster at 150K+ tokens.
  - Discount table: gpt-5.2 $1.75 input vs $0.175 cached (90% off).
  - "In the Codex CLI, system instructions, tool definitions, sandbox configuration, and environment context are kept identical and consistently ordered between requests… The agent loop appends new messages (rather than modifying earlier ones) when runtime configurations change". This summarizes OpenAI's "Unrolling the Codex agent loop" ([openai.com, not fetched](https://openai.com/index/unrolling-the-codex-agent-loop/)).
- **GPT-5.6 caching change (OpenAI cookbook, verified 2026-09-14):** "cache writes are billed" (1.25× input), with explicit cache breakpoints (`prompt_cache_breakpoint`). The default breakpoint sits after the latest message, so repeatedly caching unique messages "can increase cost without creating useful reuse" [P] — [OpenAI cookbook: Optimizing agents for cost and quality](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/agent_optimization/optimizing_agents_for_cost_and_quality.ipynb)
- **Gemini CLI:** token caching works only with API-key or Vertex auth, "not available for OAuth users (Google Personal/Enterprise accounts)"; see `/stats` [P] — [gemini-cli docs: token caching](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/token-caching.md)
- **Manus (Yichao "Peak" Ji, 2025-07-18)** [R, not verified] — [Manus blog: Context Engineering for AI Agents](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus):
  - "KV-cache hit rate is the single most important metric for a production-stage AI agent". Their input:output ratio is about 100:1. Cached Claude Sonnet input was $0.30/MTok versus $3/MTok uncached (10×).
  - Rules: never put a to-the-second timestamp at the prompt head; keep context append-only; serialize deterministically (stable JSON key order); mark cache breakpoints explicitly; route self-hosted requests by session ID.
  - "Mask, don't remove" tools: change tool availability by logit masking or prefill, not by editing tool definitions.
  - Use the file system as external, restorable memory; keep a `todo.md` recitation; keep errors in context; vary few-shot patterns.
- **Claude Code design mirrors these rules** [P] — [Claude Code docs: prompt caching](https://code.claude.com/docs/en/prompt-caching); [claude-api skill: agent design](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence):
  - Plan mode and skill loading append instructions as messages so the cached prefix stays intact.
  - Tool search appends schemas rather than swapping them.
  - Operators should use mid-conversation system messages instead of editing the top-level system prompt.
  - To change models, spawn a subagent rather than switching the main loop's model.

#### 2.2 Batch and flex APIs
- **Anthropic Batch:** 50% off "every token… including cached ones"; results within 24 h; single-shot, with no mid-batch tool loop. Flattening a tool loop into a batchable request is possible, but it "changes how the model reasons". It is "the second-largest free lever after caching" for unattended work [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence); [anthropic.com/pricing](https://www.anthropic.com/pricing)
- **OpenAI Flex:** "the same 50% token discount as Batch" via `service_tier="flex"`. In a 10,000-request head-to-head, Flex with extended caching and `prompt_cache_key` gave an 8.5% higher cache hit rate and 23% lower input cost than Batch. Batch lacks caching parity for pre-GPT-5 models [P] — [Prompt Caching 201](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/Prompt_Caching_201.ipynb)
- **Codex CLI config:** `service_tier` accepts "`default`, `priority`, or `flex`; legacy `fast` also works" [P-code] — [codex config.schema.json](https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json)
- **Grok CLI:** `grok --prompt "…" --batch-api` "uses xAI's Batch API for lower-cost unattended runs… where a delayed result is fine" [P] — [superagent-ai/grok-cli README](https://raw.githubusercontent.com/superagent-ai/grok-cli/main/README.md) (fetched 2026-09-25)

#### 2.3 Subscription quotas vs API billing
- **Anthropic plans (fetched 2026-09-25):** Pro $17/month annually ($20 monthly); Max "from $100" with a choice of 5× or 20× Pro usage. Fable on Max 5x/20x: "50% of weekly limits"; on Pro: "Usage credits" [P] — [anthropic.com/pricing](https://www.anthropic.com/pricing)
- **Opus 5.5 launch (2026-09-22):** "increasing five-hour usage limits on Pro, Max, Team, and seat-based Enterprise plans" and "a rate limit reset, which you can now save and use whenever you choose" [P] — [Introducing Claude Opus 5.5](https://www.anthropic.com/news/claude-opus-5-5)
- **Claude Code subscription mechanics** [P] — [Claude Code docs: costs](https://code.claude.com/docs/en/costs); [Claude Code docs: model config](https://code.claude.com/docs/en/model-config); [Claude Code docs: fast mode](https://code.claude.com/docs/en/fast-mode):
  - The "session limit" and "weekly limit" are seat-based windows "shared across all models", so switching models does not restore access.
  - Fable can bill to usage credits depending on plan. In `-p` and Agent SDK runs, "Claude Code never shows the consent prompt… it bills it without asking".
  - Fast mode (Opus 5.5 up to 2.5× faster, $8/$40) is usage-credits-only on subscriptions.
  - Automatic fallback model chains do **not** trigger on rate-limit errors.
- **API benchmark cost:** "the average cost is around $13 per developer per active day and $150–250 per developer per month, with costs remaining below $30 per active day for 90% of users" (enterprise deployments). Background usage is under $0.04 per session [P] — [Claude Code docs: costs](https://code.claude.com/docs/en/costs)
- **Heavy-use scale reference:** a 16-agent team built a C compiler over about 2,000 Claude Code sessions in two weeks: 2 B input + 140 M output tokens, "just under $20,000" at API rates, "extremely expensive" compared with even the top Max plan [P] — [Building a C compiler with a team of parallel Claudes (Nicholas Carlini, 2026-02-05)](https://www.anthropic.com/engineering/building-c-compiler)
- **Codex plugin note:** "if you do not pass `--model` or `--effort`, Codex chooses its own defaults" [P] — [openai/codex-plugin-cc README](https://raw.githubusercontent.com/openai/codex-plugin-cc/main/README.md)
- [R] Codex is included in ChatGPT plans with usage measured in 5-hour windows plus weekly caps, and extra credits can be bought; exact per-plan numbers changed repeatedly through 2025–2026 — [developers.openai.com/codex/pricing](https://developers.openai.com/codex/pricing) (not fetched)

#### 2.4 Model routing (cheap scouts, strong planners, cost per solved task)
- **Anthropic measured cost per solved task (Aug–Sep 2026)** [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence):
  - SWE-bench Pro subset (478 problems): Opus 5.5 at default (`medium`) 92.8% at $0.22/solved vs Fable 5.1 at default 92.3% at $1.19; Opus 5.5 at `low` 87.4% at $0.12. Fable 5.1 at `low` 88.6% at $0.54 vs Sonnet 5 default 77.4% at $0.84.
  - Internal coding benchmark: Opus 5.5 86.6% vs Fable 5.1 medium 84.2%, at under a third of the cost per attempt ($0.84 vs $2.68).
  - Haiku 4.5 costs about a fifth of Opus 5.5 per GPQA question, with 63% vs 92% accuracy. It "fits high-volume work with checkable outputs, not long agentic loops".
  - Terminal-Bench 3 upgrade ladder: Opus 4.7 → 4.8 → 5 spent $8–15 per task but solved 7/15/41%, i.e., $183 → $63 → $28 per solved task.
  - The same text is about 30% more tokens on Opus 4.7+ (tokenizer), so per-token comparisons mislead.
  - "Price the tail": 2 of 20 WideSearch problems carried 43% of spend.
- **Vendor launch claims:** Haiku 4.5 (2025-10-15) gives "similar levels of coding performance [to Sonnet 4] but at one-third the cost and more than twice the speed" [P] — [Introducing Claude Haiku 4.5](https://www.anthropic.com/news/claude-haiku-4-5). Opus 5.5 "costs 40% less to run than Opus 5" at default settings [P] — [Introducing Claude Opus 5.5](https://www.anthropic.com/news/claude-opus-5-5)
- **Multi-model strategies, measured (2026)** [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence):
  - **Advisor** (cheap executor consults a strong model):
    - Opus 5.5 at `high` with a Fable 5.1 advisor scored 90.1% at $2.92 per attempt: +1.7 points over Opus 5.5 alone at `high` ("edge of run-to-run noise") for about 2.1× the money. Opus 5.5 alone at `xhigh` scored 91.1% at $4.11.
    - The consult rate is "the fragile variable". A low-effort Opus 5.5 executor consulted on 1 of 300 Chartography tasks and scored 7 points below Opus 5.5 alone.
  - **Orchestrator:**
    - Paid on an easy BrowseComp slice: a Fable 5 coordinator plus a Sonnet 5 worker cost about half on average and a third at p90 ($12 vs $33). The solo model's most expensive run ($84) was also wrong.
    - Paid on a 21.6 M-token corpus: −47–55% cost, −10–12 points, 2.3 h vs 15–20 h.
    - Lost on the full, harder BrowseComp: Fable 5 alone matched it at 22–30% lower cost.
    - On DeepWideSearch, lowering effort matched an orchestrator with a Sonnet 5 worker at 29% lower cost.
  - An external study is cited for direction only: Kim et al., "Towards a Science of Scaling Agent Systems", arXiv:2512.08296.
- **Claude Code routing features** [P] — [Claude Code docs: model config](https://code.claude.com/docs/en/model-config); [Claude Code docs: advisor](https://code.claude.com/docs/en/advisor); [Claude Code docs: subagents](https://code.claude.com/docs/en/sub-agents):
  - `opusplan` (Opus in plan mode, Sonnet for execution; each toggle is a cache-invalidating model switch).
  - Advisor tool (experimental; seen from v2.1.117, 2026-04-21): `/advisor opus`, with pairing rules (e.g., an Opus 5.5 executor requires a Fable or Opus 5+ advisor). Claude Code warns it "may use more tokens".
  - Per-subagent `model:` and `effort:`.
- **Codex routing features** [P-code] — [codex config.schema.json](https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json); [codex-plugin-cc README](https://raw.githubusercontent.com/openai/codex-plugin-cc/main/README.md):
  - `agents.default_subagent_model`, `agents.default_subagent_reasoning_effort`, `review_model` ("Review model override used by /review"), `plan_mode_reasoning_effort`.
  - Feature flags `step_model_switching` and `fast_mode`.
  - The Claude Code plugin supports `/codex:rescue --model gpt-5.4-mini --effort medium` and `--model spark`, which maps to `gpt-5.3-codex-spark`.
- **OpenAI tiering guidance (cookbook, 2026-09-14; simulation, not measurement):** nano for classification/tags, mini for routine resolution, full model for high-risk. GPT-5.4 prices: $2.50/$0.25 cached/$15; mini $0.75/$0.075/$4.50; nano $0.20/$0.02/$1.25. GPT-5.6 Luna/Terra/Sol map to the nano/mini/full tiers. "Measure task efficiency, not just token efficiency": blended cost per verified resolution must include failed attempts [P] — [OpenAI cookbook: Optimizing agents for cost and quality](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/agent_optimization/optimizing_agents_for_cost_and_quality.ipynb)
- **Background (older than 2025):** Aider's Architect/Editor split (o1-preview architect + DeepSeek/o1-mini editor) set an 85% SOTA on Aider's editing benchmark, dated 2024-09-26 [P] — [Aider blog post source](https://raw.githubusercontent.com/Aider-AI/aider/main/aider/website/_posts/2024-09-26-architect.md)
- [R] xAI grok-code-fast-1 (2025-08-28) was priced at about $0.20/M input, $1.50/M output and $0.02/M cached input — [x.ai news](https://x.ai/news/grok-code-fast-1) (not fetched). The Grok CLI README suggests `grok-4.20-non-reasoning` "for non-reasoning workloads" [P] — [grok-cli README](https://raw.githubusercontent.com/superagent-ai/grok-cli/main/README.md)

#### 2.5 Reasoning effort / thinking budgets
- **Anthropic effort curves (measured Aug–Sep 2026)** [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence):
  - **Research and knowledge work** (Fable 5; WideSearch, DeepWideSearch, BrowseComp, GDPval): `low` gave up 1–3 points for a third to a half off; `medium` matched the default at about 70–87% of its cost; "the default bought nothing measurable over `medium`". `low` also ran faster: 4.5 vs 7.9 minutes per problem on DeepWideSearch.
  - **Long-horizon coding** (SWE-bench Pro, Opus 5.5 vs `high`): `medium` −2.5 points at about 70% of the cost; `low` −8 points at about a third; `xhigh` +1.4 points at 2.5× the cost of `high`.
  - **DeepResearch Bench II:** Fable 5.1 scored "nearly the same at low, medium, and high" while cost rose from $4.66 to $7.12.
  - **Re-run failures at higher effort:** about 97% at about $0.17 vs 95.3% at $0.29 all-`high`; starting at `medium` gave about 97% at about $0.24. "Use this policy for the saving, not the lift."
- **Opus 4.5 launch (2025-11-24):** "Set to a medium effort level, Opus 4.5 matches Sonnet 4.5's best score on SWE-bench Verified, but uses 76% fewer output tokens. At its highest effort level, Opus 4.5 exceeds Sonnet 4.5 performance by 4.3 percentage points—while using 48% fewer tokens" (vendor benchmark) [P] — [Introducing Claude Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5)
- **Claude Code effort levels and defaults (Sept 2026)** [P] — [Claude Code docs: model config](https://code.claude.com/docs/en/model-config); [Claude Code docs: costs](https://code.claude.com/docs/en/costs); [Claude Code docs: env vars](https://code.claude.com/docs/en/env-vars):
  - Fable 5.1/5 and Opus 5.5/5/4.8/4.7 support `low`–`max`, including `xhigh`.
  - Opus 5.5 defaults to `medium`, Opus 4.7 to `xhigh`, other models to `high`.
  - Thinking "can't [be turned] off on Opus 5.5 or the Fable models".
  - `MAX_THINKING_TOKENS` is ignored by adaptive-reasoning models; use effort instead.
  - Set per session with `/effort`, `--effort` or `CLAUDE_CODE_EFFORT_LEVEL`; per subagent with the `effort:` frontmatter.
- **History of the Claude Code default effort:** on 2026-03-04 Anthropic changed the default from high to medium to cut latency and usage. Users reported it "felt less intelligent", and it was reverted on 2026-04-07 ("This was the wrong tradeoff"). Internal evals had shown medium to be "slightly lower intelligence with significantly less latency" [P] — [Claude Code quality postmortem (2026-04-23)](https://www.anthropic.com/engineering/april-23-postmortem)
- **Codex effort guidance** [P] — [Codex Prompting Guide (updated 2026-02-25)](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/gpt-5/codex_prompting_guide.ipynb); [OpenAI cookbook: cost & quality](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/agent_optimization/optimizing_agents_for_cost_and_quality.ipynb):
  - "We recommend 'medium' reasoning effort as a good all-around interactive coding model that balances intelligence and speed… use high or xhigh reasoning effort for your hardest tasks."
  - "For each comparison, begin with the existing reasoning-effort setting and also evaluate one level lower."
  - `model_reasoning_effort` accepts values "advertised by the model", and there is a separate `plan_mode_reasoning_effort` [P-code] — [codex config.schema.json](https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json)
- **Task budgets** (Anthropic API beta `task-budgets-2026-03-13`; the model sees a token countdown). On SWE-bench Pro with Fable 5.1, a generous budget cut cost per task 44% for about −3 points; the tightest cut 58% for −6 points [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)
- **`max_tokens` caps do not save money per solved task.** A 16,384-token cap ended about a quarter of Opus 5.5 attempts and 43% of Fable 5.1 attempts, and cost per solved task stayed about the same as at 64K [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)
- [R] GPT-5-Codex (2025-09-15): in the bottom 10% of turns it used 93.7% fewer tokens than GPT-5, and in the top 10% it thought twice as long — [openai.com](https://openai.com/index/introducing-upgrades-to-codex/) (not fetched). [R] GPT-5.1-Codex-Max (2025-11-19): compaction-native; at `medium` it beat GPT-5.1-Codex with about 30% fewer thinking tokens; introduced `xhigh` — [openai.com](https://openai.com/index/gpt-5-1-codex-max/) (not fetched)

### Inferences
- **Orchestrator cache hygiene is the top free win.** For Fable (cache read $0.25 vs $10 input, i.e., a 40× gap), every uncached re-read of a 300K-token orchestrator context costs about 40× a cached one. The pipeline design (Fable waits while workers run) creates exactly the "person waits between turns" pattern:
  - Keep the main-conversation 1h TTL. If Fable bills to usage credits, set `promptCacheTtl: 1h`, because the TTL drops to 5 minutes on credits.
  - Consider keep-alive pings if waits regularly exceed an hour.
  - Anthropic found keep-alive cheaper than the 1h TTL on Fable 5.1.
- **Worktree parallelism has a hidden cache cost.** Parallel Claude sessions in separate worktrees do not share caches. Codex workers in worktrees likely also start cold, since the environment context differs (my inference from the Codex prefix design).
- **Build the effort ladder into acceptance.** The baseline already says "no ultrathink/xhigh by default" and leaves Codex `--effort` at the runtime default. The measured "low first + re-run failures higher" policy fits the verifier-gated ladder almost exactly. Suggested mapping:
  - attempt 1 at `low`/`medium`;
  - rework in the same thread at `medium`;
  - fresh executor at `high`/`xhigh`.
  - The verifier's DoD check is the failure signal the policy needs.
- **Route Claude-side helpers to Opus 5.5.** Given the founder's ban on Sonnet and Haiku, the only Claude-side cheaper tier is Opus 5.5, whose default already matches Fable 5.1 on coding at about a fifth of the cost. Every helper subagent (forwarders, summarizers) should run on Opus 5.5, not inherit Fable.
- **Batch fits only offline steps:** the weekly incident-journal retro, bulk re-labelling of journal entries, and LLM judges over accumulated transcripts. Grok CLI `--batch-api` and OpenAI Flex fit unattended scouting that can wait.
- **Subscriptions subsidize interactive heavy loops:** 1h cache and flat price, but hard 5-hour and weekly walls. The "agents dying at session limits" incident class is structural. Because fallback chains don't fire on rate limits, the orchestrator itself needs a cross-vendor fallback (e.g., hand the rework to Codex or pause the queue) plus checkpointed progress.

### Gaps
- How Claude subscriptions count cached versus uncached tokens against 5-hour and weekly limits is undocumented in the sources I could reach. The same applies to how ChatGPT/Codex plans count cached tokens.
- GPT-5.5-specific effort/cost curves for Codex were not found; the Codex guide is model-family-level. Current Codex plan quotas could not be verified (openai.com blocked).
- The Manus numbers are [R]; the manus.im URL could not be fetched.
- [R-lead] Thariq (Anthropic), "Lessons from building Claude Code: prompt caching is everything" (X post, 2026): mentions Claude Code treating cache-hit-rate drops as incidents. No verifiable URL.

---

## Q3 — Tool efficiency

### Takeaway
The measured tool levers are:
- **Deferred tool loading:** −85% definition tokens; cost flat instead of doubling at 502 tools.
- **Programmatic tool calling:** −24% to −37% tokens.
- **Keeping data out of the prompt via code execution:** 12× cheaper and 25/25 correct instead of 6/25.
- **Capping and filtering tool outputs:** about 10k tokens with head+tail truncation; hook-filtered test output.

Semantic/LSP navigation has only vendor-run evidence (Claude Context −39% tokens at equal F1, with a weak model). Anthropic reports that plain agentic search (glob/grep/rg) is what Claude Code relies on.

Turning repeated multi-step procedures into scripts, hooks, skills or saved workflows is strongly endorsed by Anthropic and OpenAI. Its savings are illustrated rather than benchmarked, except the data-file and hook examples.

### Cited Findings

#### 3.1 Code execution with MCP / "Code Mode"
- **Anthropic (2025-11-04):**
  - Agents discover tools as files (`./servers/…`) and write code that calls them, so intermediate results stay in the execution environment.
  - Illustrative example: "reduces the token usage from 150,000 tokens to 2,000 tokens—a time and cost saving of 98.7%". A 2-hour meeting transcript flowing through context twice "could mean processing an additional 50,000 tokens".
  - "Cloudflare published similar findings, referring to code execution with MCP as 'Code Mode'" [P] — [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- **Cloudflare `@cloudflare/codemode`** (npm since 2025-12-29, experimental): "LLMs are better at writing code than calling tools". It generates TypeScript types from tools and executes the code in isolated sandboxes [P] — [cloudflare/agents codemode README](https://raw.githubusercontent.com/cloudflare/agents/main/packages/codemode/README.md); [npm](https://registry.npmjs.org/@cloudflare/codemode). [R] Original blog 2025-09-26 — [blog.cloudflare.com/code-mode](https://blog.cloudflare.com/code-mode/)
- **Codex** has `code_mode` feature flags and a `ToolExposureSurface` enum (`code_mode` / `deferred` / `direct`) [P-code] — [codex config.schema.json](https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json)
- **Data out of the prompt (measured 2026).** 25 aggregate questions over a 1,862-row CSV:
  - pasted into the prompt: about 91,000 input tokens per request, 6/25 correct at $5.01;
  - uploaded via the Files API and queried with code execution: 25/25 correct at $0.40 (about 1/12 of the cost).
  - Model: Sonnet 5; Opus 5 showed the same pattern [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)

#### 3.2 Tool Search / deferred tool loading
- **Anthropic (2025-11-24):**
  - A five-server MCP setup has 58 tools and about 55K tokens of definitions; Anthropic saw 134K before optimizing.
  - With Tool Search Tool, about 8.7K instead of about 77K tokens: "an 85% reduction". MCP-eval accuracy: Opus 4 49%→74%, Opus 4.5 79.5%→88.1%.
  - "doesn't break prompt caching". Use it when tool definitions exceed 10K tokens; keep the 3–5 most-used tools loaded [P] — [Introducing advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)
- **API docs:** "selection accuracy… degrades once you exceed 30–50 available tools". The tool types are `tool_search_tool_regex_20251119` and `tool_search_tool_bm25_20251119` [P] — [Anthropic docs: tool search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)
- **Measured cost (2026):** with all tools loaded, run cost rose from $0.55 to $1.02 at 502 tools; with tool search it stayed at $0.56 (−45%). Accuracy was 15–18/20 either way. Deferring a GitHub MCP server's toolset cut the run 20% at equal accuracy [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)
- **Claude Code:**
  - MCP tool search auto mode became the default in v2.1.7 (2026-01-13): defer when descriptions exceed 10% of the context window.
  - Current docs: "MCP tool definitions are deferred by default". `ENABLE_TOOL_SEARCH=auto` loads them upfront if they fit within 10%; `false` loads everything [P] — [Claude Code CHANGELOG v2.1.7](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md); [Claude Code docs: costs](https://code.claude.com/docs/en/costs); [Claude Code docs: env vars](https://code.claude.com/docs/en/env-vars)
- **Codex** has `tool_search` and `tool_search_always_defer_mcp_tools` feature flags [P-code] — [codex config.schema.json](https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json)

#### 3.3 Programmatic tool calling (PTC)
- **Anthropic (2025-11-24):** Claude writes orchestration code, and only final results enter context. "Average usage dropped from 43,588 to 27,297 tokens, a 37% reduction on complex research tasks". Knowledge retrieval improved 25.6%→28.5% and GIA 46.5%→51.2%. The expense example went from 200 KB of raw data to 1 KB of results. Tool Use Examples improved complex-parameter accuracy 72%→90% [P] — [Introducing advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)
- **Later documentation figure:** "24% fewer input tokens on agentic search benchmarks, with a higher score". Mechanics: `code_execution_20260120` plus `allowed_callers`; not compatible with MCP tools or forced `tool_choice` [P] — [claude-api skill cost reference](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence); [Anthropic docs: PTC](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling). *The two sources differ (37% vs 24%); benchmark sets differ.*

#### 3.4 Trimming tool outputs
- **Anthropic tools guidance (2025-09-11):**
  - "For Claude Code, we restrict tool responses to 25,000 tokens by default."
  - A `response_format` enum (`concise` vs `detailed`): 72 vs 206 tokens, about ⅓.
  - Add pagination, filtering and truncation with steering messages [P] — [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- **Claude Code limits** [P] — [Claude Code docs: env vars](https://code.claude.com/docs/en/env-vars); [Claude Code docs: costs](https://code.claude.com/docs/en/costs):
  - `MAX_MCP_OUTPUT_TOKENS` default 25,000, with a warning above 10,000. `BASH_MAX_OUTPUT_LENGTH` default 30,000 characters (maximum 150,000).
  - A PreToolUse hook can rewrite commands; hooks can modify tool inputs since v2.0.10 (2025-10-07). The docs' example rewrites test commands to show only failures.
  - "Instead of Claude reading a 10,000-line log file… a hook can grep for ERROR… reducing context from tens of thousands of tokens to hundreds" (illustrative).
- **OpenAI guidance for Codex-style harnesses:** "Limit [tool responses] to 10k tokens… approximate this by computing num_bytes/4… use half of the budget for the beginning, half for the end, and truncate in the middle" [P] — [Codex Prompting Guide](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/gpt-5/codex_prompting_guide.ipynb). Codex config: `tool_output_token_limit` and a per-MCP-tool `output_token_limit` ("before the standard 20% serialization allowance") [P-code] — [codex config.schema.json](https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json)
- **RTK (Rust Token Killer)** [P] — [rtk-ai/rtk README](https://raw.githubusercontent.com/rtk-ai/rtk/master/README.md) (date not established):
  - A CLI proxy that "cuts up to 90% of the bash output your agent reads", with the honest caveat that this "is not the same as cutting your bill by 90%". Token counts are estimated as bytes/4.
  - Per-command claims: pytest/go test/cargo test −90%; rspec −60%+; cargo build/clippy −80%; ruff −80%; golangci-lint −85%.
  - `rtk init -g --codex` / `--gemini` hooks rewrite Bash commands. Claude Code's built-in Read/Grep/Glob are not rewritten.
- **context-mode** (npm since 2026-02-23; vendor claims) [P] — [mksglu/context-mode README](https://raw.githubusercontent.com/mksglu/context-mode/main/README.md); [npm](https://registry.npmjs.org/context-mode):
  - Sandboxes tool outputs: "315 KB becomes 5.4 KB. 98% reduction"; "47 × Read() = 700 KB… 1 × ctx_execute() = 3.6 KB".
  - Indexes session events in SQLite FTS5 and retrieves them via BM25 after compaction.
- **Output-format measurement (Anthropic 2026):** a one-line final answer used 39% fewer output tokens and cost 14% less per run than a two-line answer. A five-section memo used 6× the output tokens and cost 2.8×. All were within noise on accuracy [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)

#### 3.5 Fast code search (ripgrep, ast-grep) and glob hangs
- **OpenAI's Codex prompt:** "When searching for text or files, prefer using `rg` or `rg --files` respectively because `rg` is much faster than alternatives like `grep`". "Batch everything… Always maximize parallelism. Never read files one-by-one unless logically unavoidable" [P] — [Codex Prompting Guide](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/gpt-5/codex_prompting_guide.ipynb)
- **Claude Code** ships a bundled ripgrep; `USE_BUILTIN_RIPGREP=0` switches to the system `rg`. `CLAUDE_CODE_GLOB_TIMEOUT_SECONDS` defaults to 20 s (60 s on WSL) for "Glob tool file discovery" [P] — [Claude Code docs: troubleshooting](https://code.claude.com/docs/en/troubleshooting); [Claude Code docs: env vars](https://code.claude.com/docs/en/env-vars)
- **Claude Code's search design:** "CLAUDE.md files are naively dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time, effectively bypassing the issues of stale indexing and complex syntax trees" [P] — [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- **ast-grep** is "a CLI tool for code structural search, lint, and rewriting" (AST patterns, YAML rules). No token claims [P] — [ast-grep README](https://raw.githubusercontent.com/ast-grep/ast-grep/main/README.md)
- **Grok CLI:** the headless flags `--max-tool-rounds` (e.g., 30) and `--format json` NDJSON events (`step_start`, `text`, `tool_use`, `step_finish`, `error`) exist. Troubleshooting: "Reduce `--max-tool-rounds` for headless runs"; "Long-running sessions accumulate context; start a fresh session periodically". No glob timeout is documented [P] — [grok-cli README](https://raw.githubusercontent.com/superagent-ai/grok-cli/main/README.md)

#### 3.6 Semantic / LSP navigation (Serena, Claude Context, Claude Code LSP)
- **Claude Context (Zilliz) evaluation** [P] — [claude-context evaluation README](https://raw.githubusercontent.com/zilliztech/claude-context/master/evaluation/README.md); npm since 2025-08-03 — [npm](https://registry.npmjs.org/@zilliz/claude-context-mcp):
  - Setup: 30 SWE-bench Verified instances (15–60-minute problems, exactly 2 files modified), GPT-4o-mini, LangGraph ReAct, each method run 3×.
  - Grep-only vs +Claude Context: F1 0.40 vs 0.40; tokens 73,373 vs 44,449 (−39.4%); tool calls 8.3 vs 5.3 (−36.3%).
  - Retrieval (file localization) only; not end-to-end resolution; vendor-run.
- **Serena (Oraios):** an MCP toolkit with LSP-backed, symbol-level retrieval and editing (find symbol, references, replace symbol body) for 40+ languages. It claims agents operate "faster, more efficiently and more reliably" and that symbolic editing is "much more token-efficient", with no numbers in the README. PyPI releases run from 2025-07-21 to 1.7.0 on 2026-08-09 [P] — [oraios/serena README](https://raw.githubusercontent.com/oraios/serena/main/README.md); [PyPI](https://pypi.org/pypi/serena-agent/json)
- **Claude Code LSP:** the LSP tool arrived in v2.0.74 (2025-12-19). Current "code intelligence plugins" give Claude diagnostics after each edit ("sees a type error… without running a compiler") and symbol navigation "instead of by text search". No savings figure is given [P] — [Claude Code CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md); [Claude Code docs: code intelligence](https://code.claude.com/docs/en/plugins/code-intelligence)
- **OpenAI on adding a semantic tool to Codex:** name it unambiguously (`semantic_search`) and make its results "look different from outputs the model is accustomed to seeing… ripgrep results should look different from semantic search results to avoid the model collapsing into old habits" [P] — [Codex Prompting Guide](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/gpt-5/codex_prompting_guide.ipynb)
- [R] Cursor (2025-11) reported semantic search improving agent answer accuracy by about 12.5% on average (6.5–23.5% by model) and small online gains in code retention — [cursor.com/blog/semsearch](https://cursor.com/blog/semsearch) (not fetched)

#### 3.7 Repo maps (Aider)
- **Aider:** "a concise map of your whole git repository" with key symbols and signatures, selected by "a graph ranking algorithm" to "fit into the active token budget"; `--map-tokens` "defaults to 1k tokens"; `--map-refresh auto|always|files|manual` [P] — [Aider docs: repomap](https://raw.githubusercontent.com/Aider-AI/aider/main/aider/website/docs/repomap.md); [Aider options](https://raw.githubusercontent.com/Aider-AI/aider/main/aider/website/docs/config/options.md). No 2025–2026 token-savings benchmark was found.

#### 3.8 Turning repeated procedures into deterministic scripts, skills and workflows
- **Anthropic Skills:** code "can serve as both executable tools and as documentation"; deterministic scripts are cheaper and "consistent and repeatable" [P] — [Agent Skills (2025-10-16)](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- **Claude Code "dynamic workflows"** [P] — [Claude Code docs: workflows](https://code.claude.com/docs/en/workflows):
  - "A workflow moves the plan into code… A workflow script holds the loop, the branching, and the intermediate results itself, so Claude's context holds only the final answer."
  - Runs can be saved as reusable commands, shipped in plugins and parameterized via `args`.
  - With `ultracode` on, "each request uses more tokens and takes longer".
- **Claude Code costs doc:** "Offload processing to hooks and skills". A "codebase-overview" skill gives Claude context "immediately instead of spending tokens reading multiple files" [P] — [Claude Code docs: costs](https://code.claude.com/docs/en/costs)
- **Harness posts:** an `init.sh` that starts the dev server and runs a smoke test "saves Claude some tokens in every session" [P] — [Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- **Bash vs dedicated tools:** "Start with bash for breadth. Promote to dedicated tools when you need to gate, render, audit, or parallelize the action" [P] — claude-api skill `agent-design.md` (bundled with Claude Code 2.1.282; see [Anthropic docs](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence))
- **OpenAI:** use skills (`$skill-creator`) to make a long manual harness process "reusable and more consistent" [P] — [Iterating Development Workflows with Codex](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/codex/iterating-development-workflows-with-codex.md)

### Inferences
- **The Grok 10-minute glob hangs** are the same failure class Claude Code guards with a 20-second Glob timeout. The baseline's current fix (only absolute paths, no filesystem search) is right but lossy. Cheaper alternatives:
  - (a) A deterministic pre-step writes a repo map or symbol index (`rg --files`, ctags, ast-grep or Aider's repomap) to a file, and the scout gets its path.
  - (b) If scouts must search, allow only `rg --files -g '<pattern>' <abs-root>` with ignore files, wrapped in `timeout`.
  - (c) Consider Serena or an LSP MCP for symbol queries. Its evidence is qualitative.
- **Tool-output trimming applies directly to Codex executors and verifiers**, which run tests: `tool_output_token_limit`, RTK with `rtk init --codex`, or project scripts like `make test-quiet` that print only failures. The benefit compounds because every earlier tool output is re-sent (cached) on every later turn.
- **Tool Search, code mode and PTC** matter only if forwarder or worker sessions load MCP servers (e.g., GitHub MCP). Claude Code already defers them by default. For Codex, check whether `tool_search` is on in the installed version.
- **Largest script-conversion opportunity:** the baseline repeats a fixed "procedure" per issue: edit body, set status, post journal comments at each phase, label transitions, close with SHA. These are pure templating plus `gh` CLI calls and should be a script (e.g., `pipeline.sh dispatch|report|verify|rework|close N`). An LLM should not do them.

### Gaps
- No independent (non-vendor) benchmark was found for Serena, Claude Context or RTK-style trimming on end-to-end coding success with 2026 models.
- No measurement of how often Codex/Grok re-run commands after their outputs are truncated (the net effect of trimming).
- The Cloudflare Code Mode headline numbers and the Cursor semantic-search results are [R].

---

## Q4 — Orchestration level

### Takeaway
At the orchestration level, the measured and documented winners are:
- pass pointers or paths plus lightweight references (not content);
- give workers detailed, bounded task descriptions (objective, output format, tools, boundaries) to prevent duplicated exploration;
- write self-contained, falsifiable specs;
- time-box and budget every worker (clock plus hard limits);
- verify deterministically first.

Parallelism in git worktrees buys wall time for independent work at the price of more tokens and no cross-worktree cache sharing. Multi-agent structure should be reserved for fan-out work. The evaluator/verifier is cheap relative to the build (about 8% of spend in Anthropic's harness run), but only when it is tuned to be skeptical and backed by a real failure signal.

### Cited Findings

#### 4.1 Passing pointers/paths instead of content
- **Anthropic multi-agent:** "Subagent output to a filesystem to minimize the 'game of telephone'… Subagents call tools to store their work in external systems, then pass lightweight references back to the coordinator" [P] — [Multi-agent research system (2025-06-13)](https://www.anthropic.com/engineering/multi-agent-research-system)
- **Context engineering:** use "just in time" retrieval via "lightweight identifiers (file paths, stored queries, web links)" [P] — [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- **Claude Code headless:** "Piped stdin is capped at 10MB… write the content to a file and reference the file path in your prompt instead" [P] — [Claude Code docs: headless](https://code.claude.com/docs/en/headless)
- **Codex prompt guidance:** "Don't dump large files you've written; reference paths only" [P] — [Codex Prompting Guide](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/gpt-5/codex_prompting_guide.ipynb)
- [R] Manus: "use the file system as context" with "restorable" compression (keep the URL or path, drop the content) — [Manus blog](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)

#### 4.2 Avoiding duplicate exploration between orchestrator and workers
- **Anthropic multi-agent:**
  - "Each subagent needs an objective, an output format, guidance on the tools and sources to use, and clear task boundaries. Without detailed task descriptions, agents duplicate work, leave gaps, or fail to find necessary information."
  - Effort-scaling rules: simple fact-finding uses 1 agent and 3–10 tool calls; comparisons use 2–4 subagents with 10–15 calls each; complex research uses 10+ subagents [P] — [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- **Claude Code costs doc:** "Vague requests like 'improve this codebase' trigger broad scanning. Specific requests like 'add input validation to the login function in auth.ts' let Claude work efficiently with minimal file reads" [P] — [Claude Code docs: costs](https://code.claude.com/docs/en/costs)
- **C compiler team:** tasks are claimed via lock files in `current_tasks/`, and git forces a second claimant to pick another task. Specialized agents handled coalescing duplicate code, performance and design critique [P] — [Building a C compiler (2026-02-05)](https://www.anthropic.com/engineering/building-c-compiler)

#### 4.3 Spec quality to reduce rework
- **Claude Code best practices:** "The most useful specs are self-contained: they name the files and interfaces involved, state what is out of scope, and end with an end-to-end verification step… Time spent making the spec precise pays off more than time spent watching the implementation." Also: "start a fresh session to execute it" [P] — [Claude Code docs: best practices](https://code.claude.com/docs/en/best-practices)
- **Claude Code costs doc:** plan mode is for "preventing expensive re-work when the initial direction is wrong"; "Give verification targets"; "Test incrementally" [P] — [Claude Code docs: costs](https://code.claude.com/docs/en/costs)
- **Harness design (2026-03-24):**
  - Without the planner, "the generator under-scoped".
  - Generator and evaluator negotiated a sprint contract ("what 'done' looked like… before any code was written"); "Sprint 3 alone had 27 criteria". Findings were "specific enough to act on without extra investigation".
  - Solo run: 20 min, $9. Full harness: 6 h, $200, with a much richer product [P] — [Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- **Codex guide:** "remove all prompting for the model to communicate an upfront plan, preambles, or other status updates during the rollout, as this can cause the model to stop abruptly before the rollout is complete" (for pre-gpt-5.3-codex models; later models' updates are more communicative) [P] — [Codex Prompting Guide](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/gpt-5/codex_prompting_guide.ipynb)
- **Fable-specific guidance in Claude Code docs:** "Describe the outcome, not the steps… Skip the verification reminders: it verifies its own work with less prompting… Size up larger tasks" [P] — [Claude Code docs: model config](https://code.claude.com/docs/en/model-config). The claude-api reference adds that prompts written for prior models are often too prescriptive for Fable 5.1 and "reduce output quality" [P] — claude-api skill (bundled, Claude Code 2.1.282)
- **Prompt audit:** stale instructions cost +36% per ticket; removing "verify twice" saved a third of the cost [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence) (details in 1.5)
- **ExecPlans:** self-contained living specs (Codex worked 7+ hours from one prompt; anecdote) [P] — [OpenAI cookbook ExecPlans](https://raw.githubusercontent.com/openai/openai-cookbook/main/articles/codex_exec_plans.md)

#### 4.4 Parallelism with git worktrees
- **Claude Code worktrees** [P] — [Claude Code docs: worktrees](https://code.claude.com/docs/en/worktrees); [Claude Code CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md); [Claude Code docs: prompt caching](https://code.claude.com/docs/en/prompt-caching):
  - The `--worktree`/`-w` flag arrived in v2.1.49 (2026-02-19). `isolation: worktree` works for subagents and forks.
  - "A worktree is a fresh checkout, so initialize your development environment there". `.worktreeinclude` copies gitignored files such as `.env`.
  - Unchanged subagent worktrees are auto-removed. `-p` runs leave worktrees locked until a sweep.
  - Worktrees have separate prompt caches.
- **Measured speedups:**
  - Parallel subagents (3–5) plus parallel tool calls "cut research time by up to 90% for complex queries" [P] — [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
  - 25 concurrent workers: an episode took 2.3 h vs 15–20 h solo on the 21.6 M-token corpus [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)
  - A same-model team on DRACO cost 4.0× a single agent and took "about as long" without the clock [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)
- **Operational lessons:** "Merge conflicts are frequent, but Claude is smart enough to figure that out". Parallelism works best when there are "many distinct failing tests". A GCC oracle turned one giant failing target (the Linux kernel) into parallelizable pieces [P] — [Building a C compiler](https://www.anthropic.com/engineering/building-c-compiler)
- **Resource headroom matters:** on Terminal-Bench 2.0, infra errors fell from 5.8% (strict 1× resources) to 0.5% (uncapped), and success rose +6 percentage points (p < 0.01). "Tight limits inadvertently reward very efficient strategies" [P] — [Quantifying infrastructure noise in agentic coding evals (Gian Segato, 2026-02-05)](https://www.anthropic.com/engineering/infrastructure-noise)
- **Codex parallel controls:** `agents.max_concurrent_threads_per_session`, a `worktrees` feature flag, and `multi_agent_v2` [P-code] — [codex config.schema.json](https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json)

#### 4.5 Time boxes and watchdogs for hung workers
- **Elapsed-time clock** (measured, Fable 5.1 at `high`) [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence):
  - Method: add the instruction "Time matters here: do not spend time that can be avoided, and the earlier a correct result is obtained, the better. The elapsed time so far is shown before each of your turns", then send `Elapsed time: N seconds` as a mid-conversation system message before each later turn.
  - **Teams:**
    - DRACO: −33% time, −54% cost, −1.5 points.
    - HLE: −51% time, −54% cost, −1.7 points.
    - Physics set: −39% time, −28% cost, +0.2 points.
  - **Single agent:**
    - DRACO: −69% time, −49% cost, −1.9 points.
    - HLE: −54% time, −48% cost, −1.1 points.
    - Physics set: −34% time, −34% cost, −0.2 points.
  - For a single agent, "the clock saves more time than a lower effort level does". Some scores fell beyond pre-registered margins.
- **Time blindness (C compiler):** "Claude can't tell time and, left alone, will happily spend hours running tests instead of making progress". The harness "prints incremental progress infrequently (to avoid polluting context)" and has a default `--fast` option that runs a deterministic 1% or 10% random sample of tests per agent [P] — [Building a C compiler](https://www.anthropic.com/engineering/building-c-compiler)
- **Claude Code hard limits** [P] — [Claude Code docs: env vars](https://code.claude.com/docs/en/env-vars); [Claude Code docs: subagents](https://code.claude.com/docs/en/sub-agents); [Claude Code docs: headless](https://code.claude.com/docs/en/headless); [Claude Code CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md):
  - `BASH_DEFAULT_TIMEOUT_MS` 120 s; `BASH_MAX_TIMEOUT_MS` 600 s; `CLAUDE_CODE_GLOB_TIMEOUT_SECONDS` 20 s; `API_TIMEOUT_MS` 600 s.
  - `MCP_TOOL_TIMEOUT`, plus idle timeouts of 5 min for network servers and 30 min for stdio.
  - Subagent `maxTurns` returns output "marked as partial" that can be resumed.
  - `--max-turns`; `--max-budget-usd` (SDK/CLI since v2.0.28, 2025-10-27; it also halts background subagents).
  - SIGTERM on `claude -p` exits with code 143, and a resumed session continues the unfinished turn.
- **Claude Code `/goal`** (v2.1.139, 2026-05-11): after each turn "a small fast model checks whether the condition holds". The goal clears when met, when "judge[d] impossible", or on errors that need a fix. Idle check-ins are capped at 3 [P] — [Claude Code docs: goal](https://code.claude.com/docs/en/goal); [Claude Code docs: costs](https://code.claude.com/docs/en/costs)
- **Codex:**
  - `background_terminal_max_timeout` defaults to 300,000 ms [P-code] — [codex config.schema.json](https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json)
  - Goals (Codex 0.128.0, 2026-04-30) stop on "success, pause, clear, interruption, budget limit, or a blocker"; the config key is `goals.max_goal_token_budget` [P] — [OpenAI cookbook: Using Goals in Codex (2026-05-09)](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/codex/using_goals_in_codex.ipynb); [npm dates](https://registry.npmjs.org/@openai/codex)
- **Grok CLI:** `--max-tool-rounds N`; the `--format json` NDJSON event stream enables heartbeat monitoring; `--session latest` resumes [P] — [grok-cli README](https://raw.githubusercontent.com/superagent-ai/grok-cli/main/README.md)

#### 4.6 Early stop conditions and budgets
- **Task budgets** (the model sees them) −44% to −58% cost for −3 to −6 points. `max_tokens` is only a safety cap. Managed Agents session budgets are hard dollar stops [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)
- **Stop-sequence sentinels as "content-aware early exits"**, e.g., `<CANNOT_REVIEW>` [P] — claude-api skill cost reference (bundled with Claude Code 2.1.282; same levers as [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence))
- **Tail spend and spirals:** 2 of 20 problems carried 43% of spend. The solo model's most expensive BrowseComp run ($84) "was also wrong". "A frontier model running alone occasionally spirals on a routine problem" [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)
- **Multi-agent lesson:** "Early agents made errors like spawning 50 subagents for simple queries, scouring the web endlessly for nonexistent sources". Effort-scaling rules embedded in prompts "prevent overinvestment in simple queries" [P] — [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- **Restart rule:** "If you've corrected Claude more than twice on the same issue… Run /clear and start fresh" [P] — [Claude Code docs: best practices](https://code.claude.com/docs/en/best-practices)

#### 4.7 Cheaper verifier strategies
- **Graders:**
  - Code-based graders are "Fast", "Cheap", "Objective", "Reproducible", and can analyze transcripts (turns, tokens).
  - Model-based graders are "Non-deterministic", "More expensive than code" and "Require calibration with human graders".
  - "Deterministic graders are natural for coding agents… does the code run and do the tests pass?" [P] — [Demystifying evals for AI agents (2026-01-09)](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- **Evaluator economics in a real harness (DAW build: 4 h, $124)** [P] — [Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps):
  - Costs: planner $0.46; build rounds $71.08, $36.89, $5.88; QA rounds $3.24, $3.09, $4.06, so QA is about 8% of spend.
  - "Out of the box, Claude is a poor QA agent… talk[s] itself into deciding [issues] weren't a big deal". The evaluator had to be tuned to be skeptical, with few-shot calibration.
  - "The evaluator is not a fixed yes-or-no decision. It is worth the cost when the task sits beyond what the current model does reliably solo."
- **Separation of worker and judge:** "a verification subagent or a dynamic workflow… has a fresh model try to refute the result, so the agent doing the work isn't the one grading it". "Have Claude show evidence rather than asserting success" [P] — [Claude Code docs: best practices](https://code.claude.com/docs/en/best-practices)
- **Sampled tests during iteration:** the C compiler's `--fast` 1%/10% deterministic subsample [P] — [Building a C compiler](https://www.anthropic.com/engineering/building-c-compiler)
- **Cheap judge models:** Claude Code's `/goal` uses "a small fast model" to judge completion [P] — [Claude Code docs: goal](https://code.claude.com/docs/en/goal). Codex's `review_model` can route `/review` to a different model [P-code] — [codex config.schema.json](https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json)
- **Failure signal quality gates the savings:** "a checker that passes bad work lets those failures through" [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)

#### 4.8 Head/hands economics (single model vs orchestrator)
- "An orchestrator buys something only when there is bulk to hand off… When the work is one dependent chain, or fits in a single context, the orchestrator pays for a plan, a handoff, and a merge that a single model gets for free" [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)
- **"Decoupling the brain from the hands"** in Anthropic's Managed Agents (provisioning containers only when a tool call needs them) cut p50 TTFT by about 60% and p95 by over 90%. This is an infrastructure latency result, not a token result [P] — [Scaling Managed Agents (2026-04-08)](https://www.anthropic.com/engineering/managed-agents)

### Inferences
- **The baseline already implements the documented best practices:** pointer dispatch (`gh issue view N`), self-contained specs with falsifiable DoD, file-based reports with digests, a separate verifier, and a fresh executor after 2 failures. The remaining waste is in the **plumbing** and in **effort/time control**, not in the architecture.
- **Cross-vendor head/hands is justified by quota arbitrage, not by Anthropic's API cost curves.** Anthropic measured an orchestrator as cheaper only for bulk or tail-heavy work, but its measurement is single-vendor API pricing. The user's split is driven by Fable quota scarcity and separate Codex/Grok subscriptions, which that measurement does not capture.
- **Amortize fixed per-issue costs on small, single-file issues.** The fixed per-issue cost is spec + dispatch + verifier + ~6 journal posts + close. Batching several tiny issues into one executor session with one verifier pass cuts it. This matches the skill's own "укрупнять задачи" rule when limits run low.
- **"Lost reports" hypothesis (verify):** `codex-rescue` makes a single foreground Bash call with `--wait`, while Claude Code's Bash tool defaults to a 2-minute timeout (10-minute max unless raised). Options:
  - raise `BASH_DEFAULT_TIMEOUT_MS` / `BASH_MAX_TIMEOUT_MS` for these sessions;
  - use `--background` plus a deterministic poller;
  - or have the dispatcher script (lever 2) own the wait.
- **Watchdog design for Grok/Orca workers:**
  - Run a wall-clock `timeout` per task class (e.g., 5 min for scouts, 30 min for coding).
  - Add a heartbeat: no NDJSON event or no terminal output change for N s → `terminal read`, then kill.
  - Respawn once with a narrower spec, then escalate to `blocked`.
  - Log `hang_class` (glob/network/test) to the incident journal. This turns the "check --wait timeout ≠ failure" rule into an automatic decision.
- **Cheaper verification per issue:**
  - (1) The script runs the DoD commands and attaches output to the journal.
  - (2) An LLM verifier only for non-command DoD items, at low effort, with the same stable prompt prefix across issues so it hits cache.
  - (3) Sampled tests during reworks; the full suite at acceptance.
  - (4) The final adversarial review stays at pipeline end (already the case).
- **Worktree parallelism** is only worth it for file-disjoint groups with enough independent volume. Pre-provision worktrees (dependencies, `.env` via `.worktreeinclude`), cap concurrency by CPU/RAM (infra-noise evidence), and remember that each extra parallel session spends 5-hour quota faster.

### Gaps
- No public measurement compares LLM verifiers with deterministic DoD execution for per-issue acceptance in coding pipelines (cost and false-accept rate).
- No data on the typical overhead of a Claude Code subagent spawn (tokens and seconds) in 2026 versions beyond illustrative figures.
- The codex-companion's behavior on long `--wait` runs (whether it survives Bash timeouts) was not verified in source.

---

## Q5 — Which savings claims are measured (with methodology) vs anecdotal

### Takeaway
The best-measured 2026 source is Anthropic's live "Optimizing for cost and intelligence" guide. It names benchmarks, run dates, run counts and noise margins, and costs are computed per solved task at list prices. Anthropic's 2025 launch posts and vendor READMEs give internal-eval or illustrative numbers with thin methodology. Several practitioner claims (HumanLayer, ExecPlans, RTK, context-mode) are anecdotes or estimates.

Two important contradictions and caveats:
- Context editing: −84% tokens and +29% performance in Sep 2025, but +74% cost / no savings in Anthropic's own 2026 measurement.
- Effort defaults: medium looked fine on internal evals but was reverted after user feedback.

Infrastructure noise alone can move agentic benchmark scores by up to 6 points, so differences of 1–3 points are within noise.

### Cited Findings
- **Measured, with stated methodology (strongest)** [P] — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence):
  - Caching (2.7–5.3×; production cache-share statistics over 14 days).
  - TTL choice, tool search (502-tool catalog), data files (25 questions with pandas ground truth), context lifecycle (20-issue vs long triage runs), prompt audit (44 tickets, deterministic grading).
  - Model per solved task (SWE-bench Pro 478-problem subset, DeepResearch Bench II, Terminal-Bench 3), effort sweeps, re-run failures, task budgets, max_tokens caps (~14,000 turns), elapsed-time clock (pre-registered margins, 95% intervals), advisor/orchestrator (dated runs, 2–5 runs per configuration).
  - The guide lists benchmark references with run dates (Aug 1 – Sep 20, 2026) and notes that SWE-bench Pro subset "scores are not comparable to the public leaderboard".
- **Measured, vendor-internal, thin methodology** [P]:
  - Multi-agent +90.2%, 15× tokens, 80% variance — [Anthropic (2025-06-13)](https://www.anthropic.com/engineering/multi-agent-research-system)
  - Context editing +29% / +39% / −84% tokens — [Anthropic (2025-09-29)](https://www.anthropic.com/news/context-management)
  - Tool search −85% tokens with accuracy gains; PTC −37% — [Anthropic (2025-11-24)](https://www.anthropic.com/engineering/advanced-tool-use)
  - Opus 4.5 effort −76% / −48% tokens on SWE-bench Verified — [Anthropic (2025-11-24)](https://www.anthropic.com/news/claude-opus-4-5)
  - Haiku 4.5 at one-third cost — [Anthropic (2025-10-15)](https://www.anthropic.com/news/claude-haiku-4-5)
  - Opus 5.5 −40% cost vs Opus 5 "on typical workloads", plus early-tester anecdotes (a 200K-line codebase audited in under 3 h vs over 20 h) — [Anthropic (2026-09-22)](https://www.anthropic.com/news/claude-opus-5-5)
- **Measured, practitioner/vendor study** [P]:
  - OpenAI Prompt Caching 201: TTFT curve from 2,300 runs; Flex vs Batch on 10,000 identical requests (+8.5% hit rate, −23% input cost); the 60%→87% hit rate is one customer's anecdote — [OpenAI cookbook (2026-02-18)](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/Prompt_Caching_201.ipynb)
  - Claude Context: n = 30 SWE-bench instances × 3 runs, GPT-4o-mini, retrieval F1 only — [evaluation README](https://raw.githubusercontent.com/zilliztech/claude-context/master/evaluation/README.md)
- **Simulation or illustration, not measurement** [P]:
  - The OpenAI cost/quality cookbook states its harness is a "deterministic simulation" with "illustrative formulas" — [OpenAI cookbook (2026-09-14)](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/agent_optimization/optimizing_agents_for_cost_and_quality.ipynb)
  - Anthropic's code-execution-with-MCP 150K→2K (98.7%) is a worked example — [Anthropic (2025-11-04)](https://www.anthropic.com/engineering/code-execution-with-mcp)
  - Claude Code docs' hook "tens of thousands → hundreds" example and the context-window simulation (6,100 tokens read → 420 returned) — [Claude Code docs: costs](https://code.claude.com/docs/en/costs); [Claude Code docs: context window](https://code.claude.com/docs/en/context-window)
- **Vendor tool claims (estimates)** [P]:
  - RTK "up to 90% of bash output", estimated as bytes/4 and explicitly "not… your bill" — [RTK README](https://raw.githubusercontent.com/rtk-ai/rtk/master/README.md)
  - context-mode "315 KB → 5.4 KB (98%)" — [context-mode README](https://raw.githubusercontent.com/mksglu/context-mode/main/README.md)
  - Serena "more token-efficient", with no numbers — [Serena README](https://raw.githubusercontent.com/oraios/serena/main/README.md)
- **Anecdotal case studies** [P]:
  - HumanLayer's BAML examples and the "40–60% utilization" rule of thumb — [ACE-FCA](https://raw.githubusercontent.com/humanlayer/advanced-context-engineering-for-coding-agents/main/ace-fca.md)
  - ExecPlans "more than seven hours from a single prompt" — [OpenAI cookbook](https://raw.githubusercontent.com/openai/openai-cookbook/main/articles/codex_exec_plans.md)
  - Harness "Solo 20 min $9 vs harness 6 h $200" (one run each) — [Anthropic (2026-03-24)](https://www.anthropic.com/engineering/harness-design-long-running-apps)
  - C compiler $20K / 2,000 sessions (one project) — [Anthropic (2026-02-05)](https://www.anthropic.com/engineering/building-c-compiler)
- **Contradiction on context editing:** +29%/+39% performance and −84% tokens (2025-09-29, internal agentic-search and 100-turn eval) — [Anthropic news](https://www.anthropic.com/news/context-management); versus "cost more than it saved… context editing cost 74% more" on a 20-issue run and "changed nothing" on a long run (2026) — [Anthropic cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence). The two use different metrics: task success under context exhaustion vs dollar cost with caching.
- **Contradiction on the effort default:** internal evals showed medium "slightly lower intelligence with significantly less latency", yet the change was reverted after user reports [P] — [Claude Code quality postmortem](https://www.anthropic.com/engineering/april-23-postmortem). In Sept 2026 Claude Code's Opus 5.5 again defaults to `medium` [P] — [Claude Code docs: model config](https://code.claude.com/docs/en/model-config)
- **Noise floor:** resource configuration moved Terminal-Bench 2.0 success by +6 points from strict to uncapped, with infra errors of 5.8%→0.5% [P] — [Quantifying infrastructure noise (2026-02-05)](https://www.anthropic.com/engineering/infrastructure-noise). The cost guide itself treats "a task or two of pass rate, or cents of mean cost" as within noise on single runs [P] — claude-api skill cost reference (bundled Claude Code 2.1.282)
- **Unverified this session [R]:** Manus (production lessons), Chroma context rot (academic-style vendor research), Vercel AGENTS.md vs skills (vendor eval), ETH AGENTS.md study (academic), Cursor semantic search (vendor A/B), GPT-5-Codex −93.7% tokens and GPT-5.1-Codex-Max −30% thinking tokens (vendor), Cloudflare Code Mode (vendor).

### Inferences
- For planning, prefer the 2026 Anthropic guide's numbers. Treat them as API-priced and Claude-model-specific; the ranking holds, but magnitudes on Codex/Grok are unknown.
- Before adopting a lever, run a small A/B on your own issues. The guide's own advice is to sweep effort first and compare cost per solved task with failed attempts in the denominator. That needs the per-task accounting this baseline lacks (covered by the observability researcher).
- Any claim under about 3 points of pass rate from a single run should be treated as noise.

### Gaps
- There is no independent, peer-reviewed 2026 benchmark of "context rot" or of subagent/multi-agent overheads for CLI coding agents (Claude Code, Codex, Grok) end to end.
- There is no public cost-per-solved-task comparison across Claude Code, Codex CLI and Grok CLI harnesses under subscription billing.
- [R-leads to verify when search is available]:
  - AgentDiet ("Improving the Efficiency of LLM Agent Systems through Trajectory Reduction", 2025): reportedly −40–60% input tokens and −21–36% cost at equal performance.
  - SWE-Effi (2025): "token snowball" and "expensive failures", i.e., failed runs consume more resources than successful ones.
  - IFScale (2025): instruction-following degrades with instruction density.
  - Amp "handoff" replacing compaction.
  - The Codex usage-limit table for 2026 plans.
  - xAI Grok model pricing and caching for the CLI's default model.
