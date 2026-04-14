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
| [/blueprint](skills/blueprint/) | Create a portable architecture reference for reimplementing a system | `./install.sh blueprint` |

## Tools

| Tool | Description | Install |
|---|---|---|
| [kb-graph](phoam_paint/) | Auto-generated knowledge graph — KB_INDEX.md + graph.html for any repo | `./install.sh phoam_paint` |
| [Status Line](statusline/) | Context window usage bar for the Claude Code CLI | `./install.sh statusline` |

## Guides

- [Subagent Workflow](docs/subagent-workflow.md) — automate the plan-with-Opus, execute-with-Sonnet pattern

## Structure

```
skills/<name>/     Skills (just a SKILL.md — no install scripts needed)
statusline/        Tools — each has install.sh + uninstall.sh
docs/              Roadmap, specs, and planning
install.sh         Top-level installer: ./install.sh handoff statusline
uninstall.sh       Top-level uninstaller: ./uninstall.sh statusline
```

Skills only need a `SKILL.md`. The top-level installer handles copying them to the target project's `.claude/skills/<name>/`. Tools (like statusline, phoam_paint) have custom install logic and contain their own `install.sh` and `uninstall.sh`.

See [docs/roadmap.md](docs/roadmap.md) for the full roadmap.
