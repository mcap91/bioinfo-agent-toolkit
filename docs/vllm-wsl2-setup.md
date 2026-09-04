# Serving vLLM on WSL2 with GPU Passthrough (RTX 5080)

Tested 2026-09-02 with vLLM 0.28.0, Driver 610.47, CUDA 13.3, RTX 5080 16GB Laptop GPU, Windows 11.

## Prerequisites

1. **NVIDIA driver** installed on Windows (610.x+ for CUDA 13.3)
2. **WSL2** with GPU passthrough working (`wsl nvidia-smi` shows your GPU)
3. **Miniforge/Mamba** installed inside WSL2

Verify GPU passthrough:

```bash
# Windows
nvidia-smi

# WSL2
wsl nvidia-smi
```

Both should show the same GPU.

## WSL2 system packages

vLLM's Triton JIT compilation needs a C compiler:

```bash
sudo apt update && sudo apt install -y gcc
```

## Create the mamba env

```bash
mamba create -n olmocr-vllm python=3.11 -y
mamba activate olmocr-vllm
pip install vllm
```

## Serve

vLLM 0.28.0 on WSL2 requires three workarounds:

| Issue | Error | Fix |
|-------|-------|-----|
| V2 Model Runner requires UVA | `RuntimeError: UVA is not available` | `VLLM_USE_V2_MODEL_RUNNER=0` |
| Triton needs gcc | `RuntimeError: Failed to find C compiler` | `sudo apt install gcc` |
| FlashInfer needs nvcc | `RuntimeError: Could not find nvcc` | `VLLM_USE_FLASHINFER_SAMPLER=0` |

Additionally, `--max-model-len` must be capped for 16GB cards (default 128k OOMs).

```bash
export VLLM_USE_V2_MODEL_RUNNER=0
export VLLM_USE_FLASHINFER_SAMPLER=0
vllm serve {MODEL_ID} --max-model-len 16384
```

Wait for `Application startup complete` (first run: ~90s for compilation + CUDA graph capture; subsequent runs: ~30s with cached kernels).

The server listens on `http://0.0.0.0:8000` and is accessible from Windows at `http://localhost:8000`.

### Example: olmOCR

```bash
export VLLM_USE_V2_MODEL_RUNNER=0
export VLLM_USE_FLASHINFER_SAMPLER=0
vllm serve allenai/olmOCR-2-7B-1025-FP8 --max-model-len 16384
```

From a Windows terminal (with the `pdf-ocr-bench` or any env that has `olmocr` installed):

```
olmocr {OUTPUT_DIR} --server http://localhost:8000/v1 --model allenai/olmOCR-2-7B-1025-FP8 --markdown --pdfs {PDF_PATH}
```

### Choosing --max-model-len

The model weights take ~9.5 GiB on a 16GB card. Remaining VRAM goes to KV cache, CUDA graphs, and activation memory.

| --max-model-len | KV cache | Notes |
|-----------------|----------|-------|
| 4096 | ~1.75 GiB | Too small for olmocr (hardcodes max_tokens=8000) |
| 16384 | ~1.75 GiB, 32k tokens capacity | Works for olmocr; ~7.98x concurrency at 4096 tok/req |
| 128000 (default) | OOM | Encoder profiling exceeds 16GB |

## Model cache

First run downloads model weights to the HuggingFace cache inside WSL2:

```
~/.cache/huggingface/hub/models--{org}--{model}/
```

For `allenai/olmOCR-2-7B-1025-FP8`, this is ~9.4 GB.

To clean up:

```bash
rm -rf ~/.cache/huggingface/hub/models--allenai--olmOCR-2-7B-1025-FP8/
```

Or interactively review all cached models:

```bash
pip install huggingface-hub
huggingface-cli delete-cache
```

## Upstream status

These WSL2 issues are tracked in vLLM's GitHub:

- [#50239](https://github.com/vllm-project/vllm/issues/50239) UVA crash on RTX 5050 (sm_120)
- [#54652](https://github.com/vllm-project/vllm/issues/54652) GPUModelRunnerV2 hard-requires UVA (0.28.1rc1)
- [PR #47579](https://github.com/vllm-project/vllm/pull/47579) Proposed fix: fall back to V1 model runner when UVA unavailable (open, unmerged)

Once PR #47579 merges, `VLLM_USE_V2_MODEL_RUNNER=0` should no longer be needed. The FlashInfer/nvcc issue would be resolved by installing the CUDA Toolkit in WSL2 (`sudo apt install nvidia-cuda-toolkit`, ~3-4 GB), but the env var workaround avoids that.
