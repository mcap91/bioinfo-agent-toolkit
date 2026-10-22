"""Golden + mutated-copy tests for judge.py's response parser and recall scorer."""

from __future__ import annotations

import contextlib
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import judge  # noqa: E402

EVAL_DIR = Path(__file__).parent
CAPTURE_DIR = EVAL_DIR / "captures"
JUDGE_CAPTURE_PATH = CAPTURE_DIR / "judge_agent-viz.json"
JUDGE_META_PATH = CAPTURE_DIR / "judge_agent-viz.meta.json"
SEARCH_CAPTURE_PATH = CAPTURE_DIR / "search_agent-viz.json"
BRIEFS_PATH = EVAL_DIR / "briefs.json"

REPO_ROOT = Path(__file__).resolve().parents[4]


def _load_judge_capture() -> dict:
    return json.loads(JUDGE_CAPTURE_PATH.read_text(encoding="utf-8"))


def _response_names() -> set[str]:
    search = json.loads(SEARCH_CAPTURE_PATH.read_text(encoding="utf-8"))
    return {r["name"] for r in search["results"]}


def _parse_expecting_exit(func, *args) -> tuple[int | None, str]:
    buf = io.StringIO()
    try:
        with contextlib.redirect_stderr(buf):
            func(*args)
    except SystemExit as exc:
        return exc.code, buf.getvalue()
    return None, buf.getvalue()


def test_golden_capture_twenty_kept_all_in_response():
    raw = _load_judge_capture()
    kept = judge.parse_response(raw)
    assert len(kept) == 20
    response_names = _response_names()
    judge.check_kept("agent-viz", kept, response_names)


def test_golden_prompt_from_unedited_search_capture_matches_captured_byte_count():
    """The judge prompt must be built from the raw search stdout text byte-for-byte,
    never a re-parsed/re-serialized copy, or the byte count drifts from the capture.
    """
    meta = json.loads(JUDGE_META_PATH.read_text(encoding="utf-8"))
    raw_response_text = SEARCH_CAPTURE_PATH.read_text(encoding="utf-8")
    briefs = json.loads(BRIEFS_PATH.read_text(encoding="utf-8"))["briefs"]
    question = next(b["question"] for b in briefs if b["id"] == "agent-viz")
    prompt = judge.build_prompt(question, raw_response_text)
    assert len(prompt.encode("utf-8")) == meta["prompt_bytes"] == 232820


def test_is_error_true_exits_naming_field():
    raw = _load_judge_capture()
    raw["is_error"] = True
    code, stderr = _parse_expecting_exit(judge.parse_response, raw)
    assert code == 1
    assert "is_error" in stderr


def test_missing_structured_output_exits_naming_field():
    raw = _load_judge_capture()
    del raw["structured_output"]
    code, stderr = _parse_expecting_exit(judge.parse_response, raw)
    assert code == 1
    assert "structured_output" in stderr


def test_kept_name_not_in_response_exits_naming_brief():
    raw = _load_judge_capture()
    kept = judge.parse_response(raw) + [{"name": "not-a-real-entry", "reason": "fabricated"}]
    response_names = _response_names()
    code, stderr = _parse_expecting_exit(judge.check_kept, "agent-viz", kept, response_names)
    assert code == 1
    assert "agent-viz" in stderr
    assert "not-a-real-entry" in stderr


def test_stage3_recall_pure():
    assert judge.stage3_recall({"zoetrope", "pixel-agents"}, {"zoetrope", "herdr"}) == 0.5
    assert judge.stage3_recall(set(), set()) == 0.0


def test_score_results_name_escaping_dir_exits_before_any_read():
    original_argv = sys.argv
    sys.argv = ["judge.py", "--score-results", "../x.json"]
    try:
        code, stderr = _parse_expecting_exit(judge.main)
    finally:
        sys.argv = original_argv
    assert code == 1
    assert "../x" in stderr
    assert "--score-results" in stderr


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
    print(f"{len(tests)} tests ok")
