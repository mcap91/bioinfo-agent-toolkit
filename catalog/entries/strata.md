---
name: strata
title: Strata
url: "https://github.com/Niko1221/Strata"
category: framework
summary: "One-click inference engine for Qwen3.8-Flash-Next (125B MoE) on consumer NVIDIA GPUs (12-24GB) — expert offloading between GPU/RAM/SSD, speculative decoding via built-in MTP, 60-95 t/s on RTX 5070; multi-GPU pipeline, OpenAI/Anthropic-compatible API, vision support, browser UI with live monitor; built on ggml; MIT"
tags: [local-inference, qwen, moe, expert-offloading, speculative-decoding, one-click, nvidia, cuda, openai-compatible, consumer-gpu]
reviewed: 2026-09-29
acquired: 2026-09-29
supersedes: []
overlaps: [llama-cpp-adaptive-kv-streaming, qwen38-27b-200k-on-16gb]
license: MIT
security_flags: []
workflows: []
---

## What it does

Strata runs Qwen3.8-Flash-Next (125B parameters, 6B active per token, 24,576 experts) on a consumer gaming PC. It shares work across GPU, RAM, and SSD: the GPU handles per-token computation and caches hot experts, RAM holds all experts for CPU fallback, and the SSD stores the 29GB engram lookup table with small row reads per token. GPU and CPU work in parallel so neither waits.

Key capabilities:

- **Expert offloading**: only ~10 of 24,576 experts needed per token. GPU keeps the most-requested experts and learns which ones to retain during use.
- **Speculative decoding**: built-in MTP helper guesses next words, big model verifies in one pass — 1.6-1.8x speedup with identical output quality.
- **One-click install**: `START-HERE.bat` (Windows) or `./setup.sh` (Linux) handles Python, engine, and model download (~70GB). Calibration mode optimizes for specific hardware.
- **Multi-GPU**: pipeline parallelism across 2-3 NVIDIA cards (RTX 20+, 8GB+ each). 18-20% faster prompt processing on dual-GPU vs single.
- **API compatibility**: OpenAI (`/v1`) and Anthropic (`/v1/messages`) endpoints on localhost:8080. Thinking mode (off/low/medium/high).
- **Vision**: optional image input support.
- **AMD HIP**: experimental Radeon RX 7900 XT/XTX support on Linux.

## Mechanical details

Performance on RTX 5070 (12GB), Ryzen 5 7600, 64GB RAM:

| Quant | Decode (short) | Decode (128K) | Prompt (32K) | RAM needed |
|-------|---------------|---------------|-------------|-----------|
| Q2_0 | 93 t/s | 74 t/s | 2,170 t/s | 37.6 GB |
| IQ2_XS | 79 t/s | 63 t/s | 2,090 t/s | 39.2 GB |
| IQ3_XXS | 62 t/s | 49 t/s | 1,750 t/s | 47.0 GB |
| IQ3_S | 53 t/s | 46 t/s | 1,620 t/s | 54.8 GB |

Also supports ISTA-DASLab Coder variant (half experts pruned, 91% SWE-bench Verified score, fits 32GB RAM) and Swift 1.5 fine-tune (shorter thinking). Built on ggml (from llama.cpp). Ideas from Splash, ninfer, HyperQwen.

## Security

MIT licensed. Runs entirely local — no telemetry, no cloud calls. Model files carry their own licenses (Qwen Community License 1.0 for original). Listens on localhost by default; `--host 0.0.0.0` exposes the API with user-specified `--api-key`.