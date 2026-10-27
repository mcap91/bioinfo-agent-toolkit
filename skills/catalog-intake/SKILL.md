---
name: catalog-intake
description: Full catalog pipeline — Gmail pull, inbox curation, drain, and headless processing. Use when adding tools to the catalog or processing saved links.
---

# Catalog intake + processing

## Stage 1 — Intake (interactive)

1. **Read cursor:** call `config { action: "get-state" }` to read `gmail_last_pull_iso`. This is the
   timestamp of the last successful Gmail pull. Use it to scope the search (step 2).
2. **Gather:**
   - Gmail: search `from:me subject:catalog after:{date from cursor, YYYY/MM/DD}`.
   - **Filter duplicates:** Gmail `after:` has only day-level granularity, so the search will
     return messages from earlier in the cursor day that were already processed. Compare each
     message's `date` against the cursor timestamp and discard any message dated at or before it.
   - Extract URLs from the remaining message bodies; capture prose bodies as fenced ```text
     blocks with a `source:` line. Append all to `catalog/inbox.md`.
3. **Update cursor:** call `config { action: "set-state", key: "gmail_last_pull_iso", value: "<now ISO>" }`
   with the current UTC timestamp. Do this **after** successfully appending to inbox, not before.
4. **Curate** `catalog/inbox.md` with the user: delete junk; for any `⚠ needs-link` item
   (Instagram, LinkedIn posts, X, paywalled), replace with the real fetchable URL or paste the
   relevant prose as a ```text block. Reddit post/share links need no manual link — the capture
   step (step 6) resolves them.
5. **Drain:** call the `drain {}` MCP tool. It ingests ready items into the queue and marks
   unfetchable items `⚠ needs-link` (blocked domains, Reddit post/share links). Those stay in
   inbox until the user resolves them or the capture step (step 6) does.
6. **Capture Reddit:** one-time setup if Chromium isn't already available to Playwright:
   `uv run --project packages/catalog-capture playwright install chromium`. Then, from the repo
   root, with nothing else writing the inbox concurrently:
   ```
   uv run --project packages/catalog-capture python -m catalog_capture needs-link --inbox catalog/inbox.md --sources catalog/sources
   ```
   Each `⚠ needs-link` Reddit line becomes a captured ```text block, `⚠ capture-failed <url> — <reason>`,
   or `⚠ pdf <url>`. A `capture-failed`/`pdf` line needs a manual reset (edit it back to
   `⚠ needs-link <url>`) before it will retry; same for a Reddit item returned from processing as
   `⚠ empty-fetch`/`⚠ fetch-error` — reset it to `⚠ needs-link <url>` to have this step recapture it.
7. **Drain again:** call `drain {}` once more — the only items still ready are the fenced blocks
   the capture step just wrote.
8. Report what was ingested, blocked, captured, and skipped.

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
