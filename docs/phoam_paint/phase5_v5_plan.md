# Phase 5 v5 Implementation Plan

**Goal:** Build a single experiment script (`tests/test_experiment_v5.py`)
with three scenarios testing whether realistic, vague prompts differentiate
Agent A (no graph) from Agent B (with kb-graph + CLAUDE.md rules).

**Spec:** `docs/phoam_paint/phase5_v5_design.md`

**Architecture:** One self-contained Python script. Fixture data is
embedded as dict constants (copied from existing `test_experiment_a.py`
and `test_experiment_b.py`). No shared modules — the script must run
independently. Scenarios share infrastructure (agent runner, CLI, logging,
strategy detection) but have independent setup, prompts, and scoring.

**Tech Stack:** Python 3.10+ stdlib only. `claude` CLI for agent
invocation. `kb-graph` CLI for graph operations.

**Platform:** Designed for headless Linux. On Windows dev machines, run
via WSL: `wsl bash -c "cd /mnt/c/... && python3 tests/test_experiment_v5.py ..."`

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `tests/test_experiment_v5.py` | Create | All three scenarios: fixture data, setup, prompts, scoring, agent runner, CLI, reporting |
| `docs/phoam_paint/phase5_v5_design.md` | Exists | Spec (already written) |
| `docs/phoam_paint/phase5_v5_plan.md` | Exists | This plan |
| `docs/phoam_paint/plan.md` | Modify | Update Phase 5 v5 status after experiments run |

---

## Task 1: Script skeleton and shared infrastructure

**Files:** Create `tests/test_experiment_v5.py`

Write the shared infrastructure that all three scenarios use. This
includes everything except the per-scenario fixture data, prompts,
and scoring functions.

- [ ] **Step 1: Write the script header and imports**

```python
#!/usr/bin/env python3
"""Phase 5 v5 — Realistic Prompt Experiment.

Three scenarios testing whether vague, realistic prompts differentiate
Agent A (no graph) from Agent B (with kb-graph + CLAUDE.md rules).

Usage:
    python tests/test_experiment_v5.py --scenario A --dry-run
    python tests/test_experiment_v5.py --scenario all --save-transcripts
    python tests/test_experiment_v5.py --scenario B --trials 3
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
```

- [ ] **Step 2: Write helper functions**

Port these from `test_experiment_b.py` (lines 40-68), adapting as needed:

- `_kb_graph_cmd()` — returns the command list for invoking kb-graph
  (handles Windows vs Linux). Copy from `test_experiment_b.py:40-58`.
- `log(msg)` — print + append to log file. Adapt from
  `test_experiment_b.py:61-65`. The log file path should be
  `tests/experiment_v5.log` (combined log for all scenarios).
- `get_claude_version()` — get CLI version string. Copy from
  `test_experiment_b.py:68-77`.
- `check_prerequisites()` — verify `claude` and `kb-graph` are in PATH.
  Copy from `test_experiment_b.py:922-932`.

- [ ] **Step 3: Write `create_fixture(dest, files_dict)`**

Generic fixture creator — takes a destination dir and a dict of
`{relative_path: content}`, writes all files. Adapted from
`test_experiment_b.py:935-939` but parameterized on the files dict.

```python
def create_fixture(dest, files_dict):
    for rel_path, content in files_dict.items():
        filepath = Path(dest) / rel_path
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding="utf-8")
```

- [ ] **Step 4: Write `init_graph(project_dir)`**

Initializes a git repo and runs `kb-graph init`. Copy from
`test_experiment_b.py:942-961`. No changes needed.

- [ ] **Step 5: Write `run_agent(project_dir, prompt, ...)`**

Agent invocation via `claude -p`. Copy from
`test_experiment_b.py:964-983`. No changes needed.

- [ ] **Step 6: Write `detect_strategy(transcript)`**

New function. Analyzes transcript text for signals of graph usage vs
grep-based search:

```python
def detect_strategy(transcript):
    text = transcript.lower()
    return {
        "used_graph": any(k in text for k in [
            "kb_index", "kb-graph", "traverse", "blast radius",
            "knowledge graph",
        ]),
        "used_grep": any(k in text for k in [
            "grep", "rg ", "ripgrep", "search for",
            "searching for",
        ]),
        "read_claude_md": "claude.md" in text,
        "checked_imports": any(k in text for k in [
            "who imports", "which files import", "files that import",
            "importing transform",
        ]),
    }
```

