---
name: knowledge-work-plugins
title: Knowledge Work Plugins (Anthropic)
url: "https://github.com/anthropics/knowledge-work-plugins"
category: framework
tags: [claude-cowork, claude-code, plugins, skills, connectors, mcp, bio-research]
summary: ">-"
security_flags: []
reviewed: 2026-06-25
acquired: 2026-06-26
---

## What it does

A marketplace of 11 open-source plugins that turn Claude into a role-specific specialist. Each plugin follows a standard structure:

- `plugin.json` — manifest
- `.mcp.json` — tool connections (MCP servers for CRMs, project trackers, data warehouses, etc.)
- `commands/` — explicit slash commands (e.g. `/finance:reconciliation`, `/data:write-query`)
- `skills/` — domain knowledge Claude draws on automatically when relevant

**Available plugins:** productivity (Slack, Notion, Asana, Linear, Jira), sales (HubSpot, Close, Clay, ZoomInfo), customer-support (Intercom, HubSpot, Guru), product-management (Linear, Figma, Amplitude, Pendo), marketing (Canva, Figma, HubSpot, Ahrefs), legal (Box, Egnyte), finance (Snowflake, Databricks, BigQuery), data (Snowflake, Databricks, Hex, Amplitude), enterprise-search, bio-research (PubMed, BioRender, bioRxiv, ClinicalTrials.gov, ChEMBL, Synapse, Open Targets, Benchling), and cowork-plugin-management.

Installation via `claude plugin marketplace add` and `claude plugin install`. All file-based (markdown + JSON), no code or infrastructure required.

## Why it matters

The bio-research plugin is directly relevant — it pre-wires connections to PubMed, bioRxiv, ClinicalTrials.gov, ChEMBL, Benchling, and Open Targets, providing a ready-made starting point for life sciences agent workflows. The plugin structure (skills + MCP connectors + commands) is a proven pattern for packaging domain expertise.