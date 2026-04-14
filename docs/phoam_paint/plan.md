# phoam_paint — Spec & Implementation Plan

> Auto-generated knowledge graph for any repo. Point it at a directory, get a
> living map of how every file connects to every other file.

---

## 0. Current State (updated 2026-04-14)

**Status**: Phase 5 v3 implemented and dry-run validated. Bioinformatics
fixture with 97 files, 19 in blast radius at depth 4. Ground truth
matches `kb-graph traverse` output perfectly. Ready for experiment runs.

**Key files**:
- `phoam_paint/kb_graph.py` — the tool (single file, ~2050 lines, stdlib only)
- `phoam_paint/install.sh` — copies kb_graph.py to `~/.local/bin/kb-graph`
- `phoam_paint/uninstall.sh` — removes `~/.local/bin/kb-graph`
- `tests/fixtures/sample_project/` — fixture project with known graph properties (10 nodes, 13 edges)
- `tests/test_graph_mutations.py` — Phase 1.5 mutation tests (20 tests)
- `tests/test_generated_graph.py` — Phase 2 generated-graph correctness tests (28 tests, 100-node project)
- `tests/test_agent_experiment.py` — Phase 5 v3 A/B experiment script (97-file bioinformatics fixture, depth-4 import chains, --depth, --dry-run)
- `tests/experiment_transcripts/` — agent transcripts from 5 trials
- `docs/phoam_paint/plan.md` — this file (spec + build order)
- `docs/phoam_paint/foam_paint_reference.md` — detailed parser/output reference
- `docs/phoam_paint/check_graph_reference.md` — `/check_graph` skill reference content

**What works now**:
```bash
# Install globally
./phoam_paint/install.sh          # or: ./install.sh phoam_paint
# Uninstall globally
./phoam_paint/uninstall.sh        # or: ./uninstall.sh phoam_paint

# Set up a project
kb-graph init /path/to/repo
# Rebuilds graph, installs hook, CLAUDE.md rules, /check_graph skill, .gitignore

kb-graph rebuild tests/fixtures/sample_project/
# Produces KB_INDEX.md + graph.html in the target directory
# Output: 10 nodes, 13 edges, 2 orphans

kb-graph neighbors config.py --path tests/fixtures/sample_project/
kb-graph traverse database.py --path tests/fixtures/sample_project/
kb-graph path api-design.md config.py --path tests/fixtures/sample_project/
kb-graph orphans --path tests/fixtures/sample_project/
kb-graph analyze --path tests/fixtures/sample_project/

kb-graph uninit /path/to/repo
# Confirms, then reverses everything init did
```

**How to call the graph engine from Python** (for tests):
```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from phoam_paint.kb_graph import build_graph, write_kb_index, write_graph_html
from phoam_paint.kb_graph import resolve_node, build_adjacency, bfs_blast_radius, bfs_shortest_path

graph = build_graph("/path/to/repo")
# graph = {"nodes": {path: {description, group, type}, ...}, "edges": [{from, to, type, section}, ...]}
```

**What's stubbed**: nothing — all commands are implemented.

**To resume**: Run `python3 tests/test_agent_experiment.py --dry-run` to
verify fixture health, then `python3 tests/test_agent_experiment.py --trials 5
--save-transcripts` for the full experiment. Review Phase 5 v3 section below
for design rationale.

---

## 1. What It Is

`kb_graph.py` — a single Python file (stdlib only, Python 3.10+) that scans a
git repo, discovers all code and documentation files, parses their relationships
(imports, wiki-links, config references), and produces two outputs:

- **`KB_INDEX.md`** — a structured index of every file and its connections,
  designed for coding agents to read before making changes
- **`graph.html`** — an interactive D3.js force-directed visualization of the
  dependency graph, designed for humans to browse

The tool also provides CLI query commands for blast-radius analysis, pathfinding,
and orphan detection.

## 2. Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Single file | Yes | No package infrastructure, no imports to manage, copy-and-run |
| Stdlib only | Yes | No `pip install` dependencies, runs on any Python 3.10+ system |
| Auto-detection | Yes | Walks the tree, detects languages by extension, no config needed |
| Config file | Optional `.phoamignore` only | Gitignore syntax for excluding directories. No other config. |
| graph.html | Mandatory output | The user explicitly requires visualization as a core deliverable |
| D3.js via CDN | Yes | Keeps the HTML self-contained (one file), avoids bundling JS |
| Init command | All-in-one | Sets up hook, CLAUDE.md rules, check_graph skill — everything embedded in kb_graph.py |
| check_graph | **Skill**, not command | Skills (`.claude/skills/`) are agent-invocable — the agent can run check_graph autonomously before multi-file changes. Commands (`.claude/commands/`) are user-invoked only. **Do not change this back to a command.** |

### What we learned from references

