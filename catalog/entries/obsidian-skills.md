---
name: obsidian-skills
title: "Obsidian Skills (Kepano)"
url: https://github.com/kepano/obsidian-skills
category: skill
verdict: note
verdict_reason: "Obsidian-specific; Defuddle (web→clean markdown) and skill packaging patterns worth noting"
tags: [obsidian, skills, markdown, canvas, defuddle, web-extraction]
workflows: []
reviewed: 2026-05-25
acquired: 2026-05-25
supersedes: []
---

## What it does

A collection of five Claude Code-compatible skills for working with Obsidian vaults: Obsidian Markdown (wikilinks, embeds, callouts, properties), Obsidian Bases (database-like views with filters and formulas), JSON Canvas (visual node/edge canvas files), Obsidian CLI (vault interaction via command-line for plugin/theme dev), and Defuddle (extracts clean markdown from web pages, stripping unnecessary content to conserve tokens). Installable via plugin marketplace, npx, or manual copy. 33k stars.

## Why this verdict

The Obsidian-specific skills (Markdown, Bases, Canvas, CLI) don't apply — we use kb wiki, not Obsidian, as our knowledge layer. Defuddle is the interesting outlier: extracting clean markdown from web pages while conserving tokens is a pattern we could use for catalog research or source ingestion. The skill packaging approach (marketplace + npx + manual install paths) is also a useful reference for how to distribute skills.

## What to adopt

- Defuddle concept: consider a "web→clean markdown" extraction step for catalog research or kb source ingestion workflows.
- Multi-platform install pattern (marketplace, npx, manual) as a distribution model if we ever publish skills externally.
