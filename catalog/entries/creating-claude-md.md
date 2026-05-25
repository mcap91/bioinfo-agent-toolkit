---
name: creating-claude-md
title: "Creating CLAUDE.md"
url: https://github.com/sruthik27/creating-claude-md
category: skill-generator
verdict: skip
verdict_reason: "/init skill already covers repo-scanning CLAUDE.md generation"
tags: [claude-md, repo-scanning, code-quality]
reviewed: 2026-05-25
supersedes: []
---

## What it does

Scans a repo (manifests, linters, git history), then asks 6 targeted questions — gotchas, scope, approvals, testing, external docs, and reasoning preferences — before generating a CLAUDE.md. Enforces a hard cap at 80 lines with overflow to `agent_docs/`. Refuses to include rules that duplicate linter config, personality prompts, or pasted documentation. The 80-line philosophy reflects a real maintenance insight: CLAUDE.md files that grow without discipline become noise.

## Why this verdict

The `/init` skill already performs repo-scanning CLAUDE.md generation and is installed in this stack. There is no capability gap. The 80-line cap philosophy is worth keeping as a maintenance guideline for our own CLAUDE.md, but the tool itself adds no workflow value beyond what init provides.

## Mechanical details

No additional install needed — the `/init` skill covers this use case. If the 80-line cap discipline is wanted as a standalone rule, add it as a comment or constraint in the project CLAUDE.md rather than adopting this generator.
