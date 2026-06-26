---
name: outcomes-managed-agents
title: Outcomes / Outcome Grader (Managed Agents)
url: "https://platform.claude.com/cookbook/managed-agents-cma-verify-with-outcome-grader"
category: agent-pattern
tags: [managed-agents, verification, grading, rubric, self-correction, claude]
summary: ">-"
security_flags: [needs-api-key]
reviewed: 2026-06-25
acquired: 2026-06-26
---

## What it does

Demonstrates the Outcomes feature in Claude Managed Agents, which adds a verification loop to agent sessions:

- **Rubric definition** — A `define_outcome` event provides a task description (for the writer) and a rubric (for the grader). The rubric must make the grader produce evidence — fetch URLs, verify quotes, check filing types — not just skim and approve.
- **Independent grading** — The platform provisions a grader in its own context window with the same model and tools as the writer. The grader cannot see the writer's reasoning and re-checks the entire artifact each iteration.
- **Revision loop** — After each writer turn, the grader scores per-criterion and either passes the output or returns a structured list of gaps. The writer revises and the loop runs again, up to `max_iterations` (default 3, max 20).
- **Real example** — A research brief where the grader catches a press-release exhibit cited as a 10-K, forces the writer to find the actual SEC filing, and passes on the third iteration.

Key rubric design principles: make criteria checkable with evidence, make the grader earn "satisfied," describe goals not steps, anticipate writer shortcuts, mandate feedback format.

## Why it matters

The writer/grader separation is more reliable than self-checking in a single context because the grader has no access to the writer's reasoning shortcuts. The rubric design guidance is transferable to any agent verification system — the key insight is that a rubric must force evidence production, not just pattern matching.