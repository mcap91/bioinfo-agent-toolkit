---
name: gbrain
title: "gbrain"
url: https://github.com/garrytan/gbrain
category: framework
verdict: skip
verdict_reason: "kb wiki already provides persistent typed records with relationships and search"
tags: [memory-graph, vector-search, kb]
reviewed: 2026-05-25
acquired: 2026-05-25
supersedes: []
---

## What it does

A persistent memory graph with hybrid search (vector + keyword) and typed links. Designed for long-lived memory across sessions covering entities, experiments, and literature. Combines vector similarity search (semantic) with keyword search to retrieve relevant memory nodes.

## Why this verdict

kb wiki already provides persistent, typed records with relationships and text-based search. gbrain's typed links overlap with kb graph's structural relationships. The one genuine addition is vector search (semantic similarity), which kb's text-based search index doesn't have — but this isn't a current gap that needs closing. Only worth revisiting if kb hits a wall on search relevance that would benefit from vector embeddings.

## Mechanical details

Do not install. The use case is fully covered by kb wiki + kb graph. If search relevance becomes a concern in the future, vector embeddings could be added to the existing search index rather than adopting a separate memory graph system.
