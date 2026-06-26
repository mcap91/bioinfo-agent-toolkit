---
name: prompt-versioning-managed-agents
title: Prompt Versioning and Rollback (Managed Agents)
url: "https://platform.claude.com/cookbook/managed-agents-cma-prompt-versioning-and-rollback"
category: agent-pattern
tags: [managed-agents, prompt-management, versioning, rollback, evaluation, claude]
summary: ">-"
security_flags: [needs-api-key]
reviewed: 2026-06-25
acquired: 2026-06-26
---

## What it does

Demonstrates prompt lifecycle management using Claude Managed Agents' versioning system:

- **Version creation** — `agents.create` returns version 1; each `agents.update` produces a new immutable version with the same agent ID.
- **Version pinning** — Sessions can pin to an exact version for controlled evaluation, or use the bare agent ID to always get the latest.
- **Evaluation** — Runs a labeled test set against pinned versions to compare accuracy. The cookbook shows a support-ticket triage agent where a v2 prompt change causes billing-ticket routing to regress from 4/5 to 2/5.
- **Rollback** — Callers simply switch back to passing the previous version number. No deployment needed.

Key operational pattern: production callers always pin to an explicit version. Creating versions is exploratory; updating the production pin is the change that goes through review.

## Why it matters

Decouples prompt changes from code deployments. The version-pin pattern effectively gives prompts feature-flag semantics — canary routing, A/B testing, and instant rollback become config changes rather than deploy cycles. Relevant for any production agent system where prompt quality directly affects user outcomes.