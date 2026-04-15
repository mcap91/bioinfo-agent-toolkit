# Phase 5 v4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement two A/B experiments proving kb-graph's value: (A) doc-graph impact analysis via wiki-links, (B) code intelligence via function signatures in KB_INDEX.md.

**Architecture:** Two independent experiment scripts (`test_experiment_a.py`, `test_experiment_b.py`) each with embedded fixture data, agent invocation via `claude` CLI, and automated scoring. Experiment B requires enhancing `kb_graph.py`'s Python parser to extract `def`/`class` signatures and the `write_kb_index()` function to emit `exports:` lines. Shared patterns (logging, agent runner, CLI args) are inlined in each script — no shared module (they must run independently).

**Tech Stack:** Python 3.10+ stdlib only. `claude` CLI for agent invocation. `kb-graph` CLI for graph operations.

**Spec:** `docs/phoam_paint/phase5_v4_design.md`

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `phoam_paint/kb_graph.py` | Modify | Add `extract_exports()` function, update `build_graph()` to store exports in node metadata, update `write_kb_index()` to emit `exports:` lines |
| `tests/test_kb_graph_exports.py` | Create | Unit tests for the new `extract_exports()` function |
| `tests/test_experiment_a.py` | Create | Experiment A: doc-graph impact analysis (fixture, runner, scoring) |
| `tests/test_experiment_b.py` | Create | Experiment B: code intelligence signature change (fixture, runner, scoring) |

---

## Task 1: Add `extract_exports()` to `kb_graph.py`

**Files:**
- Modify: `phoam_paint/kb_graph.py:285-396` (after `parse_python`, before `parse_markdown`)
- Test: `tests/test_kb_graph_exports.py`

This adds a new function that extracts top-level `def` signatures and `class` definitions from Python files. It does NOT modify the parser or edge logic — it's a separate extraction pass used by `build_graph()`.

- [ ] **Step 1: Write failing tests for `extract_exports()`**

Create `tests/test_kb_graph_exports.py`:

```python
#!/usr/bin/env python3
"""Tests for extract_exports() — function/class signature extraction."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from phoam_paint.kb_graph import extract_exports


class TestExtractExports(unittest.TestCase):
    """Test extract_exports() on various Python file patterns."""

    def _write_temp(self, content):
        """Write content to a temp .py file, return its path."""
        fd, path = tempfile.mkstemp(suffix=".py")
        with os.fdopen(fd, "w") as f:
            f.write(content)
        self.addCleanup(os.unlink, path)
        return path

    def test_simple_function(self):
        path = self._write_temp(
            'def hello(name: str) -> str:\n    return f"Hello {name}"\n'
        )
        exports = extract_exports(path)
        self.assertEqual(exports, ["hello(name: str) -> str"])

    def test_simple_class(self):
        path = self._write_temp(
            "class Config:\n    pass\n"
        )
        exports = extract_exports(path)
        self.assertEqual(exports, ["class Config"])

    def test_class_with_base(self):
        path = self._write_temp(
            "class PipelineError(Exception):\n    pass\n"
        )
        exports = extract_exports(path)
        self.assertEqual(exports, ["class PipelineError(Exception)"])

    def test_multiline_signature(self):
        path = self._write_temp(
            "def transform(\n"
            "    data: DataFrame,\n"
            "    config: Config,\n"
            "    strict: bool = True,\n"
            ") -> DataFrame:\n"
            "    pass\n"
        )
        exports = extract_exports(path)
        self.assertEqual(
            exports,
            ["transform(data: DataFrame, config: Config, strict: bool = True) -> DataFrame"],
        )

    def test_skips_private_functions(self):
        path = self._write_temp(
            "def public_func():\n    pass\n\n"
            "def _private_func():\n    pass\n\n"
            "def __dunder_func__():\n    pass\n"
        )
        exports = extract_exports(path)
        self.assertEqual(exports, ["public_func()"])

    def test_skips_nested_functions(self):
        path = self._write_temp(
            "def outer():\n"
            "    def inner():\n"
            "        pass\n"
            "    return inner\n"
        )
        exports = extract_exports(path)
        self.assertEqual(exports, ["outer()"])

    def test_skips_methods_inside_class(self):
        path = self._write_temp(
            "class Foo:\n"
            "    def method(self):\n"
            "        pass\n\n"
            "def standalone():\n"
            "    pass\n"
        )
        exports = extract_exports(path)
        self.assertEqual(exports, ["class Foo", "standalone()"])

    def test_mixed_file(self):
        path = self._write_temp(
            '"""Module docstring."""\n'
            "import os\n\n"
            "MAX_RETRIES = 3\n\n\n"
            "class TransformConfig:\n"
            "    pass\n\n\n"
            "def apply_transform(data: DataFrame, config: TransformConfig, strict: bool = True) -> DataFrame:\n"
            "    pass\n\n\n"
            "def validate_schema(data: DataFrame, schema: Dict[str, str]) -> bool:\n"
            "    pass\n\n\n"
            "def _internal_helper():\n"
            "    pass\n"
        )
        exports = extract_exports(path)
        self.assertEqual(exports, [
            "class TransformConfig",
            "apply_transform(data: DataFrame, config: TransformConfig, strict: bool = True) -> DataFrame",
            "validate_schema(data: DataFrame, schema: Dict[str, str]) -> bool",
        ])

    def test_no_return_type(self):
        path = self._write_temp(
            "def setup(config):\n    pass\n"
        )
        exports = extract_exports(path)
        self.assertEqual(exports, ["setup(config)"])

    def test_empty_file(self):
        path = self._write_temp("")
        exports = extract_exports(path)
        self.assertEqual(exports, [])

    def test_init_file_no_exports(self):
        path = self._write_temp(
            "from .transform import apply_transform\n"
            "from .config import Config\n"
        )
        exports = extract_exports(path)
        self.assertEqual(exports, [])

    def test_multiline_with_defaults(self):
        path = self._write_temp(
            "def process(\n"
            '    data: List[str],\n'
            '    mode: str = "strict",\n'
            "    verbose: bool = False,\n"
            "):\n"
            "    pass\n"
        )
        exports = extract_exports(path)
        self.assertEqual(
            exports,
            ['process(data: List[str], mode: str = "strict", verbose: bool = False)'],
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 tests/test_kb_graph_exports.py -v`
Expected: `ImportError: cannot import name 'extract_exports' from 'phoam_paint.kb_graph'`

- [ ] **Step 3: Implement `extract_exports()`**

Add this function to `phoam_paint/kb_graph.py` after the `parse_python()` function (after line 396, before `parse_markdown`):

```python
def extract_exports(filepath):
    """Extract top-level function signatures and class definitions from a Python file.

    Returns a list of strings like:
        "apply_transform(data: DataFrame, config: Config, strict: bool = True) -> DataFrame"
        "class TransformConfig"
        "class PipelineError(Exception)"

    Skips private functions (_prefixed), nested functions, and methods inside classes.
    Handles multiline signatures (parentheses spanning multiple lines).
    """
    try:
        with open(filepath, "r", errors="ignore") as f:
            lines = f.readlines()
    except OSError:
        return []

    exports = []
    indent_in_class = False  # True when we're inside a class body
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()
        leading_spaces = len(line) - len(line.lstrip())

        # Track whether we're inside a class body (indented)
        if stripped and not stripped.startswith("#"):
            if leading_spaces == 0:
                indent_in_class = False

        # Top-level class definition
        if leading_spaces == 0 and re.match(r"^class\s+", stripped):
            m = re.match(r"^class\s+(\w+)(?:\(([^)]*)\))?\s*:", stripped)
            if m:
                name = m.group(1)
                bases = m.group(2)
                if bases:
                    exports.append(f"class {name}({bases.strip()})")
                else:
                    exports.append(f"class {name}")
                indent_in_class = True
            i += 1
            continue

        # Top-level function definition (not inside a class, not private)
        if leading_spaces == 0 and re.match(r"^def\s+", stripped) and not indent_in_class:
            m = re.match(r"^def\s+(\w+)\s*\(", stripped)
            if m:
                name = m.group(1)
                # Skip private functions
                if name.startswith("_"):
                    i += 1
                    continue

                # Collect the full signature (may span multiple lines)
                sig_lines = [stripped]
                # Check if parentheses are balanced
                paren_depth = stripped.count("(") - stripped.count(")")
                j = i + 1
                while paren_depth > 0 and j < len(lines):
                    sig_lines.append(lines[j].rstrip())
                    paren_depth += lines[j].count("(") - lines[j].count(")")
                    j += 1

                full_sig = " ".join(s.strip() for s in sig_lines)

                # Extract: def name(params) -> return_type:
                sig_match = re.match(
                    r"def\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*(.+?))?\s*:",
                    full_sig,
                )
                if sig_match:
                    func_name = sig_match.group(1)
                    params_raw = sig_match.group(2)
                    return_type = sig_match.group(3)

                    # Clean up params: collapse whitespace, strip trailing commas
                    params = ", ".join(
                        p.strip() for p in params_raw.split(",") if p.strip()
                    )

                    if return_type:
                        exports.append(f"{func_name}({params}) -> {return_type.strip()}")
                    else:
                        exports.append(f"{func_name}({params})")

            i += 1
            continue

        # Inside a class body — skip methods (they're indented)
        if leading_spaces > 0 and indent_in_class and re.match(r"\s+def\s+", line):
            i += 1
            continue

        i += 1

    return exports
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 tests/test_kb_graph_exports.py -v`
Expected: All 13 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add phoam_paint/kb_graph.py tests/test_kb_graph_exports.py
git commit -m "feat: add extract_exports() for Python function/class signature extraction"
```

---

## Task 2: Integrate exports into `build_graph()` and `write_kb_index()`

**Files:**
- Modify: `phoam_paint/kb_graph.py:521-555` (`build_graph()`), `phoam_paint/kb_graph.py:584-723` (`write_kb_index()`)
- Test: `tests/test_kb_graph_exports.py` (add integration tests)

- [ ] **Step 1: Write failing integration tests**

Append to `tests/test_kb_graph_exports.py`:

```python
from phoam_paint.kb_graph import build_graph, write_kb_index


