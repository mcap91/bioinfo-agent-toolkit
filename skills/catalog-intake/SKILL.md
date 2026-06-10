---
name: catalog-intake
description: Pull links into the catalog inbox (Gmail scan, chat paste), curate, and drain to the queue. Use when adding tools to the catalog or processing saved links.
---

# Catalog intake

1. **Gather** (interactive only):
   - Gmail: search `from:me subject:catalog` (primary). If `config.json` `gmail_fallback` is true,
     also `from:me newer_than:7d` filtered to github.com / reddit.com / instagram.com.
   - Extract URLs from message bodies; capture prose bodies as fenced ```text blocks with a
     `source:` line. Append all to `catalog/inbox.md`.
2. **Curate** `catalog/inbox.md` with the user: delete junk; for any `⚠ needs-link` item
   (Instagram, LinkedIn posts, X, paywalled), open it and replace it with the real fetchable
   URL or paste the relevant prose as a ```text block.
3. **Drain:** call the `drain {}` MCP tool — it ingests ready items and leaves blocked ones marked.
4. Report what was ingested, blocked, and skipped. Processing (assessment) is a separate step.
