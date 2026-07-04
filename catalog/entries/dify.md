---
name: dify
title: Dify
url: "https://github.com/langgenius/dify"
category: framework
tags: [LLM-platform, workflow, RAG, agents, LLMOps, self-hosted, visual-builder]
reviewed: 2026-07-03
security_flags: []
summary: ">-"
acquired: 2026-07-04
---

## What It Does

Dify provides an intuitive visual interface for building AI applications — from chatbots
to complex multi-step agent workflows. It combines workflow orchestration, RAG document
ingestion/retrieval, agent tool use, model management, and production observability into
a single platform.

## Key Features

- **Visual workflow canvas**: drag-and-drop AI workflow builder with branching, loops,
  and conditional logic
- **RAG pipeline**: document ingestion (PDF, PPT, etc.), chunking, embedding, and
  retrieval — all configurable through the UI
- **Agent capabilities**: Function Calling or ReAct agents with 50+ built-in tools
  (Google Search, DALL-E, Stable Diffusion, WolframAlpha)
- **Model support**: hundreds of LLMs from dozens of providers plus self-hosted models;
  any OpenAI API-compatible model works
- **Prompt IDE**: prompt crafting, model comparison, and text-to-speech in one interface
- **LLMOps**: log monitoring, performance analysis, prompt/dataset iteration based on
  production data
- **Backend-as-a-Service**: every feature exposed via API for integration into custom
  applications
- **Observability**: integrations with Opik, Langfuse, and Arize Phoenix

## Deployment

- **Docker Compose**: `docker compose up -d` with `.env` configuration
- **Kubernetes**: community Helm charts and YAML manifests
- **Cloud**: managed Dify Cloud with free tier (200 GPT-4 calls)
- **AWS/Azure/GCP**: Terraform and CDK deployment options
- **Enterprise**: additional features for organizations

## Links

- GitHub: https://github.com/langgenius/dify
- Docs: https://docs.dify.ai/
- Cloud: https://cloud.dify.ai/