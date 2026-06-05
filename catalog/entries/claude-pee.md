---
name: claude-pee
title: "claude-pee"
category: cli-tool
verdict: skip
verdict_reason: "PTY wrapper driving interactive CLI; inherently brittle, breaks on CLI version changes"
tags: [pty, automation, cli, dispatch]
reviewed: 2026-05-25
acquired: 2026-05-25
supersedes: []
---

## What it does

`claude-pee` is a PTY wrapper that drives the Claude Code interactive CLI programmatically by injecting keystrokes and reading terminal output. It attempts to automate headless dispatch by treating the interactive terminal session as a subprocess target. Because it depends on the exact output format and interactive behavior of the CLI, it breaks whenever Claude Code updates its terminal UI.

## Why this verdict

PTY automation is inherently brittle: any CLI version change that alters prompt text, cursor behavior, or output formatting will silently break automation. It provides no durability guarantees and adds a fragile intermediary layer between dispatch and the model. The kb dispatch requirement is a durable, version-stable integration surface — PTY scraping is the opposite.

## Mechanical details

Not recommended for install. No stable package source identified. Rejected in WK-0003 research as a dispatch path.
