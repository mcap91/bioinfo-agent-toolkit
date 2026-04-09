# bioinfo-agent-toolkit

Reusable Claude Code skills, subagent definitions, and orchestration guides built for bioinformatics workflows.

## Structure

```
skills/          Skill source and documentation (browseable)
  handoff/       Hand off work to a fresh agent or subagent
.claude/skills/  Symlinked or copied — makes skills functional when cloned
guides/          Workflow guides and patterns
docs/            Roadmap and project planning
```

## Skills

| Skill | Description | Status |
|---|---|---|
| `/handoff` | Generate a handoff prompt for a fresh CLI agent or subagent | Done |
| `/scripts-reference` | Generate a clickable script reference doc | Planned |
| `/plan-me-this` | Scaffold a multi-phase task package from a plan | Planned |

See [docs/roadmap.md](docs/roadmap.md) for the full list.

## Guides

- [Subagent Workflow](guides/subagent-workflow.md) — automate the plan-with-Opus, execute-with-Sonnet pattern
