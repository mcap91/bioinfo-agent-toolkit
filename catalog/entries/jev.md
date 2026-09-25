---
name: jev
title: Jev (TypeSafe AI)
url: "https://typesafe.ai"
category: framework
summary: "Non-generative 'System One' classification model from TypeSafe AI — evaluates state and returns typed answers with calibrated probabilities (choice, score, noul/boolean) instead of generating text; trained with RLCD; reports up to 200x faster inference and 400x lower cost than LLMs on classification tasks; parallel multi-question evaluation per request; LangChain integration via langchain-typesafe; use cases include model routing, agent guardrails (auto-mode safety classification), and ticket triage"
tags: [classification, inference, llm-alternative, langchain, agent-routing, guardrails, model-routing, typesafe-ai]
workflows: []
reviewed: 2026-09-18
acquired: 2026-09-18
license: ""
security_flags: []
supersedes: []
overlaps: []
---

## What it does

Jev is a classification model (not an LLM) designed for fast, structured decisions in agent workflows. TypeSafe AI calls it a "System One" model — it evaluates a state and returns typed answers with calibrated probabilities, without generating text.

API: send a state (text, structured data, or LangChain messages) and one or more questions. Three question types:
- Choice: pick from a set of options; returns probability per option plus confidence
- Score: rate against ordered levels (low/medium/high); returns continuous score plus distribution plus confidence
- Noul: yes/no question; returns probability that a statement is true

All questions in a request evaluate in parallel — adding questions barely changes response time.

LangChain integration: langchain-typesafe package exposes TypeSafeClassifier with .invoke(). Experimental middleware:
- ModelRouterMiddleware: classifies request complexity and routes to appropriate model (fast vs powerful)
- AutoModeMiddleware: classifies tool calls for risk before execution, blocking dangerous actions

Reported performance: up to 200x faster inference and 400x lower cost compared to LLMs on classification tasks.

## Security

- API key required (TYPESAFE_API_KEY)
- Designed to replace LLM calls for classification/routing/guardrail decisions in agent pipelines

## Community analysis

- **Skeptic case (r/LocalLLaMA, Sep 2026):** Core claim is that Jev's "System One model" framing repackages known zero-shot/NLI classifier behavior with modern capabilities. BTZSC benchmark (ICLR 2026, 22 datasets) evaluates dozens of zero-shot classifiers; Jev not yet benchmarked against that landscape. One Banking77 experiment: BGE-small + logistic regression scored 93.3% vs 83.2% for Jev at ~9ms locally. "Can't hallucinate" framing acknowledged by TypeSafe to mean schema-constrained output, not empirically zero error. Counter: Jev's instruction-conditioned decision orientation (state + typed question + bounded options → probability distribution) differs from plain input → fixed label classification — the same model answers many different bounded questions without retraining.
- **Architecture clarification (r/AI_Agents):** Jev is closer to a Neural Decision Fabric than a classifier: `runtime state → deterministic eligibility/safety → Jev decision → deterministic validation → action → observe result`. Can operate throughout the agent loop (context admission, model routing, tool-result judgment, retry decisions, evidence ranking, completion assessment). Implementation may use one general decision model plus specialist models (e.g., one for abstaining when evidence is insufficient, another for forms/computer-use). Deterministic routing chooses which model to call — most decisions need zero or one neural inference.