| Reference | What we adopted | What we skipped |
|-----------|----------------|-----------------|
| **Graphify** | Edge provenance tagging, summary report concept, incremental rebuild idea | LLM inference, tree-sitter AST, NetworkX dependency, multimedia |
| **KB_Index gist** | "Always read the index first" routing pattern | Formal ID dictionaries, JSONL facts, multi-file KB structure |
| **Foam** | Basename-first wiki-link resolution, section links as edge metadata, backlinks as inverted adjacency | VS Code dependency, extension-based workflow |
| **Obsidian** | `[[file]]`, `[[file#heading]]`, `[[file\|display]]` syntax; shortest-path resolution; local graph view concept | Block references (`^blockid`), unlinked mentions (too expensive) |

### Wiki-link resolution rules

1. `[[filename]]` — match by basename (without extension), search entire scanned tree
2. `[[filename#section]]` — edge to file, section stored as edge metadata (not a separate node)
3. `[[path/to/file.py]]` — if link contains `/` and a file extension, treat as direct path reference
4. Ambiguous names (multiple files with same basename) — warn during rebuild, require path-qualified link to disambiguate

## 3. CLI Interface

```bash
# ── SETUP ─────────────────────────────────────────────
# Run once per project. Does everything.
kb-graph init /path/to/repo

# What init does:
#   1. Scans the repo, builds the graph
#   2. Generates KB_INDEX.md at repo root
#   3. Generates graph.html at repo root
#   4. Creates .claude/skills/check_graph/SKILL.md (agent-invocable skill)
#   5. Creates pre-commit hook + sets git config core.hooksPath
#   6. Appends knowledge-graph rules to CLAUDE.md (creates if missing)
#   7. Adds graph.html to .gitignore

# ── REBUILD ───────────────────────────────────────────
# Regenerate KB_INDEX.md + graph.html from current state.
# This is what the pre-commit hook calls.
kb-graph rebuild [/path/to/repo]          # defaults to cwd

# ── QUERY ─────────────────────────────────────────────
kb-graph neighbors <node>                 # direct connections (depth 1)
kb-graph traverse <node> [--depth N]      # blast radius (default depth 2)
kb-graph path <from> <to>                 # shortest path between two nodes
kb-graph orphans                          # files with no inbound or outbound edges
kb-graph analyze                          # stats: node/edge counts, most-connected nodes

# ── TEARDOWN ──────────────────────────────────────────
# Reverse everything init did. Clean exit, no residue.
kb-graph uninit [/path/to/repo]           # defaults to cwd

# What uninit does:
#   1. Removes KB_INDEX.md
#   2. Removes graph.html
#   3. Removes .claude/skills/check_graph/SKILL.md
#   4. Removes the pre-commit hook (or just the phoam_paint block if
#      the hook file contains other hooks)
#   5. Reverts git config core.hooksPath (only if we set it)
#   6. Removes the "## Knowledge Graph Rules" section from CLAUDE.md
#      (leaves the rest of CLAUDE.md intact)
#   7. Removes the graph.html line from .gitignore
#   8. Removes .phoamignore if it exists
#   Confirms before acting. Does NOT remove kb-graph itself from
#   ~/.local/bin/ — that's what uninstall.sh is for.
```

All query commands operate on the graph built from the current repo state
(they run a scan internally, no cached state file).

## 4. Auto-Detection

### File discovery

- Walks the entire directory tree from the given root
- **Built-in ignore list**: `.git`, `__pycache__`, `node_modules`, `.venv`,
  `venv`, `dist`, `build`, `.tox`, `.mypy_cache`, `.pytest_cache`, `egg-info`
- **`.phoamignore`** (optional, at repo root): additional exclusions using
  gitignore syntax (e.g., `data/`, `raw_sequences/`, `vendor/`)
