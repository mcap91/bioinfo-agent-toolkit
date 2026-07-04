---
name: openhands
title: OpenHands
url: "https://github.com/OpenHands/openhands"
category: framework
tags: [agent-framework, coding-agent, self-hosted, automation, ACP, Docker]
reviewed: 2026-07-03
security_flags: []
summary: ">-"
acquired: 2026-07-04
---

## What It Does

OpenHands (formerly OpenDevin) provides an Agent Canvas UI and Agent Server for running
coding agents as a self-hosted, always-on engineering team. It supports starting
conversations, automating tasks (report generation, GitHub issue decomposition), and
integrating with third-party services.

## Key Features

- **Multi-agent support**: run OpenHands' built-in agent, Claude Code, Codex, Gemini, or
  any Agent-Client Protocol (ACP) compatible agent
- **Flexible backends**: local (direct filesystem), Docker sandbox, VM, cloud — switch
  between backends from the same UI
- **Automations**: scheduled or webhook-triggered workflows integrating with Slack,
  GitHub, Linear, Notion, Datadog
- **Agent Server**: REST API for running multiple agents on a single machine; Agent Canvas
  connects to multiple servers
- **Bring your own model**: works with any LLM

## Architecture

Agent Canvas (frontend) connects to one or more Agent Servers (backend REST API). Each
server runs on a single host and manages agent sessions. An optional Automation Server
handles scheduled and event-driven agent runs. The default agent uses the CodeAct
architecture — executable Python code as unified action space.

## Deployment Options

- **No sandbox**: `npm install -g @openhands/agent-canvas && agent-canvas` (agent has full
  filesystem access)
- **Docker sandbox**: containerized with project directory mounting
- **Cloud/Enterprise**: OpenHands Cloud commercial offering

## Links

- GitHub: https://github.com/OpenHands/openhands
- Docs: https://docs.openhands.dev/