class TestExportsInGraph(unittest.TestCase):
    """Test that exports appear in the graph and KB_INDEX.md."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        # Create a minimal Python project
        src_dir = os.path.join(self.tmpdir, "src")
        os.makedirs(src_dir)

        with open(os.path.join(src_dir, "transform.py"), "w") as f:
            f.write(
                '"""Data transformation utilities."""\n\n'
                "class TransformConfig:\n"
                "    pass\n\n\n"
                "def apply_transform(data, config, strict: bool = True):\n"
                "    pass\n\n\n"
                "def _helper():\n"
                "    pass\n"
            )

        with open(os.path.join(src_dir, "main.py"), "w") as f:
            f.write(
                "from transform import apply_transform\n\n"
                "apply_transform(None, None)\n"
            )

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_graph_nodes_have_exports(self):
        graph = build_graph(self.tmpdir)
        transform_node = graph["nodes"].get("src/transform.py")
        self.assertIsNotNone(transform_node)
        self.assertIn("exports", transform_node)
        self.assertEqual(len(transform_node["exports"]), 2)  # class + function, not _helper
        self.assertIn("class TransformConfig", transform_node["exports"])
        self.assertIn(
            "apply_transform(data, config, strict: bool = True)",
            transform_node["exports"],
        )

    def test_graph_nodes_without_exports(self):
        graph = build_graph(self.tmpdir)
        main_node = graph["nodes"].get("src/main.py")
        self.assertIsNotNone(main_node)
        # main.py has no top-level def/class exports
        self.assertEqual(main_node.get("exports", []), [])

    def test_kb_index_contains_exports(self):
        graph = build_graph(self.tmpdir)
        output_path = write_kb_index(graph, self.tmpdir)
        with open(output_path) as f:
            content = f.read()
        self.assertIn("exports:", content)
        self.assertIn("apply_transform(data, config, strict: bool = True)", content)
        self.assertIn("class TransformConfig", content)
        # Private functions should NOT appear
        self.assertNotIn("_helper", content)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 tests/test_kb_graph_exports.py TestExportsInGraph -v`
Expected: FAIL — `build_graph()` doesn't populate `exports` in nodes yet.

- [ ] **Step 3: Update `build_graph()` to populate exports**

In `phoam_paint/kb_graph.py`, modify the `build_graph()` function. In the "Build nodes" loop (around line 531-536), add exports extraction for Python files:

Replace:
```python
    # Build nodes
    for filepath in tracked_files:
        nodes[filepath] = {
            "description": get_description(filepath, repo_root),
            "group": get_group(filepath),
            "type": get_file_type(filepath),
        }
```

With:
```python
    # Build nodes
    for filepath in tracked_files:
        node = {
            "description": get_description(filepath, repo_root),
            "group": get_group(filepath),
            "type": get_file_type(filepath),
        }
        # Extract function/class exports for Python files
        if os.path.splitext(filepath)[1] == ".py":
            full_path = os.path.join(repo_root, filepath)
            node["exports"] = extract_exports(full_path)
        else:
            node["exports"] = []
        nodes[filepath] = node
```

- [ ] **Step 4: Update `write_kb_index()` to emit exports**

In `phoam_paint/kb_graph.py`, inside `write_kb_index()`, add exports output for code files. Find the block that handles `file_type == "code"` (around line 644). After the description line and before the imports line, add exports:

Replace the code block starting at line 644:
```python
            if file_type == "code":
                # Imports (outbound import edges)
                import_edges = [e for e in outbound[filepath] if e["type"] == "import"]
```

With:
```python
            if file_type == "code":
                # Exports (function signatures, class definitions)
                file_exports = nodes[filepath].get("exports", [])
                for export in file_exports:
                    lines.append(f"  - exports: `{export}`")

                # Imports (outbound import edges)
                import_edges = [e for e in outbound[filepath] if e["type"] == "import"]
```

- [ ] **Step 5: Run all tests to verify they pass**

Run: `python3 tests/test_kb_graph_exports.py -v`
Expected: All tests PASS (both unit tests from Task 1 and integration tests from this task).

Also run existing tests to verify no regressions:

Run: `python3 tests/test_graph_mutations.py -v`
Expected: All 20 tests PASS.

Run: `python3 tests/test_generated_graph.py -v`
Expected: All 28 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add phoam_paint/kb_graph.py tests/test_kb_graph_exports.py
git commit -m "feat: integrate function/class exports into graph nodes and KB_INDEX.md"
```

---

## Task 3: Build Experiment A — Doc-Graph Impact Analysis

**Files:**
- Create: `tests/test_experiment_a.py`

This experiment tests wiki-link traversal in a doc-heavy fixture. No tool changes needed — uses existing wiki-link and config-ref parsers. The script follows the same structure as `test_agent_experiment.py` (v3) but with a completely different fixture and task.

- [ ] **Step 1: Create the experiment script with fixture data**

Create `tests/test_experiment_a.py`. The fixture defines ~35 files for a fictional data analytics platform with wiki-linked design docs.

```python
#!/usr/bin/env python3
"""Phase 5 v4 — Experiment A: Doc-Graph Impact Analysis

Tests whether kb-graph helps a Claude agent identify affected documents
in a wiki-link-connected knowledge base. The fixture is a set of design
docs for a fictional data analytics platform, connected by [[wiki-links]]
in prose. There are no code import chains — the only dependency mechanism
is wiki-links and config path references.

Target: docs/design/02-processing-engine.md
Expected blast radius: 13 files across depths 1-3.

Requirements:
    - Claude Code CLI (`claude` command on PATH)
    - API access configured (ANTHROPIC_API_KEY or OAuth)
    - kb-graph installed (`kb-graph` on PATH)

Usage:
    python3 tests/test_experiment_a.py                  # 1 trial
    python3 tests/test_experiment_a.py --trials 3       # 3 trials
    python3 tests/test_experiment_a.py --model sonnet   # use sonnet
    python3 tests/test_experiment_a.py --save-transcripts
    python3 tests/test_experiment_a.py --dry-run        # validate fixture only
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
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# ── Logging ──────────────────────────────────────────────────────────────

_log_file = None


def log(msg=""):
    print(msg)
    if _log_file is not None:
        _log_file.write(msg + "\n")
        _log_file.flush()


# ── Version Info ─────────────────────────────────────────────────────────

def get_claude_version():
    try:
        result = subprocess.run(
            ["claude", "--version"], capture_output=True, text=True, timeout=10,
        )
        return result.stdout.strip() or result.stderr.strip() or "unknown"
    except Exception:
        return "unknown"


# ── Fixture Files ────────────────────────────────────────────────────────
# ~35 files: design docs connected by [[wiki-links]], config files with
# path references, and noise files that mention "processing" without
# wiki-linking to the target.

