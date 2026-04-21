# Phase 5 v3 A/B Experiment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite the A/B experiment fixture from a 46-file web-app to a ~100-file bioinformatics project with depth-4 import chains, so Agent A reliably fails (20-30% recall) and Agent B reliably passes (100% recall).

**Architecture:** Replace all fixture data in `tests/test_agent_experiment.py` with bioinformatics-themed Python stubs. 19 files form the blast radius of `src/core/metadata.py` through `__init__.py` re-exports and relative imports at depths 1-4. ~80 noise files (including 5 red herrings mentioning "metadata") pad the project. The test infrastructure (copytree + overlay pattern, agent runner, scoring) stays intact with scoring extended to 4 depth levels.

**Tech Stack:** Python 3.10+, subprocess (claude CLI, kb-graph CLI), tempfile, shutil

**Spec:** `docs/phoam_paint/phase5_v3_design.md`

---

## Spec Correction: Blast Radius Depths

The spec's blast radius TABLE has an error at depth 3. The fixture structure COMMENTS are correct. Here's the corrected grouping:

The spec lists `clustering.py` at depth 3 with import `from annotation.ontology import ...`. But `ontology.py` is depth 1, so `clustering.py` is depth **2**. The fixture tree comments confirm this: `clustering.py # imports annotation.ontology (depth 2 via ontology)`.

**Corrected depth grouping (19 files):**

| Depth | Count | Files |
|-------|-------|-------|
| 1 | 4 | core/\_\_init\_\_.py, annotation/ontology.py, annotation/confidence.py, tests/test_metadata.py |
| 2 | 5 | annotation/\_\_init\_\_.py, annotation/markers.py, annotation/cell_types.py, preprocessing/base.py, analysis/clustering.py |
| 3 | 5 | preprocessing/\_\_init\_\_.py, preprocessing/normalization.py, preprocessing/qc.py, analysis/spatial.py, plotting/spatial_plot.py |
| 4 | 5 | preprocessing/ingestion.py, preprocessing/batch.py, pipelines/run_qc.py, pipelines/run_analysis.py, plotting/heatmap.py |

## Critical Parser Constraint

`kb_graph.py`'s `parse_python()` resolves `from X import Y` by first trying `X.Y` as a file path. This means:

- `from core import metadata` resolves to `src/core/metadata.py` (DIRECT edge, depth 1)
- `from core import MetadataManager` tries `core.MetadataManager` (no file) → falls back to `core` → `src/core/__init__.py` (edge to \_\_init\_\_, depth 2 via \_\_init\_\_)

**`preprocessing/base.py` MUST use `from core import MetadataManager`** (not `from core import metadata`) to create the intended depth-2 relationship through `core/__init__.py`.

## Files

- **Modify:** `tests/test_agent_experiment.py` (full rewrite of fixture data, prompts, scoring)
- **Modify:** `docs/phoam_paint/plan.md` (add Phase 5 v3 subsection)

---

### Task 1: Replace fixture data — blast radius files (depths 1-4)

**Files:**
- Modify: `tests/test_agent_experiment.py:86-918` (replace all ENHANCED_*, NEW_FILES, NOISE_FILES, ENHANCEMENTS dicts)

Replace all existing fixture string constants with a single `V3_FILES` dict. The 19 blast radius files + the target file (`metadata.py`) + its leaf dependencies (`config.py`, `logging.py`) must have imports that resolve correctly through `kb_graph.py`'s parser.

- [ ] **Step 1: Delete old fixture constants, write V3_FILES dict header and target file**

Remove everything from `ENHANCED_CONFIG_PY` (line 86) through the closing of `ENHANCEMENTS` dict (line 918). Replace with the start of `V3_FILES` and the target file + its leaf dependencies:

```python
# ── v3 Bioinformatics Fixture ──────────────────────────────────────────
# ~100 files modeling a spatial-omics analysis package.
# Target: src/core/metadata.py — 19 files in its blast radius at depth 4.
# Red herring files mention "metadata" in comments/strings but do NOT import it.
#
# Import resolution through kb_graph.py's parse_python():
#   "from core.metadata import X"  → resolves core.metadata → src/core/metadata.py
#   "from core import MetadataManager" → core.MetadataManager fails → core → src/core/__init__.py
#   "from .metadata import X"       → resolves .metadata → src/core/metadata.py
#   "from .ontology import X"       → resolves .ontology → src/annotation/ontology.py

V3_FILES = {
    # ── TARGET FILE ────────────────────────────────────────────────────
    "src/core/metadata.py": '''\
"""Sample metadata management for spatial-omics experiments.

Handles per-sample annotations: tissue origin, capture date, QC flags,
spatial coordinates, and donor demographics.  Every downstream module
that needs sample context imports MetadataManager from here.
"""
from core.config import Config
from core.logging import get_logger

logger = get_logger(__name__)


class MetadataManager:
    """Central registry of per-sample metadata records."""

    def __init__(self, config: Config):
        self.config = config
        self._records = {}
        logger.info("MetadataManager initialised")

    def register(self, sample_id, tissue, capture_date, **extra):
        """Register a new sample with required and optional fields."""
        record = {
            "sample_id": sample_id,
            "tissue": tissue,
            "capture_date": capture_date,
            **extra,
        }
        self._records[sample_id] = record
        return record

    def get(self, sample_id):
        """Retrieve metadata for a single sample."""
        return self._records.get(sample_id)

    def list_samples(self, tissue=None):
        """List sample IDs, optionally filtered by tissue type."""
        if tissue is None:
            return list(self._records.keys())
        return [sid for sid, rec in self._records.items() if rec["tissue"] == tissue]

    def summary(self):
        """Return a summary dict of all registered samples."""
        tissues = {}
        for rec in self._records.values():
            tissues[rec["tissue"]] = tissues.get(rec["tissue"], 0) + 1
        return {"total": len(self._records), "by_tissue": tissues}
''',

    # ── LEAF DEPENDENCIES (imported BY metadata.py, NOT in blast radius) ──

    "src/core/config.py": '''\
"""Global configuration for the spatial-omics pipeline."""


class Config:
    """Immutable pipeline configuration."""

    def __init__(self, data_dir="data/", n_threads=4, seed=42):
        self.data_dir = data_dir
        self.n_threads = n_threads
        self.seed = seed

    @classmethod
    def from_yaml(cls, path):
        """Load config from a YAML file (stub)."""
        return cls()

    def as_dict(self):
        return {"data_dir": self.data_dir, "n_threads": self.n_threads, "seed": self.seed}
''',

    "src/core/logging.py": '''\
"""Structured logging for the spatial-omics pipeline."""


class Logger:
    """Minimal structured logger."""

    def __init__(self, name, level="INFO"):
        self.name = name
        self.level = level

    def info(self, msg, **kw):
        print(f"[{self.level}] {self.name}: {msg}")

    def warn(self, msg, **kw):
        print(f"[WARN] {self.name}: {msg}")

    def error(self, msg, **kw):
        print(f"[ERROR] {self.name}: {msg}")


def get_logger(name):
    """Return a Logger instance for the given module name."""
    return Logger(name)
''',

    "src/core/exceptions.py": '''\
"""Custom exception hierarchy for the pipeline."""


class PipelineError(Exception):
    """Base exception for all pipeline errors."""
    def __init__(self, message, stage=None):
        super().__init__(message)
        self.stage = stage


class QCError(PipelineError):
    """Quality control check failed."""
    def __init__(self, metric, value, threshold):
        super().__init__(f"{metric}={value} below threshold {threshold}", stage="qc")
        self.metric = metric


class MetadataError(PipelineError):
    """Metadata validation failed."""
    def __init__(self, sample_id, reason):
        super().__init__(f"Sample {sample_id}: {reason}", stage="metadata")
''',
```

- [ ] **Step 2: Add depth-1 blast radius files**