- Also respects `.gitignore` if present (files git ignores shouldn't be in the graph)

### Parsers (by file extension)

| Extension | Parser | What it extracts |
|-----------|--------|-----------------|
| `.py` | Python imports | `import x`, `from x import y`, relative imports, `# Design: [[link]]` comments |
| `.md` | Wiki-links | `[[filename]]`, `[[file#section]]`, `[[path/to/file.ext]]` |
| `.R` | R source | `source("path")`, `library()` for local packages |
| `.sh`, `.bash` | Shell source | `source path`, `. path`, script invocations |
| `.yaml`, `.yml`, `.json`, `.toml` | Config refs | String values that match tracked file paths |
| `.nf` | Nextflow | `include { process } from './path'` |

Parsers are functions inside `kb_graph.py`. Adding a new language = adding one
function. The dispatcher maps extensions to parser functions.

### Node metadata

```python
{
    "path": "src/api/routes.py",           # relative to repo root
    "type": "code",                         # code | doc | config | asset
    "description": "REST API route defs",   # first docstring/heading/comment
    "group": "src/api",                     # for KB_INDEX sections and viz colors
}
```

### Edge metadata

```python
{
    "from": "src/api/routes.py",
    "to": "src/core/database.py",
    "type": "import",                       # import | wiki-link | config-ref
    "section": None,                        # populated for [[file#section]] links
}
```

### Component grouping (the `group` field)

Used for KB_INDEX.md section headers and graph.html node colors. Derived from
file path:

- Files in a top-level directory → group = that directory (e.g., `docs`, `scripts`)
- Files one level deep in `src/` → group = `src/<subdir>` (e.g., `src/api`, `src/core`)
- Files at repo root → group = `root`
- Target ~8-12 groups for readable output and distinguishable colors

## 5. Output Formats

### KB_INDEX.md

```markdown
# KB_INDEX.md
> Auto-generated by kb-graph — do not edit manually.
> Last rebuilt: 2026-04-10 14:32:07 UTC | Nodes: 24 | Edges: 41 | Orphans: 2

---

## src/core

- **database.py** — connection pool and query helpers
  - imports: `config.settings`
  - used by: `api.routes`, `api.auth`, `workers.ingest`

- **config.py** — used by 9 modules

## src/api

- **routes.py** — REST API route definitions
  - imports: `core.database`, `core.config`, `.auth`, `.serializers`
  - used by: `main`
  - docs: [[api-design#endpoints]]

## docs

- **api-design.md** — API design spec
  - links to: [[routes.py]], [[auth.py]], [[database.py]]

## Orphans

- **old_utils.py** — no connections (candidate for removal)
```

Rules:
- Grouped by component (the `group` field)
- Code files show: description, imports (local only), used-by, linked docs
- Doc files show: description, links-to
- Heavily-imported modules (used by 5+) show count, not full list
- Orphans listed in a dedicated section at the bottom
- Header shows stats: node count, edge count, orphan count, timestamp

### graph.html

Self-contained HTML file. Requirements:

- D3.js v7 loaded from CDN (`https://d3js.org/d3.v7.min.js`)
- Graph data embedded as JSON literal in the HTML
- Dark theme background (`#0d1117`)
- Force-directed layout with drag, zoom, collision detection
- Nodes colored by component group (one color per group from a 10-color palette)
- Node radius scaled by degree (more connections = larger)
- Three edge styles: solid = import, dashed = wiki-link, dotted = config-ref
- **Click a node**: highlight blast radius (depth 2), dim unrelated nodes,
  show info panel with file path, description, imports, used-by, risk level
- **Click background**: reset view
- **Legend**: component color swatches + edge type styles
- **Stats bar**: node count, edge count, orphan count
- Color palette (dark-background-friendly):
  ```
  #58a6ff, #3fb950, #d29922, #f85149, #bc8cff,
  #f778ba, #39d2c0, #ff9a3c, #56d364, #e06c9f
  ```

### traverse output (blast radius)

```
BLAST RADIUS: core/database.py

Depth 0 (the change)
  └── core/database.py

Depth 1 (direct dependents — MUST review)
  ├── api/routes.py ────── imports database
  │     L12: from core.database import get_connection
  │     L47: conn = get_connection()
  ├── api/auth.py ─────── imports database
  │     L8:  from core.database import get_connection
  └── workers/ingest.py ── imports database
        L5:  from core import database

Depth 2 (transitive — CHECK for breakage)
  ├── main.py ───────────── imports api.routes
  └── docs/api-design.md ── wiki-links to [[database.py]]

Summary: 1 changed → 3 direct → 2 transitive | Risk: HIGH (3 groups in radius)
```

For each file in the blast radius, grep for the target node's basename and show
matching lines (capped at 5 per file). Risk = number of distinct groups in
the radius: 1 = LOW, 2 = MEDIUM, 3+ = HIGH.

## 6. init — What Gets Embedded

Everything `init` writes is embedded as string constants in `kb_graph.py` itself.
No template files, no companion scripts.

### Pre-commit hook

```bash
#!/usr/bin/env bash
# Regenerate KB_INDEX.md before every commit
STAGED=$(git diff --cached --name-only --diff-filter=ACM)
HAS_TRACKED=$(echo "$STAGED" | grep -cE '\.(py|md|R|sh|yaml|yml|json|toml|nf)$' || true)
if [ "$HAS_TRACKED" -gt 0 ]; then
    echo "[pre-commit] Rebuilding KB_INDEX.md..."
    kb-graph rebuild .
    git add KB_INDEX.md
    echo "[pre-commit] KB_INDEX.md updated and staged."
fi
```

Installed to `scripts/hooks/pre-commit`. Sets `git config core.hooksPath scripts/hooks`.
If `scripts/hooks/` already has a pre-commit, append rather than overwrite.

### CLAUDE.md rules (appended)

```markdown
## Knowledge Graph Rules

1. **Read KB_INDEX.md first.** Before adding, modifying, or looking up content,
   read KB_INDEX.md to find the right files and understand their connections.
   KB_INDEX.md is auto-generated — never edit it by hand.

2. **Wiki-links in docs.** When editing any `.md` file, add `[[wiki-links]]` to
   cross-reference related docs and code. In Python files, use
   `# Design: [[doc-name#section]]` comments to link back to design docs.

3. **Query the graph before implementing.** Before starting a feature that
   touches multiple systems, run `kb-graph traverse <node> --depth 2` to
   discover all affected files. Read every file that surfaces before writing
   code. Or use `/check_graph <description>` for a full impact report.
```

### /check_graph skill

Written to `.claude/skills/check_graph/SKILL.md`. This is a **skill**, not a
command, so the agent can invoke it autonomously (e.g., before implementing a
multi-file change) — not just when the user types `/check_graph`. Spawns an
Explore agent that:
1. Runs `kb-graph rebuild .` to ensure the index is current
2. Reads KB_INDEX.md for project structure
3. Identifies entry-point files for the described change
4. Runs `kb-graph traverse <entry-point> --depth 2` for each
5. Reads every affected file
6. Returns a structured impact report (see `docs/phoam_paint/check_graph_reference.md`
   for the full report format)

## 7. Installation

### Quick install (one command)

```bash
curl -fsSL https://raw.githubusercontent.com/mcap91/bioinf-agent-toolkit/main/phoam_paint/kb_graph.py \
  -o ~/.local/bin/kb-graph && chmod +x ~/.local/bin/kb-graph
```

`~/.local/bin/` is on PATH. Now from any project:

```bash
cd ~/projects/my-project
kb-graph init .
```

### From the repo

```bash
git clone https://github.com/mcap91/bioinf-agent-toolkit.git
cd bioinf-agent-toolkit
./phoam_paint/install.sh
```

`install.sh` copies `kb_graph.py` to `~/.local/bin/kb-graph` and makes it
executable. Same pattern as `statusline/install.sh`.

### File layout in this repo

```
phoam_paint/
  kb_graph.py       # The tool — single file, stdlib only, has shebang
  install.sh        # Copies to ~/.local/bin/kb-graph
  uninstall.sh      # Removes ~/.local/bin/kb-graph (global removal)
  README.md         # Install instructions, usage, examples
```

### Two levels of removal

| Scope | Command | What it does |
|-------|---------|-------------|
| **Project** | `kb-graph uninit .` | Reverses `init` — removes KB_INDEX.md, graph.html, hook, check_graph skill, CLAUDE.md rules, .gitignore entry. The tool stays installed globally. |
| **Global** | `./phoam_paint/uninstall.sh` | Removes `~/.local/bin/kb-graph`. The tool is gone from the system. Does NOT touch any project — run `uninit` first on each project if you want a full clean removal. |

Both are safe: `uninit` confirms before acting and only removes what `init`
created. `uninstall.sh` only deletes the one binary.

## 8. Test Fixtures

A mock project at `tests/fixtures/sample_project/` with known, assertable
relationships:

```
tests/fixtures/sample_project/
  src/
    main.py              # imports api.routes, core.config
    core/
      __init__.py
      config.py          # no local imports (leaf node)
      database.py        # imports core.config
    api/
      __init__.py
      routes.py          # imports core.database, core.config, .auth
      auth.py            # imports core.database
  docs/
    README.md            # [[api-design]], [[config.py]]
    api-design.md        # [[routes.py]], [[auth.py]], [[database.py]]
    orphan-doc.md        # no links at all (orphan)
  config/
    settings.yaml        # references "src/core/config.py" in a value
  standalone.py          # no imports, not imported (orphan)
```

### Known graph properties (for assertions)

- **Node count**: 10 files (both __init__.py are empty and excluded)
- **Orphans**: `standalone.py`, `docs/orphan-doc.md`
- **Most connected**: `core/config.py` (imported by database.py, routes.py, main.py; wiki-linked from README.md)
- **Deepest path**: `docs/api-design.md` → `routes.py` → `core/database.py` → `core/config.py`
- **Cross-type edges**: `docs/README.md` → `core/config.py` (wiki-link from doc to code)
- **Config edge**: `settings.yaml` → `src/core/config.py`

## 9. Implementation Plan — Build Order

### Phase 1: Fixtures + Core Engine — DONE (2026-04-10)

**Goal**: `kb-graph rebuild` works against the fixture project and produces
correct KB_INDEX.md.

1. ~~Create `tests/fixtures/sample_project/` with all files listed above~~
2. ~~Build `kb_graph.py` scaffolding: CLI argument parsing (argparse), directory
   walker, file discovery, `.phoamignore` support~~
3. ~~Implement Python parser: `import` and `from...import` extraction, relative
   import resolution, `# Design: [[link]]` comment extraction~~
4. ~~Implement Markdown parser: `[[wiki-link]]` extraction with section support~~
5. ~~Implement Config parser: string value scanning for file path matches~~
6. ~~Build graph data structure: nodes dict + edges list, group assignment~~
7. ~~Implement `rebuild` command: scan → parse → build graph → write KB_INDEX.md~~
8. ~~**Test**: run against fixtures, verify KB_INDEX.md matches expected output~~

**Also completed (pulled forward from Phase 3):**
- graph.html generation with D3.js force-directed layout — produced on every
  `rebuild`, not as a separate command
- Click-to-highlight blast radius with depth-based visual distinction:
  depth 0 = white ring (clicked node), depth 1 = blue ring (direct),
  depth 2 = dimmed (transitive), outside = near-invisible
- Info panel showing imports, used-by, risk with direct/transitive counts

**Verified properties against fixtures (10 nodes, 13 edges, 2 orphans):**
- All 7 import edges resolve correctly (including relative `.auth`)
- All 5 wiki-link edges resolve correctly (basename matching)
- Config-ref edge: `settings.yaml` → `src/core/config.py`
- Orphans: `standalone.py`, `docs/orphan-doc.md`
- Most connected: `config.py` (5 edges: 3 imports + 1 wiki-link + 1 config-ref)
- Deepest chain: `api-design.md` → `routes.py` → `database.py` → `config.py`

**Implementation notes:**
- Node count is 10, not 11 as originally estimated — both `__init__.py` files
  are empty and correctly excluded. The original estimate was off by one.
- `KB_INDEX.md` is added to the built-in skip list (`IGNORE_FILES`) so the
  tool doesn't parse its own output and create spurious wiki-link edges.
- Risk in the fixture project is HIGH for all connected nodes (small graph,
  2 hops reaches 3+ groups). This is correct per the formula; real projects
  with more separation will show LOW/MEDIUM/HIGH spread.
- Phase 3 (visualization) was merged into Phase 1 since graph.html is a
  mandatory rebuild output, not a separate command.

### Phase 1.5: Mutation Tests — DONE (2026-04-13)

**Goal**: Verify that `rebuild` correctly detects graph changes when files
are modified. This validates the change-detection story that `/check_graph`
and the pre-commit hook depend on.

1. ~~Write `tests/test_graph_mutations.py`~~ — 20 tests across 8 test classes:
   a. ~~Baseline assertions: counts (10/13/2), orphan identity, all import edges,
      all wiki-link edges, config edge, most-connected node, KB_INDEX.md output,
      graph.html output~~
   b. ~~Add new `.py` file with imports → new node + 2 edges appear (11 nodes, 15 edges)~~
   c. ~~Remove import line → edge disappears (12 edges)~~
   d. ~~Add `[[wiki-link]]` to markdown → cross-type edge appears, orphan resolved~~
   e. ~~Add `[[wiki-link#section]]` → edge with section metadata~~
   f. ~~Create orphan files (`.py` and `.md`) → orphan count increases~~
   g. ~~`.phoamignore` by filename, by directory, and for connected files → nodes
      and edges removed~~
   h. ~~Delete connected file → node + all its edges removed~~
   i. ~~Output tests: KB_INDEX.md and graph.html reflect mutations~~
2. ~~All 20 tests pass (0.09s)~~

### Phase 2: Query Commands — DONE (2026-04-13)

**Goal**: all query commands work and produce correct output.

1. ~~Implement `neighbors` — direct connections (inbound + outbound)~~
2. ~~Implement `traverse` — BFS to depth N, with grep-for-references per file,
   output format matching Section 5 blast-radius spec~~
3. ~~Implement `path` — BFS shortest path between two nodes~~
4. ~~Implement `orphans` — nodes with degree 0~~
5. ~~Implement `analyze` — node/edge counts, top-N most-connected, group breakdown~~
6. ~~**Test**: run each command against fixtures, verify output~~

**Implementation notes:**
- Added `resolve_node()` helper for flexible node name input — accepts exact
  paths, basenames (`config.py`), partial paths (`core/config.py`), or stems
  (`config`). Resolves unambiguously or returns None.
- Blast radius (`traverse`) follows inbound edges only — traces dependents
  (files that depend on the changed file), not dependencies. This correctly
  answers "what breaks if I change this file?"
- For each file in the blast radius, greps for the target node's basename and
  shows matching lines (capped at 5 per file), per Section 5 spec.
- Risk level = distinct groups in the radius: 1 = LOW, 2 = MEDIUM, 3+ = HIGH.
- `path` uses bidirectional BFS (follows edges in both directions) to find
  the shortest connection between any two nodes.
- All commands build the graph from scratch (no cached state), per spec.
- Added `tests/test_generated_graph.py` — 28 tests against a programmatically
  generated 100-node project (40 workers, 40 guides, 15 orphans, 116 edges).
  Validates correctness of all query helpers at non-trivial scale.
- Total test suite: 48 tests (20 mutation + 28 generated), all passing (~0.3s).

### Phase 3: Init & Uninit Commands — DONE (2026-04-13)

(Was Phase 4 — renumbered since visualization was merged into Phase 1.)

**Goal**: `kb-graph init .` sets up a fresh project completely. `kb-graph uninit .`
reverses it cleanly.

1. ~~Embed pre-commit hook script as string constant (already done — `PRE_COMMIT_HOOK`)~~
2. ~~Embed CLAUDE.md rules as string constant (already done — `CLAUDE_MD_RULES`)~~
3. ~~Embed check_graph skill as string constant (`CHECK_GRAPH_SKILL`)~~
4. ~~Implement `init` command: run rebuild, write hook, set git config, write
   skill, append CLAUDE.md, update .gitignore~~
5. ~~Implement `uninit` command: remove KB_INDEX.md, graph.html, hook, skill,
   CLAUDE.md rules section, .gitignore entry, .phoamignore. Confirm before
   acting. Handle edge cases (hook file has other content, CLAUDE.md has
   content above/below the rules section)~~
6. ~~**Test**: run `init` against a fresh temp directory, verify all files created.
   Then run `uninit`, verify everything is removed and the directory is back
   to its original state~~

**Implementation notes:**
- All three string constants embedded in kb_graph.py: `PRE_COMMIT_HOOK`,
  `CLAUDE_MD_RULES`, `CHECK_GRAPH_SKILL`. No external template files.
- check_graph is a **skill** (`.claude/skills/check_graph/SKILL.md`), not a
  command. Skills have YAML frontmatter with a `description` field, which lets
  the agent discover and invoke the skill autonomously — e.g., before
  implementing a multi-file change. Commands are user-invoked only.
- `init` is idempotent: running twice does not duplicate hook blocks, CLAUDE.md
  rules, or .gitignore lines.
- `uninit` confirms before acting, prints a summary of what will be removed.
  Handles edge cases: hook file with other content (removes only the phoam_paint
  block), CLAUDE.md with other sections (removes only the rules section),
  .gitignore with other entries (removes only KB_INDEX.md and graph.html lines).
- When appending to an existing pre-commit hook, the shebang is stripped to avoid
  duplicates. When removing the hook block, a bare shebang is not considered
  "other content" — the file is deleted entirely.
- Clean round-trip verified: `init` then `uninit` restores the directory to its
  original state (no leftover files, no modified content, git config reverted).
- Existing 48 tests still pass (~0.3s).

### Phase 4: Install/Uninstall Scripts — DONE (2026-04-13)

**Goal**: installable and removable from GitHub.

1. ~~Create `phoam_paint/install.sh` (same pattern as `statusline/install.sh`)~~
2. ~~Create `phoam_paint/uninstall.sh` (same pattern as `statusline/uninstall.sh` —
   removes `~/.local/bin/kb-graph`)~~
3. ~~Create `phoam_paint/README.md`~~ (already exists — updated)
4. ~~Update `docs/roadmap.md` to mark phoam_paint components as completed~~
5. ~~Update `README.md` tools table~~

**Implementation notes:**
- `install.sh` copies `kb_graph.py` to `~/.local/bin/kb-graph`, makes it
  executable. Detects if already installed and up to date (idempotent).
  Warns if `~/.local/bin` is not on PATH.
- `uninstall.sh` removes `~/.local/bin/kb-graph`. Safe to run if already
  removed (warns, does not error). Reminds user to run `kb-graph uninit`
  on projects first.
- Top-level `./install.sh phoam_paint` and `./uninstall.sh phoam_paint`
  discover and run the scripts correctly.
- Existing 48 tests still pass (~0.3s).

### Phase 5: Agent A/B Experiment — IN PROGRESS (started 2026-04-13)

**Goal**: Prove that `/check_graph` helps a Claude agent catch distant-impact
changes that it would otherwise miss. This is the "does it actually work?"
validation — results go in the README as the primary evidence for users.
This is the most important test in the project.

#### Phase 5 v1: Rename task (2026-04-13) — ABANDONED

Tested a rename task (db_url → database_url). Both agents scored 40% perfect
because `grep -r db_url` is equally effective as the graph. The task tested
text search ability, not structural knowledge. The graph's unique value —
transitive dependency tracing — was never exercised.

| Metric | Agent A | Agent B |
|--------|---------|---------|
| Perfect runs | 2/5 (40%) | 2/5 (40%) |
| Avg missed refs | 2.2 | 1.4 |
| Avg time | 60.3s | 116.1s |

**Root cause**: The rename task is a text search problem. `grep -r db_url`
gives both agents the same answer. The graph adds no unique value.

#### Phase 5 v2: Blast radius marking (2026-04-14) — IN PROGRESS

**Redesigned experiment** to test structural knowledge instead of text search.

**Task**: Mark every file in the blast radius of `database.py` by adding
`# AFFECTED-BY: database.py` as the first line. This requires knowing
which files are directly or transitively dependent on database.py — a
graph traversal problem, not a text search problem.

**Why this works**: Files at depth 2 in the blast radius (e.g., `cli.py`
imports `routes.py` which imports `database.py`) never mention "database"
in their text. No amount of grepping will find them. Only graph traversal
(`kb-graph traverse database.py --depth 2`) surfaces the complete list.

**Fixture changes**: Added 2 new files to widen the depth-2 blast radius:
- `src/api/health.py` — imports from `api.routes`, never mentions "database"
- `scripts/monitor.py` — imports from `api.middleware`, never mentions "database"

**Expected blast radius of database.py (10 files)**:

| Depth | File | Connection | Mentions "database"? |
|-------|------|------------|---------------------|
| 1 | src/api/routes.py | imports database | YES |
| 1 | src/api/middleware.py | imports database | YES |
| 1 | src/api/auth.py | imports database | YES |
| 1 | scripts/seed.py | imports database | YES |
| 1 | docs/api-design.md | wiki-links [[database.py]] | YES |
| 2 | src/main.py | imports routes | **NO** |
| 2 | src/cli.py | imports routes | **NO** |
| 2 | src/api/health.py | imports routes | **NO** |
| 2 | scripts/monitor.py | imports middleware | **NO** |
| 2 | docs/README.md | wiki-links [[api-design]] | **NO** |

All 5 depth-2 files are invisible to `grep database`. Agent A must manually
trace import chains in a 46-file project to find them. Agent B gets the
exact list from `kb-graph traverse` via the check_graph skill.

**Measurement**: For each agent, scan all files for the marker comment.
Compute recall (expected files marked / total expected) and precision
(correct marks / all marks). A perfect run = 100% recall.

**Smoke test results (1 trial, Sonnet 4.6, CLI 2.1.108, 2026-04-14)**:

| Metric | Agent A | Agent B |
|--------|---------|---------|
| Recall | 80% (8/10) | 80% (8/10) |
| Precision | 100% | 100% |
| Time | 48.3s | 73.6s |
| Files missed | README.md, api-design.md | README.md, api-design.md |

**What happened**: Both agents found all 8 Python files (including all 4
depth-2 Python files) but missed both markdown files. Agent A traced
imports manually and found depth-2 Python files but didn't consider
wiki-link dependencies at all. Agent B ran check_graph and got the full
traverse output (which includes README.md and api-design.md), but:
1. Skipped `docs/README.md` entirely
2. Found `docs/api-design.md` but used `<!-- AFFECTED-BY: database.py -->`
   (HTML comment syntax for "valid Markdown") instead of the exact marker
   `# AFFECTED-BY: database.py`, so the scanner didn't detect it

**Problems to solve**:
1. **Prompt ambiguity**: Agents are "helpfully" using HTML comment syntax
   for markdown files instead of the exact marker text. Prompts need to
   be more explicit about using the exact string verbatim in all file types.
2. **Agent ignoring graph output**: Agent B's traverse output clearly
   listed README.md and api-design.md, but the agent either filtered them
   out or decided markdown files shouldn't be marked. Need to investigate
   whether the check_graph skill report clearly presents non-Python files
   or if the agent is making a judgment call to skip them.
3. **Surprising Agent A success**: Agent A found all depth-2 Python files
   without the graph by manually tracing imports. This is better than
   expected. The experiment may need harder conditions (more files, deeper
   chains, more noise) to differentiate the agents on Python-only deps.
4. **The real differentiator may be wiki-link deps**: The only files both
   agents missed are wiki-link connected (markdown), not import-connected
   (Python). The graph's unique advantage might be cross-type edges (doc →
   code wiki-links), not just transitive imports. This is worth exploring.

