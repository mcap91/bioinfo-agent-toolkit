"""Golden + mutated-copy tests for label.py's response parser.

Stdlib only, no pytest import, so this runs both under pytest locally
(`pytest eval/test_label.py`) and via a plain loop over module-level `test_*` functions
where pytest isn't available.
"""

from __future__ import annotations

import contextlib
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import label  # noqa: E402

CAPTURE_PATH = Path(__file__).parent / "captures" / "claude_print_json_schema.json"


def _load_capture() -> dict:
    return json.loads(CAPTURE_PATH.read_text(encoding="utf-8"))


def _parse_expecting_exit(raw: dict) -> tuple[int | None, str]:
    buf = io.StringIO()
    try:
        with contextlib.redirect_stderr(buf):
            label.parse_response(raw)
    except SystemExit as exc:
        return exc.code, buf.getvalue()
    return None, buf.getvalue()


def test_golden_capture_extracts_paddleocr_ocr_label():
    raw = _load_capture()
    labels = label.parse_response(raw)
    by_name = {entry["name"]: entry["relevant"] for entry in labels}
    assert "paddleocr" in by_name
    assert "ocr" in by_name["paddleocr"]


def test_is_error_true_exits_naming_field():
    raw = _load_capture()
    raw["is_error"] = True
    code, stderr = _parse_expecting_exit(raw)
    assert code == 1
    assert "is_error" in stderr


def test_missing_structured_output_exits_naming_field():
    raw = _load_capture()
    del raw["structured_output"]
    code, stderr = _parse_expecting_exit(raw)
    assert code == 1
    assert "structured_output" in stderr


def test_subtype_not_success_exits_naming_field():
    raw = _load_capture()
    raw["subtype"] = "error_max_turns"
    code, stderr = _parse_expecting_exit(raw)
    assert code == 1
    assert "subtype" in stderr


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
    print(f"{len(tests)} tests ok")
