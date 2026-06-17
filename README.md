# bioinfo-agent-toolkit

Reusable Claude Code skills, tools, and guides for bioinformatics workflows. Pick and choose what you need.

## Skills

Copy any skill into your project:

```bash
# From a clone of this repo
cp -r skills/<name> <your-project>/.claude/skills/<name>
```

| Skill | Description |
|---|---|
| [/blueprint](skills/blueprint/) | Create a portable architecture reference doc for reimplementation |
| [/handoff](skills/handoff/) | Generate a handoff prompt for a fresh CLI agent or subagent |
| [/plan-me-this](skills/plan-me-this/) | Package a spec into phase docs + readme_this_current_task.md |
| [/scripts-reference](skills/scripts-reference/) | Generate a clickable script reference doc |
| [/catalog-intake](skills/catalog-intake/) | Scan and curate links into the catalog inbox, then drain to the queue |
| [/agent-lockdown](skills/agent-lockdown/) | Lock down a coding agent CLI — version pin, model pin, env hardening, secrets deny, integrity checkup |

## Tools

### [Status Line](statusline/)

Context window usage bar for the Claude Code CLI. See [statusline/README.md](statusline/README.md) for setup.

## Catalog

The `catalog/` directory tracks external skills, plugins, hooks, MCP servers, agent patterns, CLI tools, frameworks, and reference material — 116 assessed entries with summaries, security reviews, and tags.

### Using the catalog from another project

The catalog ships a search index at [`catalog/.search-index.json`](catalog/.search-index.json) — a single JSON file any agent can read to find tools, benchmarks, skills, or frameworks without cloning this repo or running an MCP server.

**Add this to your project's CLAUDE.md** (or equivalent agent instructions):

```markdown
## External tool catalog

When looking for tools, skills, benchmarks, frameworks, or MCP servers, check the
bioinfo-agent-toolkit catalog first:

    https://raw.githubusercontent.com/mcap91/bioinfo-agent-toolkit/main/catalog/.search-index.json

Fetch this file and search by tags, category, decision_status, or keywords in summary/body_summary.
Decision status: adopted (in use), rejected (evaluated and ruled out); unset = open (stockpiled, undecided).
For full details on any entry, read the file at the entry's `path` field from the same repo.
```

An agent in your project can then `WebFetch` the URL (or `Read` it from a local clone) and search in-context — no MCP wiring needed.

### Managing the catalog

The catalog is managed by an MCP tool server in [`packages/catalog-mcp/`](packages/catalog-mcp/) — 15 tools for intake, research support, validation, and data management (index, search, lint, scaffold, ingest, drain, fetch-url, build-prompt, validate-entry, write-entry, annotate-entry, queue, config, goals, reddit-extract). The server never makes LLM calls; the calling agent does all reasoning. Running the `index` tool regenerates both `catalog/index.md` and `catalog/.search-index.json`.

## Structure

```
skills/<name>/         Skills (just a SKILL.md)
statusline/            Context window status bar tool
catalog/               External tool/skill catalog (data)
packages/catalog-mcp/  Catalog MCP tool server (15 tools)
docs/                  Public documentation
```

## Maintainer Setup

This repo uses the `kb` toolkit for project tracking. The wiki lives in a separate private repo and is cloned into the gitignored `wiki/` directory.

```bash
# Clone the private wiki into this repo
git clone git@github.com:mcap91/bioinfo-agent-toolkit-wiki.git wiki

# Run kb commands from the kb checkout
cd ../kb
npm run wiki -- lint --dir ../bioinfo-agent-toolkit
npm run wiki -- generate --dir ../bioinfo-agent-toolkit
```

See `AGENTS.md` for the full kb workflow.

## License

[MIT](LICENSE)
