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
| [/catalog-intake](skills/catalog-intake/) | Pull links from Gmail, curate, drain to queue, run headless processing |
| [/agent-lockdown](skills/agent-lockdown/) | Lock down a coding agent CLI — version pin, model pin, env hardening, secrets deny, integrity checkup |
| [/explain-me-this](skills/explain-me-this/) | Discuss-and-explain persona — explains, researches, and helps you decide; no code or plans. Manual-only. |

## Tools

### [Status Line](statusline/)

Context window usage bar for the Claude Code CLI. See [statusline/README.md](statusline/README.md) for setup.

## Catalog

The `catalog/` directory tracks external skills, plugins, hooks, MCP servers, agent patterns, CLI tools, frameworks, and reference material — 171 assessed entries with summaries, security reviews, and tags.

### Using the catalog from another project

Register the catalog MCP server in your project's `.mcp.json` to give your agent access to search, graph traversal, and topic discovery across all catalog entries.

**Add to your project's `.mcp.json`:**

```json
{
  "mcpServers": {
    "bioinfo-catalog": {
      "type": "stdio",
      "command": "node",
      "args": [
        "--import",
        "file:///PATH/TO/bioinfo-agent-toolkit/node_modules/tsx/dist/loader.mjs",
        "PATH/TO/bioinfo-agent-toolkit/packages/catalog-mcp/src/server.ts"
      ],
      "env": {}
    }
  }
}
```

Replace `PATH/TO` with the absolute path to your local clone of this repo.

**Key tools for cross-repo use:**

| Tool | Purpose |
|---|---|
| `search` | Keyword search with field-weighted ranking (title > tags > summary > body). Returns scores and truncation signal. |
| `graph-query` | Knowledge graph traversal. `neighbors` mode: explore connections from a known entry (overlaps, shared tags, shared category). `topic` mode: discover entries by concept (substring match on tags/categories). |
| `graph-build` | Rebuild the knowledge graph on demand (normally auto-rebuilds via `index`). |

**Add retrieval instructions to your project's CLAUDE.md:**

```markdown
## External tool catalog

This project registers the bioinfo-agent-toolkit catalog MCP server as `bioinfo-catalog`.
Use it to find tools, skills, frameworks, or MCP servers:

- `search { query: "multi-agent orchestration" }` — keyword search
- `graph-query { mode: "topic", term: "orchestration" }` — find entries by concept
- `graph-query { mode: "neighbors", entry: "mycelium" }` — explore connections from a known entry
```

**Lightweight alternative (no MCP):** The catalog ships a search index at [`catalog/.search-index.json`](catalog/.search-index.json). Any agent can fetch it via URL and search in-context:

```
https://raw.githubusercontent.com/mcap91/bioinfo-agent-toolkit/main/catalog/.search-index.json
```

### Managing the catalog

The catalog is managed by an MCP tool server in [`packages/catalog-mcp/`](packages/catalog-mcp/) — 17 tools for intake, research support, validation, knowledge graph, and data management. The server never makes LLM calls; the calling agent does all reasoning.

| Group | Tools |
|---|---|
| Intake | `ingest`, `drain`, `fetch-url`, `reddit-extract`, `build-prompt` |
| Entries | `validate-entry`, `write-entry`, `annotate-entry`, `scaffold` |
| Data | `index`, `search`, `lint`, `queue`, `config`, `goals` |
| Graph | `graph-build`, `graph-query` |

Running `index` regenerates `catalog/index.md`, `catalog/.search-index.json`, and `catalog/.graph.json`.

## Structure

```
skills/<name>/         Skills (just a SKILL.md)
statusline/            Context window status bar tool
catalog/               External tool/skill catalog (data + derived artifacts)
packages/catalog-mcp/  Catalog MCP tool server (17 tools)
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
