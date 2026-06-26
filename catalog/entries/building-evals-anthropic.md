---
name: building-evals-anthropic
title: Building Evals (Anthropic Cookbook)
url: "https://platform.claude.com/cookbook/misc-building-evals"
category: agent-pattern
tags: [evaluation, grading, testing, claude, llm-ops]
summary: ">-"
security_flags: []
reviewed: 2026-06-25
acquired: 2026-06-26
---

## What it does

Walks through the structure and grading approaches for offline LLM evaluations. Evals have four parts: an input prompt, model output, a golden answer, and a score. Three grading methods are covered:

- **Code-based grading** — exact match or regex against structured outputs; fastest and most reliable when the eval can be designed for it.
- **Human grading** — a human compares output to golden answer; most capable but slowest and most expensive.
- **Model-based grading** — Claude grades its own outputs against golden answers via a grader prompt; nearly as capable as human grading at a fraction of the cost.

Key design heuristics: prefer higher volume over higher quality questions, structure questions to enable automated grading (e.g. reformatting as multiple choice), and match eval distribution to real-world query distribution.

## Why it matters

Offline eval quality directly determines whether prompt changes, model upgrades, or system changes improve or regress production accuracy. The model-based grading pattern is particularly relevant for agent workflows where output is free-form and code-based grading is insufficient.