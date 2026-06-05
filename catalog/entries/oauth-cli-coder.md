---
name: oauth-cli-coder
title: "oauth-cli-coder"
category: cli-tool
verdict: skip
verdict_reason: "OAuth-based CLI automation; adds auth complexity without solving durability"
tags: [oauth, automation, cli, dispatch]
reviewed: 2026-05-25
acquired: 2026-05-25
supersedes: []
---

## What it does

`oauth-cli-coder` automates Claude Code CLI interactions using OAuth-based authentication rather than PTY key injection. It attempts to handle the interactive login and session flow programmatically so that the CLI can be driven in a headless or semi-automated context.

## Why this verdict

OAuth automation adds significant auth-layer complexity — token management, refresh logic, session state — without addressing the core durability problem of driving an interactive CLI. Dispatch needs a stable protocol surface (MCP or subprocess with defined I/O), not a workaround for the interactive login gate. Rejected in WK-0003 research alongside other TUI automation approaches.

## Mechanical details

Not recommended for install. No stable package source identified. Rejected in WK-0003 research as a dispatch path.
