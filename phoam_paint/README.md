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
# Set up a project (hook, CLAUDE.md rules, check_graph skill, first rebuild)
kb-graph init .

# Rebuild the graph manually
kb-graph rebuild .

# Query commands
kb-graph neighbors <node>             # direct connections (inbound + outbound)
kb-graph traverse <node> --depth 2    # blast radius (who breaks if this changes?)
kb-graph path <from> <to>             # shortest path between two nodes
kb-graph orphans                      # files with no connections
kb-graph analyze                      # stats: node/edge counts, most-connected, groups

# Remove all kb-graph artifacts from a project
kb-graph uninit .
```

### What `init` does

1. Scans the repo and builds the dependency graph
2. Generates `KB_INDEX.md` and `graph.html` at the repo root
3. Installs a `/check_graph` skill that the agent can also invoke autonomously
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

### Phase 2: Query Commands (2026-04-13)

Manual and automated verification of all five query commands against the fixture project.

**neighbors** — `kb-graph neighbors config.py --path tests/fixtures/sample_project/`

| Property | Expected | Result |
|----------|----------|--------|
| Resolves basename to full path | `config.py` → `src/core/config.py` | Correct |
| Outbound edges | 0 (config.py imports nothing locally) | 0 |
| Inbound edges | 5 (3 imports + 1 wiki-link + 1 config-ref) | 5 |
| Orphan node (standalone.py) | 0 connections | 0 |
| Unknown node error | Exit code 1, error message | Correct |

**traverse** — `kb-graph traverse database.py --path tests/fixtures/sample_project/`

| Property | Expected | Result |
|----------|----------|--------|
| Depth 1 (direct dependents) | api-design.md, auth.py, routes.py | Correct (3 nodes) |
| Depth 2 (transitive) | README.md, main.py | Correct (2 nodes) |
| Excludes dependencies | config.py NOT in blast radius | Correct |
| Grep references | Matching lines shown, capped at 5 | Correct |
| Risk level | HIGH (4 groups) | HIGH (4 groups) |
| `--depth 1` flag | Only direct dependents | Correct (3 nodes) |

**traverse** — `kb-graph traverse config.py --path tests/fixtures/sample_project/`

| Property | Expected | Result |
|----------|----------|--------|
| Depth 1 count | 5 (most-connected node) | 5 |
| Depth 2 count | 2 (api-design.md, auth.py) | 2 |
| Risk level | HIGH (5 groups) | HIGH (5 groups) |

**path** — `kb-graph path api-design.md config.py --path tests/fixtures/sample_project/`

| Property | Expected | Result |
|----------|----------|--------|
| Shortest path exists | Yes (2 hops via README.md) | Correct |
| Path display | api-design.md → README.md → config.py | Correct |
| Edge types shown | wiki-link → wiki-link | Correct |
| No path (orphan to connected) | "No path" message | Correct |
| Same-node path | 0 hops | Correct |

**orphans** — `kb-graph orphans --path tests/fixtures/sample_project/`

| Property | Expected | Result |
|----------|----------|--------|
| Orphan count | 2 | 2 |
| Orphan identity | standalone.py, orphan-doc.md | Correct |
| Descriptions shown | Yes | Yes |
| Groups shown | root, docs | Correct |

**analyze** — `kb-graph analyze --path tests/fixtures/sample_project/`

| Property | Expected | Result |
|----------|----------|--------|
| Node count | 10 | 10 |
| Edge count | 13 | 13 |
| Orphan count | 2 | 2 |
| Edge type breakdown | import: 7, wiki-link: 5, config-ref: 1 | Correct |
| File type breakdown | code: 6, doc: 3, config: 1 | Correct |
| Most connected | routes.py (5), config.py (5) | Correct |
| Group count | 6 | 6 |

### Phase 3: Init & Uninit Commands (2026-04-13)

Verified via round-trip testing against temporary git repositories. `init` creates
all artifacts, `uninit` confirms and removes them cleanly.

**Fresh project round-trip** (no pre-existing files):

| Property | Expected | Result |
|----------|----------|--------|
| `init` creates KB_INDEX.md | Yes | Yes |
| `init` creates graph.html | Yes | Yes |
| `init` creates scripts/hooks/pre-commit | Yes, executable | Yes, 0755 |
| `init` sets git config core.hooksPath | scripts/hooks | Correct |
| `init` creates .claude/skills/check_graph/SKILL.md | Yes, with YAML frontmatter | Yes |
| `init` creates CLAUDE.md | With Knowledge Graph Rules | Correct |
| `init` creates .gitignore | With KB_INDEX.md + graph.html | Correct |
| `uninit` confirms before acting | Prints summary, requires y/N | Correct |
| `uninit` removes all created files | Yes | Yes |
| `uninit` reverts git config | core.hooksPath unset | Correct |
| Round-trip clean | Post-uninit == original state | True |

**Edge cases** (pre-existing hook, CLAUDE.md, .gitignore):

| Property | Expected | Result |
|----------|----------|--------|
| `init` appends to existing hook | phoam_paint block added, original preserved | Correct |
| `init` appends to existing CLAUDE.md | Rules section added, original preserved | Correct |
| `init` appends to existing .gitignore | Lines added, original preserved | Correct |
| `uninit` edits hook (other content) | Removes only phoam_paint block | Correct |
| `uninit` edits CLAUDE.md (other content) | Removes only rules section | Correct |
| `uninit` edits .gitignore (other content) | Removes only our lines | Correct |
| All three files restored exactly | Post-uninit == pre-init content | True |

**Idempotency** (running `init` twice):

| Property | Expected | Result |
|----------|----------|--------|
| Hook blocks | 1 (not duplicated) | 1 |
| CLAUDE.md rules sections | 1 (not duplicated) | 1 |
| .gitignore KB_INDEX.md lines | 1 (not duplicated) | 1 |

**Uninit on non-initialized project**: prints "Nothing to remove" and exits cleanly.

**Existing tests**: all 48 tests still pass (~0.3s).

### Phase 4: Install/Uninstall Scripts (2026-04-13)

| Property | Expected | Result |
|----------|----------|--------|
| `install.sh` copies to `~/.local/bin/kb-graph` | Yes, executable | Yes, 0755 |
| Idempotent install (run twice) | "already installed and up to date" | Correct |
| `uninstall.sh` removes binary | Yes | Yes |
| Idempotent uninstall (run twice) | Warns "already removed?" | Correct |
| Top-level `./install.sh --list` | phoam_paint listed | Correct |
| Top-level `./install.sh phoam_paint` | Delegates to component script | Correct |
| Top-level `./uninstall.sh phoam_paint` | Delegates to component script | Correct |
| PATH warning | Shown when `~/.local/bin` not on PATH | Correct |
| Existing tests | 48 tests pass (~0.3s) | All pass |

### Phase 5 (in progress): Agent A/B Experiment

An empirical test of whether `/check_graph` helps a Claude agent catch
distant-impact changes. Two Claude Code agents get the same rename task — one
with graph tooling (KB_INDEX.md, check_graph skill, CLAUDE.md rules), one
without. This is the primary evidence for the tool's value.

**Scenario**: Rename `db_url` to `database_url` in `config.py`. The enhanced
fixture has 44 files total: 12 files with 23 `db_url` references across 7
directories (depths 0-3, including dict unpacking, f-strings, shell scripts,
YAML config, markdown code fences), plus 24 noise files. Agent A has to
search; Agent B gets a map from the graph.

| | Agent A (no graph) | Agent B (with `/check_graph`) |
|-|-------------------|-------------------------------|
| **Setup** | Bare enhanced fixture (44 files) | `kb-graph init` (39 nodes, 20 edges, KB_INDEX.md, check_graph skill, CLAUDE.md rules) |
| **Metric** | Remaining `db_url` references after agent finishes | Same |
| **Prompt** | "Rename db_url to database_url in config.py. Update all code that references db_url throughout this project." | "First read CLAUDE.md, then run the check_graph skill to analyze the impact... make the rename" |

#### Results (5 trials, Sonnet 4.6, Claude CLI 2.1.105)

| Trial | A missed | B missed | A files missed | B files missed | A time | B time |
|-------|----------|----------|----------------|----------------|--------|--------|
| 1 | 5 | 0 | settings.yaml, deployment.md, health_check.sh | none | 53.6s | 115.4s |
| 2 | 0 | 5 | none | deployment.md, health_check.sh, seed.py | 73.9s | 105.7s |
| 3 | 5 | 1 | settings.yaml, deployment.md, health_check.sh | seed.py (comment only) | 46.7s | 113.4s |
| 4 | 1 | 0 | seed.py (comment only) | none | 60.4s | 124.8s |
| 5 | 0 | 1 | none | seed.py (comment only) | 66.9s | 121.0s |

| Metric | Agent A | Agent B |
|--------|---------|---------|
| Perfect runs | 2/5 (40%) | 2/5 (40%) |
| Avg missed refs | 2.2 | 1.4 |
| Avg time | 60.3s | 116.1s |

#### Gap Analysis

**Agent B is NOT reliably outperforming Agent A.** Both agents achieve 40%
perfect runs. Agent B misses fewer references on average (1.4 vs 2.2), but
this is not a convincing gap — and Agent B takes 2x as long.

**Root cause: the graph has blind spots.** The enhanced fixture has 39 nodes
but 26 orphans (67%). Two files with `db_url` references are **invisible to
the graph** because they have no parseable edges:

| File | Why it's an orphan | Agent B behavior |
|------|-------------------|------------------|
| `docs/deployment.md` | No wiki-links to/from it — just prose with code fences | Missed in trial 2 (5 refs). Graph can't surface it. |
| `scripts/health_check.sh` | Shell parser only finds `source` commands; this file uses `curl`/`python3` | Missed in trial 2. Not connected to anything in the graph. |

When Agent B relies on the graph's blast radius to find affected files, it
misses these orphans. Agent A, by contrast, just greps the whole project and
sometimes finds them.

**The `seed.py` comment problem**: In trials 3 and 5, Agent B found and
renamed all code references in `scripts/seed.py` but left the comment
`# Dict unpacking — db_url is a key in the config dict` unchanged. This is
a real but minor miss — the graph DID surface this file (it has import edges
to config.py and database.py), the agent just didn't update the comment text.

