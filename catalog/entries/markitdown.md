---
name: markitdown
title: "MarkItDown"
url: https://github.com/microsoft/markitdown
category: cli-tool
verdict: pilot
verdict_reason: "directly useful for converting PDFs, Excel, PPTX, and other docs to markdown for LLM pipelines; MIT, Microsoft-maintained"
install: "pip install 'markitdown[all]'"
tags: [markdown, conversion, pdf, documents, excel, llm-preprocessing]
reviewed: 2026-05-27
supersedes: []
overlaps: []
---

## What it does

A lightweight Python utility from Microsoft that converts diverse file formats to Markdown for use with LLMs and text analysis pipelines. Supports PDF, PowerPoint, Word, Excel, images (with EXIF metadata and OCR), audio (with metadata and transcription), HTML, CSV, JSON, XML, ZIP files, YouTube URLs, and EPub. Preserves document structure — headings, lists, tables, and links. Offers both a CLI (`markitdown path-to-file.pdf > doc.md`) and a Python API. Optional integrations with Azure Document Intelligence for enhanced extraction and OpenAI-compatible clients for LLM-based image descriptions. Has a third-party plugin system for extended functionality.

## Why this verdict

No existing catalog entry covers file-to-markdown conversion. Directly useful for two common scenarios: (1) converting computational biology papers and supplementary PDFs into markdown for skill ingestion via Book to Skill or LLM context, and (2) converting Excel/CSV data files into structured markdown for pipeline documentation. MIT licensed, actively maintained by Microsoft, lightweight install. Pilot to verify quality of PDF table extraction on typical bioinformatics supplementary material before adopting broadly.

## Mechanical details

Install: `pip install 'markitdown[all]'` (the `[all]` extra pulls OCR and audio dependencies). CLI usage: `markitdown input.pdf -o output.md` or piped `cat input.pdf | markitdown`. Python API: `from markitdown import MarkItDown; md = MarkItDown(); result = md.convert("input.pdf")`. Docker image also available. Pilot test: convert a methods-heavy PDF with tables and check structural fidelity.
