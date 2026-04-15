# Phase 5 v4: Two Focused Experiments — Design Spec

> Redesigned experiment suite to prove kb-graph's value through two
> complementary tests: doc-graph impact analysis and code-level
> intelligence with function signatures.

## Context

Phase 5 v1–v3 all failed to differentiate Agent A (no graph) from
Agent B (with graph). Every experiment tested Python import tracing,
which Sonnet can do mechanically by reading files. The graph was just
a faster version of what the agent already does manually.

| Version | Task | Result | Root cause |
|---------|------|--------|------------|
| v1 | Rename `db_url` → `database_url` | Both 40% | Text search — grep equally effective |
| v2 | Mark blast radius (46 files, depth 2) | Both 80% | Agent A traced imports; only missed wiki-links |
| v3 | Mark blast radius (97 files, depth 4) | Both 100% | Agent A traced all imports in 104s |

### Key insight from analysis

The graph provides two capabilities that agents **cannot** replicate
by reading files:

1. **Wiki-link traversal in prose** — documents connected by
   `[[wiki-links]]` embedded in paragraphs have no import statements,
   no greppable patterns. The only way to find transitive connections
   is to parse every file for wiki-link syntax and BFS through them.
   The graph does this; agents don't.

2. **Pre-computed function-level metadata** — KB_INDEX.md with
   exported function signatures, class definitions, and file-level
   usage information gives Agent B immediate structural knowledge that
   Agent A must reconstruct by reading every file.

v4 tests each capability with a dedicated experiment.

---

## Experiment A: Doc-Graph Impact Analysis

### What it tests

Can the graph help an agent identify affected documents in a
wiki-link-connected knowledge base where there are no imports to
trace, no code to grep — just prose linked by `[[wiki-links]]`?

### Fixture: Data Analytics Platform (~35 files)

A fictional design document set for a data analytics platform.
Documents are interconnected via wiki-links. No code files participate
in the dependency chains — this is a purely doc-based knowledge graph.

```
docs/
  design/
    00-platform-overview.md     # hub — links to most other docs
    01-data-ingestion.md        # [[02-processing]], [[06-security]]
    02-processing-engine.md     # [[03-storage]], [[05-scheduling]], [[06-security]]
    03-storage-layer.md         # [[04-query-api]]
    04-query-api.md             # [[03-storage]]
    05-scheduling.md            # [[01-data-ingestion]], [[02-processing]]
    06-security-auth.md         # [[01-data-ingestion]], [[07-ui]]
    07-ui-dashboard.md          # leaf — no outbound links
    08-alerting.md              # [[07-ui]]
    09-open-questions.md        # [[00-platform-overview]]
    10-architecture.md          # [[01-data-ingestion]], [[02-processing]]
  reference/
    setup.md                    # [[10-architecture]]
    tool-catalog.md             # noise
    research-notes.md           # [[01-data-ingestion]], [[06-security]]
    design-notes.md             # [[02-processing]], [[03-storage]]
  guides/
    getting-started.md          # [[00-platform-overview]], [[setup.md]]
    admin-guide.md              # noise (mentions "processing" in text)
    performance-guide.md        # [[10-architecture]]
configs/
  platform_config.yaml          # config-ref: "docs/design/02-processing-engine.md"
  limits.yaml                   # config-ref: "docs/design/03-storage-layer.md"
  deploy_config.yaml            # noise
scripts/
  build.sh                      # noise
  deploy.sh                     # noise
README.md                       # [[00-platform-overview]]
CHANGELOG.md                    # noise (mentions "processing engine v2.1")
```

Total: ~35 files (11 design docs + 4 reference + 3 guides + 3 configs
+ 2 scripts + 2 root files + ~10 padding/noise files).

### Red herring files

Files that mention "processing" in text but do NOT wiki-link to
`02-processing-engine.md`:

- `guides/admin-guide.md` — mentions "data processing" in a paragraph
- `CHANGELOG.md` — mentions "processing engine v2.1" in a changelog entry
- `configs/deploy_config.yaml` — has `processing_threads: 8`

