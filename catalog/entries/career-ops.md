---
name: career-ops
title: Career-Ops
url: "https://github.com/santifer/career-ops"
category: cli-tool
tags: [job-search, skills, PDF-generation, ATS, batch-processing, multi-CLI]
reviewed: 2026-07-03
security_flags: []
summary: ">-"
acquired: 2026-07-04
---

## What It Does

Career-Ops turns any AI coding CLI into a job search command center. It evaluates job
offers against a user profile using a structured scoring system (10 weighted dimensions),
generates tailored ATS-optimized CVs as PDFs, scans career portals automatically, and
tracks everything in a markdown-based pipeline.

## Key Features

- **Auto-pipeline**: paste a job URL or description, get a full evaluation + PDF + tracker
  entry
- **6-block evaluation**: role summary, CV match, level strategy, comp research,
  personalization, interview prep (STAR+R), plus a posting-legitimacy scam check
- **ATS PDF generation**: keyword-injected CVs with Space Grotesk + DM Sans via
  Playwright/Puppeteer
- **Cover letter generator**: research-backed, keyword-mirrored, A4 PDF output
- **Portal scanner**: 45+ pre-configured companies + 21 provider modules (ATS APIs,
  board feeds, RSS, XML)
- **Batch processing**: parallel evaluation with headless CLI workers
- **Dashboard TUI**: Go + Bubble Tea terminal UI with 6 filter tabs, 4 sort modes
- **Contact discovery**: identifies hiring manager/recruiter/peer, drafts LinkedIn
  messages

## Architecture

Uses the shared agent-skill-standard: `AGENTS.md` holds canonical instructions, with
thin wrappers for each CLI (`CLAUDE.md`, `CODEX.md`, `OPENCODE.md`). 15 skill modes
under `modes/` handle different workflows. Data stored as markdown tables + YAML config +
TSV. All data stays local — nothing is sent to a hosted service.

## Supported CLIs

Claude Code, Codex, OpenCode, Gemini (Antigravity CLI), Qwen, Grok Build CLI, agy.

## Links

- GitHub: https://github.com/santifer/career-ops
- Author portfolio: https://santifer.io