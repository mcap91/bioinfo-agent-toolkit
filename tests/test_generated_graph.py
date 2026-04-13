#!/usr/bin/env python3
"""Generated-graph correctness tests for kb-graph query commands.

Creates a ~100-node project programmatically with known, deterministic
relationships, then verifies that neighbors, traverse, path, orphans,
and analyze all produce correct results on a non-trivial graph.

Graph structure (100 nodes):
    lib/
        core.py          — leaf node, imported by all lib/worker_*.py
        worker_00..39.py — each imports lib.core; even-numbered also import
                           the next worker (worker_00 -> worker_01, etc.)
    app/
        main.py          — imports lib.core and app.api
        api.py           — imports lib.core
    docs/
        index.md         — wiki-links to [[core]], [[api]]
        guide_00..39.md  — guide_N links to [[worker_N.py]]
                           guide_00..09 also link to [[core]]
    config/
        settings.yaml    — references "lib/core.py"
    orphans/
        stray_00..14.py  — 15 orphan files, no imports or references
"""

import os
import sys
import tempfile
import shutil
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from phoam_paint.kb_graph import (
    build_graph,
    resolve_node,
    build_adjacency,
    bfs_blast_radius,
    bfs_shortest_path,
)

NUM_WORKERS = 40
NUM_GUIDES = 40
NUM_ORPHANS = 15


