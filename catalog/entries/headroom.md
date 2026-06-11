---
name: headroom
title: Headroom
url: "https://github.com/chopratejas/headroom"
category: framework
verdict: watch
verdict_reason: "Powerful context compression with real benchmarks, but proxy/MITM position and headroom learn's CLAUDE.md writes are significant trust risks for adoption without review"
tags: [context-compression, token-reduction, mcp-server, proxy, memory, agent-wrap, claude-code]
workflows: []
reviewed: 2026-06-10
acquired: 2026-06-10
license: Apache-2.0
security_flags: [mitm-proxy, agent-instructions-write, single-author, unvetted-ml-model]
supersedes: []
overlaps: [headroom-desktop, rtk-cli-proxy, context-graph-compressor]
---

## What it does

Headroom is a context compression layer that sits between an AI agent/app and the LLM provider, compressing tool outputs, logs, RAG chunks, files, and conversation history before they reach the model. Claims 60–95% token reduction with accuracy preserved on GSM8K, TruthfulQA, SQuAD v2, and BFCL benchmarks.

Deployment modes:
- **Library**: `compress(messages)` in Python or TypeScript, inline in any app
- **Proxy**: `headroom proxy --port 8787` — drop-in OpenAI-compatible proxy, zero code changes
- **Agent wrap**: `headroom wrap claude|codex|cursor|aider|copilot` — one-command wrapping
- **MCP server**: `headroom_compress`, `headroom_retrieve`, `headroom_stats` tools for any MCP client

Additional features:
- **Cross-agent memory**: shared store across Claude, Codex, Gemini with auto-dedup
- **headroom learn**: mines failed sessions and writes corrections to CLAUDE.md / AGENTS.md / GEMINI.md
- **CCR (reversible compression)**: originals stored locally; LLM retrieves via `headroom_retrieve` on demand
- **CacheAligner**: stabilizes prompt prefixes so provider KV caches (Anthropic, OpenAI) actually hit

Compression algorithms: SmartCrusher (JSON), CodeCompressor (AST-aware for Python/JS/Go/Rust/Java/C++), Kompress-base (HuggingFace ML model trained on agentic traces), image compression (40–90% via ML router).

## Why this verdict

Watch rather than pilot or adopt for several reasons:

1. **Proxy/MITM position**: The proxy and wrap modes sit in the critical path of all LLM traffic, including prompts containing secrets, credentials, and sensitive data. This is a significant trust boundary to cross without independent security review.

2. **`headroom learn` writes agent instructions**: The failure-mining feature writes directly to CLAUDE.md, AGENTS.md, and GEMINI.md. An externally controlled process modifying agent instruction files is a high-severity attack surface — a compromised or buggy Headroom instance could inject arbitrary instructions into all future agent sessions.

3. **Single-author repo**: Limited supply chain transparency; no signed releases observed; no multi-contributor review process evident from README.

4. **Unvetted ML model**: Kompress-base is a HuggingFace model trained on "agentic traces" with no described data governance, privacy guarantees, or independent evaluation of what the model has learned to compress away.

The benchmark results are credible in format and methodology is described (`python -m headroom.evals suite`), and the tool addresses a genuine need at scale. Worth monitoring for maturity signals (more contributors, signed releases, security audit) before adoption in production agent workflows.

## Mechanical details

Install: `pip install "headroom-ai[all]"` (Python 3.10+) or `npm install headroom-ai`. Granular extras: `[proxy]`, `[mcp]`, `[ml]`, `[code]`, `[memory]`, `[relevance]`, `[image]`, `[agno]`, `[langchain]`, `[evals]`.

Pipeline lifecycle: Setup → Pre-Start → Post-Start → Input Received → Input Cached → Input Routed → Input Compressed → Input Remembered → Pre-Send → Post-Send → Response Received.

SDK integrations: `withHeadroom(new Anthropic())`, `withHeadroom(new OpenAI())`, Vercel AI SDK middleware, LiteLLM callback, LangChain model wrapper, Agno model wrapper, Strands guide, ASGI middleware.

Bundles RTK binary for shell-output rewriting; can use lean-ctx as CLI context tool via `HEADROOM_CONTEXT_TOOL=lean-ctx`. Devcontainers provided with memory-stack variant (Qdrant + Neo4j).

Claude Code compatibility: `headroom wrap claude --memory --code-graph`. MCP install: `headroom mcp install`.

## Security

- **License**: Apache-2.0 — permissive, no copyleft obligations.
- **Proxy/MITM**: Modes that intercept all LLM traffic (`headroom proxy`, `headroom wrap`) require trusting the Headroom process with all prompts, tool outputs, and model responses. This includes any secrets or PII in context.
- **Agent instruction injection**: `headroom learn` writes to CLAUDE.md/AGENTS.md/GEMINI.md based on session analysis. A compromised or misbehaving Headroom instance could persistently modify agent behavior across all future sessions.
- **Cross-agent memory**: Shared memory store across agents has no described access controls or isolation model in the README.
- **ML model (Kompress-base)**: Trained on "agentic traces" — unclear what data, whether it memorizes sensitive content from training, or what it might selectively compress away from agent context.
- **Supply chain**: Single primary author (chopratejas), no signed releases visible, recent active repo. Tests exist (`pytest`), CI configuration present (devcontainers), contributing guide provided.
- **security_flags**: `mitm-proxy` (proxy intercepts all LLM traffic), `agent-instructions-write` (headroom learn modifies CLAUDE.md/AGENTS.md), `single-author` (limited review coverage), `unvetted-ml-model` (Kompress-base provenance unknown).
