# /catalog skill

Research, assess, and catalog external tools, skills, and reference material.

## What it does

The `/catalog` skill gives you a structured workflow for evaluating external tools against your existing stack. It supports single-URL research, batch research via an inbox file (parallel subagents), index generation with three views (by verdict, by workflow, by category), and search.

Entries are standalone Markdown files with YAML frontmatter. Each gets a verdict (`adopt`, `pilot`, `watch`, `note`, `skip`) with a one-line reason.

## Directory layout

```
skills/catalog/
  SKILL.md          # Skill definition (Claude Code loads this)
  README.md         # This file

catalog/
  entries/*.md      # Individual tool/skill assessments
  index.md          # Generated index (three views)
  inbox.md          # Paste URLs here for batch research
```

The skill definition lives in `skills/catalog/`, but the data directory is `catalog/` at the repo root.

## Installation

### Prerequisites

- Claude Code with skill support
- WebFetch tool access (for research subagents to fetch URLs)
- Agent tool access (for parallel batch research)

### Steps

1. Copy `skills/catalog/SKILL.md` into your project's skill directory (typically `.claude/skills/catalog/SKILL.md` or wherever your project loads skills from).

2. Create the data directory structure at your repo root:

   ```
   mkdir catalog
   mkdir catalog/entries
   ```

3. Create `catalog/inbox.md`:

   ```markdown
   # Catalog Inbox

   URLs and references to evaluate for catalog entries.
   ```

4. Create an empty `catalog/index.md` (or run `/catalog index` after adding entries):

   ```markdown
   # Catalog Index

   Generated from 0 entries in `catalog/entries/`. Regenerate with `/catalog index`.
   ```

5. (Optional) Add `/catalog` to your project's skill table in `README.md`.

## Usage

| Command | Purpose |
|---|---|
| `/catalog research <url>` | Fetch and assess a single tool |
| `/catalog research catalog/inbox.md` | Batch-research all URLs in inbox |
| `/catalog index` | Regenerate `catalog/index.md` |
| `/catalog search <query>` | Find entries by tag, category, verdict, or keyword |

### Typical workflow

1. Paste URLs into `catalog/inbox.md` as you discover them
2. Run `/catalog research catalog/inbox.md` to evaluate the batch
3. Review proposed verdicts and adjust
4. Run `/catalog index` to regenerate the index

### Search examples

```
/catalog search spatial              # freeform keyword
/catalog search verdict:pilot        # field filter
/catalog search category:mcp-server  # by category
```

## Customization

The entry schema (categories, verdicts, body sections) is defined in `SKILL.md`. To adapt for your domain:

- Edit the `category` enum to match your tool taxonomy
- Add domain-specific `workflows` values
- Adjust body section templates if your assessments need different structure

## Dependencies

None beyond Claude Code itself. The skill uses only built-in tools (WebFetch, Agent, Glob, Grep, Read, Write).
