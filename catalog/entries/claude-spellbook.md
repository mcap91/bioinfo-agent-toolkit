---
name: claude-spellbook
title: "Claude Spellbook"
url: ""
category: reference
verdict: note
verdict_reason: "50 skills, 7 agents, 11 slash commands — use as pattern reference, not default install"
tags: [skills, agents, hooks, patterns]
reviewed: 2026-05-25
supersedes: []
---

## What it says

A bundled toolkit of 50 skills, 7 agents, and 11 slash commands with auto-formatting hooks. Provides a worked example of the "skill + agent + hook" integration pattern — showing how these three Claude Code primitives can be combined into a coherent operational system. Sourced from a Reddit r/claudeskills post.

## Why this verdict

Installing all 50 skills would create routing noise and override conflicts with the existing superpowers stack. The value is in the pattern library — how individual skills are structured, how agents are wired to skills, and how hooks trigger behavior automatically. Useful to browse when designing new integrations, not as a default install.

## What to adopt

Browse the repo when designing a new skill + agent + hook integration to see existing examples. Specific skills or hook patterns that solve a gap can be cherry-picked rather than adopting the full bundle. No bulk install.