These 4 files directly import `src/core/metadata.py`:

```python
    # ── DEPTH 1 — direct dependents of metadata.py ────────────────────

    "src/core/__init__.py": '''\
"""Core package — re-exports key classes for convenient access."""
from .metadata import MetadataManager
from .config import Config
from .logging import get_logger

__all__ = ["MetadataManager", "Config", "get_logger"]
''',

    "src/annotation/ontology.py": '''\
"""Gene Ontology term mapping for spatial features."""
from core.metadata import MetadataManager


class OntologyMapper:
    """Maps gene IDs to GO terms using sample context from metadata."""

    def __init__(self, meta: MetadataManager):
        self._meta = meta
        self._cache = {}

    def annotate(self, gene_id, sample_id):
        """Return GO terms for a gene in the context of a sample."""
        sample = self._meta.get(sample_id)
        tissue = sample["tissue"] if sample else "unknown"
        return self._cache.get((gene_id, tissue), [])

    def load_ontology(self, path):
        """Load a GO OBO file (stub)."""
        self._cache.clear()
        return self
''',

    "src/annotation/confidence.py": '''\
"""Confidence scoring for spatial annotations."""
from core.metadata import MetadataManager


class ConfidenceScorer:
    """Scores annotation confidence based on sample QC metadata."""

    def __init__(self, meta: MetadataManager):
        self._meta = meta

    def score(self, annotation, sample_id):
        """Return a confidence float in [0, 1] for an annotation."""
        sample = self._meta.get(sample_id)
        if sample is None:
            return 0.0
        base = 0.8
        if sample.get("qc_pass", False):
            base += 0.15
        return min(1.0, base)

    def batch_score(self, annotations, sample_id):
        """Score a list of annotations for one sample."""
        return [self.score(a, sample_id) for a in annotations]
''',

    "tests/test_metadata.py": '''\
"""Tests for the MetadataManager class."""
from core.metadata import MetadataManager
from core.config import Config
import unittest


class TestMetadataManager(unittest.TestCase):
    """Verify MetadataManager CRUD and query operations."""

    def setUp(self):
        self.mgr = MetadataManager(Config())

    def test_register_and_get(self):
        rec = self.mgr.register("S001", "brain", "2026-01-15")
        self.assertEqual(self.mgr.get("S001"), rec)

    def test_list_samples_all(self):
        self.mgr.register("S001", "brain", "2026-01-15")
        self.mgr.register("S002", "liver", "2026-01-16")
        self.assertEqual(len(self.mgr.list_samples()), 2)

    def test_list_samples_by_tissue(self):
        self.mgr.register("S001", "brain", "2026-01-15")
        self.mgr.register("S002", "liver", "2026-01-16")
        self.assertEqual(self.mgr.list_samples(tissue="brain"), ["S001"])

    def test_summary(self):
        self.mgr.register("S001", "brain", "2026-01-15")
        s = self.mgr.summary()
        self.assertEqual(s["total"], 1)
''',
```

- [ ] **Step 3: Add depth-2 blast radius files**

These 5 files import depth-1 files. Note `preprocessing/base.py` uses `from core import MetadataManager` to resolve to `core/__init__.py` (NOT directly to `metadata.py`):

```python
    # ── DEPTH 2 — import depth-1 files ────────────────────────────────

    "src/annotation/__init__.py": '''\
"""Annotation package — re-exports main annotation classes."""
from .ontology import OntologyMapper
from .confidence import ConfidenceScorer

__all__ = ["OntologyMapper", "ConfidenceScorer"]
''',

    "src/annotation/markers.py": '''\
"""Cell-type marker gene management."""
from .ontology import OntologyMapper


class MarkerDatabase:
    """Curated marker gene sets for cell-type identification."""

    def __init__(self, ontology: OntologyMapper):
        self._ontology = ontology
        self._markers = {}

    def add_marker(self, cell_type, gene_id):
        """Register a marker gene for a cell type."""
        self._markers.setdefault(cell_type, []).append(gene_id)

    def get_markers(self, cell_type):
        """Return marker genes for a cell type."""
        return self._markers.get(cell_type, [])

    def annotate_markers(self, cell_type, sample_id):
        """Return GO-annotated markers for a cell type."""
        genes = self.get_markers(cell_type)
        return [(g, self._ontology.annotate(g, sample_id)) for g in genes]
''',

    "src/annotation/cell_types.py": '''\
"""Cell-type classification using annotation confidence."""
from .confidence import ConfidenceScorer


class CellTypeClassifier:
    """Assigns cell types to spatial spots based on marker expression."""

    def __init__(self, scorer: ConfidenceScorer, threshold=0.5):
        self._scorer = scorer
        self._threshold = threshold

    def classify(self, expression_vector, sample_id):
        """Return the best cell-type label for an expression vector."""
        candidates = self._rank_candidates(expression_vector)
        for label, score_val in candidates:
            conf = self._scorer.score(label, sample_id)
            if conf >= self._threshold:
                return label, conf
        return "unknown", 0.0

    def _rank_candidates(self, expression_vector):
        """Rank cell-type candidates by expression similarity (stub)."""
        return [("neuron", 0.9), ("astrocyte", 0.7), ("microglia", 0.4)]
''',

    "src/preprocessing/base.py": '''\
"""Base preprocessor with metadata-aware sample handling.

Imports MetadataManager via the core package __init__.py re-export,
NOT directly from core.metadata.  This creates a depth-2 dependency:
base.py -> core/__init__.py -> core/metadata.py
"""
from core import MetadataManager


class BasePreprocessor:
    """Abstract base for all preprocessing steps."""

    def __init__(self, meta: MetadataManager):
        self._meta = meta

    def validate_sample(self, sample_id):
        """Check that a sample exists in the metadata registry."""
        return self._meta.get(sample_id) is not None

    def preprocess(self, sample_id, data):
        """Override in subclasses to implement preprocessing logic."""
        if not self.validate_sample(sample_id):
            raise ValueError(f"Unknown sample: {sample_id}")
        return data

    def get_tissue(self, sample_id):
        """Look up the tissue type for a sample."""
        rec = self._meta.get(sample_id)
        return rec["tissue"] if rec else None
''',

    "src/analysis/clustering.py": '''\
"""Spatial clustering with ontology-aware feature selection."""
from annotation.ontology import OntologyMapper


class ClusterAnalyzer:
    """Clusters spatial spots using GO-term-weighted features."""

    def __init__(self, ontology: OntologyMapper, n_clusters=10):
        self._ontology = ontology
        self.n_clusters = n_clusters

    def fit(self, expression_matrix, sample_id):
        """Fit clusters to an expression matrix (stub)."""
        return list(range(self.n_clusters))

    def predict(self, expression_vector):
        """Assign a spot to a cluster (stub)."""
        return 0

    def feature_weights(self, gene_ids, sample_id):
        """Weight genes by GO-term relevance for clustering."""
        weights = {}
        for gid in gene_ids:
            terms = self._ontology.annotate(gid, sample_id)
            weights[gid] = len(terms) + 1  # more GO terms = higher weight
        return weights
''',
```

- [ ] **Step 4: Add depth-3 blast radius files**

