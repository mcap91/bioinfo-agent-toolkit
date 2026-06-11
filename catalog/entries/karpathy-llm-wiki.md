---
name: karpathy-llm-wiki
title: "Karpathy's LLM Wiki Pattern"
url: "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
category: reference
verdict: adopt
verdict_reason: Foundational pattern doc for LLM-maintained personal knowledge bases — directly describes the architecture kb-wiki implements
tags: [knowledge-base, wiki, llm-pattern, obsidian, personal-knowledge-management, rag-alternative]
workflows: []
reviewed: 2026-06-10
acquired: 2026-06-10
license: NOASSERTION
security_flags: []
supersedes: []
overlaps: [third-brain-v5-wiki]
---

## What it says

A pattern document (idea file) by Andrej Karpathy for building personal knowledge bases using LLMs. The core insight: instead of RAG (re-deriving knowledge from raw sources on every query), have the LLM incrementally build and maintain a persistent wiki — structured, interlinked markdown files that compound over time. Three layers: raw sources (immutable), the wiki (LLM-owned markdown), and the schema (CLAUDE.md/AGENTS.md that configures the LLM as a wiki maintainer). Three operations: ingest (process source → update wiki pages), query (search wiki → synthesize answer → optionally file back), lint (health-check for contradictions, orphans, stale claims). Designed for Obsidian as the reading interface, git as version control, with optional CLI tools for search at scale.

## Why this verdict

This is the foundational pattern behind what kb-wiki implements. The three-layer architecture (sources → wiki → schema), the ingest/query/lint operations, and the philosophy of "LLM does the bookkeeping, human does the thinking" map directly to the toolkit's wiki workflow. Adopt as a canonical reference — revisit when evolving kb-wiki's architecture.

## What to adopt

- The index.md + log.md navigation pattern (kb-wiki already implements variants of both)
- The lint operation concept: contradiction detection, orphan pages, missing cross-references, stale claims
- The principle that good query answers should be filed back into the wiki as pages
- The "schema co-evolution" idea — the CLAUDE.md and wiki conventions evolve together as you learn what works

## Security

This is a gist (idea document), not executable code. No dependencies, no installation, no runtime. No security concerns. License not specified on the gist — treating as NOASSERTION.