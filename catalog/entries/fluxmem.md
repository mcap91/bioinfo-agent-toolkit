---
name: fluxmem
title: "FluxMem: Continuously Evolving Memory Connectivity"
url: "https://arxiv.org/abs/2505.00000"
category: reference
tags: [memory, agent-memory, research-paper, rag, semantic-memory, episodic-memory, procedural-memory, self-repair]
reviewed: 2026-07-21
summary: ">-"
acquired: 2026-07-22
---

## What it covers

A memory architecture for AI agents that treats memory as an evolving
graph of interconnected nodes rather than a flat retrieval store.

### Three memory layers

- **Semantic memory**: factual knowledge — documents, dialogue history,
  tool instructions
- **Episodic memory**: concrete experiences — observations, actions taken,
  task trajectories
- **Procedural memory**: reusable skills distilled from repeated
  experience — planning patterns, tool-use sequences

Layers are interconnected: a fact links to the episode where it proved
useful; related episodes link to a procedural skill extracted from their
common structure.

### Runtime self-repair (feedback-driven)

After retrieval, the system attempts a step, receives feedback, and
diagnoses whether the activated memory helped:

- **Link expansion**: searches for relevant but inactive memory nodes
  when critical context is missing (under-connection)
- **Link pruning**: removes connections that introduce noise or push
  toward incorrect actions (over-connection)
- **Content reshaping**: expands coarse memories or compresses overly
  detailed ones to match task granularity (treats abstraction level as
  revisable, not fixed at storage time)

### Offline consolidation

Clusters similar episodic trajectories, extracts shared skill/reasoning
patterns via LLM, tests against source tasks, iterates until Procedure
Evolution Maturity Score (PEMS) converges. PEMS combines task success
rate, conciseness, and stability across revisions.

### Benchmark results

- LoCoMo (long-conversation reasoning): 95.06% with GPT-4.1-mini
  (baseline 81.23%; feedback-driven refinement most impactful)
- Mind2Web (web navigation): 8.1% cross-task success with GPT-4.1-mini
  (baseline 3.6%; procedural consolidation most impactful)
- GAIA (general assistant): 64.85% with Kimi K2 (baseline 52.12%)

### Practitioner takeaways

- Separate facts, experiences, and procedures as distinct memory types
- Keep provenance between skills and source experiences
- Use failure as retrieval feedback (missing connection vs distractor vs
  wrong granularity)
- Let memory granularity change post-storage
- Measure the cost of evolution — adaptive memory can spend more on
  refining than it saves
