---
name: microsoft-eval-guide
title: Microsoft Eval Guide
url: "https://github.com/microsoft/eval-guide"
category: plugin
tags: [evaluation, testing, claude-code-plugin, copilot, copilot-studio, microsoft, agent-eval, test-generation]
reviewed: 2026-07-21
summary: ">-"
acquired: 2026-07-22
---

## What it does

A plugin providing six skills that walk through a five-stage evaluation
lifecycle for AI agents built on Microsoft Copilot Studio. Grounded in
Microsoft's Practical Guidance on Agent Evaluation — a 10-step playbook.

### Skills

- **/eval-guide**: full eval lifecycle — discover, plan, generate, run,
  interpret
- **/eval-suite-planner**: populated Eval Suite Template workbook + HTML
  review page for eval sets, methods, gates, human inputs
- **/eval-generator**: test cases for single-response and conversation
  (multi-turn) evaluation modes; outputs Copilot Studio-importable CSV
- **/eval-result-interpreter**: SHIP/ITERATE/BLOCK verdict with root-cause
  classification
- **/eval-triage-and-improvement**: interactive diagnosis and remediation
  for failing evals
- **/eval-faq**: methodology questions answered from Microsoft's eval
  ecosystem

### Five stages

0. **Discover**: articulate agent purpose, success criteria, risk tier
1. **Plan**: scope eval depth by architecture, set pass-rate targets/gates
2. **Generate & Baseline**: produce test-case CSVs or conversation
   blueprints; design regression partition
3. **Run**: execute baseline against a live agent (requires running agent)
4. **Interpret & Improve**: triage results, gate-based verdict, optimization
   loop

Stages 0–2 work from just an agent description — no running agent required.

### Architecture-aware scoping

Automatically adjusts evaluation depth based on agent architecture:
prompt-level (response quality, tone, boundaries), RAG/knowledge-grounded
(adds retrieval accuracy, grounding, hallucination prevention), or agentic
(adds tool selection, action correctness, error recovery, task completion).

### Interactive dashboards

Each stage generates a standalone HTML dashboard (zero dependencies, served
by a Python script) for inline review and editing. Feedback auto-saves via
localStorage. Final deliverables (.docx, .csv) are generated only after
dashboard confirmation.

### Installation

Claude Code: `claude plugin marketplace add microsoft/eval-guide`.
GitHub Copilot: `npx skills add microsoft/eval-guide`. Optional companion
plugin `skills-for-copilot-studio` enables live agent connection via
DirectLine API.