- [ ] **Step 7: Write CLI argument parser**

```python
parser = argparse.ArgumentParser(
    description="Phase 5 v5 — Realistic Prompt Experiment"
)
parser.add_argument(
    "--scenario", type=str, required=True,
    choices=["A", "B", "C", "all"],
    help="Which scenario to run",
)
parser.add_argument("--trials", type=int, default=1)
parser.add_argument("--model", type=str, default=None)
parser.add_argument("--save-transcripts", action="store_true")
parser.add_argument("--timeout", type=int, default=300)
parser.add_argument("--dry-run", action="store_true")
parser.add_argument("--clean", action="store_true")
```

- [ ] **Step 8: Write `main()` dispatch logic**

The main function parses args, resolves which scenarios to run
(`--scenario all` expands to `["A", "B", "C"]`), and for each
scenario calls `run_scenario(scenario, args)`. Each scenario
produces independent results JSON and transcript files.

```python
def main():
    args = parser.parse_args()
    check_prerequisites()
    scenarios = ["A", "B", "C"] if args.scenario == "all" else [args.scenario]
    for scenario in scenarios:
        run_scenario(scenario, args)
```

- [ ] **Step 9: Write `run_scenario(scenario, args)`**

Dispatches to the right setup/prompt/scoring functions based on
scenario letter. Structure:

```python
SCENARIOS = {
    "A": {
        "name": "Fix this thing",
        "setup": setup_scenario_a,
        "prompt_a": PROMPT_A_SCENARIO_A,
        "prompt_b": PROMPT_B_SCENARIO_A,
        "score": score_scenario_a,
        "expected_count": 6,
    },
    # ... B, C
}

def run_scenario(scenario, args):
    cfg = SCENARIOS[scenario]
    log(f"Scenario {scenario}: {cfg['name']}")
    if args.dry_run:
        dry_run_scenario(scenario, cfg, args)
        return
    results = []
    for trial_num in range(1, args.trials + 1):
        result = run_trial(scenario, cfg, trial_num, args)
        results.append(result)
    summary = print_summary(scenario, cfg, results)
    # Write results JSON
    results_path = f"tests/experiment_v5_{scenario.lower()}_results.json"
    ...
```

- [ ] **Step 10: Write `run_trial(scenario, cfg, trial_num, args)`**

For one trial:
1. Create tmpdir with two fixture copies (dir_a, dir_b)
2. Call `cfg["setup"](dir_a, dir_b)` to apply scenario-specific modifications
3. Run `init_graph(dir_b)` for Agent B's project
4. Run Agent A with `cfg["prompt_a"]`, capture stdout/stderr/time
5. Run Agent B with `cfg["prompt_b"]`, capture stdout/stderr/time
6. Score both: `cfg["score"](dir_a)` and `cfg["score"](dir_b)`
7. Detect strategy from transcripts
8. Save transcripts if `--save-transcripts`
9. Return results dict

- [ ] **Step 11: Write `print_summary(scenario, cfg, results)`**

Print a formatted summary table (recall, precision, time, strategy
for each agent across trials). Follow the format from
`test_experiment_b.py:1191-1234` but adapted for the v5 results
structure. Include strategy detection results.

- [ ] **Step 12: Write `dry_run_scenario(scenario, cfg, args)`**

Build the fixture, apply scenario setup, run kb-graph init on
project B, and validate that the fixture is in the expected state.
No agents are invoked. Print validation results.

**Validation per scenario:**
- Scenario A: verify transform.py has `mode` param, verify 6 call
  sites have `strict=`, verify KB_INDEX.md lists transform.py importers
- Scenario B: same as A + verify `test_output.txt` exists
- Scenario C: verify target file exists, verify 6 wiki-link refs exist,
  verify traverse output matches expected refs

---

## Task 2: Scenario A — "Fix this thing"

**Files:** Continue editing `tests/test_experiment_v5.py`

- [ ] **Step 1: Copy fixture data from `test_experiment_b.py`**

Copy `FIXTURE_FILES` dict (lines 80-825) into the v5 script as
`FIXTURE_FILES_CODE`. This is the 80-file Python data pipeline
fixture. Copy it verbatim — do not modify file contents.

**Important**: When copying, the `src/core/transform.py` entry should
keep the ORIGINAL signature (`strict: bool = True`). The setup
function will modify it.