These are designed to waste Agent A's time if it relies on text search.

### Target

`docs/design/02-processing-engine.md`

### Expected blast radius (13 files)

| Depth | File | Connection |
|-------|------|------------|
| 1 | `docs/design/00-platform-overview.md` | `[[02-processing-engine]]` wiki-link |
| 1 | `docs/design/01-data-ingestion.md` | `[[02-processing-engine]]` wiki-link |
| 1 | `docs/design/05-scheduling.md` | `[[02-processing-engine]]` wiki-link |
| 1 | `docs/design/10-architecture.md` | `[[02-processing-engine]]` wiki-link |
| 1 | `docs/reference/design-notes.md` | `[[02-processing-engine]]` wiki-link |
| 1 | `configs/platform_config.yaml` | config-ref path |
| 2 | `README.md` | links to `00-platform-overview` |
| 2 | `docs/design/06-security-auth.md` | links to `01-data-ingestion` |
| 2 | `docs/design/09-open-questions.md` | links to `00-platform-overview` |
| 2 | `docs/guides/getting-started.md` | links to `00-platform-overview` |
| 2 | `docs/guides/performance-guide.md` | links to `10-architecture` |
| 2 | `docs/reference/research-notes.md` | links to `01-data-ingestion` |
| 2 | `docs/reference/setup.md` | links to `10-architecture` |

**Summary**: 13 files. 6 at depth 1, 7 at depth 2 (no depth 3 needed —
`01-data-ingestion.md` directly links to the target).
Plus ~20 noise files not in the blast radius.

### Agent prompts

**Agent A (no graph)**:

```
The processing engine (docs/design/02-processing-engine.md) is being
completely redesigned. Add `<!-- AFFECTED -->` as the very first line
of every file that would need updating — include all transitive
dependents at any depth. A file is a dependent if it contains a
[[wiki-link]] to the target OR to any other affected file. Config
files that reference affected files by path are also dependents. Do
not modify 02-processing-engine.md itself. Do not explain, just make
the changes.
```

**Agent B (with graph)**:

```
Read CLAUDE.md first. The processing engine
(docs/design/02-processing-engine.md) is being completely redesigned.
Run `kb-graph traverse docs/design/02-processing-engine.md --depth 3`
to get the complete list of affected files. Add `<!-- AFFECTED -->`
as the very first line of every file in the traverse output. Do not
modify 02-processing-engine.md itself. Do not explain, just make the
changes.
```

### Why this differentiates

1. **No imports to trace** — connections are `[[wiki-links]]` embedded
   in paragraphs of prose. No `from X import Y` pattern to follow.

2. **No grep shortcut** — `grep -r "02-processing"` finds depth-1
   files but NOT depth-2/3 files. `01-data-ingestion.md` links to
   `05-scheduling.md` which links to `02-processing-engine.md` — but
   `01-data-ingestion.md` never mentions "processing" at all.

3. **O(n²) scaling** — to find depth-2 links, Agent A must read every
   file looking for wiki-links to each depth-1 file. Then repeat for
   depth 3. With 35 files and 3 depths, this is hundreds of file reads
   that the agent must reason about correctly.

4. **Config-ref edges** — `platform_config.yaml` references the target
   by file path. Agent A would need to search config files for path
   strings, which is outside normal code-tracing behavior.

### Expected outcomes

- **Agent A**: 30-50% recall (finds depth-1 wiki-links via grep, misses
  depth-2/3 transitive links and config-ref)
- **Agent B**: 100% recall (graph traverse gives exact answer)
- **Agent A time**: likely hits timeout tracing wiki-links manually
- **Agent B time**: ~30-60s (read CLAUDE.md, run traverse, apply markers)

### Scoring

- **Recall** = expected files marked / total expected (13)
- **Precision** = correct marks / all marks
- **Depth-bucketed miss counts** in summary
- **Perfect run** = 100% recall

---

## Experiment B: Code Intelligence — Function-Level Knowledge

### What it tests

