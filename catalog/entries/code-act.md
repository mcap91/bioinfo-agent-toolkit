---
name: code-act
title: CodeAct
url: "https://github.com/xingyaoww/code-act"
category: agent-pattern
tags: [agent-framework, code-execution, LLM-agents, python, research-paper]
reviewed: 2026-07-03
security_flags: []
summary: ">-"
acquired: 2026-07-03
---

## What It Does

CodeAct proposes using executable Python code as a unified action space for LLM agents.
Integrated with a Python interpreter, agents can execute code actions and dynamically
revise prior actions or emit new actions based on execution results through multi-turn
interactions. This replaces constrained JSON or text-based action formats with the full
expressiveness of Python, enabling tool composition, control flow, and dynamic
self-debugging.

## Key Components

- **CodeAct action space**: agents emit Python code that is executed in a sandboxed
  interpreter, with stdout/stderr fed back as observations
- **CodeActInstruct**: 7k multi-turn interaction dataset for instruction-tuning agents
  on the CodeAct paradigm
- **CodeActAgent**: fine-tuned models (Llama2, Mistral) that use CodeAct for autonomous
  task execution including model training and self-debugging
- **M3ToolEval benchmark**: evaluation suite for multi-tool, multi-step agent tasks

## Ecosystem

CodeAct is the foundational agent architecture for OpenHands (formerly OpenDevin), which
adopted it as its default generalist agent. The CodeAct paradigm has been integrated into
Microsoft's Agent Framework (2026) and recognized in Apple ML Research (ACL 2026).

## Links

- Paper: https://arxiv.org/abs/2402.01030
- ICML proceedings: https://proceedings.mlr.press/v235/wang24h.html
- HuggingFace: https://huggingface.co/papers/2402.01030