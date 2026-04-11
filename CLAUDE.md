# bioinfo-agent-toolkit

A collection of reusable Claude Code skills, subagent definitions, and orchestration guides for bioinformatics workflows.

## Project Structure

```
skills/<name>/       Skills (SKILL.md + install.sh + uninstall.sh)
statusline/          Tools (script + install.sh + uninstall.sh)
guides/              Workflow patterns and reference docs
docs/                Roadmap, specs, and planning
install.sh           Top-level installer: ./install.sh handoff statusline
uninstall.sh         Top-level uninstaller: ./uninstall.sh statusline
```

## Modularity Convention

Every installable component — whether a skill, tool, or system — lives in its own directory and **must** contain:

- `install.sh` — installs the component to the user's system
- `uninstall.sh` — cleanly removes it without affecting anything else

The top-level `install.sh` / `uninstall.sh` discover components automatically: any directory with an `install.sh` is installable. No registration step needed.

### Where components install to

| Type | Target | Example |
|------|--------|---------|
| Skill | `<project>/.claude/skills/<name>/` (project-specific) | handoff |
| Tool | `~/.claude/` + settings.json (user-global) | statusline |

Skills accept `--project <path>` to target a specific project (defaults to current directory).

### Adding a new skill

1. Create `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`)
2. Add `skills/<name>/install.sh` that copies SKILL.md to `$PROJECT_DIR/.claude/skills/<name>/`
3. Add `skills/<name>/uninstall.sh` that removes `$PROJECT_DIR/.claude/skills/<name>/`
4. Update `docs/roadmap.md` and the tables in `README.md`

### Adding a new tool

1. Create `<name>/` at repo root with the tool's files
2. Add `<name>/install.sh` and `<name>/uninstall.sh`
3. Update `docs/roadmap.md` and the tables in `README.md`

## General Conventions

- Skills follow Claude Code's SKILL.md format with YAML frontmatter (`name`, `description`)
- Guides are standalone Markdown — no project-specific paths or data
- Keep docs general-purpose; use placeholders (`{YOUR_PROJECT}`, `{SCRIPT_DIR}`) where examples need paths
- Do **not** check in `.claude/skills/` — that directory is the install target on the user's system, not a source directory in this repo

## Code Quality
- Prefer correct, complete implementations over minimal ones.
- Use appropriate data structures and algorithms — don't brute-force what has a known better solution.
- When fixing a bug, fix the root cause, not the symptom.
- If something I asked for requires error handling or validation to work reliably, include it without asking
