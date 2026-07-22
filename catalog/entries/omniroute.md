---
name: omniroute
title: OmniRoute
url: "https://github.com/diegosouzapw/OmniRoute"
category: framework
tags: [ai-gateway, llm-router, openai-compatible, multi-provider, token-compression, mcp-server, a2a, failover, routing, cost-optimization, proxy]
reviewed: 2026-07-21
summary: ">-"
security_flags: [transparent MITM/TPROXY capture of CLI traffic that ignores proxy env vars, TLS fingerprint stealth (JA3/JA4 spoofing via wreq-js) to evade provider detection, loopback-only restriction on process-spawning routes]
acquired: 2026-07-22
---

## What it does

OmniRoute is a self-hosted AI gateway that sits between coding tools and LLM
providers. It exposes a single OpenAI-compatible endpoint
(`http://localhost:20128/v1`) and routes requests across a catalog of 271+
providers, 90+ of which have free tiers (40+ free forever).

### Routing

The system provides 18 routing strategies: priority, fill-first, weighted,
round-robin, power-of-two-choices, least-used, random, cost-optimized,
headroom, reset-window, context-relay, context-optimized, LKGP
(last-known-good-path), auto (12-factor live scoring), fusion (fan-out to
panel + judge synthesis), and pipeline (chained stages).

"Combos" chain models across providers — when quota runs out, a provider
fails, or costs spike, the combo silently falls back to the next model.
Zero-config `auto` variants (`auto/coding`, `auto/fast`, `auto/cheap`,
`auto/smart`) build virtual combos scored live.

### Token compression

An 11-engine composable pipeline runs transparently on every request:
Session-Dedup, CCR (archive behind retrieve markers), RTK (tool-result
filtering), Headroom (tabular compaction via GCF codec), Relevance
(extractive scoring), Caveman (rule-based prose compression), LLMLingua-2
(ML semantic pruning via MobileBERT ONNX), Lite (whitespace trimming),
Aggressive (summarization + aging), and Ultra (heuristic token pruning).
Presets range from Lite (~15%) to Stacked RTK→Caveman (78–95%).

### Quota-Share

Distributes a provider's time-based quota across multiple keys in a pool
using DRR scheduling, with per-connection concurrency, multi-window buckets,
and session stickiness for prompt-cache integrity.

### Protocols

- MCP server: 104 tools across stdio, HTTP stream, and SSE transports
- A2A agent protocol: 6 skills, JSON-RPC 2.0 + SSE
- Full CLI with 80+ commands, interactive TUI chat, setup wizard, diagnostics

### Platforms

Runs via npm (global), Docker (multi-arch), Electron desktop app, Termux
(Android), PWA, Nix flake, Podman, and from source. Remote mode supports
driving a VPS instance from a local CLI via scoped access tokens.

## Lineage

Started as a fork of 9router (~22.7k stars) and a TypeScript port of the Go
project CLIProxyAPI (~43.6k stars). Acknowledges LiteLLM, Caveman (~90.8k
stars), RTK (~71.8k stars), headroom (~60.1k stars), and others as
inspirations for specific subsystems.
