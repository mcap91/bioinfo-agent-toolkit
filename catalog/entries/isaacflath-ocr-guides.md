---
name: isaacflath-ocr-guides
title: Isaac Flath — Documents in AI Products (OCR Pipeline Guides)
category: reference
summary: "14-post blog series covering OCR model selection, VLM OCR, speculative decoding, PDF retrieval, chunking, quantization, and document QA — practical guidelines for designing OCR pipelines"
tags: [ocr, vlm, retrieval, chunking, quantization, colbert, rag, document-processing, pdf]
workflows: [ocr-bench]
reviewed: 2026-09-03
acquired: 2026-09-03
supersedes: []
license: n/a
security_flags: []
overlaps: [ovisocr2, opendataloader-pdf]
---

## What it does

Three blog series by Isaac Flath (isaacflath.com) covering the full document-AI pipeline: reading documents (OCR model selection, VLM architectures, speculative decoding, failure modes), searching documents (BM25, dense/multivector retrieval, ColBERT quantization, late chunking, reranking), and using documents (citation-grounded QA, RLM agent architecture). Includes benchmark comparisons of OCR models, retrieval methods, and cost/latency tradeoffs.

## Assessment

Directly applicable to OCR pipeline design. Covers the decision matrix for self-host vs API, open pipeline vs VLM, and cost tradeoffs at scale. The retrieval posts inform chunking and search strategy downstream of OCR. Written by a practitioner (talks feature Joe Barrow from Adobe Document Intelligence Lab). Content is opinionated and grounded in production experience at Pattern Data (~7M pages of local laws, hundreds of millions of document pages).

## Mechanical details

Source: isaacflath.com, API at `/api/posts`. Full verbatim content archived locally:

- `catalog/sources/isaacflath/reading-documents.md` — Speculative Decoding, OCR Examples Gallery, How to Choose an OCR Model, VLM OCR for Hard Documents
- `catalog/sources/isaacflath/searching-documents-1.md` — What Actually Improves PDF Retrieval, Query Disambiguation, Quantization for ColBERT, RAG Context Problem
- `catalog/sources/isaacflath/searching-documents-2.md` — mgrep, Keyword Search, Late Chunking, Retrieval 101
- `catalog/sources/isaacflath/using-documents.md` — Document Answers You Can Check, How My RLM Tool Works

Key models/tools discussed: Chandra 2, Surya, LightOnOCR-2, PaddleOCR, MonkeyOCR, GLM-OCR, AWS Textract, Gemini 3.5 Flash, Mixedbread Wholembed, ColBERT, Jina, Voyage, vLLM, Modal.

## Security

Blog content, no code execution. Source files are local archival copies for personal reference.