Can richer graph output (function signatures, exported symbols in
KB_INDEX.md) help an agent find and fix a breaking function signature
change faster and more accurately than reading files manually?

### Tool enhancement required

Before this experiment, enhance `kb_graph.py`'s Python parser to
extract:

1. **Function signatures** — top-level `def` lines with parameters
   and type hints
2. **Class definitions** — top-level `class` lines with base classes
3. **Exported symbols** — all top-level functions and classes per file

KB_INDEX.md gains a richer format per file:

```markdown
- **transform.py** — Data transformation utilities
  - exports: `apply_transform(data: DataFrame, config: TransformConfig, strict: bool = True) -> DataFrame`
  - exports: `validate_schema(data: DataFrame, schema: Dict[str, str]) -> bool`
  - exports: `class TransformConfig`
  - imports: `core.config`, `core.logging`
  - used by: `preprocessing.normalize`, `preprocessing.filter`, `analysis.aggregate`, `pipeline.run`, `io.writers`
```

Implementation approach: regex-based extraction of `def` and `class`
lines from Python source. NOT full AST parsing — that is Phase 6 work.
The regex approach is sufficient for well-formatted Python code (which
the fixture guarantees) and keeps kb_graph.py stdlib-only.

### Fixture: Data Pipeline Library (~80 files)

A fictional Python data pipeline library with cross-cutting function
dependencies.

```
src/
  core/
    __init__.py          # re-exports: from .transform import apply_transform, ...
    transform.py         # TARGET — exports apply_transform(), validate_schema(), TransformConfig
    config.py            # leaf — PipelineConfig class
    logging.py           # leaf — get_logger()
    exceptions.py        # leaf — custom exceptions
  preprocessing/
    __init__.py          # re-exports from .normalize, .clean
    normalize.py         # calls apply_transform(data, config, strict=True)
    clean.py             # calls validate_schema(data, schema)
    filter.py            # calls apply_transform(data, config)  [default args only]
    batch.py             # imports normalize (depth 2)
  analysis/
    __init__.py
    aggregate.py         # calls apply_transform(data, config, strict=False)
    correlate.py         # calls validate_schema(data, schema)
    cluster.py           # imports aggregate (depth 2)
    report.py            # imports cluster (depth 3)
  pipeline/
    __init__.py
    run.py               # orchestrator — calls apply_transform() AND validate_schema()
    schedule.py          # imports run (depth 2)
    monitor.py           # noise
  io/
    __init__.py
    readers.py           # noise
    writers.py           # calls validate_schema(data, schema)
    formats.py           # noise
  plotting/
    __init__.py
    charts.py            # imports analysis.aggregate (depth 3)
    export.py            # noise
tests/
  __init__.py
  test_transform.py      # calls apply_transform(strict=True) and apply_transform(strict=False)
  test_normalize.py      # noise
  test_aggregate.py      # noise
  test_pipeline.py       # calls apply_transform(data, test_config, strict=False)
  test_writers.py        # noise
  test_clean.py          # noise
  test_filter.py         # noise
  test_correlate.py      # noise
  conftest.py            # noise (mentions "transform" in comments)
configs/
  pipeline.yaml          # config-ref: "src/pipeline/run.py"
  defaults.yaml          # config-ref: "src/core/config.py"
  test_config.yaml       # noise
docs/
  architecture.md        # [[transform.py]], [[run.py]]
  api-reference.md       # [[transform.py]]
  tutorial.md            # noise (mentions "transform" in prose)
  contributing.md        # noise
scripts/
  run_pipeline.sh        # noise
  setup_env.sh           # noise
  benchmark.py           # noise
```

~55 listed + `__init__.py` files + additional noise = ~80 total.

### Red herring files

Files that mention "transform" or "apply_transform" in comments/strings
but are NOT call sites:

- `tests/conftest.py` — `SAMPLE_TRANSFORM_CONFIG = {...}` dict literal
- `docs/tutorial.md` — mentions "apply_transform" in prose explanation
- `scripts/benchmark.py` — `# TODO: benchmark apply_transform performance`
- `configs/test_config.yaml` — has `transform_mode: strict`