```python
    # ── DEPTH 3 — import depth-2 files ────────────────────────────────

    "src/preprocessing/__init__.py": '''\
"""Preprocessing package — re-exports BasePreprocessor."""
from .base import BasePreprocessor

__all__ = ["BasePreprocessor"]
''',

    "src/preprocessing/normalization.py": '''\
"""Expression matrix normalization."""
from .base import BasePreprocessor


class Normalizer(BasePreprocessor):
    """Log-normalizes expression counts per sample."""

    def __init__(self, meta, scale_factor=10000):
        super().__init__(meta)
        self.scale_factor = scale_factor

    def preprocess(self, sample_id, data):
        """Normalize a count matrix (stub — returns input unchanged)."""
        super().preprocess(sample_id, data)
        return data

    def log_normalize(self, counts):
        """Apply log1p normalization to raw counts (stub)."""
        return counts
''',

    "src/preprocessing/qc.py": '''\
"""Quality control filtering for spatial-omics data."""
from .base import BasePreprocessor


class QualityChecker(BasePreprocessor):
    """Filters low-quality spots and genes."""

    def __init__(self, meta, min_genes=200, min_counts=500):
        super().__init__(meta)
        self.min_genes = min_genes
        self.min_counts = min_counts

    def preprocess(self, sample_id, data):
        """Run QC filters on a count matrix (stub)."""
        super().preprocess(sample_id, data)
        return data

    def filter_spots(self, count_matrix):
        """Remove spots below gene/count thresholds (stub)."""
        return count_matrix

    def filter_genes(self, count_matrix, min_spots=10):
        """Remove genes expressed in too few spots (stub)."""
        return count_matrix
''',

    "src/analysis/spatial.py": '''\
"""Spatial autocorrelation and neighbourhood analysis."""
from preprocessing.base import BasePreprocessor


class SpatialAnalyzer:
    """Computes spatial statistics over preprocessed data."""

    def __init__(self, preprocessor: BasePreprocessor):
        self._preprocessor = preprocessor

    def morans_i(self, expression, coordinates):
        """Compute Moran's I spatial autocorrelation (stub)."""
        return 0.0

    def hotspot_detection(self, expression, coordinates, threshold=0.05):
        """Identify spatial hotspots using Getis-Ord Gi* (stub)."""
        return []

    def neighborhood_enrichment(self, labels, coordinates, n_perms=1000):
        """Test neighbourhood enrichment between cell types (stub)."""
        return {}
''',

    "src/plotting/spatial_plot.py": '''\
"""Spatial scatter plots coloured by cluster labels."""
from analysis.clustering import ClusterAnalyzer


class SpatialPlotter:
    """Generates spatial scatter plots with cluster overlays."""

    def __init__(self, analyzer: ClusterAnalyzer):
        self._analyzer = analyzer

    def plot_clusters(self, coordinates, labels, output_path=None):
        """Render a 2D scatter plot coloured by cluster (stub)."""
        return {"type": "scatter", "n_points": len(coordinates)}

    def plot_expression(self, coordinates, values, gene_name, output_path=None):
        """Render expression levels on spatial coordinates (stub)."""
        return {"type": "expression", "gene": gene_name}
''',
```

- [ ] **Step 5: Add depth-4 blast radius files**

```python
    # ── DEPTH 4 — import depth-3 files ────────────────────────────────

    "src/preprocessing/ingestion.py": '''\
"""Data ingestion from various spatial-omics platforms."""
from .normalization import Normalizer


class DataIngestor:
    """Reads raw data from Visium, MERFISH, or SlideSeq formats."""

    def __init__(self, normalizer: Normalizer):
        self._normalizer = normalizer

    def read_visium(self, path):
        """Load 10x Visium data from a directory (stub)."""
        return {"format": "visium", "path": path}

    def read_merfish(self, path):
        """Load MERFISH data from CSV files (stub)."""
        return {"format": "merfish", "path": path}

    def ingest(self, path, platform="visium"):
        """Auto-detect platform and load data."""
        loaders = {"visium": self.read_visium, "merfish": self.read_merfish}
        loader = loaders.get(platform, self.read_visium)
        return loader(path)
''',

    "src/preprocessing/batch.py": '''\
"""Batch effect correction across samples."""
from .qc import QualityChecker


class BatchCorrector:
    """Removes technical batch effects between samples."""

    def __init__(self, qc: QualityChecker):
        self._qc = qc

    def harmony(self, expression_matrix, batch_labels):
        """Run Harmony integration (stub)."""
        return expression_matrix

    def combat(self, expression_matrix, batch_labels):
        """Run ComBat batch correction (stub)."""
        return expression_matrix

    def correct(self, expression_matrix, batch_labels, method="harmony"):
        """Apply batch correction using the specified method."""
        methods = {"harmony": self.harmony, "combat": self.combat}
        return methods.get(method, self.harmony)(expression_matrix, batch_labels)
''',

    "src/pipelines/run_qc.py": '''\
"""QC pipeline entry point."""
from preprocessing.qc import QualityChecker


def run_qc_pipeline(config, sample_ids):
    """Execute QC checks across all samples (stub)."""
    results = {}
    for sid in sample_ids:
        results[sid] = {"passed": True, "metrics": {}}
    return results


if __name__ == "__main__":
    print("QC pipeline placeholder")
''',

    "src/pipelines/run_analysis.py": '''\
"""Full analysis pipeline entry point."""
from analysis.spatial import SpatialAnalyzer


def run_analysis_pipeline(config, sample_ids):
    """Execute spatial analysis across all samples (stub)."""
    results = {}
    for sid in sample_ids:
        results[sid] = {"clusters": [], "hotspots": []}
    return results


if __name__ == "__main__":
    print("Analysis pipeline placeholder")
''',

    "src/plotting/heatmap.py": '''\
"""Heatmap visualisation for spatial expression data."""
from analysis.spatial import SpatialAnalyzer


class HeatmapRenderer:
    """Renders gene expression heatmaps with spatial context."""

    def __init__(self, analyzer: SpatialAnalyzer):
        self._analyzer = analyzer

    def render(self, expression_matrix, gene_names, output_path=None):
        """Generate a clustered heatmap (stub)."""
        return {"type": "heatmap", "n_genes": len(gene_names)}

    def render_spatial(self, expression, coordinates, gene, output_path=None):
        """Overlay expression heatmap on spatial coordinates (stub)."""
        return {"type": "spatial_heatmap", "gene": gene}
''',
```

- [ ] **Step 6: Verify blast radius file count**

At this point the dict should contain:
- 1 target file (metadata.py)
- 3 leaf dependencies (config.py, logging.py, exceptions.py)
- 4 depth-1 files
- 5 depth-2 files
- 5 depth-3 files
- 5 depth-4 files
= 23 files so far in V3_FILES

---

### Task 2: Add noise files and red herrings

**Files:**
- Modify: `tests/test_agent_experiment.py` (continue V3_FILES dict)

Add ~75 more files to bring the total to ~100. Red herring files mention "metadata" in comments/strings but do NOT import from `core.metadata`.

