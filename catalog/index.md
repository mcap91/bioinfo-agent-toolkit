# Catalog Index

Generated from 116 entries in `catalog/entries/`. Regenerate with the catalog `index` tool.

## By Decision Status

| Item | Category | Status | Reason | Tags |
|---|---|---|---|---|
| [AI Memory Comparison](entries/ai-memory-comparison.md) | reference | adopted | Definitive source-backed survey of 73 open-source AI agent memory systems across 79 features — every claim cites public code or docs. | memory, agents, comparison, survey, mcp, rag, vector-db |
| [Claude Agent Teams](entries/agent-teams.md) | agent-pattern | adopted | primary interactive dispatch path; subscription billing, no API credits needed | agents, teams, dispatch, orchestration |
| [Claude Native Subagents](entries/native-subagents.md) | agent-pattern | adopted | lightweight HO consultation route within existing sessions; no separate billing | agents, subagents, dispatch, consultation |
| [Karpathy's 12 Rules for CLAUDE.md](entries/karpathy-12-rules.md) | reference | adopted | Rules 6 (token budgets) and 12 (fail loud) not yet in our stack | claude-md, best-practices, token-budgets |
| [Karpathy's LLM Wiki Pattern](entries/karpathy-llm-wiki.md) | reference | adopted | Foundational pattern doc for LLM-maintained personal knowledge bases — directly describes the architecture kb-wiki implements | knowledge-base, wiki, llm-pattern, obsidian, personal-knowledge-management, rag-alternative |
| [Superpowers: Verification Before Completion](entries/superpowers-verification-before-completion.md) | skill | adopted | canonical 'evidence before claims' gate skill — already active in this project and referenced by other catalog entries as the standard | verification, quality, agent-discipline, completion-gate, tdd |
| [Syncthing](entries/syncthing.md) | cli-tool | adopted | Mature, audited, decentralized file sync daemon — production-grade for agent artifact persistence and cross-machine data sharing. | file-sync, decentralized, p2p, self-hosted, cross-platform, golang, tls, data-safety |
| [Vaultwarden](entries/vaultwarden.md) | framework | adopted | Production-grade self-hosted Bitwarden-compatible password server in Rust; fraction of the resource footprint of the official server | password-manager, self-hosted, bitwarden, rust, docker, security, secrets |
| [Web Artifacts Builder](entries/web-artifacts-builder.md) | skill | adopted | use when markdown isn't enough for interactive reports/dashboards | html, reports, dashboards, visualization |
| [Claude Mem](entries/claude-mem.md) | framework | rejected | kb wiki + Claude Code built-in memory cover our needs; adds SQLite + Chroma + worker complexity without clear benefit | memory, persistence, vector-search, sessions, hooks, kb |
| [claude-pee](entries/claude-pee.md) | cli-tool | rejected | PTY wrapper driving interactive CLI; inherently brittle, breaks on CLI version changes | pty, automation, cli, dispatch |
| [Creating CLAUDE.md](entries/creating-claude-md.md) | skill-generator | rejected | /init skill already covers repo-scanning CLAUDE.md generation | claude-md, repo-scanning, code-quality |
| [gbrain](entries/gbrain.md) | framework | rejected | kb wiki already provides persistent typed records with relationships and search | memory-graph, vector-search, kb |
| [Get Shit Done (GSD)](entries/get-shit-done.md) | framework | rejected | deprecated (moved to GSD Redux); superpowers skill system already covers meta-prompting and spec-driven development | meta-prompting, context-engineering, spec-driven, claude-md, workflow, kb |
| [gstack](entries/gstack.md) | framework | rejected | kb dispatch covers the relevant orchestration patterns; browser/deployment out of scope | workflow, orchestration, browser, kb |
| [oauth-cli-coder](entries/oauth-cli-coder.md) | cli-tool | rejected | OAuth-based CLI automation; adds auth complexity without solving durability | oauth, automation, cli, dispatch |
| [OpenClaw](entries/openclaw.md) | framework | rejected | ecosystem signal for agentic workspaces; not a concrete kb comparison | assistant, orchestration, local-first, kb |
| [Skill Router](entries/skill-router.md) | meta-skill | rejected | superpowers using-superpowers already handles skill routing | meta-skill, routing, skill-discovery |
| [Spiderbrain V3](entries/spiderbrain-v3.md) | framework | rejected | BSL license; master/column concept is the key takeaway for kb graph | dependency-graph, token-reduction, scoring, kb |
| [Storybloq](entries/storybloq.md) | framework | rejected | PolyForm Noncommercial license + heavy overlap with kb wiki | project-state, wiki, tickets, kb |
| [Third Brain V5 (Wiki/Knowledge Layer)](entries/third-brain-v5-wiki.md) | framework | rejected | Obsidian-specific schema, heavy; staleness and contradiction detection concepts worth noting for kb | wiki, knowledge-os, ingest, lint, kb |
| [Unforget](entries/unforget.md) | skill | rejected | scan-for-escaped-items pattern worth noting for future kb lint rule or audit command | deferred-work, scanner, todos, kb |
| [AdGuard Home](entries/adguard-home.md) | framework | open | Production-ready network-wide DNS ad/tracker blocker — infrastructure tool, not an agent/dev workflow component | dns, privacy, ad-blocking, network, self-hosted, docker |
| [ADHD](entries/adhd.md) | skill | open | parallel divergent ideation via isolated cognitive frames; overlaps with superpowers:brainstorming but the frame isolation and scoring mechanics are worth studying | ideation, brainstorming, parallel, divergent-thinking, cognitive-frames, subagents |
| [Advise Project Approach](entries/advise-project-approach.md) | skill | open | structured project-level architecture research with comparable analysis, cost checks, and tradeoff discipline; complements /catalog (tool-level) with project-level advisory | architecture, stack-selection, comparables, cost-analysis, project-strategy, decision-methodology |
| [Advisor Strategy](entries/advisor-strategy.md) | agent-pattern | open | architectural concept for cost-effective agent orchestration; executor/advisor split | agents, cost-optimization, dispatch, patterns |
| [Agent Session Resume](entries/agent-session-resume.md) | skill | open | Cross-agent session resume skill with structured checkpoint workflow; overlaps with our handoff skill but adds multi-agent-platform support (Codex, Cursor, Antigravity, OpenCode) | handoff, session-resume, cross-agent, claude-code, codex, cursor |
| [AI Needs What ALCOA+ Gave Records](entries/alcoa-plus-for-ai.md) | reference | open | Useful framing for regulated-AI governance but no actionable tool or framework yet — CASTEM teased but unpublished | ai-governance, gxp, regulatory, data-integrity, pharma |
| [AirLLM](entries/airllm.md) | framework | open | Clever layer-shard inference to run 70B models on 4GB VRAM, but maintenance has stalled since August 2024 while better-maintained alternatives (Ollama/llama.cpp) have matured. | llm-inference, low-vram, memory-optimization, python, huggingface, quantization |
| [Architect Loop](entries/architect-loop.md) | agent-pattern | open | Research-backed cross-vendor agent loop with strong separation of concerns; excellent design patterns for gated, worktree-isolated multi-agent builds | multi-agent, cross-vendor, claude-code-skill, codex, worktree-isolation, gates, research, orchestration |
| [ASI-Evolve](entries/asi-evolve.md) | framework | open | Impressive autonomous research-loop results but arbitrary code execution per round, no stated license, and very new (2026 academic repo) | autonomous-research, agentic, evolutionary-search, experiment-automation, bioinformatics, llm-driven, multi-agent |
| [Autoharness](entries/autoharness.md) | framework | open | needs eval benchmarks first; pilot when we have eval criteria for our skills/agents | harness, optimization, eval, benchmarks |
| [Autoresearch](entries/autoresearch.md) | framework | open | Highly influential autonomous experimentation loop pattern, but ML-training-specific — transferable idea, not transferable code | autonomous-agents, ml-training, experimentation, karpathy, agent-loop |
| [Awesome Claude Code](entries/awesome-claude-code.md) | reference | open | curated Claude Code ecosystem list; use as discovery source for future catalog inbox items | awesome-list, skills, agents, hooks, orchestrators, discovery |
| [BioMysteryBench](entries/biomysterybench.md) | reference | open | 99-problem bioinformatics research benchmark from Anthropic — directly useful for evaluating agent performance on real research tasks. | benchmark, bioinformatics, evaluation, dataset, research, anthropic |
| [BMAD Skill Forge](entries/bmad-skill-forge.md) | skill-generator | open | strong fit for bioinformatics tool skill generation; start with Brief tier on samtools | skill-generation, provenance, ast, cli-tools |
| [Book to Skill](entries/book-to-skill.md) | skill | open | directly useful for computational biology methods PDFs | pdf, knowledge, querying |
| [Browser Use](entries/browser-use.md) | framework | open | MIT-licensed Python/Rust framework giving LLM agents real browser control — useful for web scraping, form automation, and accessing bioinformatics portals, but Rust-core beta is still experimental and full capability requires commercial cloud | browser-automation, web-scraping, agent, python, rust, claude-code-skill |
| [CASTEM: First Principles for Model-Mediated Work](entries/castem-first-principles-model-mediated-work.md) | reference | open | Portable 6-criterion mnemonic (Credible, Auditable, Supervised, Traceable, Explainable, Monitored) for AI governance in regulated settings — good design checklist, no tooling. | ai-governance, compliance, regulated-ai, mnemonic, audit, validation, oversight |
| [CL4R1T4S](entries/cl4r1t4s.md) | reference | open | Collection of leaked AI system prompts; useful security-awareness reference but README contains embedded prompt injection | system-prompts, ai-transparency, security-awareness, prompt-injection |
| [Claude Code Remote Prompt Hardening](entries/claude-code-remote-prompt-hardening.md) | reference | open | env vars to block remote system prompt injection in Claude Code; operational hardening knowledge for security-sensitive environments | claude-code, security, privacy, env-vars, hardening, system-prompt, version-pinning |
| [Claude Decision Pressure-Test & Context Handoff Prompts](entries/claude-decision-pressure-test-and-context-handoff.md) | reference | open | Two reusable prompting patterns — steelman/red-team verdict loop and structured context handoff — worth keeping as copy-paste references | prompting, decision-making, context-management, red-teaming, handoff |
| [Claude Howto](entries/claude-howto.md) | reference | open | Well-structured tutorial guide with copy-paste templates, but it is a learning reference rather than an installable tool. | claude-code, tutorial, learning-path, slash-commands, skills, hooks, mcp, subagents, templates |
| [Claude Meta-Skill](entries/claude-meta-skill.md) | reference | open | Curated collection of 11 Claude Code skills; mostly Chinese-language or general-dev focused, with significant overlap to existing catalog entries | claude-code, skills, collection, prompt-engineering, mcp, refactoring |
| [Claude Peers MCP](entries/claude-peers-mcp.md) | mcp-server | open | Novel multi-session peer messaging, but mandatory --dangerously-skip-permissions flag is a hard blocker for safe use | multi-agent, inter-session, messaging, coordination, broker, sqlite, bun |
| [Claude Spellbook](entries/claude-spellbook.md) | reference | open | 50 skills, 7 agents, 11 slash commands — use as pattern reference, not default install | skills, agents, hooks, patterns |
| [Claw Code](entries/claw-code.md) | framework | open | Rust reimplementation of a CLI agent harness; self-described museum exhibit maintained by agents rather than a production tool | rust, cli-agent, claude-code-alternative, agent-harness, ultraworkers |
| [CLI-Anything](entries/cli-anything.md) | framework | open | Generates production-grade, agent-native CLI harnesses from any codebase via a 7-phase pipeline; directly integrates with Claude Code as a plugin and emits SKILL.md files for skill discovery. | cli-generation, agent-native, skill-generation, claude-code-plugin, python, bioinformatics-adjacent |
| [Cobalt](entries/cobalt.md) | cli-tool | open | General-purpose media downloader with a self-hosted API; no agent, skill, or bioinformatics relevance. | media-download, self-hosted, api, proxy, youtube, video |
| [Codebase Reasoning Topology](entries/codebase-reasoning-topology.md) | reference | open | heavy for daily use but interesting as a pre-flight checklist concept | invariants, state-ownership, blast-radius, checklist |
| [Codex Memory Cleanup](entries/codex-memory-cleanup.md) | reference | open | operational tip: delete state/log/global-state files if Codex performance degrades | codex, maintenance, performance |
| [Context Graph Compressor](entries/context-graph-compressor.md) | skill | open | Structured JSON graph handoff with importance tagging and cross-LLM portability beats plain-text handoff skills; too new/single-contributor to adopt outright | context-management, handoff, token-reduction, json, claude-ai, cross-llm, session-resume |
| [Crawl4AI](entries/crawl4ai.md) | framework | open | Best-in-class async web-to-Markdown crawler for agent/RAG pipelines, but Docker API has had dense critical CVEs; library mode is safe to pilot | web-scraping, markdown, rag, agents, async, playwright, docker, llm-extraction |
| [CrowdSec](entries/crowdsec.md) | framework | open | Production-ready crowdsourced IDS/IPS framework — valuable for hardening servers hosting agent infrastructure, outside direct agent/bioinformatics workflows. | security, ids, ips, waf, threat-intelligence, crowdsourced, ip-blocklist, infrastructure |
| [Deny .env Reads via Permissions](entries/deny-env-reads.md) | reference | open | Useful security hygiene tip for Claude Code projects; documents a built-in feature rather than a new tool | security, permissions, claude-code, env-files, secrets |
| [Distill](entries/distill.md) | cli-tool | open | Local 1.7B model pipe-filter for CLI output compression is a real problem but requires 8–16 GB RAM and relies on an unaudited HuggingFace model; overlaps with rtk. | token-reduction, cli, pipe, local-model, output-compression |
| [ECC — Everything Claude Code (GitHub)](entries/ecc-github.md) | framework | open | massive cross-harness skill/hook/agent system worth monitoring but high adoption complexity and scope overlap with existing stack | skills, hooks, agents, rules, security, cross-harness, plugin, claude-code |
| [ERA — Empirical Research Assistant](entries/era-empirical-research-assistant.md) | framework | open | Interesting LLM+tree-search loop for scientific code generation, but Gemini-locked, research-grade, and not directly applicable to Claude Code workflows today | scientific-computing, code-generation, tree-search, llm-loop, bioinformatics, single-cell, python, google-research, research-paper |
| [Everything Claude Code (ECC)](entries/ecc-plugin.md) | plugin | open | rate-limited (429 errors); trial when accessible | plugin, hub, all-in-one |
| [FluidDocs Deck Builder](entries/fluiddocs-deck-builder.md) | plugin | open | Well-built skill/plugin pack for HTML slide decks; interesting multi-reviewer architecture but outside bioinformatics workflows | presentation, slides, skill-pack, claude-code-plugin, html, pdf-import |
| [Frontier](entries/frontier.md) | plugin | open | Well-architected multi-harness orchestration runtime for Claude Code; early preview but the token-economics argument and delegation model are sound | claude-code, orchestration, multi-model, delegation, pi, codex, ollama, omlx |
| [Google Workspace CLI (gws)](entries/googleworkspace-cli.md) | cli-tool | open | Rust CLI with agent-first JSON output and 100+ bundled SKILL.md files covering all Workspace APIs; pre-v1.0 with breaking changes expected | google-workspace, gmail, drive, calendar, sheets, agent-skills, oauth, json-output, rust |
| [Graphify](entries/graphify.md) | framework | open | direct inspiration for kb graph; concepts like confidence-tagged edges and clustering worth learning from | knowledge-graph, ast, visualization, kb |
| [GraphRAG & Agent Memory LinkedIn Series](entries/graphrag-agent-memory-linkedin-series.md) | reference | open | Six-post series covering GraphRAG design, ontology modeling, and unified agent memory architecture — useful conceptual grounding for KG-backed agents. | graphrag, knowledge-graph, ontology, agent-memory, reasoning, langgraph, crewai |
| [Grill With Docs](entries/grill-with-docs.md) | skill | open | Well-structured DDD design-review skill that enforces domain language, but relies on companion format files (CONTEXT-FORMAT.md, ADR-FORMAT.md) not bundled with the skill. | domain-driven-design, design-review, documentation, adr, glossary, planning |
| [Headroom](entries/headroom.md) | framework | open | Powerful context compression with real benchmarks, but proxy/MITM position and headroom learn's CLAUDE.md writes are significant trust risks for adoption without review | context-compression, token-reduction, mcp-server, proxy, memory, agent-wrap, claude-code |
| [Headroom Desktop](entries/headroom-desktop.md) | plugin | open | Solid local-first Claude Code cost optimizer with hook injection into ~/.claude/settings.json — worth monitoring given agent-lockdown relevance, but macOS-only stable and single-contributor | token-optimization, cost-reduction, claude-code, proxy, compression, tauri, hook |
| [Immich](entries/immich.md) | framework | open | Production-ready self-hosted Google Photos alternative with AI search; not agent tooling but solid self-hosted media infrastructure. | self-hosted, photo-management, video, mobile, ai-search, facial-recognition, oauth, docker |
| [Inbox Zero](entries/inbox-zero.md) | framework | open | AI-powered self-hostable email management app — strong open-source email assistant, not a developer/agent toolkit. | email, ai-assistant, gmail, productivity, self-hosted, open-source |
| [jcode](entries/jcode.md) | framework | open | Feature-rich Rust coding agent harness with exceptional performance (14ms boot, 28MB RAM), swarm collaboration, and 30+ provider integrations; compelling alternative harness to watch | cli-agent, rust, multi-provider, swarm, memory, browser-automation, performance |
| [Karakeep](entries/karakeep.md) | framework | open | Self-hostable AI bookmark manager with REST API, official agent skills, and Ollama support — agent-friendly but self-described as under heavy development. | bookmarks, knowledge-management, self-hosted, llm, tagging, search, rest-api, agent-friendly |
| [Langflow](entries/langflow.md) | framework | open | Heavy visual-builder platform with native MCP-server export; too large for direct adoption but worth monitoring for MCP workflow integration patterns. | visual-builder, agentic-workflows, mcp-server, llm-orchestration, multi-agent, python, open-source |
| [LocateAnything](entries/locate-anything.md) | framework | open | novel parallel box decoding for vision-language grounding; 3B model on HuggingFace; evaluate for spatial/histology image analysis when pipeline matures | vision, grounding, object-detection, nvidia, spatial, histology, image-analysis |
| [MarkItDown](entries/markitdown.md) | cli-tool | open | directly useful for converting PDFs, Excel, PPTX, and other docs to markdown for LLM pipelines; MIT, Microsoft-maintained | markdown, conversion, pdf, documents, excel, llm-preprocessing |
| [Maxun](entries/maxun.md) | framework | open | Capable no-code web data platform with MCP support and LLM extraction, but early-stage and AGPLv3 copyleft limits commercial embedding | web-scraping, data-extraction, no-code, mcp-server, llm, crawling, self-hosted |
| [MemPalace](entries/mempalace.md) | framework | open | Local-first AI memory with 96.6% R@5 retrieval, 33 MCP tools, verbatim storage, and pluggable backends; strong benchmarks and Claude Code integration make it worth trialing | memory, semantic-search, mcp-server, local-first, chromadb, knowledge-graph, claude-code |
| [MemStack](entries/memstack.md) | framework | open | Free-tier skill library is substantial but the PyPI MCP loader performs opaque license checks and stores credentials in-process, warranting supply-chain caution before adoption | skills, memory, sqlite, hooks, tts, mcp-server, freemium, skill-loader, claude-code |
| [mlx-vlm TurboQuant (Apple Silicon KV Cache Compression)](entries/mlx-vlm-turboquant.md) | framework | open | Production-quality Metal kernels implementing TurboQuant on Apple Silicon; benchmarked and ready for review but PR not yet merged | quantization, kv-cache, apple-silicon, mlx, metal, inference, vision-language |
| [Model Workspace Protocol (MWP)](entries/model-workspace-protocol.md) | reference | open | Research paper proposing filesystem structure as agent orchestration; numbered folders + markdown prompts replace multi-agent frameworks for sequential workflows | research, orchestration, filesystem, agent-architecture, unix-philosophy, markdown |
| [n8n MCP Server](entries/n8n-mcp.md) | mcp-server | open | powerful workflow automation bridge but heavy dependency; evaluate when pipeline orchestration needs outgrow kb dispatch | mcp, n8n, workflow-automation, orchestration, integrations |
| [NVIDIA Build (NIM)](entries/nvidia-build.md) | framework | open | NVIDIA's model API catalog and NIM inference microservices; broad model access but enterprise-focused with GPU-heavy deployment requirements | nvidia, nim, model-api, inference, gpu, enterprise |
| [OBLITERATUS](entries/obliteratus.md) | framework | open | Mechanistic interpretability research toolkit for refusal removal — notable as a reference for alignment geometry, but not safe to adopt in agent pipelines and irrelevant to bioinformatics workflows | llm, mechanistic-interpretability, abliteration, alignment, safety-bypass, research, gradio, python |
| [Obsidian Skills (Kepano)](entries/obsidian-skills.md) | skill | open | Obsidian-specific; Defuddle (web→clean markdown) and skill packaging patterns worth noting | obsidian, skills, markdown, canvas, defuddle, web-extraction |
| [Odysseus](entries/odysseus.md) | framework | open | Feature-rich self-hosted AI workspace with massive community momentum, but weeks-old with unsandboxed agent shell execution | self-hosted, ai-workspace, agents, local-models, docker, research, email, mcp |
| [One Skill to Rule Them All](entries/one-skill-to-rule-them-all.md) | meta-skill | open | proposes NEW skills from observed patterns; complementary to superpowers routing | meta-skill, pattern-detection, skill-generation |
| [Onyx AI Platform](entries/onyx-ai-platform.md) | framework | open | Full self-hostable AI platform with agentic RAG and MCP — notable architecture reference, but too deployment-heavy to adopt as a composable toolkit component | rag, agentic-rag, self-hosted, llm, mcp, knowledge-retrieval, enterprise, connectors |
| [Open Knowledge Format (OKF)](entries/open-knowledge-format.md) | reference | open | Google's draft spec for agent-friendly knowledge representation using Markdown + YAML frontmatter; closely aligned with our wiki pattern but v0.1 draft status | knowledge-management, specification, google, markdown, frontmatter, agent-friendly, wiki |
| [Open WebUI](entries/open-webui.md) | framework | open | Leading self-hosted LLM web UI with RAG, pipelines, and enterprise auth — relevant infrastructure context but custom non-SPDX license limits adoption | llm-ui, self-hosted, rag, ollama, openai-compatible, pipelines, enterprise, docker, python |
| [opencode-fff-search](entries/opencode-fff-search.md) | plugin | open | Drop-in OpenCode grep/glob replacement with Rust-backed in-memory index, frecency ranking, and SIMD literal matching — 3-10x faster than process-spawning ripgrep at scale. | opencode, search, grep, glob, rust, performance, fuzzy-search, lmdb, frecency, simd |
| [OpenDataLoader PDF](entries/opendataloader-pdf.md) | cli-tool | open | Top-benchmarked open-source PDF parser with bounding boxes, formula extraction, and RAG-ready output — worth piloting for bioinformatics literature ingestion before committing. | pdf, rag, ocr, markdown, json, bioinformatics, langchain, accessibility |
| [OpenRouter](entries/openrouter.md) | framework | open | Unified LLM API gateway supporting 200+ models — useful as infrastructure reference, not directly needed when using Claude natively. | llm, api-gateway, model-routing, openai-compatible, infrastructure |
| [OpenSpace](entries/openspace.md) | framework | open | Compelling skill-evolution engine for Claude Code agents but very new (v0.1.0), self-published benchmark, and significant security surface from community skill ingestion | skill-evolution, mcp-server, claude-code, agent-learning, skill-sharing, token-efficiency |
| [Overcut — Agentic SDLC Orchestration](entries/overcut.md) | framework | open | Commercial orchestration layer for multi-agent SDLC; addresses real coordination gap but closed-source, early-stage, and not yet individually usable | agent-orchestration, sdlc, multi-agent, devops, workflow-automation |
| [Paperless-ngx](entries/paperless-ngx.md) | framework | open | Mature self-hosted document management system — useful for archiving research docs but not an agent tool or developer library | document-management, self-hosted, ocr, search, archive, docker, paperless |
| [Pi-hole](entries/pi-hole.md) | reference | open | Network-wide DNS ad blocker — mature infrastructure tool, informational for lab network hygiene | dns, ad-blocking, privacy, self-hosted, network, sinkhole, dhcp |
| [PII Detection / Compliance Skills](entries/pii-detection.md) | skill | open | HIPAA/CCPA/PCI-DSS coverage; pilot if handling sensitive data | pii, compliance, hipaa, ccpa, security |
| [Ponytail](entries/ponytail.md) | plugin | open | YAGNI enforcement plugin with strong benchmarks (80-94% less code, 47-77% cheaper); multi-platform support and clean design make it worth trialing | claude-code, codex, plugin, yagni, minimalism, code-quality, over-engineering |
| [Qwen3.6-27B](entries/qwen3-6-27b.md) | framework | open | Strong open-weight 27B model with near-frontier coding scores and 262K context; promising local worker model but requires multi-GPU or quantization for practical use | llm, open-weights, coding, agentic, multimodal, qwen, local-inference, llama-cpp |
| [Remote Control](entries/remote-control.md) | reference | open | built-in feature; try for long sessions | mobile, remote, sessions |
| [Repowire](entries/repowire.md) | framework | open | Compelling multi-agent mesh for cross-repo coordination, but macOS/Linux only and default spawn config ships dangerous permission flags | multi-agent, orchestration, mcp, claude-code, codex, gemini-cli, daemon, mesh, tmux, telegram, slack |
| [rtk — CLI Proxy for LLM Token Reduction](entries/rtk.md) | cli-tool | open | Directly reduces Claude Code token costs 60-90% via transparent Bash hook; Windows hook requires WSL but filters work natively | token-optimization, claude-code, cli, rust, bash-hook, ai-tooling |
| [RuView WiFi Sensing Platform](entries/ruview-wifi-sensing.md) | framework | open | Interesting hardware+agent integration with a Claude Code plugin and MCP server, but beta software requiring physical ESP32 hardware for core capabilities | wifi-sensing, esp32, mcp-server, claude-code-plugin, edge-ai, vital-signs, presence-detection, iot, physiological-signals |
| [Scheduled Multi-Agent Coordinator Pattern](entries/scheduled-multi-agent-coordinator.md) | agent-pattern | open | Useful architecture pattern for persistent scheduled agents with coordinator + messaging; NanoClaw and Hermes are mature implementations | multi-agent, scheduling, coordinator, persistent-agent, messaging-integration, codex, nanoclaw, hermes |
| [SkillOpt](entries/skillopt.md) | framework | open | Microsoft research framework that optimizes agent skills via training loops; +23.5 point lifts on Claude Code, Sleep mode for nightly skill consolidation is directly relevant | skill-optimization, microsoft, training-loop, claude-code, codex, agent-skills, research |
| [sota-scan](entries/sota-scan.md) | skill | open | Useful comparative benchmarking skill for Claude Code, but single-contributor, no tests, and high token cost for exhaustive mode | benchmarking, competitive-analysis, code-quality, claude-code, skill |
| [Stirling PDF](entries/stirling-pdf.md) | cli-tool | open | Self-hosted REST API for 50+ PDF operations enables privacy-preserving agentic PDF workflows without external services | pdf, self-hosted, rest-api, docker, ocr, document-processing, automation |
| [Synthesize Bio](entries/synthesize-bio.md) | mcp-server | open | Generates synthetic human gene expression profiles on demand via natural-language prompts — unique bioinformatics capability, but proprietary SaaS requiring account and external API trust. | bioinformatics, rna-seq, gene-expression, synthetic-data, genomics, single-cell, bulk-rna |
| [TeamPCP/Miasma npm Supply Chain Attack (June 2026)](entries/teampcp-miasma-npm-supply-chain-attack-2026.md) | reference | open | Incident writeup documenting credential-harvesting malware and ~/.claude/settings.json hook persistence — directly relevant to agent-lockdown hardening (WK-0031) | security, supply-chain, npm, claude-code, incident-report, credential-theft, persistence |
| [Tolvi — Engineering Decision Vault](entries/tolvi.md) | framework | open | Solid CAG/RAG dual-mode decision-capture design but pre-1.0, small project, and overlaps with kb already in use | decisions, knowledge-management, adr, vault, claude-code-skill, rag, cag, go-cli, agent-integration |
| [TurboQuant — Extreme KV Cache Compression](entries/turboquant.md) | reference | open | Foundational Google Research algorithm (ICLR 2026) for 3-4 bit KV cache compression with zero accuracy loss; growing downstream ecosystem but no single canonical package yet | quantization, kv-cache, compression, inference, memory-optimization, google-research |
| [Tutorial Creator](entries/tutorial-creator.md) | skill | open | good for knowledge retention and onboarding | tutorials, onboarding, knowledge-retention |
| [UI/UX Pro Max Skill](entries/ui-ux-pro-max-skill.md) | skill | open | comprehensive design system generation but focused on general web/mobile UI; evaluate when dashboard/report aesthetics become a priority | ui, ux, design-system, typography, color-palettes, dashboards, visualization |
| [Understand Anything](entries/understand-anything.md) | plugin | open | Interactive knowledge graph plugin for codebases with multi-agent pipeline and broad platform support; impressive but heavy — watch for maturity and real-world performance on large repos | claude-code, knowledge-graph, codebase-analysis, visualization, tree-sitter, onboarding, plugin |
| [Verify Before Claim (Third Brain V5)](entries/verify-before-claim.md) | reference | open | superpowers verification-before-completion covers this; confidence model is the novel addition | verification, quality, confidence-model |
| [Weft](entries/weft-language.md) | framework | open | Novel AI orchestration language with typed nodes, durable execution, and human-in-the-loop primitives — early-stage but architecturally interesting | programming-language, ai-orchestration, durable-execution, visual-programming, human-in-the-loop, rust |
| [Zero to Mastery ML](entries/zero-to-mastery-ml.md) | reference | open | Comprehensive ML/DS course materials (NumPy, pandas, sklearn, TensorFlow); useful learning reference but not a tool or workflow component | machine-learning, data-science, course, numpy, pandas, scikit-learn, tensorflow, jupyter |

## By Workflow

### scRNA-seq

- [BMAD Skill Forge](entries/bmad-skill-forge.md) — open — strong fit for bioinformatics tool skill generation; start with Brief tier on samtools
- [Book to Skill](entries/book-to-skill.md) — open — directly useful for computational biology methods PDFs
- [Web Artifacts Builder](entries/web-artifacts-builder.md) — adopted — use when markdown isn't enough for interactive reports/dashboards

### spatial

- [BMAD Skill Forge](entries/bmad-skill-forge.md) — open — strong fit for bioinformatics tool skill generation; start with Brief tier on samtools
- [Book to Skill](entries/book-to-skill.md) — open — directly useful for computational biology methods PDFs
- [LocateAnything](entries/locate-anything.md) — open — novel parallel box decoding for vision-language grounding; 3B model on HuggingFace; evaluate for spatial/histology image analysis when pipeline matures
- [Web Artifacts Builder](entries/web-artifacts-builder.md) — adopted — use when markdown isn't enough for interactive reports/dashboards

### General

- [AdGuard Home](entries/adguard-home.md) — open — Production-ready network-wide DNS ad/tracker blocker — infrastructure tool, not an agent/dev workflow component
- [ADHD](entries/adhd.md) — open — parallel divergent ideation via isolated cognitive frames; overlaps with superpowers:brainstorming but the frame isolation and scoring mechanics are worth studying
- [Advise Project Approach](entries/advise-project-approach.md) — open — structured project-level architecture research with comparable analysis, cost checks, and tradeoff discipline; complements /catalog (tool-level) with project-level advisory
- [Advisor Strategy](entries/advisor-strategy.md) — open — architectural concept for cost-effective agent orchestration; executor/advisor split
- [Agent Session Resume](entries/agent-session-resume.md) — open — Cross-agent session resume skill with structured checkpoint workflow; overlaps with our handoff skill but adds multi-agent-platform support (Codex, Cursor, Antigravity, OpenCode)
- [AI Memory Comparison](entries/ai-memory-comparison.md) — adopted — Definitive source-backed survey of 73 open-source AI agent memory systems across 79 features — every claim cites public code or docs.
- [AI Needs What ALCOA+ Gave Records](entries/alcoa-plus-for-ai.md) — open — Useful framing for regulated-AI governance but no actionable tool or framework yet — CASTEM teased but unpublished
- [AirLLM](entries/airllm.md) — open — Clever layer-shard inference to run 70B models on 4GB VRAM, but maintenance has stalled since August 2024 while better-maintained alternatives (Ollama/llama.cpp) have matured.
- [Architect Loop](entries/architect-loop.md) — open — Research-backed cross-vendor agent loop with strong separation of concerns; excellent design patterns for gated, worktree-isolated multi-agent builds
- [ASI-Evolve](entries/asi-evolve.md) — open — Impressive autonomous research-loop results but arbitrary code execution per round, no stated license, and very new (2026 academic repo)
- [Autoharness](entries/autoharness.md) — open — needs eval benchmarks first; pilot when we have eval criteria for our skills/agents
- [Autoresearch](entries/autoresearch.md) — open — Highly influential autonomous experimentation loop pattern, but ML-training-specific — transferable idea, not transferable code
- [Awesome Claude Code](entries/awesome-claude-code.md) — open — curated Claude Code ecosystem list; use as discovery source for future catalog inbox items
- [BioMysteryBench](entries/biomysterybench.md) — open — 99-problem bioinformatics research benchmark from Anthropic — directly useful for evaluating agent performance on real research tasks.
- [Browser Use](entries/browser-use.md) — open — MIT-licensed Python/Rust framework giving LLM agents real browser control — useful for web scraping, form automation, and accessing bioinformatics portals, but Rust-core beta is still experimental and full capability requires commercial cloud
- [CASTEM: First Principles for Model-Mediated Work](entries/castem-first-principles-model-mediated-work.md) — open — Portable 6-criterion mnemonic (Credible, Auditable, Supervised, Traceable, Explainable, Monitored) for AI governance in regulated settings — good design checklist, no tooling.
- [CL4R1T4S](entries/cl4r1t4s.md) — open — Collection of leaked AI system prompts; useful security-awareness reference but README contains embedded prompt injection
- [Claude Agent Teams](entries/agent-teams.md) — adopted — primary interactive dispatch path; subscription billing, no API credits needed
- [Claude Code Remote Prompt Hardening](entries/claude-code-remote-prompt-hardening.md) — open — env vars to block remote system prompt injection in Claude Code; operational hardening knowledge for security-sensitive environments
- [Claude Decision Pressure-Test & Context Handoff Prompts](entries/claude-decision-pressure-test-and-context-handoff.md) — open — Two reusable prompting patterns — steelman/red-team verdict loop and structured context handoff — worth keeping as copy-paste references
- [Claude Howto](entries/claude-howto.md) — open — Well-structured tutorial guide with copy-paste templates, but it is a learning reference rather than an installable tool.
- [Claude Mem](entries/claude-mem.md) — rejected — kb wiki + Claude Code built-in memory cover our needs; adds SQLite + Chroma + worker complexity without clear benefit
- [Claude Meta-Skill](entries/claude-meta-skill.md) — open — Curated collection of 11 Claude Code skills; mostly Chinese-language or general-dev focused, with significant overlap to existing catalog entries
- [Claude Native Subagents](entries/native-subagents.md) — adopted — lightweight HO consultation route within existing sessions; no separate billing
- [Claude Peers MCP](entries/claude-peers-mcp.md) — open — Novel multi-session peer messaging, but mandatory --dangerously-skip-permissions flag is a hard blocker for safe use
- [Claude Spellbook](entries/claude-spellbook.md) — open — 50 skills, 7 agents, 11 slash commands — use as pattern reference, not default install
- [claude-pee](entries/claude-pee.md) — rejected — PTY wrapper driving interactive CLI; inherently brittle, breaks on CLI version changes
- [Claw Code](entries/claw-code.md) — open — Rust reimplementation of a CLI agent harness; self-described museum exhibit maintained by agents rather than a production tool
- [CLI-Anything](entries/cli-anything.md) — open — Generates production-grade, agent-native CLI harnesses from any codebase via a 7-phase pipeline; directly integrates with Claude Code as a plugin and emits SKILL.md files for skill discovery.
- [Cobalt](entries/cobalt.md) — open — General-purpose media downloader with a self-hosted API; no agent, skill, or bioinformatics relevance.
- [Codebase Reasoning Topology](entries/codebase-reasoning-topology.md) — open — heavy for daily use but interesting as a pre-flight checklist concept
- [Codex Memory Cleanup](entries/codex-memory-cleanup.md) — open — operational tip: delete state/log/global-state files if Codex performance degrades
- [Context Graph Compressor](entries/context-graph-compressor.md) — open — Structured JSON graph handoff with importance tagging and cross-LLM portability beats plain-text handoff skills; too new/single-contributor to adopt outright
- [Crawl4AI](entries/crawl4ai.md) — open — Best-in-class async web-to-Markdown crawler for agent/RAG pipelines, but Docker API has had dense critical CVEs; library mode is safe to pilot
- [Creating CLAUDE.md](entries/creating-claude-md.md) — rejected — /init skill already covers repo-scanning CLAUDE.md generation
- [CrowdSec](entries/crowdsec.md) — open — Production-ready crowdsourced IDS/IPS framework — valuable for hardening servers hosting agent infrastructure, outside direct agent/bioinformatics workflows.
- [Deny .env Reads via Permissions](entries/deny-env-reads.md) — open — Useful security hygiene tip for Claude Code projects; documents a built-in feature rather than a new tool
- [Distill](entries/distill.md) — open — Local 1.7B model pipe-filter for CLI output compression is a real problem but requires 8–16 GB RAM and relies on an unaudited HuggingFace model; overlaps with rtk.
- [ECC — Everything Claude Code (GitHub)](entries/ecc-github.md) — open — massive cross-harness skill/hook/agent system worth monitoring but high adoption complexity and scope overlap with existing stack
- [ERA — Empirical Research Assistant](entries/era-empirical-research-assistant.md) — open — Interesting LLM+tree-search loop for scientific code generation, but Gemini-locked, research-grade, and not directly applicable to Claude Code workflows today
- [Everything Claude Code (ECC)](entries/ecc-plugin.md) — open — rate-limited (429 errors); trial when accessible
- [FluidDocs Deck Builder](entries/fluiddocs-deck-builder.md) — open — Well-built skill/plugin pack for HTML slide decks; interesting multi-reviewer architecture but outside bioinformatics workflows
- [Frontier](entries/frontier.md) — open — Well-architected multi-harness orchestration runtime for Claude Code; early preview but the token-economics argument and delegation model are sound
- [gbrain](entries/gbrain.md) — rejected — kb wiki already provides persistent typed records with relationships and search
- [Get Shit Done (GSD)](entries/get-shit-done.md) — rejected — deprecated (moved to GSD Redux); superpowers skill system already covers meta-prompting and spec-driven development
- [Google Workspace CLI (gws)](entries/googleworkspace-cli.md) — open — Rust CLI with agent-first JSON output and 100+ bundled SKILL.md files covering all Workspace APIs; pre-v1.0 with breaking changes expected
- [Graphify](entries/graphify.md) — open — direct inspiration for kb graph; concepts like confidence-tagged edges and clustering worth learning from
- [GraphRAG & Agent Memory LinkedIn Series](entries/graphrag-agent-memory-linkedin-series.md) — open — Six-post series covering GraphRAG design, ontology modeling, and unified agent memory architecture — useful conceptual grounding for KG-backed agents.
- [Grill With Docs](entries/grill-with-docs.md) — open — Well-structured DDD design-review skill that enforces domain language, but relies on companion format files (CONTEXT-FORMAT.md, ADR-FORMAT.md) not bundled with the skill.
- [gstack](entries/gstack.md) — rejected — kb dispatch covers the relevant orchestration patterns; browser/deployment out of scope
- [Headroom](entries/headroom.md) — open — Powerful context compression with real benchmarks, but proxy/MITM position and headroom learn's CLAUDE.md writes are significant trust risks for adoption without review
- [Headroom Desktop](entries/headroom-desktop.md) — open — Solid local-first Claude Code cost optimizer with hook injection into ~/.claude/settings.json — worth monitoring given agent-lockdown relevance, but macOS-only stable and single-contributor
- [Immich](entries/immich.md) — open — Production-ready self-hosted Google Photos alternative with AI search; not agent tooling but solid self-hosted media infrastructure.
- [Inbox Zero](entries/inbox-zero.md) — open — AI-powered self-hostable email management app — strong open-source email assistant, not a developer/agent toolkit.
- [jcode](entries/jcode.md) — open — Feature-rich Rust coding agent harness with exceptional performance (14ms boot, 28MB RAM), swarm collaboration, and 30+ provider integrations; compelling alternative harness to watch
- [Karakeep](entries/karakeep.md) — open — Self-hostable AI bookmark manager with REST API, official agent skills, and Ollama support — agent-friendly but self-described as under heavy development.
- [Karpathy's 12 Rules for CLAUDE.md](entries/karpathy-12-rules.md) — adopted — Rules 6 (token budgets) and 12 (fail loud) not yet in our stack
- [Karpathy's LLM Wiki Pattern](entries/karpathy-llm-wiki.md) — adopted — Foundational pattern doc for LLM-maintained personal knowledge bases — directly describes the architecture kb-wiki implements
- [Langflow](entries/langflow.md) — open — Heavy visual-builder platform with native MCP-server export; too large for direct adoption but worth monitoring for MCP workflow integration patterns.
- [MarkItDown](entries/markitdown.md) — open — directly useful for converting PDFs, Excel, PPTX, and other docs to markdown for LLM pipelines; MIT, Microsoft-maintained
- [Maxun](entries/maxun.md) — open — Capable no-code web data platform with MCP support and LLM extraction, but early-stage and AGPLv3 copyleft limits commercial embedding
- [MemPalace](entries/mempalace.md) — open — Local-first AI memory with 96.6% R@5 retrieval, 33 MCP tools, verbatim storage, and pluggable backends; strong benchmarks and Claude Code integration make it worth trialing
- [MemStack](entries/memstack.md) — open — Free-tier skill library is substantial but the PyPI MCP loader performs opaque license checks and stores credentials in-process, warranting supply-chain caution before adoption
- [mlx-vlm TurboQuant (Apple Silicon KV Cache Compression)](entries/mlx-vlm-turboquant.md) — open — Production-quality Metal kernels implementing TurboQuant on Apple Silicon; benchmarked and ready for review but PR not yet merged
- [Model Workspace Protocol (MWP)](entries/model-workspace-protocol.md) — open — Research paper proposing filesystem structure as agent orchestration; numbered folders + markdown prompts replace multi-agent frameworks for sequential workflows
- [n8n MCP Server](entries/n8n-mcp.md) — open — powerful workflow automation bridge but heavy dependency; evaluate when pipeline orchestration needs outgrow kb dispatch
- [NVIDIA Build (NIM)](entries/nvidia-build.md) — open — NVIDIA's model API catalog and NIM inference microservices; broad model access but enterprise-focused with GPU-heavy deployment requirements
- [oauth-cli-coder](entries/oauth-cli-coder.md) — rejected — OAuth-based CLI automation; adds auth complexity without solving durability
- [OBLITERATUS](entries/obliteratus.md) — open — Mechanistic interpretability research toolkit for refusal removal — notable as a reference for alignment geometry, but not safe to adopt in agent pipelines and irrelevant to bioinformatics workflows
- [Obsidian Skills (Kepano)](entries/obsidian-skills.md) — open — Obsidian-specific; Defuddle (web→clean markdown) and skill packaging patterns worth noting
- [Odysseus](entries/odysseus.md) — open — Feature-rich self-hosted AI workspace with massive community momentum, but weeks-old with unsandboxed agent shell execution
- [One Skill to Rule Them All](entries/one-skill-to-rule-them-all.md) — open — proposes NEW skills from observed patterns; complementary to superpowers routing
- [Onyx AI Platform](entries/onyx-ai-platform.md) — open — Full self-hostable AI platform with agentic RAG and MCP — notable architecture reference, but too deployment-heavy to adopt as a composable toolkit component
- [Open Knowledge Format (OKF)](entries/open-knowledge-format.md) — open — Google's draft spec for agent-friendly knowledge representation using Markdown + YAML frontmatter; closely aligned with our wiki pattern but v0.1 draft status
- [Open WebUI](entries/open-webui.md) — open — Leading self-hosted LLM web UI with RAG, pipelines, and enterprise auth — relevant infrastructure context but custom non-SPDX license limits adoption
- [OpenClaw](entries/openclaw.md) — rejected — ecosystem signal for agentic workspaces; not a concrete kb comparison
- [opencode-fff-search](entries/opencode-fff-search.md) — open — Drop-in OpenCode grep/glob replacement with Rust-backed in-memory index, frecency ranking, and SIMD literal matching — 3-10x faster than process-spawning ripgrep at scale.
- [OpenDataLoader PDF](entries/opendataloader-pdf.md) — open — Top-benchmarked open-source PDF parser with bounding boxes, formula extraction, and RAG-ready output — worth piloting for bioinformatics literature ingestion before committing.
- [OpenRouter](entries/openrouter.md) — open — Unified LLM API gateway supporting 200+ models — useful as infrastructure reference, not directly needed when using Claude natively.
- [OpenSpace](entries/openspace.md) — open — Compelling skill-evolution engine for Claude Code agents but very new (v0.1.0), self-published benchmark, and significant security surface from community skill ingestion
- [Overcut — Agentic SDLC Orchestration](entries/overcut.md) — open — Commercial orchestration layer for multi-agent SDLC; addresses real coordination gap but closed-source, early-stage, and not yet individually usable
- [Paperless-ngx](entries/paperless-ngx.md) — open — Mature self-hosted document management system — useful for archiving research docs but not an agent tool or developer library
- [Pi-hole](entries/pi-hole.md) — open — Network-wide DNS ad blocker — mature infrastructure tool, informational for lab network hygiene
- [PII Detection / Compliance Skills](entries/pii-detection.md) — open — HIPAA/CCPA/PCI-DSS coverage; pilot if handling sensitive data
- [Ponytail](entries/ponytail.md) — open — YAGNI enforcement plugin with strong benchmarks (80-94% less code, 47-77% cheaper); multi-platform support and clean design make it worth trialing
- [Qwen3.6-27B](entries/qwen3-6-27b.md) — open — Strong open-weight 27B model with near-frontier coding scores and 262K context; promising local worker model but requires multi-GPU or quantization for practical use
- [Remote Control](entries/remote-control.md) — open — built-in feature; try for long sessions
- [Repowire](entries/repowire.md) — open — Compelling multi-agent mesh for cross-repo coordination, but macOS/Linux only and default spawn config ships dangerous permission flags
- [rtk — CLI Proxy for LLM Token Reduction](entries/rtk.md) — open — Directly reduces Claude Code token costs 60-90% via transparent Bash hook; Windows hook requires WSL but filters work natively
- [RuView WiFi Sensing Platform](entries/ruview-wifi-sensing.md) — open — Interesting hardware+agent integration with a Claude Code plugin and MCP server, but beta software requiring physical ESP32 hardware for core capabilities
- [Scheduled Multi-Agent Coordinator Pattern](entries/scheduled-multi-agent-coordinator.md) — open — Useful architecture pattern for persistent scheduled agents with coordinator + messaging; NanoClaw and Hermes are mature implementations
- [Skill Router](entries/skill-router.md) — rejected — superpowers using-superpowers already handles skill routing
- [SkillOpt](entries/skillopt.md) — open — Microsoft research framework that optimizes agent skills via training loops; +23.5 point lifts on Claude Code, Sleep mode for nightly skill consolidation is directly relevant
- [sota-scan](entries/sota-scan.md) — open — Useful comparative benchmarking skill for Claude Code, but single-contributor, no tests, and high token cost for exhaustive mode
- [Spiderbrain V3](entries/spiderbrain-v3.md) — rejected — BSL license; master/column concept is the key takeaway for kb graph
- [Stirling PDF](entries/stirling-pdf.md) — open — Self-hosted REST API for 50+ PDF operations enables privacy-preserving agentic PDF workflows without external services
- [Storybloq](entries/storybloq.md) — rejected — PolyForm Noncommercial license + heavy overlap with kb wiki
- [Superpowers: Verification Before Completion](entries/superpowers-verification-before-completion.md) — adopted — canonical 'evidence before claims' gate skill — already active in this project and referenced by other catalog entries as the standard
- [Syncthing](entries/syncthing.md) — adopted — Mature, audited, decentralized file sync daemon — production-grade for agent artifact persistence and cross-machine data sharing.
- [Synthesize Bio](entries/synthesize-bio.md) — open — Generates synthetic human gene expression profiles on demand via natural-language prompts — unique bioinformatics capability, but proprietary SaaS requiring account and external API trust.
- [TeamPCP/Miasma npm Supply Chain Attack (June 2026)](entries/teampcp-miasma-npm-supply-chain-attack-2026.md) — open — Incident writeup documenting credential-harvesting malware and ~/.claude/settings.json hook persistence — directly relevant to agent-lockdown hardening (WK-0031)
- [Third Brain V5 (Wiki/Knowledge Layer)](entries/third-brain-v5-wiki.md) — rejected — Obsidian-specific schema, heavy; staleness and contradiction detection concepts worth noting for kb
- [Tolvi — Engineering Decision Vault](entries/tolvi.md) — open — Solid CAG/RAG dual-mode decision-capture design but pre-1.0, small project, and overlaps with kb already in use
- [TurboQuant — Extreme KV Cache Compression](entries/turboquant.md) — open — Foundational Google Research algorithm (ICLR 2026) for 3-4 bit KV cache compression with zero accuracy loss; growing downstream ecosystem but no single canonical package yet
- [Tutorial Creator](entries/tutorial-creator.md) — open — good for knowledge retention and onboarding
- [UI/UX Pro Max Skill](entries/ui-ux-pro-max-skill.md) — open — comprehensive design system generation but focused on general web/mobile UI; evaluate when dashboard/report aesthetics become a priority
- [Understand Anything](entries/understand-anything.md) — open — Interactive knowledge graph plugin for codebases with multi-agent pipeline and broad platform support; impressive but heavy — watch for maturity and real-world performance on large repos
- [Unforget](entries/unforget.md) — rejected — scan-for-escaped-items pattern worth noting for future kb lint rule or audit command
- [Vaultwarden](entries/vaultwarden.md) — adopted — Production-grade self-hosted Bitwarden-compatible password server in Rust; fraction of the resource footprint of the official server
- [Verify Before Claim (Third Brain V5)](entries/verify-before-claim.md) — open — superpowers verification-before-completion covers this; confidence model is the novel addition
- [Weft](entries/weft-language.md) — open — Novel AI orchestration language with typed nodes, durable execution, and human-in-the-loop primitives — early-stage but architecturally interesting
- [Zero to Mastery ML](entries/zero-to-mastery-ml.md) — open — Comprehensive ML/DS course materials (NumPy, pandas, sklearn, TensorFlow); useful learning reference but not a tool or workflow component

## By Category

### agent-pattern

- [Advisor Strategy](entries/advisor-strategy.md) — open — architectural concept for cost-effective agent orchestration; executor/advisor split
- [Architect Loop](entries/architect-loop.md) — open — Research-backed cross-vendor agent loop with strong separation of concerns; excellent design patterns for gated, worktree-isolated multi-agent builds
- [Claude Agent Teams](entries/agent-teams.md) — adopted — primary interactive dispatch path; subscription billing, no API credits needed
- [Claude Native Subagents](entries/native-subagents.md) — adopted — lightweight HO consultation route within existing sessions; no separate billing
- [Scheduled Multi-Agent Coordinator Pattern](entries/scheduled-multi-agent-coordinator.md) — open — Useful architecture pattern for persistent scheduled agents with coordinator + messaging; NanoClaw and Hermes are mature implementations

### cli-tool

- [claude-pee](entries/claude-pee.md) — rejected — PTY wrapper driving interactive CLI; inherently brittle, breaks on CLI version changes
- [Cobalt](entries/cobalt.md) — open — General-purpose media downloader with a self-hosted API; no agent, skill, or bioinformatics relevance.
- [Distill](entries/distill.md) — open — Local 1.7B model pipe-filter for CLI output compression is a real problem but requires 8–16 GB RAM and relies on an unaudited HuggingFace model; overlaps with rtk.
- [Google Workspace CLI (gws)](entries/googleworkspace-cli.md) — open — Rust CLI with agent-first JSON output and 100+ bundled SKILL.md files covering all Workspace APIs; pre-v1.0 with breaking changes expected
- [MarkItDown](entries/markitdown.md) — open — directly useful for converting PDFs, Excel, PPTX, and other docs to markdown for LLM pipelines; MIT, Microsoft-maintained
- [oauth-cli-coder](entries/oauth-cli-coder.md) — rejected — OAuth-based CLI automation; adds auth complexity without solving durability
- [OpenDataLoader PDF](entries/opendataloader-pdf.md) — open — Top-benchmarked open-source PDF parser with bounding boxes, formula extraction, and RAG-ready output — worth piloting for bioinformatics literature ingestion before committing.
- [rtk — CLI Proxy for LLM Token Reduction](entries/rtk.md) — open — Directly reduces Claude Code token costs 60-90% via transparent Bash hook; Windows hook requires WSL but filters work natively
- [Stirling PDF](entries/stirling-pdf.md) — open — Self-hosted REST API for 50+ PDF operations enables privacy-preserving agentic PDF workflows without external services
- [Syncthing](entries/syncthing.md) — adopted — Mature, audited, decentralized file sync daemon — production-grade for agent artifact persistence and cross-machine data sharing.

### framework

- [AdGuard Home](entries/adguard-home.md) — open — Production-ready network-wide DNS ad/tracker blocker — infrastructure tool, not an agent/dev workflow component
- [AirLLM](entries/airllm.md) — open — Clever layer-shard inference to run 70B models on 4GB VRAM, but maintenance has stalled since August 2024 while better-maintained alternatives (Ollama/llama.cpp) have matured.
- [ASI-Evolve](entries/asi-evolve.md) — open — Impressive autonomous research-loop results but arbitrary code execution per round, no stated license, and very new (2026 academic repo)
- [Autoharness](entries/autoharness.md) — open — needs eval benchmarks first; pilot when we have eval criteria for our skills/agents
- [Autoresearch](entries/autoresearch.md) — open — Highly influential autonomous experimentation loop pattern, but ML-training-specific — transferable idea, not transferable code
- [Browser Use](entries/browser-use.md) — open — MIT-licensed Python/Rust framework giving LLM agents real browser control — useful for web scraping, form automation, and accessing bioinformatics portals, but Rust-core beta is still experimental and full capability requires commercial cloud
- [Claude Mem](entries/claude-mem.md) — rejected — kb wiki + Claude Code built-in memory cover our needs; adds SQLite + Chroma + worker complexity without clear benefit
- [Claw Code](entries/claw-code.md) — open — Rust reimplementation of a CLI agent harness; self-described museum exhibit maintained by agents rather than a production tool
- [CLI-Anything](entries/cli-anything.md) — open — Generates production-grade, agent-native CLI harnesses from any codebase via a 7-phase pipeline; directly integrates with Claude Code as a plugin and emits SKILL.md files for skill discovery.
- [Crawl4AI](entries/crawl4ai.md) — open — Best-in-class async web-to-Markdown crawler for agent/RAG pipelines, but Docker API has had dense critical CVEs; library mode is safe to pilot
- [CrowdSec](entries/crowdsec.md) — open — Production-ready crowdsourced IDS/IPS framework — valuable for hardening servers hosting agent infrastructure, outside direct agent/bioinformatics workflows.
- [ECC — Everything Claude Code (GitHub)](entries/ecc-github.md) — open — massive cross-harness skill/hook/agent system worth monitoring but high adoption complexity and scope overlap with existing stack
- [ERA — Empirical Research Assistant](entries/era-empirical-research-assistant.md) — open — Interesting LLM+tree-search loop for scientific code generation, but Gemini-locked, research-grade, and not directly applicable to Claude Code workflows today
- [gbrain](entries/gbrain.md) — rejected — kb wiki already provides persistent typed records with relationships and search
- [Get Shit Done (GSD)](entries/get-shit-done.md) — rejected — deprecated (moved to GSD Redux); superpowers skill system already covers meta-prompting and spec-driven development
- [Graphify](entries/graphify.md) — open — direct inspiration for kb graph; concepts like confidence-tagged edges and clustering worth learning from
- [gstack](entries/gstack.md) — rejected — kb dispatch covers the relevant orchestration patterns; browser/deployment out of scope
- [Headroom](entries/headroom.md) — open — Powerful context compression with real benchmarks, but proxy/MITM position and headroom learn's CLAUDE.md writes are significant trust risks for adoption without review
- [Immich](entries/immich.md) — open — Production-ready self-hosted Google Photos alternative with AI search; not agent tooling but solid self-hosted media infrastructure.
- [Inbox Zero](entries/inbox-zero.md) — open — AI-powered self-hostable email management app — strong open-source email assistant, not a developer/agent toolkit.
- [jcode](entries/jcode.md) — open — Feature-rich Rust coding agent harness with exceptional performance (14ms boot, 28MB RAM), swarm collaboration, and 30+ provider integrations; compelling alternative harness to watch
- [Karakeep](entries/karakeep.md) — open — Self-hostable AI bookmark manager with REST API, official agent skills, and Ollama support — agent-friendly but self-described as under heavy development.
- [Langflow](entries/langflow.md) — open — Heavy visual-builder platform with native MCP-server export; too large for direct adoption but worth monitoring for MCP workflow integration patterns.
- [LocateAnything](entries/locate-anything.md) — open — novel parallel box decoding for vision-language grounding; 3B model on HuggingFace; evaluate for spatial/histology image analysis when pipeline matures
- [Maxun](entries/maxun.md) — open — Capable no-code web data platform with MCP support and LLM extraction, but early-stage and AGPLv3 copyleft limits commercial embedding
- [MemPalace](entries/mempalace.md) — open — Local-first AI memory with 96.6% R@5 retrieval, 33 MCP tools, verbatim storage, and pluggable backends; strong benchmarks and Claude Code integration make it worth trialing
- [MemStack](entries/memstack.md) — open — Free-tier skill library is substantial but the PyPI MCP loader performs opaque license checks and stores credentials in-process, warranting supply-chain caution before adoption
- [mlx-vlm TurboQuant (Apple Silicon KV Cache Compression)](entries/mlx-vlm-turboquant.md) — open — Production-quality Metal kernels implementing TurboQuant on Apple Silicon; benchmarked and ready for review but PR not yet merged
- [NVIDIA Build (NIM)](entries/nvidia-build.md) — open — NVIDIA's model API catalog and NIM inference microservices; broad model access but enterprise-focused with GPU-heavy deployment requirements
- [OBLITERATUS](entries/obliteratus.md) — open — Mechanistic interpretability research toolkit for refusal removal — notable as a reference for alignment geometry, but not safe to adopt in agent pipelines and irrelevant to bioinformatics workflows
- [Odysseus](entries/odysseus.md) — open — Feature-rich self-hosted AI workspace with massive community momentum, but weeks-old with unsandboxed agent shell execution
- [Onyx AI Platform](entries/onyx-ai-platform.md) — open — Full self-hostable AI platform with agentic RAG and MCP — notable architecture reference, but too deployment-heavy to adopt as a composable toolkit component
- [Open WebUI](entries/open-webui.md) — open — Leading self-hosted LLM web UI with RAG, pipelines, and enterprise auth — relevant infrastructure context but custom non-SPDX license limits adoption
- [OpenClaw](entries/openclaw.md) — rejected — ecosystem signal for agentic workspaces; not a concrete kb comparison
- [OpenRouter](entries/openrouter.md) — open — Unified LLM API gateway supporting 200+ models — useful as infrastructure reference, not directly needed when using Claude natively.
- [OpenSpace](entries/openspace.md) — open — Compelling skill-evolution engine for Claude Code agents but very new (v0.1.0), self-published benchmark, and significant security surface from community skill ingestion
- [Overcut — Agentic SDLC Orchestration](entries/overcut.md) — open — Commercial orchestration layer for multi-agent SDLC; addresses real coordination gap but closed-source, early-stage, and not yet individually usable
- [Paperless-ngx](entries/paperless-ngx.md) — open — Mature self-hosted document management system — useful for archiving research docs but not an agent tool or developer library
- [Qwen3.6-27B](entries/qwen3-6-27b.md) — open — Strong open-weight 27B model with near-frontier coding scores and 262K context; promising local worker model but requires multi-GPU or quantization for practical use
- [Repowire](entries/repowire.md) — open — Compelling multi-agent mesh for cross-repo coordination, but macOS/Linux only and default spawn config ships dangerous permission flags
- [RuView WiFi Sensing Platform](entries/ruview-wifi-sensing.md) — open — Interesting hardware+agent integration with a Claude Code plugin and MCP server, but beta software requiring physical ESP32 hardware for core capabilities
- [SkillOpt](entries/skillopt.md) — open — Microsoft research framework that optimizes agent skills via training loops; +23.5 point lifts on Claude Code, Sleep mode for nightly skill consolidation is directly relevant
- [Spiderbrain V3](entries/spiderbrain-v3.md) — rejected — BSL license; master/column concept is the key takeaway for kb graph
- [Storybloq](entries/storybloq.md) — rejected — PolyForm Noncommercial license + heavy overlap with kb wiki
- [Third Brain V5 (Wiki/Knowledge Layer)](entries/third-brain-v5-wiki.md) — rejected — Obsidian-specific schema, heavy; staleness and contradiction detection concepts worth noting for kb
- [Tolvi — Engineering Decision Vault](entries/tolvi.md) — open — Solid CAG/RAG dual-mode decision-capture design but pre-1.0, small project, and overlaps with kb already in use
- [Vaultwarden](entries/vaultwarden.md) — adopted — Production-grade self-hosted Bitwarden-compatible password server in Rust; fraction of the resource footprint of the official server
- [Weft](entries/weft-language.md) — open — Novel AI orchestration language with typed nodes, durable execution, and human-in-the-loop primitives — early-stage but architecturally interesting

### mcp-server

- [Claude Peers MCP](entries/claude-peers-mcp.md) — open — Novel multi-session peer messaging, but mandatory --dangerously-skip-permissions flag is a hard blocker for safe use
- [n8n MCP Server](entries/n8n-mcp.md) — open — powerful workflow automation bridge but heavy dependency; evaluate when pipeline orchestration needs outgrow kb dispatch
- [Synthesize Bio](entries/synthesize-bio.md) — open — Generates synthetic human gene expression profiles on demand via natural-language prompts — unique bioinformatics capability, but proprietary SaaS requiring account and external API trust.

### meta-skill

- [One Skill to Rule Them All](entries/one-skill-to-rule-them-all.md) — open — proposes NEW skills from observed patterns; complementary to superpowers routing
- [Skill Router](entries/skill-router.md) — rejected — superpowers using-superpowers already handles skill routing

### plugin

- [Everything Claude Code (ECC)](entries/ecc-plugin.md) — open — rate-limited (429 errors); trial when accessible
- [FluidDocs Deck Builder](entries/fluiddocs-deck-builder.md) — open — Well-built skill/plugin pack for HTML slide decks; interesting multi-reviewer architecture but outside bioinformatics workflows
- [Frontier](entries/frontier.md) — open — Well-architected multi-harness orchestration runtime for Claude Code; early preview but the token-economics argument and delegation model are sound
- [Headroom Desktop](entries/headroom-desktop.md) — open — Solid local-first Claude Code cost optimizer with hook injection into ~/.claude/settings.json — worth monitoring given agent-lockdown relevance, but macOS-only stable and single-contributor
- [opencode-fff-search](entries/opencode-fff-search.md) — open — Drop-in OpenCode grep/glob replacement with Rust-backed in-memory index, frecency ranking, and SIMD literal matching — 3-10x faster than process-spawning ripgrep at scale.
- [Ponytail](entries/ponytail.md) — open — YAGNI enforcement plugin with strong benchmarks (80-94% less code, 47-77% cheaper); multi-platform support and clean design make it worth trialing
- [Understand Anything](entries/understand-anything.md) — open — Interactive knowledge graph plugin for codebases with multi-agent pipeline and broad platform support; impressive but heavy — watch for maturity and real-world performance on large repos

### reference

- [AI Memory Comparison](entries/ai-memory-comparison.md) — adopted — Definitive source-backed survey of 73 open-source AI agent memory systems across 79 features — every claim cites public code or docs.
- [AI Needs What ALCOA+ Gave Records](entries/alcoa-plus-for-ai.md) — open — Useful framing for regulated-AI governance but no actionable tool or framework yet — CASTEM teased but unpublished
- [Awesome Claude Code](entries/awesome-claude-code.md) — open — curated Claude Code ecosystem list; use as discovery source for future catalog inbox items
- [BioMysteryBench](entries/biomysterybench.md) — open — 99-problem bioinformatics research benchmark from Anthropic — directly useful for evaluating agent performance on real research tasks.
- [CASTEM: First Principles for Model-Mediated Work](entries/castem-first-principles-model-mediated-work.md) — open — Portable 6-criterion mnemonic (Credible, Auditable, Supervised, Traceable, Explainable, Monitored) for AI governance in regulated settings — good design checklist, no tooling.
- [CL4R1T4S](entries/cl4r1t4s.md) — open — Collection of leaked AI system prompts; useful security-awareness reference but README contains embedded prompt injection
- [Claude Code Remote Prompt Hardening](entries/claude-code-remote-prompt-hardening.md) — open — env vars to block remote system prompt injection in Claude Code; operational hardening knowledge for security-sensitive environments
- [Claude Decision Pressure-Test & Context Handoff Prompts](entries/claude-decision-pressure-test-and-context-handoff.md) — open — Two reusable prompting patterns — steelman/red-team verdict loop and structured context handoff — worth keeping as copy-paste references
- [Claude Howto](entries/claude-howto.md) — open — Well-structured tutorial guide with copy-paste templates, but it is a learning reference rather than an installable tool.
- [Claude Meta-Skill](entries/claude-meta-skill.md) — open — Curated collection of 11 Claude Code skills; mostly Chinese-language or general-dev focused, with significant overlap to existing catalog entries
- [Claude Spellbook](entries/claude-spellbook.md) — open — 50 skills, 7 agents, 11 slash commands — use as pattern reference, not default install
- [Codebase Reasoning Topology](entries/codebase-reasoning-topology.md) — open — heavy for daily use but interesting as a pre-flight checklist concept
- [Codex Memory Cleanup](entries/codex-memory-cleanup.md) — open — operational tip: delete state/log/global-state files if Codex performance degrades
- [Deny .env Reads via Permissions](entries/deny-env-reads.md) — open — Useful security hygiene tip for Claude Code projects; documents a built-in feature rather than a new tool
- [GraphRAG & Agent Memory LinkedIn Series](entries/graphrag-agent-memory-linkedin-series.md) — open — Six-post series covering GraphRAG design, ontology modeling, and unified agent memory architecture — useful conceptual grounding for KG-backed agents.
- [Karpathy's 12 Rules for CLAUDE.md](entries/karpathy-12-rules.md) — adopted — Rules 6 (token budgets) and 12 (fail loud) not yet in our stack
- [Karpathy's LLM Wiki Pattern](entries/karpathy-llm-wiki.md) — adopted — Foundational pattern doc for LLM-maintained personal knowledge bases — directly describes the architecture kb-wiki implements
- [Model Workspace Protocol (MWP)](entries/model-workspace-protocol.md) — open — Research paper proposing filesystem structure as agent orchestration; numbered folders + markdown prompts replace multi-agent frameworks for sequential workflows
- [Open Knowledge Format (OKF)](entries/open-knowledge-format.md) — open — Google's draft spec for agent-friendly knowledge representation using Markdown + YAML frontmatter; closely aligned with our wiki pattern but v0.1 draft status
- [Pi-hole](entries/pi-hole.md) — open — Network-wide DNS ad blocker — mature infrastructure tool, informational for lab network hygiene
- [Remote Control](entries/remote-control.md) — open — built-in feature; try for long sessions
- [TeamPCP/Miasma npm Supply Chain Attack (June 2026)](entries/teampcp-miasma-npm-supply-chain-attack-2026.md) — open — Incident writeup documenting credential-harvesting malware and ~/.claude/settings.json hook persistence — directly relevant to agent-lockdown hardening (WK-0031)
- [TurboQuant — Extreme KV Cache Compression](entries/turboquant.md) — open — Foundational Google Research algorithm (ICLR 2026) for 3-4 bit KV cache compression with zero accuracy loss; growing downstream ecosystem but no single canonical package yet
- [Verify Before Claim (Third Brain V5)](entries/verify-before-claim.md) — open — superpowers verification-before-completion covers this; confidence model is the novel addition
- [Zero to Mastery ML](entries/zero-to-mastery-ml.md) — open — Comprehensive ML/DS course materials (NumPy, pandas, sklearn, TensorFlow); useful learning reference but not a tool or workflow component

### skill

- [ADHD](entries/adhd.md) — open — parallel divergent ideation via isolated cognitive frames; overlaps with superpowers:brainstorming but the frame isolation and scoring mechanics are worth studying
- [Advise Project Approach](entries/advise-project-approach.md) — open — structured project-level architecture research with comparable analysis, cost checks, and tradeoff discipline; complements /catalog (tool-level) with project-level advisory
- [Agent Session Resume](entries/agent-session-resume.md) — open — Cross-agent session resume skill with structured checkpoint workflow; overlaps with our handoff skill but adds multi-agent-platform support (Codex, Cursor, Antigravity, OpenCode)
- [Book to Skill](entries/book-to-skill.md) — open — directly useful for computational biology methods PDFs
- [Context Graph Compressor](entries/context-graph-compressor.md) — open — Structured JSON graph handoff with importance tagging and cross-LLM portability beats plain-text handoff skills; too new/single-contributor to adopt outright
- [Grill With Docs](entries/grill-with-docs.md) — open — Well-structured DDD design-review skill that enforces domain language, but relies on companion format files (CONTEXT-FORMAT.md, ADR-FORMAT.md) not bundled with the skill.
- [Obsidian Skills (Kepano)](entries/obsidian-skills.md) — open — Obsidian-specific; Defuddle (web→clean markdown) and skill packaging patterns worth noting
- [PII Detection / Compliance Skills](entries/pii-detection.md) — open — HIPAA/CCPA/PCI-DSS coverage; pilot if handling sensitive data
- [sota-scan](entries/sota-scan.md) — open — Useful comparative benchmarking skill for Claude Code, but single-contributor, no tests, and high token cost for exhaustive mode
- [Superpowers: Verification Before Completion](entries/superpowers-verification-before-completion.md) — adopted — canonical 'evidence before claims' gate skill — already active in this project and referenced by other catalog entries as the standard
- [Tutorial Creator](entries/tutorial-creator.md) — open — good for knowledge retention and onboarding
- [UI/UX Pro Max Skill](entries/ui-ux-pro-max-skill.md) — open — comprehensive design system generation but focused on general web/mobile UI; evaluate when dashboard/report aesthetics become a priority
- [Unforget](entries/unforget.md) — rejected — scan-for-escaped-items pattern worth noting for future kb lint rule or audit command
- [Web Artifacts Builder](entries/web-artifacts-builder.md) — adopted — use when markdown isn't enough for interactive reports/dashboards

### skill-generator

- [BMAD Skill Forge](entries/bmad-skill-forge.md) — open — strong fit for bioinformatics tool skill generation; start with Brief tier on samtools
- [Creating CLAUDE.md](entries/creating-claude-md.md) — rejected — /init skill already covers repo-scanning CLAUDE.md generation
