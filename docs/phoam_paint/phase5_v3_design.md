# Phase 5 v3: Harder A/B Experiment — Design Spec

> Redesigned experiment to prove /check_graph value on a bioinformatics-style
> fixture with deep import chains and __init__.py re-exports.

## Context

Phase 5 v2 (blast radius marking on a web-app fixture) produced identical
80% recall for both agents. Agent A manually traced all Python import chains
in a 46-file project. The only differentiator was markdown wiki-link deps,
which both agents ignored. The experiment failed to demonstrate the graph's
value because:

1. The fixture was too small (~46 files) for manual tracing to be impractical
2. Import chains were shallow (depth 2) and direct (no re-exports)
3. The task tested text search as much as structural knowledge

v3 fixes all three problems with a larger, deeper, indirection-heavy fixture
modeled on real bioinformatics repositories.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Fixture style | Bioinformatics (not web-app) | Proves value for target audience; mirrors real repos like SpatialCore-Dev |
| Target file | `src/core/metadata.py` | Core utility with high fan-out; cascades through annotation, preprocessing, analysis, plotting, pipelines |
| Blast radius depth | 4 | Deep enough that manual tracing is unreliable in 100-file project; shallow enough to validate ground truth |
| Focus | Python-only deps | User priority; markdown/config cross-type edges are noise files, not blast radius members |
| Prompt fairness | Same task text, different tools | Clean A/B variable isolation: the graph is the only difference |
| Agent B approach | Hybrid — CLAUDE.md + direct CLI | Agent B has project context from CLAUDE.md/KB_INDEX.md; prompt tells it to run `kb-graph traverse` directly |

## Fixture Structure (~100 files)

```
tests/fixtures/sample_project/
  src/
    core/
      __init__.py          # re-exports: from .metadata import MetadataManager
      metadata.py          # TARGET — defines MetadataManager class
      config.py            # leaf node, imported by metadata.py
      logging.py           # utility, imported by metadata.py
      exceptions.py        # custom exception hierarchy
    annotation/
      __init__.py          # re-exports from .ontology, .confidence
      ontology.py          # imports core.metadata directly
      confidence.py        # imports core.metadata directly
      markers.py           # imports .ontology (depth 2 via ontology)
      cell_types.py        # imports .confidence (depth 2 via confidence)
    preprocessing/
      __init__.py          # re-exports from .base
      base.py              # from core import metadata (via core/__init__.py re-export)
      normalization.py     # imports .base (depth 2 via base)
      qc.py                # imports .base (depth 2 via base)
      ingestion.py         # imports .normalization (depth 3)
      batch.py             # imports .qc (depth 3)
    analysis/
      __init__.py          # barrel file (no metadata connection)
      spatial.py           # imports preprocessing.base (depth 3 via base)
      clustering.py        # imports annotation.ontology (depth 2 via ontology)
      diffusion.py         # NO connection to metadata (noise)
      trajectory.py        # NO connection (noise)
    plotting/
      __init__.py          # barrel file (no metadata connection)
      heatmap.py           # imports analysis.spatial (depth 4 via spatial)
      volcano.py           # NO connection (noise)
      spatial_plot.py      # imports analysis.clustering (depth 3 via clustering)
      umap.py              # NO connection (noise)
    pipelines/
      __init__.py          # barrel file
      run_qc.py            # imports preprocessing.qc (depth 3 via qc)
      run_analysis.py      # imports analysis.spatial (depth 4 via spatial)
      run_plotting.py      # NO connection (noise)
  tests/
    __init__.py
    test_metadata.py       # imports core.metadata (depth 1 — greppable)
    test_config.py         # noise
    test_ontology.py       # noise
    test_normalization.py  # noise
    test_spatial.py        # noise
    test_clustering.py     # noise
    test_qc.py             # noise
    test_plotting.py       # noise
    test_ingestion.py      # noise
    test_batch.py          # noise
    conftest.py            # noise
  scripts/
    setup_env.sh           # noise
    run_pipeline.sh        # noise
    download_data.py       # noise
    validate_output.py     # noise
    benchmark.py           # noise
  docs/
    README.md              # noise (no wiki-links)
    architecture.md        # noise
    api_reference.md       # noise
    preprocessing_guide.md # noise
    analysis_tutorial.md   # noise
  configs/
    pipeline_config.yaml   # noise
    logging_config.yaml    # noise
    test_config.yaml       # noise
  R/
    spatial_stats.R        # noise
    visualization.R        # noise
    utils.R                # noise
    deconvolution.R        # noise
    bridge.R               # noise
```

Total: ~75 listed files. Additional noise files (empty `__init__.py` in
tests/scripts/docs, a `.phoamignore`, `.env.example`, `pyproject.toml`,
`setup.cfg`) pad to ~100. Exact count will be confirmed by `--dry-run`.

### Red herring files (mention "metadata" but are NOT dependents)

These files contain the word "metadata" in comments or strings but do NOT
import from `core.metadata`, so they are NOT in the blast radius:

- `scripts/download_data.py` — has `# Download sample metadata from GEO`
- `docs/preprocessing_guide.md` — mentions "metadata" in prose
- `configs/pipeline_config.yaml` — has `metadata_columns: [...]` as a config key
- `tests/conftest.py` — has `SAMPLE_METADATA = {...}` dict literal
- `src/analysis/trajectory.py` — has `# TODO: add metadata tracking`

These are designed to waste Agent A's time if it relies on `grep -r metadata`.

## Expected Blast Radius (19 files)

Target: `src/core/metadata.py`

| Depth | File | Import chain | Mentions "metadata"? |
|-------|------|-------------|---------------------|
| 1 | `src/core/__init__.py` | `from .metadata import MetadataManager` | YES |
| 1 | `src/annotation/ontology.py` | `from core.metadata import MetadataManager` | YES |
| 1 | `src/annotation/confidence.py` | `from core.metadata import MetadataManager` | YES |
| 1 | `tests/test_metadata.py` | `from core.metadata import MetadataManager` | YES |
| 2 | `src/annotation/__init__.py` | re-exports ontology, confidence | NO |
| 2 | `src/annotation/markers.py` | `from .ontology import ...` | NO |
| 2 | `src/annotation/cell_types.py` | `from .confidence import ...` | NO |
| 2 | `src/preprocessing/base.py` | `from core import metadata` (via __init__) | MAYBE (imports "core") |
| 3 | `src/preprocessing/__init__.py` | re-exports from .base | NO |
| 3 | `src/preprocessing/normalization.py` | `from .base import ...` | NO |
| 3 | `src/preprocessing/qc.py` | `from .base import ...` | NO |
| 3 | `src/analysis/clustering.py` | `from annotation.ontology import ...` | NO |
| 3 | `src/analysis/spatial.py` | `from preprocessing.base import ...` | NO |
| 3 | `src/plotting/spatial_plot.py` | `from analysis.clustering import ...` | NO |
| 4 | `src/preprocessing/ingestion.py` | `from .normalization import ...` | NO |
| 4 | `src/preprocessing/batch.py` | `from .qc import ...` | NO |
| 4 | `src/pipelines/run_qc.py` | `from preprocessing.qc import ...` | NO |
| 4 | `src/pipelines/run_analysis.py` | `from analysis.spatial import ...` | NO |
| 4 | `src/plotting/heatmap.py` | `from analysis.spatial import ...` | NO |

**Summary**: 19 files total. 4 at depth 1 (greppable). 15 at depth 2-4 (invisible to grep).

## Agent Prompts

### Agent A (no graph)

```
A breaking change is planned for src/core/metadata.py. Add
`# AFFECTED-BY: metadata.py` as the very first line of every Python
file that would be affected — include all transitive dependents. Do
not modify metadata.py itself. Do not explain, just make the changes.
```

### Agent B (with graph)

```
Read CLAUDE.md first. A breaking change is planned for
src/core/metadata.py. Run `kb-graph traverse metadata.py --depth 4`
to get the complete list of affected files. Add
`# AFFECTED-BY: metadata.py` as the very first line of every file
in the traverse output. Do not modify metadata.py itself. Do not
explain, just make the changes.
```

### Prompt design rationale

- Same task description, different tools — clean A/B isolation
- Agent A says "all transitive dependents" without specifying depth
- Agent B gets the exact CLI command — deterministic answer
- Both say "do not explain" to reduce time spent on output formatting
- Neither mentions specific file counts to avoid anchoring

## Experiment Infrastructure Changes

### File: `tests/test_agent_experiment.py`

1. **Replace all fixture data** — `ENHANCED_*`, `NEW_FILES`, `NOISE_FILES` dicts
   replaced with bioinformatics fixture content
2. **Update `EXPECTED_BLAST_RADIUS`** — 19 files grouped by depth (1-4)
3. **Update `PROMPT_A` and `PROMPT_B`** — as designed above
4. **Update `MARKER`** — `# AFFECTED-BY: metadata.py` (was `database.py`)
5. **Increase default timeout** — 180s → 300s
6. **4-level depth scoring** — extend summary to show misses at depth 1/2/3/4
7. **Add `--depth` CLI arg** — default 4, passed to kb-graph traverse in
   Agent B's prompt template and used for ground truth validation
8. **Validate ground truth in `--dry-run`** — run `kb-graph traverse
   metadata.py --depth 4` on the fixture and assert output matches
   `EXPECTED_BLAST_RADIUS` exactly

### Scoring (unchanged logic)

- **Recall** = expected files marked / total expected (19)
- **Precision** = correct marks / all marks
- **Perfect run** = 100% recall
- Depth-bucketed miss counts in summary

### Expected outcomes

- **Agent A**: 20-30% recall (finds depth-1 files via grep, misses depth 2-4)
- **Agent B**: 100% recall (graph gives the exact answer)
- **Agent A time**: likely hits timeout or ~200s+ trying to trace manually
- **Agent B time**: ~60-90s (read CLAUDE.md, run traverse, apply markers)

## Verification Plan

1. `python3 tests/test_agent_experiment.py --dry-run`
   - Builds fixture, runs kb-graph init, validates traverse output matches
     EXPECTED_BLAST_RADIUS
   - Confirms all 19 expected files exist in the fixture
   - Confirms red herring files exist but are NOT in traverse output
