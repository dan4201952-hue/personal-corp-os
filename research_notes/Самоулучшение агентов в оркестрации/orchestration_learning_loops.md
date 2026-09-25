# Learning / retrospective loops in orchestrator → CLI-agent systems (research notes, as of 2026-09-25)

Verification tags used on every finding: **[V]** = verified this session in a primary source that was fetched and read (repo file via raw.githubusercontent.com, npm/PyPI registry metadata, anthropic.com or code.claude.com); **[S]** = seen only in a WebSearch result snippet or title (the page itself could not be fetched because of the egress policy); **[B]** = background knowledge that could not be verified this session (these appear only in Gaps). Dates are publication or release dates. Anything published before 2025 is labelled as background. Note for the report writer: the shared WebSearch budget ran out partway through, so Every's articles, Yegge's Medium posts, OpenAI's harness-engineering post, Factory, Cognition/Devin, Manus and Conductor could only be covered through snippets, or not at all. Repo files and official docs were read directly wherever that was possible.

User baseline for comparison ("fable-ruki-agenty", local file `skills/fable-ruki-agenty/SKILL.md`, § "Журнал сбоев (self-improvement loop)", lines 222–235): the orchestrator (Fable) records every pipeline misfire in a private `incidents.md` (misunderstood spec, empty prompt, lost report, agent death, hung worker, verifier failure, spec/reality mismatch, missing commit). It reviews the journal at each pipeline start. When 2+ open entries of one class exist, it makes an issue-first skill edit and closes the entries with the commit. New observations stay in the journal until they are established, and only then move into the skill text. The ladder is: rework 1 and 2 by the same executor → fresh executor → `blocked` (SKILL.md lines 196–207). The forwarder journal posts ▶ dispatch / ↩ executor report / ✔✖ verifier / 🔁 rework N / ⛔ blocked as issue comments (lines 215–218).

---

## 1. Ralph loop family: Huntley's original, Anthropic's ralph-wiggum / ralph-loop plugin, snarktank/ralph and similar variants. What does each iteration write, how are learnings accumulated and pruned, and what results and costs are reported?

### Takeaway
Ralph is a worker-side learning loop. A dumb outer loop (bash or a Stop hook) re-feeds the same prompt to a fresh CLI-agent context. The only memory is files and git: a plan/progress file, plus an `AGENTS.md` that the agent itself is told to update with operational learnings. The human "sits on the loop" and adds "signs" (guardrails) whenever Ralph fails in a specific way. Pruning is manual or prompt-driven: keep AGENTS.md operational and brief, clean the plan, throw the plan away and regenerate it. Anthropic's plugin variant has no learning store at all. Reported results are anecdotal and self-reported, with no controlled comparisons.

### Cited Findings

