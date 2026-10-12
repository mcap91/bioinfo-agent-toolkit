# Semantic Search

Hybrid semantic + lexical search over catalog entries. Concept queries like "PDF parsing
scientific papers with tables" surface relevant tools even when they share no exact keywords
with the query, blended with field-weighted lexical ranking for precise keyword matches.

## What it does

Search runs two scorers and blends them:

- **Semantic**: embeds the query and every catalog entry with a local model
  ([fastembed](https://github.com/qdrant/fastembed), `BAAI/bge-small-en-v1.5`, 384 dimensions,
  ~34MB quantized ONNX model), then ranks by cosine similarity.
- **Lexical**: field-weighted keyword scoring (title: 10, name: 5, summary: 3, body: 1, tags: 5).

The two scores are blended:

```
final_score = (1 - alpha) * lexical_normalized + alpha * cosine_similarity
```

`alpha` defaults to `0.5` and is tunable per query.

## Prerequisites

- Python 3.10+
- [uv](https://astral.sh/uv) — Python package/environment manager
- `fastembed` (installed via the setup command below)

## Setup

```bash
cd {YOUR_PROJECT}/packages/catalog-embedder
uv venv
uv pip install -r requirements.txt
```

The embedding model (~34MB) downloads once to `~/.cache/fastembed/` on first use, then runs
offline.

## CLI usage

Build the vector index for all entries:

```bash
python -m catalog_embedder build --dir {YOUR_PROJECT}
```

Run a search:

```bash
python -m catalog_embedder search --query "PDF parsing scientific papers with tables" \
  --dir {YOUR_PROJECT} \
  [--limit 10] \
  [--alpha 0.5] \
  [--decision-status adopted] \
  [--category "document-processing"]
```

Both commands take `--dir`, the path to the project root containing the catalog data.

## Auto-rebuild

Vectors are a derived artifact — not committed to source control — and rebuild automatically
in three cases:

1. **On index** — whenever the catalog's `index` tool regenerates derived files.
2. **On `git pull`** — a git post-merge hook detects changes to catalog entries and rebuilds.
3. **On first search** — if no vector file exists yet, a search triggers a build before
   returning results.

There is no manual build step for normal use.

### Enabling the post-merge hook

Git hooks aren't enabled by default on clone. Point git at the repo's hooks directory once:

```bash
git config core.hooksPath .githooks
```

After that, pulling changes that touch catalog entries automatically rebuilds the vector
index in the background.

## Using this from another repo

Consuming repos don't need to run the CLI directly. Register the project's MCP server in
`.mcp.json` as usual, then call its `search` tool — the tool invokes the embedding CLI as a
subprocess and handles the semantic+lexical blend transparently. No extra configuration is
required beyond the one-time `uv`/`fastembed` setup on the host running the server.

If the Python environment isn't set up, `search` returns an error describing the missing
setup step rather than silently falling back to lexical-only results.

## Performance

- **Cold start**: ~1-2 seconds per query (Python interpreter startup, model load, embedding,
  scoring).
- **Build**: tens of seconds for a few hundred entries; scales with catalog size.
- **Model**: downloaded once (~34MB), then fully offline.
