# Catalog Index

Generated from 116 entries in `catalog/entries/`. Regenerate with the catalog `index` tool.

## By Category

### agent-pattern

- [Advisor Strategy](entries/advisor-strategy.md) — note — architectural concept for cost-effective agent orchestration; executor/advisor split
- [Architect Loop](entries/architect-loop.md) — pilot — Research-backed cross-vendor agent loop with strong separation of concerns; excellent design patterns for gated, worktree-isolated multi-agent builds
- [Claude Agent Teams](entries/agent-teams.md) — adopt — primary interactive dispatch path; subscription billing, no API credits needed
- [Claude Native Subagents](entries/native-subagents.md) — adopt — lightweight HO consultation route within existing sessions; no separate billing
- [Scheduled Multi-Agent Coordinator Pattern](entries/scheduled-multi-agent-coordinator.md) — note — Useful architecture pattern for persistent scheduled agents with coordinator + messaging; NanoClaw and Hermes are mature implementations

### cli-tool

- [claude-pee](entries/claude-pee.md) — skip — PTY wrapper driving interactive CLI; inherently brittle, breaks on CLI version changes
- [Cobalt](entries/cobalt.md) — note — General-purpose media downloader with a self-hosted API; no agent, skill, or bioinformatics relevance.
- [Distill](entries/distill.md) — watch — Local 1.7B model pipe-filter for CLI output compression is a real problem but requires 8–16 GB RAM and relies on an unaudited HuggingFace model; overlaps with rtk.
- [Google Workspace CLI (gws)](entries/googleworkspace-cli.md) — pilot — Rust CLI with agent-first JSON output and 100+ bundled SKILL.md files covering all Workspace APIs; pre-v1.0 with breaking changes expected
- [MarkItDown](entries/markitdown.md) — pilot — directly useful for converting PDFs, Excel, PPTX, and other docs to markdown for LLM pipelines; MIT, Microsoft-maintained
- [oauth-cli-coder](entries/oauth-cli-coder.md) — skip — OAuth-based CLI automation; adds auth complexity without solving durability
- [OpenDataLoader PDF](entries/opendataloader-pdf.md) — pilot — Top-benchmarked open-source PDF parser with bounding boxes, formula extraction, and RAG-ready output — worth piloting for bioinformatics literature ingestion before committing.
- [rtk — CLI Proxy for LLM Token Reduction](entries/rtk.md) — pilot — Directly reduces Claude Code token costs 60-90% via transparent Bash hook; Windows hook requires WSL but filters work natively
- [Stirling PDF](entries/stirling-pdf.md) — pilot — Self-hosted REST API for 50+ PDF operations enables privacy-preserving agentic PDF workflows without external services
- [Syncthing](entries/syncthing.md) — adopt — Mature, audited, decentralized file sync daemon — production-grade for agent artifact persistence and cross-machine data sharing.

### framework

