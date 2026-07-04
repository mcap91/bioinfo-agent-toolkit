---
name: agentic-rag
title: Agentic RAG
url: "https://huggingface.co/learn/cookbook/agent_rag"
category: agent-pattern
tags: [RAG, retrieval, agents, smolagents, vector-search, self-query]
reviewed: 2026-07-03
security_flags: []
summary: ">-"
acquired: 2026-07-03
---

## What It Does

Agentic RAG wraps a vector-database retriever as a tool available to an LLM agent. Instead
of embedding the user's raw question for a single retrieval pass, the agent:

1. **Reformulates the query** into affirmative-form statements closer to the target
   documents (recovering the HyDE technique)
2. **Critiques retrieved snippets** and re-retrieves with different queries if the initial
   results are insufficient (recovering Self-Query)
3. **Iterates** through multiple retrieval rounds before synthesizing a final answer

## Reference Implementation

The HuggingFace cookbook (by Aymeric Roucher) demonstrates the pattern using:

- **smolagents** `ToolCallingAgent` with a custom `RetrieverTool`
- **LangChain** `FAISS` vector store with `RecursiveCharacterTextSplitter`
- **HuggingFace Inference API** for both the agent LLM and embedding model
- Evaluation via LLM-as-judge on the `m-ric/huggingface_doc_qa_eval` dataset

## Key Insight

The agent's ability to reformulate queries in affirmative form (rather than questions) and
to re-retrieve on unsatisfactory results recovers advanced RAG techniques automatically,
without explicit retrieval pipeline engineering.

## Links

- HuggingFace Cookbook: https://huggingface.co/learn/cookbook/agent_rag
- smolagents RAG example: https://huggingface.co/docs/smolagents/en/examples/rag
- HuggingFace Agents Course: https://github.com/huggingface/agents-course