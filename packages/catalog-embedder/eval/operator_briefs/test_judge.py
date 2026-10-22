"""Golden + mutated-copy tests for judge.py's response parser and recall scorer."""

from __future__ import annotations

import contextlib
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
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


def test_kept_item_not_object_exits_naming_index():
    raw = _load_judge_capture()
    raw["structured_output"]["kept"][0] = {}
    code, stderr = _parse_expecting_exit(judge.parse_response, raw)
    assert code == 1
    assert "kept[0]" in stderr
    assert "name" in stderr


def test_kept_item_name_non_string_exits_naming_index():
    raw = _load_judge_capture()
    raw["structured_output"]["kept"][0]["name"] = 123
    code, stderr = _parse_expecting_exit(judge.parse_response, raw)
    assert code == 1
    assert "kept[0]" in stderr
    assert "name" in stderr


def test_kept_item_reason_empty_exits_naming_index():
    raw = _load_judge_capture()
    raw["structured_output"]["kept"][0]["reason"] = ""
    code, stderr = _parse_expecting_exit(judge.parse_response, raw)
    assert code == 1
    assert "kept[0]" in stderr
    assert "reason" in stderr


def test_kept_name_not_in_response_exits_naming_brief():
    raw = _load_judge_capture()
    kept = judge.parse_response(raw) + [{"name": "not-a-real-entry", "reason": "fabricated"}]
    response_names = _response_names()
    code, stderr = _parse_expecting_exit(judge.check_kept, "agent-viz", kept, response_names)
    assert code == 1
    assert "agent-viz" in stderr
    assert "not-a-real-entry" in stderr


def test_judge_brief_on_golden_capture_reports_counts_cost_prompt_size_and_both_recalls():
    """Stage 3 reporting per the baseline ruling: kept count, full-key and agreed-subset
    recall, prompt size, and cost — and the raw response is on disk before any check."""
    import tempfile

    capture = _load_judge_capture()
    search_text = SEARCH_CAPTURE_PATH.read_text(encoding="utf-8")
    question = next(b["question"] for b in json.loads(BRIEFS_PATH.read_text(encoding="utf-8"))["briefs"] if b["id"] == "agent-viz")
    original = judge.call_claude
    judge.call_claude = lambda prompt: capture
    try:
        with tempfile.TemporaryDirectory() as tmp:
            raw_path = Path(tmp) / "judge-agent-viz.json"
            result = judge.judge_brief("agent-viz", question, search_text, raw_path)
            assert json.loads(raw_path.read_text(encoding="utf-8")) == capture
    finally:
        judge.call_claude = original
    answer_key = json.loads(judge.ANSWER_KEY_PATH.read_text(encoding="utf-8"))
    kept_names = {item["name"] for item in capture["structured_output"]["kept"]}
    key = set(answer_key["relevant"]["agent-viz"])
    agreed = judge.agreed_key_names(answer_key, "agent-viz")
    assert result["kept_count"] == 20
    assert result["prompt_bytes"] == 232820
    assert result["cost_usd"] == capture["total_cost_usd"]
    assert result["n"] == len(key) and result["agreed_n"] == len(agreed)
    assert result["stage3_recall"] == len(kept_names & key) / len(key)
    assert result["stage3_agreed_recall"] == len(kept_names & agreed) / len(agreed)


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