FIXTURE_FILES = {
    # ── TARGET ───────────────────────────────────────────────────────
    "docs/design/02-processing-engine.md": """\
# Processing Engine

The processing engine handles all data transformation, enrichment, and
validation steps. It receives raw ingestion batches from the
[[01-data-ingestion]] system and writes results to the [[03-storage-layer]].

## Core Pipeline

The engine uses a DAG-based execution model with the [[05-scheduling]]
system managing step ordering and retries. All pipeline access is
governed by [[06-security-auth]] policies.

## Data Formats

Supports Parquet, CSV, and JSON. Schema validation happens before
any transformation step.

## Error Handling

Failed batches are quarantined and flagged for manual review.
""",

    # ── DESIGN DOCS ──────────────────────────────────────────────────

    "docs/design/00-platform-overview.md": """\
# Platform Overview

The data analytics platform provides end-to-end data processing,
storage, querying, and visualization.

## Key Subsystems

- [[01-data-ingestion]] — batch and streaming data intake
- [[02-processing-engine]] — transformation and enrichment
- [[03-storage-layer]] — durable columnar storage
- [[04-query-api]] — SQL and programmatic access
- [[05-scheduling]] — job orchestration
- [[06-security-auth]] — access control and audit logging
- [[07-ui-dashboard]] — monitoring and exploration
- [[08-alerting]] — threshold and anomaly alerting
- [[10-architecture]] — system design and infrastructure
""",

    "docs/design/01-data-ingestion.md": """\
# Data Ingestion

Handles batch file uploads, streaming connectors, and webhook
receivers. Validated data is forwarded to the [[02-processing-engine]]
for transformation.

## Connectors

Supports S3, GCS, Kafka, and HTTP webhooks. Each connector
implements the IngestionAdapter interface.

## Validation

Schema checks happen at ingest time. Invalid records are logged
and routed to a dead-letter queue. Security policies from
[[06-security-auth]] govern which sources are permitted.
""",

    "docs/design/03-storage-layer.md": """\
# Storage Layer

Columnar storage backed by Parquet files on object storage.
Provides the data substrate for the [[04-query-api]].

## Partitioning

Data is partitioned by date and source. Compaction runs nightly.

## Retention

Configurable retention policies per dataset. Expired data is
archived to cold storage before deletion.
""",

    "docs/design/04-query-api.md": """\
# Query API

SQL and programmatic access to data in the [[03-storage-layer]].

## Endpoints

- `/query` — ad-hoc SQL queries
- `/datasets` — dataset metadata
- `/export` — bulk data export

## Authentication

All requests require a valid token from the auth system.
""",

    "docs/design/05-scheduling.md": """\
# Scheduling

Job orchestration for the [[01-data-ingestion]] and
[[02-processing-engine]] systems. Manages dependencies, retries,
and backpressure.

## DAG Execution

Jobs are modeled as DAGs. The scheduler ensures upstream steps
complete before downstream steps begin.

## Monitoring

Job status is exposed to the dashboard via a metrics endpoint.
""",

    "docs/design/06-security-auth.md": """\
# Security & Authentication

Access control and audit logging for the platform. Governs access
to the [[01-data-ingestion]] endpoints and the [[07-ui-dashboard]].

## Token Model

JWT-based tokens with role claims. Tokens are rotated every 24h.

## Audit Log

All data access is logged with user, timestamp, and query hash.
""",

    "docs/design/07-ui-dashboard.md": """\
# UI Dashboard

Monitoring and exploration interface for platform operators.

## Features

- Real-time job status
- Query history browser
- Dataset explorer
- Alert configuration

## Technology

React + TypeScript SPA served from a CDN.
""",

    "docs/design/08-alerting.md": """\
# Alerting

Threshold and anomaly alerting with notifications to the
[[07-ui-dashboard]] and external channels (email, Slack).

## Rules

Alert rules are defined as YAML configs. Each rule specifies
a metric, threshold, and notification target.

## Silencing

Operators can silence alerts during maintenance windows.
""",

    "docs/design/09-open-questions.md": """\
# Open Questions

Unresolved design decisions tracked here. See
[[00-platform-overview]] for the full system map.

## Questions

1. Should we support real-time streaming queries?
2. How should cross-region replication work?
3. What SLA targets for the query API?
""",

    "docs/design/10-architecture.md": """\
# Architecture

System design and infrastructure for the platform. Covers
deployment topology, service boundaries, and data flow.

## Services

The platform is composed of:
- [[01-data-ingestion]] service (Go)
- [[02-processing-engine]] service (Python)
- Storage and query services (Rust)

## Infrastructure

Kubernetes on GCP with Terraform-managed infrastructure.
""",

    # ── REFERENCE DOCS ───────────────────────────────────────────────

    "docs/reference/setup.md": """\
# Setup Guide

Instructions for setting up a development environment.
See [[10-architecture]] for the full system topology.

## Prerequisites

- Docker Desktop
- kubectl
- Terraform 1.5+
""",

    "docs/reference/tool-catalog.md": """\
# Tool Catalog

List of tools used across the platform.

## Build Tools

- Bazel for monorepo builds
- Docker for containerization

## Monitoring

- Prometheus for metrics
- Grafana for dashboards
""",

    "docs/reference/research-notes.md": """\
# Research Notes

Background research and spikes.

## Ingestion Benchmarks

Tested throughput for the [[01-data-ingestion]] connectors.
S3 connector achieves 50k records/sec. Kafka connector
achieves 200k records/sec.

## Security Audit

Reviewed the [[06-security-auth]] token rotation mechanism.
Recommended reducing rotation interval to 12h.
""",

    "docs/reference/design-notes.md": """\
# Design Notes

Informal notes from design sessions.

## Session 2026-03-15

Discussed the [[02-processing-engine]] DAG execution model.
Decided on pull-based scheduling over push-based.

## Session 2026-03-22

Reviewed the [[03-storage-layer]] partitioning strategy.
Agreed on date + source composite partitioning.
""",

    # ── GUIDES ───────────────────────────────────────────────────────

    "docs/guides/getting-started.md": """\
# Getting Started

Quick start guide for new developers.

Start by reading the [[00-platform-overview]] to understand the
system. Then follow the [[setup.md]] instructions to configure
your local environment.

## First Steps

1. Clone the repo
2. Run `make setup`
3. Start the local cluster with `make dev`
""",

    "docs/guides/admin-guide.md": """\
# Admin Guide

Operations and maintenance procedures.

## Data Processing

The data processing pipeline runs on a fixed schedule. If a batch
fails, check the processing logs in Grafana. Processing errors
are usually caused by schema mismatches.

## Scaling

Adjust replica counts in the Helm values file.
""",

    "docs/guides/performance-guide.md": """\
# Performance Guide

Performance tuning and optimization.

See [[10-architecture]] for the system topology that informs
these recommendations.

## Query Optimization

Use partitioned scans where possible. Avoid full-table scans
on datasets larger than 10TB.

## Ingestion Tuning

Increase batch size for higher throughput. Monitor backpressure
metrics.
""",

    # ── CONFIG FILES ─────────────────────────────────────────────────

    "configs/platform_config.yaml": """\
# Platform configuration
api_port: 8080
log_level: info
processing_doc: "docs/design/02-processing-engine.md"
max_workers: 16
""",

    "configs/limits.yaml": """\
# Resource limits
query_timeout_seconds: 300
max_export_rows: 1000000
storage_doc: "docs/design/03-storage-layer.md"
retention_days: 90
""",

    "configs/deploy_config.yaml": """\
# Deployment configuration
cluster: prod-us-east
namespace: analytics
replicas: 3
processing_threads: 8
image_tag: latest
""",

    # ── SCRIPTS (noise) ──────────────────────────────────────────────

    "scripts/build.sh": """\
#!/usr/bin/env bash
# Build all services
set -euo pipefail
echo "Building platform services..."
docker compose build
""",

    "scripts/deploy.sh": """\
#!/usr/bin/env bash
# Deploy to staging
set -euo pipefail
echo "Deploying to staging..."
kubectl apply -f k8s/
""",

    # ── ROOT FILES ───────────────────────────────────────────────────

    "README.md": """\
# Data Analytics Platform

End-to-end data processing and analytics.

See [[00-platform-overview]] for the full system design.

## Quick Start

```bash
make setup
make dev
```
""",

    "CHANGELOG.md": """\
# Changelog

## v2.3.0 (2026-04-01)

- Upgraded processing engine v2.1 to support Parquet V2
- Fixed query API timeout handling
- Added batch retry logic to ingestion

## v2.2.0 (2026-03-15)

- Initial scheduling system
- Dashboard v1.0
""",

    # ── PADDING / NOISE FILES ────────────────────────────────────────

    "docs/design/README.md": """\
# Design Documents

This directory contains the canonical design documents for the
platform. Each document covers one subsystem.

See `00-platform-overview.md` for the index.
""",

    "docs/reference/glossary.md": """\
# Glossary

- **DAG**: Directed Acyclic Graph
- **DLQ**: Dead Letter Queue
- **SLA**: Service Level Agreement
""",

    "docs/guides/troubleshooting.md": """\
# Troubleshooting

Common issues and solutions.

## Ingestion Failures

Check the connector logs. Most failures are transient network errors.

## Query Timeouts

Increase the timeout in `configs/limits.yaml`.
""",

    "LICENSE": """\
MIT License

Copyright (c) 2026 Example Corp
""",

    ".phoamignore": """\
# Ignore non-doc files for graph scanning
node_modules/
.git/
""",
}

# ── Ground Truth ─────────────────────────────────────────────────────

TARGET = "docs/design/02-processing-engine.md"
MARKER = "<!-- AFFECTED -->"

EXPECTED_DEPTH_1 = [
    "docs/design/00-platform-overview.md",
    "docs/design/05-scheduling.md",
    "docs/design/10-architecture.md",
    "docs/reference/design-notes.md",
    "configs/platform_config.yaml",
]

EXPECTED_DEPTH_2 = [
    "docs/design/01-data-ingestion.md",      # links to 05-scheduling
    "docs/design/09-open-questions.md",       # links to 00-platform-overview
    "docs/guides/getting-started.md",         # links to 00-platform-overview
    "README.md",                              # links to 00-platform-overview
    "docs/reference/setup.md",                # links to 10-architecture
    "docs/guides/performance-guide.md",       # links to 10-architecture
]

EXPECTED_DEPTH_3 = [
    "docs/design/06-security-auth.md",        # links to 01-data-ingestion
    "docs/reference/research-notes.md",       # links to 01-data-ingestion
]

EXPECTED_BLAST_RADIUS = EXPECTED_DEPTH_1 + EXPECTED_DEPTH_2 + EXPECTED_DEPTH_3

DEPTH_GROUPS = {
    1: set(EXPECTED_DEPTH_1),
    2: set(EXPECTED_DEPTH_2),
    3: set(EXPECTED_DEPTH_3),
}

RED_HERRING_FILES = [
    "docs/guides/admin-guide.md",      # mentions "processing" in prose
    "CHANGELOG.md",                    # mentions "processing engine v2.1"
    "configs/deploy_config.yaml",      # has processing_threads: 8
]

# ── Agent Prompts ────────────────────────────────────────────────────

PROMPT_A = (
    "The processing engine (docs/design/02-processing-engine.md) is being "
    "completely redesigned. Add `<!-- AFFECTED -->` as the very first line "
    "of every file that would need updating — include all transitive "
    "dependents at any depth. A file is a dependent if it contains a "
    "[[wiki-link]] to the target OR to any other affected file. Config "
    "files that reference affected files by path are also dependents. Do "
    "not modify 02-processing-engine.md itself. Do not explain, just make "
    "the changes."
)

PROMPT_B = (
    "Read CLAUDE.md first. The processing engine "
    "(docs/design/02-processing-engine.md) is being completely redesigned. "
    "Run `kb-graph traverse docs/design/02-processing-engine.md --depth 3` "
    "to get the complete list of affected files. Add `<!-- AFFECTED -->` "
    "as the very first line of every file in the traverse output. Do not "
    "modify 02-processing-engine.md itself. Do not explain, just make the "
    "changes."
)


# ── Helpers ──────────────────────────────────────────────────────────

def check_prerequisites():
    missing = []
    for cmd in ("claude", "kb-graph"):
        if shutil.which(cmd) is None:
            missing.append(cmd)
    if missing:
        log(f"ERROR: Missing prerequisites: {', '.join(missing)}")
        sys.exit(1)


def create_fixture(dest):
    """Write all fixture files to dest directory."""
    for rel_path, content in FIXTURE_FILES.items():
        filepath = Path(dest) / rel_path
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)


