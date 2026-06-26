---
name: contextual-retrieval-anthropic
title: Contextual Retrieval (Anthropic Cookbook)
url: "https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide"
category: agent-pattern
tags: [rag, embeddings, retrieval, bm25, reranking, claude, prompt-caching]
summary: ">-"
security_flags: [needs-api-key]
reviewed: 2026-06-25
acquired: 2026-06-26
---

## What it does

Demonstrates three progressive techniques for improving RAG retrieval quality over a baseline chunked-embedding approach:

1. **Contextual Embeddings** — Before embedding each chunk, Claude generates a short description situating the chunk within its source document. The context is prepended to the chunk before embedding. Improves Pass@10 from 87% to 92%. Prompt caching makes this practical: sequential same-document processing achieves ~62% cache hit rate, reducing ingestion cost from ~$9 to ~$3 for the demo corpus.

2. **Contextual BM25 Hybrid Search** — Combines contextual semantic search with BM25 keyword search (via Elasticsearch) using weighted Reciprocal Rank Fusion (default 80% semantic / 20% BM25). Catches exact keyword matches that embeddings miss.

3. **Reranking** — Over-retrieves 10x candidates, then uses Cohere's rerank model to score and select the top-k. Achieves 95.26% Pass@10 — a 47% reduction in retrieval failures vs baseline.

Uses Voyage AI for embeddings, Elasticsearch for BM25, and Cohere for reranking.

## Why it matters

The contextual embeddings technique addresses a fundamental RAG weakness: chunks embedded in isolation lose document-level context. The ~35% reduction in retrieval failures from this single technique offers the best cost/performance tradeoff. The full stack (contextual embeddings + hybrid + reranking) nearly eliminates retrieval failures at the cost of added infrastructure and per-query latency.