---
name: advise-project-approach
title: "Advise Project Approach"
url: https://github.com/AaravKashyap12/advise-project-approach
category: skill
verdict: pilot
verdict_reason: "structured project-level architecture research with comparable analysis, cost checks, and tradeoff discipline; complements /catalog (tool-level) with project-level advisory"
install: "npx skills@latest add AaravKashyap12/advise-project-approach --skill advise-project-approach"
tags: [architecture, stack-selection, comparables, cost-analysis, project-strategy, decision-methodology]
reviewed: 2026-06-02
supersedes: []
overlaps: []
---

## What it does

A Claude Code skill (22KB SKILL.md) that automates the research loop a strong engineer would do before committing to a technology stack. Three operating modes: pre-build strategy (no repo yet — research comparables, evaluate stacks, recommend an approach), mid-build course correction (inspect existing repo against goals and external references), and post-build review (architecture, quality, deployment readiness against mature comparables). The skill enforces a structured decision methodology: frame constraints, research comparable projects, extract transferable patterns, check operating costs against real pricing pages, compare 2-4 approaches in a tradeoff matrix, and recommend with explicit failure conditions. Distinguishing features include comparable bias controls (popularity doesn't override fit), pricing reality checks (separates "free to start" from actual operating cost), and calibrated output contracts (weekend prototype and production SaaS get different standards). MIT licensed, 32 stars, 3 releases (latest v0.3.0). Also available as a packaged `.skill` file.

## Why this verdict

Nothing in the current stack does project-level architecture advisory. Our `/catalog` skill evaluates individual tools (one URL → one entry with a verdict), while this skill evaluates entire project approaches (comparable projects, stack options, architecture, costs → strategy or review doc). The decision methodology section — constraints-first evaluation, comparable bias controls, operating-cost reality checks, and explicit "when this becomes wrong" failure conditions — is well-engineered and could inform how we structure our own catalog verdicts. The hard gates (no trendy recommendations, no invented data, no "free to start" marketing as proof) align with our catalog's evidence-based approach. Risk is low: it's a standalone SKILL.md with no dependencies, and its trigger conditions ("project strategy", "stack selection", "architecture critique") don't overlap with any existing skill.

## Mechanical details

Install: `npx skills@latest add AaravKashyap12/advise-project-approach --skill advise-project-approach` or manually download from `dist/advise-project-approach.skill` or GitHub releases. The skill is vendor-agnostic (core SKILL.md can be copied to non-Claude agents). Uses WebFetch and WebSearch for external research when available; degrades to local-only analysis when browsing is blocked. No runtime dependencies beyond the Claude Code skill system. Trigger conditions include: "project strategy", "optimal approach", "research comparables", "stack selection", "architecture critique", or "implementation feedback". Does not trigger for narrow single-bug debugging or isolated file edits.
