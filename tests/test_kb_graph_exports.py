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


if __name__ == "__main__":
    unittest.main()