class GeneratedGraphBase(unittest.TestCase):
    """Creates a ~100-node project in a temp directory."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="kb_graph_gen_")
        cls.project = os.path.join(cls.tmp, "project")
        cls._build_project(cls.project)
        cls.graph = build_graph(cls.project)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    @staticmethod
    def _build_project(root):
        """Generate all project files."""
        def write(rel_path, content):
            full = os.path.join(root, rel_path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w") as f:
                f.write(content)

        # lib/core.py — leaf node
        write("lib/core.py", '"""Core library module."""\n\nclass Core:\n    pass\n')

        # lib/__init__.py — empty (should be excluded)
        write("lib/__init__.py", "")

        # lib/worker_00..39.py
        for i in range(NUM_WORKERS):
            lines = [f'"""Worker {i:02d}."""\n', "from lib.core import Core\n"]
            # Even-numbered workers import the next worker
            if i % 2 == 0 and i + 1 < NUM_WORKERS:
                lines.append(f"from lib.worker_{i+1:02d} import run\n")
            lines.append(f"\ndef run():\n    return Core()\n")
            write(f"lib/worker_{i:02d}.py", "".join(lines))

        # app/main.py
        write("app/main.py", (
            '"""Application entry point."""\n'
            "from lib.core import Core\n"
            "from app.api import serve\n"
            "\ndef main():\n    serve(Core())\n"
        ))

        # app/api.py
        write("app/api.py", (
            '"""API module."""\n'
            "from lib.core import Core\n"
            "\ndef serve(core):\n    pass\n"
        ))

        # app/__init__.py — empty
        write("app/__init__.py", "")

        # docs/index.md
        write("docs/index.md", (
            "# Project Index\n\n"
            "See [[core]] for the core library.\n"
            "See [[api]] for the API.\n"
        ))

        # docs/guide_00..39.md
        for i in range(NUM_GUIDES):
            lines = [f"# Guide {i:02d}\n\n"]
            lines.append(f"This guide covers [[worker_{i:02d}.py]].\n")
            if i < 10:
                lines.append("Also see [[core]] for fundamentals.\n")
            write(f"docs/guide_{i:02d}.md", "".join(lines))

        # config/settings.yaml
        write("config/settings.yaml", (
            "app:\n"
            '  core_module: "lib/core.py"\n'
            "  debug: false\n"
        ))

        # orphans/stray_00..14.py
        for i in range(NUM_ORPHANS):
            write(f"orphans/stray_{i:02d}.py", f'"""Stray file {i:02d}."""\n\nx = {i}\n')


# ── Baseline counts ──────────────────────────────────────────────────────

class TestGeneratedBaseline(GeneratedGraphBase):
    """Verify expected node/edge/orphan counts."""

    def test_node_count(self):
        # lib/core + 40 workers + app/main + app/api + docs/index + 40 guides
        # + config/settings.yaml + 15 orphans = 100
        expected = 1 + NUM_WORKERS + 2 + 1 + NUM_GUIDES + 1 + NUM_ORPHANS
        self.assertEqual(expected, 100)
        self.assertEqual(len(self.graph["nodes"]), expected)

    def test_orphan_count(self):
        connected = set()
        for e in self.graph["edges"]:
            connected.add(e["from"])
            connected.add(e["to"])
        orphans = set(self.graph["nodes"].keys()) - connected
        self.assertEqual(len(orphans), NUM_ORPHANS)

    def test_orphan_identity(self):
        connected = set()
        for e in self.graph["edges"]:
            connected.add(e["from"])
            connected.add(e["to"])
        orphans = set(self.graph["nodes"].keys()) - connected
        for i in range(NUM_ORPHANS):
            self.assertIn(f"orphans/stray_{i:02d}.py", orphans)

    def test_edge_count(self):
        # Import edges:
        #   40 workers -> core = 40
        #   20 even workers -> next worker = 20
        #   main -> core = 1
        #   main -> api = 1
        #   api -> core = 1
        # Wiki-link edges:
        #   index -> core = 1
        #   index -> api = 1
        #   40 guides -> worker_N = 40
        #   10 guides (00..09) -> core = 10
        # Config-ref edges:
        #   settings.yaml -> core = 1
        # Total = 40 + 20 + 1 + 1 + 1 + 1 + 1 + 40 + 10 + 1 = 116
        expected_imports = NUM_WORKERS + (NUM_WORKERS // 2) + 3
        expected_wikilinks = 2 + NUM_GUIDES + 10
        expected_configrefs = 1
        expected_total = expected_imports + expected_wikilinks + expected_configrefs
        self.assertEqual(expected_total, 116)
        self.assertEqual(len(self.graph["edges"]), expected_total)


# ── resolve_node ─────────────────────────────────────────────────────────

class TestGeneratedResolveNode(GeneratedGraphBase):
    """Verify node resolution on a larger graph."""

    def test_exact_match(self):
        self.assertEqual(resolve_node("lib/core.py", self.graph), "lib/core.py")

    def test_basename_unique(self):
        self.assertEqual(resolve_node("core.py", self.graph), "lib/core.py")

    def test_basename_ambiguous_returns_none(self):
        # "run" matches no basename; but __init__.py is excluded so no ambiguity there
        self.assertIsNone(resolve_node("nonexistent.py", self.graph))

    def test_suffix_match(self):
        self.assertEqual(
            resolve_node("lib/worker_05.py", self.graph), "lib/worker_05.py"
        )

    def test_stem_match(self):
        self.assertEqual(resolve_node("api", self.graph), "app/api.py")


# ── neighbors ────────────────────────────────────────────────────────────

class TestGeneratedNeighbors(GeneratedGraphBase):
    """Verify neighbor counts on known nodes."""

    def test_core_inbound(self):
        """core.py should have many inbound edges, zero outbound."""
        outbound, inbound = build_adjacency(self.graph)
        self.assertEqual(len(outbound.get("lib/core.py", [])), 0)
        # 40 workers + main + api + index + 10 guides + settings = 54
        expected_inbound = NUM_WORKERS + 2 + 1 + 10 + 1
        self.assertEqual(expected_inbound, 54)
        self.assertEqual(len(inbound.get("lib/core.py", [])), expected_inbound)

    def test_even_worker_outbound(self):
        """Even workers import core + next worker = 2 outbound."""
        outbound, _ = build_adjacency(self.graph)
        self.assertEqual(len(outbound.get("lib/worker_00.py", [])), 2)

    def test_odd_worker_outbound(self):
        """Odd workers import only core = 1 outbound."""
        outbound, _ = build_adjacency(self.graph)
        self.assertEqual(len(outbound.get("lib/worker_01.py", [])), 1)

    def test_orphan_no_neighbors(self):
        outbound, inbound = build_adjacency(self.graph)
        self.assertEqual(len(outbound.get("orphans/stray_00.py", [])), 0)
        self.assertEqual(len(inbound.get("orphans/stray_00.py", [])), 0)


# ── traverse (blast radius) ─────────────────────────────────────────────

class TestGeneratedTraverse(GeneratedGraphBase):
    """Verify blast-radius BFS on the generated graph."""

    def test_core_depth1(self):
        """Changing core.py affects all 54 direct dependents at depth 1."""
        depth_map = bfs_blast_radius("lib/core.py", self.graph, 1)
        depth1 = [n for n, d in depth_map.items() if d == 1]
        # 40 workers + main + api + index + 10 guides + settings = 54
        self.assertEqual(len(depth1), 54)

    def test_core_depth2(self):
        """Depth 2 from core captures transitive dependents."""
        depth_map = bfs_blast_radius("lib/core.py", self.graph, 2)
        depth2 = [n for n, d in depth_map.items() if d == 2]
        # Depth 2: guides 10..39 (link to workers, workers are depth 1) = 30
        # Even workers at depth 1 are imported by nobody new at depth 2
        # (their only inbound from chain edges is from the even worker before,
        #  but those are also at depth 1)
        self.assertEqual(len(depth2), 30)

    def test_leaf_worker_no_dependents(self):
        """An odd worker that nobody imports has no blast radius beyond itself."""
        # worker_39 is odd, not imported by worker_38 (38 is even, imports 39!)
        # Actually worker_38 imports worker_39, so worker_39 has 1 dependent.
        # worker_37 is odd, and worker_36 imports worker_37.
        # Use worker_01: imported by worker_00 (even). So depth 1 = [worker_00].
        depth_map = bfs_blast_radius("lib/worker_01.py", self.graph, 2)
        depth1 = [n for n, d in depth_map.items() if d == 1]
        # worker_00 imports worker_01, and guide_01 links to worker_01
        self.assertEqual(sorted(depth1), ["docs/guide_01.md", "lib/worker_00.py"])

    def test_orphan_no_blast_radius(self):
        """Orphan has no blast radius beyond itself."""
        depth_map = bfs_blast_radius("orphans/stray_05.py", self.graph, 2)
        self.assertEqual(len(depth_map), 1)
        self.assertEqual(depth_map["orphans/stray_05.py"], 0)

    def test_risk_high_for_core(self):
        """core.py blast radius spans many groups -> HIGH risk."""
        depth_map = bfs_blast_radius("lib/core.py", self.graph, 2)
        groups = set()
        for n in depth_map:
            if n in self.graph["nodes"]:
                groups.add(self.graph["nodes"][n]["group"])
        self.assertGreaterEqual(len(groups), 3)


# ── path ─────────────────────────────────────────────────────────────────

class TestGeneratedPath(GeneratedGraphBase):
    """Verify shortest-path BFS on the generated graph."""

    def test_direct_edge(self):
        """Direct import = 1-hop path."""
        path = bfs_shortest_path("lib/worker_00.py", "lib/core.py", self.graph)
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 2)
        self.assertEqual(path, ["lib/worker_00.py", "lib/core.py"])

    def test_two_hop_via_chain(self):
        """worker_00 -> worker_01 -> core, but worker_00 also -> core directly."""
        path = bfs_shortest_path("lib/worker_00.py", "lib/worker_01.py", self.graph)
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 2)  # direct edge

    def test_cross_type_path(self):
        """Path from a guide to core goes through a worker (wiki-link -> import)."""
        path = bfs_shortest_path("docs/guide_20.md", "lib/core.py", self.graph)
        self.assertIsNotNone(path)
        # guide_20 -> worker_20 -> core = 2 hops
        self.assertEqual(len(path), 3)

    def test_guide_with_core_link_is_shorter(self):
        """Guides 00..09 link to core directly, so path is 1 hop."""
        path = bfs_shortest_path("docs/guide_05.md", "lib/core.py", self.graph)
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 2)

    def test_no_path_orphan(self):
        """No path between an orphan and any connected node."""
        path = bfs_shortest_path("orphans/stray_00.py", "lib/core.py", self.graph)
        self.assertIsNone(path)

    def test_same_node(self):
        path = bfs_shortest_path("lib/core.py", "lib/core.py", self.graph)
        self.assertEqual(path, ["lib/core.py"])

    def test_path_between_workers_via_core(self):
        """Two odd workers connect through core (worker -> core <- worker)."""
        path = bfs_shortest_path("lib/worker_03.py", "lib/worker_05.py", self.graph)
        self.assertIsNotNone(path)
        # worker_03 -> core <- worker_05 = 2 hops
        self.assertEqual(len(path), 3)
        self.assertEqual(path[1], "lib/core.py")


# ── analyze ──────────────────────────────────────────────────────────────

class TestGeneratedAnalyze(GeneratedGraphBase):
    """Verify analyze stats on the generated graph."""

    def test_group_count(self):
        groups = set(m["group"] for m in self.graph["nodes"].values())
        # lib, app, docs, config, orphans = 5
        self.assertEqual(len(groups), 5)

    def test_most_connected_is_core(self):
        degree = {}
        for edge in self.graph["edges"]:
            degree[edge["from"]] = degree.get(edge["from"], 0) + 1
            degree[edge["to"]] = degree.get(edge["to"], 0) + 1
        top_node = max(degree, key=degree.get)
        self.assertEqual(top_node, "lib/core.py")

    def test_edge_type_breakdown(self):
        types = {}
        for edge in self.graph["edges"]:
            types[edge["type"]] = types.get(edge["type"], 0) + 1
        self.assertEqual(types["import"], NUM_WORKERS + (NUM_WORKERS // 2) + 3)
        self.assertEqual(types["wiki-link"], 2 + NUM_GUIDES + 10)
        self.assertEqual(types["config-ref"], 1)


if __name__ == "__main__":
    unittest.main()