def init_graph(project_dir):
    """Run kb-graph init on a project directory."""
    subprocess.run(
        ["git", "init", "-q"], cwd=project_dir, capture_output=True,
    )
    subprocess.run(
        ["git", "add", "."], cwd=project_dir, capture_output=True,
    )
    subprocess.run(
        ["git", "commit", "-q", "-m", "initial", "--no-gpg-sign"],
        cwd=project_dir, capture_output=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "test@test",
             "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "test@test"},
    )
    result = subprocess.run(
        ["kb-graph", "init", "."], cwd=project_dir,
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        log(f"WARNING: kb-graph init failed:\n{result.stderr}")
    return result.returncode == 0


def run_agent(project_dir, prompt, *, model=None, timeout=300):
    cmd = [
        "claude", "-p", prompt,
        "--dangerously-skip-permissions", "--no-session-persistence",
    ]
    if model:
        cmd.extend(["--model", model])

    start = time.monotonic()
    try:
        result = subprocess.run(
            cmd, cwd=project_dir, capture_output=True, text=True,
            timeout=timeout,
            env={**os.environ, "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"},
        )
        elapsed = time.monotonic() - start
        return result.stdout, result.stderr, result.returncode, elapsed
    except subprocess.TimeoutExpired:
        elapsed = time.monotonic() - start
        return "", f"TIMEOUT after {timeout}s", -1, elapsed


def scan_markers(project_dir):
    """Scan all files for the AFFECTED marker on line 1."""
    marked = set()
    project = Path(project_dir)
    for filepath in project.rglob("*"):
        if not filepath.is_file():
            continue
        rel = str(filepath.relative_to(project)).replace("\\", "/")
        if any(part.startswith(".") for part in Path(rel).parts):
            continue
        if Path(rel).name in ("KB_INDEX.md", "graph.html"):
            continue
        try:
            first_line = filepath.read_text().split("\n", 1)[0].strip()
        except (UnicodeDecodeError, PermissionError):
            continue
        if first_line == MARKER:
            marked.add(rel)
    return marked


def classify_results(marked_files, expected_files):
    expected = set(expected_files)
    hits = marked_files & expected
    misses = expected - marked_files
    false_positives = marked_files - expected
    recall = len(hits) / len(expected) if expected else 1.0
    precision = len(hits) / len(marked_files) if marked_files else 0.0
    return {
        "hits": sorted(hits),
        "misses": sorted(misses),
        "false_positives": sorted(false_positives),
        "recall": recall,
        "precision": precision,
        "perfect": len(misses) == 0,
    }


# ── Dry Run ──────────────────────────────────────────────────────────

def dry_run():
    """Validate fixture + ground truth without running agents."""
    log("DRY RUN: Validating fixture and ground truth...\n")

    tmpdir = tempfile.mkdtemp(prefix="kb_exp_a_dry_")
    try:
        create_fixture(tmpdir)

        # Verify all expected files exist
        for rel_path in EXPECTED_BLAST_RADIUS:
            fp = Path(tmpdir) / rel_path
            assert fp.exists(), f"Expected blast radius file missing: {rel_path}"
        log(f"  {len(EXPECTED_BLAST_RADIUS)} blast radius files exist in fixture")

        # Verify red herring files exist
        for rel_path in RED_HERRING_FILES:
            fp = Path(tmpdir) / rel_path
            assert fp.exists(), f"Red herring file missing: {rel_path}"
        log(f"  {len(RED_HERRING_FILES)} red herring files exist in fixture")

        # Verify target exists
        assert (Path(tmpdir) / TARGET).exists(), f"Target missing: {TARGET}"
        log(f"  Target file exists: {TARGET}")

        # Init graph and validate traverse output
        log("\n  Running kb-graph init...")
        if not init_graph(tmpdir):
            log("  WARNING: kb-graph init had issues")

        log("  Running kb-graph traverse...")
        result = subprocess.run(
            ["kb-graph", "traverse", TARGET, "--depth", "3"],
            cwd=tmpdir, capture_output=True, text=True,
        )
        log(f"  Traverse output:\n{result.stdout}")

        # Parse traverse output for file paths
        traverse_files = set()
        for line in result.stdout.split("\n"):
            line = line.strip()
            # Lines like "├── docs/design/00-platform-overview.md ─── ..."
            # or just file paths
            for token in line.split():
                token = token.strip("├└──│─ ")
                if "/" in token and not token.startswith("BLAST"):
                    # Check if it looks like a file path
                    if any(token.endswith(ext) for ext in (".md", ".yaml", ".yml", ".py", ".sh")):
                        traverse_files.add(token)

        # Compare traverse output with expected blast radius
        expected = set(EXPECTED_BLAST_RADIUS)
        missing = expected - traverse_files
        extra = traverse_files - expected - {TARGET}

        if missing:
            log(f"\n  WARNING: Expected files NOT in traverse output: {sorted(missing)}")
        if extra:
            log(f"\n  WARNING: Extra files in traverse output: {sorted(extra)}")

        # Check red herrings are NOT in traverse
        for rh in RED_HERRING_FILES:
            if rh in traverse_files:
                log(f"  ERROR: Red herring leaked into traverse: {rh}")

        if not missing and not extra:
            log("\n  PASS: Ground truth matches traverse output exactly.")
        else:
            log("\n  FAIL: Ground truth mismatch. Review fixture wiki-links.")

        # Total file count
        total = sum(1 for _ in Path(tmpdir).rglob("*") if _.is_file()
                    and not any(p.startswith(".") for p in _.relative_to(tmpdir).parts))
        log(f"\n  Total fixture files: {total}")
        log(f"  Blast radius: {len(EXPECTED_BLAST_RADIUS)}")
        log(f"  Noise files: {total - len(EXPECTED_BLAST_RADIUS) - 1}")  # -1 for target

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# ── Trial Runner ─────────────────────────────────────────────────────

def run_trial(trial_num, *, model=None, save_transcripts=False, timeout=300):
    log(f"\n{'='*60}")
    log(f"  Trial {trial_num}")
    log(f"{'='*60}")

    tmpdir = tempfile.mkdtemp(prefix=f"kb_exp_a_{trial_num}_")
    dir_a = os.path.join(tmpdir, "project_a")
    dir_b = os.path.join(tmpdir, "project_b")

    try:
        log(f"  Setting up projects in {tmpdir}")
        os.makedirs(dir_a)
        os.makedirs(dir_b)
        create_fixture(dir_a)
        create_fixture(dir_b)

        expected_count = len(EXPECTED_BLAST_RADIUS)
        for rel_path in EXPECTED_BLAST_RADIUS:
            assert (Path(dir_a) / rel_path).exists(), f"Missing: {rel_path}"
        log(f"  Fixture verified: {expected_count} expected blast radius files")

        # Init graph on project B only
        log("  Running kb-graph init on project B...")
        if not init_graph(dir_b):
            log("  WARNING: kb-graph init had issues")

        has_index = (Path(dir_b) / "KB_INDEX.md").exists()
        has_claude_md = (Path(dir_b) / "CLAUDE.md").exists()
        log(f"  Project B: KB_INDEX.md={has_index}, CLAUDE.md={has_claude_md}")

        # Run agents
        log(f"\n  Running Agent A (no graph)...")
        stdout_a, stderr_a, rc_a, elapsed_a = run_agent(
            dir_a, PROMPT_A, model=model, timeout=timeout
        )
        log(f"  Agent A finished in {elapsed_a:.1f}s (exit={rc_a})")

        log(f"  Running Agent B (with graph)...")
        stdout_b, stderr_b, rc_b, elapsed_b = run_agent(
            dir_b, PROMPT_B, model=model, timeout=timeout
        )
        log(f"  Agent B finished in {elapsed_b:.1f}s (exit={rc_b})")

        # Score
        marked_a = scan_markers(dir_a)
        marked_b = scan_markers(dir_b)
        results_a = classify_results(marked_a, EXPECTED_BLAST_RADIUS)
        results_b = classify_results(marked_b, EXPECTED_BLAST_RADIUS)

        log(f"\n  Results:")
        log(f"  Agent A: recall={results_a['recall']:.0%} ({len(results_a['hits'])}/{expected_count}), "
            f"precision={results_a['precision']:.0%}, missed={results_a['misses']}")
        log(f"  Agent B: recall={results_b['recall']:.0%} ({len(results_b['hits'])}/{expected_count}), "
            f"precision={results_b['precision']:.0%}, missed={results_b['misses']}")

        if results_a["false_positives"]:
            log(f"  Agent A false positives: {results_a['false_positives']}")
        if results_b["false_positives"]:
            log(f"  Agent B false positives: {results_b['false_positives']}")

        if save_transcripts:
            ts_dir = REPO_ROOT / "tests" / "experiment_transcripts"
            ts_dir.mkdir(exist_ok=True)
            (ts_dir / f"exp_a_trial_{trial_num}_agent_a.txt").write_text(
                f"=== PROMPT ===\n{PROMPT_A}\n\n=== STDOUT ===\n{stdout_a}\n\n=== STDERR ===\n{stderr_a}\n"
            )
            (ts_dir / f"exp_a_trial_{trial_num}_agent_b.txt").write_text(
                f"=== PROMPT ===\n{PROMPT_B}\n\n=== STDOUT ===\n{stdout_b}\n\n=== STDERR ===\n{stderr_b}\n"
            )
            log(f"\n  Transcripts saved to {ts_dir}/")

        return {
            "trial": trial_num,
            "expected_count": expected_count,
            "agent_a": {
                "recall": results_a["recall"],
                "precision": results_a["precision"],
                "perfect": results_a["perfect"],
                "hits": results_a["hits"],
                "misses": results_a["misses"],
                "false_positives": results_a["false_positives"],
                "elapsed": elapsed_a,
                "exit_code": rc_a,
            },
            "agent_b": {
                "recall": results_b["recall"],
                "precision": results_b["precision"],
                "perfect": results_b["perfect"],
                "hits": results_b["hits"],
                "misses": results_b["misses"],
                "false_positives": results_b["false_positives"],
                "elapsed": elapsed_b,
                "exit_code": rc_b,
            },
        }
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# ── Summary ──────────────────────────────────────────────────────────

def print_summary(results):
    expected_count = results[0]["expected_count"]
    n = len(results)

    log(f"\n{'='*70}")
    log(f"  EXPERIMENT A SUMMARY — {n} trial(s), {expected_count} expected blast radius files")
    log(f"{'='*70}\n")

    log(f"  {'Trial':>5}  {'A recall':>8}  {'B recall':>8}  {'A prec':>7}  {'B prec':>7}  {'A time':>8}  {'B time':>8}")
    log(f"  {'-'*5}  {'-'*8}  {'-'*8}  {'-'*7}  {'-'*7}  {'-'*8}  {'-'*8}")
    for r in results:
        a, b = r["agent_a"], r["agent_b"]
        log(f"  {r['trial']:>5}  {a['recall']:>7.0%}  {b['recall']:>7.0%}  "
            f"{a['precision']:>6.0%}  {b['precision']:>6.0%}  "
            f"{a['elapsed']:>7.1f}s  {b['elapsed']:>7.1f}s")

    a_recalls = [r["agent_a"]["recall"] for r in results]
    b_recalls = [r["agent_b"]["recall"] for r in results]
    a_times = [r["agent_a"]["elapsed"] for r in results]
    b_times = [r["agent_b"]["elapsed"] for r in results]
    a_perfect = sum(1 for r in results if r["agent_a"]["perfect"])
    b_perfect = sum(1 for r in results if r["agent_b"]["perfect"])

    log(f"\n  Perfect runs: Agent A = {a_perfect}/{n}, Agent B = {b_perfect}/{n}")
    log(f"  Avg recall:   Agent A = {sum(a_recalls)/n:.0%}, Agent B = {sum(b_recalls)/n:.0%}")
    log(f"  Avg time:     Agent A = {sum(a_times)/n:.1f}s, Agent B = {sum(b_times)/n:.1f}s")

    # Depth-bucketed misses
    a_miss_counts = {}
    b_miss_counts = {}
    for r in results:
        for f in r["agent_a"]["misses"]:
            a_miss_counts[f] = a_miss_counts.get(f, 0) + 1
        for f in r["agent_b"]["misses"]:
            b_miss_counts[f] = b_miss_counts.get(f, 0) + 1

    if a_miss_counts or b_miss_counts:
        all_missed = sorted(set(list(a_miss_counts.keys()) + list(b_miss_counts.keys())))
        for depth in (1, 2, 3):
            depth_set = DEPTH_GROUPS[depth]
            missed_at_depth = [f for f in all_missed if f in depth_set]
            if missed_at_depth:
                log(f"\n  Depth-{depth} files missed:")
                for f in missed_at_depth:
                    a_n = a_miss_counts.get(f, 0)
                    b_n = b_miss_counts.get(f, 0)
                    log(f"    {f}: Agent A = {a_n}/{n}, Agent B = {b_n}/{n}")

    log(f"\n  Verdict:")
    a_avg = sum(a_recalls) / n
    b_avg = sum(b_recalls) / n
    if b_avg > a_avg:
        log(f"  -> Agent B (with kb-graph) achieved {b_avg:.0%} avg recall vs Agent A's {a_avg:.0%}.")
    elif b_avg == a_avg:
        log(f"  -> Both agents achieved equal recall ({a_avg:.0%}).")
    else:
        log(f"  -> Agent A outperformed Agent B — unexpected result.")

    return {
        "trials": n,
        "expected_count": expected_count,
        "agent_a_avg_recall": sum(a_recalls) / n,
        "agent_b_avg_recall": sum(b_recalls) / n,
        "agent_a_perfect": a_perfect,
        "agent_b_perfect": b_perfect,
    }


# ── Main ─────────────────────────────────────────────────────────────

def main():
    global _log_file

    parser = argparse.ArgumentParser(description="Phase 5 v4 — Experiment A: Doc-Graph Impact Analysis")
    parser.add_argument("--trials", type=int, default=1, help="Number of A/B trials")
    parser.add_argument("--model", type=str, default=None, help="Model name (e.g., sonnet)")
    parser.add_argument("--save-transcripts", action="store_true", help="Save agent stdout/stderr")
    parser.add_argument("--timeout", type=int, default=300, help="Agent timeout in seconds")
    parser.add_argument("--dry-run", action="store_true", help="Validate fixture without running agents")
    parser.add_argument("--clean", action="store_true", help="Remove previous results before running")
    args = parser.parse_args()

    log_path = REPO_ROOT / "tests" / "experiment_a.log"
    _log_file = open(log_path, "w")

    try:
        log(f"Phase 5 v4 — Experiment A: Doc-Graph Impact Analysis")
        log(f"Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        log(f"Claude CLI: {get_claude_version()}")
        log(f"Model: {args.model or 'default'}")
        log(f"Trials: {args.trials}")
        log(f"Timeout: {args.timeout}s")
        log(f"Target: {TARGET}")
        log(f"Expected blast radius: {len(EXPECTED_BLAST_RADIUS)} files")
        log("")

        if args.dry_run:
            dry_run()
            return

        if args.clean:
            ts_dir = REPO_ROOT / "tests" / "experiment_transcripts"
            if ts_dir.exists():
                for f in ts_dir.glob("exp_a_*"):
                    f.unlink()
                log("Cleaned previous Experiment A transcripts.")

        check_prerequisites()

        results = []
        for i in range(1, args.trials + 1):
            result = run_trial(
                i, model=args.model, save_transcripts=args.save_transcripts,
                timeout=args.timeout,
            )
            results.append(result)

        summary = print_summary(results)

        # Save results JSON
        results_path = REPO_ROOT / "tests" / "experiment_a_results.json"
        with open(results_path, "w") as f:
            json.dump({"summary": summary, "trials": results}, f, indent=2)
        log(f"\nResults saved to {results_path}")

    finally:
        if _log_file:
            _log_file.close()
            _log_file = None


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Validate fixture with dry-run**

Run: `python3 tests/test_experiment_a.py --dry-run`
Expected: "PASS: Ground truth matches traverse output exactly." with 13 blast radius files found.

**IMPORTANT — wiki-link resolution**: `kb_graph.py`'s `resolve_wikilink()` matches by stem (filename without extension). `[[02-processing]]` will NOT resolve to `docs/design/02-processing-engine.md` because stems don't match (`02-processing` ≠ `02-processing-engine`). The fixture content MUST use `[[02-processing-engine]]` as the wiki-link text. The same applies to all other wiki-links — the link text must match the target file's stem exactly. Before the dry-run, verify every wiki-link in `FIXTURE_FILES` against the actual filenames. Fix any mismatches in the fixture content strings.

- [ ] **Step 3: Commit**

```bash
git add tests/test_experiment_a.py
git commit -m "feat: Experiment A — doc-graph impact analysis script with fixture"
```

---

## Task 4: Build Experiment B — Code Intelligence Signature Change

**Files:**
- Create: `tests/test_experiment_b.py`

This experiment tests whether function signatures in KB_INDEX.md help agents apply a breaking parameter change. Requires Task 1+2 (exports in KB_INDEX.md) to be complete first.

- [ ] **Step 1: Create the experiment script with fixture data**

Create `tests/test_experiment_b.py`. The fixture defines ~80 files for a fictional Python data pipeline library. The scoring logic checks actual code substitutions, not just markers.

```python
#!/usr/bin/env python3
"""Phase 5 v4 — Experiment B: Code Intelligence — Function-Level Knowledge

Tests whether function signatures in KB_INDEX.md help a Claude agent
find and fix a breaking parameter change. The fixture is a Python data
pipeline library. The target function apply_transform() has its
`strict: bool` parameter replaced by `mode: str`.

Target: src/core/transform.py — apply_transform() signature change
Expected: 6 call sites across 5 files need updating.

Requirements:
    - Claude Code CLI (`claude` command on PATH)
    - API access configured (ANTHROPIC_API_KEY or OAuth)
    - kb-graph installed (`kb-graph` on PATH)

Usage:
    python3 tests/test_experiment_b.py                  # 1 trial
    python3 tests/test_experiment_b.py --trials 3       # 3 trials
    python3 tests/test_experiment_b.py --model sonnet   # use sonnet
    python3 tests/test_experiment_b.py --save-transcripts
    python3 tests/test_experiment_b.py --dry-run        # validate fixture only
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
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# ── Logging ──────────────────────────────────────────────────────────────

_log_file = None


def log(msg=""):
    print(msg)
    if _log_file is not None:
        _log_file.write(msg + "\n")
        _log_file.flush()


def get_claude_version():
    try:
        result = subprocess.run(
            ["claude", "--version"], capture_output=True, text=True, timeout=10,
        )
        return result.stdout.strip() or result.stderr.strip() or "unknown"
    except Exception:
        return "unknown"


# ── Fixture Files ────────────────────────────────────────────────────────

FIXTURE_FILES = {
    # ── TARGET ───────────────────────────────────────────────────────
    "src/core/transform.py": '''\
"""Data transformation utilities for the pipeline."""


class TransformConfig:
    """Configuration for data transformations."""

    def __init__(self, steps=None, validate=True):
        self.steps = steps or []
        self.validate = validate


def apply_transform(data, config, strict=True):
    """Apply a sequence of transformations to the data.

    Args:
        data: Input DataFrame.
        config: TransformConfig with transformation steps.
        strict: If True, raise on validation errors. If False, skip invalid rows.

    Returns:
        Transformed DataFrame.
    """
    if config.validate and strict:
        _validate(data, config)
    for step in config.steps:
        data = step(data)
    return data


def validate_schema(data, schema):
    """Validate data against a schema definition.

    Args:
        data: Input DataFrame.
        schema: Dict mapping column names to expected types.

    Returns:
        True if valid, False otherwise.
    """
    return True  # stub


def _validate(data, config):
    """Internal validation helper."""
    pass


def _apply_single_step(data, step):
    """Internal step application."""
    return step(data)
''',

    # ── CORE MODULES ─────────────────────────────────────────────────

    "src/core/__init__.py": '''\
"""Core package — re-exports key symbols."""
from .transform import TransformConfig, apply_transform, validate_schema
from .config import PipelineConfig
from .logging import get_logger

__all__ = [
    "TransformConfig", "apply_transform", "validate_schema",
    "PipelineConfig", "get_logger",
]
''',

    "src/core/config.py": '''\
"""Pipeline configuration."""


class PipelineConfig:
    """Global pipeline settings."""

    def __init__(self, parallelism=4, retry_count=3, log_level="INFO"):
        self.parallelism = parallelism
        self.retry_count = retry_count
        self.log_level = log_level
''',

    "src/core/logging.py": '''\
"""Logging utilities."""


class Logger:
    def __init__(self, name):
        self.name = name

    def info(self, msg):
        print(f"[INFO] {self.name}: {msg}")

    def error(self, msg):
        print(f"[ERROR] {self.name}: {msg}")


def get_logger(name):
    return Logger(name)
''',

    "src/core/exceptions.py": '''\
"""Custom exceptions."""


class PipelineError(Exception):
    pass


class ValidationError(PipelineError):
    pass


class TransformError(PipelineError):
    pass
''',

    # ── PREPROCESSING ────────────────────────────────────────────────

    "src/preprocessing/__init__.py": '''\
"""Preprocessing package."""
from .normalize import normalize_data
from .clean import clean_data
''',

    "src/preprocessing/normalize.py": '''\
"""Data normalization."""
from core.transform import apply_transform, TransformConfig
from core.logging import get_logger

logger = get_logger(__name__)


def normalize_data(data, config=None):
    """Normalize data using standard transformations."""
    if config is None:
        config = TransformConfig(steps=[_scale, _center])
    logger.info("Normalizing data")
    return apply_transform(data, config, strict=True)


def _scale(data):
    return data


def _center(data):
    return data
''',

    "src/preprocessing/clean.py": '''\
"""Data cleaning."""
from core.transform import validate_schema
from core.logging import get_logger

logger = get_logger(__name__)

STANDARD_SCHEMA = {"id": "int", "value": "float", "label": "str"}


def clean_data(data, schema=None):
    """Clean and validate incoming data."""
    if schema is None:
        schema = STANDARD_SCHEMA
    logger.info("Cleaning data")
    if not validate_schema(data, schema):
        logger.error("Schema validation failed")
        return None
    return data
''',

    "src/preprocessing/filter.py": '''\
"""Data filtering."""
from core.transform import apply_transform, TransformConfig
from core.logging import get_logger

logger = get_logger(__name__)


def filter_data(data, predicates):
    """Filter data by applying predicate functions."""
    config = TransformConfig(steps=predicates)
    logger.info(f"Filtering with {len(predicates)} predicates")
    return apply_transform(data, config)
''',

    "src/preprocessing/batch.py": '''\
"""Batch preprocessing."""
from preprocessing.normalize import normalize_data
from core.logging import get_logger

logger = get_logger(__name__)


def process_batch(batch, config=None):
    """Process a batch of records through normalization."""
    logger.info(f"Processing batch of {len(batch)} records")
    return [normalize_data(record, config) for record in batch]
''',

    # ── ANALYSIS ─────────────────────────────────────────────────────

    "src/analysis/__init__.py": '''\
"""Analysis package."""
from .aggregate import aggregate_data
''',

    "src/analysis/aggregate.py": '''\
"""Data aggregation."""
from core.transform import apply_transform, TransformConfig
from core.logging import get_logger

logger = get_logger(__name__)


def aggregate_data(data, group_by, metrics):
    """Aggregate data with lenient validation (skip bad rows)."""
    config = TransformConfig(steps=[_group, _compute_metrics])
    logger.info(f"Aggregating by {group_by}")
    return apply_transform(data, config, strict=False)


def _group(data):
    return data


def _compute_metrics(data):
    return data
''',

    "src/analysis/correlate.py": '''\
"""Correlation analysis."""
from core.transform import validate_schema
from core.logging import get_logger

logger = get_logger(__name__)

CORRELATION_SCHEMA = {"feature_a": "float", "feature_b": "float"}


def compute_correlation(data):
    """Compute pairwise correlations."""
    if not validate_schema(data, CORRELATION_SCHEMA):
        logger.error("Invalid schema for correlation")
        return None
    return {"pearson": 0.85, "spearman": 0.82}
''',

    "src/analysis/cluster.py": '''\
"""Clustering analysis."""
from analysis.aggregate import aggregate_data
from core.logging import get_logger

logger = get_logger(__name__)


def cluster_data(data, n_clusters=5):
    """Cluster data after aggregation."""
    aggregated = aggregate_data(data, "cluster_id", ["mean", "std"])
    logger.info(f"Clustering into {n_clusters} groups")
    return aggregated
''',

    "src/analysis/report.py": '''\
"""Report generation."""
from analysis.cluster import cluster_data
from core.logging import get_logger

logger = get_logger(__name__)


def generate_report(data, output_path):
    """Generate an analysis report."""
    clusters = cluster_data(data)
    logger.info(f"Writing report to {output_path}")
    return {"clusters": clusters, "path": output_path}
''',

    # ── PIPELINE ─────────────────────────────────────────────────────

    "src/pipeline/__init__.py": '''\
"""Pipeline package."""
from .run import run_pipeline
''',

    "src/pipeline/run.py": '''\
"""Pipeline orchestration."""
from core.transform import apply_transform, validate_schema, TransformConfig
from core.config import PipelineConfig
from core.logging import get_logger

logger = get_logger(__name__)


def run_pipeline(data, pipeline_config=None):
    """Run the full data pipeline."""
    if pipeline_config is None:
        pipeline_config = PipelineConfig()

    logger.info("Starting pipeline")

    # Validate input
    schema = {"id": "int", "value": "float"}
    if not validate_schema(data, schema):
        logger.error("Input validation failed")
        return None

    # Transform with strict validation
    cfg = TransformConfig(steps=[_enrich, _deduplicate])
    result = apply_transform(data, cfg, strict=True)

    logger.info("Pipeline complete")
    return result


def _enrich(data):
    return data


def _deduplicate(data):
    return data
''',

    "src/pipeline/schedule.py": '''\
"""Pipeline scheduling."""
from pipeline.run import run_pipeline
from core.logging import get_logger

logger = get_logger(__name__)


def schedule_pipeline(data, cron_expr):
    """Schedule a pipeline run."""
    logger.info(f"Scheduling pipeline: {cron_expr}")
    return run_pipeline(data)
''',

    "src/pipeline/monitor.py": '''\
"""Pipeline monitoring."""
from core.logging import get_logger

logger = get_logger(__name__)


def check_health():
    """Check pipeline health status."""
    logger.info("Health check OK")
    return {"status": "healthy", "uptime": 3600}
''',

    # ── IO ───────────────────────────────────────────────────────────

    "src/io/__init__.py": '''\
"""IO package."""
from .readers import read_csv
from .writers import write_csv
''',

    "src/io/readers.py": '''\
"""Data readers."""
from core.logging import get_logger

logger = get_logger(__name__)


def read_csv(path):
    """Read data from a CSV file."""
    logger.info(f"Reading {path}")
    return []
''',

    "src/io/writers.py": '''\
"""Data writers."""
from core.transform import validate_schema
from core.logging import get_logger

logger = get_logger(__name__)


def write_csv(data, path, schema=None):
    """Write data to a CSV file with optional schema validation."""
    if schema and not validate_schema(data, schema):
        logger.error("Output schema validation failed")
        return False
    logger.info(f"Writing to {path}")
    return True
''',

    "src/io/formats.py": '''\
"""Format detection utilities."""


def detect_format(path):
    """Detect file format from extension."""
    if path.endswith(".csv"):
        return "csv"
    elif path.endswith(".parquet"):
        return "parquet"
    elif path.endswith(".json"):
        return "json"
    return "unknown"
''',

    # ── PLOTTING ─────────────────────────────────────────────────────

    "src/plotting/__init__.py": '''\
"""Plotting package."""
from .charts import plot_histogram
''',

    "src/plotting/charts.py": '''\
"""Chart generation."""
from analysis.aggregate import aggregate_data
from core.logging import get_logger

logger = get_logger(__name__)


def plot_histogram(data, column, bins=20):
    """Generate a histogram for a data column."""
    agg = aggregate_data(data, column, ["count"])
    logger.info(f"Plotting histogram for {column}")
    return {"type": "histogram", "data": agg, "bins": bins}
''',

    "src/plotting/export.py": '''\
"""Plot export utilities."""
from core.logging import get_logger

logger = get_logger(__name__)


def export_png(chart, path):
    """Export a chart to PNG."""
    logger.info(f"Exporting chart to {path}")
    return True
''',

    # ── TESTS ────────────────────────────────────────────────────────

    "tests/__init__.py": "",

    "tests/test_transform.py": '''\
"""Tests for core transform functions."""
import unittest
from core.transform import apply_transform, validate_schema, TransformConfig


class TestApplyTransform(unittest.TestCase):
    def test_strict_mode(self):
        config = TransformConfig(steps=[lambda x: x])
        result = apply_transform([], config, strict=True)
        self.assertEqual(result, [])

    def test_lenient_mode(self):
        config = TransformConfig(steps=[lambda x: x])
        result = apply_transform([], config, strict=False)
        self.assertEqual(result, [])

    def test_default_strict(self):
        config = TransformConfig(steps=[])
        result = apply_transform([], config)
        self.assertEqual(result, [])


class TestValidateSchema(unittest.TestCase):
    def test_valid_schema(self):
        self.assertTrue(validate_schema([], {"id": "int"}))


if __name__ == "__main__":
    unittest.main()
''',

    "tests/test_normalize.py": '''\
"""Tests for normalization."""
import unittest


class TestNormalize(unittest.TestCase):
    def test_placeholder(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
''',

    "tests/test_aggregate.py": '''\
"""Tests for aggregation."""
import unittest


class TestAggregate(unittest.TestCase):
    def test_placeholder(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
''',

    "tests/test_pipeline.py": '''\
"""Tests for the pipeline runner."""
import unittest
from core.transform import apply_transform, TransformConfig


class TestPipeline(unittest.TestCase):
    def test_pipeline_transform(self):
        config = TransformConfig(steps=[])
        data = [1, 2, 3]
        result = apply_transform(data, config, strict=False)
        self.assertEqual(result, [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
''',

    "tests/test_writers.py": '''\
"""Tests for data writers."""
import unittest


class TestWriters(unittest.TestCase):
    def test_placeholder(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
''',

    "tests/test_clean.py": '''\
"""Tests for data cleaning."""
import unittest


class TestClean(unittest.TestCase):
    def test_placeholder(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
''',

    "tests/test_filter.py": '''\
"""Tests for data filtering."""
import unittest


class TestFilter(unittest.TestCase):
    def test_placeholder(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
''',

    "tests/test_correlate.py": '''\
"""Tests for correlation analysis."""
import unittest


class TestCorrelate(unittest.TestCase):
    def test_placeholder(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
''',

    "tests/conftest.py": '''\
"""Shared test fixtures."""

# Sample transform configuration for tests
SAMPLE_TRANSFORM_CONFIG = {
    "steps": ["scale", "center", "normalize"],
    "strict": True,
    "timeout": 30,
}


def make_test_data(n=100):
    """Generate test data records."""
    return [{"id": i, "value": float(i)} for i in range(n)]
''',

    # ── CONFIG FILES ─────────────────────────────────────────────────

    "configs/pipeline.yaml": '''\
# Pipeline configuration
parallelism: 8
retry_count: 3
pipeline_runner: "src/pipeline/run.py"
log_level: INFO
''',

    "configs/defaults.yaml": '''\
# Default settings
config_module: "src/core/config.py"
batch_size: 1000
max_memory_mb: 4096
''',

    "configs/test_config.yaml": '''\
# Test environment settings
transform_mode: strict
debug: true
test_data_path: data/test_fixtures/
''',

    # ── DOCS ─────────────────────────────────────────────────────────

    "docs/architecture.md": """\
# Architecture

System architecture for the data pipeline library.

## Core Modules

The [[transform.py]] module provides the central transformation
engine. The [[run.py]] module orchestrates pipeline execution.

## Design Principles

- Strict validation by default
- Pluggable transformation steps
- Schema-driven I/O
""",

    "docs/api-reference.md": """\
# API Reference

## Core

### apply_transform

See [[transform.py]] for the full signature.

Transforms data through a sequence of steps defined in a
TransformConfig. Supports strict and lenient validation modes.
""",

    "docs/tutorial.md": """\
# Tutorial

Learn how to use the data pipeline library.

## Quick Start

Import and call `apply_transform` with your data:

```python
from core.transform import apply_transform, TransformConfig

config = TransformConfig(steps=[my_step])
result = apply_transform(data, config, strict=True)
```

The `strict` parameter controls validation behavior.
""",

    "docs/contributing.md": """\
# Contributing

## Development Setup

1. Clone the repo
2. Create a virtual environment
3. Install dependencies: `pip install -e .`

## Code Style

Follow PEP 8. Use type annotations for public functions.
""",

    # ── SCRIPTS ──────────────────────────────────────────────────────

    "scripts/run_pipeline.sh": """\
#!/usr/bin/env bash
set -euo pipefail
echo "Running pipeline..."
python3 -m pipeline.run
""",

    "scripts/setup_env.sh": """\
#!/usr/bin/env bash
echo "Setting up environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
""",

    "scripts/benchmark.py": '''\
"""Benchmark script."""
# TODO: benchmark apply_transform performance
# This should test various batch sizes and step counts

import time


def run_benchmark():
    """Placeholder benchmark."""
    start = time.time()
    # Benchmark code here
    elapsed = time.time() - start
    print(f"Benchmark completed in {elapsed:.2f}s")


if __name__ == "__main__":
    run_benchmark()
''',

    # ── ROOT FILES ───────────────────────────────────────────────────

    "README.md": """\
# Data Pipeline Library

A composable data transformation and pipeline library.

## Quick Start

```python
from core.transform import apply_transform, TransformConfig

config = TransformConfig(steps=[my_step])
result = apply_transform(data, config)
```
""",

    ".phoamignore": """\
.venv/
__pycache__/
*.pyc
""",

    "pyproject.toml": """\
[project]
name = "data-pipeline"
version = "0.1.0"
requires-python = ">=3.10"
""",
}

# ── Ground Truth: Call Sites Requiring Changes ───────────────────────

TARGET = "src/core/transform.py"

# Each entry: (file, line_pattern_before, line_pattern_after)
# line_pattern_before: regex matching the line BEFORE the fix
# line_pattern_after: regex matching the line AFTER the correct fix
EXPECTED_FIXES = [
    {
        "file": "src/preprocessing/normalize.py",
        "before": r"apply_transform\(data,\s*config,\s*strict\s*=\s*True\)",
        "after": r'apply_transform\(data,\s*config,\s*mode\s*=\s*"strict"\)',
        "description": "normalize_data() calls apply_transform with strict=True",
    },
    {
        "file": "src/analysis/aggregate.py",
        "before": r"apply_transform\(data,\s*config,\s*strict\s*=\s*False\)",
        "after": r'apply_transform\(data,\s*config,\s*mode\s*=\s*"lenient"\)',
        "description": "aggregate_data() calls apply_transform with strict=False",
    },
    {
        "file": "src/pipeline/run.py",
        "before": r"apply_transform\(data,\s*cfg,\s*strict\s*=\s*True\)",
        "after": r'apply_transform\(data,\s*cfg,\s*mode\s*=\s*"strict"\)',
        "description": "run_pipeline() calls apply_transform with strict=True",
    },
    {
        "file": "tests/test_transform.py",
        "before": r"apply_transform\(\[\],\s*config,\s*strict\s*=\s*True\)",
        "after": r'apply_transform\(\[\],\s*config,\s*mode\s*=\s*"strict"\)',
        "description": "test_strict_mode() calls apply_transform with strict=True",
    },
    {
        "file": "tests/test_transform.py",
        "before": r"apply_transform\(\[\],\s*config,\s*strict\s*=\s*False\)",
        "after": r'apply_transform\(\[\],\s*config,\s*mode\s*=\s*"lenient"\)',
        "description": "test_lenient_mode() calls apply_transform with strict=False",
    },
    {
        "file": "tests/test_pipeline.py",
        "before": r"apply_transform\(data,\s*config,\s*strict\s*=\s*False\)",
        "after": r'apply_transform\(data,\s*config,\s*mode\s*=\s*"lenient"\)',
        "description": "test_pipeline_transform() calls apply_transform with strict=False",
    },
]

# Files that should NOT be modified (call apply_transform with defaults only,
# or call validate_schema, or don't call apply_transform at all)
SHOULD_NOT_MODIFY = [
    "src/core/transform.py",         # target — must not be changed
    "src/preprocessing/filter.py",   # calls apply_transform() without strict arg
    "src/preprocessing/clean.py",    # calls validate_schema, not apply_transform
    "src/analysis/correlate.py",     # calls validate_schema, not apply_transform
    "src/io/writers.py",             # calls validate_schema, not apply_transform
    "tests/conftest.py",             # mentions "strict" in dict, not a call site
    "docs/tutorial.md",              # mentions apply_transform in prose
    "scripts/benchmark.py",          # mentions apply_transform in comment
]

RED_HERRING_FILES = [
    "tests/conftest.py",             # SAMPLE_TRANSFORM_CONFIG has "strict": True
    "docs/tutorial.md",              # prose mentions apply_transform with strict=True
    "scripts/benchmark.py",          # comment mentions apply_transform
    "configs/test_config.yaml",      # has transform_mode: strict
]


# ── Agent Prompts ────────────────────────────────────────────────────

PROMPT_A = (
    "The function `apply_transform()` in `src/core/transform.py` has a "
    "breaking parameter change: `strict: bool = True` is now "
    '`mode: str = "strict"`. Update every call site in the project: '
    '`strict=True` becomes `mode="strict"`, `strict=False` becomes '
    '`mode="lenient"`. Call sites using the default (not passing '
    "`strict`) need no change. Do not modify `src/core/transform.py` "
    "itself. Do not explain, just make the changes."
)

PROMPT_B = (
    "Read CLAUDE.md first, then read KB_INDEX.md. The function "
    "`apply_transform()` in `src/core/transform.py` has a breaking "
    "parameter change: `strict: bool = True` is now "
    '`mode: str = "strict"`. KB_INDEX.md lists every file that imports '
    "transform.py — check those files for call sites. Update every call "
    'site: `strict=True` becomes `mode="strict"`, `strict=False` becomes '
    '`mode="lenient"`. Call sites using the default (not passing '
    "`strict`) need no change. Do not modify `src/core/transform.py` "
    "itself. Do not explain, just make the changes."
)


# ── Helpers ──────────────────────────────────────────────────────────

def check_prerequisites():
    missing = []
    for cmd in ("claude", "kb-graph"):
        if shutil.which(cmd) is None:
            missing.append(cmd)
    if missing:
        log(f"ERROR: Missing prerequisites: {', '.join(missing)}")
        sys.exit(1)


def create_fixture(dest):
    for rel_path, content in FIXTURE_FILES.items():
        filepath = Path(dest) / rel_path
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)


def init_graph(project_dir):
    subprocess.run(
        ["git", "init", "-q"], cwd=project_dir, capture_output=True,
    )
    subprocess.run(
        ["git", "add", "."], cwd=project_dir, capture_output=True,
    )
    subprocess.run(
        ["git", "commit", "-q", "-m", "initial", "--no-gpg-sign"],
        cwd=project_dir, capture_output=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "test@test",
             "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "test@test"},
    )
    result = subprocess.run(
        ["kb-graph", "init", "."], cwd=project_dir,
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        log(f"WARNING: kb-graph init failed:\n{result.stderr}")
    return result.returncode == 0


def run_agent(project_dir, prompt, *, model=None, timeout=300):
    cmd = [
        "claude", "-p", prompt,
        "--dangerously-skip-permissions", "--no-session-persistence",
    ]
    if model:
        cmd.extend(["--model", model])

    start = time.monotonic()
    try:
        result = subprocess.run(
            cmd, cwd=project_dir, capture_output=True, text=True,
            timeout=timeout,
            env={**os.environ, "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"},
        )
        elapsed = time.monotonic() - start
        return result.stdout, result.stderr, result.returncode, elapsed
    except subprocess.TimeoutExpired:
        elapsed = time.monotonic() - start
        return "", f"TIMEOUT after {timeout}s", -1, elapsed


def score_fixes(project_dir):
    """Score the agent's code changes against expected fixes.

    Returns dict with correct_fixes, missed_fixes, wrong_fixes,
    false_positives, recall, precision.
    """
    correct = []
    missed = []
    wrong = []

    for fix in EXPECTED_FIXES:
        filepath = Path(project_dir) / fix["file"]
        try:
            content = filepath.read_text()
        except (FileNotFoundError, UnicodeDecodeError):
            missed.append(fix)
            continue

        has_before = re.search(fix["before"], content)
        has_after = re.search(fix["after"], content)

        if has_after and not has_before:
            correct.append(fix)
        elif has_before and not has_after:
            missed.append(fix)
        elif has_before and has_after:
            # Both patterns present — partial fix or duplicate
            missed.append(fix)
        else:
            # Neither pattern — file was modified in an unexpected way
            wrong.append(fix)

    # Check for false positives: files that should NOT have been modified
    false_positives = []
    for rel_path in SHOULD_NOT_MODIFY:
        filepath = Path(project_dir) / rel_path
        if not filepath.exists():
            continue
        try:
            content = filepath.read_text()
        except UnicodeDecodeError:
            continue
        # Check if the file was changed (look for mode= where strict= was)
        if re.search(r'mode\s*=\s*"(strict|lenient)"', content):
            # Exception: if this file is also in EXPECTED_FIXES, it's expected
            if rel_path not in [f["file"] for f in EXPECTED_FIXES]:
                false_positives.append(rel_path)

    total_needed = len(EXPECTED_FIXES)
    n_correct = len(correct)
    n_all_changes = n_correct + len(wrong) + len(false_positives)
    recall = n_correct / total_needed if total_needed else 1.0
    precision = n_correct / n_all_changes if n_all_changes else 0.0

    return {
        "correct": [f["description"] for f in correct],
        "missed": [f["description"] for f in missed],
        "wrong": [f["description"] for f in wrong],
        "false_positives": false_positives,
        "recall": recall,
        "precision": precision,
        "perfect": n_correct == total_needed and not wrong and not false_positives,
    }


# ── Dry Run ──────────────────────────────────────────────────────────

def dry_run():
    log("DRY RUN: Validating fixture and ground truth...\n")

    tmpdir = tempfile.mkdtemp(prefix="kb_exp_b_dry_")
    try:
        create_fixture(tmpdir)

        # Verify all expected fix files exist
        for fix in EXPECTED_FIXES:
            fp = Path(tmpdir) / fix["file"]
            assert fp.exists(), f"Expected fix file missing: {fix['file']}"
            content = fp.read_text()
            assert re.search(fix["before"], content), (
                f"Before pattern not found in {fix['file']}: {fix['before']}"
            )
        log(f"  {len(EXPECTED_FIXES)} call sites verified in fixture")

        # Verify red herring files exist
        for rel_path in RED_HERRING_FILES:
            assert (Path(tmpdir) / rel_path).exists(), f"Red herring missing: {rel_path}"
        log(f"  {len(RED_HERRING_FILES)} red herring files verified")

        # Init graph and verify KB_INDEX.md has exports
        log("\n  Running kb-graph init...")
        if not init_graph(tmpdir):
            log("  WARNING: kb-graph init had issues")

        kb_index = Path(tmpdir) / "KB_INDEX.md"
        if kb_index.exists():
            content = kb_index.read_text()
            if "exports:" in content:
                log("  KB_INDEX.md contains exports — enhanced format working")
                if "apply_transform" in content:
                    log("  KB_INDEX.md lists apply_transform signature")
                else:
                    log("  WARNING: apply_transform not found in KB_INDEX.md exports")
            else:
                log("  WARNING: KB_INDEX.md does NOT contain exports lines")
                log("  Experiment B requires Task 1+2 (extract_exports) to be implemented first")
        else:
            log("  WARNING: KB_INDEX.md not generated")

        # Total file count
        total = sum(1 for _ in Path(tmpdir).rglob("*") if _.is_file()
                    and not any(p.startswith(".") for p in _.relative_to(tmpdir).parts))
        log(f"\n  Total fixture files: {total}")
        log(f"  Call sites to fix: {len(EXPECTED_FIXES)}")
        log(f"  Files with fixes: {len(set(f['file'] for f in EXPECTED_FIXES))}")

        log("\n  PASS: Fixture validated.")

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# ── Trial Runner ─────────────────────────────────────────────────────

def run_trial(trial_num, *, model=None, save_transcripts=False, timeout=300):
    log(f"\n{'='*60}")
    log(f"  Trial {trial_num}")
    log(f"{'='*60}")

    tmpdir = tempfile.mkdtemp(prefix=f"kb_exp_b_{trial_num}_")
    dir_a = os.path.join(tmpdir, "project_a")
    dir_b = os.path.join(tmpdir, "project_b")

    try:
        log(f"  Setting up projects in {tmpdir}")
        os.makedirs(dir_a)
        os.makedirs(dir_b)
        create_fixture(dir_a)
        create_fixture(dir_b)

        # Init graph on project B only
        log("  Running kb-graph init on project B...")
        if not init_graph(dir_b):
            log("  WARNING: kb-graph init had issues")

        has_index = (Path(dir_b) / "KB_INDEX.md").exists()
        has_claude_md = (Path(dir_b) / "CLAUDE.md").exists()
        log(f"  Project B: KB_INDEX.md={has_index}, CLAUDE.md={has_claude_md}")

        # Run agents
        log(f"\n  Running Agent A (no graph)...")
        stdout_a, stderr_a, rc_a, elapsed_a = run_agent(
            dir_a, PROMPT_A, model=model, timeout=timeout
        )
        log(f"  Agent A finished in {elapsed_a:.1f}s (exit={rc_a})")

        log(f"  Running Agent B (with graph)...")
        stdout_b, stderr_b, rc_b, elapsed_b = run_agent(
            dir_b, PROMPT_B, model=model, timeout=timeout
        )
        log(f"  Agent B finished in {elapsed_b:.1f}s (exit={rc_b})")

        # Score
        results_a = score_fixes(dir_a)
        results_b = score_fixes(dir_b)

        n_fixes = len(EXPECTED_FIXES)
        log(f"\n  Results:")
        log(f"  Agent A: recall={results_a['recall']:.0%} ({len(results_a['correct'])}/{n_fixes}), "
            f"precision={results_a['precision']:.0%}")
        log(f"    correct: {results_a['correct']}")
        log(f"    missed:  {results_a['missed']}")
        log(f"    wrong:   {results_a['wrong']}")
        log(f"    false+:  {results_a['false_positives']}")

        log(f"  Agent B: recall={results_b['recall']:.0%} ({len(results_b['correct'])}/{n_fixes}), "
            f"precision={results_b['precision']:.0%}")
        log(f"    correct: {results_b['correct']}")
        log(f"    missed:  {results_b['missed']}")
        log(f"    wrong:   {results_b['wrong']}")
        log(f"    false+:  {results_b['false_positives']}")

        if save_transcripts:
            ts_dir = REPO_ROOT / "tests" / "experiment_transcripts"
            ts_dir.mkdir(exist_ok=True)
            (ts_dir / f"exp_b_trial_{trial_num}_agent_a.txt").write_text(
                f"=== PROMPT ===\n{PROMPT_A}\n\n=== STDOUT ===\n{stdout_a}\n\n=== STDERR ===\n{stderr_a}\n"
            )
            (ts_dir / f"exp_b_trial_{trial_num}_agent_b.txt").write_text(
                f"=== PROMPT ===\n{PROMPT_B}\n\n=== STDOUT ===\n{stdout_b}\n\n=== STDERR ===\n{stderr_b}\n"
            )
            log(f"\n  Transcripts saved to {ts_dir}/")

        return {
            "trial": trial_num,
            "total_fixes": n_fixes,
            "agent_a": {**results_a, "elapsed": elapsed_a, "exit_code": rc_a},
            "agent_b": {**results_b, "elapsed": elapsed_b, "exit_code": rc_b},
        }
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# ── Summary ──────────────────────────────────────────────────────────

def print_summary(results):
    n_fixes = results[0]["total_fixes"]
    n = len(results)

    log(f"\n{'='*70}")
    log(f"  EXPERIMENT B SUMMARY — {n} trial(s), {n_fixes} call sites to fix")
    log(f"{'='*70}\n")

    log(f"  {'Trial':>5}  {'A recall':>8}  {'B recall':>8}  {'A prec':>7}  {'B prec':>7}  {'A time':>8}  {'B time':>8}")
    log(f"  {'-'*5}  {'-'*8}  {'-'*8}  {'-'*7}  {'-'*7}  {'-'*8}  {'-'*8}")
    for r in results:
        a, b = r["agent_a"], r["agent_b"]
        log(f"  {r['trial']:>5}  {a['recall']:>7.0%}  {b['recall']:>7.0%}  "
            f"{a['precision']:>6.0%}  {b['precision']:>6.0%}  "
            f"{a['elapsed']:>7.1f}s  {b['elapsed']:>7.1f}s")

    a_recalls = [r["agent_a"]["recall"] for r in results]
    b_recalls = [r["agent_b"]["recall"] for r in results]
    a_perfect = sum(1 for r in results if r["agent_a"]["perfect"])
    b_perfect = sum(1 for r in results if r["agent_b"]["perfect"])

    log(f"\n  Perfect runs: Agent A = {a_perfect}/{n}, Agent B = {b_perfect}/{n}")
    log(f"  Avg recall:   Agent A = {sum(a_recalls)/n:.0%}, Agent B = {sum(b_recalls)/n:.0%}")

    log(f"\n  Verdict:")
    a_avg = sum(a_recalls) / n
    b_avg = sum(b_recalls) / n
    if b_avg > a_avg:
        log(f"  -> Agent B (with kb-graph) achieved {b_avg:.0%} avg recall vs Agent A's {a_avg:.0%}.")
    elif b_avg == a_avg:
        log(f"  -> Both agents achieved equal recall ({a_avg:.0%}).")
    else:
        log(f"  -> Agent A outperformed Agent B — unexpected result.")

    return {
        "trials": n,
        "total_fixes": n_fixes,
        "agent_a_avg_recall": sum(a_recalls) / n,
        "agent_b_avg_recall": sum(b_recalls) / n,
        "agent_a_perfect": a_perfect,
        "agent_b_perfect": b_perfect,
    }


# ── Main ─────────────────────────────────────────────────────────────

def main():
    global _log_file

    parser = argparse.ArgumentParser(description="Phase 5 v4 — Experiment B: Code Intelligence")
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--save-transcripts", action="store_true")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()

    log_path = REPO_ROOT / "tests" / "experiment_b.log"
    _log_file = open(log_path, "w")

    try:
        log(f"Phase 5 v4 — Experiment B: Code Intelligence")
        log(f"Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        log(f"Claude CLI: {get_claude_version()}")
        log(f"Model: {args.model or 'default'}")
        log(f"Trials: {args.trials}")
        log(f"Timeout: {args.timeout}s")
        log(f"Target: {TARGET}")
        log(f"Expected fixes: {len(EXPECTED_FIXES)}")
        log("")

        if args.dry_run:
            dry_run()
            return

        if args.clean:
            ts_dir = REPO_ROOT / "tests" / "experiment_transcripts"
            if ts_dir.exists():
                for f in ts_dir.glob("exp_b_*"):
                    f.unlink()
                log("Cleaned previous Experiment B transcripts.")

        check_prerequisites()

        results = []
        for i in range(1, args.trials + 1):
            result = run_trial(
                i, model=args.model, save_transcripts=args.save_transcripts,
                timeout=args.timeout,
            )
            results.append(result)

        summary = print_summary(results)

        results_path = REPO_ROOT / "tests" / "experiment_b_results.json"
        with open(results_path, "w") as f:
            json.dump({"summary": summary, "trials": results}, f, indent=2)
        log(f"\nResults saved to {results_path}")

    finally:
        if _log_file:
            _log_file.close()
            _log_file = None


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Validate fixture with dry-run**

Run: `python3 tests/test_experiment_b.py --dry-run`
Expected: "PASS: Fixture validated." with 6 call sites verified and KB_INDEX.md containing exports (requires Task 1+2 complete).

If Task 1+2 is not yet done, the dry-run will warn "KB_INDEX.md does NOT contain exports lines" — this is expected and the experiment will still work once exports are implemented.

- [ ] **Step 3: Commit**

```bash
git add tests/test_experiment_b.py
git commit -m "feat: Experiment B — code intelligence signature change script with fixture"
```

---

## Task 5: Dry-Run Validation and Wiki-Link Tuning

**Files:**
- Possibly modify: `tests/test_experiment_a.py` (fixture content, wiki-link text)

The wiki-link resolver in `kb_graph.py` uses basename/stem matching. This task validates that the fixture's wiki-links resolve correctly and adjusts link text if needed.

- [ ] **Step 1: Run Experiment A dry-run**

Run: `python3 tests/test_experiment_a.py --dry-run`

Check the output for:
1. "13 blast radius files exist in fixture" — all expected files present
2. The traverse output lists exactly the 13 expected files
3. "PASS: Ground truth matches traverse output exactly."

- [ ] **Step 2: Debug wiki-link resolution if needed**

If files are missing from the traverse output, the issue is wiki-link text vs. filename matching. The resolver works by:
The fixture content already uses full stems (e.g., `[[02-processing-engine]]` not `[[02-processing]]`). But if the dry-run shows missing files, the most likely issue is a wiki-link stem mismatch. Check each `[[link]]` in the fixture against the target file's stem (filename without extension). Common pitfalls:
- `[[02-processing]]` would NOT match `02-processing-engine.md` — must use `[[02-processing-engine]]`
- `[[setup.md]]` works because the resolver does basename matching when the link has an extension

Update the `FIXTURE_FILES` dict in `test_experiment_a.py` to fix any wiki-link mismatches.

- [ ] **Step 3: Run Experiment B dry-run**

Run: `python3 tests/test_experiment_b.py --dry-run`

Check for:
1. "6 call sites verified in fixture" — all before patterns match
2. "KB_INDEX.md contains exports" and "KB_INDEX.md lists apply_transform signature"
3. "PASS: Fixture validated."

- [ ] **Step 4: Fix any issues and re-run dry-runs**

Iterate until both dry-runs pass completely.

- [ ] **Step 5: Commit any fixes**

```bash
git add tests/test_experiment_a.py tests/test_experiment_b.py
git commit -m "fix: tune wiki-link text and fixture content for dry-run validation"
```

---

## Task 6: Run Experiments

**Files:** none modified (this is execution only)

- [ ] **Step 1: Run Experiment A — 1 trial with transcripts**

Run: `python3 tests/test_experiment_a.py --save-transcripts`

Check results. Expected: Agent B recall >> Agent A recall. If both agents achieve similar recall, review the transcripts to understand why and note the result.

- [ ] **Step 2: Run Experiment B — 1 trial with transcripts**

Run: `python3 tests/test_experiment_b.py --save-transcripts`

Check results. Expected: Agent B higher recall and precision than Agent A.

- [ ] **Step 3: Document results**

Update `docs/phoam_paint/phase5_v4_design.md` with the actual experiment results, following the same format as the v3 results section. Include:
- Table with recall, precision, time for each agent
- What happened (narrative)
- Whether the experiment differentiated the agents

- [ ] **Step 4: Update plan.md status**

Update the Phase 5 v4 status in `docs/phoam_paint/plan.md` from "Not started" to the actual outcome.

- [ ] **Step 5: Commit results**

```bash
git add docs/phoam_paint/phase5_v4_design.md docs/phoam_paint/plan.md
git add tests/experiment_a_results.json tests/experiment_b_results.json
git add tests/experiment_a.log tests/experiment_b.log
git commit -m "docs: Phase 5 v4 experiment results"
```