#### Identified Gaps — What Needs to Improve

1. **Graph coverage gap**: `docs/deployment.md` and `scripts/health_check.sh`
   are orphans because the graph has no edge type that connects them. The
   shell parser doesn't understand `curl` or inline `python3 -c` calls.
   Markdown files without wiki-links are invisible.
   - **Possible fix**: Add a "string-match" edge type that connects any file
     containing a tracked identifier (like `db_url`) back to where it's
     defined. This is what makes the graph valuable — surfacing connections
     that grep alone can't prioritize.
   - **Possible fix**: The `/check_graph` skill should do a project-wide grep
     for the target identifier AFTER traversing the graph, to catch orphan
     files the graph missed. The graph narrows the search; grep catches
     stragglers.

2. **Agent B over-trusts the graph**: When check_graph returns a blast radius,
   Agent B treats it as exhaustive and doesn't verify with grep. The skill
   should explicitly tell the agent: "These are the graph-connected files.
   Also grep for `<identifier>` project-wide to catch files the graph may
   not know about."

3. **Comment handling is non-deterministic**: Both agents sometimes update
   comments mentioning `db_url` and sometimes don't. This is agent behavior,
   not a graph problem.

4. **Agent B is 2x slower**: The overhead of reading CLAUDE.md, running
   check_graph (which spawns an Explore agent, rebuilds the graph, runs
   traverse), then making changes — this doubles the wall time. For the
   graph to be worth it, it needs to be MORE reliable, not just different.

**Status**: Experiment infrastructure works. Results show the graph helps
with connected files but has dangerous blind spots for orphans. The system
needs improvement before the graph provides reliable value over grep.
See `docs/phoam_paint/plan.md` Phase 5 for the improvement plan.

**Reproducing**: `python3 tests/test_agent_experiment.py --trials N --model sonnet --save-transcripts --clean`
