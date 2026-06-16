---
name: catalog-intake
description: Full catalog pipeline — Gmail pull, inbox curation, drain, and headless processing. Use when adding tools to the catalog or processing saved links.
---

# Catalog intake + processing

## Stage 1 — Intake (interactive)

1. **Read cursor:** call `config { action: "get-state" }` to read `gmail_last_pull_iso`. This is the
   timestamp of the last successful Gmail pull. Use it to scope the search (step 2).
2. **Gather:**
   - Gmail: search `from:me subject:catalog after:{date from cursor, YYYY/MM/DD}` (primary).
     If `config.json` `gmail_fallback` is true, also `from:me newer_than:7d` filtered to
     github.com / reddit.com / instagram.com.
   - Extract URLs from message bodies; capture prose bodies as fenced ```text blocks with a
     `source:` line. Append all to `catalog/inbox.md`.
3. **Update cursor:** call `config { action: "set-state", key: "gmail_last_pull_iso", value: "<now ISO>" }`
   with the current UTC timestamp. Do this **after** successfully appending to inbox, not before.
4. **Curate** `catalog/inbox.md` with the user: delete junk; for any `⚠ needs-link` item
   (Instagram, Reddit `/s/` share links, LinkedIn posts, X, paywalled), replace with the real
   fetchable URL or paste the relevant prose as a ```text block.
5. **Drain:** call the `drain {}` MCP tool. It ingests ready items into the queue and marks
   unfetchable items `⚠ needs-link` (blocked domains, Reddit `/s/` share links). Those stay in
   inbox until the user resolves them.
6. Report what was ingested, blocked, and skipped.

## Stage 2 — Processing (headless)

Run the headless pipeline to assess every queued item and write catalog entries:

```
npm run -w @catalog/mcp catalog:process
```

Run this in the background. It launches `claude --print` with the catalog MCP server attached,
follows `catalog/recipe.md`, and processes every pending queue item unattended.

**What it does per item:** fetch URL → build research prompt → assess the tool → validate →
write entry to `catalog/entries/` → remove from queue. Items it can't fetch are parked.

**After it finishes:**
- Check `catalog/queue.json` — any `parked` or `error` items need manual attention.
- New entries are in `catalog/entries/`. Index is regenerated automatically.
- Commit the new entries and updated index.
