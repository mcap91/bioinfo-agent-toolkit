# phoam_paint (kb-graph)

Auto-generated knowledge graph for any repo. Point it at a directory, get a living map of how every file connects to every other file.

- **`KB_INDEX.md`** — structured index for coding agents to read before making changes
- **`graph.html`** — interactive D3.js force-directed visualization for humans

Single file, stdlib only, Python 3.10+. No dependencies.

## Install

### Quick install (from this repo)

```bash
git clone https://github.com/mcap91/bioinf-agent-toolkit.git
cd bioinf-agent-toolkit
./phoam_paint/install.sh
```

### Quick install (standalone)

```bash
curl -fsSL https://raw.githubusercontent.com/mcap91/bioinf-agent-toolkit/main/phoam_paint/kb_graph.py \
  -o ~/.local/bin/kb-graph && chmod +x ~/.local/bin/kb-graph
```

`~/.local/bin/` must be on your PATH.

## Usage

```bash
# Set up a project (hook, CLAUDE.md rules, slash command, first rebuild)
kb-graph init .

# Rebuild the graph manually
kb-graph rebuild .

# Query commands (Phase 2 — not yet implemented)
kb-graph neighbors <node>
kb-graph traverse <node> --depth 2
kb-graph path <from> <to>
kb-graph orphans
kb-graph analyze

# Remove all kb-graph artifacts from a project
kb-graph uninit .
```

### What `init` does

1. Scans the repo and builds the dependency graph
2. Generates `KB_INDEX.md` and `graph.html` at the repo root
3. Creates a `/check_graph` slash command for Claude Code
4. Installs a pre-commit hook that rebuilds on every commit
5. Appends knowledge-graph rules to `CLAUDE.md`
6. Adds `graph.html` to `.gitignore`

### What it detects

| File type | What it parses |
|-----------|---------------|
| `.py` | `import x`, `from x import y`, relative imports, `# Design: [[link]]` |
| `.md` | `[[wiki-links]]`, `[[file#section]]` |
| `.yaml`/`.yml`/`.json`/`.toml` | String values matching tracked file paths |
| `.R` | `source()`, `library()` (Phase 6) |
| `.sh`/`.bash` | `source`, `. path` (Phase 6) |
| `.nf` | `include { } from './path'` (Phase 6) |

## Uninstall

**Remove from a project** (keeps the tool installed globally):
```bash
kb-graph uninit .
```

**Remove the tool entirely**:
```bash
./phoam_paint/uninstall.sh
```

---

## Validation

Test results from the fixture project at `tests/fixtures/sample_project/` — a
minimal Python project with known graph properties (10 nodes, 13 edges,
2 orphans across Python, Markdown, and YAML files).

### Phase 1: Core Engine (2026-04-10)

Manual verification of `kb-graph rebuild` against the fixture project.

| Property | Expected | Result |
|----------|----------|--------|
| Node count | 10 | 10 |
| Edge count | 13 | 13 |
| Orphan count | 2 | 2 |
| Import edges (Python) | 7 | 7 (including relative `.auth`) |
| Wiki-link edges (Markdown) | 5 | 5 (basename resolution) |
| Config-ref edges (YAML) | 1 (`settings.yaml` -> `config.py`) | 1 |
| Orphan identity | `standalone.py`, `orphan-doc.md` | Correct |
| Most connected node | `config.py` (5 edges) | Correct |
| Deepest chain | `api-design.md` -> `routes.py` -> `database.py` -> `config.py` | Correct |
| Empty `__init__.py` excluded | Yes | Yes (both 0-byte files skipped) |
| `KB_INDEX.md` not self-referencing | Yes | Yes (in `IGNORE_FILES`) |
| `graph.html` generated | D3.js force-directed, dark theme | Correct |

### Phase 1.5: Mutation Tests (2026-04-13)

Automated test suite: `tests/test_graph_mutations.py` — 20 tests, all passing.

Each test copies the fixture project to a temp directory, mutates it, rebuilds
the graph, and asserts the delta. This validates that `rebuild` correctly
tracks changes — the foundation for the pre-commit hook and `/check_graph`.

```
$ python3 -m unittest tests.test_graph_mutations -v

TestBaseline (9 tests)
  baseline_counts ..................... 10 nodes, 13 edges, 2 orphans
  baseline_orphans ................... standalone.py, orphan-doc.md
  baseline_import_edges .............. all 7 import edges present
  baseline_wikilink_edges ............ all 5 wiki-link edges present
  baseline_config_edge ............... settings.yaml -> config.py
  baseline_most_connected ............ config.py has 5 edges
  kb_index_generated ................. stats header correct
  graph_html_generated ............... D3 + dark theme present

TestAddFile (1 test)
  add_python_file_with_imports ....... 11 nodes, 15 edges, 2 orphans

TestRemoveImport (1 test)
  remove_import_drops_edge ........... 10 nodes, 12 edges

TestAddWikiLink (2 tests)
  add_wikilink_creates_edge .......... orphan-doc -> routes.py, orphans drop to 1
  add_wikilink_with_section .......... section metadata = "endpoints"

TestAddOrphan (2 tests)
  new_orphan_python .................. 11 nodes, 3 orphans
  new_orphan_markdown ................ 11 nodes, 3 orphans

TestPhoamignore (3 tests)
  ignore_file_by_name ................ standalone.py excluded, 9 nodes
  ignore_directory ................... docs/ excluded, 7 nodes, no doc edges
  ignore_connected_file .............. auth.py + its edges removed

TestDeleteFile (1 test)
  delete_connected_file .............. auth.py gone, dangling import = no edge

TestOutputReflectsMutations (2 tests)
  kb_index_reflects_added_file ....... middleware.py in output, "Nodes: 11"
  graph_html_reflects_added_file ..... middleware.py in visualization

----------------------------------------------------------------------
Ran 20 tests in 0.09s — OK
```

### Phase 5 (planned): Agent A/B Experiment

An empirical test that proves `/check_graph` helps a Claude agent catch
distant-impact changes. Two Claude Code agents get the same task — one with
the graph tooling, one without. Results will be recorded here.

**Scenario**: Rename the `db_url` parameter to `database_url` in `config.py`.
This is a 1-line change in `config.py`, but it silently breaks `database.py`
(depth 1), and transitively affects `routes.py` and `auth.py` (depth 2).
A thorough fix requires updating every file that passes `db_url=`.

| | Agent A (no graph) | Agent B (with `/check_graph`) |
|-|-------------------|-------------------------------|
| **Setup** | Bare fixture project | `kb-graph init` (KB_INDEX.md, hook, slash command) |
| **Prompt** | "Rename db_url to database_url in config.py. Update all code." | "Run /check_graph to understand impact, then rename db_url to database_url." |
| **Metric** | Remaining references to old `db_url` name after agent finishes | Same |
| **Expected** | May miss distant callers | Blast-radius traversal surfaces all affected files |

**What we're measuring**:
- **Completeness**: did the agent update every `db_url` reference?
- **Depth**: did it look beyond the file it was told to change?
- **Confidence**: did it verify its own work?

Results will be non-deterministic (LLM behavior varies). We'll run multiple
trials and report the pattern. Full agent transcripts will be saved for
reproducibility.

*Status: not yet run. Requires Phase 2 (query commands) and Phase 3 (init).*