- [AdGuard Home](entries/adguard-home.md) — note — Production-ready network-wide DNS ad/tracker blocker — infrastructure tool, not an agent/dev workflow component
- [AirLLM](entries/airllm.md) — watch — Clever layer-shard inference to run 70B models on 4GB VRAM, but maintenance has stalled since August 2024 while better-maintained alternatives (Ollama/llama.cpp) have matured.
- [ASI-Evolve](entries/asi-evolve.md) — watch — Impressive autonomous research-loop results but arbitrary code execution per round, no stated license, and very new (2026 academic repo)
- [Autoharness](entries/autoharness.md) — watch — needs eval benchmarks first; pilot when we have eval criteria for our skills/agents
- [Autoresearch](entries/autoresearch.md) — note — Highly influential autonomous experimentation loop pattern, but ML-training-specific — transferable idea, not transferable code
- [Browser Use](entries/browser-use.md) — pilot — MIT-licensed Python/Rust framework giving LLM agents real browser control — useful for web scraping, form automation, and accessing bioinformatics portals, but Rust-core beta is still experimental and full capability requires commercial cloud
- [Claude Mem](entries/claude-mem.md) — skip — kb wiki + Claude Code built-in memory cover our needs; adds SQLite + Chroma + worker complexity without clear benefit
- [Claw Code](entries/claw-code.md) — note — Rust reimplementation of a CLI agent harness; self-described museum exhibit maintained by agents rather than a production tool
- [CLI-Anything](entries/cli-anything.md) — pilot — Generates production-grade, agent-native CLI harnesses from any codebase via a 7-phase pipeline; directly integrates with Claude Code as a plugin and emits SKILL.md files for skill discovery.
- [Crawl4AI](entries/crawl4ai.md) — pilot — Best-in-class async web-to-Markdown crawler for agent/RAG pipelines, but Docker API has had dense critical CVEs; library mode is safe to pilot
- [CrowdSec](entries/crowdsec.md) — note — Production-ready crowdsourced IDS/IPS framework — valuable for hardening servers hosting agent infrastructure, outside direct agent/bioinformatics workflows.
- [ECC — Everything Claude Code (GitHub)](entries/ecc-github.md) — watch — massive cross-harness skill/hook/agent system worth monitoring but high adoption complexity and scope overlap with existing stack
- [ERA — Empirical Research Assistant](entries/era-empirical-research-assistant.md) — watch — Interesting LLM+tree-search loop for scientific code generation, but Gemini-locked, research-grade, and not directly applicable to Claude Code workflows today
- [gbrain](entries/gbrain.md) — skip — kb wiki already provides persistent typed records with relationships and search
- [Get Shit Done (GSD)](entries/get-shit-done.md) — skip — deprecated (moved to GSD Redux); superpowers skill system already covers meta-prompting and spec-driven development
- [Graphify](entries/graphify.md) — note — direct inspiration for kb graph; concepts like confidence-tagged edges and clustering worth learning from
- [gstack](entries/gstack.md) — skip — kb dispatch covers the relevant orchestration patterns; browser/deployment out of scope
- [Headroom](entries/headroom.md) — watch — Powerful context compression with real benchmarks, but proxy/MITM position and headroom learn's CLAUDE.md writes are significant trust risks for adoption without review
- [Immich](entries/immich.md) — note — Production-ready self-hosted Google Photos alternative with AI search; not agent tooling but solid self-hosted media infrastructure.
- [Inbox Zero](entries/inbox-zero.md) — note — AI-powered self-hostable email management app — strong open-source email assistant, not a developer/agent toolkit.
- [jcode](entries/jcode.md) — watch — Feature-rich Rust coding agent harness with exceptional performance (14ms boot, 28MB RAM), swarm collaboration, and 30+ provider integrations; compelling alternative harness to watch
- [Karakeep](entries/karakeep.md) — pilot — Self-hostable AI bookmark manager with REST API, official agent skills, and Ollama support — agent-friendly but self-described as under heavy development.
- [Langflow](entries/langflow.md) — watch — Heavy visual-builder platform with native MCP-server export; too large for direct adoption but worth monitoring for MCP workflow integration patterns.
- [LocateAnything](entries/locate-anything.md) — watch — novel parallel box decoding for vision-language grounding; 3B model on HuggingFace; evaluate for spatial/histology image analysis when pipeline matures
- [Maxun](entries/maxun.md) — watch — Capable no-code web data platform with MCP support and LLM extraction, but early-stage and AGPLv3 copyleft limits commercial embedding
- [MemPalace](entries/mempalace.md) — pilot — Local-first AI memory with 96.6% R@5 retrieval, 33 MCP tools, verbatim storage, and pluggable backends; strong benchmarks and Claude Code integration make it worth trialing
- [MemStack](entries/memstack.md) — watch — Free-tier skill library is substantial but the PyPI MCP loader performs opaque license checks and stores credentials in-process, warranting supply-chain caution before adoption
- [mlx-vlm TurboQuant (Apple Silicon KV Cache Compression)](entries/mlx-vlm-turboquant.md) — pilot — Production-quality Metal kernels implementing TurboQuant on Apple Silicon; benchmarked and ready for review but PR not yet merged
- [NVIDIA Build (NIM)](entries/nvidia-build.md) — note — NVIDIA's model API catalog and NIM inference microservices; broad model access but enterprise-focused with GPU-heavy deployment requirements
- [OBLITERATUS](entries/obliteratus.md) — note — Mechanistic interpretability research toolkit for refusal removal — notable as a reference for alignment geometry, but not safe to adopt in agent pipelines and irrelevant to bioinformatics workflows
- [Odysseus](entries/odysseus.md) — watch — Feature-rich self-hosted AI workspace with massive community momentum, but weeks-old with unsandboxed agent shell execution
- [Onyx AI Platform](entries/onyx-ai-platform.md) — watch — Full self-hostable AI platform with agentic RAG and MCP — notable architecture reference, but too deployment-heavy to adopt as a composable toolkit component
- [Open WebUI](entries/open-webui.md) — watch — Leading self-hosted LLM web UI with RAG, pipelines, and enterprise auth — relevant infrastructure context but custom non-SPDX license limits adoption
- [OpenClaw](entries/openclaw.md) — skip — ecosystem signal for agentic workspaces; not a concrete kb comparison
- [OpenRouter](entries/openrouter.md) — note — Unified LLM API gateway supporting 200+ models — useful as infrastructure reference, not directly needed when using Claude natively.
- [OpenSpace](entries/openspace.md) — watch — Compelling skill-evolution engine for Claude Code agents but very new (v0.1.0), self-published benchmark, and significant security surface from community skill ingestion
- [Overcut — Agentic SDLC Orchestration](entries/overcut.md) — watch — Commercial orchestration layer for multi-agent SDLC; addresses real coordination gap but closed-source, early-stage, and not yet individually usable
- [Paperless-ngx](entries/paperless-ngx.md) — note — Mature self-hosted document management system — useful for archiving research docs but not an agent tool or developer library
- [Qwen3.6-27B](entries/qwen3-6-27b.md) — watch — Strong open-weight 27B model with near-frontier coding scores and 262K context; promising local worker model but requires multi-GPU or quantization for practical use
- [Repowire](entries/repowire.md) — watch — Compelling multi-agent mesh for cross-repo coordination, but macOS/Linux only and default spawn config ships dangerous permission flags
- [RuView WiFi Sensing Platform](entries/ruview-wifi-sensing.md) — watch — Interesting hardware+agent integration with a Claude Code plugin and MCP server, but beta software requiring physical ESP32 hardware for core capabilities
- [SkillOpt](entries/skillopt.md) — pilot — Microsoft research framework that optimizes agent skills via training loops; +23.5 point lifts on Claude Code, Sleep mode for nightly skill consolidation is directly relevant
- [Spiderbrain V3](entries/spiderbrain-v3.md) — skip — BSL license; master/column concept is the key takeaway for kb graph
- [Storybloq](entries/storybloq.md) — skip — PolyForm Noncommercial license + heavy overlap with kb wiki
- [Third Brain V5 (Wiki/Knowledge Layer)](entries/third-brain-v5-wiki.md) — skip — Obsidian-specific schema, heavy; staleness and contradiction detection concepts worth noting for kb
- [Tolvi — Engineering Decision Vault](entries/tolvi.md) — watch — Solid CAG/RAG dual-mode decision-capture design but pre-1.0, small project, and overlaps with kb already in use
- [Vaultwarden](entries/vaultwarden.md) — adopt — Production-grade self-hosted Bitwarden-compatible password server in Rust; fraction of the resource footprint of the official server
- [Weft](entries/weft-language.md) — watch — Novel AI orchestration language with typed nodes, durable execution, and human-in-the-loop primitives — early-stage but architecturally interesting

