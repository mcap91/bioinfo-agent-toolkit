---
name: google-knowledge-catalog
title: Google Cloud Knowledge Catalog
url: "https://github.com/GoogleCloudPlatform/knowledge-catalog"
category: framework
summary: "Google Cloud's Gemini-powered data catalog and metadata management platform (formerly Dataplex); builds a dynamic context graph of structured/unstructured data assets for AI agent grounding, with MCP server integration for context retrieval"
tags: [data-catalog, metadata, google-cloud, gemini, mcp, knowledge-graph, data-governance, ai-agents]
reviewed: 2026-07-12
acquired: 2026-07-12
supersedes: []
license: Apache-2.0
security_flags: [cloud-hosted, requires-gcp-auth]
workflows: [data-discovery, metadata-enrichment, agent-grounding]
overlaps: []
---

## What it is

Google Cloud Knowledge Catalog (rebranded from Dataplex Universal Catalog in April 2026) is a fully managed data cataloging and metadata management platform. It automatically harvests technical metadata from BigQuery, AlloyDB, Spanner, Cloud SQL, Firestore, Looker, and third-party systems, then uses Gemini to infer business semantics — generating natural language descriptions, discovering relationships, and proposing verified SQL patterns ("golden queries").

The GitHub repository (`GoogleCloudPlatform/knowledge-catalog`) contains tools, agents, and samples demonstrating how to build context management, enrichment, and retrieval solutions on top of the platform.

## Core capabilities

1. **Governance foundation.** Centralized business glossary, data quality checks, anomaly detection, and policy-based governance across the data estate.

2. **Context curation.** Gemini analyzes schemas, query logs, and semantic models to generate descriptions, discover relationships, and surface example queries capturing complex business logic.

3. **Context retrieval.** AI agents retrieve enriched context via semantic search and Model Context Protocol (MCP). Two MCP implementations: a remote MCP server for cloud-native/serverless, and a local MCP Toolbox for prototyping.

## MCP integration

Knowledge Catalog exposes its context graph through MCP, allowing AI agents to discover data assets and retrieve business context without custom integration code. This grounds agent reasoning in enterprise metadata, reducing hallucinations.

## Security

Requires GCP authentication and IAM configuration. The platform is fully managed (no self-hosted option). The GitHub samples repo is Apache-2.0 licensed. Third-party integrations (Ab Initio, Anomalo, Atlan, Collibra, Datahub) may have separate licensing. Data Catalog (the predecessor service) began phased shutdown June 1, 2026.