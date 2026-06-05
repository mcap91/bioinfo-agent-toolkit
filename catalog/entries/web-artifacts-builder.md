---
name: web-artifacts-builder
title: "Web Artifacts Builder"
url: https://github.com/anthropics/skills/blob/main/skills/web-artifacts-builder/SKILL.md
category: skill
verdict: adopt
verdict_reason: "use when markdown isn't enough for interactive reports/dashboards"
tags: [html, reports, dashboards, visualization]
workflows: [scRNA-seq, spatial]
reviewed: 2026-05-25
acquired: 2026-05-25
supersedes: []
---

## What it does

Generates self-contained HTML reports and interactive dashboards as skill output. Fills the gap between static markdown output (which lacks interactivity) and full application development (which is overkill for analysis reports). Suitable for QC summaries, pipeline result dashboards, and comparative analyses where users need to explore data rather than just read it. Source is the official Anthropic skills repository.

## Why this verdict

Markdown is sufficient for most workflow documentation, but interactive outputs are needed for analysis results that users need to explore — differential expression tables, QC metric comparisons, spatial transcriptomics overlays. This skill is already in the Anthropic skills repo and is ready to adopt as a named output format option.

## Mechanical details

Install from `https://github.com/anthropics/skills/blob/main/skills/web-artifacts-builder/SKILL.md`. Use when a workflow produces results that benefit from interactivity: sortable tables, filterable lists, toggle views. Default to markdown; escalate to this skill when markdown is insufficient.
