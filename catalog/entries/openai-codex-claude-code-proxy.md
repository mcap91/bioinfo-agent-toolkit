---
name: openai-codex-claude-code-proxy
title: OpenAI Codex Claude Code Proxy
url: "https://github.com/MikeChongCan/OpenAI-Codex-Claude-Code-Proxy"
category: framework
tags: [claude-code, proxy, openai, azure, gpt, cliproxyapi, model-routing, subagent]
reviewed: 2026-07-21
summary: ">-"
acquired: 2026-07-22
---

## What it does

Two shell launchers (`claudex-oai` for OpenAI/Codex OAuth, `claudex` for
Azure OpenAI) that start Claude Code with GPT-5.6 Sol as the main model,
routing through a local CLIProxyAPI instance that translates Anthropic
Messages API requests to the OpenAI Responses API.

### Architecture

```
Claude Code → localhost:8317 → CLIProxyAPI → Codex OAuth or Azure OpenAI
```

Azure and OpenAI subscription models use separate prefixed names
(`gpt-5.6-sol` vs `azure-gpt-5.6-sol`) to prevent cross-billing.

### Model mapping

- `opus` → Sol (main agent)
- `sonnet` → Terra (implementation/review subagents)
- `haiku` → Luna (fast exploration/simple checks)

The launcher appends a routing policy to the system prompt and disables
the bundled `claude-api` skill. Per-subagent tier selection is supported
via `model: sonnet` or `model: haiku` declarations, with a session-wide
override available via `CLAUDEX_SUBAGENT_MODEL`.

### Configuration

- Deferred tool loading (`ENABLE_TOOL_SEARCH=true`) to stay under Azure's
  128-tool limit
- Effort mode enabled by default
- `.env` file for Azure endpoint, API key, and deployment names
- CLIProxyAPI handles OAuth credential storage in `~/.cli-proxy-api`

### Diagnostics

- `doctor.sh`: tests Azure and protocol translation
- `cache-doctor.py`: verifies Azure prompt-cache hits through the proxy
- Offline unit tests + live smoke tests

### Security

Proxy listens on 127.0.0.1 only. Generated config is mode 0600. Launchers
unset `ANTHROPIC_API_KEY` to prevent accidental direct Anthropic billing.
Never enables `--dangerously-skip-permissions`.
