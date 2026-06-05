---
name: get-shit-done
title: "Get Shit Done (GSD)"
url: https://github.com/glittercowboy/get-shit-done
category: framework
verdict: skip
verdict_reason: "deprecated (moved to GSD Redux); superpowers skill system already covers meta-prompting and spec-driven development"
tags: [meta-prompting, context-engineering, spec-driven, claude-md, workflow, kb]
workflows: []
reviewed: 2026-05-25
acquired: 2026-05-25
supersedes: []
overlaps: [claude-spellbook]
---

## What it does

A meta-prompting, context engineering, and spec-driven development system for Claude Code. Provides structured frameworks for organizing developer-AI interactions — agents, commands, hooks, SDKs, and documentation patterns. JavaScript/TypeScript codebase with 2,922 commits and 78 releases. Had 63.7k stars. **Deprecated**: development moved to "GSD Redux" at open-gsd/get-shit-done-redux.

## Why this verdict

Two reasons to skip: (1) The project is deprecated and no longer maintained at this URL — active development is at a different repository (GSD Redux). (2) Our superpowers skill system already covers the same problem space: brainstorming, writing-plans, executing-plans, subagent-driven-development, verification-before-completion, TDD, systematic-debugging, and dispatching-parallel-agents collectively address meta-prompting, context engineering, and spec-driven development. The superpowers approach is more modular (individual skills triggered contextually) vs. GSD's monolithic framework.

## Mechanical details

- Original repo: github.com/glittercowboy/get-shit-done (deprecated)
- Active fork: github.com/open-gsd/get-shit-done-redux
- JS 73.1%, TS 26.5%, Shell 0.4%
- Not worth tracking the Redux version separately unless it introduces novel patterns beyond our superpowers coverage
