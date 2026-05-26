---
name: catalog
description: "Research, assess, and catalog external tools and skills"
---

# /catalog

Research, assess, and catalog external skills, plugins, hooks, MCP servers, agent patterns, CLI tools, frameworks, and reference material.

## Invocations

| Command | What happens |
|---|---|
| `/catalog research <url>` | Research a single URL and draft one catalog entry |
| `/catalog research <inbox-file>` | Extract URLs from file, dispatch parallel subagents, draft entries for each |
| `/catalog index` | Regenerate `catalog/index.md` from all entry files |
| `/catalog search <query>` | Grep entries by tag, category, workflow, or verdict and return filtered table |

## Entry Schema

Each entry is a standalone `.md` file in `catalog/entries/` with YAML frontmatter:

~~~yaml
---
name: example-tool
title: "Example Tool"
url: https://github.com/org/example-tool
category: skill
verdict: pilot
verdict_reason: "one-line explanation of why this verdict"
install: "npm install example-tool"
tags: [tag1, tag2]
workflows: [scRNA-seq, spatial]
reviewed: 2026-05-25
supersedes: []
overlaps: [other-tool]
---
~~~

### Fields

| Field | Required | Description |
|---|---|---|
| `name` | yes | kebab-case slug, matches filename |
| `title` | yes | Display name |
| `url` | yes | Source URL (empty string if none) |
| `category` | yes | One of: `skill`, `hook`, `plugin`, `mcp-server`, `agent-pattern`, `cli-tool`, `framework`, `skill-generator`, `meta-skill`, `reference` |
| `verdict` | yes | One of: `adopt`, `pilot`, `skip`, `note`, `watch` |
| `verdict_reason` | yes | One-line summary of why this verdict was chosen |
| `install` | no | Install command. Omit for reference/pattern entries |
| `tags` | yes | List of tags for search |
| `workflows` | no | Bioinformatics workflows this applies to. Omit for general-purpose |
| `reviewed` | yes | Date of last review (YYYY-MM-DD) |
| `supersedes` | no | List of entry names this replaces |
| `overlaps` | no | List of entry names that serve a similar purpose or compete |

### Verdicts

| Verdict | Meaning |
|---|---|
| `adopt` | Use it. Already validated or clearly superior. |
| `pilot` | Try it on one project/task. Promising but unproven in our stack. |
| `watch` | Not ready yet. Blocked by a prerequisite or dependency. Check back later. |
| `note` | Interesting concept or reference. Not a tool to install. Ideas to learn from. |
| `skip` | Evaluated and rejected. Record WHY so we don't re-research it. |

### Entry Body

**Installable tools** (skill, plugin, mcp-server, cli-tool, framework, skill-generator, meta-skill):

~~~markdown
## What it does

4-6 sentences. The tool's mechanics, how it works, what makes it distinct.

## Why this verdict

How it compares to what you already have, what's strong, what's missing or risky.

## Mechanical details

Install command, requirements, key configuration, setup steps.
~~~

**Reference material** (reference, agent-pattern):

~~~markdown
## What it says

4-6 sentences. The core ideas, rules, or patterns.

## Why this verdict

Which parts are already covered by your existing stack, which parts are novel.

## What to adopt

Specific, actionable items.
~~~

## Research Workflow

### Single URL: `/catalog research <url>`

1. Fetch the URL via WebFetch
2. Read `catalog/index.md` to understand the existing stack
3. Draft an entry file to `catalog/entries/{name}.md`
4. Propose a verdict with reasoning
5. Present the draft for user review
6. After user approval, finalize and regenerate index

### Batch: `/catalog research <inbox-file>`

1. Read the inbox file, extract all URLs and attached notes
2. Read `catalog/index.md` for stack context
3. Dispatch one subagent per URL in parallel. Each subagent:
   - Has WebFetch access
   - Receives the URL, any attached notes, the entry schema, and the current index
   - Writes a draft entry to `catalog/entries/{name}.md`
   - Proposes a verdict with reasoning
4. Present a summary table of all drafts with proposed verdicts
5. User adjusts verdicts, tags, workflows, notes
6. Finalize entries with user adjustments
7. Clear processed URLs from inbox
8. Regenerate index

#### Subagent Prompt Template

When dispatching research subagents, use this structure:

~~~
Research this URL for the bioinfo-agent-toolkit catalog.

URL: {url}
Notes: {notes or "none"}

Read the current catalog index at catalog/index.md to understand what tools are already tracked.

Fetch the URL via WebFetch. Read the README, documentation, or main content.

Write a catalog entry to catalog/entries/{proposed-name}.md using this schema:

[paste entry schema from above]

Use the [installable tools | reference material] body format based on the category.

Propose a verdict (adopt/pilot/watch/note/skip) with a one-line verdict_reason.
~~~

## Index Generation

`/catalog index` reads all `catalog/entries/*.md` files and generates `catalog/index.md` with three views:

### By Verdict

Summary table sorted: adopt first, then pilot, watch, note, skip.

~~~markdown
## By Verdict

| Item | Category | Verdict | Reason | Tags |
|---|---|---|---|---|
| [Tool Name](entries/tool-name.md) | skill | adopt | one-line reason | tag1, tag2 |
~~~

### By Workflow

Grouped list. Each workflow as a heading with its tools. General-purpose tools under "General".

~~~markdown
## By Workflow

### scRNA-seq
- [Tool A](entries/tool-a.md) - verdict - one-line reason

### General
- [Tool C](entries/tool-c.md) - verdict - one-line reason
~~~

### By Category

Grouped list. Each category as a heading with its tools.

~~~markdown
## By Category

### skill
- [Tool A](entries/tool-a.md) - verdict - one-line reason
~~~

All item names link to the full entry file.

## Search

`/catalog search` greps entry frontmatter and body text. Returns a filtered summary table.

Examples:
- `/catalog search spatial` — entries tagged with or mentioning spatial
- `/catalog search verdict:pilot` — all pilot entries
- `/catalog search category:skill` — all skills
- `/catalog search kb` — anything tagged with or mentioning kb

Implementation:
1. Glob `catalog/entries/*.md`
2. For `field:value` queries, grep frontmatter for the field
3. For freeform queries, grep both frontmatter and body
4. Format results as summary table: Item | Category | Verdict | Reason | Tags

## Inbox

`catalog/inbox.md` is a freeform scratchpad. Paste URLs with optional notes:

~~~markdown
# Catalog Inbox

https://github.com/some/cool-skill
saw this on reddit, might help with QC reports

https://github.com/another/tool
competitor to BMAD?
~~~

URLs are extracted and cleared from inbox after research completes and entries are finalized.

## Scope

This skill does NOT:
- Install or configure any cataloged tool — it records assessments
- Replace the wiki or kb — the catalog is for external tool tracking
- Auto-discover tools — input is user-curated (inbox links)
- Make final verdict decisions — subagents propose, user decides
