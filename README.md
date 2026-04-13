# bioinfo-agent-toolkit

Reusable Claude Code skills, tools, and guides for bioinformatics workflows. Pick and choose what you need.

## Quick Start

```bash
git clone https://github.com/mcap91/bioinf-agent-toolkit.git
cd bioinf-agent-toolkit

# See what's available
./install.sh --list

# Install into your project
./install.sh handoff statusline --project ~/projects/my-app

# Or install into current directory
./install.sh handoff statusline

# Remove what you don't need
./uninstall.sh statusline
```

Skills install into the project's `.claude/skills/` directory. Tools (like statusline) install into `~/.claude/` (user-global).

## Skills

| Skill | Description | Install |
|---|---|---|
| [/handoff](skills/handoff/) | Generate a handoff prompt for a fresh CLI agent or subagent | `./install.sh handoff` |
| [/scripts-reference](skills/scripts-reference/) | Generate a clickable script reference doc | `./install.sh scripts-reference` |
| [/plan-me-this](skills/plan-me-this/) | Package a spec into phase docs + readme_this_current_task.md | `./install.sh plan-me-this` |

## Tools

| Tool | Description | Install |
|---|---|---|
| [Status Line](statusline/) | Context window usage bar for the Claude Code CLI | `./install.sh statusline` |

## Guides

- [Subagent Workflow](guides/subagent-workflow.md) — automate the plan-with-Opus, execute-with-Sonnet pattern

## Structure

```
skills/<name>/     Skills — each has SKILL.md + install.sh + uninstall.sh
statusline/        Tools — each has install.sh + uninstall.sh
guides/            Workflow patterns and reference docs
docs/              Roadmap, specs, and planning
install.sh         Top-level installer (dispatches to per-component scripts)
uninstall.sh       Top-level uninstaller
```

Every installable component has its own `install.sh` and `uninstall.sh`. The top-level scripts are convenience wrappers — you can also run component scripts directly (e.g. `./skills/handoff/install.sh`).

See [docs/roadmap.md](docs/roadmap.md) for the full roadmap.
