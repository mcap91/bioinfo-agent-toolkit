---
name: unsloth
title: Unsloth
url: "https://github.com/unslothai/unsloth"
category: framework
summary: "LLM fine-tuning and inference framework — trains 500+ models up to 2x faster with 70% less VRAM via custom Triton kernels; Unsloth Studio web UI for running/training text, audio, vision, embedding models; supports LoRA, full fine-tune, RL (GRPO), FP8, pretraining; GGUF/safetensors export; NVIDIA/AMD/Intel/Apple Silicon; API endpoint for Claude Code/Codex integration; Apache 2.0 (core) + AGPL-3.0 (Studio UI)"
tags: [fine-tuning, lora, rl, grpo, quantization, gguf, local-inference, training, vram-optimization, triton]
workflows: []
reviewed: 2026-07-06
acquired: 2026-07-06
license: Apache-2.0
security_flags: []
supersedes: []
overlaps: [axolotl, llamafactory, trl]
---

## What it does

Framework for fine-tuning and running LLMs with custom Triton and mathematical kernels that reduce VRAM usage by up to 70% and increase training speed by up to 2x with no accuracy loss. Two interfaces: Unsloth Core (Python library) and Unsloth Studio (web UI).

### Training capabilities

- **Fine-tuning methods** — LoRA, full fine-tuning, 4-bit, 16-bit, FP8
- **Reinforcement learning** — GRPO with 80% less VRAM, advanced batching for 7x longer context RL
- **Pretraining** — supports 500K+ context training on 80GB GPUs for 20B models
- **Data Recipes** — auto-create datasets from PDF, CSV, DOCX in visual-node workflow editor
- **Model export** — GGUF, 16-bit safetensors, and other formats
- **MoE optimization** — 12x faster MoE training with 35% less VRAM (DeepSeek, GLM, Qwen, gpt-oss)
- **Embedding fine-tuning** — 1.8–3.3x faster
- **Multi-GPU** — supported, with improvements in progress

### Inference

- Search, download, and run models (GGUF, LoRA adapters, safetensors)
- Tool calling with self-healing, web search, code execution in sandbox
- API inference endpoint deployable as backend for Claude Code and Codex
- Chat with images, audio, PDFs, code, DOCX
- Connect to external providers (OpenAI, Anthropic) or servers (vLLM, Ollama)

### Unsloth Studio (web UI)

- Live training observability — loss, GPU usage, customizable graphs
- Visual data recipe editor
- In-UI model search and management
- Remote access via Cloudflare HTTPS tunnel (`--secure`)

## Differentiators

- **Custom Triton kernels** — hand-written kernels (RoPE, MLP, padding-free packing) rather than wrapping standard HF training loops
- **VRAM efficiency** — consistently 50–80% less VRAM across model families (Gemma 4, Qwen3.5, gpt-oss, Llama 3)
- **Upstream model fixes** — works directly with Qwen, Llama, Mistral, Gemma, Phi teams to fix accuracy bugs
- **API endpoint for coding agents** — local LLMs deployable as backends for Claude Code and Codex

## Mechanical details / What to adopt

- Install Studio: `curl -fsSL https://unsloth.ai/install.sh | sh` (macOS/Linux/WSL), `irm https://unsloth.ai/install.ps1 | iex` (Windows)
- Install Core: `uv pip install unsloth --torch-backend=auto` (requires Python 3.13, uv)
- Launch Studio: `unsloth studio -p 8888`
- Docker: `unsloth/unsloth` image with GPU support
- Hardware: NVIDIA RTX 30/40/50, Blackwell, DGX Spark; macOS (MLX + GGUF); AMD (chat + data, training via Core); Intel (guide available)
- GGUF-only mode: `UNSLOTH_NO_TORCH=1` skips PyTorch install

## Security

Apache 2.0 (core library), AGPL-3.0 (Studio UI). Studio binds to localhost by default. `--secure` mode uses free Cloudflare tunnel (fails closed if tunnel can't start). Server-side tools (web search, Python/terminal execution) run as the current user — anyone with the API key can execute code. `--disable-tools` flag available when exposing Studio. Installer uses `curl | sh` (standard pipe-to-shell risk).