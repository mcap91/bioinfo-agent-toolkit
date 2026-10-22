"""Golden + mutated-copy tests for expand.py's response parser, re-checks, and the
tools.ts tool-description extraction.
"""

from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import expand  # noqa: E402

CAPTURE_DIR = Path(__file__).parent / "captures"
CAPTURE_PATH = CAPTURE_DIR / "expand_agent-viz.json"
META_PATH = CAPTURE_DIR / "expand_agent-viz.meta.json"

REPO_ROOT = Path(__file__).resolve().parents[4]


def _load_capture() -> dict:
    return json.loads(CAPTURE_PATH.read_text(encoding="utf-8"))


def _load_meta() -> dict:
    return json.loads(META_PATH.read_text(encoding="utf-8"))


def _parse_expecting_exit(func, *args) -> tuple[int | None, str]:
    buf = io.StringIO()
    try:
        with contextlib.redirect_stderr(buf):
            func(*args)
    except SystemExit as exc:
        return exc.code, buf.getvalue()
    return None, buf.getvalue()


def test_golden_capture_forty_terms_incl_zoetrope():
    raw = _load_capture()
    expansion = expand.parse_response(raw)
    expand.check_expansion("agent-viz", expansion)
    assert len(expansion["terms"]) == 40
    assert "zoetrope" in expansion["terms"]


def test_golden_tool_description_matches_committed_capture():
    meta = _load_meta()
    text = subprocess.run(
        ["git", "show", f"{meta['main_commit']}:packages/catalog-mcp/src/tools.ts"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert expand.extract_tool_description(text) == meta["tool_description"]


def test_is_error_true_exits_naming_field():
    raw = _load_capture()
    raw["is_error"] = True
    code, stderr = _parse_expecting_exit(expand.parse_response, raw)
    assert code == 1
    assert "is_error" in stderr


def test_missing_structured_output_exits_naming_field():
    raw = _load_capture()
    del raw["structured_output"]
    code, stderr = _parse_expecting_exit(expand.parse_response, raw)
    assert code == 1
    assert "structured_output" in stderr


def test_too_many_terms_exits_naming_brief():
    raw = _load_capture()
    expansion = dict(expand.parse_response(raw))
    expansion["terms"] = list(expansion["terms"]) * 2  # 80 terms
    code, stderr = _parse_expecting_exit(expand.check_expansion, "agent-viz", expansion)
    assert code == 1
    assert "agent-viz" in stderr


def test_term_too_long_exits_naming_brief():
    raw = _load_capture()
    expansion = dict(expand.parse_response(raw))
    expansion["terms"] = list(expansion["terms"])
    expansion["terms"][0] = "x" * 201
    code, stderr = _parse_expecting_exit(expand.check_expansion, "agent-viz", expansion)
    assert code == 1
    assert "agent-viz" in stderr


def test_tool_description_extraction_fails_on_zero_matches():
    code, stderr = _parse_expecting_exit(expand.extract_tool_description, "no search tool here")
    assert code == 1
    assert "found 0" in stderr


def test_tool_description_extraction_fails_on_multiple_matches():
    duped = "name: 'search', description: 'a',\nname: 'search', description: 'b',"
    code, stderr = _parse_expecting_exit(expand.extract_tool_description, duped)
    assert code == 1
    assert "found 2" in stderr


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
    print(f"{len(tests)} tests ok")
