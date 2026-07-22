---
name: prompt-caching-mcp
title: Prompt Caching MCP
url: "https://github.com/flightlesstux/prompt-caching"
category: mcp-server
tags: [prompt-caching, anthropic-api, mcp, token-optimization, cost-reduction, claude-code-plugin]
reviewed: 2026-07-21
summary: ">-"
acquired: 2026-07-22
---

## What it does

An MCP server that helps developers building applications with the Anthropic
SDK optimize prompt caching. It automatically places `cache_control`
breakpoints on stable content blocks so cached reads cost 0.1x instead of
1x full input price.

### Target audience

Developers writing their own Anthropic API applications (Python scripts,
Node apps, AI agents). Claude Code already handles prompt caching for its
own sessions automatically — this plugin addresses the layer where custom
code calls the API directly.

### Tools

- **optimize_messages**: injects `cache_control` breakpoints into a messages
  array before Anthropic API calls; returns optimized array + change summary
- **get_cache_stats**: cumulative token savings for current session — hit
  rate, tokens saved, estimated cost reduction
- **reset_cache_stats**: reset session statistics
- **analyze_cacheability**: dry-run showing which segments would be cached
  and estimated savings without modifying anything

### Caching strategy

Identifies three types of stable content: system prompts (cached on first
turn, reused every subsequent turn), tool definitions (cached once per
session), and large user messages (cached when exceeding a configurable
token threshold). Break-even at turn 2; every turn after is pure savings.

### Benchmarks (measured against Anthropic API with Sonnet)

- Bug fix (20 turns): 85% savings
- Refactor 5 files (15 turns): 80% savings
- General coding (40 turns): 92% savings
- Repeated file reads (5x5): 90% savings

### Installation

Available as a Claude Code plugin (`/plugin marketplace add`) or via npm
(`npm install -g prompt-caching-mcp`) for Cursor, Windsurf, Zed,
Continue.dev, or any MCP client. Optional `.prompt-cache.json` config
for tuning thresholds.

## Usage notes

- Prompt caching is a critical optimization for AI coding agents — saves up to 90% in token costs and cuts latency in half by storing structural prompt prefixes (system rules, tool definitions, file trees) so they are not reprocessed on every turn. A single byte change can invalidate the entire cache downstream, which is why dedicated tools exist to stabilize, extend, and audit caching behavior.
