# Catalog Index

Generated from 85 entries in `catalog/entries/`. Regenerate with the catalog `index` tool.

## By Verdict

| Item | Category | Verdict | Reason | Tags |
|---|---|---|---|---|
| [AI Memory Comparison](entries/ai-memory-comparison.md) | reference | adopt | Definitive source-backed survey of 73 open-source AI agent memory systems across 79 features — every claim cites public code or docs. | memory, agents, comparison, survey, mcp, rag, vector-db |
| [Claude Agent Teams](entries/agent-teams.md) | agent-pattern | adopt | primary interactive dispatch path; subscription billing, no API credits needed | agents, teams, dispatch, orchestration |
| [Claude Native Subagents](entries/native-subagents.md) | agent-pattern | adopt | lightweight HO consultation route within existing sessions; no separate billing | agents, subagents, dispatch, consultation |
| [Karpathy's 12 Rules for CLAUDE.md](entries/karpathy-12-rules.md) | reference | adopt | Rules 6 (token budgets) and 12 (fail loud) not yet in our stack | claude-md, best-practices, token-budgets |
| [Karpathy's LLM Wiki Pattern](entries/karpathy-llm-wiki.md) | reference | adopt | Foundational pattern doc for LLM-maintained personal knowledge bases — directly describes the architecture kb-wiki implements | knowledge-base, wiki, llm-pattern, obsidian, personal-knowledge-management, rag-alternative |
| [Superpowers: Verification Before Completion](entries/superpowers-verification-before-completion.md) | skill | adopt | canonical 'evidence before claims' gate skill — already active in this project and referenced by other catalog entries as the standard | verification, quality, agent-discipline, completion-gate, tdd |
| [Web Artifacts Builder](entries/web-artifacts-builder.md) | skill | adopt | use when markdown isn't enough for interactive reports/dashboards | html, reports, dashboards, visualization |
| [Advise Project Approach](entries/advise-project-approach.md) | skill | pilot | structured project-level architecture research with comparable analysis, cost checks, and tradeoff discipline; complements /catalog (tool-level) with project-level advisory | architecture, stack-selection, comparables, cost-analysis, project-strategy, decision-methodology |
| [BMAD Skill Forge](entries/bmad-skill-forge.md) | skill-generator | pilot | strong fit for bioinformatics tool skill generation; start with Brief tier on samtools | skill-generation, provenance, ast, cli-tools |
| [Book to Skill](entries/book-to-skill.md) | skill | pilot | directly useful for computational biology methods PDFs | pdf, knowledge, querying |
| [Browser Use](entries/browser-use.md) | framework | pilot | MIT-licensed Python/Rust framework giving LLM agents real browser control — useful for web scraping, form automation, and accessing bioinformatics portals, but Rust-core beta is still experimental and full capability requires commercial cloud | browser-automation, web-scraping, agent, python, rust, claude-code-skill |
| [CLI-Anything](entries/cli-anything.md) | framework | pilot | Generates production-grade, agent-native CLI harnesses from any codebase via a 7-phase pipeline; directly integrates with Claude Code as a plugin and emits SKILL.md files for skill discovery. | cli-generation, agent-native, skill-generation, claude-code-plugin, python, bioinformatics-adjacent |
| [Context Graph Compressor](entries/context-graph-compressor.md) | skill | pilot | Structured JSON graph handoff with importance tagging and cross-LLM portability beats plain-text handoff skills; too new/single-contributor to adopt outright | context-management, handoff, token-reduction, json, claude-ai, cross-llm, session-resume |
| [Crawl4AI](entries/crawl4ai.md) | framework | pilot | Best-in-class async web-to-Markdown crawler for agent/RAG pipelines, but Docker API has had dense critical CVEs; library mode is safe to pilot | web-scraping, markdown, rag, agents, async, playwright, docker, llm-extraction |
| [Google Workspace CLI (gws)](entries/googleworkspace-cli.md) | cli-tool | pilot | Rust CLI with agent-first JSON output and 100+ bundled SKILL.md files covering all Workspace APIs; pre-v1.0 with breaking changes expected | google-workspace, gmail, drive, calendar, sheets, agent-skills, oauth, json-output, rust |
| [Grill With Docs](entries/grill-with-docs.md) | skill | pilot | Well-structured DDD design-review skill that enforces domain language, but relies on companion format files (CONTEXT-FORMAT.md, ADR-FORMAT.md) not bundled with the skill. | domain-driven-design, design-review, documentation, adr, glossary, planning |
| [MarkItDown](entries/markitdown.md) | cli-tool | pilot | directly useful for converting PDFs, Excel, PPTX, and other docs to markdown for LLM pipelines; MIT, Microsoft-maintained | markdown, conversion, pdf, documents, excel, llm-preprocessing |
| [One Skill to Rule Them All](entries/one-skill-to-rule-them-all.md) | meta-skill | pilot | proposes NEW skills from observed patterns; complementary to superpowers routing | meta-skill, pattern-detection, skill-generation |
| [OpenDataLoader PDF](entries/opendataloader-pdf.md) | cli-tool | pilot | Top-benchmarked open-source PDF parser with bounding boxes, formula extraction, and RAG-ready output — worth piloting for bioinformatics literature ingestion before committing. | pdf, rag, ocr, markdown, json, bioinformatics, langchain, accessibility |
| [PII Detection / Compliance Skills](entries/pii-detection.md) | skill | pilot | HIPAA/CCPA/PCI-DSS coverage; pilot if handling sensitive data | pii, compliance, hipaa, ccpa, security |
| [rtk — CLI Proxy for LLM Token Reduction](entries/rtk.md) | cli-tool | pilot | Directly reduces Claude Code token costs 60-90% via transparent Bash hook; Windows hook requires WSL but filters work natively | token-optimization, claude-code, cli, rust, bash-hook, ai-tooling |
| [sota-scan](entries/sota-scan.md) | skill | pilot | Useful comparative benchmarking skill for Claude Code, but single-contributor, no tests, and high token cost for exhaustive mode | benchmarking, competitive-analysis, code-quality, claude-code, skill |
| [Stirling PDF](entries/stirling-pdf.md) | cli-tool | pilot | Self-hosted REST API for 50+ PDF operations enables privacy-preserving agentic PDF workflows without external services | pdf, self-hosted, rest-api, docker, ocr, document-processing, automation |
| [Synthesize Bio](entries/synthesize-bio.md) | mcp-server | pilot | Generates synthetic human gene expression profiles on demand via natural-language prompts — unique bioinformatics capability, but proprietary SaaS requiring account and external API trust. | bioinformatics, rna-seq, gene-expression, synthetic-data, genomics, single-cell, bulk-rna |
| [Tutorial Creator](entries/tutorial-creator.md) | skill | pilot | good for knowledge retention and onboarding | tutorials, onboarding, knowledge-retention |
| [AirLLM](entries/airllm.md) | framework | watch | Clever layer-shard inference to run 70B models on 4GB VRAM, but maintenance has stalled since August 2024 while better-maintained alternatives (Ollama/llama.cpp) have matured. | llm-inference, low-vram, memory-optimization, python, huggingface, quantization |
| [ASI-Evolve](entries/asi-evolve.md) | framework | watch | Impressive autonomous research-loop results but arbitrary code execution per round, no stated license, and very new (2026 academic repo) | autonomous-research, agentic, evolutionary-search, experiment-automation, bioinformatics, llm-driven, multi-agent |
| [Autoharness](entries/autoharness.md) | framework | watch | needs eval benchmarks first; pilot when we have eval criteria for our skills/agents | harness, optimization, eval, benchmarks |
| [Claude Peers MCP](entries/claude-peers-mcp.md) | mcp-server | watch | Novel multi-session peer messaging, but mandatory --dangerously-skip-permissions flag is a hard blocker for safe use | multi-agent, inter-session, messaging, coordination, broker, sqlite, bun |
| [Distill](entries/distill.md) | cli-tool | watch | Local 1.7B model pipe-filter for CLI output compression is a real problem but requires 8–16 GB RAM and relies on an unaudited HuggingFace model; overlaps with rtk. | token-reduction, cli, pipe, local-model, output-compression |
| [ECC — Everything Claude Code (GitHub)](entries/ecc-github.md) | framework | watch | massive cross-harness skill/hook/agent system worth monitoring but high adoption complexity and scope overlap with existing stack | skills, hooks, agents, rules, security, cross-harness, plugin, claude-code |
| [ERA — Empirical Research Assistant](entries/era-empirical-research-assistant.md) | framework | watch | Interesting LLM+tree-search loop for scientific code generation, but Gemini-locked, research-grade, and not directly applicable to Claude Code workflows today | scientific-computing, code-generation, tree-search, llm-loop, bioinformatics, single-cell, python, google-research, research-paper |
| [Everything Claude Code (ECC)](entries/ecc-plugin.md) | plugin | watch | rate-limited (429 errors); trial when accessible | plugin, hub, all-in-one |
| [GraphRAG & Agent Memory LinkedIn Series](entries/graphrag-agent-memory-linkedin-series.md) | reference | watch | Six-post series covering GraphRAG design, ontology modeling, and unified agent memory architecture — useful conceptual grounding for KG-backed agents. | graphrag, knowledge-graph, ontology, agent-memory, reasoning, langgraph, crewai |
| [Headroom](entries/headroom.md) | framework | watch | Powerful context compression with real benchmarks, but proxy/MITM position and headroom learn's CLAUDE.md writes are significant trust risks for adoption without review | context-compression, token-reduction, mcp-server, proxy, memory, agent-wrap, claude-code |
| [Headroom Desktop](entries/headroom-desktop.md) | plugin | watch | Solid local-first Claude Code cost optimizer with hook injection into ~/.claude/settings.json — worth monitoring given agent-lockdown relevance, but macOS-only stable and single-contributor | token-optimization, cost-reduction, claude-code, proxy, compression, tauri, hook |
| [Langflow](entries/langflow.md) | framework | watch | Heavy visual-builder platform with native MCP-server export; too large for direct adoption but worth monitoring for MCP workflow integration patterns. | visual-builder, agentic-workflows, mcp-server, llm-orchestration, multi-agent, python, open-source |
| [LocateAnything](entries/locate-anything.md) | framework | watch | novel parallel box decoding for vision-language grounding; 3B model on HuggingFace; evaluate for spatial/histology image analysis when pipeline matures | vision, grounding, object-detection, nvidia, spatial, histology, image-analysis |
| [Maxun](entries/maxun.md) | framework | watch | Capable no-code web data platform with MCP support and LLM extraction, but early-stage and AGPLv3 copyleft limits commercial embedding | web-scraping, data-extraction, no-code, mcp-server, llm, crawling, self-hosted |
| [MemStack](entries/memstack.md) | framework | watch | Free-tier skill library is substantial but the PyPI MCP loader performs opaque license checks and stores credentials in-process, warranting supply-chain caution before adoption | skills, memory, sqlite, hooks, tts, mcp-server, freemium, skill-loader, claude-code |
| [n8n MCP Server](entries/n8n-mcp.md) | mcp-server | watch | powerful workflow automation bridge but heavy dependency; evaluate when pipeline orchestration needs outgrow kb dispatch | mcp, n8n, workflow-automation, orchestration, integrations |
| [Onyx AI Platform](entries/onyx-ai-platform.md) | framework | watch | Full self-hostable AI platform with agentic RAG and MCP — notable architecture reference, but too deployment-heavy to adopt as a composable toolkit component | rag, agentic-rag, self-hosted, llm, mcp, knowledge-retrieval, enterprise, connectors |
| [Open WebUI](entries/open-webui.md) | framework | watch | Leading self-hosted LLM web UI with RAG, pipelines, and enterprise auth — relevant infrastructure context but custom non-SPDX license limits adoption | llm-ui, self-hosted, rag, ollama, openai-compatible, pipelines, enterprise, docker, python |
| [opencode-fff-search](entries/opencode-fff-search.md) | plugin | watch | Drop-in OpenCode grep/glob replacement with Rust-backed in-memory index, frecency ranking, and SIMD literal matching — 3-10x faster than process-spawning ripgrep at scale. | opencode, search, grep, glob, rust, performance, fuzzy-search, lmdb, frecency, simd |
| [OpenSpace](entries/openspace.md) | framework | watch | Compelling skill-evolution engine for Claude Code agents but very new (v0.1.0), self-published benchmark, and significant security surface from community skill ingestion | skill-evolution, mcp-server, claude-code, agent-learning, skill-sharing, token-efficiency |
| [Repowire](entries/repowire.md) | framework | watch | Compelling multi-agent mesh for cross-repo coordination, but macOS/Linux only and default spawn config ships dangerous permission flags | multi-agent, orchestration, mcp, claude-code, codex, gemini-cli, daemon, mesh, tmux, telegram, slack |
| [RuView WiFi Sensing Platform](entries/ruview-wifi-sensing.md) | framework | watch | Interesting hardware+agent integration with a Claude Code plugin and MCP server, but beta software requiring physical ESP32 hardware for core capabilities | wifi-sensing, esp32, mcp-server, claude-code-plugin, edge-ai, vital-signs, presence-detection, iot, physiological-signals |
| [Tolvi — Engineering Decision Vault](entries/tolvi.md) | framework | watch | Solid CAG/RAG dual-mode decision-capture design but pre-1.0, small project, and overlaps with kb already in use | decisions, knowledge-management, adr, vault, claude-code-skill, rag, cag, go-cli, agent-integration |
| [UI/UX Pro Max Skill](entries/ui-ux-pro-max-skill.md) | skill | watch | comprehensive design system generation but focused on general web/mobile UI; evaluate when dashboard/report aesthetics become a priority | ui, ux, design-system, typography, color-palettes, dashboards, visualization |
| [Weft](entries/weft-language.md) | framework | watch | Novel AI orchestration language with typed nodes, durable execution, and human-in-the-loop primitives — early-stage but architecturally interesting | programming-language, ai-orchestration, durable-execution, visual-programming, human-in-the-loop, rust |
| [ADHD](entries/adhd.md) | skill | note | parallel divergent ideation via isolated cognitive frames; overlaps with superpowers:brainstorming but the frame isolation and scoring mechanics are worth studying | ideation, brainstorming, parallel, divergent-thinking, cognitive-frames, subagents |
| [Advisor Strategy](entries/advisor-strategy.md) | agent-pattern | note | architectural concept for cost-effective agent orchestration; executor/advisor split | agents, cost-optimization, dispatch, patterns |
| [Agent Session Resume](entries/agent-session-resume.md) | skill | note | Cross-agent session resume skill with structured checkpoint workflow; overlaps with our handoff skill but adds multi-agent-platform support (Codex, Cursor, Antigravity, OpenCode) | handoff, session-resume, cross-agent, claude-code, codex, cursor |
| [AI Needs What ALCOA+ Gave Records](entries/alcoa-plus-for-ai.md) | reference | note | Useful framing for regulated-AI governance but no actionable tool or framework yet — CASTEM teased but unpublished | ai-governance, gxp, regulatory, data-integrity, pharma |
| [Autoresearch](entries/autoresearch.md) | framework | note | Highly influential autonomous experimentation loop pattern, but ML-training-specific — transferable idea, not transferable code | autonomous-agents, ml-training, experimentation, karpathy, agent-loop |
| [Awesome Claude Code](entries/awesome-claude-code.md) | reference | note | curated Claude Code ecosystem list; use as discovery source for future catalog inbox items | awesome-list, skills, agents, hooks, orchestrators, discovery |
| [CASTEM: First Principles for Model-Mediated Work](entries/castem-first-principles-model-mediated-work.md) | reference | note | Portable 6-criterion mnemonic (Credible, Auditable, Supervised, Traceable, Explainable, Monitored) for AI governance in regulated settings — good design checklist, no tooling. | ai-governance, compliance, regulated-ai, mnemonic, audit, validation, oversight |
| [Claude Code Remote Prompt Hardening](entries/claude-code-remote-prompt-hardening.md) | reference | note | env vars to block remote system prompt injection in Claude Code; operational hardening knowledge for security-sensitive environments | claude-code, security, privacy, env-vars, hardening, system-prompt, version-pinning |
| [Claude Decision Pressure-Test & Context Handoff Prompts](entries/claude-decision-pressure-test-and-context-handoff.md) | reference | note | Two reusable prompting patterns — steelman/red-team verdict loop and structured context handoff — worth keeping as copy-paste references | prompting, decision-making, context-management, red-teaming, handoff |
| [Claude Howto](entries/claude-howto.md) | reference | note | Well-structured tutorial guide with copy-paste templates, but it is a learning reference rather than an installable tool. | claude-code, tutorial, learning-path, slash-commands, skills, hooks, mcp, subagents, templates |
| [Claude Spellbook](entries/claude-spellbook.md) | reference | note | 50 skills, 7 agents, 11 slash commands — use as pattern reference, not default install | skills, agents, hooks, patterns |
| [Cobalt](entries/cobalt.md) | cli-tool | note | General-purpose media downloader with a self-hosted API; no agent, skill, or bioinformatics relevance. | media-download, self-hosted, api, proxy, youtube, video |
| [Codebase Reasoning Topology](entries/codebase-reasoning-topology.md) | reference | note | heavy for daily use but interesting as a pre-flight checklist concept | invariants, state-ownership, blast-radius, checklist |
| [Codex Memory Cleanup](entries/codex-memory-cleanup.md) | reference | note | operational tip: delete state/log/global-state files if Codex performance degrades | codex, maintenance, performance |
| [Deny .env Reads via Permissions](entries/deny-env-reads.md) | reference | note | Useful security hygiene tip for Claude Code projects; documents a built-in feature rather than a new tool | security, permissions, claude-code, env-files, secrets |
| [FluidDocs Deck Builder](entries/fluiddocs-deck-builder.md) | plugin | note | Well-built skill/plugin pack for HTML slide decks; interesting multi-reviewer architecture but outside bioinformatics workflows | presentation, slides, skill-pack, claude-code-plugin, html, pdf-import |
| [Graphify](entries/graphify.md) | framework | note | direct inspiration for kb graph; concepts like confidence-tagged edges and clustering worth learning from | knowledge-graph, ast, visualization, kb |
| [OBLITERATUS](entries/obliteratus.md) | framework | note | Mechanistic interpretability research toolkit for refusal removal — notable as a reference for alignment geometry, but not safe to adopt in agent pipelines and irrelevant to bioinformatics workflows | llm, mechanistic-interpretability, abliteration, alignment, safety-bypass, research, gradio, python |
| [Obsidian Skills (Kepano)](entries/obsidian-skills.md) | skill | note | Obsidian-specific; Defuddle (web→clean markdown) and skill packaging patterns worth noting | obsidian, skills, markdown, canvas, defuddle, web-extraction |
| [Remote Control](entries/remote-control.md) | reference | note | built-in feature; try for long sessions | mobile, remote, sessions |
| [TeamPCP/Miasma npm Supply Chain Attack (June 2026)](entries/teampcp-miasma-npm-supply-chain-attack-2026.md) | reference | note | Incident writeup documenting credential-harvesting malware and ~/.claude/settings.json hook persistence — directly relevant to agent-lockdown hardening (WK-0031) | security, supply-chain, npm, claude-code, incident-report, credential-theft, persistence |
| [Verify Before Claim (Third Brain V5)](entries/verify-before-claim.md) | reference | note | superpowers verification-before-completion covers this; confidence model is the novel addition | verification, quality, confidence-model |
| [Claude Mem](entries/claude-mem.md) | framework | skip | kb wiki + Claude Code built-in memory cover our needs; adds SQLite + Chroma + worker complexity without clear benefit | memory, persistence, vector-search, sessions, hooks, kb |
| [claude-pee](entries/claude-pee.md) | cli-tool | skip | PTY wrapper driving interactive CLI; inherently brittle, breaks on CLI version changes | pty, automation, cli, dispatch |
| [Creating CLAUDE.md](entries/creating-claude-md.md) | skill-generator | skip | /init skill already covers repo-scanning CLAUDE.md generation | claude-md, repo-scanning, code-quality |
| [gbrain](entries/gbrain.md) | framework | skip | kb wiki already provides persistent typed records with relationships and search | memory-graph, vector-search, kb |
| [Get Shit Done (GSD)](entries/get-shit-done.md) | framework | skip | deprecated (moved to GSD Redux); superpowers skill system already covers meta-prompting and spec-driven development | meta-prompting, context-engineering, spec-driven, claude-md, workflow, kb |
| [gstack](entries/gstack.md) | framework | skip | kb dispatch covers the relevant orchestration patterns; browser/deployment out of scope | workflow, orchestration, browser, kb |
| [oauth-cli-coder](entries/oauth-cli-coder.md) | cli-tool | skip | OAuth-based CLI automation; adds auth complexity without solving durability | oauth, automation, cli, dispatch |
| [OpenClaw](entries/openclaw.md) | framework | skip | ecosystem signal for agentic workspaces; not a concrete kb comparison | assistant, orchestration, local-first, kb |
| [Skill Router](entries/skill-router.md) | meta-skill | skip | superpowers using-superpowers already handles skill routing | meta-skill, routing, skill-discovery |
| [Spiderbrain V3](entries/spiderbrain-v3.md) | framework | skip | BSL license; master/column concept is the key takeaway for kb graph | dependency-graph, token-reduction, scoring, kb |
| [Storybloq](entries/storybloq.md) | framework | skip | PolyForm Noncommercial license + heavy overlap with kb wiki | project-state, wiki, tickets, kb |
| [Third Brain V5 (Wiki/Knowledge Layer)](entries/third-brain-v5-wiki.md) | framework | skip | Obsidian-specific schema, heavy; staleness and contradiction detection concepts worth noting for kb | wiki, knowledge-os, ingest, lint, kb |
| [Unforget](entries/unforget.md) | skill | skip | scan-for-escaped-items pattern worth noting for future kb lint rule or audit command | deferred-work, scanner, todos, kb |

## By Workflow

### scRNA-seq

- [BMAD Skill Forge](entries/bmad-skill-forge.md) — pilot — strong fit for bioinformatics tool skill generation; start with Brief tier on samtools
- [Book to Skill](entries/book-to-skill.md) — pilot — directly useful for computational biology methods PDFs
- [Web Artifacts Builder](entries/web-artifacts-builder.md) — adopt — use when markdown isn't enough for interactive reports/dashboards

### spatial

- [BMAD Skill Forge](entries/bmad-skill-forge.md) — pilot — strong fit for bioinformatics tool skill generation; start with Brief tier on samtools
- [Book to Skill](entries/book-to-skill.md) — pilot — directly useful for computational biology methods PDFs
- [LocateAnything](entries/locate-anything.md) — watch — novel parallel box decoding for vision-language grounding; 3B model on HuggingFace; evaluate for spatial/histology image analysis when pipeline matures
- [Web Artifacts Builder](entries/web-artifacts-builder.md) — adopt — use when markdown isn't enough for interactive reports/dashboards

### General

- [ADHD](entries/adhd.md) — note — parallel divergent ideation via isolated cognitive frames; overlaps with superpowers:brainstorming but the frame isolation and scoring mechanics are worth studying
- [Advise Project Approach](entries/advise-project-approach.md) — pilot — structured project-level architecture research with comparable analysis, cost checks, and tradeoff discipline; complements /catalog (tool-level) with project-level advisory
- [Advisor Strategy](entries/advisor-strategy.md) — note — architectural concept for cost-effective agent orchestration; executor/advisor split
- [Agent Session Resume](entries/agent-session-resume.md) — note — Cross-agent session resume skill with structured checkpoint workflow; overlaps with our handoff skill but adds multi-agent-platform support (Codex, Cursor, Antigravity, OpenCode)
- [AI Memory Comparison](entries/ai-memory-comparison.md) — adopt — Definitive source-backed survey of 73 open-source AI agent memory systems across 79 features — every claim cites public code or docs.
- [AI Needs What ALCOA+ Gave Records](entries/alcoa-plus-for-ai.md) — note — Useful framing for regulated-AI governance but no actionable tool or framework yet — CASTEM teased but unpublished
- [AirLLM](entries/airllm.md) — watch — Clever layer-shard inference to run 70B models on 4GB VRAM, but maintenance has stalled since August 2024 while better-maintained alternatives (Ollama/llama.cpp) have matured.
- [ASI-Evolve](entries/asi-evolve.md) — watch — Impressive autonomous research-loop results but arbitrary code execution per round, no stated license, and very new (2026 academic repo)
- [Autoharness](entries/autoharness.md) — watch — needs eval benchmarks first; pilot when we have eval criteria for our skills/agents
- [Autoresearch](entries/autoresearch.md) — note — Highly influential autonomous experimentation loop pattern, but ML-training-specific — transferable idea, not transferable code
- [Awesome Claude Code](entries/awesome-claude-code.md) — note — curated Claude Code ecosystem list; use as discovery source for future catalog inbox items
- [Browser Use](entries/browser-use.md) — pilot — MIT-licensed Python/Rust framework giving LLM agents real browser control — useful for web scraping, form automation, and accessing bioinformatics portals, but Rust-core beta is still experimental and full capability requires commercial cloud
- [CASTEM: First Principles for Model-Mediated Work](entries/castem-first-principles-model-mediated-work.md) — note — Portable 6-criterion mnemonic (Credible, Auditable, Supervised, Traceable, Explainable, Monitored) for AI governance in regulated settings — good design checklist, no tooling.
- [Claude Agent Teams](entries/agent-teams.md) — adopt — primary interactive dispatch path; subscription billing, no API credits needed
- [Claude Code Remote Prompt Hardening](entries/claude-code-remote-prompt-hardening.md) — note — env vars to block remote system prompt injection in Claude Code; operational hardening knowledge for security-sensitive environments
- [Claude Decision Pressure-Test & Context Handoff Prompts](entries/claude-decision-pressure-test-and-context-handoff.md) — note — Two reusable prompting patterns — steelman/red-team verdict loop and structured context handoff — worth keeping as copy-paste references
- [Claude Howto](entries/claude-howto.md) — note — Well-structured tutorial guide with copy-paste templates, but it is a learning reference rather than an installable tool.
- [Claude Mem](entries/claude-mem.md) — skip — kb wiki + Claude Code built-in memory cover our needs; adds SQLite + Chroma + worker complexity without clear benefit
- [Claude Native Subagents](entries/native-subagents.md) — adopt — lightweight HO consultation route within existing sessions; no separate billing
- [Claude Peers MCP](entries/claude-peers-mcp.md) — watch — Novel multi-session peer messaging, but mandatory --dangerously-skip-permissions flag is a hard blocker for safe use
- [Claude Spellbook](entries/claude-spellbook.md) — note — 50 skills, 7 agents, 11 slash commands — use as pattern reference, not default install
- [claude-pee](entries/claude-pee.md) — skip — PTY wrapper driving interactive CLI; inherently brittle, breaks on CLI version changes
- [CLI-Anything](entries/cli-anything.md) — pilot — Generates production-grade, agent-native CLI harnesses from any codebase via a 7-phase pipeline; directly integrates with Claude Code as a plugin and emits SKILL.md files for skill discovery.
- [Cobalt](entries/cobalt.md) — note — General-purpose media downloader with a self-hosted API; no agent, skill, or bioinformatics relevance.
- [Codebase Reasoning Topology](entries/codebase-reasoning-topology.md) — note — heavy for daily use but interesting as a pre-flight checklist concept
- [Codex Memory Cleanup](entries/codex-memory-cleanup.md) — note — operational tip: delete state/log/global-state files if Codex performance degrades
- [Context Graph Compressor](entries/context-graph-compressor.md) — pilot — Structured JSON graph handoff with importance tagging and cross-LLM portability beats plain-text handoff skills; too new/single-contributor to adopt outright
- [Crawl4AI](entries/crawl4ai.md) — pilot — Best-in-class async web-to-Markdown crawler for agent/RAG pipelines, but Docker API has had dense critical CVEs; library mode is safe to pilot
- [Creating CLAUDE.md](entries/creating-claude-md.md) — skip — /init skill already covers repo-scanning CLAUDE.md generation
- [Deny .env Reads via Permissions](entries/deny-env-reads.md) — note — Useful security hygiene tip for Claude Code projects; documents a built-in feature rather than a new tool
- [Distill](entries/distill.md) — watch — Local 1.7B model pipe-filter for CLI output compression is a real problem but requires 8–16 GB RAM and relies on an unaudited HuggingFace model; overlaps with rtk.
- [ECC — Everything Claude Code (GitHub)](entries/ecc-github.md) — watch — massive cross-harness skill/hook/agent system worth monitoring but high adoption complexity and scope overlap with existing stack
- [ERA — Empirical Research Assistant](entries/era-empirical-research-assistant.md) — watch — Interesting LLM+tree-search loop for scientific code generation, but Gemini-locked, research-grade, and not directly applicable to Claude Code workflows today
- [Everything Claude Code (ECC)](entries/ecc-plugin.md) — watch — rate-limited (429 errors); trial when accessible
- [FluidDocs Deck Builder](entries/fluiddocs-deck-builder.md) — note — Well-built skill/plugin pack for HTML slide decks; interesting multi-reviewer architecture but outside bioinformatics workflows
- [gbrain](entries/gbrain.md) — skip — kb wiki already provides persistent typed records with relationships and search
- [Get Shit Done (GSD)](entries/get-shit-done.md) — skip — deprecated (moved to GSD Redux); superpowers skill system already covers meta-prompting and spec-driven development
- [Google Workspace CLI (gws)](entries/googleworkspace-cli.md) — pilot — Rust CLI with agent-first JSON output and 100+ bundled SKILL.md files covering all Workspace APIs; pre-v1.0 with breaking changes expected
- [Graphify](entries/graphify.md) — note — direct inspiration for kb graph; concepts like confidence-tagged edges and clustering worth learning from
- [GraphRAG & Agent Memory LinkedIn Series](entries/graphrag-agent-memory-linkedin-series.md) — watch — Six-post series covering GraphRAG design, ontology modeling, and unified agent memory architecture — useful conceptual grounding for KG-backed agents.
- [Grill With Docs](entries/grill-with-docs.md) — pilot — Well-structured DDD design-review skill that enforces domain language, but relies on companion format files (CONTEXT-FORMAT.md, ADR-FORMAT.md) not bundled with the skill.
- [gstack](entries/gstack.md) — skip — kb dispatch covers the relevant orchestration patterns; browser/deployment out of scope
- [Headroom](entries/headroom.md) — watch — Powerful context compression with real benchmarks, but proxy/MITM position and headroom learn's CLAUDE.md writes are significant trust risks for adoption without review
- [Headroom Desktop](entries/headroom-desktop.md) — watch — Solid local-first Claude Code cost optimizer with hook injection into ~/.claude/settings.json — worth monitoring given agent-lockdown relevance, but macOS-only stable and single-contributor
- [Karpathy's 12 Rules for CLAUDE.md](entries/karpathy-12-rules.md) — adopt — Rules 6 (token budgets) and 12 (fail loud) not yet in our stack
- [Karpathy's LLM Wiki Pattern](entries/karpathy-llm-wiki.md) — adopt — Foundational pattern doc for LLM-maintained personal knowledge bases — directly describes the architecture kb-wiki implements
- [Langflow](entries/langflow.md) — watch — Heavy visual-builder platform with native MCP-server export; too large for direct adoption but worth monitoring for MCP workflow integration patterns.
- [MarkItDown](entries/markitdown.md) — pilot — directly useful for converting PDFs, Excel, PPTX, and other docs to markdown for LLM pipelines; MIT, Microsoft-maintained
- [Maxun](entries/maxun.md) — watch — Capable no-code web data platform with MCP support and LLM extraction, but early-stage and AGPLv3 copyleft limits commercial embedding
- [MemStack](entries/memstack.md) — watch — Free-tier skill library is substantial but the PyPI MCP loader performs opaque license checks and stores credentials in-process, warranting supply-chain caution before adoption
- [n8n MCP Server](entries/n8n-mcp.md) — watch — powerful workflow automation bridge but heavy dependency; evaluate when pipeline orchestration needs outgrow kb dispatch
- [oauth-cli-coder](entries/oauth-cli-coder.md) — skip — OAuth-based CLI automation; adds auth complexity without solving durability
- [OBLITERATUS](entries/obliteratus.md) — note — Mechanistic interpretability research toolkit for refusal removal — notable as a reference for alignment geometry, but not safe to adopt in agent pipelines and irrelevant to bioinformatics workflows
- [Obsidian Skills (Kepano)](entries/obsidian-skills.md) — note — Obsidian-specific; Defuddle (web→clean markdown) and skill packaging patterns worth noting
- [One Skill to Rule Them All](entries/one-skill-to-rule-them-all.md) — pilot — proposes NEW skills from observed patterns; complementary to superpowers routing
- [Onyx AI Platform](entries/onyx-ai-platform.md) — watch — Full self-hostable AI platform with agentic RAG and MCP — notable architecture reference, but too deployment-heavy to adopt as a composable toolkit component
- [Open WebUI](entries/open-webui.md) — watch — Leading self-hosted LLM web UI with RAG, pipelines, and enterprise auth — relevant infrastructure context but custom non-SPDX license limits adoption
- [OpenClaw](entries/openclaw.md) — skip — ecosystem signal for agentic workspaces; not a concrete kb comparison
- [opencode-fff-search](entries/opencode-fff-search.md) — watch — Drop-in OpenCode grep/glob replacement with Rust-backed in-memory index, frecency ranking, and SIMD literal matching — 3-10x faster than process-spawning ripgrep at scale.
- [OpenDataLoader PDF](entries/opendataloader-pdf.md) — pilot — Top-benchmarked open-source PDF parser with bounding boxes, formula extraction, and RAG-ready output — worth piloting for bioinformatics literature ingestion before committing.
- [OpenSpace](entries/openspace.md) — watch — Compelling skill-evolution engine for Claude Code agents but very new (v0.1.0), self-published benchmark, and significant security surface from community skill ingestion
- [PII Detection / Compliance Skills](entries/pii-detection.md) — pilot — HIPAA/CCPA/PCI-DSS coverage; pilot if handling sensitive data
- [Remote Control](entries/remote-control.md) — note — built-in feature; try for long sessions
- [Repowire](entries/repowire.md) — watch — Compelling multi-agent mesh for cross-repo coordination, but macOS/Linux only and default spawn config ships dangerous permission flags
- [rtk — CLI Proxy for LLM Token Reduction](entries/rtk.md) — pilot — Directly reduces Claude Code token costs 60-90% via transparent Bash hook; Windows hook requires WSL but filters work natively
- [RuView WiFi Sensing Platform](entries/ruview-wifi-sensing.md) — watch — Interesting hardware+agent integration with a Claude Code plugin and MCP server, but beta software requiring physical ESP32 hardware for core capabilities
- [Skill Router](entries/skill-router.md) — skip — superpowers using-superpowers already handles skill routing
- [sota-scan](entries/sota-scan.md) — pilot — Useful comparative benchmarking skill for Claude Code, but single-contributor, no tests, and high token cost for exhaustive mode
- [Spiderbrain V3](entries/spiderbrain-v3.md) — skip — BSL license; master/column concept is the key takeaway for kb graph
- [Stirling PDF](entries/stirling-pdf.md) — pilot — Self-hosted REST API for 50+ PDF operations enables privacy-preserving agentic PDF workflows without external services
- [Storybloq](entries/storybloq.md) — skip — PolyForm Noncommercial license + heavy overlap with kb wiki
- [Superpowers: Verification Before Completion](entries/superpowers-verification-before-completion.md) — adopt — canonical 'evidence before claims' gate skill — already active in this project and referenced by other catalog entries as the standard
- [Synthesize Bio](entries/synthesize-bio.md) — pilot — Generates synthetic human gene expression profiles on demand via natural-language prompts — unique bioinformatics capability, but proprietary SaaS requiring account and external API trust.
- [TeamPCP/Miasma npm Supply Chain Attack (June 2026)](entries/teampcp-miasma-npm-supply-chain-attack-2026.md) — note — Incident writeup documenting credential-harvesting malware and ~/.claude/settings.json hook persistence — directly relevant to agent-lockdown hardening (WK-0031)
- [Third Brain V5 (Wiki/Knowledge Layer)](entries/third-brain-v5-wiki.md) — skip — Obsidian-specific schema, heavy; staleness and contradiction detection concepts worth noting for kb
- [Tolvi — Engineering Decision Vault](entries/tolvi.md) — watch — Solid CAG/RAG dual-mode decision-capture design but pre-1.0, small project, and overlaps with kb already in use
- [Tutorial Creator](entries/tutorial-creator.md) — pilot — good for knowledge retention and onboarding
- [UI/UX Pro Max Skill](entries/ui-ux-pro-max-skill.md) — watch — comprehensive design system generation but focused on general web/mobile UI; evaluate when dashboard/report aesthetics become a priority
- [Unforget](entries/unforget.md) — skip — scan-for-escaped-items pattern worth noting for future kb lint rule or audit command
- [Verify Before Claim (Third Brain V5)](entries/verify-before-claim.md) — note — superpowers verification-before-completion covers this; confidence model is the novel addition
- [Weft](entries/weft-language.md) — watch — Novel AI orchestration language with typed nodes, durable execution, and human-in-the-loop primitives — early-stage but architecturally interesting

## By Category

### agent-pattern

- [Advisor Strategy](entries/advisor-strategy.md) — note — architectural concept for cost-effective agent orchestration; executor/advisor split
- [Claude Agent Teams](entries/agent-teams.md) — adopt — primary interactive dispatch path; subscription billing, no API credits needed
- [Claude Native Subagents](entries/native-subagents.md) — adopt — lightweight HO consultation route within existing sessions; no separate billing

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

### framework

- [AirLLM](entries/airllm.md) — watch — Clever layer-shard inference to run 70B models on 4GB VRAM, but maintenance has stalled since August 2024 while better-maintained alternatives (Ollama/llama.cpp) have matured.
- [ASI-Evolve](entries/asi-evolve.md) — watch — Impressive autonomous research-loop results but arbitrary code execution per round, no stated license, and very new (2026 academic repo)
- [Autoharness](entries/autoharness.md) — watch — needs eval benchmarks first; pilot when we have eval criteria for our skills/agents
- [Autoresearch](entries/autoresearch.md) — note — Highly influential autonomous experimentation loop pattern, but ML-training-specific — transferable idea, not transferable code
- [Browser Use](entries/browser-use.md) — pilot — MIT-licensed Python/Rust framework giving LLM agents real browser control — useful for web scraping, form automation, and accessing bioinformatics portals, but Rust-core beta is still experimental and full capability requires commercial cloud
- [Claude Mem](entries/claude-mem.md) — skip — kb wiki + Claude Code built-in memory cover our needs; adds SQLite + Chroma + worker complexity without clear benefit
- [CLI-Anything](entries/cli-anything.md) — pilot — Generates production-grade, agent-native CLI harnesses from any codebase via a 7-phase pipeline; directly integrates with Claude Code as a plugin and emits SKILL.md files for skill discovery.
- [Crawl4AI](entries/crawl4ai.md) — pilot — Best-in-class async web-to-Markdown crawler for agent/RAG pipelines, but Docker API has had dense critical CVEs; library mode is safe to pilot
- [ECC — Everything Claude Code (GitHub)](entries/ecc-github.md) — watch — massive cross-harness skill/hook/agent system worth monitoring but high adoption complexity and scope overlap with existing stack
- [ERA — Empirical Research Assistant](entries/era-empirical-research-assistant.md) — watch — Interesting LLM+tree-search loop for scientific code generation, but Gemini-locked, research-grade, and not directly applicable to Claude Code workflows today
- [gbrain](entries/gbrain.md) — skip — kb wiki already provides persistent typed records with relationships and search
- [Get Shit Done (GSD)](entries/get-shit-done.md) — skip — deprecated (moved to GSD Redux); superpowers skill system already covers meta-prompting and spec-driven development
- [Graphify](entries/graphify.md) — note — direct inspiration for kb graph; concepts like confidence-tagged edges and clustering worth learning from
- [gstack](entries/gstack.md) — skip — kb dispatch covers the relevant orchestration patterns; browser/deployment out of scope
- [Headroom](entries/headroom.md) — watch — Powerful context compression with real benchmarks, but proxy/MITM position and headroom learn's CLAUDE.md writes are significant trust risks for adoption without review
- [Langflow](entries/langflow.md) — watch — Heavy visual-builder platform with native MCP-server export; too large for direct adoption but worth monitoring for MCP workflow integration patterns.
- [LocateAnything](entries/locate-anything.md) — watch — novel parallel box decoding for vision-language grounding; 3B model on HuggingFace; evaluate for spatial/histology image analysis when pipeline matures
- [Maxun](entries/maxun.md) — watch — Capable no-code web data platform with MCP support and LLM extraction, but early-stage and AGPLv3 copyleft limits commercial embedding
- [MemStack](entries/memstack.md) — watch — Free-tier skill library is substantial but the PyPI MCP loader performs opaque license checks and stores credentials in-process, warranting supply-chain caution before adoption
- [OBLITERATUS](entries/obliteratus.md) — note — Mechanistic interpretability research toolkit for refusal removal — notable as a reference for alignment geometry, but not safe to adopt in agent pipelines and irrelevant to bioinformatics workflows
- [Onyx AI Platform](entries/onyx-ai-platform.md) — watch — Full self-hostable AI platform with agentic RAG and MCP — notable architecture reference, but too deployment-heavy to adopt as a composable toolkit component
- [Open WebUI](entries/open-webui.md) — watch — Leading self-hosted LLM web UI with RAG, pipelines, and enterprise auth — relevant infrastructure context but custom non-SPDX license limits adoption
- [OpenClaw](entries/openclaw.md) — skip — ecosystem signal for agentic workspaces; not a concrete kb comparison
- [OpenSpace](entries/openspace.md) — watch — Compelling skill-evolution engine for Claude Code agents but very new (v0.1.0), self-published benchmark, and significant security surface from community skill ingestion
- [Repowire](entries/repowire.md) — watch — Compelling multi-agent mesh for cross-repo coordination, but macOS/Linux only and default spawn config ships dangerous permission flags
- [RuView WiFi Sensing Platform](entries/ruview-wifi-sensing.md) — watch — Interesting hardware+agent integration with a Claude Code plugin and MCP server, but beta software requiring physical ESP32 hardware for core capabilities
- [Spiderbrain V3](entries/spiderbrain-v3.md) — skip — BSL license; master/column concept is the key takeaway for kb graph
- [Storybloq](entries/storybloq.md) — skip — PolyForm Noncommercial license + heavy overlap with kb wiki
- [Third Brain V5 (Wiki/Knowledge Layer)](entries/third-brain-v5-wiki.md) — skip — Obsidian-specific schema, heavy; staleness and contradiction detection concepts worth noting for kb
- [Tolvi — Engineering Decision Vault](entries/tolvi.md) — watch — Solid CAG/RAG dual-mode decision-capture design but pre-1.0, small project, and overlaps with kb already in use
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
- [Headroom Desktop](entries/headroom-desktop.md) — watch — Solid local-first Claude Code cost optimizer with hook injection into ~/.claude/settings.json — worth monitoring given agent-lockdown relevance, but macOS-only stable and single-contributor
- [opencode-fff-search](entries/opencode-fff-search.md) — watch — Drop-in OpenCode grep/glob replacement with Rust-backed in-memory index, frecency ranking, and SIMD literal matching — 3-10x faster than process-spawning ripgrep at scale.

### reference

- [AI Memory Comparison](entries/ai-memory-comparison.md) — adopt — Definitive source-backed survey of 73 open-source AI agent memory systems across 79 features — every claim cites public code or docs.
- [AI Needs What ALCOA+ Gave Records](entries/alcoa-plus-for-ai.md) — note — Useful framing for regulated-AI governance but no actionable tool or framework yet — CASTEM teased but unpublished
- [Awesome Claude Code](entries/awesome-claude-code.md) — note — curated Claude Code ecosystem list; use as discovery source for future catalog inbox items
- [CASTEM: First Principles for Model-Mediated Work](entries/castem-first-principles-model-mediated-work.md) — note — Portable 6-criterion mnemonic (Credible, Auditable, Supervised, Traceable, Explainable, Monitored) for AI governance in regulated settings — good design checklist, no tooling.
- [Claude Code Remote Prompt Hardening](entries/claude-code-remote-prompt-hardening.md) — note — env vars to block remote system prompt injection in Claude Code; operational hardening knowledge for security-sensitive environments
- [Claude Decision Pressure-Test & Context Handoff Prompts](entries/claude-decision-pressure-test-and-context-handoff.md) — note — Two reusable prompting patterns — steelman/red-team verdict loop and structured context handoff — worth keeping as copy-paste references
- [Claude Howto](entries/claude-howto.md) — note — Well-structured tutorial guide with copy-paste templates, but it is a learning reference rather than an installable tool.
- [Claude Spellbook](entries/claude-spellbook.md) — note — 50 skills, 7 agents, 11 slash commands — use as pattern reference, not default install
- [Codebase Reasoning Topology](entries/codebase-reasoning-topology.md) — note — heavy for daily use but interesting as a pre-flight checklist concept
- [Codex Memory Cleanup](entries/codex-memory-cleanup.md) — note — operational tip: delete state/log/global-state files if Codex performance degrades
- [Deny .env Reads via Permissions](entries/deny-env-reads.md) — note — Useful security hygiene tip for Claude Code projects; documents a built-in feature rather than a new tool
- [GraphRAG & Agent Memory LinkedIn Series](entries/graphrag-agent-memory-linkedin-series.md) — watch — Six-post series covering GraphRAG design, ontology modeling, and unified agent memory architecture — useful conceptual grounding for KG-backed agents.
- [Karpathy's 12 Rules for CLAUDE.md](entries/karpathy-12-rules.md) — adopt — Rules 6 (token budgets) and 12 (fail loud) not yet in our stack
- [Karpathy's LLM Wiki Pattern](entries/karpathy-llm-wiki.md) — adopt — Foundational pattern doc for LLM-maintained personal knowledge bases — directly describes the architecture kb-wiki implements
- [Remote Control](entries/remote-control.md) — note — built-in feature; try for long sessions
- [TeamPCP/Miasma npm Supply Chain Attack (June 2026)](entries/teampcp-miasma-npm-supply-chain-attack-2026.md) — note — Incident writeup documenting credential-harvesting malware and ~/.claude/settings.json hook persistence — directly relevant to agent-lockdown hardening (WK-0031)
- [Verify Before Claim (Third Brain V5)](entries/verify-before-claim.md) — note — superpowers verification-before-completion covers this; confidence model is the novel addition

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
