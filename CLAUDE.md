# bioinfo-agent-toolkit

A collection of reusable Claude Code skills, subagent definitions, and orchestration guides for bioinformatics workflows.

## Project Structure

```
skills/<name>/     Skills (just a SKILL.md)
statusline/        Context window status bar tool
catalog/           External tool/skill catalog
docs/              Public documentation
wiki/              Private wiki (separate repo, gitignored)
```

### Adding a new skill

1. Create `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`)
2. Update the tables in `README.md`

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

# kb Integration

This repo is managed with the `kb` toolkit from `../kb`.

Use this operating model:

- run the `kb` wiki MCP server from `../kb`
- run the `kb` dispatch MCP server from `../kb` when you need handoff lifecycle tools
- use MCP for wiki operations against this repo
- use dispatch MCP or `../kb` CLI for dispatch
- use `../kb` CLI for graph
- target this repo explicitly with `dir`
- keep Claude project MCP config in this repo, not copied verbatim from `../kb/.mcp.json`

Repository-context retrieval is a wiki/docs retrieval problem first, not a broad filesystem search problem first.

Before substantive work:

1. Start from `wiki/catalog.md`.
2. Read the relevant durable `docs/` reference pages.
3. Check related `wiki/decisions/`, `wiki/issues/`, `wiki/initiatives/`, `wiki/areas/`, and `wiki/sources/`.
4. Only then inspect implementation files.

Do not use raw `rg` as the first retrieval step for repo-context questions. Use `wiki/catalog.md` or `wiki search` first.

Do not parallelize implementation search with the initial retrieval pass. Complete steps 1-3 before searching code.

## Commands

Install or update `kb`:

```bash
cd ../kb
npm install
npm run typecheck
npm test
```

If Claude runs in this consuming repo, put a repo-local `.mcp.json` here that points back to `../kb`.

If Codex runs on this machine, register the `kb` checkout once from `../kb`:

```bash
cd ../kb
npm run codex:mcp:register
```

Do not copy `../kb/.mcp.json` into this repo unchanged. That file is only for the self-hosted `kb` repo case.

Bootstrap this repo:

```bash
cd ../kb
npm run wiki -- bootstrap --dir ../bioinfo-agent-toolkit --repo mcap91/bioinfo-agent-toolkit
npm run dispatch -- init-config
npm run wiki -- generate --dir ../bioinfo-agent-toolkit
npm run wiki -- build-search-index --dir ../bioinfo-agent-toolkit
npm run graph -- --dir ../bioinfo-agent-toolkit
```

Update this repo after `kb` changes:

```bash
cd ../kb
git pull
npm install
npm run typecheck
npm test
npm run wiki -- sync-contract --dir ../bioinfo-agent-toolkit
npm run wiki -- lint --dir ../bioinfo-agent-toolkit
npm run wiki -- generate --dir ../bioinfo-agent-toolkit
npm run wiki -- build-search-index --dir ../bioinfo-agent-toolkit
npm run graph -- --dir ../bioinfo-agent-toolkit
```

If this repo uses dispatch and is upgrading from the older dispatch registry format:

```bash
cd ../kb
npm run dispatch -- init-config --force
```

`sync-contract` does not update this repo's `AGENTS.md` or `CLAUDE.md`.
It also does not overwrite `wiki/schema.md`, `wiki/conventions.md`, or `wiki/index.md`.

## Rules

- Prefer `kb` MCP for wiki operations.
- Prefer dispatch MCP or `kb` CLI for `dispatch`.
- Use `kb` CLI for `graph`.
- Do not create `HO-*` with `wiki create`.
- Run `kb` from `../kb`, not from this repo root.
