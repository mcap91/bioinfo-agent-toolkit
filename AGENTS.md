# kb Integration

This repository uses the `kb` toolkit from `../kb`.

Assumptions:

- this repo is the consuming repo
- the `kb` repo lives at `../kb`
- all `kb` commands are run from `../kb`
- this repo is targeted via `dir`
- this repo does not reuse `../kb/.mcp.json` verbatim

## Required Behavior

When you need wiki operations, prefer the `kb` wiki MCP server running from `../kb`.

Use MCP for:

- `bootstrap`
- `sync-contract`
- `allocate-id`
- `create`
- `lint`
- `generate`
- `build-search-index`
- `search`

Always pass `dir` pointing at this repository.

When you need dispatch operations, prefer the `kb` dispatch MCP server or the `kb` CLI from `../kb`.

Dispatch operations:

- `init-config`
- `check-environment`
- `create-handoff`
- `review`
- `launch`
- `review-and-launch`
- `status`
- `cleanup`

When you need graph operations, use the `kb` CLI from `../kb`.

Do not run `kb` commands from this repo root unless explicitly instructed. Run them from `../kb` and point back to this repo with `--dir`.

Repository-context retrieval is a wiki/docs retrieval problem first, not a broad filesystem search problem first.

Before substantive work:

1. Start from `wiki/catalog.md`.
2. Read the relevant durable `docs/` reference pages.
3. Check related `wiki/decisions/`, `wiki/issues/`, `wiki/initiatives/`, `wiki/areas/`, and `wiki/sources/`.
4. Only then inspect implementation files.

Do not use raw `rg` as the first retrieval step for repo-context questions. Use `wiki/catalog.md` or `wiki search` first.

Do not parallelize implementation search with the initial retrieval pass. Complete steps 1-3 before searching code.

## First-Time Setup

If `../kb` dependencies are not installed:

```bash
cd ../kb
npm install
npm run typecheck
npm test
```

If Claude will run in this consuming repo, create this repo's own `.mcp.json` that points back to `../kb` or to the absolute `kb` path.

If Codex will run on this machine, register the `kb` checkout once and reuse it:

```bash
cd ../kb
npm run codex:mcp:register
```

Do not copy `../kb/.mcp.json` into this repo verbatim. That file is only for self-hosting the `kb` repo itself.

If this repo has not been bootstrapped yet:

1. Derive the repo slug from git remote if possible.
2. Run:

```bash
cd ../kb
npm run wiki -- bootstrap --dir ../bioinfo-agent-toolkit --repo mcap91/bioinfo-agent-toolkit
npm run dispatch -- init-config
npm run wiki -- generate --dir ../bioinfo-agent-toolkit
npm run wiki -- build-search-index --dir ../bioinfo-agent-toolkit
npm run graph -- --dir ../bioinfo-agent-toolkit
```

If you already know the absolute path to this repo, you may use that instead of a relative path.

## Day-2 Operations

After updating `kb`:

```bash
cd ../kb
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

- Prefer MCP over CLI for wiki operations.
- Prefer dispatch MCP or CLI for `dispatch`.
- Use CLI for `graph`.
- Do not create `HO-*` via `wiki create`.
- `wiki/handoffs/` is dispatch-owned and excluded from wiki scanning operations.
- Always keep `kb` validation green before relying on it:

```bash
cd ../kb
npm run typecheck
npm test
```
