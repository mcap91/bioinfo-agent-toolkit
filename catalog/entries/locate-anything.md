---
name: locate-anything
title: "LocateAnything"
url: https://research.nvidia.com/labs/lpr/locate-anything/
category: framework
verdict: watch
verdict_reason: "novel parallel box decoding for vision-language grounding; 3B model on HuggingFace; evaluate for spatial/histology image analysis when pipeline matures"
tags: [vision, grounding, object-detection, nvidia, spatial, histology, image-analysis]
workflows: [spatial]
reviewed: 2026-05-27
acquired: 2026-05-27
supersedes: []
overlaps: []
---

## What it does

A unified vision-language grounding model from NVIDIA that predicts bounding boxes and point coordinates for visual grounding and object detection tasks. The key innovation is Parallel Box Decoding (PBD) — predicting complete bounding boxes as atomic units in a single forward pass rather than sequential token generation, achieving 12.7 boxes per second (10x faster than Qwen3-VL's textual approach). Architecture: Moon-ViT vision encoder with Qwen2.5 language decoder connected via MLP projector. Three inference modes: Fast Mode (MTP) for speed, Slow Mode (NTP) for precision, and Hybrid Mode that detects format irregularities and falls back to autoregressive generation. Handles general object detection, GUI element grounding, referring expression comprehension, OCR localization, layout understanding, and point-based localization. 3B parameter model.

## Why this verdict

Potentially relevant for spatial transcriptomics workflows — grounding arbitrary text descriptions to regions in H&E or fluorescence images. The model is available on HuggingFace (`nvidia/LocateAnything-3B`) with an interactive demo, and code is on GitHub (`NVlabs/Eagle/tree/main/Embodied`). However, this is a general-purpose vision-language model, not trained on histology or biomedical images. The blocker is evaluating whether it generalizes to tissue morphology and cell-type localization tasks without fine-tuning. Dataset listed as "incoming" suggests the project is still maturing.

## Mechanical details

Model: `huggingface.co/nvidia/LocateAnything-3B`. Code: `github.com/NVlabs/Eagle/tree/main/Embodied`. Demo: `huggingface.co/spaces/nvidia/LocateAnything`. Paper: arXiv:2605.27365 (Wang et al., 2026). Pilot trigger: when spatial transcriptomics pipeline includes an image grounding step, evaluate on a representative H&E image with tissue-type text queries.
