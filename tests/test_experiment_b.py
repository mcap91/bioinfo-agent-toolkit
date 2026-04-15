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


def _kb_graph_cmd():
    """Return the command prefix for invoking kb-graph.

    On Windows, extensionless scripts can't be found by subprocess
    without shell=True. We resolve the full path and invoke via Python.
    """
    kb = shutil.which("kb-graph")
    if kb:
        return [sys.executable, kb]
    # Fallback: check common install location
    home_bin = Path.home() / ".local" / "bin" / "kb-graph"
    if home_bin.exists():
        return [sys.executable, str(home_bin)]
    return ["kb-graph"]


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
    if shutil.which("claude") is None:
        missing.append("claude")
    # kb-graph: shutil.which fails on Windows for extensionless scripts
    kb_cmd = _kb_graph_cmd()
    if kb_cmd == ["kb-graph"]:
        missing.append("kb-graph")
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
        [*_kb_graph_cmd(), "init", "."], cwd=project_dir,
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
