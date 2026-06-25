---
name: agent-skills-spec
title: Agent Skills Open Standard (agentskills.io)
url: "https://agentskills.io/home"
category: reference
summary: "Anthropic's open SKILL.md specification for packaging agent capabilities — adopted by 32+ tools (Claude Code, Codex, Cursor, Gemini CLI, Kiro, Junie, Goose); progressive-disclosure format (name/description → full instructions → scripts/assets); 100K+ stars on anthropics/skills; the cross-vendor standard our skills are built on"
tags: [specification, open-standard, skill-format, anthropic, interoperability]
workflows: []
reviewed: 2026-06-25
acquired: 2026-06-25
license: MIT
security_flags: []
supersedes: []
overlaps: []
---

## What it says

The Agent Skills specification defines a universal format for packaging procedural knowledge for AI coding agents. A skill is a folder containing a required SKILL.md file (YAML frontmatter with `name` and `description`, plus Markdown instructions) and optional subdirectories for scripts, references, assets, and other resources.

Agents interact with skills through progressive disclosure: (1) Discovery — load only name/description at startup for low context cost, (2) Activation — read full SKILL.md when a task matches, (3) Execution — follow instructions, optionally running bundled code or loading referenced files. This keeps many skills available without consuming context.

Released by Anthropic on December 18, 2025 as an open standard. Within 48 hours, Microsoft (VS Code) and OpenAI (ChatGPT, Codex CLI) integrated it. By March 2026, 32 tools adopted it including Google Gemini CLI, JetBrains Junie, AWS Kiro, Block Goose, Sourcegraph Amp, Snowflake, Databricks, ByteDance, Mistral AI, and Spring AI. Vercel's skills.sh marketplace lists 89K+ skills.

## Assessment

This is the foundational specification our own skills are built on. Understanding the spec is essential for skill authorship and for evaluating third-party skills. The progressive disclosure model (metadata-first, instructions-on-demand) is the key design decision that makes large skill libraries practical — it's why an agent can have 100+ skills registered without blowing the context window.

The spec follows the same playbook as MCP: solve a real interoperability problem, release as an open standard, let adoption create ecosystem value. The 32-tool adoption in 3 months is the fastest cross-vendor standardization event in AI tooling.

Key academic work has followed: SkillTester (benchmarking skill utility and security), formal supply-chain analysis for skill packages, EvoSkills (self-evolving skills via co-evolutionary verification), and the Knowledge Activation paper framing skills as institutional knowledge primitives.

## Mechanical details

- Spec site: agentskills.io
- GitHub: anthropics/skills (100K+ stars)
- Marketplace: skills.sh (Vercel, 89K+ skills)
- Minimum skill: a folder with SKILL.md containing `name:` and `description:` in YAML frontmatter
- Our skills directory (`skills/`) follows this format exactly

## Security

The spec itself is clean. Supply-chain concerns exist at the ecosystem level — third-party skills can bundle executable scripts, and marketplace discovery doesn't currently enforce signing or provenance. The SkillTester and formal supply-chain papers address this gap academically but no universal mitigation exists in the spec yet.