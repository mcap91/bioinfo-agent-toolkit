# bioinfo-agent-toolkit

<!-- BEGIN kb-managed -->
Managed by kb — edits inside this block are overwritten by `kb bootstrap` / `kb sync-contract`; edit outside the markers.

@AGENTS.md
<!-- END kb-managed -->


A collection of reusable Claude Code skills, subagent definitions, and orchestration guides for scientific workflows.

## Project Structure

```
skills/<name>/         Skills (just a SKILL.md)
statusline/            Context window status bar tool
catalog/               External tool/skill catalog (data)
packages/catalog-mcp/  Catalog MCP tool server (15 tools)
docs/                  Public documentation
wiki/                  Private wiki (separate repo, gitignored)
```

### Adding a new skill

1. Create `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`)
2. Update the tables in `README.md`

## Catalog MCP Server

The catalog is managed by an MCP tool server at `packages/catalog-mcp/`. The server provides 17 tools for intake, research support, validation, knowledge graph, and data management. It never makes LLM calls — the calling agent does all reasoning. The data lives in `catalog/` (entries, index, queue, config, goals, inbox, recipe).

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

`ingest`, `drain`, `fetch-url`, `reddit-extract`, `build-prompt`, `validate-entry`, `write-entry`, `annotate-entry`, `index`, `search`, `lint`, `scaffold`, `queue`, `config`, `goals`, `graph-build`, `graph-query`

### Catalog pipeline — intake → processing

The full flow is documented in `skills/catalog-intake/SKILL.md`. Summary:

1. **Intake (interactive).** Run the `/catalog-intake` skill or follow it manually. It pulls from
   Gmail (`from:me subject:catalog after:<cursor>`), appends URLs/prose to `catalog/inbox.md`,
   updates the cursor in `catalog/state.json` via `config { action: "set-state" }`, curates with
   the user, then drains. Blocked/unfetchable items (Instagram, Reddit `/s/` share links, X,
   LinkedIn posts) stay in inbox marked `⚠ needs-link` until resolved.
2. **Processing (headless).** Run in the background:
   ```
   npm run -w @catalog/mcp catalog:process
   ```
   This launches `claude --print` with the catalog MCP server, follows `catalog/recipe.md`, and
   processes every pending queue item unattended. The queue holds only pending work: every item
   ends as a catalog entry or returns to `catalog/inbox.md` marked `⚠ <reason>`, so after a clean
   run `catalog/queue.json` is empty. Check `inbox.md` for any returned items, then commit the new entries.

**Direct writes.** Entries go straight to `catalog/entries/` — no draft gate. The security boundary
is at **adoption/installation** (WK-0031), not cataloging time. The adapter
(`src/adapter/run-processing.ts`) pins the `claude --print` flag format; re-verify with
`claude --help` if the CLI is upgraded.

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