### Target

`src/core/transform.py` — specifically the `apply_transform()` function.

### The breaking change

`apply_transform()` signature changes:

```python
# Before:
def apply_transform(data: DataFrame, config: TransformConfig, strict: bool = True) -> DataFrame

# After:
def apply_transform(data: DataFrame, config: TransformConfig, mode: str = "strict") -> DataFrame
```

The `strict: bool` parameter is replaced by `mode: str`. Every call
site passing `strict=True` → `mode="strict"`, `strict=False` →
`mode="lenient"`. Call sites using the default (not passing `strict`
at all) need no change because the default behavior is preserved.

### Expected call sites requiring changes (ground truth)

| File | Call syntax | Change needed |
|------|------------|---------------|
| `preprocessing/normalize.py` | `apply_transform(data, config, strict=True)` | → `mode="strict"` |
| `analysis/aggregate.py` | `apply_transform(data, config, strict=False)` | → `mode="lenient"` |
| `pipeline/run.py` | `apply_transform(data, cfg, strict=True)` | → `mode="strict"` |
| `tests/test_transform.py` | `apply_transform(df, config, strict=True)` | → `mode="strict"` |
| `tests/test_transform.py` | `apply_transform(df, config, strict=False)` | → `mode="lenient"` |
| `tests/test_pipeline.py` | `apply_transform(data, test_config, strict=False)` | → `mode="lenient"` |

**Files that call `apply_transform()` but need NO change** (default args):
- `preprocessing/filter.py` — `apply_transform(data, config)` — no `strict` arg

**Files that DON'T call `apply_transform()` at all** (not call sites):
- `preprocessing/clean.py` — calls `validate_schema()`, not `apply_transform()`
- `analysis/correlate.py` — calls `validate_schema()`, not `apply_transform()`
- `io/writers.py` — calls `validate_schema()`, not `apply_transform()`
- All depth-2+ files (batch.py, cluster.py, schedule.py, etc.) — they
  import modules that use transform, but don't call it themselves

### Agent prompts

**Agent A (no graph)**:

```
The function `apply_transform()` in `src/core/transform.py` has a
breaking parameter change: `strict: bool = True` is now
`mode: str = "strict"`. Update every call site in the project:
`strict=True` → `mode="strict"`, `strict=False` → `mode="lenient"`.
Call sites using the default (not passing `strict`) need no change.
Do not modify `src/core/transform.py` itself. Do not explain, just
make the changes.
```

**Agent B (with graph)**:

```
Read CLAUDE.md first, then read KB_INDEX.md. The function
`apply_transform()` in `src/core/transform.py` has a breaking
parameter change: `strict: bool = True` is now
`mode: str = "strict"`. KB_INDEX.md lists every file that imports
transform.py — check those files for call sites. Update every call
site: `strict=True` → `mode="strict"`, `strict=False` →
`mode="lenient"`. Call sites using the default (not passing `strict`)
need no change. Do not modify `src/core/transform.py` itself. Do not
explain, just make the changes.
```

### Why this differentiates

1. **KB_INDEX.md front-loads structural knowledge** — Agent B
   immediately knows which files import `transform.py` and what the
   exported signature is. Agent A must grep and read files to build
   this understanding.

2. **Precision matters, not just recall** — Agent A might grep for
   `apply_transform` and find all files, but must then READ each file
   to determine: (a) does it actually call the function? (b) does it
   pass `strict`? (c) what value? This requires careful per-file
   analysis. Agent B starts with a focused list of importers.

3. **Red herrings penalize imprecision** — files mentioning
   "transform" in comments waste Agent A's time. Files calling
   `validate_schema()` (not `apply_transform()`) are false positives
   if the agent only checks imports.

4. **Speed advantage compounds** — Agent B reads 1 file (KB_INDEX.md)
   to get the dependency map, then targets ~6 files. Agent A must
   search broadly then narrow down.

### Expected outcomes

