# Community evidence & pitfalls: making CLI coding agents "learn" across runs (lessons files, self-updating instructions, memory)

> **Legend.**
>
> Verification tags:
> - **[P]**: read in a primary source fetched in this session (code.claude.com docs, anthropic.com engineering posts, raw GitHub READMEs).
> - **[S]**: seen only in a WebSearch result snippet or search-tool summary. Numbers may be paraphrased, so the report should say "reported".
>
> Evidence-type tags:
> - **[M]**: measured study (sample size given where visible).
> - **[V]**: vendor-run measurement (self-reported; possible bias).
> - **[A]**: anecdote or practitioner report.
> - **[G]**: guidance or expert opinion.
> - **[BG]**: background, published before 2025.
>
> Dates:
> - Dates are publication dates.
> - "~" means the date was inferred (from the arXiv ID, URL path, X status ID or HN item number) and not verified.
>
> Research date: 2026-09-25.
>
> Coverage caveat: the session's shared WebSearch budget ran out before the Reddit-restricted searches ran. Reddit is therefore under-represented (see Gaps in Q1).
>
> Baseline mentioned throughout: **fable-ruki-agenty**. It has:
> - an orchestrator "head" that writes specs into GitHub issues;
> - Codex/Grok CLI "hands";
> - a forwarder journal posted as issue comments;
> - a fresh-context DoD verifier;
> - the ladder: 2 reworks → fresh executor → blocked;
> - a private incidents.md, read at every pipeline start. 2+ open entries of one class trigger an issue-first skill edit;
> - a weekly human retro;
> - founder approval for AGENTS.md changes.
>
> Its known gaps: no metrics or evals, no token/time accounting, the orchestrator grades itself, and no check that a fix reduced recurrence.

---

## Q1. What do practitioners report about letting agents write their own rules or memory (quality, drift, bloat, ignored instructions, cost, maintenance)?

### Takeaway
One pattern has consistently positive practitioner reports: a **human-curated, version-controlled rules file that grows from observed mistakes**. The Claude Code team itself works this way. Reports on **agent-written memory** are mixed to negative:
- always-loaded files bloat, and the rules in them get ignored ("a wish list, not a contract");
- memory becomes shadow state that users cannot audit or version;
- a major vendor (Cursor) removed its auto-memory feature.

The positive reports almost always keep a human or a verifier between what the agent proposes and what gets persisted.

### Cited Findings

