---
name: smithery
title: Smithery
url: "https://smithery.ai/"
category: reference
tags: [MCP, registry, discovery, hosting, CLI, tool-directory]
reviewed: 2026-07-03
security_flags: []
summary: ">-"
acquired: 2026-07-03
---

## What It Does

Smithery is a central hub for discovering, installing, and hosting Model Context Protocol
servers. Developers can search thousands of MCP servers, install them locally via the
Smithery CLI, or run them as hosted remote endpoints on Smithery's infrastructure with no
setup of their own.

## Key Features

- **Registry & discovery**: 7,000+ MCP servers indexed and searchable
- **Dual deployment**: local install via CLI or Smithery-hosted remote endpoints
- **Toolbox (meta-MCP router)**: a single MCP server that dynamically connects an agent
  to other servers in the registry — no manual wiring per server
- **Managed OAuth**: generated OAuth modals for hosted servers; credential handling via
  open-source agent.pw vault
- **CLI tooling**: `npx smithery auth login`, `npx smithery mcp add <server>`,
  `npx smithery tool call` — supports multiple languages and transports
- **Usage analytics**: call counts and observability for published servers

## Architecture

Connect once, use everywhere — connections carry across runtimes (Claude, GPT,
open-source models, background agents, CLI tools). Auth, credentials, and sessions are
handled by the platform. Powered by agent.pw, an open-source agent credential vault.

## Comparable Registries

Other MCP registries include Glama (~50k servers), mcp.so (~20k), and the
punkpeye/awesome-mcp-servers GitHub list. Smithery pairs the registry with a hosting
layer and meta-MCP router, which the others lack.

## Links

- Main site: https://smithery.ai/
- Server registry: https://smithery.ai/servers