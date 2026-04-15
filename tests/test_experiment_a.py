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
    "docs/design/00-platform-overview.md",    # [[02-processing-engine]] wiki-link
    "docs/design/01-data-ingestion.md",       # [[02-processing-engine]] wiki-link
    "docs/design/05-scheduling.md",           # [[02-processing-engine]] wiki-link
    "docs/design/10-architecture.md",         # [[02-processing-engine]] wiki-link
    "docs/reference/design-notes.md",         # [[02-processing-engine]] wiki-link
    "configs/platform_config.yaml",           # config-ref path
]

EXPECTED_DEPTH_2 = [
    "README.md",                              # links to 00-platform-overview
    "docs/design/06-security-auth.md",        # links to 01-data-ingestion
    "docs/design/09-open-questions.md",       # links to 00-platform-overview
    "docs/guides/getting-started.md",         # links to 00-platform-overview
    "docs/guides/performance-guide.md",       # links to 10-architecture
    "docs/reference/research-notes.md",       # links to 01-data-ingestion
    "docs/reference/setup.md",               # links to 10-architecture
]

EXPECTED_DEPTH_3 = [
    # None — all transitives are reachable within depth 2 because
    # 01-data-ingestion.md directly links to [[02-processing-engine]]
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
            [*_kb_graph_cmd(), "traverse", TARGET, "--depth", "3"],
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
                if not token or token.startswith("BLAST"):
                    continue
                # Check if it looks like a file path (with / or a root-level file)
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
