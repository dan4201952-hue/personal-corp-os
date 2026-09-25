# Observability, transcript mining, failure taxonomies and evals for orchestrated CLI coding agents

_Legend: **[V]** = verified in a primary source fetched in this session (official docs on code.claude.com / anthropic.com, source code or README on raw.githubusercontent.com, PyPI / npm registry metadata). **[S]** = seen only in a WebSearch result snippet; the page itself was not opened. **[I]** = my inference. "Background" = published before 2025. Research date: 2026-09-25. Doc pages are living documents, so "current" means "as fetched on 2026-09-25". Claude Code version dates come from npm publish times of `@anthropic-ai/claude-code` [V] ([npm](https://registry.npmjs.org/@anthropic-ai/claude-code)). The shared WebSearch budget ran out partway through, so academic items reachable only through arXiv or search are thinner; they are listed under Gaps._

_Baseline for comparison ("fable-ruki-agenty", `skills/fable-ruki-agenty/SKILL.md` in this repo): Fable, the orchestrator, only writes specs into GitHub issue bodies. It dispatches by pointer to Codex (coding, review, verification, through the `codex:codex-rescue` / codex-companion plugin) and to Grok workers in Orca terminals. A forwarder posts a per-issue journal (▶ dispatch → ↩ executor report → ✔/✖ verifier → 🔁 rework N → ⛔ blocked / close) with labels `wip:dispatched`, `wip:verifying`, `wip:rework` and `blocked`. A fresh-context Codex verifier checks the DoD. The ladder is 2 reworks, then a fresh executor, then blocked. There is a private `incidents.md`, a rule of "2+ open entries of one class → issue-first skill edit", and a weekly human retro. Known gaps: no metrics or evals, no token or time accounting, the orchestrator grades itself, and no check on recurrence._

## 1. Telemetry: turning agent runs into data (tokens, cost, time, tool calls, errors, reworks)

### Takeaway
Every CLI in the user's stack now emits structured data that can be tied to a prompt or turn:
- **Claude Code** has the most: OpenTelemetry metrics, events and beta traces. They carry `prompt.id`, subagent lineage, per-tool success, duration and result size, and cost attributed to each skill, plugin or subagent.
- **Codex CLI** has OTel events (including a per-turn cost event, `codex.turn_cost`), a typed JSONL stream from `codex exec --json` with usage for each turn, and on-disk session rollouts.
- **Gemini CLI** has OTel (with built-in loop-detection events).
- **Grok Build CLI** writes usage for each turn to `~/.grok`.

The cheapest route needs no infrastructure: parse the local logs with **ccusage**, which reads Claude Code, Codex, Gemini, Grok Build, OpenCode and more. No tool knows about "rework", "verifier verdict" or "blocked". Those exist only in the orchestrator's own journal, which in the baseline is the GitHub issue timeline. That journal is the join key the telemetry needs.

### Cited Findings

#### 1.1 Claude Code (Fable's own runtime): OpenTelemetry [V]
- **Enablement.** Set `CLAUDE_CODE_ENABLE_TELEMETRY=1` plus the standard `OTEL_METRICS_EXPORTER` / `OTEL_LOGS_EXPORTER` / `OTEL_TRACES_EXPORTER` variables (otlp, prometheus, console or none). Metrics export every 60 s by default and logs and events every 5 s. Content is redacted unless `OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_ASSISTANT_RESPONSES`, `OTEL_LOG_TOOL_DETAILS`, `OTEL_LOG_TOOL_CONTENT` or `OTEL_LOG_RAW_API_BODIES` is set. Custom team or cost-centre tags go in `OTEL_RESOURCE_ATTRIBUTES`. — [Claude Code: Monitoring](https://code.claude.com/docs/en/monitoring-usage)
- **Metrics.**
  - `claude_code.session.count`, `lines_of_code.count`, `pull_request.count`, `commit.count` and `active_time.total` (type `user` or `cli`).
  - `claude_code.cost.usage` (USD) and `claude_code.token.usage` (type `input` / `output` / `cacheRead` / `cacheCreation`), both with attributes `model`, `query_source` (`main` / `subagent` / `auxiliary`), `effort`, `agent.name`, `skill.name`, `plugin.name`, `mcp_server.name` and `mcp_tool.name`.
  - `claude_code.code_edit_tool.decision`, with `source` values `config`, `hook`, `user_permanent`, `user_temporary`, `user_abort` and `user_reject`.
  - Source: [Monitoring](https://code.claude.com/docs/en/monitoring-usage)
- **Events and correlation.**
  - Events: `user_prompt`, `assistant_response` (v2.1.193+, 2026-06-25), `tool_result`, `tool_decision`, `api_request`, `api_error`, `api_retries_exhausted`, `api_refusal`, `skill_activated` and `at_mention`.
  - Correlation attributes: `prompt.id` (one UUID links every event from a single user prompt), `event.sequence`, `message.uuid` (joins to the transcript entry, v2.1.214+) and `client_request_id`. Events carry `trace_id` / `span_id` from v2.1.214 (2026-07-18).
  - Source: [Monitoring](https://code.claude.com/docs/en/monitoring-usage)
- **Fields useful for waste detection.**
  - `tool_result` carries `success`, `duration_ms`, `error_type` (for example `Error:ENOENT`, `ShellError`), `decision_source`, `tool_input_size_bytes` and `tool_result_size_bytes`. Result size is a direct "oversized read" signal.
  - `api_request` carries `duration_ms`, `cost_usd`, `cost_usd_micros`, input, output and cache token counts, `query_source` and `effort`.
  - `api_error` carries `attempt` (retries).
  - Source: [Monitoring (markdown source)](https://code.claude.com/docs/en/monitoring-usage.md)
- **Traces (beta, `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`).**
  - Span tree: `claude_code.interaction`, containing `claude_code.llm_request`, `claude_code.hook` and `claude_code.tool`; a tool span contains `tool.blocked_on_user`, `tool.execution` and subagent spans.
  - `llm_request` carries `agent_id`, `parent_agent_id`, `workflow.run_id`, `ttft_ms`, tokens and `stop_reason`.
  - `tool` carries `duration_ms`, `result_tokens` and `bash_command_class`.
  - `tool.execution` carries `success`, `error` and `error_class`.
  - Source: [Monitoring](https://code.claude.com/docs/en/monitoring-usage)
- **Trace propagation across processes.**
  - Bash subprocesses inherit a W3C `TRACEPARENT` for the active tool span.
  - `-p` and Agent SDK sessions read `TRACEPARENT` / `TRACESTATE` from the environment when an interaction starts, so an external orchestrator script can parent a Claude Code run under its own trace.
  - Source: [Monitoring](https://code.claude.com/docs/en/monitoring-usage)
- **Change history (dated via npm).**
  - New Active Time metric: v1.0.39 (2025-07-01).
  - `tool_decision` fixed in headless/SDK mode: v2.1.47 (2026-02-18).
  - `OTEL_LOG_RAW_API_BODIES`: v2.1.111 (2026-04-16).
  - `tool_use_id` added to `tool_result` / `tool_decision`: v2.1.119 (2026-04-23).
  - `skill_activated` gained `invocation_trigger`: v2.1.126 (2026-04-30).
  - `agent_id` / `parent_agent_id` on spans: v2.1.139 and v2.1.145 (2026-05-11 and 2026-05-19).
  - Sources: [CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md); [npm times](https://registry.npmjs.org/@anthropic-ai/claude-code)
- **Caveat on custom skills.** User-defined and third-party plugin skill names are redacted by default: `skill.name = "custom_skill"`, and `plugin.name` is `third-party`. Real names appear only with `OTEL_LOG_TOOL_DETAILS=1`. — [Measure plugin cost and usage](https://code.claude.com/docs/en/plugins/measure); [Monitoring](https://code.claude.com/docs/en/monitoring-usage.md)
- **Cost is an estimate.** Claude Code prices tokens locally at list price unless an admin sets a `modelPricing` table (v2.1.242+). The docs say OTel is "the only option that streams per-user token and cost metrics into your own observability stack in near real time". For enterprise deployments they give an average of about $13 per developer per active day ($150–250 per month), with 90% of users under $30 per active day. — [Manage costs](https://code.claude.com/docs/en/costs)

#### 1.2 Claude Code: in-session and scripted cost fields [V]
- **`/usage`** (with `/cost` and `/stats` as aliases).
  - Session block: total cost, API duration, wall duration, lines changed, and per-model input, output, cache read and cache write.
  - Cache line (v2.1.251+, 2026-08-28): share of input served from cache, number of misses, and a "likely cause" for the last miss.
  - On subscription plans: **attribution** of recent usage to skills, subagents, plugins and MCP servers, and **behavior flags** for any behavior (long context, cache misses) that accounts for 10% or more of recent usage.
  - The "Loops" rows (v2.1.242+) cover `/loop` and other scheduled tasks. They are not reasoning loops.
  - For Pro and Max subscribers the session dollar figure is "not relevant for billing".
  - Source: [Manage costs](https://code.claude.com/docs/en/costs)
- **Status line JSON.** Fields include `cost.total_cost_usd`, `cost.total_duration_ms`, `cost.total_api_duration_ms`, `cost.total_lines_added/removed`, `context_window.used_percentage` and `context_window.total_input_tokens`. This repo already ships a statusline, so the same numbers can be logged per session. — [Status line](https://code.claude.com/docs/en/statusline)
- **Headless mode (`claude -p`).**
  - `--output-format json` returns `total_cost_usd` and a per-model cost breakdown. `stream-json` ends with a `result` message.
  - Subagent messages carry `parent_tool_use_id`. `--forward-subagent-text` (v2.1.211+) adds subagent text and thinking, so each subagent transcript can be rebuilt.
  - `system/api_retry` events carry attempt and error category. `system/init` lists `plugin_errors` and `mcp_server_errors`. The result lists `permission_denials`.
  - `--bare` is recommended for scripted runs and "will become the default for `-p`".
  - Source: [Run Claude Code programmatically](https://code.claude.com/docs/en/headless)
- **Agent SDK.**
  - Scope of the cost fields: `total_cost_usd` and `modelUsage` include subagents; `usage` excludes them and undercounts once nesting occurs. Parallel tool calls share a message ID, so deduplicate by ID. Per-step `output_tokens` is a placeholder.
  - Session totals on resume: since v2.1.277 (2026-09-18) a resumed session restores its totals, so summing results across resumes double-counts.
  - Accuracy: all figures are client-side estimates, and the docs say "Do not bill end users… from these fields".
  - Source: [Track cost and usage](https://code.claude.com/docs/en/agent-sdk/cost-tracking)
- **Team-level analytics.** The Console/Teams dashboards and the Claude Code Analytics API give daily per-user metrics: lines accepted, suggestion accept rate, DAU and sessions, and PRs and lines shipped (contribution metrics are in public beta). — [Analytics](https://code.claude.com/docs/en/analytics); [Manage costs](https://code.claude.com/docs/en/costs)

#### 1.3 Claude Code hooks as a data tap [V]
- **Events.** 33 hook events, including `PostToolUseFailure` (with `error`), `PostToolBatch`, `StopFailure`, `SubagentStart`/`SubagentStop`, `PreCompact`/`PostCompact`, `InstructionsLoaded` and `SessionEnd`. — [Hooks reference](https://code.claude.com/docs/en/hooks)
- **Input fields.** Every hook gets `session_id`, `prompt_id` (v2.1.196+), `transcript_path`, `cwd`, `agent_id` and `agent_type`. `SubagentStop` adds `agent_transcript_path` and `last_assistant_message`. — [Hooks reference](https://code.claude.com/docs/en/hooks)
- **Blocking `Stop`.** A `Stop` hook can block with exit code 2, forcing the model to keep working (for example, to verify). Handler types are `command`, `http`, `mcp_tool`, `prompt` and `agent`. — [Hooks reference](https://code.claude.com/docs/en/hooks)
- **How the tracing integrations use hooks.** Langfuse, Arize and Braintrust all trace Claude Code through hooks that read the transcript. For example, Langfuse uses a Stop hook that converts transcripts into traces grouped by `session_id`. — [Langfuse Claude Code docs](https://langfuse.com/integrations/developer-tools/claude-code) [S]; [Langfuse plugin README](https://raw.githubusercontent.com/langfuse/claude-observability-plugin/main/README.md) [V]

#### 1.4 Codex CLI (baseline hands: coding, review, verifier)
- **`codex exec --json` event schema** [V, from source on `main`]:
  - Thread and turn events: `thread.started` (`thread_id`), `turn.started`, `turn.completed` (with `usage`: `input_tokens`, `cached_input_tokens`, `cache_write_input_tokens`, `output_tokens`, `reasoning_output_tokens`) and `turn.failed`.
  - Item events: `item.started`, `item.updated` and `item.completed`, over item types `agent_message`, `reasoning`, `command_execution` (`command`, `aggregated_output`, `exit_code`, status `in_progress` / `completed` / `failed` / `declined`), `file_change` (path, kind add / delete / update, apply status), `mcp_tool_call`, `collab_tool_call` (spawn_agent / send_input / wait / close_agent), `web_search`, `todo_list` and `error`.
  - Source: [exec_events.rs](https://raw.githubusercontent.com/openai/codex/main/codex-rs/exec/src/exec_events.rs)
- **OTel event names in source** [V]:
  - `codex.conversation_starts`, `codex.api_request`, `codex.sse_event`, `codex.user_prompt`, `codex.tool_decision`, `codex.sandbox_outcome` and `codex.turn_ttft`.
  - `codex.turn_cost`, with `usage.estimated_usd`, `turn.interrupted`, `speed` and `reasoning_effort`, plus a matching micro-USD counter metric.
  - `codex.startup_phase`, `codex.websocket_*` and the span fields `codex.usage.total_tokens` / `codex.usage.reasoning_output_tokens`.
  - Source: [session_telemetry.rs](https://raw.githubusercontent.com/openai/codex/main/codex-rs/otel/src/events/session_telemetry.rs)
- **codex-otel crate** [V]:
  - OTLP HTTP and gRPC exporters for logs, traces and metrics, with W3C trace-context helpers.
  - Opt-in `otel.log_agent_responses` emits `codex.agent_response`, tagged `agent.type` main/subagent with `conversation.id` / `parent.conversation.id` lineage.
  - Opt-in `otel.log_guardian_assessments`.
  - Source: [codex-rs/otel/README.md](https://raw.githubusercontent.com/openai/codex/main/codex-rs/otel/README.md)
- **User-facing config** [S]:
  - `[otel]` in `config.toml`, with `exporter = "none" | "otlp-http" | "otlp-grpc"`, `environment` and `log_user_prompt = false`. Off by default.
  - `codex.tool_decision` records approved or denied, and whether the decision came from config or the user. `codex.tool_result` carries duration, success and an output snippet.
  - Sources: [OpenAI Codex advanced config](https://developers.openai.com/codex/config-advanced); [SigNoz Codex](https://signoz.io/docs/codex-monitoring/); [original PR #2103](https://github.com/openai/codex/pull/2103); third-party consumers [Opik](https://www.comet.com/docs/opik/integrations/openai-codex), [LangWatch](https://langwatch.ai/docs/coding-agents/openai-codex) and [Monad detection engineering](https://www.monad.com/blog/detection-engineering-for-openai-codex-otel)
- **On-disk rollouts** [V]:
  - Codex writes session JSONL under `CODEX_HOME` (default `~/.codex`) in `sessions/` and `archived_sessions/`.
  - `token_count` events exist only since commit 0269096 (2025-09-06).
  - Codex CLI ≥0.144.0 persists `thread_settings_applied` events (for example the speed setting).
  - ccusage can also read saved `codex exec --json` output.
  - Source: [ccusage Codex guide](https://raw.githubusercontent.com/ccusage/ccusage/main/docs/guide/codex/index.md)
- **Maturity** [V]: `@openai/codex` on npm since 2025-04-16; latest 0.157.0, published 2026-09-25. — [npm](https://registry.npmjs.org/@openai/codex)

#### 1.5 Gemini CLI [V]
- **Configuration.** `telemetry` block in `.gemini/settings.json` (or `GEMINI_TELEMETRY_*` environment variables) with `target` gcp or local, `otlpEndpoint`, `outfile` and `logPrompts`. — [telemetry.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/telemetry.md)
- **Events.**
  - `gemini_cli.tool_call` (`function_name`, `duration_ms`, `success`, `decision` accept / reject / modify / auto_accept, `error`) and `api_response` (`input_token_count`, `output_token_count`, `duration_ms`).
  - `chat_compression` (`tokens_before`, `tokens_after`), `tool_output_truncated`, `conversation_finished` (`turnCount`) and `agent.start/finish`.
  - Source: [telemetry.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/telemetry.md)
- **Metrics.** `token.usage` (input / output / thought / cache / tool), `tool.call.count` and `tool.call.latency`, `api.request.latency`, `file.operation.count`, `lines.changed`, `agent.turns`, plus GenAI semantic-convention metrics `gen_ai.client.token.usage` and `gen_ai.client.operation.duration`. — [telemetry.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/telemetry.md)
- **Loop detection.** The CLI ships a `LoopDetectionService`:
  - Loop types: 5 identical consecutive tool calls; a "content chanting" loop of 10 repeats of a 50-character chunk; and an LLM-judged loop check that starts after 30 turns and repeats every 5–15 turns, firing at confidence ≥0.9.
  - It emits `loop_detected` and `gemini_cli.llm_loop_check` events.
  - Sources: [loopDetectionService.ts](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/packages/core/src/services/loopDetectionService.ts); [telemetry types.ts](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/packages/core/src/telemetry/types.ts)
- **Maturity** [V]: `@google/gemini-cli` since 2025-06-25; 0.61.0 on 2026-09-25. — [npm](https://registry.npmjs.org/@google/gemini-cli)

#### 1.6 Grok CLI (baseline scouts in Orca)
- **Local logs** [V]. ccusage reads completed turns from `updates.jsonl` under `GROK_HOME` (default `~/.grok`) for "Grok Build CLI". — [ccusage Grok guide](https://raw.githubusercontent.com/ccusage/ccusage/main/docs/guide/grok/index.md)
- **Further details** [S]:
  - Session dirs hold `updates.jsonl` with `turn_completed` usage, including `costUsdTicks` at 1e-10 USD. A global `~/.grok/logs/unified.jsonl` has `shell.turn.inference_done` rows.
  - Grok Build OTel telemetry is double opt-in and tags events with `session.id` and `prompt.id`.
  - Sources: [thermal PR #10](https://github.com/jadmadi/thermal/pull/10); [SigNoz Grok Build](https://signoz.io/docs/grok-build-observability/)
- **Two packages exist** [V]: the official `@xai-official/grok` ("Bring Grok into your terminal"; created 2025-10-22; 1.0.41 on 2026-09-22) and the community `@vibe-kit/grok-cli` (2025-07-21; last release 2025-11-27, so dormant). — [npm official](https://registry.npmjs.org/@xai-official/grok); [npm community](https://registry.npmjs.org/@vibe-kit/grok-cli)

#### 1.7 Session-cost tools
- **ccusage** [V]
  - What it is: by ryoppippi, now the `ccusage` org. "Analyze coding (agent) CLI token usage and costs from local data."
  - Coverage: 18 sources, including Claude Code, Codex, OpenCode, Amp, Droid, Gemini CLI, GitHub Copilot CLI, Grok Build CLI, Kimi, Qwen and Goose.
  - Reports: daily, weekly, monthly and session, plus Claude 5-hour `blocks` and a beta `statusline`. `--json` and `--by-agent` are supported.
  - Pricing: taken from a pinned LiteLLM price file. `--offline` works.
  - Maturity: npm since 2025-05-29; v20.0.24 on 2026-09-21; 136 versions; sponsors listed. The old `@ccusage/codex` package is deprecated in favour of `ccusage codex`.
  - Sources: [README](https://raw.githubusercontent.com/ryoppippi/ccusage/main/apps/ccusage/README.md); [npm](https://registry.npmjs.org/ccusage); [@ccusage/codex](https://registry.npmjs.org/@ccusage/codex)
- **Limitations** [V]: costs are estimates from local files only; Codex logs before 2025-09-06 have no token events; some Codex usage stays unclassified by speed. — [ccusage Codex guide](https://raw.githubusercontent.com/ccusage/ccusage/main/docs/guide/codex/index.md)
- **Other cost tools** [S]: SuperBased, ClawMetry and Lineman.io (a ccusage sponsor that claims "40% lower token usage"). Not evaluated. — [search result list](https://superbased.app/docs/track/grok); [ccusage README](https://raw.githubusercontent.com/ryoppippi/ccusage/main/apps/ccusage/README.md)

#### 1.8 Integrations and dashboards
- **Langfuse** [V]
  - Official plugin `langfuse/Claude-Observability-Plugin`. It traces prompts, turns, generations (tokens and cost), thinking blocks, tool calls, skills, subagents and images.
  - Setup [S]: needs `langfuse>=4.0`. Langfuse also publishes a guide to tracing Claude Code, Codex, Copilot and others.
  - Langfuse is self-hostable. PyPI `langfuse` 4.15.6 (2026-09-24).
  - Sources: [README](https://raw.githubusercontent.com/langfuse/claude-observability-plugin/main/README.md); [docs](https://langfuse.com/integrations/developer-tools/claude-code) [S]; [coding-agent tracing](https://langfuse.com/resources/engineering/coding-agent-tracing) [S]; [PyPI](https://pypi.org/pypi/langfuse/json)
- **LangSmith** [V]
  - Plugin `langsmith-tracing@langsmith-claude-code-plugins` traces conversations, tool calls, subagent executions and context compaction.
  - [S]: enabled per project with `TRACE_TO_LANGSMITH=true`; "LangSmith Insights" looks for trends across traces; first announced around August 2025.
  - Sources: [README](https://raw.githubusercontent.com/langchain-ai/langsmith-claude-code-plugins/main/README.md); [docs](https://docs.langchain.com/langsmith/trace-claude-code) [S]; [X announcement](https://x.com/LangChainAI/status/1953103695765295333) [S]; [LangChain blog: debug coding agents with traces](https://www.langchain.com/blog/your-coding-agents-are-a-black-box-heres-how-to-crack-them-open) [S]
- **Arize AX / Phoenix** [V]
  - `Arize-ai/coding-harness-tracing` traces Claude Code CLI/Agent SDK, **Codex CLI**, Cursor, Copilot and **Gemini CLI** with OpenInference spans. Each Claude Code turn becomes a CHAIN with LLM spans, TOOL spans and an AGENT subtree for subagents. Phoenix is open source and self-hostable.
  - OpenInference instrumentation for the Claude Agent SDK: PyPI since 2026-03-04, v0.1.18 on 2026-09-10.
  - Sources: [README](https://raw.githubusercontent.com/Arize-ai/coding-harness-tracing/main/README.md); [PyPI](https://pypi.org/pypi/openinference-instrumentation-claude-agent-sdk/json); [Phoenix docs](https://arize.com/docs/phoenix/integrations/coding-agents/claude-code) [S]
- **Braintrust** [V]
  - Plugin generated from `braintrust-coding-agent-plugins`. It covers the Claude Code CLI and desktop Claude Code mode, but not Cowork, and uses the `bt` CLI.
  - [S]: each session becomes one trace with session, turn, model call, tool and subagent spans. A second plugin lets Claude query Braintrust logs and experiments.
  - Sources: [README](https://raw.githubusercontent.com/braintrustdata/braintrust-claude-plugin/main/README.md); [docs](https://www.braintrust.dev/docs/integrations/developer-tools/claude-code) [S]; [blog](https://www.braintrust.dev/blog/claude-code-braintrust-integration) [S]
- **Datadog** [S]: Agent Console has a Claude Code tile covering usage, cost, latency, errors and tool decisions, over OTLP through the Datadog Agent. — [Datadog Agent Console setup](https://docs.datadoghq.com/ai_agents_console/setup/); [Martin Amps](https://ma.rtin.so/posts/monitoring-claude-code-with-datadog/)
- **Grafana, SigNoz and Honeycomb.**
  - SigNoz [S]: prebuilt dashboards for Claude Code, Codex and Grok Build. — [SigNoz Claude Code](https://signoz.io/docs/claude-code-monitoring/)
  - Grafana [S]: dashboard 25052. — [Grafana dashboard](https://grafana.com/grafana/dashboards/25052-claude-code/)
  - `ColeMurray/claude-code-otel` [V]: an open-source OTel stack with dashboards for cost by model and user, tool usage, API latency and success rate, and sessions. — [README](https://raw.githubusercontent.com/ColeMurray/claude-code-otel/main/README.md)
  - Honeycomb [S]: described as good for session-level investigation, with Claude Code boards and MCP support. — [Dash0 comparison of 8 tools, 2026](https://www.dash0.com/comparisons/claude-code-monitoring-tools)
- **Helicone.** Not found. The Claude Code docs describe the general **LLM-gateway** pattern and name LiteLLM for per-key spend tracking [V]. — [Manage costs](https://code.claude.com/docs/en/costs); [LLM gateway](https://code.claude.com/docs/en/llm-gateway)

### Inferences
- **[I] Baseline delta.** The baseline journal already logs phase *transitions* (dispatch, report, verdict, rework N, blocked/close) with timestamps and labels. It does not log *resources*. All the needed resource data already exists on disk: Fable's Claude Code transcripts and OTel, Codex rollouts and `turn.completed` usage, and Grok `updates.jsonl`. The missing piece is a join key. Have the forwarder record, for every dispatch, the executor's session or thread id and the start and end time next to issue #N. Then a nightly script (or `ccusage session --json`) can attach tokens, $, wall time, tool calls and tool errors to each journal entry.
- **[I] Codex metrics.** Codex is reached through the codex-companion plugin rather than raw `codex exec --json`. The robust source is therefore the rollout JSONL in `~/.codex/sessions`: its `token_count` events give tokens, and tool calls and command exit codes appear there too. If the forwarder ever calls `codex exec --json` directly, the stream alone gives per-turn usage and per-command `exit_code` / `status=failed|declined`, which is enough to count "tool errors" and "declined commands" per task.
- **[I] One end-to-end trace.** Claude Code passes `TRACEPARENT` to Bash subprocesses, and codex-otel has W3C trace-context support. If the forwarder launches hands through Bash from a traced session, the hands' spans might nest under the orchestrator's span, giving one trace per issue. Whether Codex or Grok actually read `TRACEPARENT` from the environment is unverified (see Gaps).
- **[I] Measure Fable's cost per skill.** Fable's own cost is the scarcest resource in the baseline ("Токены Fable — самый дорогой ресурс"). `claude_code.cost.usage` split by `query_source` and `skill.name` measures it directly, but only with `OTEL_LOG_TOOL_DETAILS=1`; otherwise the skill appears as `custom_skill`. Without OTel, `/usage` attribution gives a coarser weekly share per skill.
- **[I] Subscriptions.** Where the Claude, Codex and Grok CLIs run on subscriptions, list-price dollars are a *normalised effort unit*, not spend. Tokens (especially cache-read vs uncached input) and wall time are the operational metrics.

### Gaps
- Codex user-facing `[otel]` keys, and whether Codex and Grok honour an inherited `TRACEPARENT`, were not verified in primary docs (developers.openai.com is not reachable from here).
- Grok CLI: the exact telemetry schema (`costUsdTicks`, `unified.jsonl`) is snippet-only. It is unknown which Grok CLI (official xAI or vibe-kit) the user's Orca workers run.
- Orca (terminal manager) telemetry or event-log formats were not researched; the name is ambiguous in search.
- Helicone integration with these CLIs was not found. Datadog, SigNoz, Grafana and Honeycomb details are snippet-only.
- Other session-cost tools popular in 2026 (tokscale, splitrail, vibe-log and others) were not researched because the search budget ran out.

## 2. Transcript mining: finding inefficient or wrong behaviour inside transcripts

### Takeaway
The raw material is already on disk: Claude Code JSONL, Codex rollouts and Grok `updates.jsonl`. The practitioner consensus, stated explicitly by Anthropic, is: read transcripts regularly, compute cheap trajectory metrics (turns, tool calls, tokens, tool errors, result sizes), then use an LLM to cluster or explain. Treat LLM judges as *candidate generators, not ground truth*. The best model localises errors in agent traces only 11% of the time on TRAIL, and a self-grading agent skews positive.

Built-in, zero-setup analysers now exist for Claude Code: `/insights`, `/usage` attribution and behaviour flags, `/skill-doctor` and `claude plugin details`. For Codex and Grok the options are ccusage, claude-code-log (Codex beta), tracing plugins (Arize for Codex/Gemini) and home-made parsers.

### Cited Findings

#### 2.1 Where transcripts live and how long [V]
- **Claude Code.** JSONL at `~/.claude/projects/<project>/<session-id>.jsonl`. Retention is **30 days by default** (`cleanupPeriodDays`), so longitudinal mining needs a longer retention or an archive. `claude --resume <path.jsonl>` reopens a transcript. — [Manage sessions](https://code.claude.com/docs/en/sessions)
- **Hooks.** Hooks receive `transcript_path`, and `SubagentStop` also receives `agent_transcript_path`, so a hook can snapshot every transcript, including subagents, at the moment it finishes. — [Hooks](https://code.claude.com/docs/en/hooks)
- **Codex.** `~/.codex/sessions/` and `archived_sessions/` (JSONL rollouts). **Grok Build:** `~/.grok/.../updates.jsonl`. — [ccusage Codex](https://raw.githubusercontent.com/ccusage/ccusage/main/docs/guide/codex/index.md); [ccusage Grok](https://raw.githubusercontent.com/ccusage/ccusage/main/docs/guide/grok/index.md)

#### 2.2 Built-in analysers in Claude Code [V]
- **`/insights`** writes an HTML report on "what you work on, friction points such as misunderstood requests or buggy code, and suggestions".
  - Scope: up to 200 sessions not seen before per run, skipping very short ones. Report goes to `~/.claude/usage-data/report.html` with timestamped copies.
  - Cost: it runs through the same provider and account, so its tokens count against plan or API.
  - Limits: local sessions only; not available in cloud sessions.
  - Sources: [Manage costs](https://code.claude.com/docs/en/costs); [Commands](https://code.claude.com/docs/en/commands)
  - First changelog mention is a fix in v2.1.101 (2026-04-10), so it launched earlier; the exact launch date is unverified. — [CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md)
  - v2.1.281 (2026-09-23) added an auto-mode recommendation estimating how many permission prompts auto mode could have handled. — [CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md)
  - **Conflict:** blog posts [S] describe it as "last 30 days, up to 50 sessions" and "nothing leaves your machine". The official doc says up to 200 sessions per run and that the analysis runs through your model provider. The product has changed, and the "nothing leaves" claim is misleading. — [MindStudio](https://www.mindstudio.ai/blog/claude-code-insights-command-workflow-audit) [S]; [Pasquale Pillitteri](https://pasqualepillitteri.it/en/news/408/claude-code-insights-command-workflow) [S]
  - A user report [S] says friction (wrong approach, buggy code, misunderstood requests) was about 4% of messages, and that the report produces paste-ready CLAUDE.md rules tied to the sessions where the problem occurred. — [Vincent Qiao](https://blog.vincentqiao.com/en/posts/claude-code-insights/) [S]; [1,282 hours with /insights](https://vanja.io/claude-code-insights-revealed/) [S]
- **`/usage`**: per-skill, subagent, plugin and MCP attribution, plus behaviour flags for long context and cache misses (≥10% of usage). — [Manage costs](https://code.claude.com/docs/en/costs)
- **`/skill-doctor`** (v2.1.252+) shows each skill's context cost and how often it is used, and flags skills that were never invoked. `/doctor` lists unused skills, MCP servers and plugins. — [Commands](https://code.claude.com/docs/en/commands); [Measure plugins](https://code.claude.com/docs/en/plugins/measure)
- **`claude plugin details <plugin>`** projects each plugin's **always-on token cost** (names and descriptions loaded into every session) and each skill's cost when invoked. The official marketplace highlights plugins that cost 2,000 or more tokens per turn. — [Measure plugin cost and usage](https://code.claude.com/docs/en/plugins/measure)

#### 2.3 Third-party transcript viewers and miners
- **claude-code-log** (daaain) [V]
  - Converts Claude Code JSONL to HTML or Markdown, with a TUI, watch mode, token usage per message and per session, and date filters.
  - `--detail full|high|low|minimal|user-only` plus `--compact` are meant "to feed past conversations back to an LLM for analysis or experience building".
  - Codex CLI support is beta and Antigravity is alpha, single-session only.
  - Maturity: PyPI since 2025-06-15; v1.6.0 on 2026-08-31; 34 releases.
  - Sources: [README](https://raw.githubusercontent.com/daaain/claude-code-log/main/README.md); [PyPI](https://pypi.org/pypi/claude-code-log/json)
- **sniffly** (Chip Huyen) [V]: a local dashboard for Claude Code logs covering usage patterns, an **error breakdown** ("see where Claude Code makes mistakes") and message history. It looks stale: PyPI releases span only 2025-07-16 to 2025-07-28 (0.1.5). — [README](https://raw.githubusercontent.com/chiphuyen/sniffly/main/README.md); [PyPI](https://pypi.org/pypi/sniffly/json)
- **Docent** (Transluce) [V]: an "AI agent analysis platform" that ingests transcripts and is self-hostable. It is active: `docent-python` (renamed `docent`) has 90 releases from 2025-06-27 to 2026-09-16. Feature details were not verified. — [README](https://raw.githubusercontent.com/TransluceAI/docent/main/README.md); [PyPI](https://pypi.org/pypi/docent-python/json)
- **HAL harness** (Princeton) [V]: logs agent traces automatically, tracks cost through W&B Weave, and publishes encrypted traces with `hal-decrypt`. The leaderboard is **paused**; the team now focuses on an agent **reliability** dashboard. — [README](https://raw.githubusercontent.com/princeton-pli/hal-harness/main/README.md)

#### 2.4 LLM-as-judge over trajectories [V unless noted]
- **MAST annotator (`agentdash`, UC Berkeley)** labels a multi-agent trace with the 14 MAST failure modes through an LLM judge. The default model is `o1-mini` and it is OpenAI-only. It returns binary flags per mode, a summary and a task-completion flag. Maturity is low: one release (0.1.0, 2025-08-12). A 1K+ trace MAST dataset is on Hugging Face (`mcemri/MAD`). — [PyPI agentdash](https://pypi.org/project/agentdash/); [MAST README](https://raw.githubusercontent.com/multi-agent-systems-failure-taxonomy/MAST/main/README.md)
- **TRAIL** (Patronus AI, arXiv 2505.08638, May 2025) has 148 annotated traces with 841 errors across reasoning, execution and planning, drawn from SWE-bench and GAIA. **The best model reaches only 11% accuracy** at localising the errors. — [TRAIL README](https://raw.githubusercontent.com/patronus-ai/trail-benchmark/main/README.md)
- **Who&When** (ICML 2025 spotlight) is a benchmark for automated failure attribution: which agent, which step. It has 184 annotated failures from CaptainAgent and Magentic-One systems, and compares three judging strategies: all-at-once, step-by-step and binary search. Its accuracy numbers were not verified here. — [README](https://raw.githubusercontent.com/mingyin1/Agents_Failure_Attribution/main/README.md)
- **AgentDebug** (arXiv 2509.25370, Sept 2025) introduces AgentErrorTaxonomy (17 error types across memory, reflection, planning, action and system) and AgentErrorBench, with a two-stage detector: fine-grained step analysis, then critical-error identification. — [README](https://raw.githubusercontent.com/ulab-uiuc/AgentDebug/main/README.md)
- **Agent-as-a-Judge** (ICML 2025; first posted in 2024, so background) is an agentic judge that gives step-by-step feedback. It claims to save 97.72% of time and 97.64% of cost versus human experts. — [README](https://raw.githubusercontent.com/metauto-ai/agent-as-a-judge/main/README.md)
- **Judges inside eval tools.**
  - `claude plugin eval` `llm` graders pass on 2 of 3 votes. With `focus: trace`, the judge sees **only the first 12 and last 12 messages**; a `regex` grader sees the whole trace. — [Plugin evals](https://code.claude.com/docs/en/plugin-evals)
  - `@vercel/agent-eval` has a transcript judge (`expect(transcript).toSatisfyCriterion('diagnosed with DevTools, not trial-and-error edits')`) that reads the transcript by path, so the transcript is never pasted into the prompt. — [agent-eval README](https://raw.githubusercontent.com/vercel-labs/agent-eval/main/README.md)
- **Leniency.** Anthropic reports that "agents reliably skew positive when grading their own work". Separating the doer from the judge "proves to be a strong lever", and "tuning a standalone evaluator to be skeptical turns out to be far more tractable". (2026-03-24) — [Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)

#### 2.5 Cheap heuristic detectors (no LLM)
- **Gemini CLI's detectors** can be ported to any JSONL: identical consecutive tool calls ≥5, repeated 50-character content chunks ≥10, and an LLM check only after 30 turns. — [loopDetectionService.ts](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/packages/core/src/services/loopDetectionService.ts)
- **Claude Code signals** for "oversized reads" and "failed tools": `tool_result_size_bytes`, `success`/`error_type` and `result_tokens`. — [Monitoring](https://code.claude.com/docs/en/monitoring-usage.md)
- **Transcript summary in `@vercel/agent-eval`** (`results.o11y`): `shellCommands` (with `exitCode` and `success`), `filesRead`, `filesModified`, `toolCalls` per tool, `totalToolCalls`, `webFetches`, `totalTurns`, `errors` and `thinkingBlocks`. Assertions can use them, for example `expect(results.o11y.totalToolCalls).toBeLessThan(50)`. — [agent-eval README](https://raw.githubusercontent.com/vercel-labs/agent-eval/main/README.md)

#### 2.6 Teams doing transcript reviews, and what they found [V]
- **Anthropic Research (2025-06-13).** They "built simulations… then watched agents work step-by-step". This revealed agents that kept going after they had enough results, used overly verbose search queries and picked the wrong tools. Early agents spawned "50 subagents for simple queries", searched endlessly for nonexistent sources, and distracted each other with excessive updates. Prompt engineering was the primary fix. — [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- **Anthropic tools (2025-09-11).**
  - "What agents omit in their feedback… can often be more important than what they include."
  - "Review the raw transcripts (including tool calls and tool responses)."
  - Lots of redundant calls suggests adjusting pagination or token limits; lots of invalid-parameter errors suggests clearer tool descriptions.
  - Transcript review showed Claude appending "2025" to web-search queries, which was fixed through the tool description.
  - They "concatenate the transcripts… and paste them into Claude Code" for analysis.
  - Source: [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- **Anthropic C compiler (2026-02-05).** The author watched "for mistakes Claude was making, then design[ed] new tests as I identified those failure modes". This is transcript review turned directly into regression tests. — [Building a C compiler](https://www.anthropic.com/engineering/building-c-compiler)
- **Anthropic Claude Code postmortem (2026-04-23).** Quality complaints were "challenging to distinguish from normal variation in user feedback", and "neither our internal usage nor evals initially reproduced" them. User `/feedback` reports and reproducible public examples were what "ultimately allowed us to identify and fix" the problems. — [Postmortem](https://www.anthropic.com/engineering/april-23-postmortem)

### Inferences
- **[I] Baseline delta.** The baseline "reads" behaviour only through the orchestrator's own incident notes and the weekly human retro. Nothing systematically scans Codex or Grok transcripts, so waste inside the hands (re-reads, Glob hangs, repeated failing commands) is invisible unless it causes a visible misfire. A weekly batch job could do this cheaply:
  - Parse the week's Codex rollouts and Grok `updates.jsonl` together with the issue journal.
  - Compute per-task trajectory stats: turns, tool calls, failed commands, repeated identical commands (Gemini-style), total bytes read, cache-hit share.
  - Pick outliers (top-cost tasks, any rework or blocked) for LLM-judge review under a fixed rubric (MAST modes plus the local incident classes).
  - Feed the judge's candidate labels into the human retro for confirmation. The TRAIL result (11%) argues against auto-filing its findings.
- **[I] Removing the orchestrator's self-grading.** Anthropic's leniency finding argues that the incident journal should not be written *only* by Fable. Run the classification pass in a separate fresh context, ideally a different model family (for example a Codex or Gemini judge over Claude transcripts, and vice versa), with a skeptical rubric. Fable should see its verdicts, not produce them.
- **[I] Retention.** A 30-day default is too short for "did the fix reduce recurrence" analyses spanning months. Either raise `cleanupPeriodDays` or archive transcripts per issue, for example with the `SubagentStop`/`SessionEnd` hook copying `transcript_path`.
- **[I] Privacy.** This is a public repo, and CLAUDE.md forbids private data in issues. Mined findings should go to the private `incidents.md` or a private dashboard. Self-hosted Langfuse, Phoenix or SigNoz avoid shipping transcripts to SaaS.

### Gaps
- Could not verify the details of `/insights` output (sections, how it classifies friction), when it launched, or its accuracy.
- Could not verify what Docent does in detail (search and clustering features), or LangSmith Insights and Braintrust topic clustering; each is only a title or snippet here.
- Who&When accuracy figures, and MAST inter-annotator agreement (kappa) and dataset composition, were not verified (arXiv not reachable).
- Could not find public, dated accounts of teams running *periodic* reviews of Codex CLI or Grok transcripts. The examples found are from Anthropic on Claude.

## 3. Failure taxonomies and anti-patterns (MAST, trajectory studies, token waste)

### Takeaway
MAST (2025) is the most widely reused multi-agent failure taxonomy. It has 14 modes in 3 groups (specification, inter-agent misalignment, task verification) and maps well onto an orchestrator → hands pipeline. The verification group alone (premature termination, missing or incorrect verification, weak verification) matches the baseline's verifier and ladder. It is complemented by:
- trace-level taxonomies: TRAIL (reasoning, execution, planning) and AgentErrorTaxonomy (17 types in 5 modules);
- a benchmark for test-gaming: ImpossibleBench;
- Anthropic's first-hand anti-patterns: premature "done", self-praise, subagent explosion, time blindness, context pollution.

On efficiency, the verified evidence is that token usage dominates both cost and outcome variance (80% of variance in Anthropic's BrowseComp analysis). Multi-agent setups use about 15× the tokens of chat.

### Cited Findings
- **MAST** ("Why Do Multi-Agent LLM Systems Fail?", Cemri et al., UC Berkeley; arXiv 2503.13657, March 2025) [V]:
  - Specification issues: 1.1 Disobey task specification; 1.2 Disobey role specification; 1.3 Step repetition; 1.4 Loss of conversation history; 1.5 Unaware of termination conditions.
  - Inter-agent misalignment: 2.1 Conversation reset; 2.2 Fail to ask for clarification; 2.3 Task derailment; 2.4 Information withholding; 2.5 Ignored other agent's input; 2.6 Action–reasoning mismatch.
  - Task verification: 3.1 Premature termination; 3.2 No or incorrect verification; 3.3 Weak verification.
  - Each mode is tagged Pre, Exec or Post stage. The dataset has 1K+ annotated traces, and there is an LLM-judge annotator.
  - Sources: [agentdash PyPI (mode table)](https://pypi.org/project/agentdash/); [MAST README](https://raw.githubusercontent.com/multi-agent-systems-failure-taxonomy/MAST/main/README.md)
- **TRAIL** (May 2025): trace errors in reasoning, execution and planning categories; 841 errors across 148 traces; best model 11%. — [TRAIL README](https://raw.githubusercontent.com/patronus-ai/trail-benchmark/main/README.md)
- **AgentErrorTaxonomy** (Sept 2025): 17 error types across 5 modules (memory, reflection, planning, action, system). — [AgentDebug README](https://raw.githubusercontent.com/ulab-uiuc/AgentDebug/main/README.md)
- **ImpossibleBench** (safety-research, arXiv 2510.20270, Oct 2025) measures "agents' propensity to exploit test cases" using impossible task variants, where passing "necessarily implies specification-violating shortcuts or 'cheating'". Variants cover LiveCodeBench and SWE-bench, implemented in Inspect AI. — [README](https://raw.githubusercontent.com/safety-research/impossiblebench/main/README.md)
- **Premature completion** (Anthropic, 2025-11-26): "Claude's tendency to mark a feature as complete without proper testing… would fail [to] recognize that the feature didn't work end-to-end". The mitigation was a feature list in which every item is initially marked "failing", plus explicit end-to-end testing. — [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- **A weak verifier means the wrong problem gets solved** (2026-02-05): "the task verifier [must be] nearly perfect, otherwise Claude will solve the wrong problem". The same post describes two further anti-patterns:
  - **Time blindness**: Claude "will happily spend hours running tests". The harness answers with a `--fast` 1–10% sample.
  - **Context pollution**: the harness keeps its output sparse and writes grep-able ERROR lines.
  - Source: [Building a C compiler](https://www.anthropic.com/engineering/building-c-compiler)
- **Multi-agent specific** (2025-06-13): spawning 50 subagents for simple queries, endless searching, agents distracting each other, continuing after sufficient results. — [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- **Self-evaluation leniency** (2026-03-24): "agents reliably skew positive when grading their own work". — [Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- **Loops as a named class**: Gemini CLI's loop types are consecutive identical tool calls, content "chanting", and LLM-detected loops. — [loopDetectionService.ts](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/packages/core/src/services/loopDetectionService.ts)
- **Token economics** [V]:
  - "Token usage by itself explains 80% of the variance" in BrowseComp performance, with tool-call count and model choice as the other factors (95% together).
  - Agents use about 4× the tokens of chat, and multi-agent systems about 15×.
  - Source: [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- **Waste drivers named by the vendor** for Claude Code [V]: long never-cleared sessions, cache misses after idle periods beyond the TTL, scheduled tasks and idle check-ins resending full context, agent teammates (about 7× tokens in plan mode), large MCP and tool listings, broad vague prompts that trigger scanning, and the always-on cost of plugin and skill descriptions. — [Manage costs](https://code.claude.com/docs/en/costs); [Measure plugins](https://code.claude.com/docs/en/plugins/measure)
- **Instruction-level regression** (2026-04-23) [V]: one system-prompt line ("Keep final responses to ≤100 words…"), added to cut Opus 4.7's verbosity, passed "multiple weeks of internal testing and no regressions in the set of evaluations we ran". Line-by-line ablations on a broader eval set then showed a **3% drop** for Opus 4.6 and 4.7, and the line was reverted. — [Postmortem](https://www.anthropic.com/engineering/april-23-postmortem)

### Inferences
- **[I] Mapping baseline incident classes to MAST gives a shared vocabulary and makes recurrence countable:**
  - "the executor misunderstood" → 1.1 Disobey task specification;
  - "spec vs reality mismatch, the executor improvised" → 2.2 Fail to ask for clarification (the baseline already prescribes STOP);
  - "lost report / only an idle notification" → 2.4 Information withholding, or an infrastructure class;
  - "empty prompt at spawn" → 2.1 Conversation reset (infrastructure);
  - "verifier passed broken work" → 3.2 / 3.3;
  - "executor declared done without running the DoD" → 3.1 / 1.5;
  - "worker hung on Glob" → 1.3 Step repetition, or a tool/infrastructure class;
  - "scout returned judgement" → 1.2 Disobey role specification.
- **[I] Infrastructure classes need their own bucket.** Session-limit death, empty spawn prompts, Codex network sandboxing and grok Glob hangs are harness or infrastructure faults, not model reasoning faults. MAST is not designed for them, and mixing them in inflates the "model" failure rate.
- **[I] Probe the Codex verifier for test-gaming.** Because the baseline trusts a Codex verifier that *runs* DoD checks, ImpossibleBench-style probing is relevant. Occasionally seed tasks whose DoD cannot honestly pass and confirm the verifier returns ✖ or "unverifiable", not ✔.

### Gaps
- Several SWE-agent and OpenHands trajectory-failure studies could not be verified: the reasoning–action "overthinking" dilemma study (Feb 2025), empirical studies of success and failure trajectories on SWE-bench, "Are 'Solved Issues' in SWE-bench Really Solved Correctly?", and process-oriented error analyses of software agents. arXiv and search were unavailable. Their titles are from memory and must be checked before citing.
- Efficiency-aware benchmarks and token-waste analyses (for example SWE-Effi, "Tokenomics"-style analyses of where tokens go in agentic software engineering, OPPO's "Efficient Agents", "Cost-of-Pass") are not verified. I found no primary data here on the share of coding-agent tokens spent re-reading files.
- MAST follow-ups (NeurIPS version, kappa, frameworks covered) are not verified.

## 4. Evals and regression tests for agent configurations (prompts, skills, AGENTS.md / CLAUDE.md)

### Takeaway
There is now first-party, CI-ready tooling for exactly the user's question ("did this skill or instruction change make things better?"). The key habits: run each golden task 3+ times, compare against a baseline arm (no skill or old skill), track cost and time alongside pass rate, pin the models, and never trust a green that hasn't been ablated.
- **`claude plugin eval`** (Claude Code v2.1.269, 2026-09-11) runs a plugin's cases 3× each, with and without the plugin, and reports Δ, cost and duration.
- **skill-creator** runs with-skill vs baseline (or old-skill snapshot) benchmarks with tokens and time (mean ± stddev), a blind A/B and description-trigger tuning.

For the *hands* (Codex, Grok, Gemini), the neutral harnesses are Harbor (the Terminal-Bench 2.0 harness), Inspect AI + inspect_swe (`claude_code()`, `codex_cli()`, `gemini_cli()` agents), promptfoo (Claude Agent SDK and Codex SDK providers with trajectory and cost assertions) and `@vercel/agent-eval` (A/B "does this doc or config help agents?" with transcript metrics).

### Cited Findings
- **Anthropic, "Demystifying evals for AI agents"** (2026-01-09; Grace, Hadfield, Olivares, De Jonghe) [V]:
  - Graders are code-based, model-based or human. Capability evals start at a low pass rate; regression evals "should have a nearly 100% pass rate".
  - "20-50 simple tasks drawn from real failures is a great start." A good task is one "where two domain experts would independently reach the same pass/fail verdict". Use reference solutions, balanced sets, isolated clean environments, and "grade what the agent produced, not the path it took".
  - "You won't know if your graders are working well unless you read the transcripts."
  - Transcript metrics: `n_turns`, `n_toolcalls`, `n_total_tokens` and latency.
  - Grader bugs they cite: CORE-Bench, where Opus 4.5 initially scored 42% due to rigid grading and ambiguous specs; and a τ2-bench case where Opus 4.5 "failed" by finding a better policy loophole.
  - Tools mentioned: Harbor, Braintrust, LangSmith, Langfuse and Arize Phoenix.
  - Source: [Demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- **pass@k vs pass^k** [V]:
  - pass@k is the probability that at least one of k trials succeeds; pass^k is the probability that all k succeed. Example: a 75% per-trial rate gives (0.75)³ ≈ 42% pass^3. "pass@k approaches 100% while pass^k falls to 0%." — [Demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
  - Origin and data: τ-bench (Sierra, 2024, background). Airline, claude-3-5-sonnet-20241022: pass^1 0.460 → pass^4 0.225. Retail: 0.692 → 0.462. — [τ-bench README](https://raw.githubusercontent.com/sierra-research/tau-bench/main/README.md)
- **`claude plugin eval`** (new, [V]):
  - Availability: added in v2.1.269 (npm 2026-09-11). The docs still carry "early access" and "switched off server-side" troubleshooting entries. — [CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md); [Plugin evals](https://code.claude.com/docs/en/plugin-evals)
  - Setup: cases live under `evals/`, and `claude plugin eval init` drafts them. Each run is a fresh, isolated `-p` session with only the plugin loaded.
  - Scoring: a run scores the fraction of its graders that passed; a case scores the mean over runs, **3 runs by default**. The **no-plugin baseline arm** gives WITH, W/OUT and **Δ**. Skill-invocation graders are excluded from the score so Δ is not inflated.
  - Graders:
    - `regex` over the last message, the trace, the list of files created, a file's contents, or mock calls;
    - `tool_used` with `input_match`, `min` and `max` (for example `min:0 max:0` for "never called");
    - `tool_order`;
    - `file_exists`;
    - `llm`: 2 of 3 judge votes; sees only the first 12 and last 12 trace messages;
    - `baseline`: judges the run against a **reference transcript `.jsonl`**.
  - CI use:
    - Flags: `--runs`, `--threshold` (exit code 1 below it), `--max-cost-usd` (exit code 2 on a partial run), and `--model` / `--judge-model` pinned so "a model rollout isn't mistaken for a plugin regression".
    - Output: `--json` gives `schemaVersion: 1` with `aggregates.overallScore`, `meanDelta`, per-case `delta`, `costUsd`, `durationSeconds` and `claudeVersion`.
    - Also: MCP mocks with record/replay.
  - Source: [Plugin evals](https://code.claude.com/docs/en/plugin-evals)
- **skill-creator** (Anthropic; `anthropics/skills` and the official plugin) [V]:
  - Setup: 2–3 realistic prompts stored in `evals/evals.json`. With-skill and baseline subagents are spawned in the same turn; the baseline is no skill for a new skill, or a **snapshot of the old skill** when improving one.
  - Capture and grading: `total_tokens` and `duration_ms` are recorded per run. Grading goes to `grading.json` with `passed` and `evidence`.
  - Aggregation: `benchmark.json` with pass rate, time and tokens (mean ± stddev, and delta). An analyst pass flags non-discriminating assertions, flaky high-variance evals and time/token trade-offs.
  - Comparison and triggering: a blind comparator for version A/B; a description optimiser using 20 should/shouldn't-trigger queries, a 60/40 train/test split, 3 runs per query and up to 5 iterations.
  - Improvement guidance: "read the transcripts, not just the final outputs"; if every test run writes the same helper script, bundle it into the skill.
  - Sources: [skill-creator SKILL.md](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md); [Skills docs](https://code.claude.com/docs/en/skills)
- **promptfoo** (MIT; npm since 2023; 0.123.1 on 2026-09-18; 423 versions) [V]:
  - Claude Agent SDK provider: `working_dir`, `setting_sources` (to load CLAUDE.md and skills), `plugins`, `max_budget_usd`. Assertions include `skill-used`, JS assertions over `metadata.toolCalls`, and `trace-span-count` on `gen_ai.turn *` spans (for example "≤3 LLM round-trips"). It propagates `TRACEPARENT` to the SDK subprocess.
  - Codex SDK provider: final text, `tokenUsage` and estimated cost, thread IDs, traced shell/MCP/file steps. `skill-used` for Codex is a *heuristic* based on reads of `SKILL.md` files.
  - Deterministic assertions include `cost`, `latency`, `tool-call-f1`, `trajectory:tool-used`, `trajectory:tool-args-match`, `trajectory:tool-sequence`, `trajectory:step-count` and `trace-error-spans`.
  - Sources: [Claude Agent SDK provider](https://raw.githubusercontent.com/promptfoo/promptfoo/main/site/docs/providers/claude-agent-sdk.md); [Codex SDK provider](https://raw.githubusercontent.com/promptfoo/promptfoo/main/site/docs/providers/openai-codex-sdk.md); [assertions](https://raw.githubusercontent.com/promptfoo/promptfoo/main/site/docs/configuration/expected-outputs/deterministic.md); [npm](https://registry.npmjs.org/promptfoo)
- **Inspect AI** (UK AISI; PyPI since 2024-04; 0.3.268 on 2026-09-22; 246 releases) and **inspect_swe** (Meridian Labs; PyPI since 2025-08-30; 0.2.71 on 2026-09-17) [V]. inspect_swe exports agent solvers `claude_code`, `codex_cli`, `gemini_cli`, `opencode`, `kimi_code`, `antigravity` and `mini_swe_agent`, plus interactive ACP variants. The real CLIs can therefore be evaluated inside Inspect's sandboxed tasks and scorers. — [inspect_swe `__init__.py`](https://raw.githubusercontent.com/meridianlabs-ai/inspect_swe/main/src/inspect_swe/__init__.py); [PyPI inspect-ai](https://pypi.org/pypi/inspect-ai/json); [PyPI inspect-swe](https://pypi.org/pypi/inspect-swe/json)
- **Harbor** ("from the creators of Terminal-Bench"; PyPI since 2025-11-02; 0.23.0 on 2026-09-24; 158 releases) [V]:
  - Evaluates "arbitrary agents like Claude Code, OpenHands, Codex CLI". You can build custom benchmarks and environments and run thousands in parallel on Daytona, Modal and others.
  - It is the official harness for Terminal-Bench 2.0 (`harbor run --dataset terminal-bench@2.0 --agent claude-code`).
  - The old `terminal-bench` harness (last PyPI 2025-09-26) points new users to Harbor.
  - Sources: [Harbor README](https://raw.githubusercontent.com/laude-institute/harbor/main/README.md); [Terminal-Bench README](https://raw.githubusercontent.com/laude-institute/terminal-bench/main/README.md); [PyPI](https://pypi.org/pypi/harbor/json)
- **`@vercel/agent-eval`** (Vercel Labs; npm since 2026-01-29; 2.3.0 on 2026-09-18) [V]:
  - Built to answer "Your documentation helps agents write correct code? Adding an MCP server improves agent success rates? … Your latest API changes broke agent compatibility?"
  - Runs controlled experiments with result reuse by fingerprint, `--dry` (no cost) and `--smoke` modes. Supports `claude-code`, `codex`, `gemini` and `opencode`.
  - Asserts on files and on the transcript summary (`totalToolCalls`, `totalTurns`, `errors`, `filesRead`), and uses an agentic transcript judge.
  - Used for Next.js agent evals with withheld assertions.
  - Sources: [README](https://raw.githubusercontent.com/vercel-labs/agent-eval/main/README.md); [npm](https://registry.npmjs.org/@vercel/agent-eval); [next-evals-oss](https://raw.githubusercontent.com/vercel/next-evals-oss/main/README.md)
- **Environment noise** (Anthropic, 2026-02-05) [V]: infrastructure configuration alone moved Terminal-Bench 2.0 scores by 6 percentage points between the most- and least-resourced setups (p < 0.01). That is "sometimes more than the leaderboard gap between top models". — [Quantifying infrastructure noise](https://www.anthropic.com/engineering/infrastructure-noise)
- **How Anthropic now gates instruction changes** (2026-04-23) [V]: "run a broad suite of per-model evals for every system prompt change… continuing ablations to understand the impact of each line", new tooling to review and audit prompt changes, CLAUDE.md guidance to gate model-specific changes to their model, and "soak periods, a broader eval suite, and gradual rollouts". — [Postmortem](https://www.anthropic.com/engineering/april-23-postmortem)
- **Starting small** [V]: early on, "a prompt tweak might boost success rates from 30% to 80%", and about 20 real queries were enough to see changes. — [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- **Cost-aware scoring** [V]:
  - HAL argues "What does it mean if an agent has 1% higher accuracy… but is 10x more expensive?" and uses cost-controlled evaluations with cost/accuracy trade-offs, building on "AI Agents That Matter" (arXiv 2407.01502, 2024, background). — [HAL README](https://raw.githubusercontent.com/princeton-pli/hal-harness/main/README.md)
  - `claude plugin eval` reports `costUsd` per suite, and skill-creator reports the token and time overhead of a skill against its pass-rate gain. — [Plugin evals](https://code.claude.com/docs/en/plugin-evals); [Skills docs](https://code.claude.com/docs/en/skills)
- **Automated instruction optimisers** that close the loop from failures to text edits (no fine-tuning) [V]. These are optimisation levers covered by other researchers; listed only as loop closers.
  - **GEPA**: reflective, Pareto evolutionary search over any text artifact. "100–500 evaluations vs. 5,000–25,000+ for GRPO"; the authors claim "55% → 82% coding agent resolve rate on Jinja via auto-learned skills". — [GEPA README](https://raw.githubusercontent.com/gepa-ai/gepa/main/README.md)
  - **ACE**: evolving "playbooks" from execution feedback without labels; +10.6% on AppWorld agent tasks (arXiv 2510.04618). — [ACE README](https://raw.githubusercontent.com/ace-agent/ace/main/README.md)
  - **Arize prompt-learning**: an agent → LLM evaluator writes textual feedback → a meta-prompt revises the instructions. — [prompt-learning README](https://raw.githubusercontent.com/Arize-ai/prompt-learning/main/README.md)

### Inferences
- **[I] The repo can adopt `claude plugin eval` directly.** The repo is already a Claude Code plugin marketplace; its CLAUDE.md release checklist runs `claude plugin validate`. So `claude plugin eval` fits as a new release-checklist step. A skill edit gets a PR-time A/B: with the new skill, without it, or against the previous release via skill-creator's old-skill snapshot.
- **[I] Limitation for the orchestration skill.** `fable-ruki-agenty` is user-invoked (`disable-model-invocation: true`) and its value shows up only across a *multi-agent pipeline*. `claude plugin eval` checks one Claude session with mocks. It can test Fable's *orchestrator behaviour*, and these properties are testable with `tool_used`/`regex` graders plus Codex/Orca calls mocked as MCP tools or recorded outputs:
  - the spec contains all sections and no "вероятно" (probably);
  - Fable never calls Bash;
  - it dispatches by pointer;
  - it never writes "closes #N".
- **[I] Evaluating the hands needs a neutral harness.** Harbor or inspect_swe (`codex_cli`) with golden tasks rebuilt from real closed issues: a repo snapshot at the start SHA, the issue body as the spec, the DoD command as the verifier. `@vercel/agent-eval` adds transcript assertions such as "never ran `find`/Glob", "≤N tool calls" and "didn't read files outside the paths in the spec".
- **[I] Suggested gate for a skill edit.** Take the golden suite, 20–50 tasks drawn from past incidents per Anthropic's guidance; the "Rigor Pack" A/B the baseline cites used only 2–3 tasks per skill, which is the signal level the baseline itself admits. Plus a regression suite, near 100% by definition, made of one task per previously fixed incident class. Run k≥3 trials per arm with models, effort and environment pinned. Report:
  - pass@1;
  - **pass^3** (reliability, which the ladder hides because it retries);
  - mean and stddev of tokens, $ and wall time per *accepted* task;
  - Δ vs the old skill.
  Accept only if regression pass^k does not drop and cost per accepted task does not rise beyond a set tolerance.
- **[I] Line ablation.** The April postmortem shows why "no regressions on our evals" is weak evidence when the eval set is narrow. For long skills like `fable-ruki-agenty`, a line ablation (remove one rule, rerun) at least identifies dead rules that cost tokens without changing outcomes.

### Gaps
- No independent, dated evidence found on how *reliable* `claude plugin eval` Δ is (variance across the 3 default runs), or on community adoption. The command is two weeks old.
- AGENTS.md / CLAUDE.md effectiveness studies could not be verified: a 2026 ETH-style study reportedly found LLM-generated context files reduce success and raise cost; Vercel's January 2026 "AGENTS.md vs skills" eval; OpenAI's "testing agent skills with evals" post on `codex exec --json` traces. Search and the vendor blogs were unavailable. Treat them as leads only.
- Inspect AI's `epochs` and `pass_at_k` reducers were not verified in docs this session.
- No verified source on "eval awareness" effects for golden-task replay. Anthropic has a 2026-03-06 post on eval awareness in BrowseComp that I did not read.

## 5. Per-task metrics practitioners track, and how they close the loop

### Takeaway
Verified practitioner metric sets converge on the following:
- **outcome**: pass/fail per grader, and a reliability measure over k trials;
- **efficiency**: turns, tool calls, total and cache tokens, latency/TTFT, wall time, $ estimate;
- **errors**: tool errors, retries, refusals, denied or declined actions;
- **human load**: permission prompts or blocks, feedback.

Metrics specific to an orchestrator are not provided by any tool and must come from the journal: rework loops, verifier failure rate, fresh-executor escalations, blocked rate, and recurrence of an incident class after a fix. The verified loop-closing practice from Anthropic has four steps: read transcripts → name the failure mode → encode it as a test or grader → change the prompt, tool or skill → re-run broad evals with ablations, then soak and roll out gradually. What almost nobody publishes is a measured drop in recurrence; that remains the baseline's biggest opportunity.

### Cited Findings
- **Anthropic tool evals** [V]: beyond accuracy, "total runtime of individual tool calls and tasks, the total number of tool calls, the total token consumption, and tool errors". — [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- **Anthropic eval guidance** [V]: `n_turns`, `n_toolcalls`, `n_total_tokens`, time to first token, output tokens/sec, time to last token; pass@k and pass^k. — [Demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- **Claude Code telemetry** [V]:
  - Cost and tokens by type, model, subagent, skill and plugin.
  - Active time (user vs CLI).
  - Tool success, duration and size; API retries (`attempt`) and errors; refusals.
  - Permission decisions: `tool_decision` / `code_edit_tool.decision` sources, including `user_reject` / `user_abort`, and the duration of `tool.blocked_on_user` spans. These are a direct proxy for **human interventions**.
  - Lines, commits and PRs.
  - Source: [Monitoring](https://code.claude.com/docs/en/monitoring-usage)
- **Codex telemetry** [V]: per-turn estimated cost and `turn.interrupted` (`codex.turn_cost`), TTFT (`codex.turn_ttft`), sandbox outcome, tool decisions, and per-turn usage with reasoning tokens (`turn.completed`). — [session_telemetry.rs](https://raw.githubusercontent.com/openai/codex/main/codex-rs/otel/src/events/session_telemetry.rs); [exec_events.rs](https://raw.githubusercontent.com/openai/codex/main/codex-rs/exec/src/exec_events.rs)
- **Eval-harness per-run metrics** [V]:
  - `claude plugin eval`: per-case score, Δ vs baseline, "perfect runs" share, `costUsd` and `durationSeconds`. — [Plugin evals](https://code.claude.com/docs/en/plugin-evals)
  - skill-creator: pass rate, time and tokens as mean ± stddev. — [SKILL.md](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md)
  - agent-eval: `totalTurns`, `totalToolCalls`, `errors`, and shell commands with exit codes. — [agent-eval](https://raw.githubusercontent.com/vercel-labs/agent-eval/main/README.md)
- **Closing the loop, examples** [V]:
  - (a) Watch transcripts → prompt changes. Early wins can be large (30% → 80%). — [Multi-agent research](https://www.anthropic.com/engineering/multi-agent-research-system)
  - (b) Observed failure mode → new tests in the harness. — [C compiler](https://www.anthropic.com/engineering/building-c-compiler)
  - (c) Metric anomaly → tool description fix (redundant calls, invalid params, the "2025" query suffix). — [Writing tools](https://www.anthropic.com/engineering/writing-tools-for-agents)
  - (d) User feedback → line ablations → revert. After the April 2026 postmortem, the process became per-model evals for every prompt change, soak periods and gradual rollouts. — [Postmortem](https://www.anthropic.com/engineering/april-23-postmortem)
  - (e) `/insights` friction analysis → suggested CLAUDE.md rules. [S] for the rule suggestions — [Vincent Qiao](https://blog.vincentqiao.com/en/posts/claude-code-insights/); feature [V] — [Manage costs](https://code.claude.com/docs/en/costs)
  - (f) skill-creator iteration loop: rerun into `iteration-N+1`, compare with the previous workspace, and stop when feedback is empty or progress stalls. — [SKILL.md](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md)
- **Separate evaluator** [V]: a standalone skeptical evaluator is "far more tractable than making a generator critical of its own work". — [Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps)

### Inferences
- **[I] Per-task record to append to each issue journal.** The forwarder already posts one comment per phase; this is a small change. Store the raw data privately and post only sanitised numbers in the public repo.
  - Identity: `issue`, `pipeline_id`, `executor` (codex / grok / claude), `executor_session_id`, `model`, `effort`.
  - Per phase: tokens in, out, cache-read and cache-write; $ estimate; wall time and API time; turns; tool calls; failed or declined commands; max context %.
  - Outcome fields: `rework_idx` (0/1/2), `fresh_executor` (bool), `verifier_verdict` per DoD item (pass / fail / unverifiable), `spec_defect` (bool: rework caused by spec vs reality).
  - Orchestrator share: `fable_tokens_for_issue`.
- **[I] Pipeline KPIs to review weekly, next to the incidents:**
  - first-pass acceptance rate (closed with `rework_idx = 0`);
  - average reworks per task;
  - escalation rate (fresh executor) and blocked rate;
  - verifier ✖ rate and "unverifiable" rate;
  - cost and wall time per *accepted* task, including reworks and verification;
  - Fable token share of the total (the baseline's own stated goal);
  - spec-defect rate (a quality metric for Fable's specs);
  - hands-level waste: failed-command share, repeated identical commands, bytes read per task.
- **[I] Recurrence check, closing the known gap.** Tag each `incidents.md` entry with a class (MAST ID or local infrastructure class), a timestamp and a pipeline id. When a skill edit lands (commit SHA), record `fix_sha` on the class. Recurrence is incidents of that class per 10 pipelines (or per 100 dispatches) in a fixed window before vs after `fix_sha`. Close the class only after N clean pipelines, for example 10; otherwise reopen it and mark the fix "ineffective". Because incidents are rare, report counts with exposure (dispatches), not just "0 since fix". A class with a golden task gets an automated regression check too.
- **[I] A feasible loop, in order of cost:**
  1. `ccusage session --json` plus a journal parser (a few hours of work; no infrastructure).
  2. A weekly outlier pack: top-cost, rework or blocked tasks, with Codex/Grok transcripts rendered through claude-code-log's Markdown `--detail low` mode. An independent-model judge produces MAST-labelled candidates, and the human retro confirms.
  3. Golden and regression suites from real issues, run through Harbor or inspect_swe for hands and `claude plugin eval` / skill-creator for Fable's skill, gating every skill edit.
  4. Optionally, OTel to a self-hosted Langfuse, Phoenix or SigNoz for live dashboards, using `prompt.id` / `agent_id` for per-dispatch drill-down.
- **[I] Mapping to the "head and hands" design.**
  - The baseline's separate verifier already implements the "separate evaluator" lever, but only at *task* level.
  - At *system* level (which rules to change), the orchestrator still grades itself. The judge pass, human confirmation and recurrence KPI above move that grading outside Fable.
  - The acceptance ladder is effectively "pass@3 with feedback", so pass rate alone overstates reliability. Tracking first-pass acceptance (≈ pass@1) and golden-suite pass^k exposes it.

### Gaps
- Found no published, dated case where a team measured incident-class recurrence before and after an instruction fix in a CLI-agent pipeline. The recurrence method above is an inference.
- Found no primary-source benchmark of "human interventions per task" for CLI agents beyond Claude Code's permission-decision telemetry.
- Practitioner metric sets from Codex-centred teams (for example OpenAI's "harness engineering" post) and Cursor, Factory, Sourcegraph and others could not be verified (openai.com and search were unavailable).
