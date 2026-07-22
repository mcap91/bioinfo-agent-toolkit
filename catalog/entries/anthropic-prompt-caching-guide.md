---
name: anthropic-prompt-caching-guide
title: "Anthropic Prompt Caching Design & Optimization Guide"
url: "https://github.com/anthropics/skills/blob/main/skills/claude-api/shared/prompt-caching.md"
category: reference
tags: [prompt-caching, anthropic-api, optimization, cost-reduction, claude-api-skill, official]
reviewed: 2026-07-21
summary: ">-"
acquired: 2026-07-22
---

## What it covers

The official Anthropic reference for designing prompt-building code that
maximizes cache hit rates. Part of the `anthropics/skills` repository,
used by the bundled `claude-api` skill.

### Core invariant

Prompt caching is a prefix match. Any change anywhere in the prefix
invalidates everything after it. The cache key is derived from exact bytes
up to each `cache_control` breakpoint. Render order is:
tools → system → messages.

### Placement patterns

- **Large system prompt**: breakpoint on last system text block (caches
  tools + system together)
- **Multi-turn conversations**: breakpoint on last content block of the
  most recently appended turn; earlier breakpoints remain valid read points
- **Shared prefix, varying suffix**: breakpoint at end of shared portion,
  not end of whole prompt
- **Mid-conversation system messages** (Opus 4.8+): use `role: "system"`
  in messages array rather than editing top-level system, to preserve
  cached prefix

### Silent invalidators

`datetime.now()` in system prompt, `uuid4()` early in content, non-
deterministic JSON serialization, user-ID interpolation in system prompt,
conditional system sections, per-user tool sets.

### Key technical details

- Max 4 breakpoints per request
- Minimum cacheable prefix varies by model: 4096 tokens (Opus 4.8/4.7/4.6,
  Haiku 4.5), 2048 (Fable 5, Sonnet 4.6), 1024 (Sonnet 4.5/4.1/4)
- 20-block lookback window per breakpoint — long agentic turns with many
  tool_use/tool_result pairs can exceed this
- Concurrent requests all pay full price — send 1, await first streamed
  token, then fire remaining N-1
- Pre-warming with `max_tokens: 0` eliminates first-request latency
- Cache reads: 0.1x base price; 5-min writes: 1.25x; 1-hour writes: 2x

## Usage notes

- Companion Jupyter notebook with runnable examples: https://github.com/anthropics/claude-cookbooks/blob/main/misc/prompt_caching.ipynb
