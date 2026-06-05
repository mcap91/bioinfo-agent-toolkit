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

## Tools

### [Status Line](statusline/)

Context window usage bar for the Claude Code CLI. See [statusline/README.md](statusline/README.md) for setup.

## Catalog

The `catalog/` directory tracks external skills, plugins, hooks, MCP servers, agent patterns, CLI tools, frameworks, and reference material. See `catalog/index.md` for the current index.

The catalog is managed by an MCP tool server in [`packages/catalog-mcp/`](packages/catalog-mcp/) — 13 tools for intake, research support, validation, and data management (index, search, lint, scaffold, ingest, fetch-url, build-prompt, validate-entry, write-entry, queue, config, goals, reddit-extract). The server never makes LLM calls; the calling agent does all reasoning.

## Structure

```
skills/<name>/         Skills (just a SKILL.md)
statusline/            Context window status bar tool
catalog/               External tool/skill catalog (data)
packages/catalog-mcp/  Catalog MCP tool server (13 tools)
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