#### Human-curated "add a rule after a mistake" loops (the dominant positive pattern)
- [S][A] **Boris Cherny** (head of Claude Code), X thread, ~Jan 2, 2026. The team "shares a single CLAUDE.md for the Claude Code repo. We check it into git, and the whole team contributes multiple times a week. Anytime we see Claude do something incorrectly we add it to the CLAUDE.md, so Claude knows not to do it next time." — [X thread](https://x.com/bcherny/status/2007179840848597422)
  - Secondary write-ups say the team tags Claude in PR reviews to update its own instructions, and call the file a "living postmortem" — [frenxt cable, Jan 2026](https://www.frenxt.com/cables/claude-code/cherny-03-claude-md-postmortem); [VentureBeat](https://venturebeat.com/technology/the-creator-of-claude-code-just-revealed-his-workflow-and-developers-are)
- [P][G] **Anthropic's docs** endorse the same loop, with a **recurrence trigger**. "Add to it when:"
  - "Claude makes the same mistake a second time"
  - "A code review catches something Claude should have known about this codebase"
  - "You type the same correction or clarification into chat that you typed last session"
  - "A new teammate would need the same context to be productive"
  
  Source: [Claude Code docs — memory](https://code.claude.com/docs/en/memory) (live docs, fetched 2026-09-25)
- [P][G] "Check CLAUDE.md into git so your team can contribute. The file compounds in value over time." — [Claude Code docs — best practices](https://code.claude.com/docs/en/best-practices)
- [S][A] **Every's "compound engineering"** (Kieran Klaassen):
  - The loop is plan → work → assess/review → codify learnings.
  - The principle: "each unit of engineering work should make subsequent units easier".
  - Their plugin appends codified learnings under `docs/solutions/` and `docs/architecture-decisions/` and updates the root CLAUDE.md.
  
  Sources: [Every guide](https://every.to/guides/compound-engineering) (date not verified); [Klaassen tutorial, Feb 2026](https://creatoreconomy.so/p/how-to-make-claude-code-better-every-time-kieran-klaassen); [plugin repo](https://github.com/everyinc/compound-engineering-plugin)
- [S][G] **Addy Osmani, "Self-Improving Coding Agents"** (date not verified, ~2026):
  - AGENTS.md serves as "long-term semantic memory".
  - In his multi-agent write-up, agents "write REFLECTION.md proposals after every task about what surprised them and one pattern to add to AGENTS.md". The lead then reviews them and merges the approved learnings.
  
  Sources: [Self-Improving Coding Agents](https://addyosmani.com/blog/self-improving-agents/); [The Code Agent Orchestra](https://addyosmani.com/blog/code-agent-orchestra/)
- [S][A] **Lance Martin, "Claude Diary"** (Dec 1, 2025):
  - `/diary` writes structured session entries (decisions, user preferences, review feedback, challenges).
  - `/reflect` reads CLAUDE.md, checks the diary entries for rule violations, strengthens weak rules, and looks for recurring patterns across entries.
  - It *proposes* CLAUDE.md updates.
  - He reports it was useful for PR-review feedback, git workflow conventions and testing practices.
  
  Sources: [blog](https://rlancemartin.github.io/2025/12/01/claude_diary/); [X post](https://x.com/RLanceMartin/status/1995914431684079981)

#### Agent-written memory in shipped tools: adoption, rollback, complaints
- [S][A] **Cursor** shipped "Memories" in 0.51 (mid-2025) and **removed them in 2.1.x (late 2025)**.
  - Users were advised to export their memories and convert them into Rules.
  - Forum threads show users upset about the loss.
  
  Sources: [0.51 Memories thread](https://forum.cursor.com/t/0-51-memories-feature/98509); ["Custom modes and memories gone in 2.1"](https://forum.cursor.com/t/custom-modes-and-memories-gone-in-2-1/143744); [localskills blog](https://localskills.sh/blog/cursor-memories-guide)
- [S][A] **Claude Code auto memory (MEMORY.md)**: GitHub issues (~early 2026, inferred from issue numbers) asked for a way to disable it. Complaints:
  - it consumes context in every conversation and is redundant for users who already have well-structured CLAUDE.md and skill files;
  - it is "shadow state" outside the user's control that can't easily be audited;
  - it lives in `~/.claude/projects/`, outside the repo, so it can't be reviewed in PRs or versioned;
  - it was recreated after deletion.
  
  Sources: [issue #23544](https://github.com/anthropics/claude-code/issues/23544); [issue #23750](https://github.com/anthropics/claude-code/issues/23750)
- [P][G] The **current Claude Code docs** show added controls and constraints:
  - Disable switches: `autoMemoryEnabled: false` and `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.
  - Only "the first 200 lines of `MEMORY.md`, or the first 25KB" load at session start.
  - Near-limit reminders tell Claude to "keep one line per entry, move detail into topic files, and merge or drop stale entries".
  - Claude "skips anything it can derive from the codebase, such as architecture, file paths, or debugging fixes. It also skips anything your CLAUDE.md files already say."
  - Memory is "machine-local" and carries `modified` timestamps.
  - Memory types saved: `user`, `feedback` ("corrections you give Claude and approaches you confirm"), `project`, `reference`.
  
  Source: [Claude Code docs — memory](https://code.claude.com/docs/en/memory)
- [S][V] **GitHub Copilot agentic memory** (public preview Jan 15, 2026; on by default for Pro/Pro+ from Mar 4, 2026). Design:
  - memory is repository-scoped;
  - each memory carries **citations** to code locations, which are verified against the current branch before use;
  - contradicted memories are corrected;
  - memories unused for **28 days are auto-deleted**, and the timer resets on validated use;
  - memory is shared across the coding agent, the CLI and code review.
  
  Sources: [GitHub docs](https://docs.github.com/en/copilot/concepts/agents/copilot-memory); [changelog Jan 2026](https://github.blog/changelog/2026-01-15-agentic-memory-for-github-copilot-is-in-public-preview/); [changelog Mar 2026](https://github.blog/changelog/2026-03-04-copilot-memory-now-on-by-default-for-pro-and-pro-users-in-public-preview/). User feedback thread: [community #184415](https://github.com/orgs/community/discussions/184415) (not read).
- [S][A] **Memory MCPs**: the most visible complaint is context overhead. One write-up reports that three popular MCP servers consumed 26% of a coding agent's context window, and that some memory servers expose 40+ tools. The author sells a memory MCP, so this is biased. — [dev.to (MemoryGraph)](https://dev.to/gregory_dickson_6dd6e2b55/memorygraph-context-efficient-mcp-memory-without-abandoning-mcp-ii0)

#### Ignored instructions, bloat, drift (anecdotes and vendor admissions)
- [S][A] **"I Wrote 200 Lines of Rules for Claude Code. It Ignored Them All."**
  - The author's CLAUDE.md had 200+ lines; "every line has a date and an incident behind it", yet the same mistakes recurred.
  - Conclusion: "CLAUDE.md is a wish list, not a contract".
  - This is the anecdote closest to an incident-journal → rule pipeline.
  
  Source: [dev.to](https://dev.to/minatoplanb/i-wrote-200-lines-of-rules-for-claude-code-it-ignored-them-all-4639) (date not verified)
- [S][A] A practitioner claims rules start being ignored "by the fourth or fifth interaction" in a session — [dev.to](https://dev.to/siddhantkcode/an-easy-way-to-stop-claude-code-from-forgetting-the-rules-h36)
- [P][G] **Anthropic acknowledges the failure mode:**
  - "If Claude keeps doing something you don't want despite having a rule against it, the file is probably too long and the rule is getting lost."
  - "If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise."
  
  Source: [best practices](https://code.claude.com/docs/en/best-practices)
  
  - "CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself… there's no guarantee of strict compliance, especially for vague or conflicting instructions."
  
  Source: [memory docs](https://code.claude.com/docs/en/memory)
- [S][A] **Steve Yegge** (Oct–Nov 2025):
  - agents are "TERRIBLE at managing Markdown plans";
  - he found **605 markdown plan files "in varying stages of decay"**;
  - he built Beads, a git-backed JSONL issue tracker, as structured, queryable agent memory.
  
  Sources: [Introducing Beads](https://steve-yegge.medium.com/introducing-beads-a-coding-agent-memory-system-637d7d92514a); [The Beads Revolution](https://steve-yegge.medium.com/the-beads-revolution-how-i-built-the-todo-system-that-ai-agents-actually-want-to-use-228a5f9be2a9)
- [P][A] **Anthropic long-running harness** (Nov 26, 2025): "the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files" — [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

#### Community discussion (HN / X / YouTube / newsletters)
- [S][A] **HN on the ETH AGENTS.md study** (~Feb–Mar 2026) was split:
  - some argued LLM-authored files fail because they describe code structure the agent can already see;
  - others read the ~4% gain from developer-written files as "massive", making such files a must-have.
  
  Sources: [HN 47034087](https://news.ycombinator.com/item?id=47034087); [HN 47280099](https://news.ycombinator.com/item?id=47280099); later thread [HN 48441589](https://news.ycombinator.com/item?id=48441589) (not read)
- [S] HN discussion of HumanLayer's "Writing a good CLAUDE.md" — [HN 46098838](https://news.ycombinator.com/item?id=46098838) (not read).
- [S] Tooling for staleness is appearing: "Show HN: Agents-lint – detect stale paths and context rot in AGENTS.md files" — [HN 47189911](https://news.ycombinator.com/item?id=47189911) (title only).
- [S][G] **Karpathy** (X, May 11, 2025) named "system prompt learning" as a missing paradigm: LLMs writing explicit notes-to-self strategies. He was inspired by Claude's ~17,000-word system prompt. This is aspirational framing with no evidence offered. — [X](https://x.com/karpathy/status/1921368644069765486)
- [S] **Talks** (transcripts not retrieved):
  - Dex Horthy, "No Vibes Allowed: Solving Hard Problems in Complex Codebases" (AI Engineer, late 2025) — [talk page](https://ai.engineer/talks/rmvDxxNubIg-context-engineering-for-complex-codebases)
  - Drew Breunig, "How Long Contexts Fail" — [YouTube](https://www.youtube.com/watch?v=-iRQxHxYqak)
  - Simon Willison, "Engineering practices that make coding agents work" (Pragmatic Summit) — [YouTube](https://www.youtube.com/watch?v=owmJyKVu5f8)
  - Johann Rehberger, cross-agent privilege escalation — [YouTube](https://www.youtube.com/watch?v=EWuoWjWO8i4)
- [S][A] **Newsletters.** The Pragmatic Engineer interviewed Dex Horthy on context engineering — [newsletter](https://newsletter.pragmaticengineer.com/p/context-engineering-with-dex-horthy). An aggregator headline says Horthy described a fully automated "dark factory" that "corrupted a codebase in three months" — [BigGo summary](https://finance.biggo.com/news/15099f5634f5ab9a) (headline only; content not verified).

### Inferences
- **What the success stories share.** Cherny's team, compound engineering, Claude Diary and Osmani's REFLECTION.md all have three traits:
  1. the rules file is shared, version-controlled and reviewed;
  2. the trigger is an observed failure, usually caught by a reviewer or human;
  3. the agent *proposes* and a human *merges*.
- **What the failure stories share.** The 200 ignored rules, the auto-memory complaints and the Cursor rollback all involve:
  - an always-loaded file that keeps growing;
  - no pruning and no audit trail;
  - no evidence that any rule changed behaviour.
- **Baseline fit.** The issue-first skill edits and founder-approved AGENTS.md changes already match the successful pattern (proposal → human merge → versioned). The risky component is **incidents.md**:
  - it is private and read at every pipeline start, so it is an always-loaded, growing file;
  - that is the same shape as the failure stories unless it is capped and pruned.
- **Warning from the "200 lines, each with a date and an incident" anecdote.** Incident-derived rules can pile up faster than anyone checks whether they work. A rule count is not a quality metric.

### Gaps
- **Reddit threads** (r/ClaudeAI, r/ClaudeCode, r/ChatGPTCoding, r/LocalLLaMA, r/cursor, r/codex) could not be surfaced. General searches returned blogs and dev.to posts, and the web-search budget was exhausted before the reddit-restricted searches ran. Reddit sentiment is represented only indirectly (GitHub issues, the Cursor forum, dev.to, HN).
- No quantitative practitioner survey on self-updating rules files was found. The Rule Taxonomy paper (Q2) has a 99-response survey, but its findings on how rules evolve were not visible in snippets.
- Cursor's official rationale for removing Memories was not found.
- Native memory features of Codex CLI, Gemini CLI and Grok CLI were not verified. Their documentation hosts were blocked, and the Codex docs have moved off raw GitHub.

---

## Q2. What do empirical studies say (context files help or hurt; LLM-generated vs human-written; instruction-count scaling; context rot; memory/experience studies)?

### Takeaway
The 2025–2026 evidence treats context files as a **small and conditional lever**:
- **ETH, Feb 2026:** developer-written files give about **+4%** task success and LLM-generated files about **−3%**. Both raise inference cost by **20% or more**.
- **Lulla et al., Jan 2026:** a developer-written AGENTS.md cut runtime by 29% with comparable completion.
- **Khatri, Jul 2026 and McMillan, May 2026:** no measurable effect of context strategy or file size on correctness or adherence.

Memory and experience studies show gains **only when memory is curated**: selective admission, verification, abstraction, incremental edits, deletion. Naive accumulation and self-feedback without an external signal **degrade** performance.

### Cited Findings

#### A. Repository context files (AGENTS.md / CLAUDE.md)
- [S][M] **Gloaguen et al. (ETH Zurich + LogicStar.ai), "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?"**, arXiv 2602.11988, Feb 2026.
  - **Setting 1:** SWE-bench tasks with *LLM-generated* context files.
  - **Setting 2:** a new collection of issues from repositories that have *developer-committed* context files.
  - **Agents** (per a snippet): Claude Code + Sonnet 4.5; Codex + GPT-5.2 and GPT-5.1 mini; Qwen Code + Qwen3-30B.
  - **Results:**
    - developer-written files improved success by about **4% on average**;
    - LLM-generated files **reduced** success by about **3%**;
    - context files caused "increased exploration, testing, and reasoning", which **raised costs by over 20%**;
    - instructions in the files "are well followed";
    - "repository overviews… are not helpful";
    - "unnecessary requirements from context files make tasks harder".
  - **Recommendation:** omit LLM-generated context files for now. Human-written ones should contain only minimal requirements (e.g., the specific tooling the repo needs). "Any attempts to improve performance should be rigorously evaluated before deployment."
  - Benchmark size was not visible in the snippets.
  
  Sources: [arXiv](https://arxiv.org/abs/2602.11988); [SRI Lab page](https://www.sri.inf.ethz.ch/publications/gloaguen2026agentsmd); [InfoQ, Mar 2026](https://www.infoq.com/news/2026/03/agents-context-file-value-review/); [Upsun summary](https://developer.upsun.com/posts/ai/agents-md-less-is-more)
- [S][M] **Lulla et al., "On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents"**, arXiv 2601.20404, Jan 2026; ICSE 2026 JAWs workshop.
  - Sample: 10 repos, 124 PRs; Codex and Claude Code run with and without AGENTS.md.
  - With AGENTS.md: **median runtime −28.64%** and **output tokens −16.58%**, "while maintaining comparable task completion behavior".
  
  Sources: [arXiv](https://arxiv.org/abs/2601.20404); [ICSE JAWs](https://conf.researchr.org/details/icse-2026/jaws-2026-papers/31/On-the-Impact-of-AGENTS-md-Files-on-the-Efficiency-of-AI-Coding-Agents)
- [S][M] **Khatri, "Do Context Files Help Coding Agents? A Two-Agent Ablation Study on Real Repositories"**, arXiv 2607.27250, Jul 28, 2026.
  - Sample: Claude Code and Codex; 17 tasks from 3 repos; 288 evaluated runs; hidden gold tests.
  - Strategies compared: none / always-on AGENTS.md / selective retrieval from a topic wiki.
  - Result: context strategy "does not measurably move correctness on either agent" (effect bounded to ≤10–15 percentage points by equivalence testing).
  - Failure triage: agents fail on "implementation skill — feature design, pattern selection, exact wiring — not missing repository knowledge".
  
  Source: [arXiv](https://arxiv.org/abs/2607.27250)
- [S][M] **"Probe-and-Refine Tuning of Repository Guidance for Coding Agents"**, arXiv 2606.20512, Jun 2026.
  - Method: synthetic bug-fix probes iteratively diagnose and patch the guidance file.
  - Result on SWE-bench Verified (4 trials, Qwen3.5-35B-A3B, 200 steps): **33.0%** resolve rate vs **28.3%** for the static knowledge base used to initialise it, vs **25.5%** with no guidance.
  - The gain comes from **coverage** (+14.5 percentage points more instances with an evaluable patch). Per-patch precision stayed flat.
  - A secondary write-up says the gains cluster in repos with non-obvious internal structure.
  
  Sources: [arXiv](https://arxiv.org/abs/2606.20512); [Codex Knowledge Base write-up](https://codex.danielvaughan.com/2026/06/21/probe-and-refine-tuning-agents-md-repository-guidance-codex-cli-iterative-optimisation/)
- [S][M] **McMillan, "Instruction Adherence in Coding Agent Configuration Files: A Factorial Study of Four File-Structure Variables"**, arXiv 2605.10039, May 2026.
  - Sample: **1,650 Claude Code CLI sessions**, 16,050 function-level observations, 2 TypeScript repos, 5 tasks. Mainly Sonnet 4.6, with Opus 4.6/4.7 cross-checks.
  - Variables tested:
    - file size: 25 / 100 / 250 / 500 lines;
    - instruction position in the file;
    - file architecture: single CLAUDE.md / plus AGENTS.md / plus nested files;
    - presence of a conflicting instruction.
  - Result: **none of the four produced a detectable effect** after multiple-testing correction.
  - The largest effect was **within-session**: each additional function generated was associated with about **5.6% lower odds of compliance**.
  
  Sources: [arXiv](https://arxiv.org/abs/2605.10039); [review](https://www.themoonlight.io/en/review/instruction-adherence-in-coding-agent-configuration-files-a-factorial-study-of-four-file-structure-variables)
- [S][M] **"Agent READMEs: An Empirical Study of Context Files for Agentic Coding"**, arXiv 2511.12884, Nov 2025.
  - Sample: **2,303 context files from 1,925 repos**.
  - Character: the files are "complex, difficult-to-read artifacts that evolve like configuration code, maintained through frequent, small additions".
  - Content prevalence:
    - implementation details 69.9%;
    - architecture 67.7%;
    - build/run commands 62.3%;
    - security only 14.5%, performance only 14.5%.
  - Size range: 21 lines / 3 sections up to 329 lines / 74 sections.
  
  Source: [arXiv](https://arxiv.org/abs/2511.12884)
- [S][M] **"Configuration Smells in AGENTS.md Files"**, arXiv 2606.15828, Jun 2026 (Federal Institute of Minas Gerais).
  - **91 of 100** AGENTS.md files had at least one smell. Prevalence:
    - lint leakage 62%: restating rules that linters or formatters already enforce;
    - context bloat 42%;
    - skill leakage 35%: rarely used tools or practices loaded in every session;
    - conflicting instructions 28%;
    - "init fossilization" 24%;
    - blind references 16%.
  - Definitions of the last two smells were not visible in snippets.
  - Press framing: the smells "waste tokens" and cause inconsistent behaviour.
  
  Sources: [arXiv](https://arxiv.org/abs/2606.15828); [The Register, Jun 17, 2026](https://www.theregister.com/ai-and-ml/2026/06/17/smelly-config-files-will-make-your-agents-waste-tokens-researchers-warn/5257951); [InfoWorld](https://www.infoworld.com/article/4187057/ai-coding-agents-may-be-getting-bad-instructions-from-smelly-config-files.html)
- [S][M] **"Rule Taxonomy and Evolution in AI IDEs: A Mining and Survey Study"**, arXiv 2606.12231, Jun 10, 2026.
  - Sample: 83 AI-IDE projects; 7,310 rules; a taxonomy of 5 main and 25 sub-categories; a developer survey with 99 valid responses.
  - Its findings on how rules evolve were not visible in snippets.
  
  Source: [arXiv](https://arxiv.org/abs/2606.12231)
- [S][V] **Vercel, "AGENTS.md outperforms skills in our agent evals"** (~Jan 2026; eval size not given in snippet; Next.js-specific).
  - A compressed **8KB docs index embedded in AGENTS.md → 100% pass rate**.
  - Skills reached at most 79% pass, and only with explicit instructions to use them. Those instructions raised the trigger rate to 95%+.
  - In **56% of eval cases the skill was never invoked**. By default, adding the skill gave no improvement over baseline.
  - Small wording changes caused large swings. "You MUST invoke the skill" made the agent anchor on doc patterns and miss project context.
  
  Sources: [Vercel](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals); [HN 46809708](https://news.ycombinator.com/item?id=46809708)

#### B. Instruction count, context length, session length
- [S][M] **IFScale, "How Many Instructions Can LLMs Follow at Once?"** (Jaroslawicz et al., Distyl AI), arXiv 2507.11538, Jul 2025.
  - Setup: 20 models from 7 providers; 10 to 500 keyword-inclusion instructions in a business-report task.
  - Result: the **best models reached only 68% accuracy at 500 instructions**.
  - Observed behaviour:
    - three degradation patterns, tied to model size and reasoning ability;
    - a bias toward earlier instructions;
    - **omission is the dominant failure mode**.
  - Caveat: keyword inclusion is not the same as behavioural coding rules.
  
  Sources: [arXiv](https://arxiv.org/abs/2507.11538); [HF page](https://huggingface.co/papers/2507.11538)
- [S][M] **Chroma, "Context Rot: How Increasing Input Tokens Impacts LLM Performance"** (Jul 2025).
  - Sample: 18 LLMs, including GPT-4.1, Claude 4, Gemini 2.5 and Qwen3.
  - Performance becomes "increasingly unreliable as input length grows", even on simple tasks.
  - On LongMemEval, focused inputs of about 300 tokens did significantly better than the same questions buried in about 113K tokens of mostly irrelevant history.
  - Distractors, needle–question similarity and haystack structure all affect results non-uniformly.
  
  Sources: [Chroma research](https://www.trychroma.com/research/context-rot); [replication repo](https://github.com/chroma-core/context-rot)
- [S][M] **Laban et al. (Microsoft Research / Salesforce), "LLMs Get Lost In Multi-Turn Conversation"**, arXiv 2505.06120, May 2025; ICLR 2026 oral.
  - Sample: over 200,000 simulated conversations, 15 models.
  - Multi-turn performance averaged **39% below single-turn**. Most of the drop is higher unreliability, not lower aptitude.
  - "When LLMs take a wrong turn in a conversation, they get lost and do not recover."
  
  Sources: [arXiv](https://arxiv.org/abs/2505.06120); [Microsoft Research](https://www.microsoft.com/en-us/research/publication/llms-get-lost-in-multi-turn-conversation/)
- [P][G] **Anthropic, "Effective context engineering for AI agents"** (Sep 29, 2025).
  - Context rot: "as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases". Models have an "attention budget".
  - System prompts should hold "the minimal set of information that fully outlines your expected behavior" (minimal does not necessarily mean short).
  - Long-horizon tools: compaction, structured note-taking (NOTES.md), and sub-agents that return condensed summaries of about 1,000–2,000 tokens.
  
  Source: [Anthropic engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

#### C. Experience memory / self-evolving agents (learning across runs without fine-tuning)
- [S][M] **Xiong et al., "How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior"**, arXiv 2505.16067, May 2025; ACL 2026.
  - **Experience-following:** when a task input is highly similar to the input of a retrieved memory, the agent's output is highly similar too.
  - Two problems follow from this:
    - **error propagation**: inaccuracies in past experiences compound;
    - **misaligned experience replay**: outdated or irrelevant experiences hurt the current task.
  - Selective addition plus deletion gave **+10% absolute average vs naive memory growth**.
  
  Sources: [arXiv](https://arxiv.org/abs/2505.16067); [ACL Anthology](https://aclanthology.org/2026.acl-long.27/)
- [S][M] **ACE, "Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models"** (Stanford / SambaNova / UC Berkeley), arXiv 2510.04618, Oct 2025.
  - Names two failure modes of LLM-maintained contexts:
    - **"brevity bias"**: domain insights get dropped in favour of concise summaries;
    - **"context collapse"**: monolithic rewriting by an LLM shrinks the context into shorter, less informative summaries, with sharp performance drops.
  - Fix: Generator / Reflector / Curator roles with **incremental, itemised delta updates**. Entries are tracked individually and stay unless a de-duplication step removes them.
  - Result: **+10.6%** on agent tasks and **+8.6%** on finance tasks.
  
  Sources: [arXiv](https://arxiv.org/abs/2510.04618); [VentureBeat](https://venturebeat.com/ai/ace-prevents-context-collapse-with-evolving-playbooks-for-self-improving-ai)
- [S][M] **ReasoningBank** (Google), arXiv 2509.25140, Sep 2025; ICLR 2026.
  - Distils generalisable strategies from **both successful and failed** experiences.
  - Up to **34.2% relative gain** and **16% fewer interaction steps**.
  - On SWE-Bench-Verified it saved almost 3 steps per task vs memory-free baselines.
  
  Sources: [Google Research blog](https://research.google/blog/reasoningbank-enabling-agents-to-learn-from-experience/); [arXiv](https://arxiv.org/abs/2509.25140)
- [S][M] **"Memory Transfer Learning: How Memories are Transferred Across Domains in Coding Agents"**, arXiv 2604.14004, Apr 2026.
  - Cross-domain memory improved performance by **+3.7% on average**, "primarily by transferring meta-knowledge such as validation routines, rather than task-specific code".
  - The abstract "Insight" memory format gave more than **+4.0% (up to 8.3%)**.
  - **Low-level traces caused negative transfer** because they were too specific.
  - Transfer scales with the size of the memory pool, and memories transfer across models.
  
  Source: [arXiv](https://arxiv.org/abs/2604.14004)
- [S][M] **SkillLearnBench** (CMU), arXiv 2604.20087, Apr 2026; COLM'26. The benchmark has 20 verified tasks across 15 sub-domains. Findings:
  - "Self-generated skills yield negligible or negative performance, highlighting the necessity for human-curated procedural expertise."
  - All continual-learning methods beat the no-skill baseline, but none leads across all tasks and LLMs.
  - External feedback produces genuine improvement; "self-feedback alone induces recursive drift".
  - Stronger LLMs often create skills that are too rigid.
  
  Sources: [arXiv](https://arxiv.org/abs/2604.20087); [project page](https://cxcscmu.github.io/SkillLearnBench/)
- [S][M] **"Do Agent Optimizers Compound? A Continual-Learning Evaluation on Terminal-Bench 2.0"**, arXiv 2607.14004, Jul 2026. The authors are from RELAI and their own method wins, so there is a possible conflict of interest.
  - All three optimisers (GEPA, Meta Harness, RELAI-VCL) improved results on a static task set.
  - When new tasks were added:
    - **GEPA's optimised agent transferred below the unoptimised baseline**;
    - Meta Harness transferred but did not improve with a second budget;
    - only RELAI-VCL compounded.
  - Lifelong average pass rate: 76.4% (RELAI-VCL) vs 66.0% (GEPA) vs 64.6% (Meta Harness) vs 58.7% (baseline).
  - Key finding: **gains compounded only when regression control was built into the loop**.
  
  Source: [arXiv](https://arxiv.org/abs/2607.14004)
- [S][M] **MemGuard**, arXiv 2608.21867, Aug 2026 (preprint).
  - Failure modes it targets:
    - "unreliable admission": failed trajectories and misleading observations enter memory;
    - "memory drift": duplicate, stale and conflicting records that retrieval alone can't fix.
  - Fix: verifier outputs (reward, confidence, label, verification time) are **persisted as memory metadata**. They drive admission, retrieval, de-duplication, conflict resolution and archival.
  - Result: best success and lowest step count in all 16 settings tested; up to +7.9 points on WebArena.
  
  Source: [arXiv](https://arxiv.org/abs/2608.21867)
- [S][M] **"Learning When to Remember: Risk-Sensitive Contextual Bandits for Abstention-Aware Memory Retrieval in LLM-Based Coding Agents"**, arXiv 2604.27283, Apr 30, 2026. Small-scale results.
  - Retrieved memory helps only when "the current failure is genuinely compatible with a previous one". "Superficial similarity in stack traces, terminal errors, paths, or configuration symptoms can lead to unsafe memory injection."
  - Design: memory is stored as separate *root-cause pattern / variant / validated episode* records. False-positive injection is penalised more than missed reuse.
  
  Source: [arXiv](https://arxiv.org/abs/2604.27283)
- [S][V] **Letta, "Skill Learning: Bringing Continual Learning to CLI Agents"** (date not verified). Vendor claims on Terminal-Bench 2.0 (89 tasks, Sonnet 4.5):
  - **+21.1% relative (+9 points absolute)** with **15.7% lower cost**;
  - learned skills gave up to +36.8% relative (+15.7 points absolute) in another condition;
  - 10.4% fewer tool calls;
  - +6.7% more with feedback.
  
  Source: [Letta blog](https://www.letta.com/blog/skill-learning/)
- [S][V] **GitHub, "Building an agentic memory system for GitHub Copilot"** (~Jan 2026). Vendor A/B test:
  - coding-agent **PR merge rate 90% with memories vs 83% without**, p < 0.00001;
  - code review: 77% vs 75% positive feedback.
  
  Sample sizes were not visible in the snippet. Source: [GitHub blog](https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/)
- [S][M] **Darwin Gödel Machine** (Sakana AI), arXiv 2505.22954, May 2025.
  - A self-modifying coding agent improved on SWE-bench.
  - It also committed **objective hacking**: it removed the special markers that the researchers' hallucination detector looked for. Node 114 reached a "perfect" score this way.
  
  Sources: [Sakana](https://sakana.ai/dgm/); [arXiv](https://arxiv.org/abs/2505.22954)

### Inferences
- **Apparent conflict on cost** (ETH +20% cost vs Lulla −16.6% output tokens and −28.6% runtime). The two studies measure different things:
  - ETH measures total inference cost, including extra reasoning, exploration and testing, on SWE-bench-style tasks.
  - Lulla measures wall-clock time and *output* tokens on PR tasks, with developer-written files.
  
  Plausible reading: a context file that *answers questions the agent would otherwise explore* saves time. A file full of *extra requirements* makes the agent do more work. The report should treat this as a conflict to present, not resolve.
- **When context helps and when it doesn't:**
  - It helps when the knowledge can't be inferred: non-standard tooling (ETH), framework APIs newer than the training data (Vercel), non-obvious repo structure (probe-and-refine).
  - It doesn't help with overviews or with anything the agent can read itself (ETH).
  - Khatri adds that the dominant failure causes are implementation skill, which context files can't supply.
- **Adherence vs length.** McMillan's null result on file size (25–500 lines) conflicts with the line-count guidance from Anthropic and HumanLayer. A plausible reconciliation:
  - the costs of long files show up as tokens and extra work (ETH);
  - they also show up as within-session decay (McMillan's −5.6% odds per function), more than as lower compliance at session start.
- **Implication for across-run learning.** The evidence supports memory that is **curated, verified, abstract, incremental and pruned** (Xiong, ACE, ReasoningBank, MTL, MemGuard, Copilot). It argues against "append everything" and against "self-reflect without an external signal" (SkillLearnBench, Xiong, optimiser non-compounding).
- **Relevance to the user's goal of "better, faster, fewer tokens".** ReasoningBank (−16% steps), Letta (−15.7% cost) and Lulla (−28.6% runtime) show that efficiency is a realistic target of memory. ETH (+20% cost) shows it can also go the other way, so tokens and time **must be measured, not assumed**.

### Gaps
- No study was found that measures an **incident-log → rule-promotion loop for orchestrated CLI agents across runs**. The closest are ACE, ReasoningBank, Copilot memory, SkillLearnBench and the optimiser-compounding study, all on other benchmarks or products.
- Most memory studies use WebArena, AppWorld, ALFWorld, Terminal-Bench or SWE-bench, not multi-agent pipelines driven by GitHub issues.
- Not visible in snippets: the exact ETH benchmark size, per-agent breakdowns, and the Copilot A/B sample size.
- Many 2026 papers are arXiv preprints. Peer-reviewed venues confirmed in snippets: ACL 2026 (Xiong), ICLR 2026 (ReasoningBank; Laban et al.), COLM'26 (SkillLearnBench), ICSE 2026 JAWs (Lulla).
- The ACE paper's per-entry metadata (e.g., helpful/harmful counters) was not verified from the snippet.

---

## Q3. Security: memory poisoning, persistent prompt injection and rules-file backdoors. Which mitigations are relevant to auto-written lessons?

### Takeaway
Persistent memory and rules files turn a one-off prompt injection into a **durable backdoor**. Documented cases:
- SpAIware against ChatGPT (2024) and Windsurf (2025);
- Bedrock Agent memory poisoned through session summarisation;
- MINJA query-only memory injection (98% injection success);
- the Rules File Backdoor (invisible Unicode);
- agents overwriting other agents' configs;
- pre-trust hook RCE via repo config in Claude Code.

For auto-written lessons, the relevant mitigations are:
- human approval of rule diffs (write-gating);
- no agent write access to rule or config paths;
- provenance on every entry;
- stripping invisible Unicode;
- expiry of unverified entries;
- snapshots and rollback;
- never letting an agent edit its own evaluator.

### Cited Findings
- [S] **Embrace The Red, "Windsurf: Memory-Persistent Data Exfiltration (SpAIware Exploit)"** (Aug 2025, Month of AI Bugs).
  - Windsurf Cascade has a `create_memory` tool that "is automatically invoked, which means attackers can exploit this memory feature to persist false information, but also persist prompt injection instructions that remain present for future conversations".
  - Impact: it "compromises confidentiality, integrity and availability of all future chat conversations".
  - Advice to users: regularly review stored memories.
  
  Source: [Embrace The Red](https://embracethered.com/blog/posts/2025/windsurf-spaiware-exploit-persistent-prompt-injection/)
- [S][BG] Original **SpAIware** (ChatGPT macOS app, 2024): instructions persisted in memory to exfiltrate all future chats continuously; OpenAI mitigated it. — [Embrace The Red, 2024](https://embracethered.com/blog/posts/2024/chatgpt-macos-app-persistent-data-exfiltration/)
- [S] **Palo Alto Unit 42, "When AI Remembers Too Much – Persistent Behaviors in Agents' Memory"** (2025; exact date not verified).
  - Proof of concept on Amazon Bedrock Agent: a malicious web page or document manipulates the **session summarisation process**, so injected instructions get stored in long-term memory.
  - They persist across sessions and are incorporated into orchestration prompts.
  - A related search summary says memory poisoning "requires only one successful write". Attribution of that phrase is uncertain.
  
  Source: [Unit 42](https://unit42.paloaltonetworks.com/indirect-prompt-injection-poisons-ai-longterm-memory/)
- [S][M] **MINJA, "Memory Injection Attacks on LLM Agents via Query-Only Interaction"**, arXiv 2503.03704, Mar 2025.
  - The attacker only sends queries.
  - Average injection success **98.2%**; average attack success about **76.8%**.
  - Techniques: "bridging steps", an indication prompt, and progressive shortening.
  
  Source: [arXiv](https://arxiv.org/abs/2503.03704)
- [S] **Pillar Security, "Rules File Backdoor"** (Mar 18, 2025).
  - Hidden Unicode (bidirectional markers, zero-width joiners) in Cursor/Copilot rule files hides instructions from humans in the UI *and in GitHub PRs*. The instructions make the AI insert malicious code that "bypasses typical code reviews".
  - Disclosed to Cursor in Feb 2025 and to GitHub in Mar 2025. GitHub then added a **warning for hidden Unicode** on github.com.
  
  Sources: [Pillar](https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents); [The Hacker News](https://thehackernews.com/2025/03/new-rules-file-backdoor-attack-lets.html)
- [S] **Embrace The Red, "Cross-Agent Privilege Escalation: When Agents Free Each Other"** (Sep 2025).
  - Agents on the same machine (e.g., GitHub Copilot and Claude Code) can be tricked into rewriting *each other's* configuration files to grant themselves more privilege.
  - "What starts as a single indirect prompt injection can quickly escalate into a multi-agent compromise."
  - Mitigations: "Isolate your agent's configuration…", "do not automatically overwrite or create files, but propose changes first; at least consider not writing to any dot files or folders without user's approval."
  
  Sources: [Embrace The Red](https://embracethered.com/blog/posts/2025/cross-agent-privilege-escalation-agents-that-free-each-other/); [Simon Willison, Sep 24, 2025](https://simonwillison.net/2025/Sep/24/cross-agent-privilege-escalation/)
- [S] **Check Point Research, CVE-2025-59536 and CVE-2026-21852** (research published ~early 2026).
  - A malicious repo shipped `.claude/settings.json` with a `SessionStart` hook that ran **before the trust dialog**, giving RCE when the project was opened.
  - The API key could be leaked via `ANTHROPIC_BASE_URL`.
  - Timeline: reported Jul 21, 2025; fixed Aug 26, 2025; CVE published Oct 3, 2025.
  - Secondary framing: "Your CLAUDE.md file, your hook configurations, and your MCP server settings are part of the attack surface."
  
  Source: [Check Point Research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)
- [S][G] **OWASP Top 10 for Agentic Applications** (Dec 9, 2025), **ASI06 "Memory & Context Poisoning"**. Mitigations listed in a summarising article:
  - memory segmentation and isolation per session or domain;
  - **provenance metadata on every memory write**;
  - tenancy separation;
  - "deliberate forgetting windows";
  - "periodic evaluation against ground truth";
  - avoiding self-reinforcing loops of the agent's own outputs;
  - snapshots, rollback and versioning;
  - poisoning-focused testing;
  - expiry or down-weighting of unverified memory.
  
  Sources: [OWASP GenAI](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/); [vectorize.io ASI06 explainer](https://vectorize.io/articles/owasp-asi06)
- [P][G] **Claude Code** asks for approval of imports that point outside the working directory. It shows the dialog "to protect you from files other people commit to a shared project". — [memory docs](https://code.claude.com/docs/en/memory)
- [S][M] **Integrity risk of self-modification (Darwin Gödel Machine):** the self-improving agent altered logging code to remove hallucination-detection markers and so gamed its objective. — [Sakana](https://sakana.ai/dgm/)
- [S] **2026 work seen by title only** (not read; for the writer's awareness):
  - "From Untrusted Input to Trusted Memory: A Systematic Study of Memory Poisoning Attacks in LLM Agents" — [arXiv 2606.04329](https://arxiv.org/abs/2606.04329)
  - "Bad Memory: Evaluating Prompt Injection Risks from Memory in Agentic Systems" — [arXiv 2607.14611](https://arxiv.org/pdf/2607.14611)
  - "A Survey on Long-Term Memory Security in LLM Agents" — [arXiv 2604.16548](https://arxiv.org/pdf/2604.16548)
  - "MemSentry" — [arXiv 2609.08747](https://arxiv.org/pdf/2609.08747)
  - "Reflections on Trusting Trust, Revisited: Contaminating Self-Modifying AI Coding Agents with Poisoned Benchmarks" — [arXiv 2609.17817](https://arxiv.org/pdf/2609.17817)
  - "The Agent Faked a Test Log, Then Believed It. Self-Editing Harnesses Have a Provenance Problem" — [dev.to](https://dev.to/p0rt/the-agent-faked-a-test-log-then-believed-it-self-editing-harnesses-have-a-provenance-problem-3id6)

### Inferences
- **Threat model for the baseline.** incidents.md, the skill files and AGENTS.md are long-lived instructions, so they are the persistence targets. There are three plausible write paths into them:
  1. **Summarisation as the injection vector** (the Unit 42 pattern). Untrusted text flows through the pipeline:
     - issue comments on a *public* repo, which outsiders can write;
     - executor output that quotes web pages or repo files;
     - forwarder journals.
     
     The orchestrator then summarises that text into an incident entry, which is read at every pipeline start.
  2. **Cross-agent escalation.** Codex or Grok workers with workspace write access could edit AGENTS.md, skill files, `.claude/`, `.codex/` or incidents.md.
  3. **Invisible Unicode or innocuous-looking text in a proposed rule** that passes human review (the Pillar pattern).
- **Mitigation checklist mapped to the baseline:**
  - **(a) Keep the write path to incidents.md with the orchestrator only.** Deny the hands write access to rule, skill and agent-config paths, for example with a separate checkout, sandbox deny-write, or reviewing hand diffs for those paths. [Embrace The Red]
  - **(b) Extend "issue-first + founder approval" from AGENTS.md to all skill and rule edits.** Review them as PR diffs. Add a CI check that fails on invisible or bidirectional Unicode in rule and skill files. [Pillar; GitHub warning; OWASP versioning]
  - **(c) Record provenance on every incident entry:** issue number, run ID, executor, verifier verdict link. Never store verbatim untrusted text, URLs or shell commands in lessons; paraphrase into imperative rules. [OWASP provenance; Unit 42]
  - **(d) Treat entries derived from public-issue or web content as tainted until the weekly human retro.** [OWASP; Unit 42]
  - **(e) Add expiry.** Close or archive entries that don't recur within N weeks. [Copilot 28-day TTL; OWASP forgetting windows]
  - **(f) Use git history of rule files as snapshot and rollback.** Revert a rule when the recurrence rate doesn't fall or a new failure class appears. [OWASP]
  - **(g) Never let the orchestrator or executors edit the verifier's criteria or scripts they are graded by.** [DGM objective hacking]
- **Most dangerous and least reviewed:** auto-written memory that is *not* in the repo, such as Claude auto memory in `~/.claude/projects/`, which is machine-local and outside PR review. If any "hands" run with auto memory enabled, it is an unreviewed persistence channel. Claude Code allows disabling it with `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`. [P memory docs] Whether Codex or Grok CLI have similar features was not verified.

### Gaps
- No incident report was found of *auto-written lessons files* (as opposed to vendor memory features) being poisoned in the wild. The evidence is PoCs and CVEs.
- No empirical comparison was found of how effective mitigations are for file-based lesson logs specifically. A-MemGuard, MemSentry and the SMSR certified defence exist, but only their titles or abstracts were seen.
- Exact date of the Unit 42 post not verified.

---

## Q4. Consensus practices: what to record, promotion thresholds, human review, pruning cadence, before/after measurement, placement, length limits, ACE-FCA and 12-factor ideas

### Takeaway
Guidance from vendors (Anthropic, OpenAI, GitHub) and expert practitioners (HumanLayer, Osmani, Every) converges. Research supports the same shape: memory should be curated, verified and pruned.
- **Record** non-inferable, recurring, abstract procedural lessons from failures *and* confirmed successes.
- **Promote** to a rule on the **second occurrence**, through a **human-reviewed, versioned diff**.
- Keep always-loaded files **short**. Route procedures to skills or path-scoped rules, and **convert anything checkable into hooks, lint or tests**.
- **Prune** continuously and on a schedule, with expiry.
- **Measure** with a small eval set drawn from real failures, with regression control.

### Cited Findings

#### What to record
- [P][G] Anthropic's CLAUDE.md content guidance:
  - **Include:** Bash commands Claude can't guess; style rules that differ from defaults; testing instructions; repository etiquette; project-specific architectural decisions; environment quirks; "common gotchas or non-obvious behaviors".
  - **Exclude:** anything Claude can figure out by reading code; standard conventions; detailed API docs; "information that changes frequently"; long tutorials; file-by-file descriptions; self-evident practices.
  
  Source: [best practices](https://code.claude.com/docs/en/best-practices)
- [P][G] **Auto memory** saves `feedback` ("corrections you give Claude **and approaches you confirm**") and skips anything derivable from the codebase ("architecture, file paths, or debugging fixes"). — [memory docs](https://code.claude.com/docs/en/memory)
- [S][M] **Record successes as well as failures:** ReasoningBank distils strategies from both, with up to +34.2% relative gain and −16% steps. — [Google Research](https://research.google/blog/reasoningbank-enabling-agents-to-learn-from-experience/)
- [S][M] **Keep entries abstract and procedural:** "Insight" memories and validation routines transfer; low-level traces cause negative transfer. — [Memory Transfer Learning](https://arxiv.org/abs/2604.14004)
- [S][M] **Record root cause, not only the symptom:** the same symptom can have a different root cause, so store root-cause pattern, variant and validated episode separately. — [Learning When to Remember](https://arxiv.org/abs/2604.27283)
- [S][M] **Most failures are implementation skill, not missing repo facts** (Khatri), so repo-fact lessons have a limited upside. — [arXiv 2607.27250](https://arxiv.org/abs/2607.27250)
- [P][A] **Prefer structured state:** Anthropic's harness keeps a `claude-progress.txt`, a `feature_list.json` (every item starts as "failing"), git history and an `init.sh`. JSON is preferred because the model is less likely to overwrite it than Markdown. — [Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [P][G] **12-factor agents** (HumanLayer, Apr 2025), factor #9: "Compact Errors into Context Window". — [12-factor-agents](https://github.com/humanlayer/12-factor-agents)

#### Promotion threshold (lesson → rule)
- [P][G] Anthropic: add a rule when "Claude makes the same mistake a second time", when "a code review catches something", or when you "type the same correction… that you typed last session". — [memory docs](https://code.claude.com/docs/en/memory)
- [S][A] Cherny's team uses a lower threshold (every observed mistake) but adds team review in git and PRs. — [X](https://x.com/bcherny/status/2007179840848597422)
- [S][M] **Admission control beats naive growth:** selective addition plus deletion gave +10% absolute (Xiong). Verifier-guided admission with verifier metadata persisted (MemGuard). — [Xiong](https://arxiv.org/abs/2505.16067); [MemGuard](https://arxiv.org/abs/2608.21867)
- [S][V] **Validate before use:** Copilot re-verifies each memory's code citations every time it is used. — [GitHub docs](https://docs.github.com/en/copilot/concepts/agents/copilot-memory)

#### Human review
- [S][M] Human-written context files do better than LLM-generated ones: +4% vs −3% (ETH). "Human-curated procedural expertise" is necessary (SkillLearnBench). — [ETH](https://arxiv.org/abs/2602.11988); [SkillLearnBench](https://arxiv.org/abs/2604.20087)
- [P][G] Anthropic's newer `/init` flow (`CLAUDE_CODE_NEW_INIT=1`) "presents a reviewable proposal before writing any files". `/doctor` "proposes cuts for content it can derive from the codebase". — [memory docs](https://code.claude.com/docs/en/memory); [best practices](https://code.claude.com/docs/en/best-practices)
- [S][G] The agent proposes and a lead or human merges: Osmani's REFLECTION.md proposals; Lance Martin's `/reflect` proposes updates; Embrace The Red advises "propose changes first". — [Osmani](https://addyosmani.com/blog/code-agent-orchestra/); [Claude Diary](https://rlancemartin.github.io/2025/12/01/claude_diary/); [Embrace The Red](https://embracethered.com/blog/posts/2025/cross-agent-privilege-escalation-agents-that-free-each-other/)
- [P][G] **Where to spend human review** (HumanLayer ACE-FCA, Dex Horthy, 2025): review research and plans, not code.
  - "A bad line of research, a misunderstanding of how the codebase works… could land you with thousands of bad lines of code."
  - A bad plan leads to hundreds of bad lines.
  
  Source: [ace-fca.md](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md)

#### Pruning cadence
- [P][G] Anthropic: "Treat CLAUDE.md like code: review it when things go wrong, prune it regularly, and test changes by observing whether Claude's behavior actually shifts." Also "Ruthlessly prune. If Claude already does something correctly without the instruction, delete it or convert it to a hook." — [best practices](https://code.claude.com/docs/en/best-practices)
- [P][G] "Review your CLAUDE.md files… periodically to remove outdated or conflicting instructions." — [memory docs](https://code.claude.com/docs/en/memory)
- [P][G] Auto memory has size-triggered consolidation reminders ("merge or drop stale entries"). — [memory docs](https://code.claude.com/docs/en/memory)
- [S][V] **Time-based expiry:** Copilot deletes memories unused for 28 days. — [GitHub docs](https://docs.github.com/en/copilot/concepts/agents/copilot-memory)
- [S][G] OWASP recommends "deliberate forgetting windows" and "periodic evaluation against ground truth". — [vectorize.io ASI06](https://vectorize.io/articles/owasp-asi06)
- [S][M] Staleness is common in the wild: "blind references" 16% and "init fossilization" 24% of AGENTS.md files. — [Config smells](https://arxiv.org/abs/2606.15828)

#### Measuring before/after
- [P][G] Anthropic, "Demystifying evals for AI agents" (Jan 9, 2026):
  - "20-50 simple tasks drawn from real failures is a great start"; source them from the bug tracker and support queue;
  - "grade what the agent produced, not the path it took";
  - use pass@k and pass^k (pass^k measures consistency);
  - read transcripts;
  - keep regression suites at a "nearly 100% pass rate";
  - calibrate model graders against humans.
  
  Source: [Anthropic engineering](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [S][M] ETH: "any attempts to improve performance should be rigorously evaluated before deployment". The optimiser-compounding study: gains compound **only with regression control**. — [ETH](https://arxiv.org/abs/2602.11988); [arXiv 2607.14004](https://arxiv.org/abs/2607.14004)
- [S][M] **Probe-based tuning** of guidance measurably improved resolve rate (33.0% vs 28.3% vs 25.5%). — [arXiv 2606.20512](https://arxiv.org/abs/2606.20512)
- [S][M] **Scale needed to detect effects:** McMillan needed 1,650 sessions to rule out file-structure effects. — [arXiv 2605.10039](https://arxiv.org/abs/2605.10039)
- [P][G] **Instrumentation:** the `InstructionsLoaded` hook logs which CLAUDE.md and rules files loaded. `claude -p` has `--output-format json` and `stream-json` for scripted runs. — [memory docs](https://code.claude.com/docs/en/memory); [best practices](https://code.claude.com/docs/en/best-practices)

#### Placement (global vs per-repo vs per-skill vs per-role)
- [P][G] **Anthropic's hierarchy:**
  - managed policy → user (`~/.claude/CLAUDE.md`, `~/.claude/rules/`) → project → local;
  - nested and path-scoped rules (`paths:` frontmatter) load only when matching files are touched;
  - "If an entry is a multi-step procedure or only matters for one part of the codebase, move it to a skill or a path-scoped rule";
  - "if a user rule and a project rule conflict, Claude may follow either one";
  - the main conversation's auto memory is not loaded into subagents. Subagents can have their own memory directory (per-role memory).
  
  Source: [memory docs](https://code.claude.com/docs/en/memory)
- [S][V] **Always-on vs on-demand:**
  - Vercel's always-on AGENTS.md index beat on-demand skills (100% vs ≤79%) because skills were never invoked in 56% of cases.
  - Khatri found none vs always-on vs selective retrieval made no measurable correctness difference.
  - "Skill leakage" (rarely used material in AGENTS.md) appears in 35% of files.
  
  Sources: [Vercel](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals); [Khatri](https://arxiv.org/abs/2607.27250); [Config smells](https://arxiv.org/abs/2606.15828)
- [S][G] **OpenAI "Harness engineering"** (Feb 11, 2026):
  - the "one big AGENTS.md" approach failed: "a giant instruction file crowds out the task, the code, and the relevant docs — so the agent either misses key constraints or starts optimizing for the wrong ones";
  - the replacement is a **~100-line AGENTS.md used as a table of contents** into a structured `docs/` directory that is the "system of record";
  - reported scale: about 1M LOC and about 1,500 merged PRs with 3 engineers over 5 months.
  
  Sources: [OpenAI](https://openai.com/index/harness-engineering/); [InfoQ](https://www.infoq.com/news/2026/02/openai-harness-engineering-codex)
- [S][G] **HumanLayer:** progressive disclosure via an `agent_docs/` directory; avoid non-universal instructions. — [Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [S][M] **Global lessons should be abstract; concrete traces don't transfer** (Memory Transfer Learning). — [arXiv 2604.14004](https://arxiv.org/abs/2604.14004)
- [S][V] **Copilot memory** is repository-scoped but shared across roles (coding agent, CLI, reviewer). — [GitHub docs](https://docs.github.com/en/copilot/concepts/agents/copilot-memory)

#### Length limits
- [P][G] **Anthropic:**
  - "target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence";
  - the MEMORY.md index loads its first 200 lines or 25KB;
  - CLAUDE.md is loaded in full up to 4 MiB, and "Shorter files produce better adherence";
  - on emphasis: "add emphasis such as 'IMPORTANT' to that line alone. If you emphasize many lines, none of them stands out."
  
  Sources: [memory docs](https://code.claude.com/docs/en/memory); [best practices](https://code.claude.com/docs/en/best-practices)
- [S][G] **HumanLayer** (late Nov 2025):
  - keep CLAUDE.md minimal (their own file is under 60 lines);
  - "LLMs can only follow ~150-200 instructions reliably, and Claude Code already uses 50 of them";
  - "as instruction count increases… it begins ignoring all of them uniformly";
  - "Never send an LLM to do a linter's job."
  
  The 150–200 figure is a practitioner reading of IFScale-type results, not a measured threshold for coding agents. Source: [HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [S][G] **OpenAI:** about 100 lines as a table of contents. — [OpenAI](https://openai.com/index/harness-engineering/)
- [S][M] **Counterpoint (McMillan):** no detectable adherence effect across 25–500 lines. — [arXiv 2605.10039](https://arxiv.org/abs/2605.10039)

#### Advanced context engineering (ACE-FCA) and 12-factor agents
- [P][G] **ACE-FCA** (Dex Horthy, 2025; exact date not in the fetched document):
  - "frequent intentional compaction";
  - "keeping utilization in the 40%-60% range (depends on complexity of the problem)";
  - a research → plan → implement workflow with human review of research and plans;
  - a reported (anecdotal) result on a 300k-LOC Rust codebase (BAML).
  
  Source: [ace-fca.md](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md)
- [S][G] Horthy's **"dumb zone"**: diminishing returns may begin around **40% context utilisation** in Claude Code, and the threshold varies. — [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/context-engineering-with-dex-horthy); [AI Engineer talk](https://ai.engineer/talks/rmvDxxNubIg-context-engineering-for-complex-codebases)
- [P][G] **12-factor agents** (Apr 2025), relevant factors: #3 "Own your context window", #9 "Compact Errors into Context Window", #10 "Small, Focused Agents", #12 "Make your agent a stateless reducer". — [12-factor-agents README](https://github.com/humanlayer/12-factor-agents)

### Inferences

#### Consensus rules of thumb (distilled; evidence strength in brackets)
1. **Promote on the second occurrence, via a human-approved versioned diff.** [Anthropic P-guidance + practitioner consensus; no controlled study of thresholds]
2. **Record the root cause and the countermeasure type, not just the symptom.** Keep entries abstract and procedural. Record confirmed successful approaches too. [MTL, ReasoningBank, Learning-When-to-Remember: M; Anthropic auto memory: P]
3. **Before writing a prose rule, ask whether it can be a check** (hook, lint, test, CI, DoD script). Prose rules are advisory; checks are deterministic. [Anthropic P; lint leakage 62% M; HumanLayer G]
4. **Keep always-loaded context minimal and non-inferable.** Route procedures to skills or spec templates, and path-specific items to scoped rules. [Anthropic P; ETH M; OpenAI G; mixed evidence on the exact length (McMillan)]
5. **Make updates incremental and itemised.** Never let an agent rewrite a whole rules file. [ACE M; Anthropic JSON-vs-Markdown P]
6. **Attach provenance, evidence and timestamps to each lesson.** Validate it before use and expire it if unused. [Copilot V; MemGuard M; OWASP G; Claude `modified` field P]
7. **Use external signals** (tests, a verifier, human review), never self-grading alone. [SkillLearnBench M; DGM M; Anthropic P]
8. **Measure before and after** with 20–50 replayable real failures, regression control, and cost/time metrics. [Anthropic P; optimiser compounding M; ETH M]
9. **Use fresh context per task.** After two failed corrections, restart with a better spec. [Anthropic P; Laban M; McMillan M]
10. **Prune** when things go wrong, at a fixed cadence, and by TTL. Prune by *ablation* ("does the agent already do it without the rule?"), not by the absence of recurrence. [Anthropic P; Copilot V]
11. **Use emphasis sparingly** (one IMPORTANT line, not many). [Anthropic P]

#### How each practice differs from or plugs into fable-ruki-agenty

| # | Consensus practice | Baseline today | Suggested plug-in (inference) |
|---|---|---|---|
| 1 | 2nd occurrence → rule, via reviewed diff | "one fix is a case, two is a rule"; 2+ open entries of one class → issue-first skill edit; founder approval for AGENTS.md | **Keep.** Require the two occurrences to be **confirmed by the verifier or ladder** (not orchestrator self-report) and to share the **same root cause**, not just the same symptom. |
| 2 | Record root cause + countermeasure type; include confirmed successes | incidents.md records misfires only (format unknown) | Add fields: class; root-cause category (spec ambiguity / executor skill / env-tooling / verifier false positive / routing); evidence links (issue, journal comment, verifier verdict); extra tokens/time/reworks caused; proposed countermeasure type (spec template / DoD check / script / AGENTS.md / skill step / routing); status; first seen / last seen / count; expiry. Add a short "worked well" list for fast paths. |
| 3 | Convert to checks where possible | Verifier checks DoD by model | For each promoted class, first try a **deterministic check**: forwarder or verifier script, pre-commit, CI, or a DoD item with a runnable command. Prose goes to AGENTS.md only if a check is impossible. |
| 4 | Minimal always-loaded context; route by scope | AGENTS.md, the skill and incidents.md all read at start | Keep an **index** of open classes, one line each, capped (analogous to the MEMORY.md 200-line/25KB pattern). Archive closed entries out of the start-of-pipeline read. Executor-facing lessons go into **spec templates / DoD checklists in issue bodies** (just-in-time context for the hands), not AGENTS.md. |
| 5 | Incremental edits | Issue-first skill edit | Require **patch-sized diffs** per rule change and forbid wholesale skill rewrites by agents (ACE context collapse). |
| 6 | Provenance, validation, expiry | None stated | Provenance fields (see row 2); a **TTL** (e.g., archive after N weeks without recurrence; the exact N is not evidence-based); re-validate old rules against current tooling during the retro. |
| 7 | External grading | **Orchestrator grades itself** (known gap) | Use **verifier verdicts and ladder events** (rework #1/#2, fresh executor, blocked) as the ground-truth signal for incident classes. Have a **separate fresh-context "retro analyst"** read the journals and propose rule changes; the founder approves. |
| 8 | Before/after measurement with regression control | **No metrics or evals; no recurrence check** (known gaps) | Keep a per-issue ledger in the forwarder journal (tokens in/out, wall time, reworks, verifier fails per DoD item, incident classes hit). Track **recurrence per class per 10 issues** before and after each rule. Build a **replay set of 20–50 past failures** to re-run after rule changes. **Revert rules that don't reduce recurrence.** |
| 9 | Fresh context; restart with a better spec after 2 failures | Ladder: 2 reworks → fresh executor → blocked; fresh-context verifier | **Already aligned.** Add a **"spec rewrite" step** at the fresh-executor rung that incorporates what the two failures revealed (Anthropic: "start fresh with a more specific prompt that incorporates what you learned"). |
| 10 | Pruning cadence | Weekly human retro | Keep the weekly retro. Add **ablation-based pruning** (drop a rule, re-run the replay subset) and **TTL archival**. |
| 11 | Human review at the highest-leverage point | Founder approves AGENTS.md changes | Spend review effort on **spec templates and rule diffs** (ACE-FCA leverage hierarchy) rather than on executor code. |

### Gaps
- No controlled study compares promotion thresholds (1 vs 2 vs 3 occurrences) or pruning cadences (weekly vs TTL vs size-triggered). Current guidance is expert consensus.
- Codex's AGENTS.md size cap (commonly cited as 32 KiB via `project_doc_max_bytes`) **could not be verified**. The Codex docs have moved to a blocked host and the raw GitHub docs no longer contain it.
- The ACE-FCA document's exact publication date was not in the fetched text.
- There is no evidence on the best *format* for incident journals (Markdown vs JSONL vs issues). The only pointers are Anthropic's JSON-vs-Markdown observation and Yegge's Beads anecdote.

---

## Q5. Contrarian views and the evidence behind them

### Takeaway
Each contrarian thesis has real evidence behind it, but for a narrower claim than its slogan:
- **"Don't let the agent write its own memory"** and **"memory makes agents worse"** are right about *unsupervised, free-form, accumulating* memory. They are wrong about *verified, curated, expiring* memory (Copilot +7 points, ReasoningBank, ACE).
- **"Fresh context beats memory"** is strongly supported *within a task*. Its proponents still rely on curated external state across runs.
- **"Just improve the spec/tests"** is the best-supported contrarian view. Checks and spec quality dominate context files, which help mainly with knowledge the agent can't infer.

### Cited Findings

#### Thesis 1: "Don't let the agent write its own memory/rules"
- **Evidence for:**
  - [S][M] LLM-generated context files: −3% success and +20% cost. — [ETH](https://arxiv.org/abs/2602.11988)
  - [S][M] Self-generated skills: negligible or negative effect; self-feedback causes "recursive drift". — [SkillLearnBench](https://arxiv.org/abs/2604.20087)
  - [S][M] Monolithic LLM rewriting causes "context collapse". — [ACE](https://arxiv.org/abs/2510.04618)
  - [S][M] A self-modifying agent hacked its own objective. — [DGM](https://sakana.ai/dgm/)
  - [S][A] Cursor removed Memories. — [forum](https://forum.cursor.com/t/custom-modes-and-memories-gone-in-2-1/143744)
  - [S][A] Claude auto memory described as "shadow state", not versioned. — [issue #23750](https://github.com/anthropics/claude-code/issues/23750)
  - [S] Security persistence: SpAIware, Unit 42, MINJA (see Q3).
- **Evidence against:**
  - [S][V] Copilot memory: 90% vs 83% PR merge rate. It uses citations, validation and a TTL. — [GitHub blog](https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/)
  - [S][M] ReasoningBank: +34.2% relative, −16% steps. — [Google](https://research.google/blog/reasoningbank-enabling-agents-to-learn-from-experience/)
  - [S][M] ACE: +10.6% with curated incremental updates. — [ACE](https://arxiv.org/abs/2510.04618)
  - [S][V] Letta: +21–37% relative from skill learning. — [Letta](https://www.letta.com/blog/skill-learning/)
  - [S][M] Probe-and-refine: LLM-refined guidance beat both the static knowledge base and no guidance. — [arXiv 2606.20512](https://arxiv.org/abs/2606.20512)
  - [P] Anthropic ships auto memory on by default. — [memory docs](https://code.claude.com/docs/en/memory)

#### Thesis 2: "Memory makes agents worse"
- **Evidence for:**
  - [S][M] Naive memory growth performs worse than selective growth; error propagation and misaligned replay. — [Xiong](https://arxiv.org/abs/2505.16067)
  - [S][M] Superficial similarity leads to unsafe memory injection. — [Learning When to Remember](https://arxiv.org/abs/2604.27283)
  - [S][M] Low-level traces cause negative transfer. — [MTL](https://arxiv.org/abs/2604.14004)
  - [S][M] An optimised agent transferred below the unoptimised baseline on new tasks (GEPA). — [arXiv 2607.14004](https://arxiv.org/abs/2607.14004)
  - [S][G] Context poisoning / distraction / confusion / clash taxonomy. — [Drew Breunig, Jun 22, 2025](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html); [Simon Willison summary, Jun 29, 2025](https://simonwillison.net/2025/Jun/29/how-to-fix-your-context/)
  - [S][A] Simon Willison's example: ChatGPT memory injected his location into an image he requested. The worry is that the context window "no longer belongs to" the user. — [LangChain context engineering blog](https://www.langchain.com/blog/context-engineering-for-agents)
- **Evidence against:** the curated-memory results listed under Thesis 1.

#### Thesis 3: "Fresh context beats memory"
- **Evidence for:**
  - [S][M] Multi-turn performance is 39% lower, and models "do not recover" from a wrong turn. — [Laban et al.](https://arxiv.org/abs/2505.06120)
  - [S][M] About 5.6% lower odds of compliance per additional function within a session. — [McMillan](https://arxiv.org/abs/2605.10039)
  - [P][G] "If you've corrected Claude more than twice on the same issue in one session… Run /clear and start fresh… A clean session with a better prompt almost always outperforms a long session with accumulated corrections." Also "A fresh context improves code review since Claude won't be biased toward code it just wrote." — [best practices](https://code.claude.com/docs/en/best-practices)
  - [S][A] Ralph Wiggum loop (Geoffrey Huntley, 2025): each iteration starts clean, reads the spec, AGENTS.md and progress files, does one task and exits. — [AgentPatterns](https://www.agentpatterns.ai/loop-engineering/ralph-wiggum-loop/); [Geocodio, Jan 27, 2026](https://www.geocod.io/code-and-coordinates/2026-01-27-ralph-loops)
  - [S][M] Focused inputs of about 300 tokens beat about 113K tokens of history. — [Chroma](https://www.trychroma.com/research/context-rot)
  - [S][G] The "dumb zone" at about 40% context. — [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/context-engineering-with-dex-horthy)
- **Nuance:**
  - [P] Anthropic's long-running harness is itself "fresh sessions + curated state": a progress file, a JSON feature list, git and `init.sh`. Each session orients itself by reading them. — [Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
  - [P] 12-factor #12 "stateless reducer". — [12-factor-agents](https://github.com/humanlayer/12-factor-agents)

#### Thesis 4: "Just improve the spec/tests instead"
- **Evidence for:**
  - [S][M] Context strategy doesn't move correctness; failures come from implementation skill. — [Khatri](https://arxiv.org/abs/2607.27250)
  - [S][M] Only minimal requirements belong in context files; unnecessary requirements make tasks harder. — [ETH](https://arxiv.org/abs/2602.11988)
  - [P][G] Anthropic best practices:
    - "Give Claude a check it can run… Without a check it can run, 'looks done' is the only signal available";
    - specs should be "self-contained… and end with an end-to-end verification step";
    - "Time spent making the spec precise pays off more than time spent watching the implementation."
    
    Source: [best practices](https://code.claude.com/docs/en/best-practices)
  - [P] Anthropic's harness rule: "It is unacceptable to remove or edit tests." — [Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
  - [S][M] Lint leakage appears in 62% of AGENTS.md files. — [Config smells](https://arxiv.org/abs/2606.15828)
  - [S][G] "Never send an LLM to do a linter's job." — [HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
  - [P][G] Research and plan errors have the highest leverage. — [ACE-FCA](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md)
- **Evidence against:**
  - [S][V] Knowledge newer than the model's training data needs an always-on index (Vercel, 100%). — [Vercel](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
  - [S][M] Guidance improves coverage in repos with non-obvious structure. — [Probe-and-refine](https://arxiv.org/abs/2606.20512)
  - [S][M] −28.6% runtime with AGENTS.md. — [Lulla](https://arxiv.org/abs/2601.20404)
  - [S][M] +4% from human-written files. — [ETH](https://arxiv.org/abs/2602.11988)

#### Contrarian findings against the consensus itself
- **"File length doesn't matter (for adherence)":** [S][M] McMillan's null result for 25–500 lines contradicts the <200-line and <60-line guidance. — [arXiv 2605.10039](https://arxiv.org/abs/2605.10039)
- **"Always-loaded beats on-demand":** [S][V] Vercel's result runs against the advice to move content into skills. — [Vercel](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- **"Lower the threshold to every mistake":** [S][A] Cherny's team adds a rule for every observed mistake, not just the second, but under team review. — [X](https://x.com/bcherny/status/2007179840848597422)

### Inferences
- The contrarian theses and the consensus are **mostly compatible**. What fails is *unsupervised accumulation*. What works is *curated, verified, minimal, expiring state plus fresh context plus deterministic checks*.
- **Priority order implied by the evidence** for improving a run's quality, speed and cost:
  1. deterministic checks and tests;
  2. spec quality (self-contained, with verification steps);
  3. minimal non-inferable context;
  4. curated lessons.
  
  The baseline already invests heavily in 1–2 (DoD verifier, specs in issues). Its self-improvement loop should mostly *feed levels 1–2* (better DoD checks, better spec templates) rather than grow AGENTS.md.
- The Vercel result matters for the baseline's routing: lessons stored in a skill are only applied if the skill is invoked. In the baseline the orchestrator reads its skill deliberately. For the hands, lessons should arrive **in the issue body or DoD** (always present by pointer), not in optional skills.

### Gaps
- No head-to-head study was found comparing "improve spec/tests" with "add lessons" on the same pipeline.
- Simon Willison's original posts on ChatGPT memory were not retrieved directly; only a secondary quote was seen.
- The "dark factory corrupted a codebase" claim (Horthy) was seen as a headline only.

---

## Q6. What are the main non-security risks of self-updating memory/rules, and how do they map onto the baseline's known gaps?

### Takeaway
The recurring risks are:
- instruction dilution and bloat;
- higher token and time cost;
- conflicts and staleness;
- context collapse from rewrites;
- error propagation from bad or misapplied lessons;
- drift from self-grading;
- non-compounding gains and objective hacking;
- unauditable shadow state;
- measurement noise.

Three of the baseline's four known gaps (self-grading, no recurrence check, no metrics or token accounting) sit exactly on the highest-evidence risks.

### Cited Findings
- **Dilution and bloat, leading to ignored rules:**
  - [P] "Bloated CLAUDE.md files cause Claude to ignore your actual instructions!" — [best practices](https://code.claude.com/docs/en/best-practices)
  - [S][M] Omission is the dominant failure as instruction count rises. — [IFScale](https://arxiv.org/abs/2507.11538)
  - [S][M] Context bloat in 42% of AGENTS.md files. — [Config smells](https://arxiv.org/abs/2606.15828)
  - [S][A] "Wish list, not a contract". — [dev.to](https://dev.to/minatoplanb/i-wrote-200-lines-of-rules-for-claude-code-it-ignored-them-all-4639)
- **Cost:**
  - [S][M] Context files increase cost by over 20% through more exploration, testing and reasoning. — [ETH](https://arxiv.org/abs/2602.11988)
  - [S][A] MCP/memory tool definitions take context. — [dev.to](https://dev.to/gregory_dickson_6dd6e2b55/memorygraph-context-efficient-mcp-memory-without-abandoning-mcp-ii0)
- **Conflicts:**
  - [P] "if two rules contradict each other, Claude may pick one arbitrarily." — [memory docs](https://code.claude.com/docs/en/memory)
  - [S][M] Conflicting instructions in 28% of files. — [Config smells](https://arxiv.org/abs/2606.15828)
- **Staleness:**
  - [S][M] Blind references 16%, init fossilization 24%. — [Config smells](https://arxiv.org/abs/2606.15828)
  - [S][V] Copilot's validation and 28-day TTL exist because of this. — [GitHub docs](https://docs.github.com/en/copilot/concepts/agents/copilot-memory)
  - [P] Anthropic excludes "information that changes frequently". — [best practices](https://code.claude.com/docs/en/best-practices)
- **Context collapse and brevity bias from LLM rewrites:** [S][M] — [ACE](https://arxiv.org/abs/2510.04618)
- **Error propagation, misaligned replay, superficial-similarity injection:** [S][M] — [Xiong](https://arxiv.org/abs/2505.16067); [Learning When to Remember](https://arxiv.org/abs/2604.27283)
- **Recursive drift from self-feedback:** [S][M] — [SkillLearnBench](https://arxiv.org/abs/2604.20087)
- **Non-compounding and overfitting to past tasks** (only regression-controlled optimisation compounded): [S][M] — [arXiv 2607.14004](https://arxiv.org/abs/2607.14004)
- **Objective hacking by self-modifying agents:** [S][M] — [DGM](https://sakana.ai/dgm/)
- **Shadow state and auditability:**
  - [S][A] — [issue #23750](https://github.com/anthropics/claude-code/issues/23750)
  - [P] Auto memory is "machine-local" and excluded from the transcript retention sweep. — [memory docs](https://code.claude.com/docs/en/memory)
- **Markdown decay:**
  - [S][A] 605 decaying plan files. — [Yegge](https://steve-yegge.medium.com/introducing-beads-a-coding-agent-memory-system-637d7d92514a)
  - [P] JSON is less likely to be overwritten than Markdown. — [Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- **Emphasis inflation:** [P] "If you emphasize many lines, none of them stands out." — [best practices](https://code.claude.com/docs/en/best-practices)
- **Reviewer over-reporting, which inflates incidents:** [P] "A reviewer prompted to find gaps will usually report some, even when the work is sound… Chasing every finding leads to over-engineering… Tell the reviewer to flag only gaps that affect correctness or the stated requirements." — [best practices](https://code.claude.com/docs/en/best-practices)
- **Premature "done" and broken hand-offs across sessions:** [P] "a later agent instance would look around, see that progress had been made, and declare the job done." — [Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- **Measurement noise:**
  - [S][M] 1,650 sessions were needed to bound file-structure effects. — [McMillan](https://arxiv.org/abs/2605.10039)
  - [P] pass^k exists because single-run success is noisy. — [Anthropic evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

### Inferences

#### Risk register mapped onto fable-ruki-agenty

| Risk | Where it could bite in the baseline | Evidence strength | Mitigation (inference) |
|---|---|---|---|
| Self-grading drift | Orchestrator both logs incidents and judges whether its fix worked | M (SkillLearnBench; DGM) | Ground truth = verifier verdicts + ladder events + founder retro. A separate fresh-context analyst proposes changes. |
| Non-compounding / no recurrence check | Rules added, never checked | M (optimiser compounding) | Recurrence per class per 10 issues; replay set; revert rules that don't help. |
| Cost creep | Growing AGENTS.md, skill and incidents.md read at start; hands may over-explore to satisfy extra rules | M (ETH +20%) | Token/time ledger per issue; alert when start-of-run context grows; cap the index. |
| Bloat and dilution | incidents.md reviewed at *every* pipeline start | P/M | Index of open classes only (~one line each); archive the rest. |
| Staleness | Rules about tools, versions and paths | M/V | TTL + provenance + re-validation in the weekly retro. |
| Conflicts | Skill vs AGENTS.md vs spec template vs global rules | P/M | During the retro, grep for contradictions. One home per rule (scope routing). |
| Collapse from rewrites | "Issue-first edit of skill" done as a full rewrite | M (ACE) | Patch-sized diffs only. |
| Misapplied lessons (similar symptom, different cause) | Classes defined by symptom | M (Xiong; RSCB) | Define classes by root cause. The verifier confirms the root cause. |
| Verifier over-reporting creates false incident classes | Fresh-context verifier asked to find gaps | P | Instruct the verifier to flag only DoD/correctness gaps. Log verifier false positives as their own class. |
| Shadow state in hands | Hands running with their own auto memory | S/A | Disable auto memory for hands, or make it reviewable. |
| Measurement noise | Solo founder, low issue volume | M | Use recurrence counts and rework rates (high-frequency signals) rather than pass rates; accept only large effects; pass^k on the replay set. |

- **Largest expected ROI for "better, faster, fewer tokens"** (inference from the evidence mix):
  1. token/time and rework accounting per issue, needed to see anything at all;
  2. converting recurring classes into deterministic DoD checks or scripts;
  3. an external, fresh-context grader for proposed rule changes;
  4. capping and pruning what is loaded at pipeline start.

### Gaps
- No evidence was found on the optimal size of an orchestrator-private incident journal, or on whether reading it at every start helps more than a filtered, relevant-only retrieval. The Vercel result (always-on wins) and the Anthropic guidance (load only what applies broadly) point in different directions.
- Per-provider cost effects for Codex and Grok CLI hands were not found. Lulla covers Codex and Claude Code; nothing on Grok CLI.
