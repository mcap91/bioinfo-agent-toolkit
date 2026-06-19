---
name: firecrawl
title: Firecrawl
url: "https://github.com/mendableai/firecrawl"
category: framework
summary: "Production-grade web scraping/search/interaction API for AI agents — clean markdown output, JS rendering, anti-bot handling, MCP server mode; AGPL-3.0, YC-backed, 40K+ stars, but copyleft license limits embedding"
tags: [web-scraping, mcp-server, rag, agent-infrastructure, markdown]
workflows: []
reviewed: 2026-06-19
acquired: 2026-06-19
license: AGPL-3.0-only
security_flags: []
supersedes: []
overlaps: [crawl4ai, browser-use]
---

## What it does

Firecrawl is a web data API that turns websites into LLM-ready content. Three core capabilities:

- **Scrape**: Extract any URL as clean markdown, HTML, screenshots, or structured JSON. Handles JavaScript rendering, proxies, and anti-bot measures.
- **Search**: Web search with full page content from results in one call.
- **Interact**: Scrape a page then continue working with it — click buttons, fill forms, extract dynamic content via natural language or code.

Built by Mendable (now Firecrawl), YC-backed. SDKs in JavaScript, Python, Java, and Elixir. Ships an MCP server for direct integration with Claude Code, Cursor, Windsurf, and VS Code. Also available as a CLI (`npx firecrawl-cli`).

Cloud-hosted service with free and paid tiers. Self-hosting is free under AGPL-3.0 but excludes managed-only features like the `/agent` endpoint.

## Assessment

Strong production web scraping infrastructure used by 80K+ teams. The MCP server mode makes it immediately useful for agent workflows that need web content — literature searches, documentation fetching, data extraction from bioinformatics portals. Overlaps with Crawl4AI (async crawler, MIT) but Firecrawl is more polished, better maintained, and has richer features (search, interact). The tradeoff is AGPL-3.0 copyleft vs Crawl4AI's MIT license.

For our catalog MCP server's `fetch-url` tool, Firecrawl could serve as an upstream provider for harder-to-scrape sites. The MCP server mode is the most relevant integration path.

## Mechanical details

- **Install MCP**: `npx -y firecrawl-cli@latest init --all --browser`
- **Cloud API**: Requires API key from firecrawl.dev
- **Self-host**: Docker compose available in repo; AGPL-3.0 applies
- **SDK install**: `pip install firecrawl` / `npm install @mendable/firecrawl-js`
- 40K+ GitHub stars, 79+ contributors, active development
- Recent releases address CVEs and SSRF hardening in Playwright service

## Security

- **License**: AGPL-3.0 — copyleft; any network-accessible service using Firecrawl code must release source. Self-hosting is free but commercial SaaS embedding requires license review.
- **Supply chain**: YC-backed company, 79+ contributors, regular releases with CVE patches. Organization migrated from mendableai to firecrawl on GitHub.
- **Code quality**: Tests, CI, multiple SDK maintainers. Recent SSRF hardening in Playwright service.
- **Dependency health**: Active CVE patching in recent releases.
- **API key handling**: Cloud mode requires API key storage; standard practice.
