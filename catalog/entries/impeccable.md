---
name: impeccable
title: Impeccable
url: "https://github.com/pbakaus/impeccable"
category: skill
tags: [design, frontend, UI, anti-patterns, linting, multi-CLI, skills]
reviewed: 2026-07-03
security_flags: []
summary: ">-"
acquired: 2026-07-04
---

## What It Does

Impeccable provides design vocabulary and quality enforcement for AI coding agents. It
catches common AI-generated frontend tells (Inter everywhere, purple gradients, nested
cards, gray text on colored backgrounds, bounce easing) through 45 deterministic detector
rules that run without an LLM. On top of that, 23 skill commands give agents a shared
design language for shaping, critiquing, and polishing UI work.

## Key Commands

- `/impeccable init` — setup flow that writes PRODUCT.md and DESIGN.md with brand context
- `/impeccable craft` — full shape-then-build flow with visual iteration
- `/impeccable audit` — technical quality checks (a11y, performance, responsive)
- `/impeccable critique` — UX design review (hierarchy, clarity, emotional resonance)
- `/impeccable polish` — final pass, design system alignment, shipping readiness
- `/impeccable bolder` / `quieter` / `distill` — intensity controls
- `/impeccable live` — visual variant mode with in-browser iteration
- `/impeccable pin <cmd>` — create standalone shortcut

## Design Hook

Installs provider-native hooks that run the detector on direct UI file edits. Claude Code
and Codex surface findings after edits; Cursor blocks bad writes before they land.

## Standalone CLI

```
npx impeccable detect src/           # scan a directory
npx impeccable detect --json .       # CI-friendly JSON output
npx impeccable detect https://...    # scan a URL via Puppeteer
```

## Supported Tools

Cursor, Claude Code, GitHub Copilot, Gemini CLI, Codex CLI, OpenCode, Pi, Kiro, Trae,
Rovo Dev, Qoder.

## Links

- GitHub: https://github.com/pbakaus/impeccable
- Site: https://impeccable.style