---
name: unforget
title: "Unforget"
url: ""
category: skill
verdict: skip
verdict_reason: "scan-for-escaped-items pattern worth noting for future kb lint rule or audit command"
tags: [deferred-work, scanner, todos, kb]
reviewed: 2026-05-25
supersedes: []
---

## What it does

Scans multiple hiding spots where deferred work tends to accumulate — Deferred.md, plan files, memory entries, TODO docs, and code TODOs — and consolidates findings into an UNFORGET.md file with 10-column rating tables. The signature column is Target, with values THIS (current session), NEXT (next session), LATER (someday), and SOMEDAY (backlog). A `/unforget promote` command handles release cycle transitions, moving NEXT items to THIS when a session begins. The key insight is that Unforget addresses a different problem than a wiki: a wiki tracks what you put into it, while Unforget finds what escaped tracking.

## Why this verdict

kb wiki tracks what you explicitly create records for — it assumes you'll create a record for everything important. Unforget assumes things escape. These are complementary problem spaces, not overlapping ones. The "scan for escaped items" pattern is genuinely useful and kb has no equivalent. However, this is a Reddit r/claudeskills post rather than a maintained tool, and the concept is simple enough to implement as a native kb lint rule.

**The escaped-items pattern**: A "sweep" or "audit" command that scans the repo for TODOs, deferred markers, and plan files that don't have corresponding wiki records. This is a gap in kb lint — it validates records that exist but doesn't detect work that was never recorded.

**What kb could learn**: A `kb lint --sweep` or `kb audit` command that scans for:
- TODO/FIXME/HACK comments in code without linked wiki issues
- Deferred.md or DEFERRED.md files without corresponding wiki records
- Plan files (PLAN.md, plan-*.md) without linked wiki initiatives
- Memory entries marked "revisit" or "later" without wiki issues

## Mechanical details

Do not install. The concept is the value, not the tool. Implementing the sweep pattern natively in kb lint would be more useful than a separate scanner that doesn't understand kb's record schema. If a future kb lint rule is implemented, the UNFORGET.md rating table format (10-column with Target column) is a useful reference for what a consolidation output could look like.
