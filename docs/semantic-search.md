# Semantic Search

Semantic-first search over catalog entries, with BM25 keyword matching as a rescue signal.
Concept queries like "PDF parsing scientific papers with tables" surface relevant tools even
when they share no exact keywords with the query, while exact tool names and rare terms still
rank highly through the BM25 rescue.

## What it does

Search runs two scorers and takes the max of the two, per entry:

- **Semantic**: embeds the query and every catalog entry with a local model
  ([fastembed](https://github.com/qdrant/fastembed), `BAAI/bge-small-en-v1.5`, 384 dimensions,
  ~34MB quantized ONNX model), then ranks by cosine similarity.
- **BM25**: an inline keyword scorer (k1=1.2, b=0.75) over all entry fields (title, name,
  summary, body, tags). Its result is normalized into `[0, BM25_RESCUE_CAP]` (0.5), not
  `[0, 1]`, so it can only *rescue* a weak semantic match — it never outranks a strong
  cosine match.

```
final_score = max(cosine_similarity, normalized_bm25)
```

There is no blend and no alpha parameter: semantic ranks everything, and BM25 can only help
entries with strong keyword overlap but weak embeddings (exact tool names, rare terms) — it
can never drag a good semantic score down. An optional `--threshold` filters results to
`score > threshold` (default `0.0`, i.e. return everything that scored above zero). A query
that's empty after tokenization bypasses scoring entirely and returns every entry with
`score = 0.0`, preserving filtered-listing behavior (e.g. `search "" --category reference`).

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
  [--threshold 0.0] \
  [--method fusion] \
  [--decision-status adopted] \
  [--category "document-processing"]
```

Both commands take `--dir`, the path to the project root containing the catalog data.
`--threshold` filters results to `score > threshold` (default `0.0`). `--method`
(`fusion` | `semantic` | `bm25`) selects a single scorer for eval baselines; the MCP
`search` tool always uses `fusion`.

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
subprocess and handles the semantic + BM25 rescue fusion transparently. No extra
configuration is required beyond the one-time `uv`/`fastembed` setup on the host running
the server.

If the Python environment isn't set up, `search` returns an error describing the missing
setup step rather than silently falling back to BM25-only results.

## Performance

- **Cold start**: ~1-2 seconds per query (Python interpreter startup, model load, embedding,
  scoring).
- **Build**: tens of seconds for a few hundred entries; scales with catalog size.
- **Model**: downloaded once (~34MB), then fully offline.
