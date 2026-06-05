---
name: agent-teams
title: "Claude Agent Teams"
url: https://code.claude.com/docs/en/agent-teams
category: agent-pattern
verdict: adopt
verdict_reason: "primary interactive dispatch path; subscription billing, no API credits needed"
tags: [agents, teams, dispatch, orchestration]
reviewed: 2026-05-25
acquired: 2026-05-25
supersedes: []
---

## What it says

Claude Agent Teams is an experimental feature (requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` and v2.1.32+) where one lead session coordinates multiple teammate sessions. Teammates share a task list (pending → in progress → completed, with dependency support) and a mailbox for direct teammate-to-teammate messaging. Each teammate is a separate Claude instance with its own context window; they load the same project context (CLAUDE.md, MCP servers, skills) but not the lead's conversation history. Display modes are in-process (works everywhere, Shift+Down to cycle) and split panes (requires tmux or iTerm2 — not supported in Windows Terminal, VS Code terminal, or Ghostty). Subagent definitions can serve as teammate roles: their `tools` allowlist and `model` are honored and their body is appended to the teammate's system prompt, but `skills` and `mcpServers` frontmatter fields are not applied — teammates load those from project/user settings.

## Why this verdict

Billing runs under interactive subscription — no API billing or Agent SDK credits needed. This directly satisfies the core kb dispatch constraint introduced by the June 15, 2026 Agent SDK credit change. kb dispatch interoperability is strong: if kb-wiki MCP is configured, teammates have full read/write access to wiki records. Dispatch cannot launch agent teams (interactive-only, no `-p` mode), and the task list is transient, but teammates can write durably via MCP — so the integration surface is MCP, not subprocess launch.

## What to adopt

1. Don't wrap agent teams in dispatch. Teammates call `create-handoff`, `get-response`, and `review` via kb-wiki MCP directly during the team session.
2. Assign a "scribe" teammate to write HO-style summaries as wiki records at session end so outputs survive past the transient task list.
3. Agent teams are operator-directed — dispatch defines the protocol (what an HO is, how responses are structured, where artifacts go) but does not own execution.
4. Use in-process display mode on Windows; reserve split-pane mode for tmux/iTerm2 environments.
5. Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` and confirm v2.1.32+ before relying on this path.

**kb dispatch interoperability table**:

| Question | Answer |
|---|---|
| Can teammates read kb wiki? | Yes. If kb-wiki MCP is configured, teammates have full access. |
| Can teammates write to kb wiki? | Yes. Same MCP access. Teammates can create/update WK issues. |
| Can dispatch launch agent teams? | No. Agent teams are interactive-only. No `-p` mode. |
| Can dispatch capture team outputs? | Not directly. Task list is transient. Teammates must write durably via MCP. |
| Is billing acceptable? | Yes. Subscription only. No API credits. |
