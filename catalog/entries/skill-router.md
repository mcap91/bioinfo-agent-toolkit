---
name: skill-router
title: "Skill Router"
url: https://github.com/pcx-wave/skill-router
category: meta-skill
verdict: skip
verdict_reason: "superpowers using-superpowers already handles skill routing"
tags: [meta-skill, routing, skill-discovery]
reviewed: 2026-05-25
supersedes: []
---

## What it does

Scans installed skills, builds a lightweight keyword index, and routes incoming requests to the most relevant skill. Operates in two modes: suggest (presents matches for confirmation) and auto (applies high-confidence matches without prompting). Conservative by design — only triggers on high-confidence keyword matches to avoid false routing.

## Why this verdict

`superpowers using-superpowers` already handles skill discovery and routing in this stack. Skill Router would duplicate that responsibility without adding capability. No gap to fill.

## Mechanical details

Not recommended for install. If skill routing gaps are discovered that superpowers does not cover, revisit this entry before building a custom solution.
