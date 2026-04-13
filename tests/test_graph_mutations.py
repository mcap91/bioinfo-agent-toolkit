#!/usr/bin/env python3
"""Phase 1.5 — Mutation tests for kb-graph rebuild.

Verifies that build_graph correctly detects graph changes when files are
added, modified, or ignored. Each test copies the fixture project to a
temp directory, mutates it, rebuilds, and asserts the delta.
"""

import os
import shutil
import sys
import tempfile
import unittest

# Make the repo root importable so we can reach phoam_paint.kb_graph
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from phoam_paint.kb_graph import build_graph, write_kb_index, write_graph_html

FIXTURE_DIR = os.path.join(REPO_ROOT, "tests", "fixtures", "sample_project")


class MutationTestBase(unittest.TestCase):
    """Base class that copies the fixture project into a temp directory."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="kb_graph_test_")
        self.project = os.path.join(self.tmp, "project")
        shutil.copytree(FIXTURE_DIR, self.project)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def rebuild(self):
        """Build the graph and return it."""
        return build_graph(self.project)

    # ── helpers ────────────────────────────────────────────────────────

    def node_count(self, graph):
        return len(graph["nodes"])

    def edge_count(self, graph):
        return len(graph["edges"])

    def orphan_count(self, graph):
        connected = set()
        for e in graph["edges"]:
            connected.add(e["from"])
            connected.add(e["to"])
        return len(set(graph["nodes"].keys()) - connected)

    def has_edge(self, graph, src, dst, edge_type=None):
        """True if an edge from src to dst exists (optionally filtered by type)."""
        for e in graph["edges"]:
            if e["from"] == src and e["to"] == dst:
                if edge_type is None or e["type"] == edge_type:
                    return True
        return False

    def edges_involving(self, graph, node):
        """Return all edges where node is source or target."""
        return [
            e for e in graph["edges"]
            if e["from"] == node or e["to"] == node
        ]

    def write_file(self, rel_path, content):
        """Write a file into the temp project."""
        full = os.path.join(self.project, rel_path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            f.write(content)

    def read_file(self, rel_path):
        """Read a file from the temp project."""
        with open(os.path.join(self.project, rel_path)) as f:
            return f.read()

    def delete_file(self, rel_path):
        """Delete a file from the temp project."""
        os.remove(os.path.join(self.project, rel_path))


class TestBaseline(MutationTestBase):
    """Verify the fixture project produces the expected baseline graph."""

    def test_baseline_counts(self):
        g = self.rebuild()
        self.assertEqual(self.node_count(g), 10, f"nodes: {sorted(g['nodes'].keys())}")
        self.assertEqual(self.edge_count(g), 13, f"edges: {g['edges']}")
        self.assertEqual(self.orphan_count(g), 2)

    def test_baseline_orphans(self):
        g = self.rebuild()
        connected = set()
        for e in g["edges"]:
            connected.add(e["from"])
            connected.add(e["to"])
        orphans = set(g["nodes"].keys()) - connected
        self.assertIn("standalone.py", orphans)
        self.assertIn("docs/orphan-doc.md", orphans)

    def test_baseline_import_edges(self):
        g = self.rebuild()
        # main.py imports
        self.assertTrue(self.has_edge(g, "src/main.py", "src/core/config.py", "import"))
        self.assertTrue(self.has_edge(g, "src/main.py", "src/api/routes.py", "import"))
        # database.py imports config
        self.assertTrue(self.has_edge(g, "src/core/database.py", "src/core/config.py", "import"))
        # routes.py imports
        self.assertTrue(self.has_edge(g, "src/api/routes.py", "src/core/database.py", "import"))
        self.assertTrue(self.has_edge(g, "src/api/routes.py", "src/core/config.py", "import"))
        self.assertTrue(self.has_edge(g, "src/api/routes.py", "src/api/auth.py", "import"))
        # auth.py imports database
        self.assertTrue(self.has_edge(g, "src/api/auth.py", "src/core/database.py", "import"))

    def test_baseline_wikilink_edges(self):
        g = self.rebuild()
        self.assertTrue(self.has_edge(g, "docs/README.md", "docs/api-design.md", "wiki-link"))
        self.assertTrue(self.has_edge(g, "docs/README.md", "src/core/config.py", "wiki-link"))
        self.assertTrue(self.has_edge(g, "docs/api-design.md", "src/api/routes.py", "wiki-link"))
        self.assertTrue(self.has_edge(g, "docs/api-design.md", "src/api/auth.py", "wiki-link"))
        self.assertTrue(self.has_edge(g, "docs/api-design.md", "src/core/database.py", "wiki-link"))

    def test_baseline_config_edge(self):
        g = self.rebuild()
        self.assertTrue(self.has_edge(g, "config/settings.yaml", "src/core/config.py", "config-ref"))

    def test_baseline_most_connected(self):
        """config.py should have the most edges (5 total)."""
        g = self.rebuild()
        edges = self.edges_involving(g, "src/core/config.py")
        self.assertEqual(len(edges), 5)

    def test_kb_index_generated(self):
        g = self.rebuild()
        path = write_kb_index(g, self.project)
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
        self.assertIn("Nodes: 10", content)
        self.assertIn("Edges: 13", content)
        self.assertIn("Orphans: 2", content)

    def test_graph_html_generated(self):
        g = self.rebuild()
        path = write_graph_html(g, self.project)
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
        self.assertIn("d3.v7", content)
        self.assertIn("#0d1117", content)


class TestAddFile(MutationTestBase):
    """Adding a new Python file with imports creates new node + edges."""

    def test_add_python_file_with_imports(self):
        self.write_file("src/api/middleware.py", (
            '"""Request middleware."""\n'
            'from core.config import Config\n'
            'from .auth import verify_token\n'
            '\n'
            'def require_auth(handler):\n'
            '    pass\n'
        ))

        g = self.rebuild()

        # New node exists
        self.assertIn("src/api/middleware.py", g["nodes"])
        self.assertEqual(self.node_count(g), 11)

        # New edges from the imports
        self.assertTrue(self.has_edge(g, "src/api/middleware.py", "src/core/config.py", "import"))
        self.assertTrue(self.has_edge(g, "src/api/middleware.py", "src/api/auth.py", "import"))

        # Total edges increased by 2
        self.assertEqual(self.edge_count(g), 15)

        # Orphan count unchanged (new file is connected)
        self.assertEqual(self.orphan_count(g), 2)


class TestRemoveImport(MutationTestBase):
    """Removing an import line removes the corresponding edge."""

    def test_remove_import_drops_edge(self):
        # routes.py imports: core.database, core.config, .auth
        # Remove the config import
        original = self.read_file("src/api/routes.py")
        modified = original.replace("from core.config import Config\n", "")
        self.write_file("src/api/routes.py", modified)

        g = self.rebuild()

        # Edge from routes → config should be gone
        self.assertFalse(self.has_edge(g, "src/api/routes.py", "src/core/config.py", "import"))

        # Other routes edges still present
        self.assertTrue(self.has_edge(g, "src/api/routes.py", "src/core/database.py", "import"))
        self.assertTrue(self.has_edge(g, "src/api/routes.py", "src/api/auth.py", "import"))

        # Total edges decreased by 1
        self.assertEqual(self.edge_count(g), 12)

        # Node count unchanged (config.py still has other connections)
        self.assertEqual(self.node_count(g), 10)


class TestAddWikiLink(MutationTestBase):
    """Adding a wiki-link to a markdown file creates a cross-type edge."""

    def test_add_wikilink_creates_edge(self):
        original = self.read_file("docs/orphan-doc.md")
        modified = original + "\nSee also: [[routes.py]] for the API.\n"
        self.write_file("docs/orphan-doc.md", modified)

        g = self.rebuild()

        # New edge from orphan-doc to routes
        self.assertTrue(self.has_edge(g, "docs/orphan-doc.md", "src/api/routes.py", "wiki-link"))

        # orphan-doc is no longer an orphan
        self.assertEqual(self.orphan_count(g), 1)

        # Edge count increased by 1
        self.assertEqual(self.edge_count(g), 14)

    def test_add_wikilink_with_section(self):
        original = self.read_file("docs/orphan-doc.md")
        modified = original + "\nSee [[api-design#endpoints]] for details.\n"
        self.write_file("docs/orphan-doc.md", modified)

        g = self.rebuild()

        # Edge exists with section metadata
        matching = [
            e for e in g["edges"]
            if e["from"] == "docs/orphan-doc.md"
            and e["to"] == "docs/api-design.md"
            and e["type"] == "wiki-link"
        ]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0]["section"], "endpoints")


class TestAddOrphan(MutationTestBase):
    """Creating a new file with no connections increases orphan count."""

    def test_new_orphan_python(self):
        self.write_file("scratch.py", '"""A scratch file."""\n\ndef foo():\n    return 1\n')

        g = self.rebuild()

        self.assertIn("scratch.py", g["nodes"])
        self.assertEqual(self.node_count(g), 11)
        self.assertEqual(self.orphan_count(g), 3)
        # Edge count unchanged
        self.assertEqual(self.edge_count(g), 13)

    def test_new_orphan_markdown(self):
        self.write_file("docs/notes.md", "# Notes\n\nJust some notes.\n")

        g = self.rebuild()

        self.assertIn("docs/notes.md", g["nodes"])
        self.assertEqual(self.node_count(g), 11)
        self.assertEqual(self.orphan_count(g), 3)


class TestPhoamignore(MutationTestBase):
    """Adding a .phoamignore entry removes a file from the graph."""

    def test_ignore_file_by_name(self):
        self.write_file(".phoamignore", "standalone.py\n")

        g = self.rebuild()

        self.assertNotIn("standalone.py", g["nodes"])
        self.assertEqual(self.node_count(g), 9)
        # standalone was an orphan, so orphan count drops by 1
        self.assertEqual(self.orphan_count(g), 1)

    def test_ignore_directory(self):
        self.write_file(".phoamignore", "docs/\n")

        g = self.rebuild()

        # All docs should be excluded
        for node in g["nodes"]:
            self.assertFalse(node.startswith("docs/"), f"docs file still in graph: {node}")

        # Nodes: 10 - 3 docs = 7
        self.assertEqual(self.node_count(g), 7)

        # All wiki-link edges to/from docs should be gone
        for e in g["edges"]:
            self.assertFalse(e["from"].startswith("docs/"), f"edge from docs: {e}")
            self.assertFalse(e["to"].startswith("docs/"), f"edge to docs: {e}")

    def test_ignore_connected_file_removes_edges(self):
        """Ignoring a connected file removes it AND its edges."""
        self.write_file(".phoamignore", "auth.py\n")

        g = self.rebuild()

        self.assertNotIn("src/api/auth.py", g["nodes"])
        # No edges should reference auth.py
        for e in g["edges"]:
            self.assertNotEqual(e["from"], "src/api/auth.py")
            self.assertNotEqual(e["to"], "src/api/auth.py")


class TestDeleteFile(MutationTestBase):
    """Deleting a file removes the node and all its edges."""

    def test_delete_connected_file(self):
        self.delete_file("src/api/auth.py")

        g = self.rebuild()

        self.assertNotIn("src/api/auth.py", g["nodes"])
        self.assertEqual(self.node_count(g), 9)

        # No edges should reference auth.py
        for e in g["edges"]:
            self.assertNotEqual(e["from"], "src/api/auth.py")
            self.assertNotEqual(e["to"], "src/api/auth.py")

        # routes.py import of .auth should become a dangling reference (no edge)
        self.assertFalse(self.has_edge(g, "src/api/routes.py", "src/api/auth.py"))


class TestOutputReflectsMutations(MutationTestBase):
    """KB_INDEX.md and graph.html reflect graph mutations."""

    def test_kb_index_reflects_added_file(self):
        self.write_file("src/api/middleware.py", (
            '"""Request middleware."""\n'
            'from .auth import verify_token\n'
        ))

        g = self.rebuild()
        path = write_kb_index(g, self.project)
        with open(path) as f:
            content = f.read()

        self.assertIn("middleware.py", content)
        self.assertIn("Nodes: 11", content)

    def test_graph_html_reflects_added_file(self):
        self.write_file("src/api/middleware.py", (
            '"""Request middleware."""\n'
            'from .auth import verify_token\n'
        ))

        g = self.rebuild()
        path = write_graph_html(g, self.project)
        with open(path) as f:
            content = f.read()

        self.assertIn("middleware.py", content)


if __name__ == "__main__":
    unittest.main()