### mcp-server

- [Claude Peers MCP](entries/claude-peers-mcp.md) — watch — Novel multi-session peer messaging, but mandatory --dangerously-skip-permissions flag is a hard blocker for safe use
- [n8n MCP Server](entries/n8n-mcp.md) — watch — powerful workflow automation bridge but heavy dependency; evaluate when pipeline orchestration needs outgrow kb dispatch
- [Synthesize Bio](entries/synthesize-bio.md) — pilot — Generates synthetic human gene expression profiles on demand via natural-language prompts — unique bioinformatics capability, but proprietary SaaS requiring account and external API trust.

### meta-skill

- [One Skill to Rule Them All](entries/one-skill-to-rule-them-all.md) — pilot — proposes NEW skills from observed patterns; complementary to superpowers routing
- [Skill Router](entries/skill-router.md) — skip — superpowers using-superpowers already handles skill routing

### plugin

- [Everything Claude Code (ECC)](entries/ecc-plugin.md) — watch — rate-limited (429 errors); trial when accessible
- [FluidDocs Deck Builder](entries/fluiddocs-deck-builder.md) — note — Well-built skill/plugin pack for HTML slide decks; interesting multi-reviewer architecture but outside bioinformatics workflows
- [Frontier](entries/frontier.md) — watch — Well-architected multi-harness orchestration runtime for Claude Code; early preview but the token-economics argument and delegation model are sound
- [Headroom Desktop](entries/headroom-desktop.md) — watch — Solid local-first Claude Code cost optimizer with hook injection into ~/.claude/settings.json — worth monitoring given agent-lockdown relevance, but macOS-only stable and single-contributor
- [opencode-fff-search](entries/opencode-fff-search.md) — watch — Drop-in OpenCode grep/glob replacement with Rust-backed in-memory index, frecency ranking, and SIMD literal matching — 3-10x faster than process-spawning ripgrep at scale.
- [Ponytail](entries/ponytail.md) — pilot — YAGNI enforcement plugin with strong benchmarks (80-94% less code, 47-77% cheaper); multi-platform support and clean design make it worth trialing
- [Understand Anything](entries/understand-anything.md) — watch — Interactive knowledge graph plugin for codebases with multi-agent pipeline and broad platform support; impressive but heavy — watch for maturity and real-world performance on large repos

