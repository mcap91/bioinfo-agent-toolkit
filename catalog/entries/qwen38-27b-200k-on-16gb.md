---
name: qwen38-27b-200k-on-16gb
title: Qwen 3.8 27B at 200K Context on 16GB VRAM (tutorial)
url: "https://huggingface.co/unsloth/Qwen3.8-27B-GGUF"
category: agent-pattern
summary: "Practitioner recipe for running Qwen 3.8 27B UD-IQ4_XS at ~196K context and 50 t/s on a single RTX 5070 Ti (16GB) — prune non-ASCII rows from the embedding table and LM head (~700MB, ASCII-condensed variant published), offload the embedding table to CPU, disable MTP, use adaptive-KV streaming (llama.cpp fork) to page KV cache from host RAM, and quantize cache Q8 K / Q4 V"
tags: [qwen, local-inference, llama-cpp, quantization, kv-cache, long-context, vram-optimization, gguf, unsloth, embedding-pruning]
workflows: []
reviewed: 2026-09-10
acquired: 2026-09-10
license: LicenseRef-forum-content
security_flags: [community-modified-weights]
supersedes: []
overlaps: [kv-cache-vram-sizing, qwen3-8-27b-uncensored-hauhaucs-aggressive-gguf]
---

## What it says

A tutorial post for fitting Qwen 3.8 27B with ~196K tokens of context on a 16GB consumer GPU (RTX 5070 Ti, Ryzen 7 9700X, Windows 11) at ~50 t/s, stacking five techniques:

1. **Base quant:** Unsloth's UD-IQ4_XS GGUF of Qwen3.8-27B.
2. **Embedding/LM-head pruning:** since Qwen3.8 reasons exclusively in English unless prompted otherwise and the workload is English + code, prune most non-ASCII rows from the embedding table and LM head, saving ~700MB (author published the result as `bsaleh03/Qwen3.8-27B-ASCII-Condensed`).
3. **CPU-offload the embedding table** (`-ot "token_embd.weight=CPU"`): another 270MB of VRAM freed.
4. **Disable MTP** (keep the multi-token-prediction head off the GPU), leaving 3.6GB for context — 84K tokens natively.
5. **Adaptive-KV streaming:** a llama.cpp fork (`RaymondHuang210129/llama.cpp-adaptive-kv-streaming`) pages the KV cache and streams it from host RAM at some depth-performance cost; with Q8 K-cache and Q4 V-cache quantization this reaches 196,608 tokens.

Full args: `-ngl 99 -fa on -ctk q8_0 -ctv q4_0 -np 1 -ub 128 -b 512 -ot "token_embd.weight=CPU" --jinja`.

## Key takeaways

- Vocabulary pruning is an unusual lever: when the workload is ASCII-only, the multilingual embedding rows are dead weight recoverable as context budget.
- The stack is composable — each step is independent (quant, prune, offload, MTP off, KV paging), so partial adoption is possible on other hardware.
- KV paging trades throughput at depth for context length; the 50 t/s figure is at the author's settings, not at full 196K depth.

## What to adopt

- The exact llama.cpp argument set for 16GB-class GPUs running 27B models long-context.
- The ASCII-condensed pruning idea generalizes to any English/code-only local deployment.

## Security

- `community-modified-weights` — both the pruned model and the adaptive-KV llama.cpp fork are individual community artifacts without upstream review; weights modified by a third party warrant verification against the base model before trust-sensitive use.
- Forum tutorial; performance numbers are the author's single-machine reports.