**1a. Huntley's original technique and the "Ralph Playbook"**
- Name/URLs: "Ralph Wiggum as a 'software engineer'", [ghuntley.com/ralph](https://ghuntley.com/ralph/) [S]. Repo [ghuntley/how-to-ralph-wiggum](https://github.com/ghuntley/how-to-ralph-wiggum), described as "the AI development methodology that reduces software costs to less than a fast food worker's wage" [S].
- Date: LinearB says the technique was "first described in May 2025" [(LinearB)](https://linearb.io/blog/ralph-loop-agentic-engineering-geoffrey-huntley) [S]. The Playbook says "December 2025 boiled Ralph's … face to the top of most AI-related timelines" [(Playbook)](https://raw.githubusercontent.com/ghuntley/how-to-ralph-wiggum/main/README.md) [V]. The Playbook cites X posts by Matt Pocock and Ryan Carson and Huntley's "nah" reply. Decoded from their status IDs, these date to 2026-01-05, 2026-01-06 and 2026-01-07 [V: derived from snowflake IDs in the Playbook links].
- Authorship caveat: the Playbook in Huntley's repo was written by Clayton Farr, who says he "dug in to really RTFM on recent videos and Geoff's original post". It is a secondary synthesis hosted in Huntley's repo [(Playbook)](https://raw.githubusercontent.com/ghuntley/how-to-ralph-wiggum/main/README.md) [V].
- Structure: "3 phases, 2 prompts, 1 loop". PLANNING does gap analysis and writes a prioritized TODO list. BUILDING implements, tests and commits [(LinearB)](https://linearb.io/blog/ralph-loop-agentic-engineering-geoffrey-huntley) [S]; confirmed in [Playbook](https://raw.githubusercontent.com/ghuntley/how-to-ralph-wiggum/main/README.md) [V].
- What each iteration loads: `PROMPT.md` + `AGENTS.md`, plus `specs/*` and `IMPLEMENTATION_PLAN.md` from disk. The plan file is the shared state between otherwise isolated iterations [(Playbook)](https://raw.githubusercontent.com/ghuntley/how-to-ralph-wiggum/main/README.md) [V].
- What each iteration writes: step 7 is "Update IMPLEMENTATION_PLAN.md – mark task done, note discoveries/bugs", and step 8 is "Update AGENTS.md – if operational learnings" [(Playbook)](https://raw.githubusercontent.com/ghuntley/how-to-ralph-wiggum/main/README.md) [V].
- Worker-side inefficiency trigger, quoted from the building prompt: "When you learn something new about how to run the application, update @AGENTS.md using a subagent but keep it brief. For example if you run commands multiple times before learning the correct command then that file should be updated." [(Playbook)](https://raw.githubusercontent.com/ghuntley/how-to-ralph-wiggum/main/README.md) [V].
- "For any bugs you notice, resolve them or document them in @IMPLEMENTATION_PLAN.md … even if it is unrelated to the current piece of work." This is a "noticed, didn't touch" analogue [(Playbook)](https://raw.githubusercontent.com/ghuntley/how-to-ralph-wiggum/main/README.md) [V].
- Pruning and anti-bloat rules in the prompt:
  - "When @IMPLEMENTATION_PLAN.md becomes large periodically clean out the items that are completed."
  - "IMPORTANT: Keep @AGENTS.md operational only — status updates and progress notes belong in IMPLEMENTATION_PLAN.md. A bloated AGENTS.md pollutes every future loop's context."
  - Source: [(Playbook)](https://raw.githubusercontent.com/ghuntley/how-to-ralph-wiggum/main/README.md) [V].
- The plan is disposable. "Regeneration cost is one Planning loop; cheap compared to Ralph going in circles." Regenerate when Ralph goes off track, the plan feels stale, there is too much clutter, or specs change. Geoff: "I have deleted the TODO list multiple times" [(Playbook)](https://raw.githubusercontent.com/ghuntley/how-to-ralph-wiggum/main/README.md) [V].
- Who writes the post-mortem: the human operator. "Observe and course correct … What signs does he need? The prompts you start with won't be the prompts you end with — they evolve through observed failure patterns. Tune it like a guitar … When Ralph fails a specific way, add a sign to help him next time." Signs can be prompt guardrails, AGENTS.md, or code utilities Ralph discovers [(Playbook)](https://raw.githubusercontent.com/ghuntley/how-to-ralph-wiggum/main/README.md) [V]. Huntley on the official plugin: "if you just set it off and run away, you're not going to get a great outcome. You really want to babysit this thing." [(Dev Interrupted / LinearB)](https://linearb.io/dev-interrupted/podcast/inventing-the-ralph-wiggum-loop) [S].
- "Backpressure" is the verification mechanism: tests, typechecks and lints reject bad work. AGENTS.md holds the project-specific commands, so "the BUILDING prompt says 'run tests' generically; AGENTS.md specifies the actual commands". Optional LLM-as-judge tests give binary pass/fail on subjective criteria [(Playbook)](https://raw.githubusercontent.com/ghuntley/how-to-ralph-wiggum/main/README.md) [V].
- Context tactics: "up to 500 parallel Sonnet subagents for searches/reads and only 1 Sonnet subagent for build/tests", and "Each subagent gets ~156kb that's garbage collected" [(Playbook)](https://raw.githubusercontent.com/ghuntley/how-to-ralph-wiggum/main/README.md) [V].

**1b. Anthropic's plugin: `ralph-wiggum` in anthropics/claude-code, renamed `ralph-loop` in claude-plugins-official**
- Mechanism: a Stop hook blocks exit and feeds the same prompt back. "The prompt never changes between iterations. Claude's previous work persists in files." Commands are `/ralph-loop "<prompt>" --max-iterations <n> --completion-promise "<text>"` and `/cancel-ralph`. `--max-iterations` defaults to unlimited. The completion promise is an exact string match, so it "cannot use it for multiple completion conditions (like 'SUCCESS' vs 'BLOCKED')" [(plugin README)](https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/ralph-wiggum/README.md) [V].
- Learning store: none. Recommended escape hatch: "After 15 iterations, if not complete: Document what's blocking progress, List what was attempted, Suggest alternative approaches" [(plugin README)](https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/ralph-wiggum/README.md) [V].
- Stated results, all self-reported: "Successfully generated 6 repositories overnight in Y Combinator hackathon testing; One $50k contract completed for $297 in API costs; Created entire programming language ('cursed') over 3 months" [(plugin README)](https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/ralph-wiggum/README.md) [V].
- Rename: the official marketplace copy is titled "Ralph Loop Plugin" and says it is "inspired by the Ralph Wiggum coding technique". Its cache path is still `claude-plugins-official/ralph-wiggum/<hash>`, and it adds a Windows Git-Bash workaround [(ralph-loop README)](https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/plugins/ralph-loop/README.md) [V]. The date the plugin was first added was not verified.

**1c. snarktank/ralph (Ryan Carson)**
- What it is: "an autonomous AI agent loop that runs AI coding tools (Amp or Claude Code) repeatedly until all PRD items are complete. Each iteration is a fresh instance with clean context. Memory persists via git history, `progress.txt`, and `prd.json`." It links Carson's X article, dated 2026-01-06 via its status ID [(README)](https://raw.githubusercontent.com/snarktank/ralph/main/README.md) [V].
- Per-iteration flow: pick the highest-priority story with `passes: false`, implement, run quality checks, commit if they pass, set `passes: true`, "Append learnings to progress.txt", and update AGENTS.md. Default 10 iterations. Stop condition is `<promise>COMPLETE</promise>` [(README)](https://raw.githubusercontent.com/snarktank/ralph/main/README.md) [V].
- Exact progress entry format, appended and never replaced: `## [Date/Time] - [Story ID]`, `Thread: https://ampcode.com/threads/$AMP_CURRENT_THREAD_ID`, what was implemented, files changed, "Learnings for future iterations" (patterns, gotchas, useful context). The thread URL is included "so future iterations can use the read_thread tool" [(prompt.md)](https://raw.githubusercontent.com/snarktank/ralph/main/prompt.md) [V].
- Consolidation: "If you discover a reusable pattern … add it to the `## Codebase Patterns` section at the TOP of progress.txt … Only add patterns that are general and reusable, not story-specific details." Each iteration reads that section first [(prompt.md)](https://raw.githubusercontent.com/snarktank/ralph/main/prompt.md) [V].
- AGENTS.md rules: before committing, find directories with edited files, check for an AGENTS.md nearby, and add genuinely reusable knowledge (e.g. "When modifying X, also update Y", "Tests require the dev server running on PORT 3000"). "Do NOT add: Story-specific implementation details, Temporary debugging notes, Information already in progress.txt" [(prompt.md)](https://raw.githubusercontent.com/snarktank/ralph/main/prompt.md) [V]. The README explains why: "AI coding tools automatically read these files, so future iterations (and future human developers) benefit" [(README)](https://raw.githubusercontent.com/snarktank/ralph/main/README.md) [V].
- Pruning: previous runs are archived to `archive/YYYY-MM-DD-feature-name/` when a new `branchName` starts [(README)](https://raw.githubusercontent.com/snarktank/ralph/main/README.md) [V]. The script resets the progress file for a new run [(ralph.sh)](https://raw.githubusercontent.com/snarktank/ralph/main/ralph.sh) [V]. There is no other pruning of AGENTS.md.
- CLI invocation: `amp --dangerously-allow-all` or `claude --dangerously-skip-permissions --print < CLAUDE.md` [(ralph.sh)](https://raw.githubusercontent.com/snarktank/ralph/main/ralph.sh) [V].

**1d. Other Ralph-style variants (2025–2026)**
- RepoMirror, YC agents-hackathon write-up "We Put a Coding Agent in a While Loop and It Shipped 6 Repos Overnight" (2025, exact date not verified). Loop: `while :; do cat prompt.md | claude -p --dangerously-skip-permissions; done`, with a `.agent/` scratchpad for plans and todos. Cost: "a little less than $800 on inference … ~1100 commits … Each Sonnet agent costs about $10.50/hour". Bloat evidence: "we tried 'improving' the prompt with Claude's help. It ballooned to 1,500 words. The agent immediately got slower and dumber. We went back to 103 words and it was back on track." Also: "we ended up going in and updating the prompts incrementally" [(repomirror.md)](https://raw.githubusercontent.com/repomirrorhq/repomirror/main/repomirror.md) [V].
- Continuous Claude (Anand Chowdhary, date not verified). A bash "conductor" repeatedly invokes Claude Code, opens PRs, and monitors CI with `gh pr checks`. On failure it closes the PR and discards the work; "with knowledge of test failures, the next attempt can try something different". A shared markdown notes file is the "relay race … baton". "Without specific prompting instructions, it would create verbose logs that harm more than help." Example: the previous iteration's note "tried adding tests to X but failed on edge case, need to handle null input in function Y" was picked up and prioritised by the next run [(README)](https://raw.githubusercontent.com/AnandChowdhary/continuous-claude/main/README.md) [V].
- Ralph Orchestrator (mikeyobrien). Rust. Multi-backend: Claude Code, Kiro, Gemini CLI, Codex, Amp, Copilot CLI, OpenCode and more. Uses "Hats", backpressure gates, and "Memories & Tasks — Persistent learning" [(README)](https://raw.githubusercontent.com/mikeyobrien/ralph-orchestrator/main/README.md) [V]. Memories live in `.ralph/agent/memories.md` and are typed `pattern | decision | fix | context` with tags. They are auto-injected at the start of each iteration with a budget of 2,000 tokens ("Max tokens to inject") and filters by type, tag or `recent` days [(memories-and-tasks.md)](https://raw.githubusercontent.com/mikeyobrien/ralph-orchestrator/main/docs/concepts/memories-and-tasks.md) [V].
- bmad-loop (BMAD org, "early open beta"): "A deterministic ralph-loop orchestrator for the BMAD-METHOD implementation phase". Details are in Q4 [(README)](https://raw.githubusercontent.com/bmad-code-org/bmad-loop/main/README.md) [V].
- Anthropic's C compiler experiment (Feb 5, 2026, Nicholas Carlini) used "a harness that sticks Claude in a simple loop (if you've seen Ralph-loop, this should look familiar)". Details are in Q6 [(Anthropic)](https://www.anthropic.com/engineering/building-c-compiler) [V].
- HumanLayer published "A Brief History of Ralph" [(HumanLayer)](https://www.humanlayer.dev/blog/brief-history-of-ralph) [S, title only].

### Inferences
- In Ralph variants, the post-mortem writer is the worker itself (self-report in progress.txt or AGENTS.md) plus the human operator. The orchestrator is code with no judgment. The baseline is the inverse: the orchestrator writes incidents, and workers' discoveries are not persisted into target repos. This is exactly the baseline's "no path for lessons to reach worker instruction files" gap.
- The cheapest plug-in for the baseline is snarktank's and Huntley's rule, added as a DoD item in every issue spec. For example: "if you needed more than one attempt to find the right build/test command, or hit a non-obvious gotcha, add one line to the nearest AGENTS.md (operational only, no story detail); otherwise write 'no learnings'". The verifier then checks that diff against the Huntley/snarktank exclusion list. The worker's transcript/thread ID should also go into the executor report, as snarktank does with Amp thread URLs, so later analysis can mine it.
- The Ralph evidence on bloat is consistent across sources. There is Huntley's "bloated AGENTS.md pollutes every future loop", RepoMirror's 1,500 → 103 words, and Continuous Claude's "verbose logs harm". Any baseline change that pushes lessons into worker files needs a size budget; Ralph Orchestrator's 2,000-token injection budget is a concrete precedent.
- None of the Ralph sources measure whether a "sign" reduced recurrence. Improvement is judged by eye. That matches the baseline's "no check that a fix reduced recurrence" gap rather than solving it.

### Gaps
- Huntley's original post, his later talks and his cost claims (e.g. $/hour) could not be read directly (ghuntley.com blocked, search budget exhausted). The exact original date is unverified: LinearB says May 2025, and it is often cited as July 2025 [B].
- The date the Anthropic ralph-wiggum plugin was added, and the date of the rename to ralph-loop, are unverified.
- There are no controlled measurements of Ralph effect versus a baseline (tokens per story, rework rate) in any source found.

---

## 2. Every's Compound Engineering (Kieran Klaassen, Dan Shipper; compound-engineering plugin): the Plan → Work → Review → Compound cycle, what the "compound" step writes (docs/solutions, new rules, new review agents), and who approves

### Takeaway
As of Sept 2026, Compound Engineering is a 36-skill, cross-host plugin (Claude Code, Codex CLI/app, Cursor, Grok Build, Devin CLI, Copilot, Factory Droid, OpenCode and others). Its loop is brainstorm → plan → work → simplify → review → compound. `ce-compound` writes one durable learning per run into `docs/solutions/<category>/…md` with YAML frontmatter, under a strict "non-obvious, durable, material" counterfactual bar. It validates claims against the tree, detects overlap, and can mine Claude Code/Codex session history. Learnings are read by the next plan and review. A separate `ce-compound-refresh` skill prunes and consolidates them, and a "Compound Packs" ladder promotes hardened learnings into enforced rules. Approval sits at the PR merge, plus explicit consent for any edit to AGENTS.md/CLAUDE.md. In the current version the compound step does not create new review agents.

### Cited Findings
- Name/URLs/authors: [EveryInc/compound-engineering-plugin](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/README.md) [V]. It is "Maintained by Kieran Klaassen and Trevin Chow, with contributions from the open-source community" [V]. Every's article "Compound Engineering: How Every Codes With Agents" is at [every.to](https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents) [S, title only]. The origin story "My AI had already fixed the code before I saw it" is linked from the README [(README)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/README.md) at [every.to](https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it) [V link / S content].
- Maturity: "a plugin of 36 skills … runs on 14 agent hosts, including Claude Code, Cursor, and Codex". Release automation ships versions; CHANGELOG entries run to v3.13.1 (2026-06-17), and after that "GitHub Releases are the canonical release-notes surface" [(README)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/README.md), [(CHANGELOG)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/CHANGELOG.md) [V].
- Renames and timeline:
  - The command form `/workflows:compound` appears in issue #186, "Understanding how /workflows:compound captures learnings from sub-agent work" [(issue)](https://github.com/EveryInc/compound-engineering-plugin/issues/186) [S, title only]. The contents of that issue were not read; it would be relevant to orchestrator/sub-agent capture.
  - The `ce:*` naming (e.g. `ce:compound`, `ce:review`) is used in 2026-03 changelog entries.
  - v3.0.0 (2026-04-22): "rename all skills and agents to consistent ce- prefix".
  - v2.45.0 (2026-03-19): Claude Code auto memory integrated "as supplementary data source for ce:compound and ce:compound-refresh".
  - v2.52.0 (2026-03-25): "consolidation support and overlap detection" added.
  - v2.64.0 (2026-04-10): cross-platform session-history agent (`/ce-sessions`) added.
  - Sources: [(CHANGELOG)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/CHANGELOG.md) [V]. The plugin later "moved to a root-native, skills-only layout" [(README)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/README.md) [V].
- Current loop: "brainstorm the requirements, plan the implementation, work through the plan, simplify what you wrote, review the result, then compound the learning". "80% is in planning and review, 20% is in execution". "`/ce-compound` writes learnings that the next `/ce-brainstorm` and `/ce-plan` read as grounding … That return arrow is the whole point." [(README)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/README.md) [V]. The README demo claims "Run one teaches it. Run two remembers": a learning about an env-var trap was found by `ce-plan` 18 days later on unrelated work (anecdote, anonymised) [(README)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/README.md) [V].
- What `ce-compound` writes:
  - "One doc in `docs/solutions/`, plus optional `CONCEPTS.md` vocabulary capture. Interactive Full may also edit `AGENTS.md`/`CLAUDE.md` for discoverability after consent." [(ce-compound guide)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/docs/guides/ce-compound.md) [V].
  - Bug-track docs have sections Symptoms / What Didn't Work / Solution / Why This Works / Prevention. Knowledge-track docs have Context / Guidance / Why This Matters / When to Apply / Examples.
  - Frontmatter fields: closed enums for `problem_type`, `severity` and `resolution_type`, and open vocabulary for `component` and `root_cause`. Categories are auto-detected (e.g. `build-errors/`, `test-failures/`, `workflow-issues/`, `developer-experience/`) [(guide)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/docs/guides/ce-compound.md) [V].
- Write boundary: "Only the orchestrator writes product files. Phase 1 subagents write to per-run scratch only." The orchestrator may additionally write CONCEPTS.md, and, "only in interactive Full mode after consent", a discoverability line in an instruction file. Also only in interactive mode, when the user selects them, it may write a rule file into a writable Compound Pack and a `packs:` config entry. "Nothing else in the tree is written." [(SKILL.md)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/skills/ce-compound/SKILL.md) [V]. In the current version, therefore, the compound step does not generate new review agents or skills.
- Promotion bar (threshold): "A learning earns its place only when it holds durable project reasoning that is not readily recoverable from the final code, tests, types, comments, or existing documentation, and losing it would plausibly cause recurrence, material risk, or substantial rediscovery. Apply this counterfactual: if the learning document disappeared, would a future engineer … still be likely to repeat the mistake …? Completion, effort, and diff size do not establish eligibility." "One learning per run." [(SKILL.md)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/skills/ce-compound/SKILL.md) [V].
- "Narrowest durable home" table: machine-enforceable behavior → test/type/assertion; local rationale → code comment; change history → commit/PR; shared language → `CONCEPTS.md`; cross-boundary reasoning → `docs/solutions/` [(guide)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/docs/guides/ce-compound.md) [V].
- Full-mode mechanics:
  - Three parallel research subagents: Context Analyzer, Solution Extractor and Related Docs Finder.
  - Overlap is scored on 5 dimensions: problem, root cause, solution, referenced files, prevention rules. High overlap (4–5) updates the existing doc and adds `last_updated`. Moderate overlap (2–3) creates a new doc and flags it for consolidation.
  - Claims are validated by a deterministic script (paths, SHAs, links) plus a read-only validator subagent that quotes defining source lines.
  - A session-history probe scans Claude Code (`~/.claude/projects/`) and Codex (`~/.codex/sessions/`) sessions for the repo and escalates only on "current-branch match or at least two topic-keyword hits". Findings fold into "What Didn't Work".
  - Source: [(guide)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/docs/guides/ce-compound.md) [V].
- Triggering: completion phrases like "that worked" or "it's fixed" mark the checkpoint but "are not sufficient triggers". Users can add a standing AGENTS.md/CLAUDE.md line to "offer" or "automatically invoke the ce-compound skill with mode:non-interactive". Auto-run "writes to docs/solutions/ … without asking. Non-interactive never edits AGENTS.md/CLAUDE.md" [(guide)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/docs/guides/ce-compound.md) [V].
- Who approves:
  - The learning is committed so it "can ship in the PR that produced it". `/lfg` "never pauses for approval", and "Merging stays with you unless you grant" it. Leftover review findings become an "Unapplied review findings" checklist in the PR body for the human reviewer [(lfg guide)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/docs/guides/lfg.md) [V].
  - `ce-code-review` is "report-only by default; local fixes need apply:local" [(code-review guide)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/docs/guides/ce-code-review.md) [V].
- How learnings are applied next run: "`/ce-plan` reads `docs/solutions/` during Phase 1 research, and `/ce-ideate` reads it as grounding" [(guide)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/docs/guides/ce-compound.md) [V]. `ce-code-review` runs an "institutional-learnings pass" that also searches pack roots and flags violations with `(pack: <id>, <path>)` citations [(code-review guide)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/docs/guides/ce-code-review.md) [V]. A `project-standards-reviewer` persona runs "only when at least one criteria file governs a changed file" [(code-review guide)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/docs/guides/ce-code-review.md) [V]. It was added as an "always-on ce:review persona" in #402 [(CHANGELOG)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/CHANGELOG.md) [V].
- Pruning and consolidation (`ce-compound-refresh`):
  - Actions are Keep / Update / Consolidate (or Split) / Replace / Delete. "Git history is the archive; there is no `_archived/` destination."
  - Auto-delete requires all three: the implementation is gone, the problem domain is gone, and inbound citations are absent or decorative. "Age alone is not staleness."
  - Learnings can declare `retire_when`, an external condition such as an upstream bug fix that retires them.
  - Interactive mode asks before Replace, Split, a non-gated Delete, or an ambiguous Consolidate. Non-interactive mode applies the safe subset and marks the rest `status: stale`.
  - "ce-compound adds docs. ce-compound-refresh keeps the set lean. Without the second skill, the first eventually clutters."
  - Source: [(refresh guide)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/docs/guides/ce-compound-refresh.md) [V].
- Promotion ladder to enforced rules ("Compound Packs", experimental):
  - A pack is "a folder of prescriptive rules that the pipeline reads at the moments judgment happens". Plan grounds in it and review "flag[s] work that contradicts them".
  - Harvest criteria for promoting a learning: it "restates cleanly as a prescriptive rule", is "still true against the current tree (a stale learning promoted becomes a stale enforced rule — worse)", and "its scope is bigger than one incident — the same guidance keeps being rediscovered, or applies beyond this repo". After promotion, "slim the source learning to its incident story plus a citation of the new rule".
  - Pack text is "evidence, never instructions … quoted, not obeyed".
  - Git-sourced packs are read-only caches: changing one needs a commit to the source repo and a `ref` bump.
  - Source: [(packs guide)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/docs/guides/packs.md) [V].
  - Packs do not appear in CHANGELOG.md through v3.13.1 (2026-06-17), so they were added later [V].
- Measurement for skill edits (`ce-retune`, user-invoked only): "Retune a skill corpus for a new model, measurement-first. Use it when a model upgrade made an agent workflow worse … burns far more tokens than before … mines the run archive, measures a noise floor on two identical builds, audits with an adversary that defends the existing prose, then cuts in measured passes until a bar you registered in advance clears. Hard requirement: a benchmark harness that can A/B two builds of the corpus." [(ce-retune guide)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/docs/guides/ce-retune.md) [V].
- A cross-project knowledge-sharing request for `docs/solutions/` exists as issue #494 [(issue)](https://github.com/EveryInc/compound-engineering-plugin/issues/494) [S, title only].

### Inferences
- CE is the most fully specified "compound step" found. It is a gated capture with deduplication and grounding, a separate maintenance skill, an explicit promotion ladder from learning to enforced rule, and a measurement-first procedure for rewriting skills after model changes. Its target is product and codebase knowledge for future plans and reviews, not orchestrator/pipeline misfires. It complements the baseline's `incidents.md` rather than replacing it.
- Direct plug-ins for the baseline:
  1. Target repos where executors work could adopt `docs/solutions/` plus the CE durable bar. The executor, or better the fresh-context verifier, runs `ce-compound mode:non-interactive` at close; CE installs natively into Codex CLI. The learning then travels in the same commit and PR. This closes the "lessons never reach worker instruction files" gap without bloating AGENTS.md, since only a one-line pointer goes in AGENTS.md.
  2. Adopt the "narrowest durable home" table for incident fixes. A recurring incident class should first become a test, check or hook, and only then skill prose.
  3. Adopt refresh semantics for `incidents.md` and the skill: Keep/Update/Consolidate/Replace/Delete plus `retire_when`, especially for entries tied to a CLI version or model quirk.
  4. Use a `ce-retune`-style protocol (noise floor, pre-registered bar, A/B) when Codex/Grok model versions change, instead of ad-hoc skill edits.
- CE's session-history probe, which reads Codex session logs, is the only verified mechanism in this survey that mines terminal-agent transcripts for "What Didn't Work". That is the kind of worker-side inefficiency the user wants to capture.
- CE's "one learning per run" and its overlap scoring are a stricter threshold than the baseline's "2+ entries of a class". CE promotes on quality (counterfactual materiality) rather than frequency, and frequency only matters for promotion to packs. Combining both, frequency for orchestrator incidents and materiality for worker learnings, looks sound.

### Gaps
- Every's articles (dates, the original 4-step Plan/Work/Assess-or-Review/Compound description, Dan Shipper's role, any claims that "compound" creates new review agents or CLAUDE.md rules) could not be fetched. Only titles were seen [S]. The claim that earlier versions created new reviewer agents from learnings is therefore unverified [B].
- Issue #186 (how compound captures sub-agent learnings) could not be read.
- There are no quantitative results (fewer bugs, fewer tokens) for CE beyond the README anecdote.

---

## 3. Steve Yegge's Beads and Gas Town (2025–2026): roles (Mayor, Polecats, Witness, Refinery, Deacon, or current equivalents), how work history and learnings persist, and any retrospective or self-improvement mechanism

### Takeaway
Gas Town (v0.1.0 on 2026-01-02, v1.2.1 on 2026-06-06) is a heavy orchestration layer for 20–30 CLI agents (Claude Code, Codex, Copilot, Gemini, Pi). The Mayor coordinates, Polecats work, Witness/Deacon/Dogs patrol health, the Refinery runs the merge queue with gates, and escalations go up to the human Overseer. Its durable substrate is work state rather than lessons: Beads (a Dolt-backed issue graph), git-worktree "hooks", per-polecat identity with a "CV chain" and work history, per-session cost records, `.events.jsonl` logs queryable via `gt seance`, and OTEL metrics. No explicit retrospective or post-mortem loop was found in the repo. Improvements arrive as maintainer changes to formulas, provisioning and gates. The pieces that come closest are "prior attempt context" on re-dispatch, Promptfoo model comparison for patrol agents, cost tiers, and peer-validated "stamps" (reputation) in the Wasteland federation. Beads adds `bd remember` / `bd prime` memory injection and "memory decay" compaction.

### Cited Findings
- URLs/repos: [steveyegge/gastown README](https://raw.githubusercontent.com/steveyegge/gastown/main/README.md) [V]. The repo now presents as [gastownhall/gastown](https://github.com/gastownhall/gastown) [S]. The Beads README badges point to `gastownhall/beads` [(beads README)](https://raw.githubusercontent.com/steveyegge/beads/main/README.md) [V].
- Author posts: "Welcome to Gas Town" (New Year 2026) [(Medium)](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04) [S] and "Gas Town Emergency User Manual" ("a busy 12 days since…") [(Medium)](https://steve-yegge.medium.com/gas-town-emergency-user-manual-cf0e4556d74b) [S]. Third-party write-ups: [yegge.ai/gastown](https://yegge.ai/gastown) [S], [Daniel Vaughan, 2026-04-08, on Gas Town and Codex CLI](https://codex.danielvaughan.com/2026/04/08/gas-town-multi-agent-factory/) [S], [John McBride, 2026-01-16](https://johncodes.com/archive/2026/01-16-a-glimpse-into-the-future/) [S].
- Versions: 0.1.0 (2026-01-02), 0.2.0 (2026-01-04), 0.3.0 (2026-01-17), 0.8.0 (2026-02-23), 0.12.1 (2026-03-15), 0.13.0 (2026-03-29), 1.2.0 (2026-05-27), 1.2.1 (2026-06-06) [(CHANGELOG)](https://raw.githubusercontent.com/steveyegge/gastown/main/CHANGELOG.md) [V]. README claim: "4-10 agents become chaotic → Scale comfortably to 20-30 agents" [(README)](https://raw.githubusercontent.com/steveyegge/gastown/main/README.md) [V].
- Roles (current):
  - **Mayor**: "Your primary AI coordinator … a Claude Code instance with full context about your workspace".
  - **Polecats**: "Worker agents with persistent identity but ephemeral sessions … identity and work history persist".
  - **Witness**: "Per-rig lifecycle manager. Monitors polecats, detects stuck agents, triggers recovery".
  - **Deacon**: "Background supervisor running continuous patrol cycles across all rigs".
  - **Dogs**: "Infrastructure workers dispatched by the Deacon for maintenance tasks (e.g., Boot for triage)".
  - **Refinery**: "Per-rig merge queue processor … runs verification gates, and merges to main using a Bors-style bisecting queue. Failed MRs are isolated and either fixed inline or re-dispatched".
  - **Crew**: the human's workspace.
  - **Escalation** "routed through the Deacon, Mayor, and (if needed) Overseer" (the human).
  - Also: Convoys, Molecules/Formulas (TOML workflow templates), and a Scheduler (`scheduler.max_polecats`).
  - Source: [(README)](https://raw.githubusercontent.com/steveyegge/gastown/main/README.md) [V]. A snippet summarising Yegge's post lists "seven worker roles" including those above [(search snippet via Medium)](https://steve-yegge.medium.com/gas-town-emergency-user-manual-cf0e4556d74b) [S].
- Successor/extraction: "Gas City is an orchestration-builder SDK for multi-agent systems. It extracts the reusable infrastructure from Gas Town into a configurable toolkit with runtime providers, work routing, formulas, orders, health patrol, and a declarative city configuration" (`city.toml`; runtime providers tmux, subprocess, exec, ACP, Kubernetes). It has a "Coming from Gas Town?" role-mapping doc [(Gas City README)](https://raw.githubusercontent.com/gastownhall/gascity/main/README.md) [V]. Release date not verified.
- How work history persists:
  - "Each polecat has a permanent agent bead, CV chain, and work history that accumulates across assignments. Sessions and sandboxes are ephemeral" [(glossary)](https://raw.githubusercontent.com/steveyegge/gastown/main/docs/glossary.md) [V].
  - `gt polecat identity show` "Display CV summary for agents" arrived in 0.3.0 (2026-01-17) [(CHANGELOG)](https://raw.githubusercontent.com/steveyegge/gastown/main/CHANGELOG.md) [V].
  - Hooks are git-worktree persistent storage that "survives crashes and restarts" [(README)](https://raw.githubusercontent.com/steveyegge/gastown/main/README.md) [V].
  - **Seance**: "Discovers previous agent sessions via `.events.jsonl` logs, enabling agents to query their predecessors for context and decisions" (`gt seance --talk <id> -p "What did you find?"`) [(README)](https://raw.githubusercontent.com/steveyegge/gastown/main/README.md) [V].
- Cost and time accounting:
  - 0.2.0 (2026-01-04) added "`gt costs` command – Session cost tracking and reporting", "Costs stored in beads", and "Stop hook integration – Auto-record costs on session end".
  - 0.8.0 (2026-02-23) added "Cost-tier presets for model selection" and "Promptfoo model comparison framework for patrol agents".
  - Source: [(CHANGELOG)](https://raw.githubusercontent.com/steveyegge/gastown/main/CHANGELOG.md) [V].
  - Telemetry: all operations are emitted to OTLP, e.g. `gastown.session.starts.total`, `gastown.polecat.spawns.total`, `gastown.done.total`, and bd call durations [(README)](https://raw.githubusercontent.com/steveyegge/gastown/main/README.md) [V].
- Improvement mechanisms found, all maintainer- or orchestrator-driven with no automatic retro:
  - 0.12.1 (2026-03-15): "Prior attempt context — Polecats receive context from previous failed attempts when re-dispatched".
  - 0.8.0: "Configurable quality gates before merge in refinery" and "Bead respawn count tracking for spawn storm detection".
  - 0.13.0 (2026-03-29):
    - "Formula/path discoverability — Reference docs for formulas, beads CLI, and Dolt injected into agent context to eliminate discovery tax".
    - "Polecat CLAUDE.md provisioning — Lifecycle instructions provisioned on all spawn paths … with `gt done` reminders injected at startup and after compaction".
    - "Patrol effort tuning — Idle patrol cycles now run at reduced reasoning effort".
    - "Longer patrol backoff … reducing cost by ~66% for dormant rigs".
    - "Guard and compliance — Block polecats from pushing directly to main".
  - Source: [(CHANGELOG)](https://raw.githubusercontent.com/steveyegge/gastown/main/CHANGELOG.md) [V].
  - A keyword search of the whole changelog for retro, lesson, learn, reflect and post-mortem returned no matches [V: grep of CHANGELOG.md].
- Peer validation and reputation (Wasteland, a federation over DoltHub):
  - "When a validator reviews your completed work, they issue a stamp — a multi-dimensional attestation covering quality, reliability, and creativity … The yearbook rule applies: you cannot stamp your own work" [(WASTELAND.md)](https://raw.githubusercontent.com/steveyegge/gastown/main/docs/WASTELAND.md) [V].
  - Conflict: the README describes the stamp dimensions as "(quality, speed, complexity)" [(README)](https://raw.githubusercontent.com/steveyegge/gastown/main/README.md) [V].
  - Stamps, scorekeeper and "Spider Protocol" fraud detection arrived in 0.12.1–0.13.0 [(CHANGELOG)](https://raw.githubusercontent.com/steveyegge/gastown/main/CHANGELOG.md) [V].
- Claude Code agent-teams design (not implemented):
  - "Witness AT Team Lead: Implementation Spec … Status: Future architecture — NOT YET IMPLEMENTED … Date: 2026-02-08 … Author: furiosa (gastown polecat)". It would make the Witness a Claude Code Agent Teams lead in delegate mode.
  - It includes a `TaskCompleted` quality-gate hook that exits 2 if `git status --porcelain` is non-empty ("Uncommitted changes detected") or the branch is not pushed.
  - Its rollback plan says to "File lessons-learned bead for Phase 1 retry".
  - Source: [(design doc)](https://raw.githubusercontent.com/steveyegge/gastown/main/docs/design/witness-at-team-lead.md) [V].
- Beads (bd):
  - "Distributed graph issue tracker for AI agents, powered by Dolt … provides a persistent, structured memory for coding agents".
  - Minimal AGENTS.md block: "Run `bd prime` for workflow context … Use `bd remember "insight"` for persistent project memory; do not create MEMORY.md files". `bd prime` "Print[s] agent workflow context and persistent memories".
  - "Compaction: Semantic 'memory decay' summarizes old closed tasks to save context window".
  - `bd setup codex` installs a skill, AGENTS.md guidance and hooks.
  - Source: [(beads README)](https://raw.githubusercontent.com/steveyegge/beads/main/README.md) [V].
  - Compaction arrived in 0.9.8 (2025-10-16) as "`bd compact` … summarize old closed issues … simplified to permanent decay". Agent-driven compaction came in 0.23.0 (2025-11-08), and `bd compact --audit` (logging compaction prompts and responses) in 0.31.0 (2025-12-20). Latest is 1.3.0 (2026-09-15) [(beads CHANGELOG)](https://raw.githubusercontent.com/steveyegge/beads/main/CHANGELOG.md) [V]. npm `@beads/bd` was created 2025-11-03 [(npm)](https://registry.npmjs.org/@beads/bd) [V].

### Inferences
- Gas Town answers "where does work state live" (a ledger) much better than "how does the system learn". It has no retrospective agent. The human Overseer and the maintainers (Yegge, and interestingly polecats that write design docs) encode lessons into formulas, role CLAUDE.md provisioning, patrol settings and gates. This mirrors the baseline's issue-first skill edit, done at larger scale.
- Pieces that directly address baseline gaps:
  - Per-session cost auto-recorded by a Stop hook, and cost tiers per role. This fills the baseline's missing per-task token/time accounting: the forwarder could append tokens and time to each journal comment.
  - Per-worker CV chains. These give data for choosing an executor, and for noticing that a particular CLI/model fails a class of tasks more often.
  - "Prior attempt context" on re-dispatch. This is exactly the baseline's "fresh executor" rung: the fresh executor should get a structured digest of prior failures, not a blank slate.
  - The yearbook rule for validation. This is a cheap structural fix for "orchestrator grades itself".
- The unimplemented TaskCompleted gate (uncommitted/unpushed checks) is a ready template for converting the baseline's "missing commit" incident class into a deterministic check in the forwarder, rather than a prose rule.
- Beads' `bd remember`/`bd prime` is a per-repo memory that CLI agents load at start. It is a possible transport for worker-side lessons into target repos, but it is unreviewed and unbounded unless compaction is used.

### Gaps
- Yegge's Medium posts (role rationale, "GUPP"/propulsion, his own lessons, costs such as tokens per day or $/month) could not be read. Only snippets were seen.
- It is not verified whether Gas City has any retrospective or learning primitive ("orders", "health patrol" only).
- The date `bd remember` was introduced is not verified; the changelog mentions it at least from 1.1.0-rc.2 (2026-07-02). GitHub star counts were not visible (github.com blocked).

---

## 4. BMAD Method (retrospective after epics), GitHub Spec Kit, Agent OS (Builder Methods), CCPM, Taskmaster: which have an explicit lessons loop?

### Takeaway
Only BMAD has a first-class, built-in retrospective with lessons carried forward. `bmad-retrospective` runs after each epic, and since v6.9.0 (2026-06-21) its action items persist in `sprint-status.yaml` and are preserved by the next sprint planning. Since v6.11.0 (2026-08-09) it is an evidence-based review with a headless `-H <epic>` orchestrator interface. Its companion **bmad-loop** is the closest architectural analogue to the user's baseline found in this survey. Spec Kit core has no lessons loop, but 2026 community extensions add retrospectives with human-gated spec updates, plus an instruction-drift checker. Agent OS v3 (2026-01-20) has human-curated "discover/inject standards". CCPM and Taskmaster track progress but have no lessons loop that could be found.

### Cited Findings
**BMAD Method** (bmad-code-org)
- Latest release in the changelog: v6.12.0 (2026-09-03). The README delivery loop is "Clarify → Plan → Build and verify; Learn and adjust loops back to Plan" [(README)](https://raw.githubusercontent.com/bmad-code-org/BMAD-METHOD/main/README.md), [(CHANGELOG)](https://raw.githubusercontent.com/bmad-code-org/BMAD-METHOD/main/CHANGELOG.md) [V].
- v6.9.0 (2026-06-21): "Retrospective action items tracked in sprint-status (#2465). The retrospective step appends an `action_items` section to `sprint-status.yaml`; sprint-status validates and surfaces open items, and sprint-planning preserves them on regenerate." [(CHANGELOG)](https://raw.githubusercontent.com/bmad-code-org/BMAD-METHOD/main/CHANGELOG.md) [V].
- v6.11.0 (2026-08-09): "`bmad-retrospective` rebuilt as an evidence-based epic review (#2612, #2665). Five phases over the epic's real artifacts, with aggregate views no single diff hunk shows: architecture delta, duplication, god-class growth, pattern divergence, spec reconciliation. Team discussion is now opt-in, delegating to `bmad-party-mode` seeded with real findings. New `-H` / `--headless` flag, with `-H <epic>` as the stable orchestrator interface. It can also retro an epic that exists only as a spec folder … writing `{spec-folder}/RETROSPECTIVE.md`". [(CHANGELOG)](https://raw.githubusercontent.com/bmad-code-org/BMAD-METHOD/main/CHANGELOG.md) [V].
- Also in v6.11.0 (2026-08-09):
  - Headline: "`bmad-retrospective` judges an epic against its own artifacts, requires a source reference on every finding, and rejects an epic with unfinished stories instead of closing quietly".
  - "Intent Alignment Auditor (#2560). A fourth default Build Auto review layer fed the verbatim invocation intent alongside the diff, with an intent-ambiguity halt in planning".
  - "`bmad-project-context` replaces generated documentation with one verified block in the repository's AGENTS.md".
  - Review layers became configurable, including "swapping in an external tool over bash and therefore a different model".
  - "Quick Dev becomes Build": `bmad-dev-auto` → `bmad-build-auto`.
  - Source: [(CHANGELOG)](https://raw.githubusercontent.com/bmad-code-org/BMAD-METHOD/main/CHANGELOG.md) [V].
- v6.12.0 (2026-09-03):
  - "Review triage logs a verdict and evidence for every finding, so nothing gets dropped silently".
  - "`bmad-project-context` now adopts a handwritten `AGENTS.md` instead of rewriting it".
  - Grok added to the installer.
  - Source: [(CHANGELOG)](https://raw.githubusercontent.com/bmad-code-org/BMAD-METHOD/main/CHANGELOG.md) [V].
- Docs description: it "reads what the epic actually produced (the specs, the full diff, the per-story commits, the sprint status) … rather than anyone's recollection … What comes back is a written review, a set of owned action items, and a verdict on whether the epic met its bar" [(docs.bmad-method.org)](https://docs.bmad-method.org/explanation/retrospective/) [S]. An older description (skill registries) says it "loads project docs (PRD, architecture, prior retros) … synthesizes SMART action items … saves the retro while updating sprint-status.yaml" [(LobeHub)](https://lobehub.com/skills/kattate-katalyst_franchise_planner-bmad-retrospective) [S]. A related issue is "Epic Retrospective Workflow: Add Incremental Output and Upgrade to Step-Based Architecture" [(issue #1287)](https://github.com/bmad-code-org/BMAD-METHOD/issues/1287) [S].

**bmad-loop** (bmad-code-org; "early open beta"; installed via `uv tool` from git) [(README)](https://raw.githubusercontent.com/bmad-code-org/bmad-loop/main/README.md) [V]
- Architecture:
  - "No LLM in the control loop. Story selection, retry budgets, gates, and completion checks are code, not prompts."
  - "Coding-agent hooks (Stop / SessionStart / SessionEnd / PreCompact) write structured event files the orchestrator watches; skills … write a machine-readable `result.json`."
  - "Dev and review are separate sessions — review never inherits the implementer's context."
  - The tmux adapter drives `claude`, `codex`, `gemini`, `copilot`, `antigravity`, and per-stage models can differ (e.g. review by `codex`).
  - Source: [(README)](https://raw.githubusercontent.com/bmad-code-org/bmad-loop/main/README.md) [V].
- Verification: after each session the orchestrator checks "spec frontmatter status, baseline-commit validity, non-empty diff, sprint-status sync, and your test/lint commands before any commit" [(README)](https://raw.githubusercontent.com/bmad-code-org/bmad-loop/main/README.md) [V].
- Failure ladder and policy (`.bmad-loop/policy.toml`):
  - `max_dev_attempts = 2`, `max_review_cycles = 3`, and `retrospective = "notify"` (never | notify | auto) at the epic-boundary gate.
  - "bounded dev retries (verify-command failures keep the tree and feed the failing output to the next session via --feedback; other failures roll back to baseline)".
  - "plateau-defer when review won't converge".
  - Typed escalations: `CRITICAL` pauses the run and notifies; `PREFERENCE` is journaled and the run continues.
  - A `bmad-loop resolve` agent fixes the frozen spec with the human, then re-arms the story.
  - "Intent-gap patch-restore" applies when "the implementation was sound but read the spec differently than intended".
  - Source: [(README)](https://raw.githubusercontent.com/bmad-code-org/bmad-loop/main/README.md) [V].
- Token accounting:
  - `status` shows a "Run + sprint summary with per-story token totals — cost-weighted, with the raw count alongside".
  - Policy settings: `max_tokens_per_story = 2000000`, `cache_read_weight = 0.1`, `session_budget_mode = "warn"` (off | warn | enforce), and `max_tokens_per_session = 4000000`, commented "healthy sessions run ~1–2.5M weighted, so the default trips only true runaways".
  - `diagnose` emits "phase/token/session histograms, escalation counts".
  - Source: [(README)](https://raw.githubusercontent.com/bmad-code-org/bmad-loop/main/README.md) [V].
- Noticed-but-deferred work: "Skills accumulate an append-only ledger (`deferred-work.md`, `DW-<n>` entries) of split-off goals, pre-existing review findings, and items deferred as 'needs human decision'", processed later by `bmad-loop sweep` [(README)](https://raw.githubusercontent.com/bmad-code-org/bmad-loop/main/README.md) [V].

**GitHub Spec Kit**
- Latest release in the changelog: v1.0.11 (2026-09-24). "Constitution once per project; specify → plan → tasks → implement → converge per feature … Repeat implement → converge until convergence reports Converged." [(README)](https://raw.githubusercontent.com/github/spec-kit/main/README.md), [(CHANGELOG)](https://raw.githubusercontent.com/github/spec-kit/main/CHANGELOG.md) [V]. No lessons loop exists in core.
- Community extensions (catalog dates; the catalog does not say whether a date is created or updated):
  - `retrospective`, "Post-implementation retrospective with spec adherence scoring, drift analysis, and human-gated spec updates" (emi-dm, 2026-02-24).
  - `retro`, "Sprint retrospective analysis with metrics, spec accuracy assessment, and improvement suggestions" (2026-04-01).
  - `memorylint`, "Evidence-driven instruction drift checker: audits agent memory files for boundary, reality, conflict, and redundancy drift" (2026-04-09).
  - `archive`, "Archive merged features into main project memory" (2026-03-14).
  - `memory-md` (2026-04-23).
  - `verify-review-ship`, "…learning governance…" (2026-07-10).
  - `adrkit`, decision memory (2026-08-03).
  - Source: [(catalog.community.json)](https://raw.githubusercontent.com/github/spec-kit/main/extensions/catalog.community.json) [V].
  - The changelog confirms the retrospective extension was added to the catalog in 0.1.7 (2026-02-27) and memorylint in 0.6.0 (2026-04-09) [(CHANGELOG)](https://raw.githubusercontent.com/github/spec-kit/main/CHANGELOG.md) [V].

**Agent OS** (Brian Casel, Builder Methods)
- v3 (2026-01-20) "refocuses the framework on … establishing and injecting standards":
  - `/discover-standards` "Lets the agent surface, suggest, and create standards from your codebase".
  - `/inject-standards` injects relevant standards "into any context (conversations, plans, Claude Skills) using the new `index.yml`".
  - A "Sync script — Syncs project standards back to your base profiles".
  - Source: [(CHANGELOG)](https://raw.githubusercontent.com/buildermethods/agent-os/main/CHANGELOG.md), [(README)](https://raw.githubusercontent.com/buildermethods/agent-os/main/README.md) [V].
- Example of a maintainer-applied token lesson: v2.0.3 (2025-10-10) "Updated instructions and default standards to reduce excessive tests writing and test running during feature development to improve speed and token useage" [(CHANGELOG)](https://raw.githubusercontent.com/buildermethods/agent-os/main/CHANGELOG.md) [V].
- No automatic retrospective was found.

**CCPM** (automazeio)
- GitHub Issues are the source of truth: "Comments are the audit trail", "Progress is visible in real-time through issue comments". Parallel agents are scoped to their own files and commit as `Issue #N: …`. Tracking runs as "bash scripts — instant output, no LLM overhead" [(README)](https://raw.githubusercontent.com/automazeio/ccpm/main/README.md) [V].
- No lessons loop was found. This design is very close to the baseline's forwarder journal.

**Taskmaster** (task-master-ai, Eyal Toledano)
- Features: PRD parsing, complexity analysis/report, a research model, and "Loop Command" docs hosted on tryhamster.com [(README)](https://raw.githubusercontent.com/eyaltoledano/claude-task-master/main/README.md) [V].
- The last npm publish was 0.43.1, with registry "modified" 2026-03-31 [(npm)](https://registry.npmjs.org/task-master-ai) [V].
- No lessons or retro loop was found.

### Inferences
- BMAD's retro is epic-grained and product-focused (architecture drift, duplication, spec reconciliation). Its action items flow into the next sprint's planning file, which is a working "lessons → next dispatch" channel at the planning layer. That is a level the baseline covers only through the weekly human retro.
- bmad-loop is a near-isomorph of the baseline. It has a deterministic orchestrator (like the forwarder), fresh-context CLI workers, a separate reviewer session, 2 dev attempts, typed escalations, and a deferred-work ledger for "noticed, didn't touch" findings. It already implements three of the user's missing pieces: per-story token totals and caps; stall/no-result detection with nudges (the baseline's "hung worker" and "lost report"); and an "intent gap" classification that separates "misread spec" from "bad implementation", which maps to the baseline incident class "executor misunderstood spec". Its policy and escalation vocabulary could be borrowed as-is.
- BMAD's "Intent Alignment Auditor" (the verbatim user intent is fed to a reviewer next to the diff) is a cheap countermeasure to the baseline's "misunderstood spec" class. The verifier would receive the original intent, not only the DoD.
- Spec Kit's community `memorylint` (instruction drift checker) is a ready pattern for periodic hygiene of the skill and AGENTS.md files: boundary, reality, conflict and redundancy checks.

### Gaps
- BMAD retrospective skill source files could not be located via raw paths (the repo layout changed in v6.12: "bmm tree takes its verb-named shape, agents / plan / ship"). Phase details come from the changelog and search snippets only.
- There is no quantitative evidence that BMAD retros reduce defects or tokens in later epics.
- Contents of the Spec Kit retrospective extensions (thresholds, formats) were not read.
- The Taskmaster "loop" docs and any "update --from" drift-propagation behaviour were not verified.

---

## 5. Other orchestrators and patterns: claude-flow/Ruflo (ReasoningBank: implemented vs marketing), oh-my-opencode/oh-my-openagent (Sisyphus), Claude Code agent teams/subagents (+ dynamic workflows, Projects), Conductor/Vibe Kanban/Sculptor/Claude Squad, OpenAI's Codex orchestration (Agents SDK + Codex MCP; 2026 products), Factory, Cognition/Devin, Manus

### Takeaway
- **Ruflo** (formerly claude-flow) really does ship a ReasoningBank pipeline in `agentic-flow`: retrieve → LLM-judge → distill → consolidate over SQLite plus embeddings, with numeric thresholds. Several claims are unsupported marketing: "self-optimizing neural architecture", "<0.05ms adaptation", "95%+ knowledge retention", "60% cost savings". Implementation details also undercut the pitch: without an API key the "judge" is a substring heuristic, and "contradiction detection" is cosine similarity across outcome labels, not NLI.
- **oh-my-openagent** (renamed from oh-my-opencode) matches the "head never writes code" pattern. It has evidence ledgers, independent gate reviewers and a read-only memory-recall sidecar, but no verified post-mortem loop.
- **Claude Code** now offers three orchestration surfaces:
  - Agent teams: research preview since 2026-02-05, still experimental in Sept 2026, with TaskCompleted/TeammateIdle quality-gate hooks.
  - Dynamic workflows: since 2026-05-28. Orchestration is a rerunnable script with per-phase tokens and time.
  - Projects: public beta. A coordinator plus cloud threads, where "project memory" and corrections flow to every new thread.
- **OpenAI's** 2026 direction:
  - "Harness engineering": agent struggles are treated as signals to add docs, tools or guardrails in the repo.
  - Symphony: a work-queue orchestrator with an in-repo `WORKFLOW.md`, per-session Codex token fields and an attempt counter.
  - The Codex-MCP-server multi-agent cookbook is now archived and deprecated.
  - A 2026-05 cookbook builds a full trace → feedback → eval → HALO-ranked change → Codex-handoff improvement loop with a human-approved diff.
- **Parallel-agent managers** (Vibe Kanban, Claude Squad, Sculptor) have no learning loops. Conductor, Factory, Devin and Manus could not be verified.

### Cited Findings
**Ruflo / claude-flow (ruvnet)**
- Rename: "Claude Flow is now Ruflo". npm `ruflo` was created 2026-02-16 and `claude-flow` 2025-06-10; both have latest 3.45.0 (2026-09-24) [(README)](https://raw.githubusercontent.com/ruvnet/claude-flow/main/README.md), [(npm ruflo)](https://registry.npmjs.org/ruflo), [(npm claude-flow)](https://registry.npmjs.org/claude-flow) [V].
- Marketing claims (self-reported):
  - "agents self-organize into swarms, learn from every task, remember across sessions".
  - "98 agents, 60+ commands, 30 skills".
  - "314 MCP tools".
  - An "8.1M+ ecosystem downloads" badge.
  - "hooks system automatically routes tasks, learns from successful patterns".
  - Source: [(README)](https://raw.githubusercontent.com/ruvnet/claude-flow/main/README.md) [V].
  - Search snippets additionally claim "SAFLA" (Self-Aware Feedback Loop Algorithm) and "Self-Optimizing Neural Architecture … less than 0.05ms adaptation, 95%+ knowledge retention" [(search: npm/agent-skills pages)](https://www.npmjs.com/package/claude-flow) [S].
  - The `agentic-flow` README (npm) claims "300x faster pattern retrieval (150ms → 0.5ms)", "60% Cost Savings: LLM router" and "EWC++ prevents catastrophic forgetting", and shows illustrative output such as "Agent has 94% success rate on similar tasks" [(npm agentic-flow)](https://registry.npmjs.org/agentic-flow) [V as claims].
- What is implemented, inspected in the `agentic-flow` 2.1.3 tarball [(tarball)](https://registry.npmjs.org/agentic-flow/-/agentic-flow-2.1.3.tgz) [V]:
  - Documented pipeline: "RETRIEVE – Top-k memory injection with MMR … JUDGE – LLM-as-judge trajectory evaluation … DISTILL – Extract strategy memories from successful trajectories … CONSOLIDATE – Deduplicate, detect contradictions, prune old patterns" [(npm README)](https://registry.npmjs.org/agentic-flow) [V].
  - `config/reasoningbank.yaml`:
    - retrieve: `k: 3`, `recency_half_life_days: 45`, `min_score: 0.3`, `max_age_days: 365`.
    - judge: `model: claude-sonnet-4-5-20250929`, `fallback_label: "Failure"`.
    - distill: `max_items_per_trajectory: 3`, `success_confidence_prior: 0.75`, `failure_confidence_prior: 0.60`, PII redaction.
    - consolidate: `run_every_new_items: 20`, `prune_age_days: 180`, `min_confidence_keep: 0.30`, `dedup_similarity_threshold: 0.87`.
    - Embeddings: local `Xenova/all-MiniLM-L6-v2` (384-dim).
  - `core/judge.js`: with no `OPENROUTER_API_KEY`/`ANTHROPIC_API_KEY`/`GOOGLE_GEMINI_API_KEY` it logs "using heuristic judgment". `heuristicJudge` marks success iff no step contains the substring "error" and some step contains "complete" (confidence 0.5).
  - `core/consolidate.js`: "contradiction" is logged when two memories with different outcome labels have cosine similarity ≥ threshold ("High similarity but different outcomes = contradiction"). This is not NLI, although the YAML comment says "NLI probability threshold".
  - The dedup call reads `config.consolidate.duplicate_threshold`, while the YAML defines `consolidate.dedup_similarity_threshold`. This is a key mismatch that could leave the threshold undefined (observed in dist code; not executed).
  - All four observations above: [V: dist files].
- Ruflo's ReasoningBank skill shows a usage API with `threshold: 0.7 // Only learn from high-confidence outcomes` and `minConfidence: 0.8` [(SKILL.md)](https://raw.githubusercontent.com/ruvnet/ruflo/main/.claude/skills/reasoningbank-intelligence/SKILL.md) [V]. There is a GitHub issue titled "ReasoningBank: Persistent Memory System … Pre-Trained Models" [(issue #811)](https://github.com/ruvnet/ruflo/issues/811) [S, title only].

**oh-my-opencode → oh-my-openagent (code-yeongyu; "Sisyphus Labs")**
- Rename and editions: npm `oh-my-opencode` was created 2025-12-04 and `oh-my-openagent` 2026-03-07; both have latest 4.19.4 [(npm)](https://registry.npmjs.org/oh-my-openagent) [V]. The README lists "Ultimate Edition (omo for OpenCode) — 11 agents, 54+ lifecycle hooks … Team Mode, ulw-loop" and "Light Edition (omo for Codex CLI)", and advertises "LazyCodex": "We loved Anthropic models enough to get blocked. Now we are backing Codex" [(README)](https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/master/README.md) [V].
- Orchestration model:
  - "There is one orchestrator: the main agent … delegates units of work through `task`." In `/ulw-execute` "it never writes product code itself. Every implementation, test, QA, and review unit is delegated to a spawned worker."
  - "Five gates per checkbox: plan reread, automated verification, a Manual-QA artifact, adversarial QA, cleanup receipts. Evidence goes to `.omo/ulw-execute/ledger.jsonl`. A worker's done claim is verified by an independent reviewer … before the checkbox flip."
  - Workers are routed by `category` (e.g. `ultrabrain`, `quick`, `visual-engineering`) rather than by model name.
  - Source: [(orchestration guide)](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/refs/heads/dev/docs/guide/orchestration.md) [V].
- Memory recall: "Kibitzer is the memory component's read-only recall judge: one resident sidecar session per main agent session … fed … every prompt, tool call and tool result … It only spends a model turn when a prompt or tool call surfaces a stored memory it has not judged yet … its only output is `nudge`, which becomes a notice reading `recalled memory: <hint>`." [(orchestration guide)](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/refs/heads/dev/docs/guide/orchestration.md) [V]. A `rules-injector` hook injects `.claude/rules/` files conditionally, by globs or `alwaysApply` [(features)](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/refs/heads/dev/docs/reference/features.md) [V].
- A bare `ulw` run "records a self-review in its notepad" [(orchestration guide)](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/refs/heads/dev/docs/guide/orchestration.md) [V]. How memories are written was not found in the docs read.

**Claude Code: agent teams, subagents, dynamic workflows, Projects** (release dates from npm publish times [(npm)](https://registry.npmjs.org/@anthropic-ai/claude-code) mapped to [(CHANGELOG)](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md) [V])
- Timeline:
  - 2.1.32 (2026-02-05): "Claude Opus 4.6 is now available! … Added research preview agent teams feature for multi-agent collaboration (token-intensive feature, requires setting CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1) … Claude now automatically records and recalls memories as it works."
  - 2.1.33 (2026-02-06): "Added `TeammateIdle` and `TaskCompleted` hook events for multi-agent workflows" and "Added `memory` frontmatter field support for agents".
  - 2.1.69 (2026-03-04): these hooks support `{"continue": false}`.
  - 2.1.154 (2026-05-28): "Introducing dynamic workflows".
  - 2.1.178 (2026-06-15): "removed the TeamCreate and TeamDelete tools … every session now has one implicit team".
  - 2.1.269 (2026-09-11): "Added `claude plugin eval`".
  - Source: [V].
- Agent teams docs (Sept 2026):
  - "Agent teams are experimental and disabled by default".
  - "One session acts as the team lead … Teammates work independently, each in its own context window".
  - Teammates load "CLAUDE.md, MCP servers, and skills … The lead's conversation history does not carry over".
  - Quality gates: `TeammateIdle` / `TaskCreated` / `TaskCompleted`, where "Exit with code 2 to prevent completion and send feedback".
  - Caveat: a teammate's plan approval request is approved by Claude Code "as soon as the request arrives, without the lead reviewing it".
  - "use significantly more tokens than a single session".
  - Source: [(agent-teams)](https://code.claude.com/docs/en/agent-teams) [V].
- Subagent persistent memory: `memory: user|project|local` gives the subagent a directory to "build up knowledge over time, such as codebase patterns, debugging insights". Its prompt includes "the first 200 lines or 25KB of `MEMORY.md` … with instructions to curate `MEMORY.md` if it exceeds that limit" [(sub-agents)](https://code.claude.com/docs/en/sub-agents) [V].
- Dynamic workflows:
  - "A workflow moves the plan into code … What's repeatable: … The orchestration itself".
  - "Dozens to hundreds of agents per run".
  - The progress view "shows each phase with its agent count, token total, and elapsed time".
  - The script can be saved as a command.
  - Source: [(workflows)](https://code.claude.com/docs/en/workflows) [V].
- Projects (public beta; Pro/Max):
  - "The project conversation: one long-running session where Claude acts as coordinator … It sees what threads report back, not every step they take."
  - "Project memory: Notes Claude keeps about the project, such as requirements, decisions, and pitfalls, stored as files. Every cloud thread reads the index file `MEMORY.md` when it starts."
  - "Project instructions … up to 16,000 characters."
  - "when you correct a thread, also tell Claude to remember the correction: it goes into project memory and later cloud threads start with it."
  - Saved preferences are "instructions Claude keeps to, not enforced settings".
  - "Rules about one repository … belong in that repository's CLAUDE.md."
  - Source: [(claude-projects)](https://code.claude.com/docs/en/claude-projects) [V].
- Anthropic plugin **hookify**: "Easily create custom hooks to prevent unwanted behaviors by analyzing conversation patterns or explicit instructions", with agent `conversation-analyzer` ("Analyzes conversations for problematic behaviors") [(plugins README)](https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/README.md) [V].

**Parallel-agent managers (no learning loop found)**
- Vibe Kanban (BloopAI): "Get 10X more out of Claude Code, Gemini CLI, Codex, Amp and other coding agents". npm created 2025-06-20, modified 2026-09-19, version 0.1.44 [(README)](https://raw.githubusercontent.com/BloopAI/vibe-kanban/main/README.md), [(npm)](https://registry.npmjs.org/vibe-kanban) [V].
- Claude Squad (smtg-ai): a terminal app managing multiple Claude Code/Codex/Aider instances in tmux and worktrees, with an experimental `--autoyes` [(README)](https://raw.githubusercontent.com/smtg-ai/claude-squad/main/README.md) [V].
- Sculptor (Imbue): "a desktop app for running coding agents in parallel … an experimental research preview. We are still learning what rigorous engineering looks like with agents" [(README)](https://raw.githubusercontent.com/imbue-ai/sculptor/main/README.md) [V].
- multiclaude (Dan Lorenc): "Brownian Ratchet … CI is the ratchet. Every PR that passes gets merged", with supervisor, merge-queue and pr-shepherd agents in tmux and worktrees [(README)](https://raw.githubusercontent.com/dlorenc/multiclaude/main/README.md) [V].

**OpenAI: Codex orchestration**
- Harness engineering (2026-02-11 per a mirror's filename), Ryan Lopopolo: an "internal five-month experiment … roughly one million lines of code — with zero lines written by human hands". "When agents struggled, the instinct was not to intervene and write the code manually, but to treat the struggle as a diagnostic signal — a flag that something was missing from the environment." [(OpenAI)](https://openai.com/index/harness-engineering/), [(mirror)](https://businessdatasolutions.github.io/ai-wiki/sources/2026-02-11-lopopolo-codex-harness-engineering), [(Medium summary)](https://medium.com/@AdithyaGiridharan/openais-harness-engineering-post-is-a-blueprint-for-the-agent-first-era-d9932851dcee) [S]. The awesome-harness-engineering list describes it as a "field report on building a large application with Codex using architectural constraints, repo-local instructions, browser validation, and telemetry" [(list)](https://raw.githubusercontent.com/walkinglabs/awesome-harness-engineering/main/README.md) [V as list description].
- Agents SDK + Codex as MCP server:
  - Cookbook "Building Consistent Workflows with Codex CLI & Agents SDK" (2025-10-01, `archived: true`). It runs `codex mcp-server` exposing `codex()` and `codex-reply()` tools, with a Project Manager agent that "enforce[s] gating logic between each of the specialized downstream agents … ensures that artifacts exist before handoffs" (Designer, Frontend, Backend, Tester), plus traces.
  - It now carries the banner: "Archived example — the Codex MCP server is deprecated … For new automation and CI jobs, start with the Codex SDK … For a deeper integration … use the Codex app server."
  - Sources: [(cookbook)](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/codex/codex_mcp_agents_sdk/building_consistent_workflows_codex_cli_agents_sdk.ipynb), [(registry)](https://raw.githubusercontent.com/openai/openai-cookbook/main/registry.yaml) [V].
- Symphony (openai/symphony, "low-key engineering preview"):
  - "turns project work into isolated, autonomous implementation runs". The demo monitors a Linear board and agents return "proof of work: CI status, PR review feedback, complexity analysis, and walkthrough videos". It "works best in codebases that have adopted harness engineering".
  - The reference implementation is in Elixir, or "Tell your favorite coding agent to build Symphony" from SPEC.md.
  - Source: [(README)](https://raw.githubusercontent.com/openai/symphony/main/README.md) [V].
  - SPEC (Draft v1): it "keeps the workflow policy in-repo (`WORKFLOW.md`) so teams version the agent prompt and runtime"; runs "can end at a workflow-defined handoff state (for example Human Review)"; failures are retried "with exponential backoff". The "Run Attempt" entity (§4.1.5) records `attempt` (null for the first run, ≥1 for retries). The "Live Session (Agent Session Metadata)" entity (§4.1.6) records `codex_input_tokens`, `codex_output_tokens` and `codex_total_tokens` [(SPEC.md)](https://raw.githubusercontent.com/openai/symphony/main/SPEC.md) [V]. The SPEC has no lessons/retro mechanism (keyword grep) [V].
- Improvement-loop cookbook "Build an Agent Improvement Loop with Traces, Evals, and Codex" (2026-05-12):
  - "We start with real traces, add human and model feedback, turn that feedback into evals, and use the resulting evidence to propose the next harness changes for Codex to implement."
  - Outputs are Promptfoo evals "that can be rerun later", "A Promptfoo validation gate", a HALO optimisation pass, and a `codex_handoff.md` with "ranked recommendations, the evidence behind them".
  - "A common starting point is a reviewed loop, where the system proposes the change set and a developer approves the diff before merge." "HALO diagnoses and prioritizes. A coding agent or human still changes the harness." The next step is to "rerun the same eval suite against the updated harness".
  - Budget is "about 20 minutes for a full run" with 5 traces.
  - Source: [(cookbook)](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/agents_sdk/agent_improvement_loop.ipynb) [V].
- Cookbook "Iterating Development Workflows with Codex" (2026-08-03): an AGENTS.md prompt makes Codex keep `harness/context/phase-<NN>-<slug>-context.md`.
  - Materiality test: "Record information only when omitting it could reasonably: change the approved scope …, cause a future phase to repeat discovery …".
  - Do not capture: "Routine command output, step-by-step narration, temporary dead ends that had no lasting effect, facts already owned by another canonical file …".
  - Explicit source-of-truth boundaries between the build file, the context file and `harness/build-log.md`.
  - Source: [(cookbook)](https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/codex/iterating-development-workflows-with-codex.md) [V].
- The older "Self-Evolving Agents – A Cookbook for Autonomous Agent Retraining" (2025-11-04) is archived [(registry)](https://raw.githubusercontent.com/openai/openai-cookbook/main/registry.yaml) [V].

**Cross-agent memory with explicit promotion/decay (borderline scope): cass-memory (Dicklesworthstone, alpha)**
- "Transforms scattered agent sessions into persistent, cross-agent memory" across Claude Code, Codex, Cursor, Aider, Gemini and others. "Working Memory → Diary entries; Procedural Memory → Playbook bullets", with "reflect + curate (automated)" [(README)](https://raw.githubusercontent.com/Dicklesworthstone/cass_memory_system/main/README.md) [V].
- Thresholds:
  - "90-day half-life: Confidence halves every 90 days without revalidation".
  - "4x harmful multiplier".
  - "Maturity progression: candidate → established → proven".
  - "(3 harmful marks)" invert a rule into a "PITFALL" anti-pattern.
  - "Evidence gate: Search cass for sessions where this applied … 5 sessions found, 4 successful outcomes → ACCEPT".
  - Feedback via `cm outcome success|failure <rule ids>`, and `cm reflect --days 7` by cron or post-session.
  - Source: [(README)](https://raw.githubusercontent.com/Dicklesworthstone/cass_memory_system/main/README.md) [V].

**Skill-change testing: Superpowers (Jesse Vincent / Prime Radiant; release announcement 2025-10-09)**
- `writing-skills`: "You write test cases (pressure scenarios with subagents), watch them fail (baseline behavior), write the skill …, watch tests pass (agents comply), and refactor (close loopholes). Core principle: If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing." [(SKILL.md)](https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md) [V].
- `subagent-driven-development` dispatches "a fresh subagent per task with a review after each"; the review is "two-stage (spec compliance, then code quality)" [(README)](https://raw.githubusercontent.com/obra/superpowers/main/README.md) [V].

**HALO (context-labs / inference.net; `halo-engine` first on PyPI 2026-04-29, latest 0.3.5)**
- "a methodology for building recursively self-improving agent harnesses using RLMs". The loop: collect OTEL traces → the engine "decomposes the traces to understand common failure modes across harness executions" → the report goes to "a coding agent like Cursor or Claude Code" → redeploy → repeat.
- Key caveat: "harnesses like CC would often overfit to an error present in a single/few traces rather than generalize to harness-level problems."
- Self-reported AppWorld results: dev SGC 36.8% → 52.6% and test_normal 37.5% → 48.2% for Gemini 3 Flash; 73.7% → 89.5% and 62.5% → 73.2% for Sonnet 4.6.
- Sources: [(README)](https://raw.githubusercontent.com/context-labs/halo/main/README.md), [(PyPI)](https://pypi.org/pypi/halo-engine/json) [V].

### Inferences
- Ruflo/ReasoningBank shows what a fully automated lesson store looks like: numeric priors, decay, dedup and pruning, with no human gate in the documented pipeline. For a subscription-CLI setup (no API key), the judge collapses to substring matching. Its learnings are embeddings, not reviewable diffs, which conflicts with the baseline's issue-first, reviewable skill edits. The numeric hygiene rules are worth borrowing for incidents.md: priors, prune-if-unused-for-N-days, dedup-before-add, contradiction flags. The machinery itself is not.
- oh-my-openagent and bmad-loop both say the evidence of a worker's "done" must be checked by someone other than the worker (gate reviewer, fresh review session). The baseline already does this for task outputs, but not for its own incident self-assessment.
- Claude Code's product direction puts lessons into worker context: project memory read by every thread, subagent `MEMORY.md` capped at 200 lines/25KB, and CLAUDE.md in repos. Enforcement comes through hooks (TaskCompleted/Stop) rather than prose. Hookify's "conversation analyzer → hook rule" is the clearest precedent for converting a recurring misbehaviour into a deterministic guard.
- OpenAI's cookbook loop fills the three baseline gaps together: no evals, self-grading, and no recurrence check. Incident examples become eval cases (Promptfoo). An external analyzer (HALO) ranks harness changes. A human approves the diff. The same evals are rerun afterwards. HALO's warning about overfitting to single traces supports keeping the baseline's "2+ occurrences" frequency threshold for pipeline-level changes.
- Symphony's per-session Codex token fields, attempt counter and `WORKFLOW.md` (a versioned, repo-owned agent prompt) are the minimal schema a forwarder could adopt for per-task token accounting and for moving worker-facing rules out of the orchestrator's private skill into target repos.

### Gaps
- **Conductor** (Melty Labs): nothing verified (conductor.build blocked; no repo README found).
- **Factory** (Droids; e.g. any "memory"/org-knowledge features): not verified; blocked and no search budget left. The CE README confirms only that "Factory Droid" is a supported host [(CE README)](https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/README.md) [V].
- **Cognition/Devin**: Devin "Knowledge" auto-suggestions, "Playbooks", and Walden Yan's June 2025 essay "Don't Build Multi-Agents" (context-sharing principles) are all [B], not verified this session.
- **Manus**: "Context Engineering for AI Agents: Lessons from Building Manus" (Yichao "Peak" Ji, July 2025). Lessons such as KV-cache hit rate, masking rather than removing tools, the file system as context, `todo.md` recitation, keeping errors in context, and avoiding few-shot ruts are [B], not verified this session.
- Cursor's 2026 long-running multi-agent write-ups: [B], not verified.
- How oh-my-openagent memories are written (capture side); whether Symphony has a published release date; and any Ruflo independent benchmarks: none found.
- Out-of-scope one-line pointers:
  - Single-agent memory: Claude Code auto memory (2.1.32) and subagent memory (2.1.33) [V]; Beads `bd remember` [V].
  - Academic: the Google ReasoningBank paper, ACE [B].
  - Eval/observability: `claude plugin eval` with a no-plugin baseline (2.1.269) [(docs)](https://code.claude.com/docs/en/plugin-evals) [V]; Promptfoo; HALO; Gas Town OTEL; Anthropic "Demystifying evals for AI agents" (2026-01-09) [(Anthropic)](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) [V date only].
  - Token levers: `claude plugin details` per-skill always-on vs on-invoke token cost [(docs)](https://code.claude.com/docs/en/plugins/measure) [V].

---

## 6. Anthropic's own lessons: multi-agent research system (prompt self-improvement; tool-testing agent −40% task time), writing tools with agents, context engineering, long-running harnesses, plus 2026 follow-ups

### Takeaway
Anthropic's posts describe a consistent improvement method rather than a memory product:
- Watch transcripts and traces to find failure modes.
- Let the model itself diagnose failures and rewrite prompts and tool descriptions.
- Measure with small eval sets early (about 20 cases), held-out sets, LLM-as-judge and human testers.
- Separate the doer from the grader, and calibrate the grader against a human.
- Persist state in structured files (progress logs, JSON feature lists, init scripts, git).
- Ablate harness components as models improve, because "harnesses encode assumptions that go stale".

The 40% figure applies to a narrow, testable target: tool descriptions rewritten by a tool-testing agent.

### Cited Findings
**"How we built our multi-agent research system"** (2025-06-13) [(Anthropic)](https://www.anthropic.com/engineering/multi-agent-research-system) [V]
- Results and costs:
  - An Opus 4 lead with Sonnet 4 subagents "outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval".
  - "token usage by itself explains 80% of the variance" on BrowseComp; three factors explain 95%.
  - "agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more".
- Orchestrator-side failure modes and fixes:
  - "Early agents made errors like spawning 50 subagents for simple queries, scouring the web endlessly for nonexistent sources, and distracting each other with excessive updates. Since each agent is steered by a prompt, prompt engineering was our primary lever."
  - Delegation fix: "Each subagent needs an objective, an output format, guidance on the tools and sources to use, and clear task boundaries." Vague delegation caused duplicated searches.
  - Effort scaling rules were embedded in prompts: "Simple fact-finding requires just 1 agent with 3-10 tool calls … complex research might use more than 10 subagents".
  - Method: they "built simulations … with the exact prompts and tools … then watched agents work step-by-step."
- Self-improvement: "Let agents improve themselves … Claude 4 models can be excellent prompt engineers. When given a prompt and a failure mode, they are able to diagnose why the agent is failing and suggest improvements. We even created a tool-testing agent—when given a flawed MCP tool, it attempts to use the tool and then rewrites the tool description to avoid failures. By testing the tool dozens of times, this agent found key nuances and bugs. This process … resulted in a 40% decrease in task completion time for future agents using the new description."
- Measurement:
  - "Start evaluating immediately with small samples … A prompt tweak might boost success rates from 30% to 80% … We started with a set of about 20 queries".
  - An LLM judge using "a single LLM call with a single prompt outputting scores from 0.0-1.0 and a pass-fail grade was the most consistent and aligned with human judgements". The rubric includes "tool efficiency".
  - "Human evaluation catches what automation misses": testers found agents preferring "SEO-optimized content farms", which was fixed with source-quality heuristics in prompts.
  - "full production tracing", "rainbow deployments", "end-state evaluation".
  - "Subagent output to a filesystem to minimize the 'game of telephone'."

**"Writing effective tools for agents — with agents"** (2025-09-11) [(Anthropic)](https://www.anthropic.com/engineering/writing-tools-for-agents) [V]
- The loop: prototype → "run a comprehensive evaluation" → "collaborate with an agent to help analyze your results and determine how to improve your tools".
- Metrics: "total runtime of individual tool calls and tasks, the total number of tool calls, the total token consumption, and tool errors".
- "Simply concatenate the transcripts from your evaluation agents and paste them into Claude Code. Claude is an expert at analyzing transcripts and refactoring lots of tools all at once."
- "We relied on held-out test sets to ensure we did not overfit."
- "what agents omit in their feedback and responses can often be more important than what they include."
- Example: Claude "needlessly appending 2025 to the tool's query parameter", fixed via the tool description.

**"Effective context engineering for AI agents"** (2025-09-29) [(Anthropic)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) [V]
- "the smallest possible set of high-signal tokens".
- The system prompt should sit at the "right altitude", between "brittle if-else hardcoded prompts" and vague guidance.
- Techniques:
  - Compaction, including "tool result clearing".
  - "Structured note-taking … like … your custom agent maintaining a NOTES.md file".
  - Sub-agents that return "a condensed, distilled summary of its work (often 1,000-2,000 tokens)".
  - The memory tool (public beta with Sonnet 4.5).
- "do the simplest thing that works".

**"Effective harnesses for long-running agents"** (2025-11-26, Justin Young) [(Anthropic)](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) [V]
- Initializer agent writes "an init.sh script, a claude-progress.txt file that keeps a log of what agents have done, and an initial git commit".
- Feature list: "over 200 features … all initially marked as 'failing'". Agents may only flip `passes`, with the instruction "It is unacceptable to remove or edit tests". "JSON … the model is less likely to inappropriately change or overwrite JSON files compared to Markdown".
- "work on only one feature at a time"; leave a "clean state"; "commit its progress to git with descriptive commit messages and … write summaries of its progress in a progress file".
- Failure modes: "declare the job done" early; "mark a feature as complete without proper testing", fixed by end-to-end browser testing (Puppeteer MCP).
- Session start: read progress and git log, run init.sh and a basic e2e check, which "saves Claude some tokens in every session since it doesn't have to figure out how to test the code".
- Future work: specialised "testing agent, a quality assurance agent, or a code cleanup agent".

**2026 follow-ups**
- "Building a C compiler with a team of parallel Claudes" (2026-02-05, Nicholas Carlini) [(Anthropic)](https://www.anthropic.com/engineering/building-c-compiler) [V]:
  - Scale and cost: "16 agents … Over nearly 2,000 Claude Code sessions and $20,000 in API costs … a 100,000-line compiler". "2 billion input tokens and generated 140 million output tokens … just under $20,000".
  - Coordination: via lock files in `current_tasks/` plus git.
  - Notes: "I included instructions to maintain extensive READMEs and progress files that should be updated frequently". "When stuck on a bug, Claude will often maintain a running doc of failed approaches."
  - Test harness written for the agent: "should not print thousands of useless bytes … log all important information to a file … write ERROR and put the reason on the same line so grep will find it". Against "time blindness", a `--fast` option runs "a 1% or 10% random sample" that is deterministic per agent.
  - Recurring regressions were addressed by "a continuous integration pipeline".
  - The monolithic kernel task was split using "GCC as an online known-good compiler oracle".
  - Specialised agents for dedup, performance and design critique.
  - Lesson: "the task verifier [must be] nearly perfect, otherwise Claude will solve the wrong problem".
- "Harness design for long-running application development" (2026-03-24, Prithvi Rajasekaran) [(Anthropic)](https://www.anthropic.com/engineering/harness-design-long-running-apps) [V]:
  - Design: a planner/generator/evaluator harness with negotiated "sprint contract[s]" and file-based communication.
  - Evaluator: "Out of the box, Claude is a poor QA agent … identify legitimate issues, then talk itself into deciding they weren't a big deal and approve the work anyway." The tuning loop was: "read the evaluator's logs, find examples where its judgment diverged from mine, and update the QA's prompt … several rounds".
  - Costs: Solo run 20 min for $9; full harness 6 hr for $200. The simplified Opus 4.6 harness ran about 4 hr for $124 (planner $0.46; build round 1 $71.08; QA round 1 $3.24; build round 2 $36.89; QA round 2 $3.09).
  - Principle: "every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing, both because they may be incorrect, and because they can quickly go stale as models improve". Method: "removing one component at a time". "the evaluator is … worth the cost when the task sits beyond what the current model does reliably solo."
- "Scaling Managed Agents: Decoupling the brain from the hands" (2026-04-08, Lance Martin, Gabe Cemaj, Michael Cohen) [(Anthropic)](https://www.anthropic.com/engineering/managed-agents) [V]:
  - "Harnesses encode assumptions that go stale as models improve … Sonnet 4.5 would wrap up tasks prematurely … 'context anxiety.' We addressed this by adding context resets … on Claude Opus 4.5 … the behavior was gone. The resets had become dead weight."
  - The session is "the append-only log of everything that happened", stored outside the harness (`getEvents()`). Hands are tools (`execute(name, input) → string`).
  - Latency: "p50 TTFT dropped roughly 60% and p95 dropped over 90%".
- Claude Code best-practices doc (current) [(docs)](https://code.claude.com/docs/en/best-practices) [V]:
  - "For each line, ask: 'Would removing this cause Claude to make mistakes?' If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"
  - "Treat CLAUDE.md like code: review it when things go wrong, prune it regularly, and test changes by observing whether Claude's behavior actually shifts." `/doctor` "proposes cuts for content it can derive from the codebase".
  - Hooks "are deterministic and guarantee the action happens", unlike advisory CLAUDE.md. A Stop-hook gate is "overrid[den] … after 8 consecutive blocks".
  - "a verification subagent … has a fresh model try to refute the result, so the agent doing the work isn't the one grading it."
- Background (pre-2025): "Building effective agents" (Dec 2024) is quoted in the Mar 2026 post: "find the simplest solution possible, and only increase complexity when needed" [(Anthropic)](https://www.anthropic.com/engineering/harness-design-long-running-apps) [V].

### Inferences
- Anthropic's self-improvement is human-in-the-loop, eval-anchored prompt and tool engineering: the model diagnoses, the team measures and ships. The 40% result is specific to tool descriptions tested dozens of times. For the baseline, the analogous "tools" are the dispatch envelope, the spec template, the executor-report format and the forwarder commands. A "tool-testing agent" pass over those, driven by incidents, is a narrow, measurable way to use the Anthropic result.
- The evaluator-tuning loop (compare the evaluator's verdicts with the human's, then edit the evaluator prompt) is the structural fix for the baseline's self-grading problem. The weekly human retro can be the calibration step: sample verifier verdicts and incident classifications, mark disagreements, and edit the verifier prompt or incident taxonomy.
- The "harness assumptions go stale" principle (context resets becoming dead weight; sprints removed with Opus 4.6) implies that each rule added to the skill from an incident should record which model or CLI version it compensates for. Rules should be re-ablated when Codex or Grok models change, which is CE's `retire_when` idea again.
- The C compiler post is a worked example of worker-side inefficiency fixes done at the harness level rather than in prompts: output hygiene, grep-friendly logs, `--fast` sampling, CI regressions gate, and an oracle to split monolithic tasks. Token waste was reduced by changing what workers see, not by telling them to be efficient.

### Gaps
- Anthropic does not publish the internal eval sets or the before/after prompts for the research system. The 40% figure has no confidence interval.
- It is unknown whether Anthropic uses an automated incident/lesson store for Claude Code orchestration internally.

---

## 7. Cross-cutting: worker-side vs orchestrator-side capture, who writes post-mortems, promotion thresholds, human gates, measurement, bloat control, where lessons flow, and how each maps to the user's baseline

### Takeaway
No surveyed system combines everything the user wants. The field splits into three kinds:
- **Worker-side capture** (Ralph variants, Compound Engineering, Beads, Projects memory, Codex phase-context files). Learnings flow into repo files the next worker reads.
- **Orchestrator-side hardening by humans or maintainers** (Gas Town, BMAD/bmad-loop policies, Anthropic's prompt/tool engineering, the baseline's `incidents.md`). Lessons become gates, formulas, prompts or skill edits.
- **Measured improvement loops** (OpenAI's traces → evals → HALO → Codex handoff; CE's `ce-retune`; Superpowers' RED/GREEN for skills; `claude plugin eval`). These rerun the same evals after a change.

The baseline is strong on orchestrator-side capture and human gating. Its gaps map one-to-one onto mechanisms that already exist elsewhere:
- Token and time accounting: bmad-loop, Gas Town `gt costs`, Symphony.
- Independent grading: yearbook rule, fresh reviewer, evaluator calibration.
- Recurrence and evals: Promptfoo gate, RED/GREEN, noise floor.
- Worker instruction files: snarktank AGENTS.md rules, CE `docs/solutions` + AGENTS.md pointer, Projects memory, bmad-project-context AGENTS.md block.

### Cited Findings

Comparison table. Every cell is backed by sources cited in Q1–Q6 above. "—" means not found or not documented.

| System | Worker-side inefficiency capture | Orchestrator-side error capture | Post-mortem author | Promotion threshold to "rule" | Human gate | Measurement of improvement | Bloat control | Lessons flow into |
|---|---|---|---|---|---|---|---|---|
| **User baseline** (fable-ruki-agenty) | Executors report "noticed, didn't touch"; full reports to scratchpad (not persisted to repos) | `incidents.md`, 8 misfire classes, written immediately | Orchestrator (self) + weekly human retro | 2+ open entries of one class → issue-first skill edit | Issue-first edit; weekly retro | — (known gap) | "only established rules" enter the skill | Orchestrator skill (not worker files) |
| Huntley Ralph / Playbook | AGENTS.md updated when commands needed repeated attempts; bugs → plan | Human watches loop; adds "signs" | Worker (self) + human operator | Human judgment, N=1 ("when Ralph fails a specific way") | Human "sits on the loop" | — | AGENTS.md "operational only … brief"; plan cleaned/regenerated | AGENTS.md, prompt, code utilities |
| snarktank/ralph | progress.txt "Learnings for future iterations" + nearby AGENTS.md | — | Worker (self) | "general and reusable" → Codebase Patterns / AGENTS.md | — (autonomous) | — | exclusions list; archive per feature | progress.txt, AGENTS.md |
| Anthropic ralph-loop plugin | — (files/git only) | — | — | — | max-iterations | — | n/a | files/git |
| Continuous Claude | shared notes "relay baton"; failed PRs discarded | — | Worker | — | CI + PR review | — | "keep notes clean" | notes file |
| Ralph Orchestrator | typed memories (pattern/decision/fix/context) | — | Worker / CLI `memory add` | — | — | — | 2,000-token injection budget; recency filter | `.ralph/agent/memories.md` injected per iteration |
| Compound Engineering | "What Didn't Work" incl. Claude/Codex session history | — (codebase-focused) | Orchestrator of the skill + validator subagent | Counterfactual durable/non-obvious/material bar, 1 learning/run; pack promotion when rediscovered/broader than repo | Consent for AGENTS.md edits; PR merge; refresh deletes need approval (interactive) | `ce-retune`: noise floor, A/B, pre-registered bar | refresh Keep/Update/Consolidate/Replace/Delete, `retire_when`, no archive | `docs/solutions/` read by plan & review; packs enforced in review |
| Gas Town / Beads | costs per session (Stop hook), CV/work history, `.events.jsonl` | Witness/Deacon patrols, spawn-storm detection, escalations | Maintainers + human Overseer (no automatic retro) | — | Escalation to Overseer; refinery gates | `gt costs`, OTEL metrics, Promptfoo model comparison (patrols) | Beads compaction ("memory decay") | formulas, role CLAUDE.md provisioning, `bd prime` memories, prior-attempt context |
| BMAD retrospective | epic-level artifact analysis (duplication, drift) | — | Retrospective skill (+ optional party-mode discussion) | per-epic action items | Epic gates; human discussion opt-in | Verdict "did the epic meet its bar" | source ref required per finding | `sprint-status.yaml action_items` → next sprint planning |
| bmad-loop | per-story token totals & caps; stall nudges | typed escalations CRITICAL/PREFERENCE; intent-gap | Deterministic orchestrator + fresh review session | `max_dev_attempts=2`, plateau-defer | gates per-epic; `resolve` with human | token histograms (`diagnose`) | — | policy.toml; deferred-work ledger |
| Spec Kit (+ext) | — core | — core | ext: retrospective | ext-defined | ext: "human-gated spec updates" | ext `retro`: metrics | ext `memorylint` drift checker | constitution/specs |
| Agent OS v3 | — | — | Human + `/discover-standards` | human curation | yes | — | index.yml selective injection | standards → injected into prompts/skills |
| CCPM / Taskmaster | — | — | — | — | — | — | — | GitHub issue comments (CCPM) |
| Ruflo ReasoningBank | trajectories judged by LLM (heuristic w/o API key) | — | Automated judge/distill | confidence priors 0.75/0.60; min 0.3 | none documented | internal metrics (`rb.judge.success_rate`) | prune 180d/conf<0.3; dedup 0.87; consolidate every 20 | top-k=3 memories injected |
| oh-my-openagent | evidence ledger per checkbox | independent gate reviewer | reviewer workers | — | plan approval gate | — | — | Kibitzer recall nudges; conditional rules |
| Claude Code teams / Projects / subagents | subagent memory; project memory "pitfalls" | TaskCompleted/TeammateIdle hooks (exit 2) | Claude (auto memory) / human corrections | — | plan approval auto-approved (teams) | workflows show tokens/time per phase; `claude plugin eval` | MEMORY.md 200 lines/25KB; instructions ≤16,000 chars; "prune regularly" | CLAUDE.md, skills, project memory, subagent MEMORY.md |
| OpenAI Symphony | per-session Codex token fields + attempt counter | retries with backoff | — | — | "Human Review" handoff state | — | — | in-repo `WORKFLOW.md` |
| OpenAI improvement-loop cookbook + HALO | traces | traces (harness-level failure modes) | Human + LLM feedback; HALO report | ranked by evidence across traces (HALO warns about single-trace overfit) | "developer approves the diff before merge" | Promptfoo gate rerun; AppWorld dev/test | — | harness code/prompts via Codex |
| cass-memory | diary from all agents' sessions | — | automated reflect | evidence gate (e.g. 4/5 sessions), maturity levels | — | outcome marks | 90-day half-life; harmful ×4; 3 harmful → anti-pattern | `cm context` per task |
| Anthropic research / harness posts | transcript/trace reading; tool-testing agent | lead-agent prompt fixes (e.g. 50 subagents) | team + model-as-prompt-engineer | eval-driven | yes (team) | ~20-query evals, LLM judge, held-out sets | ablate components as models improve | lead/sub-agent prompts; tool descriptions; progress/feature files |

Supporting quotes for the less obvious cells:
- The baseline's threshold and "only established rules enter the skill": local `skills/fable-ruki-agenty/SKILL.md` lines 230–232 [V].
- The worker-side inefficiency trigger ("run commands multiple times before learning the correct command") [(Playbook)](https://raw.githubusercontent.com/ghuntley/how-to-ralph-wiggum/main/README.md) [V].
- HALO's single-trace overfit warning [(HALO)](https://raw.githubusercontent.com/context-labs/halo/main/README.md) [V].
- Projects' "when you correct a thread, also tell Claude to remember the correction" [(docs)](https://code.claude.com/docs/en/claude-projects) [V].
- Wasteland "yearbook rule: you cannot stamp your own work" [(WASTELAND.md)](https://raw.githubusercontent.com/steveyegge/gastown/main/docs/WASTELAND.md) [V].
- The `claude plugin eval` no-plugin baseline: "each case's runs are repeated with no plugin loaded by default, and you get two scores, WITH and W/OUT … Catch regressions when you change the plugin or a new model is released"; three runs per case by default [(docs)](https://code.claude.com/docs/en/plugin-evals) [V].

### Inferences
Recommended plug-in points for the baseline, derived from the cited mechanisms and ordered by cost versus value:
1. **Two channels, not one.** Keep `incidents.md` for orchestrator/pipeline misfires. Add a worker-knowledge channel into target repos. The spec DoD gets one line (Huntley/snarktank trigger plus CE's durable bar): "if you needed repeated attempts to discover a command/gotcha, add ≤1–2 operational lines to the nearest AGENTS.md or a `docs/solutions/` note; otherwise report 'no learnings'." The fresh-context verifier checks the addition against an exclusion list (no story detail, no progress notes, no duplicates). This fills the "no path to worker instruction files" gap, and review happens in the same PR.
2. **Turn recurring incident classes into gates before prose.** Order of preference: test, script or hook, then skill text (CE's "narrowest durable home"; Claude Code's "hooks are deterministic"; Hookify; the Gas Town TaskCompleted spec). For example, the "missing commit" and "lost report" classes become forwarder-side checks: non-empty diff, commit SHA present, `result.json` or report file exists, like bmad-loop's artifact verification. These stop consuming prompt tokens entirely.
3. **Per-task token and time accounting in the journal.** Each ▶/↩/✔/🔁 comment should carry tokens (input/output/cache-weighted) and wall time per step. The schemas are bmad-loop's per-story totals and caps, Symphony's `codex_*_tokens`, Gas Town's Stop-hook cost capture, and Claude Code workflows' per-phase totals. This yields the first real metrics: tokens per closed issue, rework rate, time to close. Those are the numbers needed to judge whether a skill edit helped.
4. **Recurrence check as an explicit close condition.** An incident class is "fixed" only after it stays absent for N subsequent pipeline runs of comparable tasks, or after an eval replay passes. Replayable options:
   - Superpowers-style RED/GREEN: reproduce the failure without the fix, then pass with it.
   - A small Promptfoo or `claude plugin eval`-style suite built from past incident specs, with the no-skill-change baseline arm.
   - CE `ce-retune`'s noise floor before claiming improvement.
5. **Break self-grading.** The orchestrator should not both classify incidents and certify fixes. Options include a separate cheap reviewer (fresh context) that classifies incident entries, following the yearbook rule. Another is to use the weekly human retro as an evaluator-calibration step (Anthropic's "read the evaluator's logs, find … divergence … update the prompt"). A third is to run a trace-level analyzer across many journal threads rather than single incidents (HALO's overfit warning).
6. **Promotion and pruning discipline.** Keep "2+ of a class" for orchestrator-skill edits; it matches HALO's overfit warning. Use CE's materiality bar for worker learnings. Record for each rule the model/CLI version it compensates for, plus a `retire_when`. Run a periodic refresh (Keep/Update/Consolidate/Replace/Delete) with a size budget; precedents are Ralph Orchestrator's 2,000-token budget, subagent MEMORY.md at 200 lines/25KB, and Projects instructions at ≤16,000 chars. Re-ablate rules after model upgrades (Anthropic's "dead weight" finding).
7. **Rework ladder enrichment.** When escalating to a "fresh executor", pass a structured digest of prior attempts (Gas Town "prior attempt context"; bmad-loop's failing-output `--feedback`) and the verbatim original intent (BMAD's Intent Alignment Auditor). Classify failures as "intent gap" versus "implementation defect" (bmad-loop). The misunderstood-spec class then becomes measurable.
- **Where lessons should flow.** Pipeline and orchestration lessons belong in the orchestrator skill and forwarder code, which the baseline already does. Repo, tooling and command lessons belong in target-repo AGENTS.md or `docs/solutions` (Ralph, CE, Codex phase-context, Projects). Anthropic's and OpenAI's 2026 material both push toward repo-owned, versioned agent instructions (`WORKFLOW.md`, AGENTS.md as the persistent guidance Codex reads).

### Gaps
- None of the surveyed systems publishes a controlled before/after on "tokens per task" or "rework rate" attributable to a lessons loop. Quantitative effect evidence is limited to:
  - Anthropic's −40% task time (tool descriptions) and its eval anecdotes.
  - HALO's self-reported AppWorld gains.
  - Anthropic's harness cost tables.
  - Self-reported Ralph costs ($297 contract claim; RepoMirror <$800 / ~1,100 commits).
- It could not be verified whether Codex CLI or Grok CLI expose per-session token usage in a machine-readable form suitable for the forwarder. Symphony's SPEC implies Codex reports token counts, but the Codex CLI docs were not reachable.
- Several product lines (Factory, Devin, Manus, Conductor, Cursor) remain unverified in this session, so the table omits them.