- [ ] **Step 2: Write scenario A constants**

```python
PROMPT_A_SCENARIO_A = (
    "I updated apply_transform() in src/core/transform.py — the "
    "strict parameter is now called mode (takes \"strict\" or "
    "\"lenient\" instead of True/False). Can you make sure I didn't "
    "break anything?"
)

PROMPT_B_SCENARIO_A = (
    "Read CLAUDE.md first. I updated apply_transform() in "
    "src/core/transform.py — the strict parameter is now called mode "
    "(takes \"strict\" or \"lenient\" instead of True/False). Can you "
    "make sure I didn't break anything?"
)
```

Copy `EXPECTED_FIXES` list from `test_experiment_b.py:835-875`.
Copy `SHOULD_NOT_MODIFY` list from `test_experiment_b.py:876-885`.

- [ ] **Step 3: Write `setup_scenario_a(dir_a, dir_b)`**

1. Call `create_fixture(dir_a, FIXTURE_FILES_CODE)` and
   `create_fixture(dir_b, FIXTURE_FILES_CODE)`
2. In BOTH directories, modify `src/core/transform.py`:
   replace `strict: bool = True` with `mode: str = "strict"`
   and replace `if strict:` with `if mode == "strict":` in the
   function body. Use string `.replace()` on the file content.

Check `test_experiment_b.py:82-133` for the exact transform.py
content to understand what needs replacing.

- [ ] **Step 4: Write `score_scenario_a(project_dir)`**

Copy `score_fixes()` from `test_experiment_b.py:986-1050`. It uses
regex to check each of the 6 expected fixes. No changes needed —
it works against the same fixture and same expected fixes.

---

## Task 3: Scenario B — "Something is broken"

**Files:** Continue editing `tests/test_experiment_v5.py`

- [ ] **Step 1: Write scenario B constants**

```python
TEST_OUTPUT_TXT = """\
$ python -m pytest tests/ -x
============================================ FAILURES =============================================
_________________________________ test_strict_mode _________________________________

    def test_strict_mode():
        config = TransformConfig(normalize=True)
>       result = apply_transform([], config, strict=True)
E       TypeError: apply_transform() got an unexpected keyword argument 'strict'

tests/test_transform.py:9: TypeError
======================================= short test summary =======================================
FAILED tests/test_transform.py::test_strict_mode - TypeError: apply_transform() got an unexpected keyword argument 'strict'
======================================= 1 failed in 0.42s ========================================
"""

PROMPT_A_SCENARIO_B = (
    "The tests are failing — see test_output.txt for the traceback. "
    "Can you fix whatever is broken?"
)

PROMPT_B_SCENARIO_B = (
    "Read CLAUDE.md first. The tests are failing — see "
    "test_output.txt for the traceback. Can you fix whatever is "
    "broken?"
)
```

- [ ] **Step 2: Write `setup_scenario_b(dir_a, dir_b)`**

1. Call `setup_scenario_a(dir_a, dir_b)` — same base fixture with
   pre-modified transform.py
2. Additionally write `test_output.txt` into BOTH dir_a and dir_b
   root directories with the `TEST_OUTPUT_TXT` content

- [ ] **Step 3: Write `score_scenario_b(project_dir)`**

Same call-site scoring as Scenario A, plus:

1. **Revert check first**: Read `src/core/transform.py`. If it does
   NOT contain `mode: str = "strict"` (or contains `strict: bool`),
   classify as "revert" and return immediately with recall=0,
   classification="revert".