- [ ] **Step 1: Add noise Python files in src/**

```python
    # ── NOISE FILES — NOT in blast radius ─────────────────────────────

    # analysis/ — unconnected modules
    "src/analysis/__init__.py": '''\
"""Analysis package."""
''',

    "src/analysis/diffusion.py": '''\
"""Diffusion pseudotime analysis for trajectory inference."""


class DiffusionMap:
    """Computes diffusion components from a cell-cell similarity graph."""

    def __init__(self, n_components=10, knn=30):
        self.n_components = n_components
        self.knn = knn

    def fit(self, expression_matrix):
        """Fit diffusion map to expression data (stub)."""
        return self

    def transform(self, expression_matrix):
        """Project data into diffusion space (stub)."""
        return expression_matrix
''',

    "src/analysis/trajectory.py": '''\
"""Trajectory inference for developmental processes."""
# TODO: add metadata tracking for lineage annotations


class TrajectoryInference:
    """Infers developmental trajectories from expression data."""

    def __init__(self, root_cell=None):
        self.root_cell = root_cell
        self._graph = None

    def fit(self, expression_matrix, coordinates=None):
        """Build trajectory graph (stub)."""
        self._graph = {}
        return self

    def pseudotime(self):
        """Return pseudotime ordering of cells (stub)."""
        return []

    def branch_points(self):
        """Identify branching events in the trajectory (stub)."""
        return []
''',

    # plotting/ — unconnected modules
    "src/plotting/__init__.py": '''\
"""Plotting package."""
''',

    "src/plotting/volcano.py": '''\
"""Volcano plot for differential expression results."""


class VolcanoPlot:
    """Renders volcano plots showing fold-change vs significance."""

    def __init__(self, fc_threshold=1.0, pval_threshold=0.05):
        self.fc_threshold = fc_threshold
        self.pval_threshold = pval_threshold

    def render(self, de_results, output_path=None):
        """Generate a volcano plot (stub)."""
        return {"type": "volcano", "n_genes": len(de_results)}
''',

    "src/plotting/umap.py": '''\
"""UMAP dimensionality reduction and plotting."""


class UMAPPlotter:
    """Generates 2D UMAP embeddings for visualisation."""

    def __init__(self, n_neighbors=15, min_dist=0.1):
        self.n_neighbors = n_neighbors
        self.min_dist = min_dist

    def fit_transform(self, expression_matrix):
        """Compute UMAP embedding (stub)."""
        return [[0.0, 0.0]] * 100

    def plot(self, embedding, labels=None, output_path=None):
        """Render a UMAP scatter plot (stub)."""
        return {"type": "umap", "n_points": len(embedding)}
''',

    # pipelines/ — unconnected
    "src/pipelines/__init__.py": '''\
"""Pipeline orchestration package."""
''',

    "src/pipelines/run_plotting.py": '''\
"""Plotting pipeline entry point."""


def run_plotting_pipeline(config, sample_ids):
    """Generate all standard plots for a set of samples (stub)."""
    for sid in sample_ids:
        print(f"Generating plots for {sid}")
    return True


if __name__ == "__main__":
    print("Plotting pipeline placeholder")
''',
```

- [ ] **Step 2: Add test noise files**

```python
    # tests/ — noise test files (no metadata imports)
    "tests/__init__.py": "",

    "tests/test_config.py": '''\
"""Tests for pipeline configuration."""
import unittest


class TestConfig(unittest.TestCase):
    def test_defaults(self):
        self.assertTrue(True)

    def test_from_yaml(self):
        self.assertTrue(True)
''',

    "tests/test_ontology.py": '''\
"""Tests for ontology mapping."""
import unittest


class TestOntologyMapper(unittest.TestCase):
    def test_annotate(self):
        self.assertTrue(True)

    def test_load_ontology(self):
        self.assertTrue(True)
''',

    "tests/test_normalization.py": '''\
"""Tests for expression normalisation."""
import unittest


class TestNormalizer(unittest.TestCase):
    def test_log_normalize(self):
        self.assertTrue(True)

    def test_scale_factor(self):
        self.assertTrue(True)
''',

    "tests/test_spatial.py": '''\
"""Tests for spatial analysis."""
import unittest


class TestSpatialAnalyzer(unittest.TestCase):
    def test_morans_i(self):
        self.assertTrue(True)

    def test_hotspot_detection(self):
        self.assertTrue(True)
''',

    "tests/test_clustering.py": '''\
"""Tests for spatial clustering."""
import unittest


class TestClusterAnalyzer(unittest.TestCase):
    def test_fit(self):
        self.assertTrue(True)

    def test_predict(self):
        self.assertTrue(True)

    def test_feature_weights(self):
        self.assertTrue(True)
''',

    "tests/test_qc.py": '''\
"""Tests for quality control."""
import unittest


class TestQualityChecker(unittest.TestCase):
    def test_filter_spots(self):
        self.assertTrue(True)

    def test_filter_genes(self):
        self.assertTrue(True)

    def test_min_thresholds(self):
        self.assertTrue(True)
''',

    "tests/test_plotting.py": '''\
"""Tests for plotting utilities."""
import unittest


class TestPlotting(unittest.TestCase):
    def test_volcano_render(self):
        self.assertTrue(True)

    def test_umap_plot(self):
        self.assertTrue(True)

    def test_heatmap_render(self):
        self.assertTrue(True)
''',

    "tests/test_ingestion.py": '''\
"""Tests for data ingestion."""
import unittest


class TestDataIngestor(unittest.TestCase):
    def test_read_visium(self):
        self.assertTrue(True)

    def test_read_merfish(self):
        self.assertTrue(True)
''',

    "tests/test_batch.py": '''\
"""Tests for batch correction."""
import unittest


class TestBatchCorrector(unittest.TestCase):
    def test_harmony(self):
        self.assertTrue(True)

    def test_combat(self):
        self.assertTrue(True)
''',

    "tests/test_diffusion.py": '''\
"""Tests for diffusion map analysis."""
import unittest


class TestDiffusionMap(unittest.TestCase):
    def test_fit(self):
        self.assertTrue(True)

    def test_transform(self):
        self.assertTrue(True)
''',

    "tests/test_trajectory.py": '''\
"""Tests for trajectory inference."""
import unittest


class TestTrajectoryInference(unittest.TestCase):
    def test_fit(self):
        self.assertTrue(True)

    def test_pseudotime(self):
        self.assertTrue(True)
''',

    "tests/test_cell_types.py": '''\
"""Tests for cell-type classification."""
import unittest


class TestCellTypeClassifier(unittest.TestCase):
    def test_classify(self):
        self.assertTrue(True)

    def test_threshold(self):
        self.assertTrue(True)
''',

    "tests/test_markers.py": '''\
"""Tests for marker gene management."""
import unittest


class TestMarkerDatabase(unittest.TestCase):
    def test_add_marker(self):
        self.assertTrue(True)

    def test_get_markers(self):
        self.assertTrue(True)
''',

    "tests/test_pipelines.py": '''\
"""Tests for pipeline orchestration."""
import unittest


class TestPipelines(unittest.TestCase):
    def test_qc_pipeline(self):
        self.assertTrue(True)

    def test_analysis_pipeline(self):
        self.assertTrue(True)

    def test_plotting_pipeline(self):
        self.assertTrue(True)
''',
```

- [ ] **Step 3: Add red herring files (mention "metadata" but no imports)**

```python
    # ── RED HERRING FILES — mention "metadata" but NOT dependents ─────

    "tests/conftest.py": '''\
"""Shared test fixtures and configuration."""
import os

# Sample metadata for integration tests — a plain dict literal,
# NOT imported from core.metadata
SAMPLE_METADATA = {
    "S001": {"tissue": "brain", "capture_date": "2026-01-15"},
    "S002": {"tissue": "liver", "capture_date": "2026-01-16"},
    "S003": {"tissue": "heart", "capture_date": "2026-01-17"},
}

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def get_test_sample(sample_id="S001"):
    """Return a test sample metadata dict."""
    return SAMPLE_METADATA.get(sample_id, {})
''',

    "scripts/download_data.py": '''\
"""Download reference data from public repositories."""
import os

# Download sample metadata from GEO and spatial coordinates from
# the Allen Brain Atlas.  This script does NOT import any project
# modules — it is a standalone helper.

URLS = {
    "geo_metadata": "https://ftp.ncbi.nlm.nih.gov/geo/example.csv",
    "allen_atlas": "https://atlas.brain-map.org/example.h5ad",
}


def download(url, dest_dir="data/"):
    """Download a file to the destination directory (stub)."""
    os.makedirs(dest_dir, exist_ok=True)
    print(f"Would download {url} to {dest_dir}")


if __name__ == "__main__":
    for name, url in URLS.items():
        download(url)
''',

    "docs/preprocessing_guide.md": '''\
# Preprocessing Guide

## Overview

The preprocessing pipeline prepares raw spatial-omics data for analysis.
Each sample's metadata (tissue type, capture date, QC flags) is used to
select appropriate normalisation parameters.

## Steps

1. Load raw count matrix
2. Validate sample metadata against the registry
3. Filter low-quality spots (min 200 genes, 500 UMIs)
4. Log-normalise counts with scale factor 10,000
5. Run batch correction if multiple samples

## Notes

- Always check that metadata is complete before running QC
- Missing metadata fields will cause the pipeline to abort
''',

    "configs/pipeline_config.yaml": '''\
# Pipeline configuration
pipeline:
  name: spatial-omics-v3
  version: "0.1.0"

preprocessing:
  min_genes: 200
  min_counts: 500
  scale_factor: 10000

analysis:
  n_clusters: 10
  spatial_neighbors: 6

# Column names expected in sample sheets
metadata_columns:
  - sample_id
  - tissue
  - capture_date
  - donor_id
  - qc_pass
''',
```

- [ ] **Step 4: Add remaining noise files (scripts, docs, configs, R, root)**

```python
    # ── REMAINING NOISE FILES ─────────────────────────────────────────

    "scripts/setup_env.sh": '''\
#!/usr/bin/env bash
# Set up the development environment
set -euo pipefail
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "Environment ready."
''',

    "scripts/run_pipeline.sh": '''\
#!/usr/bin/env bash
# Run the full spatial-omics pipeline
set -euo pipefail
echo "Running QC..."
echo "Running normalisation..."
echo "Running analysis..."
echo "Pipeline complete."
''',

    "scripts/validate_output.py": '''\
"""Validate pipeline output files exist and are non-empty."""
import os
import sys


def validate(output_dir):
    """Check that expected output files exist."""
    expected = ["qc_report.html", "clusters.csv", "spatial_plots/"]
    missing = [f for f in expected if not os.path.exists(os.path.join(output_dir, f))]
    if missing:
        print(f"Missing: {missing}")
        sys.exit(1)
    print("All outputs present.")


if __name__ == "__main__":
    validate(sys.argv[1] if len(sys.argv) > 1 else "output/")
''',

    "scripts/benchmark.py": '''\
"""Benchmark pipeline performance on varying dataset sizes."""
import time


def benchmark(sizes=(100, 500, 1000, 5000)):
    """Time the pipeline on different numbers of spots (stub)."""
    for n in sizes:
        start = time.time()
        # Simulate processing
        time.sleep(0.01)
        elapsed = time.time() - start
        print(f"  n={n}: {elapsed:.3f}s")


if __name__ == "__main__":
    benchmark()
''',

    "scripts/profile_memory.py": '''\
"""Profile memory usage of the preprocessing pipeline."""
import sys


def profile(sample_count=10):
    """Report memory usage estimates (stub)."""
    base_mb = 50
    per_sample_mb = 12
    total = base_mb + sample_count * per_sample_mb
    print(f"Estimated memory: {total} MB for {sample_count} samples")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    profile(n)
''',

    "scripts/export_results.py": '''\
"""Export analysis results to various formats."""


def export_csv(results, path):
    """Write results to CSV (stub)."""
    print(f"Would write {len(results)} rows to {path}")


def export_h5ad(results, path):
    """Write results to AnnData h5ad format (stub)."""
    print(f"Would write h5ad to {path}")


if __name__ == "__main__":
    export_csv([], "output/results.csv")
''',

    # docs/
    "docs/README.md": '''\
# Spatial-Omics Analysis Pipeline

A Python toolkit for spatial transcriptomics data analysis.

## Quick Start

```bash
python -m pipelines.run_qc --config configs/pipeline_config.yaml
python -m pipelines.run_analysis --config configs/pipeline_config.yaml
```

## Features

- Quality control and filtering
- Expression normalisation
- Spatial clustering
- Cell-type annotation
- Heatmap and UMAP visualisation
''',

    "docs/architecture.md": '''\
# Architecture

## Package Layout

```
src/
  core/           Configuration, logging, exceptions
  annotation/     GO terms, confidence scoring, markers
  preprocessing/  QC, normalisation, batch correction
  analysis/       Clustering, spatial stats, trajectories
  plotting/       Heatmaps, volcano, UMAP, spatial plots
  pipelines/      End-to-end pipeline entry points
```

## Design Principles

- Each package has a clear single responsibility
- Shared types flow through `core/` re-exports
- Pipeline scripts compose preprocessing + analysis + plotting
''',

    "docs/api_reference.md": '''\
# API Reference

## core.Config

Configuration class for the pipeline.

## annotation.OntologyMapper

Maps gene IDs to Gene Ontology terms.

## preprocessing.BasePreprocessor

Abstract base for preprocessing steps.

## analysis.SpatialAnalyzer

Spatial autocorrelation and neighborhood analysis.
''',

    "docs/analysis_tutorial.md": '''\
# Analysis Tutorial

## Step 1: Load Data

Load your Visium data using the ingestion module.

## Step 2: QC

Run quality control to filter low-quality spots.

## Step 3: Clustering

Use ClusterAnalyzer to identify spatial domains.

## Step 4: Visualise

Generate heatmaps and spatial plots of your results.
''',

    # configs/
    "configs/logging_config.yaml": '''\
# Logging configuration
logging:
  level: INFO
  format: "[%(levelname)s] %(name)s: %(message)s"
  file: logs/pipeline.log
''',

    "configs/test_config.yaml": '''\
# Test suite configuration
testing:
  data_dir: tests/data/
  n_samples: 3
  seed: 42
  timeout: 60
''',

    # R/
    "R/spatial_stats.R": '''\
# Spatial statistics helper functions
# Called from Python via rpy2 bridge

morans_i <- function(expression, coords) {
  # Compute Moran's I statistic (stub)
  return(0.0)
}

getis_ord <- function(expression, coords, threshold = 0.05) {
  # Getis-Ord Gi* hotspot detection (stub)
  return(list())
}
''',

    "R/visualization.R": '''\
# R-based visualization helpers using ggplot2

library(ggplot2)

plot_spatial <- function(coords, values, title = "Spatial Plot") {
  # Generate spatial scatter plot (stub)
  cat("Would generate spatial plot:", title, "\\n")
}

plot_violin <- function(expression, groups, gene) {
  # Generate violin plot for a gene across groups (stub)
  cat("Would generate violin plot for:", gene, "\\n")
}
''',

    "R/utils.R": '''\
# Utility functions for R integration

read_expression <- function(path) {
  # Read expression matrix from CSV (stub)
  cat("Would read expression from:", path, "\\n")
  return(matrix(0, nrow = 10, ncol = 10))
}

write_results <- function(results, path) {
  # Write results to RDS file (stub)
  cat("Would write results to:", path, "\\n")
}
''',

    "R/deconvolution.R": '''\
# Cell-type deconvolution using reference profiles

deconvolve <- function(bulk_expression, reference_profiles) {
  # NNLS-based deconvolution (stub)
  n_types <- ncol(reference_profiles)
  return(rep(1 / n_types, n_types))
}

build_reference <- function(single_cell_data, cell_types) {
  # Build reference profiles from scRNA-seq (stub)
  return(matrix(0, nrow = 100, ncol = length(unique(cell_types))))
}
''',

    "R/bridge.R": '''\
# Bridge between Python pipeline and R analysis functions

run_r_analysis <- function(input_path, output_path) {
  source("R/spatial_stats.R")
  source("R/utils.R")
  expr <- read_expression(input_path)
  # Process and save results
  write_results(list(expr = expr), output_path)
}
''',

    "R/clustering.R": '''\
# R-based clustering alternatives

seurat_clustering <- function(expression, resolution = 0.8) {
  # Seurat-style graph-based clustering (stub)
  n_cells <- nrow(expression)
  return(sample(1:10, n_cells, replace = TRUE))
}
''',

    "R/preprocessing.R": '''\
# R-based preprocessing helpers

sctransform <- function(counts) {
  # SCTransform normalisation (stub)
  return(log1p(counts))
}

filter_cells <- function(counts, min_genes = 200) {
  # Filter cells by minimum gene count (stub)
  return(counts)
}
''',

    # Root-level files
    "pyproject.toml": '''\
[build-system]
requires = ["setuptools>=64"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "spatial-omics-pipeline"
version = "0.1.0"
requires-python = ">=3.10"
description = "Spatial transcriptomics analysis toolkit"
''',

    "setup.cfg": '''\
[flake8]
max-line-length = 100
exclude = .git,__pycache__,.venv

[mypy]
python_version = 3.10
warn_return_any = True
''',

    ".env.example": '''\
# Environment configuration
DATA_DIR=data/
N_THREADS=4
LOG_LEVEL=INFO
''',

    ".phoamignore": '''\
# Ignore for kb-graph scanning
.venv/
__pycache__/
*.egg-info/
data/
output/
logs/
''',

    ".gitignore": '''\
.venv/
__pycache__/
*.pyc
*.egg-info/
data/
output/
logs/
.env
''',

    "requirements.txt": '''\
numpy>=1.24
scipy>=1.10
pandas>=2.0
matplotlib>=3.7
scanpy>=1.9
anndata>=0.9
''',

    "Makefile": '''\
.PHONY: test lint qc analysis

test:
\tpython -m pytest tests/ -v

lint:
\tflake8 src/ tests/
\tmypy src/

qc:
\tpython -m pipelines.run_qc

analysis:
\tpython -m pipelines.run_analysis
''',

    "LICENSE": '''\
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction.
''',
}
```

- [ ] **Step 5: Count V3_FILES entries**

Count entries in V3_FILES — should be ~90+ files. The original fixture adds a few more (some overwritten, some remaining). Total on disk should be ~95-105.

- [ ] **Step 6: Commit**

```bash
git add tests/test_agent_experiment.py
git commit -m "feat(experiment): replace v2 fixture data with v3 bioinformatics files"
```

---

### Task 3: Update experiment constants and prompts

**Files:**
- Modify: `tests/test_agent_experiment.py` (EXPECTED_BLAST_RADIUS, PROMPT_A, PROMPT_B, MARKER, ENHANCEMENTS)

- [ ] **Step 1: Replace ENHANCEMENTS, EXPECTED_BLAST_RADIUS, MARKER, and prompts**

Remove the old `ENHANCEMENTS` dict and `EXPECTED_BLAST_RADIUS` list. Replace `MARKER`, `PROMPT_A`, `PROMPT_B` with v3 versions. Add depth-group constants for scoring.

```python
# Old files from the original fixture that must be removed from copies.
# These contain web-app imports (database.py, routes.py) that would add
# unrelated edges to the graph.
OLD_FILES_TO_REMOVE = [
    "src/core/database.py",
    "src/api/routes.py",
    "src/api/auth.py",
    "src/api/__init__.py",
    "src/main.py",
    "standalone.py",
    "config/settings.yaml",
    "docs/api-design.md",
    "docs/orphan-doc.md",
]

# Expected blast radius of src/core/metadata.py at depth 4.
# Grouped by depth for scoring breakdown.
EXPECTED_DEPTH_1 = [
    "src/core/__init__.py",
    "src/annotation/ontology.py",
    "src/annotation/confidence.py",
    "tests/test_metadata.py",
]

EXPECTED_DEPTH_2 = [
    "src/annotation/__init__.py",
    "src/annotation/markers.py",
    "src/annotation/cell_types.py",
    "src/preprocessing/base.py",
    "src/analysis/clustering.py",
]

EXPECTED_DEPTH_3 = [
    "src/preprocessing/__init__.py",
    "src/preprocessing/normalization.py",
    "src/preprocessing/qc.py",
    "src/analysis/spatial.py",
    "src/plotting/spatial_plot.py",
]

EXPECTED_DEPTH_4 = [
    "src/preprocessing/ingestion.py",
    "src/preprocessing/batch.py",
    "src/pipelines/run_qc.py",
    "src/pipelines/run_analysis.py",
    "src/plotting/heatmap.py",
]

EXPECTED_BLAST_RADIUS = EXPECTED_DEPTH_1 + EXPECTED_DEPTH_2 + EXPECTED_DEPTH_3 + EXPECTED_DEPTH_4

DEPTH_GROUPS = {
    1: set(EXPECTED_DEPTH_1),
    2: set(EXPECTED_DEPTH_2),
    3: set(EXPECTED_DEPTH_3),
    4: set(EXPECTED_DEPTH_4),
}

# Red herring files — mention "metadata" but are NOT in the blast radius
RED_HERRING_FILES = [
    "scripts/download_data.py",
    "docs/preprocessing_guide.md",
    "configs/pipeline_config.yaml",
    "tests/conftest.py",
    "src/analysis/trajectory.py",
]

# ── Agent Prompts ────────────────────────────────────────────────────

PROMPT_A = (
    "A breaking change is planned for src/core/metadata.py. Add "
    "`# AFFECTED-BY: metadata.py` as the very first line of every Python "
    "file that would be affected — include all transitive dependents. Do "
    "not modify metadata.py itself. Do not explain, just make the changes."
)

PROMPT_B = (
    "Read CLAUDE.md first. A breaking change is planned for "
    "src/core/metadata.py. Run `kb-graph traverse metadata.py --depth 4` "
    "to get the complete list of affected files. Add "
    "`# AFFECTED-BY: metadata.py` as the very first line of every file "
    "in the traverse output. Do not modify metadata.py itself. Do not "
    "explain, just make the changes."
)

MARKER = "# AFFECTED-BY: metadata.py"
```

- [ ] **Step 2: Commit**

```bash
git add tests/test_agent_experiment.py
git commit -m "feat(experiment): update v3 constants, prompts, and blast radius ground truth"
```

---

### Task 4: Update create_enhanced_project

**Files:**
- Modify: `tests/test_agent_experiment.py` — `create_enhanced_project()` function

- [ ] **Step 1: Rewrite create_enhanced_project**

Replace the old function that applies ENHANCEMENTS + NEW_FILES + NOISE_FILES with one that removes old fixture files and writes V3_FILES:

```python
def create_enhanced_project(dest):
    """Copy fixture project to dest, remove old web-app files, write v3 bioinformatics files."""
    shutil.copytree(FIXTURE_DIR, dest)

    # Remove old fixture files that don't belong in the v3 bioinformatics project
    for rel_path in OLD_FILES_TO_REMOVE:
        filepath = Path(dest) / rel_path
        if filepath.exists():
            filepath.unlink()

    # Remove empty directories left behind
    for dirpath in [Path(dest) / "src" / "api", Path(dest) / "config"]:
        if dirpath.is_dir() and not any(dirpath.iterdir()):
            dirpath.rmdir()

    # Write all v3 fixture files (overwrites existing where paths collide)
    for rel_path, content in V3_FILES.items():
        filepath = Path(dest) / rel_path
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)
```

- [ ] **Step 2: Commit**

```bash
git add tests/test_agent_experiment.py
git commit -m "refactor(experiment): update create_enhanced_project for v3 fixture"
```

---

### Task 5: Update scoring for 4-level depth breakdown

**Files:**
- Modify: `tests/test_agent_experiment.py` — `print_summary()` function

- [ ] **Step 1: Rewrite depth-bucketed miss reporting in print_summary**

Replace the old depth-1/depth-2 bucketing (which used index slicing) with the DEPTH_GROUPS dict:

```python
def print_summary(results):
    """Print a summary table of all trials."""
    expected_count = results[0]["expected_count"]
    n = len(results)

    log(f"\n{'='*70}")
    log(f"  EXPERIMENT SUMMARY — {n} trial(s), {expected_count} expected blast radius files")
    log(f"{'='*70}\n")

    # Per-trial table
    log(f"  {'Trial':>5}  {'A recall':>8}  {'B recall':>8}  {'A prec':>7}  {'B prec':>7}  {'A time':>8}  {'B time':>8}")
    log(f"  {'-'*5}  {'-'*8}  {'-'*8}  {'-'*7}  {'-'*7}  {'-'*8}  {'-'*8}")
    for r in results:
        a = r["agent_a"]
        b = r["agent_b"]
        log(f"  {r['trial']:>5}  {a['recall']:>7.0%}  {b['recall']:>7.0%}  {a['precision']:>6.0%}  {b['precision']:>6.0%}  {a['elapsed']:>7.1f}s  {b['elapsed']:>7.1f}s")

    # Aggregates
    a_recalls = [r["agent_a"]["recall"] for r in results]
    b_recalls = [r["agent_b"]["recall"] for r in results]
    a_precisions = [r["agent_a"]["precision"] for r in results]
    b_precisions = [r["agent_b"]["precision"] for r in results]
    a_times = [r["agent_a"]["elapsed"] for r in results]
    b_times = [r["agent_b"]["elapsed"] for r in results]
    a_perfect = sum(1 for r in results if r["agent_a"]["perfect"])
    b_perfect = sum(1 for r in results if r["agent_b"]["perfect"])

    log(f"\n  Perfect runs (recall=100%): Agent A = {a_perfect}/{n} ({a_perfect/n*100:.0f}%), Agent B = {b_perfect}/{n} ({b_perfect/n*100:.0f}%)")
    log(f"  Avg recall:                Agent A = {sum(a_recalls)/n:.0%}, Agent B = {sum(b_recalls)/n:.0%}")
    log(f"  Avg precision:             Agent A = {sum(a_precisions)/n:.0%}, Agent B = {sum(b_precisions)/n:.0%}")
    log(f"  Avg time:                  Agent A = {sum(a_times)/n:.1f}s, Agent B = {sum(b_times)/n:.1f}s")

    # Files most commonly missed — grouped by depth
    a_miss_counts = {}
    b_miss_counts = {}
    for r in results:
        for f in r["agent_a"]["misses"]:
            a_miss_counts[f] = a_miss_counts.get(f, 0) + 1
        for f in r["agent_b"]["misses"]:
            b_miss_counts[f] = b_miss_counts.get(f, 0) + 1

    if a_miss_counts or b_miss_counts:
        all_missed = sorted(set(list(a_miss_counts.keys()) + list(b_miss_counts.keys())))

        for depth in (1, 2, 3, 4):
            depth_set = DEPTH_GROUPS[depth]
            missed_at_depth = [f for f in all_missed if f in depth_set]
            if missed_at_depth:
                greppable = " (greppable)" if depth == 1 else " (NOT greppable)"
                log(f"\n  Depth-{depth} files missed{greppable}:")
                for f in missed_at_depth:
                    a_n = a_miss_counts.get(f, 0)
                    b_n = b_miss_counts.get(f, 0)
                    log(f"    {f}: Agent A = {a_n}/{n}, Agent B = {b_n}/{n}")

    # False positives
    a_fp_counts = {}
    b_fp_counts = {}
    for r in results:
        for f in r["agent_a"]["false_positives"]:
            a_fp_counts[f] = a_fp_counts.get(f, 0) + 1
        for f in r["agent_b"]["false_positives"]:
            b_fp_counts[f] = b_fp_counts.get(f, 0) + 1

    if a_fp_counts or b_fp_counts:
        log(f"\n  False positives (marked but not in blast radius):")
        all_fps = sorted(set(list(a_fp_counts.keys()) + list(b_fp_counts.keys())))
        for f in all_fps:
            a_n = a_fp_counts.get(f, 0)
            b_n = b_fp_counts.get(f, 0)
            log(f"    {f}: Agent A = {a_n}/{n}, Agent B = {b_n}/{n}")

    # Verdict
    log(f"\n  Verdict:")
    a_avg_recall = sum(a_recalls) / n
    b_avg_recall = sum(b_recalls) / n
    if b_avg_recall > a_avg_recall:
        log(f"  -> Agent B (with kb-graph) achieved {b_avg_recall:.0%} avg recall vs Agent A's {a_avg_recall:.0%}.")
        if b_perfect > a_perfect:
            log(f"  -> Agent B had {b_perfect}/{n} perfect runs vs Agent A's {a_perfect}/{n}.")
    elif b_avg_recall == a_avg_recall:
        log(f"  -> Both agents achieved equal recall ({a_avg_recall:.0%}).")
    else:
        log(f"  -> Agent A outperformed Agent B — unexpected result.")

    return {
        "trials": n,
        "expected_count": expected_count,
        "a_perfect": a_perfect,
        "b_perfect": b_perfect,
        "a_avg_recall": a_avg_recall,
        "b_avg_recall": b_avg_recall,
        "a_avg_precision": sum(a_precisions) / n,
        "b_avg_precision": sum(b_precisions) / n,
        "a_avg_time": sum(a_times) / n,
        "b_avg_time": sum(b_times) / n,
        "a_miss_files": a_miss_counts,
        "b_miss_files": b_miss_counts,
    }
```

- [ ] **Step 2: Commit**

```bash
git add tests/test_agent_experiment.py
git commit -m "feat(experiment): 4-level depth miss breakdown in summary"
```

---

### Task 6: Update CLI args, timeout, run_trial, and dry-run validation

**Files:**
- Modify: `tests/test_agent_experiment.py` — `main()`, `run_trial()` functions

- [ ] **Step 1: Add --depth arg and increase default timeout**

In `main()`, add a `--depth` argument and change default timeout from 180 to 300:

```python
    parser.add_argument(
        "--depth", type=int, default=4,
        help="Max depth for kb-graph traverse (default: 4)",
    )
    # ... existing --timeout arg:
    parser.add_argument(
        "--timeout", type=int, default=300,
        help="Timeout per agent in seconds (default: 300)",
    )
```

- [ ] **Step 2: Update run_trial to use traverse target "metadata.py"**

In `run_trial()`, update the logging to reference the new fixture stats:

```python
    log(f"  Expected blast radius: {len(EXPECTED_BLAST_RADIUS)} files")
    log(f"  Fixture files: {len(V3_FILES)}")
```

Also update the traverse file in Agent B's prompt template if it's dynamically constructed (in current code it's a static string, so this is already handled by PROMPT_B update in Task 3).

- [ ] **Step 3: Rewrite --dry-run block for v3 validation**

Replace the dry-run section in `main()` with validation that:
1. Counts total fixture files
2. Verifies all 19 expected blast radius files exist
3. Verifies all 5 red herring files exist
4. Runs `kb-graph traverse metadata.py --depth 4`
5. Asserts traverse output matches EXPECTED_BLAST_RADIUS exactly
6. Asserts red herring files are NOT in traverse output

```python
    if args.dry_run:
        tmpdir = tempfile.mkdtemp(prefix="kb_graph_ab_dry_")
        project = os.path.join(tmpdir, "project")
        create_enhanced_project(project)
        total_files = count_project_files(project)
        log(f"\n  Dry run — v3 bioinformatics fixture: {total_files} files total")

        # Verify all expected blast radius files exist
        log(f"\n  Expected blast radius ({len(EXPECTED_BLAST_RADIUS)} files):")
        all_exist = True
        for depth, files in [(1, EXPECTED_DEPTH_1), (2, EXPECTED_DEPTH_2),
                             (3, EXPECTED_DEPTH_3), (4, EXPECTED_DEPTH_4)]:
            for rel_path in files:
                exists = (Path(project) / rel_path).exists()
                status = "OK" if exists else "MISSING"
                log(f"    [{status}] {rel_path} (depth-{depth})")
                if not exists:
                    all_exist = False

        # Verify red herring files exist
        log(f"\n  Red herring files ({len(RED_HERRING_FILES)}):")
        for rel_path in RED_HERRING_FILES:
            exists = (Path(project) / rel_path).exists()
            status = "OK" if exists else "MISSING"
            log(f"    [{status}] {rel_path}")
            if not exists:
                all_exist = False

        if not all_exist:
            log("\n  ERROR: Some expected files are missing!")
            shutil.rmtree(tmpdir, ignore_errors=True)
            return

        # Init graph and run traverse to validate ground truth
        log(f"\n  Testing kb-graph init + traverse...")
        if not init_graph(project):
            log("  ERROR: kb-graph init failed")
            shutil.rmtree(tmpdir, ignore_errors=True)
            return

        log("  kb-graph init succeeded")
        depth = args.depth
        result = subprocess.run(
            ["kb-graph", "traverse", "metadata.py", "--depth", str(depth)],
            cwd=project,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            log(f"  ERROR: traverse failed: {result.stderr}")
            shutil.rmtree(tmpdir, ignore_errors=True)
            return

        log(f"\n  kb-graph traverse metadata.py --depth {depth}:")
        for line in result.stdout.strip().splitlines():
            log(f"    {line}")

        # Parse traverse output for file paths
        traverse_output = result.stdout
        found_files = set()
        for line in traverse_output.splitlines():
            # Lines containing file paths look like: "  ├── src/core/__init__.py ── ..."
            match = re.search(r"(src/\S+\.py|tests/\S+\.py|scripts/\S+\.py)", line)
            if match:
                found_files.add(match.group(1))

        # Validate ground truth: every expected file should be in traverse output
        log(f"\n  Ground truth validation ({len(EXPECTED_BLAST_RADIUS)} expected):")
        expected_set = set(EXPECTED_BLAST_RADIUS)
        match_count = 0
        for rel_path in EXPECTED_BLAST_RADIUS:
            found = rel_path in found_files
            status = "FOUND" if found else "NOT IN OUTPUT"
            log(f"    [{status}] {rel_path}")
            if found:
                match_count += 1

        # Validate red herrings are NOT in output
        log(f"\n  Red herring validation (should NOT appear in traverse):")
        red_herring_ok = True
        for rel_path in RED_HERRING_FILES:
            found = rel_path in found_files
            status = "ABSENT (good)" if not found else "FOUND (BAD!)"
            log(f"    [{status}] {rel_path}")
            if found:
                red_herring_ok = False

        # Summary
        log(f"\n  Results: {match_count}/{len(EXPECTED_BLAST_RADIUS)} expected files found in traverse output")
        if match_count == len(EXPECTED_BLAST_RADIUS) and red_herring_ok:
            log("  PASS — ground truth matches traverse output perfectly")
        else:
            extra = found_files - expected_set
            missing = expected_set - found_files
            if missing:
                log(f"  FAIL — missing from traverse: {sorted(missing)}")
            if extra:
                log(f"  NOTE — extra in traverse (not in expected): {sorted(extra)}")
            if not red_herring_ok:
                log(f"  FAIL — red herring files appeared in traverse output")

        shutil.rmtree(tmpdir, ignore_errors=True)
        return
```

- [ ] **Step 4: Update docstring and module header**

Replace the module docstring (lines 2-30) with v3 description:

```python
"""Phase 5 v3: Agent A/B Experiment — Blast Radius Marking

Proves that kb-graph helps a Claude agent identify transitive dependencies
that are invisible to grep. Two Claude Code agents get the same task: mark
every file in the blast radius of metadata.py with a comment. Agent A has no
graph tooling; Agent B has KB_INDEX.md, kb-graph traverse, and CLAUDE.md rules.

The bioinformatics fixture has ~100 files with 19 in the blast radius of
src/core/metadata.py (4 at depth 1 — greppable, 15 at depth 2-4 — invisible
to grep). Import chains go through __init__.py re-exports, making manual
tracing unreliable.

Requirements:
    - Claude Code CLI (`claude` command on PATH)
    - API access configured (ANTHROPIC_API_KEY or OAuth)
    - kb-graph installed (`kb-graph` on PATH)

Usage:
    python3 tests/test_agent_experiment.py                  # 1 trial, default model
    python3 tests/test_agent_experiment.py --trials 3       # 3 trials
    python3 tests/test_agent_experiment.py --model sonnet   # use sonnet
    python3 tests/test_agent_experiment.py --save-transcripts  # keep agent output
    python3 tests/test_agent_experiment.py --clean          # wipe previous results first
    python3 tests/test_agent_experiment.py --dry-run        # validate fixture + blast radius
    python3 tests/test_agent_experiment.py --depth 3        # limit traverse depth

Results are printed as a table and can be appended to phoam_paint/README.md.
"""
```

- [ ] **Step 5: Update results JSON metadata**

In the `main()` results-saving block, change `total_project_files` calculation:

```python
            "meta": {
                "started_at": started_at,
                "claude_version": claude_version,
                "model": model_id,
                "task_type": "blast-radius-marking",
                "fixture_version": "v3-bioinformatics",
                "total_fixture_files": len(V3_FILES),
                "expected_blast_radius": EXPECTED_BLAST_RADIUS,
                "expected_blast_radius_count": len(EXPECTED_BLAST_RADIUS),
                "depth_groups": {str(d): list(files) for d, files in DEPTH_GROUPS.items()},
            },
```

- [ ] **Step 6: Commit**

```bash
git add tests/test_agent_experiment.py
git commit -m "feat(experiment): v3 dry-run validation, --depth arg, 300s timeout"
```

---

### Task 7: Validate with --dry-run in WSL

**Files:** None modified — validation only.

- [ ] **Step 1: Run --dry-run**

```bash
cd /mnt/c/Users/mcap9/projects/bioinfo-agent-toolkit
python3 tests/test_agent_experiment.py --dry-run
```

**Expected output:**
- `~95-105 files total`
- All 19 blast radius files: `[OK]`
- All 5 red herring files: `[OK]`
- kb-graph init succeeded
- Traverse output shows 19 files at depths 1-4
- Ground truth: `19/19 expected files found`
- Red herrings: all `ABSENT (good)`
- Final: `PASS — ground truth matches traverse output perfectly`

- [ ] **Step 2: If FAIL, debug and fix**

Common issues:
- Import doesn't resolve: check the import statement against `resolve_module()` logic
- File missing: check V3_FILES key path matches EXPECTED_BLAST_RADIUS entry
- Red herring in output: check that the file doesn't accidentally import from the metadata chain
- Old fixture file interfering: check OLD_FILES_TO_REMOVE list

---

### Task 8: Update docs/phoam_paint/plan.md

**Files:**
- Modify: `docs/phoam_paint/plan.md`

- [ ] **Step 1: Add Phase 5 v3 subsection**

Add after the existing Phase 5 v2 section:

```markdown
### Phase 5 v3 — Bioinformatics fixture redesign (2026-04-14)

**Problem**: v2 produced identical 80% recall for both agents. The 46-file
web-app fixture was too small with shallow (depth 2) import chains.

**Solution**: Replaced with a ~100-file bioinformatics fixture:
- Target: `src/core/metadata.py` (central utility with high fan-out)
- 19 files in blast radius across depths 1-4
- Import chains through `__init__.py` re-exports (not direct imports)
- 5 red herring files mention "metadata" but aren't dependents
- Only 4 of 19 blast radius files are greppable (depth 1)

**Changes**:
- `tests/test_agent_experiment.py` — full fixture rewrite, 4-level depth
  scoring, --depth CLI arg, 300s timeout, red herring validation
- Agent prompts updated for metadata.py target + `kb-graph traverse`

**Dry-run result**: [PASS/FAIL — fill in after Task 7]

**Status**: Ready for experiment runs
```

- [ ] **Step 2: Commit**

```bash
git add docs/phoam_paint/plan.md
git commit -m "docs: add Phase 5 v3 subsection to plan"
```