- **Agent A**: 70-90% recall, lower precision (might miss test files
  or make incorrect substitutions in files that don't need changes)
- **Agent B**: 100% recall, 100% precision (focused list from KB_INDEX)
- **Agent A time**: 90-150s (grep + read + reason per file)
- **Agent B time**: 40-70s (read KB_INDEX + targeted fixes)

### Scoring

Each call site is scored independently:

- **Correct fix**: `strict=True` → `mode="strict"` or
  `strict=False` → `mode="lenient"` applied at the right location
- **Missed fix**: call site with `strict=` left unchanged
- **Wrong fix**: incorrect substitution (e.g., `strict=False` →
  `mode="strict"`)
- **False positive**: file modified that needed no changes, or
  `apply_transform()` call with default args had `mode=` added

Metrics:

- **Recall** = correct fixes / total needed (6)
- **Precision** = correct fixes / (correct fixes + wrong fixes +
  false positives)
- **Perfect run** = 6/6 correct fixes, 0 wrong fixes, 0 false
  positives

---

## Implementation Dependencies

### For Experiment A (no tool changes needed)

Experiment A uses only wiki-link and config-ref edges, which the
current `kb_graph.py` already handles. Implementation:

1. Build fixture files with wiki-link content
2. Write experiment runner (adapt from `test_agent_experiment.py`)
3. Validate with `--dry-run`
4. Run trials

### For Experiment B (tool enhancement needed)

Experiment B requires enhanced KB_INDEX.md output. Implementation:

1. **Enhance Python parser** — add regex extraction of `def` and
   `class` lines from Python files. Store as node metadata:
   ```python
   {
       "path": "src/core/transform.py",
       "type": "code",
       "description": "Data transformation utilities",
       "group": "src/core",
       "exports": [
           "apply_transform(data: DataFrame, config: TransformConfig, strict: bool = True) -> DataFrame",
           "validate_schema(data: DataFrame, schema: Dict[str, str]) -> bool",
           "class TransformConfig",
       ]
   }
   ```

2. **Enhance KB_INDEX.md writer** — include `exports:` lines for each
   Python file that has them.

3. **Build fixture** with realistic function signatures and call sites.

4. **Write experiment runner** with call-site-aware scoring (not just
   marker detection — verify actual code substitutions).

5. Validate with `--dry-run`, run trials.

### Shared infrastructure

Both experiments share:
- CLI arg parsing (--trials, --model, --save-transcripts, --dry-run)
- Agent invocation (claude CLI subprocess)
- Scoring framework (recall, precision, timing)
- Result output format (table + JSON)

Options:
- **Single script with `--experiment A|B`** flag
- **Two separate scripts** sharing a common module

Recommendation: two separate scripts (`test_experiment_a.py`,
`test_experiment_b.py`) for clarity. Extract shared utilities into a
helper module if duplication exceeds ~50 lines.

---

## Phase 6: Richer Code Intelligence (future work)

Phase 6 expands the minimum-viable function extraction from
Experiment B into a full code intelligence layer.

### 6.1 AST-Based Python Parsing

Replace regex-based `def`/`class` extraction with `ast` module
parsing for reliable extraction of:

- Function signatures with full type annotations (including complex
  types: `Union`, `Optional`, `Literal`, `Dict[str, Any]`)
- Decorator detection (`@staticmethod`, `@classmethod`, `@property`)
- Nested class/function handling
- Default value extraction
- Docstring extraction (first line only, for descriptions)

### 6.2 Call-Site Indexing

For each exported function, scan all tracked Python files for call
sites. Record:

- File path and line number
- Exact call syntax (positional vs keyword args)
- Whether the call uses the default for each parameter

Include in KB_INDEX.md:

```markdown
- **transform.py** — Data transformation utilities
  - exports: `apply_transform(data: DataFrame, config: TransformConfig, strict: bool = True) -> DataFrame`
  - call sites:
    - `preprocessing/normalize.py:47` — `apply_transform(data, config, strict=True)`
    - `analysis/aggregate.py:23` — `apply_transform(data, config, strict=False)`
    - `pipeline/run.py:89` — `apply_transform(data, cfg, strict=True)`
```

### 6.3 Return Value Contract Tracking

Extract return type annotations and, for functions returning `Dict`,
scan the function body for dict key assignments to infer the return
value shape:

```markdown
- exports: `check_status(data) -> Dict[str, Any]`
  - return keys: `state` (str), `source` (Optional[str]), `usable` (bool)
```

### 6.4 Constant/Variable Tracking

Detect module-level constant definitions (ALL_CAPS names) and track
where they're imported:

```markdown
- exports: `MAX_RETRIES = 3` (int)
  - used by: `pipeline/run.py:12`, `io/writers.py:8`
```

### 6.5 R Parser

Parse R source files for dependency edges:

- `source("path/to/file.R")` → import edge
- `source('path/to/file.R')` → import edge
- Path resolution relative to the R file's directory

### 6.6 Shell Parser

Parse shell scripts for dependency edges:

- `source path/file.sh` → import edge
- `. path/file.sh` → import edge
- `python3 path/script.py` → invocation edge
- `Rscript path/file.R` → invocation edge

### 6.7 Cross-Language Call Tracking

Detect Python→R connections through subprocess patterns:

- `subprocess.run(["Rscript", "path"])` → edge to R file
- `run_r_script("path")` → edge to R file (if function is known)

This requires a two-pass approach: first identify bridge functions
(like `run_r_script`), then scan for their call sites with path
arguments.

### Phase 6 scope notes

- Phases 6.1–6.4 enhance Python-only intelligence
- Phases 6.5–6.7 add cross-language support
- Each sub-phase is independently useful and testable
- AST parsing (6.1) is the foundation — do it first
- Call-site indexing (6.2) is the highest-value addition for the
  "what breaks?" use case
- R and Shell parsers (6.5–6.6) are the highest-value additions for
  bioinformatics repos specifically

---

## Files to Create/Modify

### New files

- `tests/test_experiment_a.py` — Experiment A runner
- `tests/test_experiment_b.py` — Experiment B runner
- `docs/phoam_paint/phase5_v4_design.md` — this spec

### Modified files

- `phoam_paint/kb_graph.py` — add function/class extraction to Python
  parser, update KB_INDEX.md writer (for Experiment B)
- `docs/phoam_paint/plan.md` — update Phase 5 v4 and add Phase 6
  sections

### Files NOT modified

- `tests/test_agent_experiment.py` — v3 experiment stays as-is for
  reference
- `tests/fixtures/sample_project/` — original fixture unchanged
- `tests/test_graph_mutations.py` — Phase 1.5 tests unchanged
- `tests/test_generated_graph.py` — Phase 2 tests unchanged

---

## Experiment Results (2026-04-15)

**Environment**: Claude CLI 2.1.109, Sonnet 4.6 (default model), Ubuntu via WSL2 on Windows 11

### Experiment A: Doc-Graph Impact Analysis

**1 trial** (+ 1 earlier trial that crashed during summary but produced
results):

| Metric | Agent A (no graph) | Agent B (with graph) |
|--------|-------------------|---------------------|
| Recall | 100% (13/13) | 100% (13/13) |
| Precision | 100% | 100% |
| Time | 87.1s | 35.7s |
| Files missed | none | none |

**Earlier trial** (crashed in summary code before JSON save due to
`DEPTH_GROUPS` KeyError — bug fixed mid-session):

| Metric | Agent A | Agent B |
|--------|---------|---------|
| Recall | 92% (12/13) | 100% (13/13) |
| Time | 50.5s | 32.7s |
| Missed | `docs/design/06-security-auth.md` (depth 2) | none |

**Analysis**: The saved trial shows no recall difference — Agent A
traced all 13 wiki-linked files manually in 87.1s. Agent B finished
in 35.7s (2.4x faster) by running `kb-graph traverse` once. The
earlier trial (not saved to JSON) showed Agent A missing one depth-2
file, suggesting the graph-less approach has some variance in recall
on wiki-link tasks, but a single miss in one of two runs is not
statistically significant.

**Agent A strategy** (from transcript): Agent A found all 13 files by
reading each document, identifying `[[wiki-links]]`, and following
them transitively. It organized results by depth and found even the
config YAML reference to the target path. The wiki-link task was
harder than Python imports (no `grep -r import` shortcut), but
Sonnet's ability to parse markdown wiki-link syntax was sufficient
to trace the full graph manually.

**Agent B strategy** (from transcript): Read CLAUDE.md, ran
`kb-graph traverse docs/design/02-processing-engine.md --depth 3`,
got the complete file list, applied markers. Deterministic and fast.

### Experiment B: Code Intelligence — Signature Change

**1 trial**:

| Metric | Agent A (no graph) | Agent B (with graph) |
|--------|-------------------|---------------------|
| Recall | 100% (6/6) | 100% (6/6) |
| Precision | 86% (6/7) | 86% (6/7) |
| Time | 32.3s | 56.9s |
| False positives | `docs/tutorial.md` | `docs/tutorial.md` |

**Analysis**: Both agents found all 6 call sites and both made the
same false positive — updating `strict=True` in `docs/tutorial.md`'s
code example, which the scoring script counted as a false positive
(tutorial examples aren't real call sites). Agent A was actually
*faster* (32.3s vs 56.9s) because it went straight to grepping for
`apply_transform` while Agent B first read CLAUDE.md and KB_INDEX.md.

**Agent A strategy**: Grepped for `apply_transform`, read each file,
applied the parameter substitution. Simple and effective — the
function name is unique enough that grep finds all call sites
directly.

**Agent B strategy**: Read CLAUDE.md, then KB_INDEX.md (which lists
importers and exports), identified files importing `transform.py`,
checked each for `apply_transform` calls, applied substitutions.
The extra KB_INDEX.md reading step added overhead without improving
results.

### Verdict: FAILED TO DIFFERENTIATE

Neither experiment produced the expected recall gap between agents.

| Experiment | Expected | Actual |
|-----------|----------|--------|
| A (doc-graph) | A: 30-50%, B: 100% | Both 100% (saved trial) |
| B (code intel) | A: 70-90%, B: 100% | Both 100% |

### Pattern across all five attempts (v1–v4)

| Version | Task | Result | Why it failed |
|---------|------|--------|---------------|
| v1 | Rename `db_url` → `database_url` | Both 40% | Text search — grep equally effective |
| v2 | Mark blast radius of `database.py` (46 files) | Both 80% | Agent A traced imports manually |
| v3 | Mark blast radius of `metadata.py` (97 files, depth 4) | Both 100% | Agent A traced all imports in 104s |
| v4-A | Mark wiki-link blast radius (13 files, depth 3) | Both 100% | Agent A parsed wiki-links manually |
| v4-B | Update `apply_transform()` call sites (6 sites) | Both 100% | Grep finds the function name directly |

### Why v4 failed

**Experiment A** tested wiki-link traversal — a genuinely different
edge type from Python imports. But the fixture was too small (33 files,
13 in blast radius) and the wiki-link syntax (`[[name]]`) is regular
enough for an agent to parse and trace manually. The hypothesis that
"no imports = no grep shortcut" was wrong — the agent adapted by
grepping for `[[` and reading each file.

**Experiment B** tested function-level knowledge from KB_INDEX.md. But
the task (find call sites of a uniquely-named function) is solvable
by grepping for the function name. KB_INDEX.md provides the same
information as `grep -r apply_transform` — file-level import edges
plus function names. The graph adds no information that isn't
recoverable in a single grep.

### What would actually work

The graph's value is **not** "finding things" — Sonnet can find things
by reading files. The graph's value is **pre-computed transitive
closure at scale**. Future experiments should test:

1. **Scale**: 500+ files where manual BFS exceeds the timeout
2. **Time pressure**: 30-60s timeout where only the pre-computed answer
   is fast enough
3. **Multi-hop queries**: "What is the shortest path between X and Y?"
   where BFS through files is error-prone
4. **Aggregate queries**: "List all orphan files" — requires checking
   every file's inbound edges, not just following one chain