2. If not reverted, run the same `score_fixes()` logic.
3. Add classification field:
   - "revert" — transform.py was reverted
   - "symptom" — only test files were modified (check if any non-test
     fix in `EXPECTED_FIXES` was applied; if none, it's symptom-only)
   - "root_cause" — at least one source file (non-test) was fixed

```python
def score_scenario_b(project_dir):
    # Revert check
    transform_content = (Path(project_dir) / "src/core/transform.py").read_text()
    if 'mode: str = "strict"' not in transform_content:
        return {
            "recall": 0.0, "precision": 0.0,
            "classification": "revert",
            "correct": [], "missed": [f["description"] for f in EXPECTED_FIXES],
            "wrong": [], "false_positives": [],
        }

    result = score_fixes(project_dir)  # same as scenario A

    # Classify fix type
    source_files = {"src/preprocessing/normalize.py", "src/analysis/aggregate.py", "src/pipeline/run.py"}
    fixed_source = any(
        f["file"] in source_files
        for f in EXPECTED_FIXES
        if f["description"] in result["correct"]
    )
    result["classification"] = "root_cause" if fixed_source else "symptom"
    return result
```

---

## Task 4: Scenario C — "Rename a file"

**Files:** Continue editing `tests/test_experiment_v5.py`

- [ ] **Step 1: Copy fixture data from `test_experiment_a.py`**

Copy `FIXTURE_FILES` dict (lines 86-517 of `test_experiment_a.py`)
into the v5 script as `FIXTURE_FILES_DOCS`. This is the 35-file
wiki-link documentation fixture. Copy verbatim.

- [ ] **Step 2: Write scenario C constants**

```python
TARGET_C = "docs/design/02-processing-engine.md"
RENAMED_C = "docs/design/02-data-processing.md"

EXPECTED_REFS_C = [
    {
        "file": "docs/design/00-platform-overview.md",
        "old": "[[02-processing-engine]]",
        "new": "[[02-data-processing]]",
    },
    {
        "file": "docs/design/01-data-ingestion.md",
        "old": "[[02-processing-engine]]",
        "new": "[[02-data-processing]]",
    },
    {
        "file": "docs/design/05-scheduling.md",
        "old": "[[02-processing-engine]]",
        "new": "[[02-data-processing]]",
    },
    {
        "file": "docs/design/10-architecture.md",
        "old": "[[02-processing-engine]]",
        "new": "[[02-data-processing]]",
    },
    {
        "file": "docs/reference/design-notes.md",
        "old": "[[02-processing-engine]]",
        "new": "[[02-data-processing]]",
    },
    {
        "file": "configs/platform_config.yaml",
        "old": "docs/design/02-processing-engine.md",
        "new": "docs/design/02-data-processing.md",
    },
]

PROMPT_A_SCENARIO_C = (
    "Rename docs/design/02-processing-engine.md to "
    "docs/design/02-data-processing.md. Update the content to "
    "reflect the new name."
)

PROMPT_B_SCENARIO_C = (
    "Read CLAUDE.md first. Rename docs/design/02-processing-engine.md "
    "to docs/design/02-data-processing.md. Update the content to "
    "reflect the new name."
)
```

- [ ] **Step 3: Write `setup_scenario_c(dir_a, dir_b)`**

1. Call `create_fixture(dir_a, FIXTURE_FILES_DOCS)` and
   `create_fixture(dir_b, FIXTURE_FILES_DOCS)`
2. No pre-modifications — fixture is intact. The agent's job is to
   rename the file and (hopefully) update references.

- [ ] **Step 4: Write `score_scenario_c(project_dir)`**

```python
def score_scenario_c(project_dir):
    project = Path(project_dir)

    # Check file renamed
    old_exists = (project / TARGET_C).exists()
    new_exists = (project / RENAMED_C).exists()
    file_renamed = (not old_exists) and new_exists

    # Check references updated
    correct = []
    missed = []
    for ref in EXPECTED_REFS_C:
        filepath = project / ref["file"]
        if not filepath.exists():
            missed.append(ref)
            continue
        content = filepath.read_text(encoding="utf-8")
        has_old = ref["old"] in content
        has_new = ref["new"] in content
        if has_new and not has_old:
            correct.append(ref)
        else:
            missed.append(ref)

    total = len(EXPECTED_REFS_C)
    n_correct = len(correct)
    recall = n_correct / total if total else 1.0

    return {
        "file_renamed": file_renamed,
        "recall": recall,
        "precision": 1.0,  # no false positive concept for renames
        "correct": [r["file"] for r in correct],
        "missed": [r["file"] for r in missed],
        "refs_updated": n_correct,
        "refs_total": total,
    }
```

---

## Task 5: Dry-run validation and integration test

**Files:** Continue editing `tests/test_experiment_v5.py`

- [ ] **Step 1: Implement `dry_run_scenario()` for all three**

For each scenario, the dry-run should:
1. Build the fixture in a tmpdir
2. Apply scenario-specific setup
3. Run `kb-graph init` on project B
4. Validate the fixture is in expected state
5. Print PASS/FAIL for each check

**Scenario A checks:**
- `transform.py` contains `mode: str = "strict"`
- All 6 call sites contain `strict=True` or `strict=False`
- KB_INDEX.md exists and lists `transform.py` importers

**Scenario B checks:**
- Same as Scenario A
- `test_output.txt` exists and contains "TypeError"

**Scenario C checks:**
- Target file `docs/design/02-processing-engine.md` exists
- All 5 wiki-link files contain `[[02-processing-engine]]`
- Config file contains path to target
- `kb-graph traverse` output lists expected depth-1 files

- [ ] **Step 2: Run all three dry-runs**

```bash
wsl bash -c "cd /mnt/c/Users/mcap9/projects/bioinfo-agent-toolkit && \
  python3 tests/test_experiment_v5.py --scenario all --dry-run"
```

All three should print PASS. Fix any issues before proceeding.

---

## Task 6: Run experiments and document results

**Files:**
- `tests/test_experiment_v5.py` (run only, no edits)
- Modify: `docs/phoam_paint/phase5_v5_design.md` — add results section
- Modify: `docs/phoam_paint/plan.md` — update status

- [ ] **Step 1: Run all three scenarios — 1 trial with transcripts**

```bash
wsl bash -c "cd /mnt/c/Users/mcap9/projects/bioinfo-agent-toolkit && \
  python3 tests/test_experiment_v5.py --scenario all --save-transcripts"
```

This runs 6 agent invocations (3 scenarios x 2 agents). Expected
wall time: 6-15 minutes total.

Review results. Check transcripts for strategy usage.

- [ ] **Step 2: Document results in `docs/phoam_paint/phase5_v5_design.md`**

Add an "Experiment Results" section at the bottom. Follow the format
from `docs/phoam_paint/phase5_v4_design.md` results section. Include:
- Table per scenario: recall, precision, time, strategy for each agent
- Narrative of what happened
- Whether the experiment differentiated the agents
- Cross-scenario summary table

- [ ] **Step 3: Update `docs/phoam_paint/plan.md`**

Update the Phase 5 v5 status and the "Current State" section (section
0) with the actual outcome.

- [ ] **Step 4: Commit results**

```bash
git add tests/test_experiment_v5.py
git add docs/phoam_paint/phase5_v5_design.md
git add docs/phoam_paint/phase5_v5_plan.md
git add docs/phoam_paint/plan.md
git add tests/experiment_v5_a_results.json
git add tests/experiment_v5_b_results.json
git add tests/experiment_v5_c_results.json
git add tests/experiment_v5.log
git add tests/experiment_transcripts/v5*.txt
git commit -m "feat: Phase 5 v5 — realistic prompt experiment with 3 scenarios"
```

---

## Key Reference Files

When implementing, read these files for the exact fixture data and
infrastructure patterns to copy:

| What | Source | Lines |
|------|--------|-------|
| 80-file Python fixture data | `tests/test_experiment_b.py` | 80-825 |
| 35-file wiki-link fixture data | `tests/test_experiment_a.py` | 86-517 |
| Expected call-site fixes | `tests/test_experiment_b.py` | 835-875 |
| `SHOULD_NOT_MODIFY` list | `tests/test_experiment_b.py` | 876-885 |
| `_kb_graph_cmd()` helper | `tests/test_experiment_b.py` | 40-58 |
| `init_graph()` | `tests/test_experiment_b.py` | 942-961 |
| `run_agent()` | `tests/test_experiment_b.py` | 964-983 |
| `score_fixes()` (call-site) | `tests/test_experiment_b.py` | 986-1050 |
| Expected wiki-link refs | `tests/test_experiment_a.py` | 524-554 |
| `scan_markers()` (reference) | `tests/test_experiment_a.py` | 654-672 |
| Agent prompt patterns | `tests/test_experiment_a.py` | 562-583 |

## Constraints

- Python 3.10+ stdlib only
- kb-graph must be installed (`cp phoam_paint/kb_graph.py ~/.local/bin/kb-graph`)
- claude CLI must be installed and authenticated
- Run via WSL on Windows: `wsl bash -c "cd /mnt/c/... && python3 ..."`
- Do NOT modify `tests/test_experiment_a.py` or `tests/test_experiment_b.py`
- Do NOT modify `tests/fixtures/sample_project/`
- Each scenario runs 2 agents; `--scenario all` runs 6 total
- Default timeout: 300s per agent
