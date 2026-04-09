# bioinfo-agent-toolkit

A collection of reusable Claude Code skills, subagent definitions, and orchestration guides for bioinformatics workflows.

## Project Structure

- `.claude/skills/` — Claude Code skills (functional when repo is cloned)
- `guides/` — Workflow patterns and reference docs
- `docs/` — Roadmap and planning

## Conventions

- Skills follow Claude Code's SKILL.md format with YAML frontmatter (`name`, `description`)
- Guides are standalone Markdown — no project-specific paths or data
- Keep docs general-purpose; use placeholders (`{YOUR_PROJECT}`, `{SCRIPT_DIR}`) where examples need paths

## When contributing new skills

1. Create `.claude/skills/<skill-name>/SKILL.md`
2. Update `docs/roadmap.md` to mark it as completed
3. Add an entry to the skills table in `README.md`
