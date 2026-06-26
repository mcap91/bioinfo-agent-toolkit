---
name: knowledge-graph-construction-anthropic
title: Knowledge Graph Construction (Anthropic Cookbook)
url: "https://platform.claude.com/cookbook/capabilities-knowledge-graph-guide"
category: agent-pattern
tags: [knowledge-graph, entity-extraction, entity-resolution, structured-output, networkx, claude]
summary: ">-"
security_flags: [needs-api-key]
reviewed: 2026-06-25
acquired: 2026-06-26
---

## What it does

End-to-end pipeline for constructing knowledge graphs from unstructured documents using Claude prompts instead of trained NER/RE models:

1. **Extraction** — A single structured-output call per document extracts typed entities (PERSON, ORG, LOCATION, EVENT, ARTIFACT) and subject-predicate-object triples. Uses Pydantic schemas with `client.messages.parse()` for guaranteed valid output. Haiku handles this high-volume step.

2. **Entity Resolution** — Claude clusters surface-form variants (e.g. "Edwin Aldrin" / "Buzz Aldrin") using extraction descriptions as disambiguation context. Catches cases string-similarity methods miss entirely. Sonnet handles this judgment-heavy step. Scales via blocking (group by cheap signals first, resolve within blocks of 50-100).

3. **Graph Assembly** — Rewrites relation endpoints to canonical forms and loads into NetworkX MultiDiGraph. Nodes carry type, source documents, and mention counts.

4. **Summarization** — Hub nodes get rich profiles synthesized across all mentioning documents, with structured time ranges and key facts.

5. **Querying** — Serializes relevant subgraphs as triples and lets Claude answer multi-hop questions with edge-level citations.

Includes a precision/recall evaluation harness against gold-labeled triples.

## Why it matters

Replaces the traditional train-NER, train-RE, write-entity-resolution-heuristics pipeline with prompts. Directly applicable to biomedical literature mining, variant-gene-disease relationship extraction, and any domain where multi-hop reasoning across documents is needed.