2. Run 1 trial with `--save-transcripts` to verify both agents execute
3. Run 5 trials to get statistical significance
4. Check that Agent B achieves 100% recall in all trials
5. Check that Agent A recall is consistently < 50%

## Experiment Results (2026-04-14) — FAILED TO DIFFERENTIATE

**1 trial, Sonnet 4.6, CLI 2.1.108**:

| Metric | Agent A (no graph) | Agent B (with graph) |
|--------|-------------------|---------------------|
| Recall | 100% (19/19) | 100% (19/19) |
| Precision | 100% | 100% |
| Time | 103.9s | 43.3s |
| Files missed | none | none |

**Agent A achieved perfect recall** — it traced all 19 transitive dependents
through `__init__.py` re-exports at depth 4 without any graph tooling.

**Why this failed**: The blast-radius marking task is fundamentally a
"trace Python imports" task, and Sonnet is excellent at reading Python
import statements and following them transitively. The fixture's import
chains, while structurally deep, use standard Python import patterns that
the agent can mechanically follow:

1. Read `metadata.py` → see who imports it (grep + file reading)
2. For each importer, read that file → see who imports *it*
3. Repeat until no new files are found

This is a deterministic, well-defined algorithm that a capable agent can
execute without any special tooling. The `__init__.py` re-exports and
relative imports add indirection but not opacity — the agent can still
read each file and trace the chain. Even 97 files is small enough for
an agent to exhaustively scan the `src/` tree.

**The only measurable difference was speed**: Agent B finished in 43.3s
(2.4x faster) because it got the answer from one `kb-graph traverse`
call instead of manually tracing imports. This is a real benefit but
not the dramatic recall gap needed to prove the graph's value.

### Pattern across all three attempts

| Version | Task | Result | Why it failed |
|---------|------|--------|---------------|
| v1 | Rename `db_url` → `database_url` | Both 40% | Text search problem — grep equally effective |
| v2 | Mark blast radius of `database.py` (46 files, depth 2) | Both 80% | Agent A traced imports manually; only missed markdown wiki-links |
| v3 | Mark blast radius of `metadata.py` (97 files, depth 4) | Both 100% | Agent A traced all Python imports manually in 104s |

**Conclusion**: The blast-radius marking task does not differentiate the
agents because Sonnet can trace Python import chains reliably. The
graph's unique value is NOT "finding transitive Python imports" — the
agent can already do that. The graph's value must lie in something the
agent *cannot* do by reading files: either information that is pre-computed
and costly to derive on-the-fly, or cross-type relationships that aren't
syntactically visible.

### Alternative task types for Phase 5 v4

The next iteration needs a task where the graph provides information that
is genuinely hard to derive by reading files. Candidates:

1. **Cross-language dependency tracing**: A fixture with Python + R + shell
   scripts where `source()` in R and `. script.sh` in shell create edges
   that Python-focused import tracing misses. The agent would need to
   understand R and shell sourcing conventions — the graph abstracts
   this away into a uniform edge format.

2. **"Which files are safe to delete?" (orphan detection)**: Ask the agent
   to identify all files with zero inbound edges. This requires exhaustive
   reverse-lookup across the entire project — checking every file to see
   if *any* other file references it. `kb-graph orphans` does this in one
   call. An agent would need to read every file and build its own mental
   graph — much slower and error-prone at scale.

3. **"Find the shortest path between two files"**: Ask the agent how
   file X and file Y are connected. `kb-graph path X Y` gives the exact
   chain. Without the graph, the agent must do a BFS through import
   statements — feasible but slow and easy to miss indirect paths.

4. **Time-constrained multi-file impact assessment**: Reduce the timeout
   drastically (e.g., 60s) so that Agent A doesn't have time to manually
   trace all imports. Agent B gets the answer instantly from traverse.
   This tests the speed advantage rather than the recall advantage.

5. **Scale the fixture to 500+ files**: At some point, manual import
   tracing becomes impractical within a 300s timeout. The current 97-file
   fixture is too small. A 500-file fixture with depth-6 chains might
   finally exceed the agent's tracing capacity.

6. **Wiki-link / cross-type task**: Build a fixture where the blast radius
   includes documentation files connected via `[[wiki-links]]` and config
   files referenced by path. These cross-type edges are invisible to
   `grep -r import` and represent a genuinely different class of dependency.

**Recommended next step**: Option 4 (time-constrained) or option 2 (orphan
detection) — both play to the graph's strengths and are less likely to be
solvable by brute-force file reading.

## Files to Modify

- `tests/test_agent_experiment.py` — full rewrite of fixture data, prompts,
  and scoring display
- `docs/phoam_paint/plan.md` — update Phase 5 section with v3 design and
  results (after experiment runs)

## Files NOT Modified

- `phoam_paint/kb_graph.py` — no changes needed; existing parser handles
  __init__.py re-exports, relative imports, and depth-N traverse correctly
- `tests/fixtures/sample_project/` — the original fixture stays as-is for
  Phase 1/1.5 mutation tests; the experiment creates enhanced copies in tmpdir
