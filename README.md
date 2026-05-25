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

## Guides

- [Subagent Workflow](docs/subagent-workflow.md) — automate the plan-with-Opus, execute-with-Sonnet pattern

## Structure

```
skills/<name>/     Skills (just a SKILL.md)
statusline/        Context window status bar tool
catalog/           External tool/skill catalog
docs/              Roadmap, specs, and planning
```

See [docs/roadmap.md](docs/roadmap.md) for the full roadmap.
