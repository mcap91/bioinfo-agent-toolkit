#!/usr/bin/env python3
"""Phase 5 v5 — Realistic Prompt Experiment.

Three scenarios testing whether vague, realistic prompts differentiate
Agent A (no graph) from Agent B (with kb-graph + CLAUDE.md rules).

Scenarios:
  A: "Fix this thing"         — discover downstream call sites of a param rename
  B: "Something is broken"    — root cause vs symptom from a failing test output
  C: "Rename a file"          — discover wiki-link references to a renamed doc

Requirements:
    - Claude Code CLI (`claude` command on PATH)
    - API access configured (ANTHROPIC_API_KEY or OAuth)
    - kb-graph installed (`kb-graph` on PATH)

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


# ── Code Fixture (80-file Python data pipeline, from Experiment B) ───────

FIXTURE_FILES_CODE = {
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


# ── Docs Fixture (35-file wiki-link docs, from Experiment A) ─────────────

FIXTURE_FILES_DOCS = {
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


# ── Ground Truth: Scenarios A & B (call sites) ───────────────────────────

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

SHOULD_NOT_MODIFY = [
    "src/core/transform.py",
    "src/preprocessing/filter.py",
    "src/preprocessing/clean.py",
    "src/analysis/correlate.py",
    "src/io/writers.py",
    "tests/conftest.py",
    "docs/tutorial.md",
    "scripts/benchmark.py",
]

# Source files used for root-cause vs symptom classification in Scenario B
SOURCE_FILES_SCENARIO_B = {
    "src/preprocessing/normalize.py",
    "src/analysis/aggregate.py",
    "src/pipeline/run.py",
}


# ── Scenario A prompts ───────────────────────────────────────────────────

PROMPT_A_SCENARIO_A = (
    "I updated apply_transform() in src/core/transform.py — the strict "
    "parameter is now called mode (takes \"strict\" or \"lenient\" instead "
    "of True/False). Can you make sure I didn't break anything?"
)

PROMPT_B_SCENARIO_A = (
    "Read CLAUDE.md first. I updated apply_transform() in "
    "src/core/transform.py — the strict parameter is now called mode "
    "(takes \"strict\" or \"lenient\" instead of True/False). Can you "
    "make sure I didn't break anything?"
)


# ── Scenario B: fake test traceback ──────────────────────────────────────

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
    "The tests are failing — see test_output.txt for the traceback. Can "
    "you fix whatever is broken?"
)

PROMPT_B_SCENARIO_B = (
    "Read CLAUDE.md first. The tests are failing — see test_output.txt "
    "for the traceback. Can you fix whatever is broken?"
)


# ── Scenario C: file rename ──────────────────────────────────────────────

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
    "docs/design/02-data-processing.md. Update the content to reflect the "
    "new name."
)

PROMPT_B_SCENARIO_C = (
    "Read CLAUDE.md first. Rename docs/design/02-processing-engine.md to "
    "docs/design/02-data-processing.md. Update the content to reflect the "
    "new name."
)


# ── Helpers ──────────────────────────────────────────────────────────────

def check_prerequisites():
    missing = []
    if shutil.which("claude") is None:
        missing.append("claude")
    kb_cmd = _kb_graph_cmd()
    if kb_cmd == ["kb-graph"]:
        missing.append("kb-graph")
    if missing:
        log(f"ERROR: Missing prerequisites: {', '.join(missing)}")
        sys.exit(1)


def create_fixture(dest, files_dict):
    """Write all files in `files_dict` under `dest`."""
    for rel_path, content in files_dict.items():
        filepath = Path(dest) / rel_path
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding="utf-8")


def init_graph(project_dir):
    """Initialize git + run kb-graph init on `project_dir`."""
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
    """Invoke the claude CLI with `prompt` inside `project_dir`."""
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


def detect_strategy(transcript):
    """Classify how the agent approached the task from its transcript."""
    text = (transcript or "").lower()
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


# ── Scenario A: setup + score ────────────────────────────────────────────

def _apply_signature_change(transform_path):
    """Rewrite src/core/transform.py to use `mode: str = "strict"` instead
    of `strict=True`. The fixture source has `strict=True` (no type
    annotation) and `if config.validate and strict:` — we replace those
    exact substrings."""
    content = transform_path.read_text(encoding="utf-8")
    new = content.replace(
        "def apply_transform(data, config, strict=True):",
        'def apply_transform(data, config, mode: str = "strict"):',
    )
    new = new.replace(
        "if config.validate and strict:",
        'if config.validate and mode == "strict":',
    )
    transform_path.write_text(new, encoding="utf-8")


def setup_scenario_a(dir_a, dir_b):
    """Build code fixture in both dirs and pre-modify transform.py."""
    create_fixture(dir_a, FIXTURE_FILES_CODE)
    create_fixture(dir_b, FIXTURE_FILES_CODE)
    _apply_signature_change(Path(dir_a) / "src/core/transform.py")
    _apply_signature_change(Path(dir_b) / "src/core/transform.py")


def score_scenario_a(project_dir):
    """Score call-site fixes against EXPECTED_FIXES. Same as Experiment B."""
    correct = []
    missed = []
    wrong = []

    for fix in EXPECTED_FIXES:
        filepath = Path(project_dir) / fix["file"]
        try:
            content = filepath.read_text(encoding="utf-8")
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
            missed.append(fix)
        else:
            wrong.append(fix)

    false_positives = []
    for rel_path in SHOULD_NOT_MODIFY:
        filepath = Path(project_dir) / rel_path
        if not filepath.exists():
            continue
        try:
            content = filepath.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if re.search(r'mode\s*=\s*"(strict|lenient)"', content):
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


# ── Scenario B: setup + score ────────────────────────────────────────────

def setup_scenario_b(dir_a, dir_b):
    """Scenario A setup + add a fake test_output.txt traceback in both dirs."""
    setup_scenario_a(dir_a, dir_b)
    (Path(dir_a) / "test_output.txt").write_text(TEST_OUTPUT_TXT, encoding="utf-8")
    (Path(dir_b) / "test_output.txt").write_text(TEST_OUTPUT_TXT, encoding="utf-8")


def score_scenario_b(project_dir):
    """Score like A, plus classify as revert / symptom / root_cause."""
    transform_path = Path(project_dir) / "src/core/transform.py"
    transform_content = transform_path.read_text(encoding="utf-8") if transform_path.exists() else ""

    if 'mode: str = "strict"' not in transform_content:
        return {
            "recall": 0.0,
            "precision": 0.0,
            "classification": "revert",
            "correct": [],
            "missed": [f["description"] for f in EXPECTED_FIXES],
            "wrong": [],
            "false_positives": [],
            "perfect": False,
        }

    result = score_scenario_a(project_dir)

    fixed_source = any(
        fix["file"] in SOURCE_FILES_SCENARIO_B
        for fix in EXPECTED_FIXES
        if fix["description"] in result["correct"]
    )
    result["classification"] = "root_cause" if fixed_source else "symptom"
    return result


# ── Scenario C: setup + score ────────────────────────────────────────────

def setup_scenario_c(dir_a, dir_b):
    """Build the wiki-link docs fixture in both dirs. No pre-mutations."""
    create_fixture(dir_a, FIXTURE_FILES_DOCS)
    create_fixture(dir_b, FIXTURE_FILES_DOCS)


def score_scenario_c(project_dir):
    """Score: was the file renamed? And how many references were updated?"""
    project = Path(project_dir)

    old_exists = (project / TARGET_C).exists()
    new_exists = (project / RENAMED_C).exists()
    file_renamed = (not old_exists) and new_exists

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
        "precision": 1.0,
        "correct": [r["file"] for r in correct],
        "missed": [r["file"] for r in missed],
        "refs_updated": n_correct,
        "refs_total": total,
        "perfect": file_renamed and n_correct == total,
    }


# ── Scenario config ──────────────────────────────────────────────────────

SCENARIOS = {
    "A": {
        "name": "Fix this thing",
        "setup": setup_scenario_a,
        "prompt_a": PROMPT_A_SCENARIO_A,
        "prompt_b": PROMPT_B_SCENARIO_A,
        "score": score_scenario_a,
        "expected_total": len(EXPECTED_FIXES),
    },
    "B": {
        "name": "Something is broken",
        "setup": setup_scenario_b,
        "prompt_a": PROMPT_A_SCENARIO_B,
        "prompt_b": PROMPT_B_SCENARIO_B,
        "score": score_scenario_b,
        "expected_total": len(EXPECTED_FIXES),
    },
    "C": {
        "name": "Rename a file",
        "setup": setup_scenario_c,
        "prompt_a": PROMPT_A_SCENARIO_C,
        "prompt_b": PROMPT_B_SCENARIO_C,
        "score": score_scenario_c,
        "expected_total": len(EXPECTED_REFS_C),
    },
}


# ── Dry-run validation ───────────────────────────────────────────────────

def _check(label, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    suffix = f" — {detail}" if detail else ""
    log(f"  [{status}] {label}{suffix}")
    return bool(condition)


def _dry_run_scenario_a(dir_a, dir_b):
    """Validate Scenario A fixture state after setup."""
    ok = True

    transform_a = (Path(dir_a) / "src/core/transform.py").read_text(encoding="utf-8")
    ok &= _check(
        "A/transform.py has mode: str = \"strict\"",
        'mode: str = "strict"' in transform_a,
    )
    transform_b = (Path(dir_b) / "src/core/transform.py").read_text(encoding="utf-8")
    ok &= _check(
        "B/transform.py has mode: str = \"strict\"",
        'mode: str = "strict"' in transform_b,
    )

    for fix in EXPECTED_FIXES:
        fp = Path(dir_a) / fix["file"]
        content = fp.read_text(encoding="utf-8")
        ok &= _check(
            f"{fix['file']} — before pattern present",
            re.search(fix["before"], content) is not None,
            fix["description"],
        )

    kb_index = Path(dir_b) / "KB_INDEX.md"
    if not kb_index.exists():
        return _check("B/KB_INDEX.md exists (requires kb-graph init)", False) and ok
    content = kb_index.read_text(encoding="utf-8")
    ok &= _check(
        "B/KB_INDEX.md exists and mentions transform.py",
        "transform.py" in content,
    )
    return ok


def _dry_run_scenario_b(dir_a, dir_b):
    """Validate Scenario B fixture state after setup."""
    ok = _dry_run_scenario_a(dir_a, dir_b)
    for d in (dir_a, dir_b):
        test_output = Path(d) / "test_output.txt"
        ok &= _check(
            f"{Path(d).name}/test_output.txt exists and has TypeError",
            test_output.exists()
            and "TypeError" in test_output.read_text(encoding="utf-8"),
        )
    return ok


def _dry_run_scenario_c(dir_a, dir_b):
    """Validate Scenario C fixture state after setup."""
    ok = True
    for d in (dir_a, dir_b):
        target = Path(d) / TARGET_C
        ok &= _check(
            f"{Path(d).name}/{TARGET_C} exists",
            target.exists(),
        )
    for ref in EXPECTED_REFS_C:
        fp = Path(dir_a) / ref["file"]
        if not fp.exists():
            ok &= _check(f"{ref['file']} exists", False)
            continue
        content = fp.read_text(encoding="utf-8")
        ok &= _check(
            f"{ref['file']} contains {ref['old']}",
            ref["old"] in content,
        )

    kb_index = Path(dir_b) / "KB_INDEX.md"
    if not kb_index.exists():
        return _check("B/KB_INDEX.md exists (requires kb-graph init)", False) and ok
    content = kb_index.read_text(encoding="utf-8")
    ok &= _check(
        "B/KB_INDEX.md mentions the target doc",
        "02-processing-engine.md" in content,
    )

    traverse = subprocess.run(
        [*_kb_graph_cmd(), "traverse", TARGET_C],
        cwd=dir_b, capture_output=True, text=True,
    )
    if traverse.returncode == 0:
        out = traverse.stdout
        # Spot-check that at least one expected wiki-link referrer shows up
        depth1_ref = "00-platform-overview.md"
        ok &= _check(
            "kb-graph traverse output lists a depth-1 referrer",
            depth1_ref in out,
            depth1_ref,
        )
    else:
        ok &= _check("kb-graph traverse ran successfully", False, traverse.stderr.strip()[:120])
    return ok


DRY_RUN_CHECKERS = {
    "A": _dry_run_scenario_a,
    "B": _dry_run_scenario_b,
    "C": _dry_run_scenario_c,
}


def dry_run_scenario(scenario, cfg, args):
    log(f"\nDRY RUN — Scenario {scenario}: {cfg['name']}\n")
    tmpdir = tempfile.mkdtemp(prefix=f"kb_exp_v5_{scenario.lower()}_dry_")
    try:
        dir_a = Path(tmpdir) / "project_a"
        dir_b = Path(tmpdir) / "project_b"
        dir_a.mkdir()
        dir_b.mkdir()
        cfg["setup"](str(dir_a), str(dir_b))
        init_graph(str(dir_b))
        ok = DRY_RUN_CHECKERS[scenario](str(dir_a), str(dir_b))
        log(f"\n  {'PASS' if ok else 'FAIL'} — Scenario {scenario} dry-run")
        return ok
    finally:
        if args.clean:
            shutil.rmtree(tmpdir, ignore_errors=True)
        else:
            log(f"  (fixture left at {tmpdir})")


# ── Trial + scenario orchestration ───────────────────────────────────────

def run_trial(scenario, cfg, trial_num, args):
    log(f"\n── Scenario {scenario} / Trial {trial_num} ──")
    tmpdir = tempfile.mkdtemp(prefix=f"kb_exp_v5_{scenario.lower()}_t{trial_num}_")
    try:
        dir_a = Path(tmpdir) / "project_a"
        dir_b = Path(tmpdir) / "project_b"
        dir_a.mkdir()
        dir_b.mkdir()

        log(f"  Building fixture at {tmpdir}...")
        cfg["setup"](str(dir_a), str(dir_b))

        log("  Running kb-graph init on project_b...")
        init_graph(str(dir_b))

        log(f"  Running Agent A (no graph)... timeout={args.timeout}s")
        out_a, err_a, rc_a, t_a = run_agent(
            str(dir_a), cfg["prompt_a"], model=args.model, timeout=args.timeout,
        )
        log(f"    exit={rc_a} elapsed={t_a:.1f}s")

        log(f"  Running Agent B (with graph)... timeout={args.timeout}s")
        out_b, err_b, rc_b, t_b = run_agent(
            str(dir_b), cfg["prompt_b"], model=args.model, timeout=args.timeout,
        )
        log(f"    exit={rc_b} elapsed={t_b:.1f}s")

        score_a = cfg["score"](str(dir_a))
        score_b = cfg["score"](str(dir_b))
        strategy_a = detect_strategy(out_a + "\n" + err_a)
        strategy_b = detect_strategy(out_b + "\n" + err_b)

        if args.save_transcripts:
            transcript_dir = REPO_ROOT / "tests" / "experiment_transcripts"
            transcript_dir.mkdir(parents=True, exist_ok=True)
            for suffix, content in [
                (f"v5{scenario.lower()}_trial_{trial_num}_agent_a.txt", out_a + "\n\n--- STDERR ---\n" + err_a),
                (f"v5{scenario.lower()}_trial_{trial_num}_agent_b.txt", out_b + "\n\n--- STDERR ---\n" + err_b),
            ]:
                (transcript_dir / suffix).write_text(content, encoding="utf-8")

        return {
            "trial": trial_num,
            "agent_a": {
                "recall": score_a.get("recall", 0.0),
                "precision": score_a.get("precision", 0.0),
                "elapsed": t_a,
                "exit_code": rc_a,
                "strategy": strategy_a,
                "score": score_a,
            },
            "agent_b": {
                "recall": score_b.get("recall", 0.0),
                "precision": score_b.get("precision", 0.0),
                "elapsed": t_b,
                "exit_code": rc_b,
                "strategy": strategy_b,
                "score": score_b,
            },
        }
    finally:
        if args.clean:
            shutil.rmtree(tmpdir, ignore_errors=True)
        else:
            log(f"  (trial artifacts left at {tmpdir})")


def print_summary(scenario, cfg, results):
    log(f"\n══════ Scenario {scenario}: {cfg['name']} ══════")
    log(f"  Trials: {len(results)}")

    def avg(key, who):
        vals = [r[who][key] for r in results]
        return sum(vals) / len(vals) if vals else 0.0

    def perfect(who):
        return sum(1 for r in results if r[who]["score"].get("perfect"))

    a_recall = avg("recall", "agent_a")
    b_recall = avg("recall", "agent_b")
    a_prec = avg("precision", "agent_a")
    b_prec = avg("precision", "agent_b")
    a_time = avg("elapsed", "agent_a")
    b_time = avg("elapsed", "agent_b")

    log(f"  Agent A (no graph):   recall={a_recall:.0%} precision={a_prec:.0%} avg_time={a_time:.1f}s perfect={perfect('agent_a')}/{len(results)}")
    log(f"  Agent B (with graph): recall={b_recall:.0%} precision={b_prec:.0%} avg_time={b_time:.1f}s perfect={perfect('agent_b')}/{len(results)}")

    a_strategy = {
        k: sum(1 for r in results if r["agent_a"]["strategy"].get(k))
        for k in ["used_graph", "used_grep", "read_claude_md", "checked_imports"]
    }
    b_strategy = {
        k: sum(1 for r in results if r["agent_b"]["strategy"].get(k))
        for k in ["used_graph", "used_grep", "read_claude_md", "checked_imports"]
    }
    log(f"  Strategy counts (Agent A): {a_strategy}")
    log(f"  Strategy counts (Agent B): {b_strategy}")

    if scenario == "B":
        a_classes = [r["agent_a"]["score"].get("classification") for r in results]
        b_classes = [r["agent_b"]["score"].get("classification") for r in results]
        log(f"  Classifications (Agent A): {a_classes}")
        log(f"  Classifications (Agent B): {b_classes}")

    return {
        "trials": len(results),
        "agent_a_avg_recall": a_recall,
        "agent_b_avg_recall": b_recall,
        "agent_a_avg_precision": a_prec,
        "agent_b_avg_precision": b_prec,
        "agent_a_avg_time": a_time,
        "agent_b_avg_time": b_time,
        "agent_a_perfect": perfect("agent_a"),
        "agent_b_perfect": perfect("agent_b"),
    }


def run_scenario(scenario, args):
    cfg = SCENARIOS[scenario]
    log(f"\n═══════════════════════════════════════════════════")
    log(f"Scenario {scenario}: {cfg['name']}")
    log(f"═══════════════════════════════════════════════════")

    if args.dry_run:
        return dry_run_scenario(scenario, cfg, args)

    results = []
    for trial_num in range(1, args.trials + 1):
        result = run_trial(scenario, cfg, trial_num, args)
        results.append(result)

    summary = print_summary(scenario, cfg, results)

    results_path = REPO_ROOT / "tests" / f"experiment_v5_{scenario.lower()}_results.json"
    payload = {
        "scenario": scenario,
        "name": cfg["name"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "claude_version": get_claude_version(),
        "model": args.model or "default",
        "summary": summary,
        "trials": results,
    }
    results_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    log(f"  Results saved to {results_path}")
    return True


# ── Entry point ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Phase 5 v5 — Realistic Prompt Experiment",
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
    parser.add_argument("--clean", action="store_true",
                        help="Remove tmpdirs after each trial (default: keep for inspection)")
    args = parser.parse_args()

    log_path = REPO_ROOT / "tests" / "experiment_v5.log"
    global _log_file
    _log_file = open(log_path, "a", encoding="utf-8")
    try:
        log("")
        log(f"══════ {datetime.now(timezone.utc).isoformat()} ══════")
        log(f"Scenario(s): {args.scenario} | Trials: {args.trials} | "
            f"Model: {args.model or 'default'} | Dry-run: {args.dry_run}")

        if not args.dry_run:
            check_prerequisites()

        scenarios = ["A", "B", "C"] if args.scenario == "all" else [args.scenario]
        all_ok = True
        for scenario in scenarios:
            ok = run_scenario(scenario, args)
            all_ok &= bool(ok) if args.dry_run else True

        if args.dry_run and not all_ok:
            sys.exit(1)
    finally:
        if _log_file:
            _log_file.close()


if __name__ == "__main__":
    main()
