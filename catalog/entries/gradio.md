---
name: gradio
title: Gradio
url: "https://gradio.app/"
category: framework
tags: [python, machine-learning, UI, demo, web-app, huggingface]
reviewed: 2026-07-03
security_flags: []
summary: ">-"
acquired: 2026-07-03
---

## What It Does

Gradio lets developers create interactive web UIs for machine learning models, APIs, or
arbitrary Python functions in a few lines of code. It handles the frontend automatically —
no JavaScript, CSS, or web hosting experience required. Users interact through the browser
while Python functions run on the backend.

## Core Abstractions

- **gr.Interface**: high-level class for models with defined inputs and outputs — wraps a
  function with UI components automatically
- **gr.ChatInterface**: purpose-built chatbot UI that wraps a conversational function
- **gr.Blocks**: low-level layout API for custom multi-step workflows, conditional
  visibility, and complex data flows — still pure Python

## Architecture

FastAPI serves the backend API endpoints; a Svelte single-page app handles the frontend.
When a user triggers an action, the frontend sends an HTTP request to the FastAPI backend,
which runs the Python function and returns JSON. Supports queuing, streaming, and
ZeroGPU integration.

## Ecosystem

- **gradio_client** (Python) and **@gradio/client** (JavaScript): programmatic API clients
  for any Gradio app
- **Hugging Face Spaces**: free hosting with auto-scaling
- **gradio.Server**: headless backend mode for fully custom frontends
- **Share links**: `demo.launch(share=True)` creates a temporary public URL tunneled to localhost

## Links

- GitHub: https://github.com/gradio-app/gradio
- Docs: https://gradio.app/docs
- Quickstart: https://gradio.app/guides/quickstart