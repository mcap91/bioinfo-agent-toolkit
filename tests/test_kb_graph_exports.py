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