**Infrastructure notes**:
- Experiment runs in WSL (not Windows) — `kb_graph.py` has a shebang
  that requires LF line endings. Fixed via `.gitattributes` (`eol=lf`).
- `claude` CLI must be authenticated in WSL separately (`claude /login`).
- `node` must be installed in WSL for the `claude` CLI to work.
- Dry-run validates fixture + ground truth without needing `claude`:
  `python3 tests/test_agent_experiment.py --dry-run`

**Status**: Pausing to plan further improvements. A fresh agent session
will pick up from here to iterate on prompt design, check_graph skill
behavior, and fixture difficulty before running the full experiment.

**To resume**: Superseded by Phase 5 v3 below. v2 transcripts are in
`tests/experiment_transcripts/` (will be overwritten by v3 runs).

#### Phase 5 v3: Bioinformatics fixture redesign (2026-04-14) — READY

**Problem**: v2 produced identical 80% recall for both agents. The 46-file
web-app fixture was too small with shallow (depth 2) import chains. Agent A
manually traced all Python imports successfully — the graph provided no
measurable advantage.

**Solution**: Replaced with a 97-file bioinformatics fixture modeled on
spatial-omics analysis packages (mirrors real repos like SpatialCore-Dev):

- **Target**: `src/core/metadata.py` — central utility with high fan-out
- **Blast radius**: 19 files across depths 1-4
- **Import chains**: through `__init__.py` re-exports (not direct imports)
- **Red herrings**: 5 files mention "metadata" in comments/strings but
  are NOT dependents (designed to waste Agent A's grep time)
- **Only 4 of 19** blast radius files are greppable (depth 1)

**Corrected depth grouping** (spec table had clustering.py at depth 3,
but it imports ontology.py directly → depth 2):

| Depth | Count | Files |
|-------|-------|-------|
| 1 | 4 | core/\_\_init\_\_.py, ontology.py, confidence.py, test_metadata.py |
| 2 | 5 | annotation/\_\_init\_\_.py, markers.py, cell_types.py, base.py, clustering.py |
| 3 | 5 | preprocessing/\_\_init\_\_.py, normalization.py, qc.py, spatial.py, spatial_plot.py |
| 4 | 5 | ingestion.py, batch.py, run_qc.py, run_analysis.py, heatmap.py |

**Critical parser constraint**: `preprocessing/base.py` uses
`from core import MetadataManager` (not `from core import metadata`) so
the parser resolves to `core/__init__.py` (depth 2 via \_\_init\_\_) rather
than directly to `core/metadata.py` (which would be depth 1).

**Changes to `tests/test_agent_experiment.py`**:
- Replaced all fixture data with `V3_FILES` dict (97 bioinformatics files)
- Added `OLD_FILES_TO_REMOVE` to clean original web-app fixture files
- Updated `EXPECTED_BLAST_RADIUS` with 4 depth groups (19 files)
- Updated `PROMPT_A`, `PROMPT_B`, `MARKER` for metadata.py target
- Agent B prompt: `kb-graph traverse metadata.py --depth 4`
- Added `--depth` CLI arg (default 4)
- Increased default timeout 180s → 300s
- Extended `print_summary()` with depth 1/2/3/4 miss breakdown
- Rewrote `--dry-run` to validate traverse output against ground truth
  and confirm red herring files are absent

**Dry-run result** (2026-04-14):
```
  v3 bioinformatics fixture: 97 files total
  Expected blast radius: 19/19 [OK]
  Red herring files: 5/5 [OK], all ABSENT from traverse
  Ground truth: 19/19 expected files found in traverse output
  PASS — ground truth matches traverse output perfectly
```

**Expected experiment outcomes**:
- **Agent A**: 20-30% recall (finds 4 depth-1 files via grep, misses 15)
- **Agent B**: 100% recall (graph gives the exact answer)

**Status**: Ready for experiment runs. Run:
```bash
python3 tests/test_agent_experiment.py --trials 5 --save-transcripts
```

### Phase 6: Additional Parsers (stretch)

**Goal**: support beyond Python/Markdown.

1. R parser: `source()`, local `library()`
2. Shell parser: `source`, `. path`
3. Nextflow parser: `include` statements
4. **Test**: add fixture files for each language, verify edges

---

## 10. Open Questions (Resolved)

| Question | Resolution |
|----------|-----------|
| Multi-file package? | No. Single file. |
| Per-project config? | No config file. Auto-detect + optional `.phoamignore`. |
| Hardcoded install paths? | No. `init` writes to the repo it's pointed at. |
| graph.html optional? | No. Mandatory output, generated on every rebuild. |
| Foam as dependency? | No. Headless-first. Foam is design inspiration only. |
| Where does it live in this repo? | `phoam_paint/` directory (same level as `statusline/`). |
| How does it install? | `curl` one file to `~/.local/bin/kb-graph`, or `install.sh`. |
| `/check_graph` bundled or separate? | Bundled. `init` writes the skill into the target project's `.claude/skills/`. It is a skill (not a command) so the agent can invoke it autonomously. |

## 11. Constraints

- Python 3.10+ stdlib only — no external dependencies
- Single file (`kb_graph.py`) — everything embedded
- Project-agnostic — works on any repo, not just bioinformatics
- Headless-first — no GUI, no VS Code extensions, no browser required to use
  (graph.html is a generated artifact the user can open anywhere)
- Must work on Linux, macOS. Windows is not a target.
