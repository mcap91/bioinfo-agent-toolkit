---
name: paddleocr
title: PaddleOCR
url: "https://github.com/PaddlePaddle/PaddleOCR"
category: framework
summary: ">"
tags: [ocr, document-parsing, vision-language-model, multilingual, pdf-extraction, text-recognition, table-recognition, rag, paddlepaddle]
reviewed: 2026-09-02
acquired: 2026-09-02
supersedes: []
overlaps: []
license: Apache-2.0
security_flags: []
workflows: []
---

## What it does

PaddleOCR provides three product lines for document understanding:

### PP-OCRv6 (Scene OCR)
Universal text recognition for natural scenes — IDs, street views, books, industrial
components. Three model tiers: tiny (1.5M params), small (7.7M), medium (34.5M). Single
unified model covers Chinese, English, Japanese, and 46 Latin-script languages. 5.2x CPU
inference speedup over v5.

### PP-StructureV3 (Document Structure)
Converts complex PDFs and images into Markdown or JSON with fine-grained coordinate
information including table cell coordinates, text coordinates, and layout regions.

### PaddleOCR-VL (Vision-Language Model)
0.9B parameter VLM for document parsing — 96.3% accuracy on OmniDocBench v1.6. Handles
text, formulas, tables, charts, ancient documents, rare characters, and seals. Supports
109 languages. Structured output in Markdown and JSON.

## Deployment

- **Inference backends:** PaddlePaddle, ONNX Runtime, OpenVINO, TensorRT
- **Hardware:** NVIDIA GPU, Intel CPU, Kunlunxin XPU, Apple M-series, NVIDIA RTX 50 series
- **SDKs:** Python, C++, C#, Java, browser (PaddleOCR.js)
- **Serving:** Docker-based high-stability service deployment

## Ecosystem Integration

Deeply integrated with Dify (agentic workflows), RAGFlow (RAG engine), Pathway (ETL),
Cherry Studio (LLM client), Haystack (AI orchestration), and OmniParser (GUI agents).