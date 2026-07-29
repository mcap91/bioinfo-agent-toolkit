---
name: pi-coding-agent
title: Pi Coding Agent
url: "https://github.com/earendil-works/pi"
category: framework
summary: "Minimal, extensible terminal coding agent harness by Mario Zechner (Earendil Works). Four core tools (read, write, edit, bash), ~200-token system prompt, 37+ models across 20+ providers (Anthropic, OpenAI, Google, Bedrock, etc.). Extensible via TypeScript extensions, skills, prompt templates, themes, and packages — deliberately omits MCP, sub-agents, plan mode, and permission popups in favor of user-built alternatives. Tree-structured sessions with branching, compaction, and forking. SDK/RPC modes for embedding. MIT. ~78k GitHub stars."
install: "npm install -g --ignore-scripts @earendil-works/pi-coding-agent"
license: MIT
tags: [coding-agent, terminal, cli-tool, extensible, multi-provider, sdk, typescript, sessions, skills, themes]
reviewed: 2026-07-28
acquired: 2026-07-28
supersedes: []
overlaps: []
security_flags: []
workflows: []
---

## What it is

Pi is a minimal terminal coding agent harness from Mario Zechner (badlogic, creator of libGDX) under Earendil Works / pi.dev. It provides an interactive coding agent with four built-in tools (read, write, edit, bash) and a system prompt of approximately 200 tokens. It supports 37+ models across 20+ providers via API keys or subscriptions (Anthropic Claude Pro/Max, OpenAI ChatGPT Plus/Pro, GitHub Copilot, Google Gemini/Vertex, Azure, Bedrock, Mistral, Groq, xAI, OpenRouter, llama.cpp, and others).

Pi runs in four modes:
- **Interactive** — full TUI with editor, file references (@), image paste, message queue (steering + follow-up), keyboard shortcuts
- **Print** — single prompt, print response, exit (`pi -p`)
- **JSON** — all events as JSON lines for machine consumption
- **RPC** — stdin/stdout protocol for process integration

Sessions are tree-structured JSONL files supporting in-place branching (`/tree`), forking (`/fork`, `/clone`), and context compaction (manual or automatic). The monorepo also ships `@earendil-works/pi-ai` (unified multi-provider LLM API) and `@earendil-works/pi-agent-core` (agent framework).

## Mechanical details

- **Install:** `npm install -g --ignore-scripts @earendil-works/pi-coding-agent` or `curl -fsSL https://pi.dev/install.sh | sh`
- **Customization layers:** TypeScript extensions (tools, commands, UI, event handlers), skills (Agent Skills standard / SKILL.md), prompt templates (Markdown with `{{variables}}`), themes (hot-reloadable), pi packages (npm or git distribution)
- **No built-in:** MCP, sub-agents, plan mode, permission popups, todos, background bash — all available via extensions or packages
- **Context files:** Loads AGENTS.md / CLAUDE.md from global, parent dirs, and cwd
- **Config:** `~/.pi/agent/settings.json` (global) and `.pi/settings.json` (project)
- **Platforms:** Windows, macOS, Linux, Termux (Android), tmux
- **SDK:** `createAgentSession()` API for embedding in Node.js apps

## Security

MIT licensed. Extensions execute arbitrary code with full system access. Skills can instruct the model to perform any action including running executables. The README advises reviewing source code before installing third-party packages. Telemetry is opt-out (install/update pings to pi.dev; provider attribution headers for OpenRouter/Cloudflare/NVIDIA). No security flags observed in the core tool.