# bioinfo-agent-toolkit

<!-- BEGIN kb-managed -->
Managed by kb — edits inside this block are overwritten by `kb bootstrap` / `kb sync-contract`; edit outside the markers.

## kb integration

This repository uses the `kb` toolkit (repo-local wiki, reviewed dispatch, deterministic graph). The kb
MCP servers (`kb-wiki`, `kb-dispatch`) are registered in this repo's `.mcp.json` and run from the kb
checkout; every kb tool call targets this repository via `dir`.

### Retrieval — do this before substantive work

Repository-context retrieval is a wiki/docs retrieval problem first, not a filesystem-search problem first.

1. Search the wiki with the kb wiki MCP `search` tool. This is the first retrieval step.
2. If you need a structured overview, regenerate views with the MCP `generate` tool and read them
   (`catalog`, `now`, `inbox`, `backlog`, `archive`).
3. Then read the relevant durable `docs/` pages.
4. Then check related `wiki/decisions/`, `wiki/issues/`, `wiki/initiatives/`, `wiki/areas/`, `wiki/sources/`.
5. Only then inspect implementation files.

If the kb wiki MCP server is not available this session, run the same steps via the kb CLI from the kb
checkout (`npm run wiki -- search --dir <this repo>`, `npm run wiki -- generate --dir <this repo>`). Do
not use raw `rg`, file globbing, or direct file reads as the first retrieval step — use the wiki MCP tools
(`search`, `generate`, `lint`), or the CLI fallback, first. Do not parallelize implementation search with
the initial retrieval pass.

### Operating rules

- Wiki: prefer the `kb-wiki` MCP tools (`search`, `generate`, `lint`, `create`, `allocate-id`,
  `build-search-index`, `sync-contract`, `bootstrap`); CLI fallback `npm run wiki -- … --dir <this repo>`.
- Dispatch: prefer the `kb-dispatch` MCP tools or the kb CLI.
- Graph: kb CLI (`npm run graph -- --dir <this repo>`).
- Always pass `dir` pointing at this repository; run kb from its own checkout, not this repo root.
- Do not create `HO-*` via `wiki create` — handoffs are dispatch-owned under `wiki/handoffs/`.
- If wiki records and code/tests disagree, report the mismatch rather than trusting a grep-first conclusion.

<!-- END kb-managed -->


A collection of reusable Claude Code skills, subagent definitions, and orchestration guides for bioinformatics workflows.

## Project Structure

```
skills/<name>/         Skills (just a SKILL.md)
statusline/            Context window status bar tool
catalog/               External tool/skill catalog (data)
packages/catalog-mcp/  Catalog MCP tool server (14 tools)
docs/                  Public documentation
wiki/                  Private wiki (separate repo, gitignored)
```

### Adding a new skill

1. Create `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`)
2. Update the tables in `README.md`

## Catalog MCP Server

The catalog is managed by an MCP tool server at `packages/catalog-mcp/`. The server provides 14 tools for intake, research support, validation, and data management. It never makes LLM calls — the calling agent does all reasoning. The data lives in `catalog/` (entries, index, queue, config, goals, inbox, recipe).

### Running the server

The server is configured in `.mcp.json` (gitignored) and starts automatically when Claude Code opens this project. To run manually: `npx tsx packages/catalog-mcp/src/server.ts`.

### Interactive workflow

To add a tool to the catalog:
1. `fetch-url` — get the README
2. `build-prompt` — get a structured research prompt
3. Assess the tool yourself using the prompt
4. `validate-entry` — check your entry
5. `write-entry` — save to `catalog/entries/`
6. `index` — regenerate the index

### Available tools

`ingest`, `drain`, `fetch-url`, `reddit-extract`, `build-prompt`, `validate-entry`, `write-entry`, `index`, `search`, `lint`, `scaffold`, `queue`, `config`, `goals`

### Phase 2 — intake → processing pipeline

Two stages, split by who runs each:

1. **Intake (interactive).** Links/prose land in `catalog/inbox.md` (Gmail scan, chat paste, or hand-edit). The `/catalog-intake` skill curates the inbox and **drains** it: ready items are ingested into the queue; blocked-domain URLs (Instagram, X, LinkedIn *posts*) are marked `⚠ needs-link` and held. `config.json` `blocked_domains` drives the classification, with path exceptions (e.g. LinkedIn `/pulse/` articles are fetchable).
2. **Processing (manual or headless).** `catalog/recipe.md` is the runtime-agnostic loop: for each `pending` queue item — fetch (clean) or use `content`, `build-prompt`, assess, `validate-entry`, `write-entry`, then `queue` remove/update, and `index`. Run it headlessly with `npm run -w @catalog/mcp catalog:process`, which launches `claude -p` with the catalog server attached.

**Direct writes.** Entries are written straight to `catalog/entries/` with no draft/approved gate; `index` and `search` include every entry. The security boundary that matters for a catalogued tool is **adoption/installation**, handled at the install boundary (WK-0031, the `agent-lockdown` skill is the first piece) — not at cataloging time. The adapter (`src/adapter/run-processing.ts`) pins the verified `claude -p` flag format against a recorded CLI version; re-verify with `claude --help` if the CLI is upgraded.

## General Conventions

- Skills follow Claude Code's SKILL.md format with YAML frontmatter (`name`, `description`)
- Guides are standalone Markdown — no project-specific paths or data
- Keep docs general-purpose; use placeholders (`{YOUR_PROJECT}`, `{SCRIPT_DIR}`) where examples need paths
- Do **not** check in `.claude/skills/` — that directory is the install target on the user's system, not a source directory in this repo

## Subagents

Subagents default to Sonnet via `CLAUDE_CODE_SUBAGENT_MODEL` in `.claude/settings.json`. Pass `model: "opus"` on individual Agent calls only when the subagent needs complex reasoning or a Sonnet attempt produced inadequate results.

## Code Quality
- Prefer correct, complete implementations over minimal ones.
- Use appropriate data structures and algorithms — don't brute-force what has a known better solution.
- When fixing a bug, fix the root cause, not the symptom.
- If something I asked for requires error handling or validation to work reliably, include it without asking

