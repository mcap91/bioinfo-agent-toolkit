---
name: claude-code-commands-reference
title: Claude Code Commands Reference
url: "https://code.claude.com/docs/en/commands"
category: reference
summary: "Anthropic's official reference documentation for every Claude Code CLI slash command, covering description, parameters, aliases, and minimum CLI version per command as of v2.1.224"
tags: [claude-code, documentation, slash-commands, cli-reference, anthropic-official]
workflows: []
reviewed: 2026-08-09
acquired: 2026-08-09
security_flags: []
supersedes: []
overlaps: [claude-code-commands-announcement, claude-howto, awesome-claude-code]
---

## What it says

The official Anthropic documentation page enumerating every built-in Claude Code CLI slash command, current as of CLI v2.1.224. Each entry documents the command's syntax and arguments, a description of its behavior, any aliases, and the minimum CLI version required (many entries note version-gated behavior changes, e.g. a flag or default that changed between v2.1.16x and v2.1.22x). Commands are grouped by function rather than in the page itself, but cover: session/context management (`/clear`, `/compact`, `/resume`, `/fork`, `/branch`, `/subtask`, `/rewind`, `/cd`, `/background`, `/context`), review and quality (`/code-review` and its alias `/review`, `/simplify`, `/security-review`), planning (`/plan`, `/batch`, `/goal`), model and configuration (`/model`, `/effort`, `/config`, `/permissions`, `/mcp`, `/fast`, `/autocompact`), diagnostics (`/doctor`, `/debug`, `/insights`, `/heapdump`, `/status`), third-party integration (`/install-github-app`, `/install-slack-app`, `/import`, `/web-setup`, `/design-sync`, `/chrome`), and interface/UX settings (`/theme`, `/statusline`, `/focus`, `/tui`, `/color`, `/keybindings`).

The page also documents several skill-backed commands that route to a Skill rather than built-in logic (e.g. `/batch`, `/code-review`, `/dataviz`, `/doctor`, `/simplify`, `/verify`, `/run`, `/debug`, `/deep-research`, `/claude-api`, `/loop`, `/fewer-permission-prompts`), and notes removed/renamed commands, such as `/ultraplan` now being listed as "Removed. Use plan mode instead," and `/vim` being removed in favor of `/config` → Editor mode.

## Key takeaways

- This is the canonical, versioned source for exact command syntax, flags, and aliases — useful as a reference lookup rather than a tutorial.
- Several commands have overlapping aliases documented explicitly (`/cost` = `/usage`; `/checkpoint`/`/undo` = `/rewind`; `/allowed-tools` = `/permissions`; `/quit` = `/exit`; `/settings` = `/config`), which is useful for recognizing equivalent invocations across differently-worded instructions or older documentation.
- Feature status changes over time are captured in-line (e.g. `/review` before v2.1.186 ran a read-only single-pass PR review; from v2.1.186–v2.1.201 it ran the same multi-agent engine as `/code-review`; `/ultraplan` was later removed entirely) — useful for reconciling older third-party writeups or catalog entries against current behavior.
- `/code-review`, `/review`, and `/simplify` are documented as running as a subagent in the background of interactive sessions (as of v2.1.218+) rather than inline in the conversation, which affects how their output should be expected to appear.

## Security

Official first-party Anthropic documentation, not executable code — no installation or runtime surface. Content is a living reference tied to CLI releases, so specific version-gated details (flags, aliases, defaults) can drift out of date relative to the installed CLI version; the page itself notes the exact version threshold for many behaviors.