### reference

- [AI Memory Comparison](entries/ai-memory-comparison.md) — adopt — Definitive source-backed survey of 73 open-source AI agent memory systems across 79 features — every claim cites public code or docs.
- [AI Needs What ALCOA+ Gave Records](entries/alcoa-plus-for-ai.md) — note — Useful framing for regulated-AI governance but no actionable tool or framework yet — CASTEM teased but unpublished
- [Awesome Claude Code](entries/awesome-claude-code.md) — note — curated Claude Code ecosystem list; use as discovery source for future catalog inbox items
- [BioMysteryBench](entries/biomysterybench.md) — pilot — 99-problem bioinformatics research benchmark from Anthropic — directly useful for evaluating agent performance on real research tasks.
- [CASTEM: First Principles for Model-Mediated Work](entries/castem-first-principles-model-mediated-work.md) — note — Portable 6-criterion mnemonic (Credible, Auditable, Supervised, Traceable, Explainable, Monitored) for AI governance in regulated settings — good design checklist, no tooling.
- [CL4R1T4S](entries/cl4r1t4s.md) — note — Collection of leaked AI system prompts; useful security-awareness reference but README contains embedded prompt injection
- [Claude Code Remote Prompt Hardening](entries/claude-code-remote-prompt-hardening.md) — note — env vars to block remote system prompt injection in Claude Code; operational hardening knowledge for security-sensitive environments
- [Claude Decision Pressure-Test & Context Handoff Prompts](entries/claude-decision-pressure-test-and-context-handoff.md) — note — Two reusable prompting patterns — steelman/red-team verdict loop and structured context handoff — worth keeping as copy-paste references
- [Claude Howto](entries/claude-howto.md) — note — Well-structured tutorial guide with copy-paste templates, but it is a learning reference rather than an installable tool.
- [Claude Meta-Skill](entries/claude-meta-skill.md) — note — Curated collection of 11 Claude Code skills; mostly Chinese-language or general-dev focused, with significant overlap to existing catalog entries
- [Claude Spellbook](entries/claude-spellbook.md) — note — 50 skills, 7 agents, 11 slash commands — use as pattern reference, not default install
- [Codebase Reasoning Topology](entries/codebase-reasoning-topology.md) — note — heavy for daily use but interesting as a pre-flight checklist concept
- [Codex Memory Cleanup](entries/codex-memory-cleanup.md) — note — operational tip: delete state/log/global-state files if Codex performance degrades
- [Deny .env Reads via Permissions](entries/deny-env-reads.md) — note — Useful security hygiene tip for Claude Code projects; documents a built-in feature rather than a new tool
- [GraphRAG & Agent Memory LinkedIn Series](entries/graphrag-agent-memory-linkedin-series.md) — watch — Six-post series covering GraphRAG design, ontology modeling, and unified agent memory architecture — useful conceptual grounding for KG-backed agents.
- [Karpathy's 12 Rules for CLAUDE.md](entries/karpathy-12-rules.md) — adopt — Rules 6 (token budgets) and 12 (fail loud) not yet in our stack
- [Karpathy's LLM Wiki Pattern](entries/karpathy-llm-wiki.md) — adopt — Foundational pattern doc for LLM-maintained personal knowledge bases — directly describes the architecture kb-wiki implements
- [Model Workspace Protocol (MWP)](entries/model-workspace-protocol.md) — note — Research paper proposing filesystem structure as agent orchestration; numbered folders + markdown prompts replace multi-agent frameworks for sequential workflows
- [Open Knowledge Format (OKF)](entries/open-knowledge-format.md) — note — Google's draft spec for agent-friendly knowledge representation using Markdown + YAML frontmatter; closely aligned with our wiki pattern but v0.1 draft status
- [Pi-hole](entries/pi-hole.md) — note — Network-wide DNS ad blocker — mature infrastructure tool, informational for lab network hygiene
- [Remote Control](entries/remote-control.md) — note — built-in feature; try for long sessions
- [TeamPCP/Miasma npm Supply Chain Attack (June 2026)](entries/teampcp-miasma-npm-supply-chain-attack-2026.md) — note — Incident writeup documenting credential-harvesting malware and ~/.claude/settings.json hook persistence — directly relevant to agent-lockdown hardening (WK-0031)
- [TurboQuant — Extreme KV Cache Compression](entries/turboquant.md) — watch — Foundational Google Research algorithm (ICLR 2026) for 3-4 bit KV cache compression with zero accuracy loss; growing downstream ecosystem but no single canonical package yet
- [Verify Before Claim (Third Brain V5)](entries/verify-before-claim.md) — note — superpowers verification-before-completion covers this; confidence model is the novel addition
- [Zero to Mastery ML](entries/zero-to-mastery-ml.md) — note — Comprehensive ML/DS course materials (NumPy, pandas, sklearn, TensorFlow); useful learning reference but not a tool or workflow component

### skill

- [ADHD](entries/adhd.md) — note — parallel divergent ideation via isolated cognitive frames; overlaps with superpowers:brainstorming but the frame isolation and scoring mechanics are worth studying
- [Advise Project Approach](entries/advise-project-approach.md) — pilot — structured project-level architecture research with comparable analysis, cost checks, and tradeoff discipline; complements /catalog (tool-level) with project-level advisory
- [Agent Session Resume](entries/agent-session-resume.md) — note — Cross-agent session resume skill with structured checkpoint workflow; overlaps with our handoff skill but adds multi-agent-platform support (Codex, Cursor, Antigravity, OpenCode)
- [Book to Skill](entries/book-to-skill.md) — pilot — directly useful for computational biology methods PDFs
- [Context Graph Compressor](entries/context-graph-compressor.md) — pilot — Structured JSON graph handoff with importance tagging and cross-LLM portability beats plain-text handoff skills; too new/single-contributor to adopt outright
- [Grill With Docs](entries/grill-with-docs.md) — pilot — Well-structured DDD design-review skill that enforces domain language, but relies on companion format files (CONTEXT-FORMAT.md, ADR-FORMAT.md) not bundled with the skill.
- [Obsidian Skills (Kepano)](entries/obsidian-skills.md) — note — Obsidian-specific; Defuddle (web→clean markdown) and skill packaging patterns worth noting
- [PII Detection / Compliance Skills](entries/pii-detection.md) — pilot — HIPAA/CCPA/PCI-DSS coverage; pilot if handling sensitive data
- [sota-scan](entries/sota-scan.md) — pilot — Useful comparative benchmarking skill for Claude Code, but single-contributor, no tests, and high token cost for exhaustive mode
- [Superpowers: Verification Before Completion](entries/superpowers-verification-before-completion.md) — adopt — canonical 'evidence before claims' gate skill — already active in this project and referenced by other catalog entries as the standard
- [Tutorial Creator](entries/tutorial-creator.md) — pilot — good for knowledge retention and onboarding
- [UI/UX Pro Max Skill](entries/ui-ux-pro-max-skill.md) — watch — comprehensive design system generation but focused on general web/mobile UI; evaluate when dashboard/report aesthetics become a priority
- [Unforget](entries/unforget.md) — skip — scan-for-escaped-items pattern worth noting for future kb lint rule or audit command
- [Web Artifacts Builder](entries/web-artifacts-builder.md) — adopt — use when markdown isn't enough for interactive reports/dashboards

### skill-generator

- [BMAD Skill Forge](entries/bmad-skill-forge.md) — pilot — strong fit for bioinformatics tool skill generation; start with Brief tier on samtools
- [Creating CLAUDE.md](entries/creating-claude-md.md) — skip — /init skill already covers repo-scanning CLAUDE.md generation
