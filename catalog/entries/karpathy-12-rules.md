---
name: karpathy-12-rules
title: "Karpathy's 12 Rules for CLAUDE.md"
category: reference
decision_status: adopted
summary: Rules 6 (token budgets) and 12 (fail loud) not yet in our stack
tags: [claude-md, best-practices, token-budgets]
reviewed: 2026-05-25
acquired: 2026-05-25
supersedes: []
license: unknown
security_flags: []
workflows: []
overlaps: []
---

## What it says

A 12-rule framework for CLAUDE.md best practices, sourced from a Reddit r/AskVibecoders post. The original 4 rules cover: think before coding, simplicity first, surgical changes, goal-driven execution. Eight additional rules expand coverage to agent loops, multi-step tasks, and silent failure modes. The complete set addresses the full lifecycle from planning through verification, including context management and failure communication.

## Assessment
Most rules are partially or fully covered by the existing superpowers skill set. Two rules have no current coverage: Rule 6 (token budgets) and Rule 12 (fail loud). These address real risks in longer sessions — context exhaustion causing degraded output, and silent skips masquerading as completions. Both are actionable additions to CLAUDE.md without requiring new tooling.

## What to adopt

**Rule 6 — Token budgets**: Add per-task (4K token) and per-session (30K token) budget guidelines to CLAUDE.md. Claude should summarize and start fresh when approaching limits, and surface budget breaches rather than silently degrading.

**Rule 12 — Fail loud**: Add explicit instructions that "completed" is incorrect if anything was skipped, and "tests pass" is incorrect if any tests were skipped. Default behavior should surface uncertainty rather than paper over it. This extends what `superpowers verification-before-completion` already covers — make it explicit in CLAUDE.md rather than relying solely on the skill trigger.

## Security

This entry is a reference document containing advisory text only — no executable code, dependencies, or network calls are involved. There is no supply-chain risk from adopting these rules; the worst-case outcome of following the advice is a suboptimal CLAUDE.md configuration, which is fully reversible.

The content originated from a Reddit post (r/AskVibecoders) and has no formal provenance, license, or authorship verification. Treat it as community-sourced guidance: evaluate each rule independently against your own context rather than adopting the list wholesale.
