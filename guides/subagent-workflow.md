# Subagent Workflow Guide

How to use Claude Code's built-in subagent pattern to automate the "plan with Opus, execute with Sonnet" workflow.

## The Problem

When working on multi-phase tasks in Claude Code, context windows fill up. A common manual workaround: hit a milestone, write a handoff prompt, clear context, paste it into a new CLI session. This works but is tedious.

## The Solution: Subagents

Subagents are specialized agents that run in their own context window with a custom system prompt, specific tool access, and independent permissions. They execute a task and return results to the parent session.

This is exactly the "fresh agent with a prompt" workflow — but automated.

## Setup

Create a Markdown file in `.claude/agents/` (project-level) or `~/.claude/agents/` (global) with YAML frontmatter:

```markdown
---
name: phase-executor
description: Executes implementation phases from spec docs. Use proactively for phase implementation tasks.
tools: Bash, Read, Write, Grep, Glob
model: sonnet
---

You are an implementation specialist. You will receive a phase spec
and execute it precisely. Follow the spec document instructions exactly.
Read the project README and relevant spec docs before making changes.
Run tests after implementation to verify correctness.
```

The `model: sonnet` field routes the subagent to a faster/cheaper model while the main session stays on Opus.

## Usage Pattern

1. **Opus creates the plan/spec** as usual
2. **Delegate** a phase to the subagent instead of manually writing a handoff prompt
3. **The subagent executes** in its own fresh context
4. **Results return** to the Opus session, which continues orchestrating

You can background subagents with `Ctrl+B` and keep working while they run.

## Tips

- **Over-delegation**: Opus can be aggressive about spawning subagents. Add guidance in `CLAUDE.md` about when to use subagents vs. work directly if this becomes an issue.
- **Agent Teams** (experimental): For advanced workflows where multiple subagents need to coordinate with each other rather than just reporting back to Opus, there's an Agent Teams feature using a shared task list.
