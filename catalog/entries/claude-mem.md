---
name: claude-mem
title: "Claude Mem"
url: https://github.com/thedotmack/claude-mem
category: framework
verdict: skip
verdict_reason: "kb wiki + Claude Code built-in memory cover our needs; adds SQLite + Chroma + worker complexity without clear benefit"
tags: [memory, persistence, vector-search, sessions, hooks, kb]
workflows: []
reviewed: 2026-05-25
supersedes: []
---

## What it does

A persistent memory system for AI agents using SQLite + Chroma vector DB. Automatically captures observations via 5 lifecycle hooks (SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd), generates semantic summaries, and provides 3-layer progressive disclosure retrieval (search→timeline→full details) to minimize token usage. Runs a worker service on port 37777 with HTTP API and web UI. Provides 4 MCP tools for intelligent memory search. Supports privacy controls via `<private>` tags. 78.1k stars, Apache 2.0, requires Node 18+, Bun, and uv.

## Why this verdict

We already have two memory layers that cover this space: Claude Code's built-in auto-memory (file-based, per-project, with structured types) and kb wiki (persistent typed records with relationships, search index, and graph). claude-mem's progressive disclosure and vector search are technically interesting, but add significant infrastructure (SQLite + Chroma + Bun + worker service + 5 hooks) for a problem we've already solved. Previously skipped gbrain and Third Brain V5 for similar reasons. The 3-layer retrieval pattern (index→context→full) is a good concept already reflected in our wiki search approach.

## Mechanical details

- Install: `npx claude-mem install`
- Requires: Node 18+, Bun (auto-installed), uv (auto-installed), SQLite 3
- Config: `~/.claude-mem/settings.json` (auto-created)
- Worker: runs on port 37777, provides HTTP API + web UI
- Hooks: 5 lifecycle hooks auto-capture session activity
- Storage: SQLite for observations, Chroma for vector/semantic search
