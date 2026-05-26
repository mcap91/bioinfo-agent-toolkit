---
name: n8n-mcp
title: "n8n MCP Server"
url: https://github.com/czlonkowski/n8n-mcp
category: mcp-server
verdict: watch
verdict_reason: "powerful workflow automation bridge but heavy dependency; evaluate when pipeline orchestration needs outgrow kb dispatch"
install: "npx @czlonkowski/n8n-mcp"
tags: [mcp, n8n, workflow-automation, orchestration, integrations]
workflows: []
reviewed: 2026-05-25
supersedes: []
overlaps: [gstack]
---

## What it does

An MCP server that connects AI assistants (Claude, Copilot, Cursor) with n8n's workflow automation platform. Provides 20+ tools for node search/retrieval/validation, workflow CRUD, execution management, credential handling, and security auditing. Covers 1,851 n8n nodes (822 core + 1,029 community), 2,352 workflow templates, and 265 AI-capable tool variants. Offers a cloud dashboard (100 free daily calls), self-hosting via npx/Docker/Railway, and IDE-specific integration guides. 21.3k stars, 1,016+ commits.

## Why this verdict

kb dispatch already handles our orchestration needs (subagent dispatch, handoff lifecycle). n8n would add value for external service integrations (Slack notifications, webhook triggers, scheduled pipeline monitoring) that kb doesn't cover natively. However, it's a heavy dependency (n8n instance + API keys + MCP server) for capabilities we don't currently need. Revisit when we have concrete automation requirements connecting bioinformatics pipelines to external systems (e.g., triggering Nextflow runs from webhooks, posting QC results to Slack).

## Mechanical details

- Quick start: cloud dashboard at dashboard.n8n-mcp.com (100 daily calls, no install)
- Self-host: `npx @czlonkowski/n8n-mcp` or Docker
- Requires `N8N_API_URL` and `N8N_API_KEY` for workflow management
- Claude Code integration via `.mcp.json` configuration
- Safety emphasis: never edit production workflows directly with AI
