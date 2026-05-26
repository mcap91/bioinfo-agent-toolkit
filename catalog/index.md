# Catalog Index

Generated from 35 entries in `catalog/entries/`. Regenerate with `/catalog index`.

## By Verdict

| Item | Category | Verdict | Reason | Tags |
|---|---|---|---|---|
| [Claude Agent Teams](entries/agent-teams.md) | agent-pattern | adopt | primary interactive dispatch path; subscription billing, no API credits needed | agents, teams, dispatch, orchestration |
| [Karpathy's 12 Rules for CLAUDE.md](entries/karpathy-12-rules.md) | reference | adopt | Rules 6 (token budgets) and 12 (fail loud) not yet in our stack | claude-md, best-practices, token-budgets |
| [Claude Native Subagents](entries/native-subagents.md) | agent-pattern | adopt | lightweight HO consultation route within existing sessions; no separate billing | agents, subagents, dispatch, consultation |
| [Web Artifacts Builder](entries/web-artifacts-builder.md) | skill | adopt | use when markdown isn't enough for interactive reports/dashboards | html, reports, dashboards, visualization |
| [BMAD Skill Forge](entries/bmad-skill-forge.md) | skill-generator | pilot | strong fit for bioinformatics tool skill generation; start with Brief tier on samtools | skill-generation, provenance, ast, cli-tools |
| [Book to Skill](entries/book-to-skill.md) | skill | pilot | directly useful for computational biology methods PDFs | pdf, knowledge, querying |
| [One Skill to Rule Them All](entries/one-skill-to-rule-them-all.md) | meta-skill | pilot | proposes NEW skills from observed patterns; complementary to superpowers routing | meta-skill, pattern-detection, skill-generation |
| [PII Detection / Compliance Skills](entries/pii-detection.md) | skill | pilot | HIPAA/CCPA/PCI-DSS coverage; pilot if handling sensitive data | pii, compliance, hipaa, ccpa, security |
| [Tutorial Creator](entries/tutorial-creator.md) | skill | pilot | good for knowledge retention and onboarding | tutorials, onboarding, knowledge-retention |
| [Autoharness](entries/autoharness.md) | framework | watch | needs eval benchmarks first; pilot when we have eval criteria for our skills/agents | harness, optimization, eval, benchmarks |
| [Everything Claude Code (ECC)](entries/ecc-plugin.md) | plugin | watch | rate-limited (429 errors); trial when accessible | plugin, hub, all-in-one |
| [n8n MCP Server](entries/n8n-mcp.md) | mcp-server | watch | powerful workflow automation bridge but heavy dependency; evaluate when pipeline orchestration needs outgrow kb dispatch | mcp, n8n, workflow-automation, orchestration, integrations |
| [UI/UX Pro Max Skill](entries/ui-ux-pro-max-skill.md) | skill | watch | comprehensive design system generation but focused on general web/mobile UI; evaluate when dashboard aesthetics become a priority | ui, ux, design-system, typography, color-palettes, dashboards, visualization |
| [Advisor Strategy](entries/advisor-strategy.md) | agent-pattern | note | architectural concept for cost-effective agent orchestration; executor/advisor split | agents, cost-optimization, dispatch, patterns |
| [Awesome Claude Code](entries/awesome-claude-code.md) | reference | note | curated Claude Code ecosystem list; use as discovery source for future catalog inbox items | awesome-list, skills, agents, hooks, orchestrators, discovery |
| [Claude Spellbook](entries/claude-spellbook.md) | reference | note | 50 skills, 7 agents, 11 slash commands — use as pattern reference, not default install | skills, agents, hooks, patterns |
| [Codebase Reasoning Topology](entries/codebase-reasoning-topology.md) | reference | note | heavy for daily use but interesting as a pre-flight checklist concept | invariants, state-ownership, blast-radius, checklist |
| [Codex Memory Cleanup](entries/codex-memory-cleanup.md) | reference | note | operational tip: delete state/log/global-state files if Codex performance degrades | codex, maintenance, performance |
| [Graphify](entries/graphify.md) | framework | note | direct inspiration for kb graph; concepts like confidence-tagged edges and clustering worth learning from | knowledge-graph, ast, visualization, kb |
| [Obsidian Skills (Kepano)](entries/obsidian-skills.md) | skill | note | Obsidian-specific; Defuddle (web→clean markdown) and skill packaging patterns worth noting | obsidian, skills, markdown, canvas, defuddle, web-extraction |
| [Remote Control](entries/remote-control.md) | reference | note | built-in feature; try for long sessions | mobile, remote, sessions |
| [Verify Before Claim (Third Brain V5)](entries/verify-before-claim.md) | reference | note | superpowers verification-before-completion covers this; confidence model is the novel addition | verification, quality, confidence-model |
| [claude-pee](entries/claude-pee.md) | cli-tool | skip | PTY wrapper driving interactive CLI; inherently brittle, breaks on CLI version changes | pty, automation, cli, dispatch |
| [Claude Mem](entries/claude-mem.md) | framework | skip | kb wiki + Claude Code built-in memory cover our needs; adds SQLite + Chroma + worker complexity without clear benefit | memory, persistence, vector-search, sessions, hooks, kb |
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
- [Web Artifacts Builder](entries/web-artifacts-builder.md) — adopt — use when markdown isn't enough for interactive reports/dashboards

### General

- [Advisor Strategy](entries/advisor-strategy.md) — note — architectural concept for cost-effective agent orchestration; executor/advisor split
- [Autoharness](entries/autoharness.md) — watch — needs eval benchmarks first; pilot when we have eval criteria for our skills/agents
- [Awesome Claude Code](entries/awesome-claude-code.md) — note �� curated Claude Code ecosystem list; use as discovery source for future catalog inbox items
- [Claude Agent Teams](entries/agent-teams.md) — adopt — primary interactive dispatch path; subscription billing, no API credits needed
- [Claude Mem](entries/claude-mem.md) ��� skip — kb wiki + Claude Code built-in memory cover our needs; adds SQLite + Chroma + worker complexity without clear benefit
- [Claude Native Subagents](entries/native-subagents.md) — adopt ��� lightweight HO consultation route within existing sessions; no separate billing
- [Claude Spellbook](entries/claude-spellbook.md) — note — 50 skills, 7 agents, 11 slash commands — use as pattern reference, not default install
- [claude-pee](entries/claude-pee.md) — skip �� PTY wrapper driving interactive CLI; inherently brittle, breaks on CLI version changes
- [Codebase Reasoning Topology](entries/codebase-reasoning-topology.md) — note — heavy for daily use but interesting as a pre-flight checklist concept
- [Codex Memory Cleanup](entries/codex-memory-cleanup.md) — note — operational tip: delete state/log/global-state files if Codex performance degrades
- [Creating CLAUDE.md](entries/creating-claude-md.md) — skip — /init skill already covers repo-scanning CLAUDE.md generation
- [Everything Claude Code (ECC)](entries/ecc-plugin.md) — watch — rate-limited (429 errors); trial when accessible
- [gbrain](entries/gbrain.md) — skip — kb wiki already provides persistent typed records with relationships and search
- [Get Shit Done (GSD)](entries/get-shit-done.md) — skip — deprecated (moved to GSD Redux); superpowers skill system already covers meta-prompting and spec-driven development
- [Graphify](entries/graphify.md) — note — direct inspiration for kb graph; concepts like confidence-tagged edges and clustering worth learning from
- [gstack](entries/gstack.md) — skip — kb dispatch covers the relevant orchestration patterns; browser/deployment out of scope
- [Karpathy's 12 Rules for CLAUDE.md](entries/karpathy-12-rules.md) — adopt — Rules 6 (token budgets) and 12 (fail loud) not yet in our stack
- [n8n MCP Server](entries/n8n-mcp.md) — watch — powerful workflow automation bridge but heavy dependency; evaluate when pipeline orchestration needs outgrow kb dispatch
- [oauth-cli-coder](entries/oauth-cli-coder.md) — skip ��� OAuth-based CLI automation; adds auth complexity without solving durability
- [Obsidian Skills (Kepano)](entries/obsidian-skills.md) — note — Obsidian-specific; Defuddle (web→clean markdown) and skill packaging patterns worth noting
- [One Skill to Rule Them All](entries/one-skill-to-rule-them-all.md) — pilot — proposes NEW skills from observed patterns; complementary to superpowers routing
- [OpenClaw](entries/openclaw.md) — skip �� ecosystem signal for agentic workspaces; not a concrete kb comparison
- [PII Detection / Compliance Skills](entries/pii-detection.md) — pilot — HIPAA/CCPA/PCI-DSS coverage; pilot if handling sensitive data
- [Remote Control](entries/remote-control.md) — note — built-in feature; try for long sessions
- [Skill Router](entries/skill-router.md) — skip — superpowers using-superpowers already handles skill routing
- [Spiderbrain V3](entries/spiderbrain-v3.md) — skip — BSL license; master/column concept is the key takeaway for kb graph
- [Storybloq](entries/storybloq.md) — skip — PolyForm Noncommercial license + heavy overlap with kb wiki
- [Third Brain V5 (Wiki/Knowledge Layer)](entries/third-brain-v5-wiki.md) — skip — Obsidian-specific schema, heavy; staleness and contradiction detection concepts worth noting for kb
- [Tutorial Creator](entries/tutorial-creator.md) — pilot — good for knowledge retention and onboarding
- [UI/UX Pro Max Skill](entries/ui-ux-pro-max-skill.md) — watch — comprehensive design system generation but focused on general web/mobile UI; evaluate when dashboard aesthetics become a priority
- [Unforget](entries/unforget.md) — skip — scan-for-escaped-items pattern worth noting for future kb lint rule or audit command
- [Verify Before Claim (Third Brain V5)](entries/verify-before-claim.md) — note — superpowers verification-before-completion covers this; confidence model is the novel addition

## By Category

### agent-pattern

- [Advisor Strategy](entries/advisor-strategy.md) — note — architectural concept for cost-effective agent orchestration; executor/advisor split
- [Claude Agent Teams](entries/agent-teams.md) — adopt — primary interactive dispatch path; subscription billing, no API credits needed
- [Claude Native Subagents](entries/native-subagents.md) — adopt — lightweight HO consultation route within existing sessions; no separate billing

### cli-tool

- [claude-pee](entries/claude-pee.md) — skip ��� PTY wrapper driving interactive CLI; inherently brittle, breaks on CLI version changes
- [oauth-cli-coder](entries/oauth-cli-coder.md) — skip — OAuth-based CLI automation; adds auth complexity without solving durability

### framework

- [Autoharness](entries/autoharness.md) — watch — needs eval benchmarks first; pilot when we have eval criteria for our skills/agents
- [Claude Mem](entries/claude-mem.md) — skip — kb wiki + Claude Code built-in memory cover our needs; adds SQLite + Chroma + worker complexity without clear benefit
- [gbrain](entries/gbrain.md) — skip — kb wiki already provides persistent typed records with relationships and search
- [Get Shit Done (GSD)](entries/get-shit-done.md) — skip — deprecated (moved to GSD Redux); superpowers skill system already covers meta-prompting and spec-driven development
- [Graphify](entries/graphify.md) — note — direct inspiration for kb graph; concepts like confidence-tagged edges and clustering worth learning from
- [gstack](entries/gstack.md) — skip — kb dispatch covers the relevant orchestration patterns; browser/deployment out of scope
- [OpenClaw](entries/openclaw.md) — skip — ecosystem signal for agentic workspaces; not a concrete kb comparison
- [Spiderbrain V3](entries/spiderbrain-v3.md) — skip — BSL license; master/column concept is the key takeaway for kb graph
- [Storybloq](entries/storybloq.md) — skip — PolyForm Noncommercial license + heavy overlap with kb wiki
- [Third Brain V5 (Wiki/Knowledge Layer)](entries/third-brain-v5-wiki.md) — skip — Obsidian-specific schema, heavy; staleness and contradiction detection concepts worth noting for kb

### mcp-server

- [n8n MCP Server](entries/n8n-mcp.md) — watch — powerful workflow automation bridge but heavy dependency; evaluate when pipeline orchestration needs outgrow kb dispatch

### meta-skill

- [One Skill to Rule Them All](entries/one-skill-to-rule-them-all.md) — pilot — proposes NEW skills from observed patterns; complementary to superpowers routing
- [Skill Router](entries/skill-router.md) — skip — superpowers using-superpowers already handles skill routing

### plugin

- [Everything Claude Code (ECC)](entries/ecc-plugin.md) — watch ��� rate-limited (429 errors); trial when accessible

### reference

- [Awesome Claude Code](entries/awesome-claude-code.md) — note — curated Claude Code ecosystem list; use as discovery source for future catalog inbox items
- [Claude Spellbook](entries/claude-spellbook.md) — note ��� 50 skills, 7 agents, 11 slash commands — use as pattern reference, not default install
- [Codebase Reasoning Topology](entries/codebase-reasoning-topology.md) — note — heavy for daily use but interesting as a pre-flight checklist concept
- [Codex Memory Cleanup](entries/codex-memory-cleanup.md) ��� note — operational tip: delete state/log/global-state files if Codex performance degrades
- [Karpathy's 12 Rules for CLAUDE.md](entries/karpathy-12-rules.md) — adopt — Rules 6 (token budgets) and 12 (fail loud) not yet in our stack
- [Remote Control](entries/remote-control.md) — note — built-in feature; try for long sessions
- [Verify Before Claim (Third Brain V5)](entries/verify-before-claim.md) — note — superpowers verification-before-completion covers this; confidence model is the novel addition

### skill

- [Book to Skill](entries/book-to-skill.md) — pilot — directly useful for computational biology methods PDFs
- [Obsidian Skills (Kepano)](entries/obsidian-skills.md) — note — Obsidian-specific; Defuddle (web→clean markdown) and skill packaging patterns worth noting
- [PII Detection / Compliance Skills](entries/pii-detection.md) — pilot — HIPAA/CCPA/PCI-DSS coverage; pilot if handling sensitive data
- [Tutorial Creator](entries/tutorial-creator.md) — pilot — good for knowledge retention and onboarding
- [UI/UX Pro Max Skill](entries/ui-ux-pro-max-skill.md) — watch — comprehensive design system generation but focused on general web/mobile UI; evaluate when dashboard aesthetics become a priority
- [Unforget](entries/unforget.md) — skip — scan-for-escaped-items pattern worth noting for future kb lint rule or audit command
- [Web Artifacts Builder](entries/web-artifacts-builder.md) — adopt — use when markdown isn't enough for interactive reports/dashboards

### skill-generator

- [BMAD Skill Forge](entries/bmad-skill-forge.md) — pilot — strong fit for bioinformatics tool skill generation; start with Brief tier on samtools
- [Creating CLAUDE.md](entries/creating-claude-md.md) ��� skip — /init skill already covers repo-scanning CLAUDE.md generation
