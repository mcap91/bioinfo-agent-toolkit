"""Tests for judge_diag.py's deterministic parts, on the real agent-viz search capture."""

from __future__ import annotations

import contextlib
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).parent))
import judge_diag  # noqa: E402

SEARCH_CAPTURE_PATH = Path(__file__).parent / "captures" / "search_agent-viz.json"


def _results() -> list[dict]:
    return json.loads(SEARCH_CAPTURE_PATH.read_text(encoding="utf-8"))["results"]


def test_chunks_keep_response_order_and_cover_every_result_once():
    results = _results()
    chunks = judge_diag.chunk_results(results, 50)
    assert [len(c) for c in chunks] == [50] * 6 + [26]
    assert [r["name"] for c in chunks for r in c] == [r["name"] for r in results]


def test_entry_text_is_added_without_changing_the_search_fields():
    results = _results()[:3]
    texts = {r["name"]: f"full text of {r['name']}" for r in results}
    augmented = judge_diag.with_entry_text(results, texts)
    for original, new in zip(results, augmented):
        assert {k: v for k, v in new.items() if k != "entry_text"} == original
        assert new["entry_text"] == texts[original["name"]]
    assert json.loads(judge_diag.chunk_response_text(augmented)) == {"results": augmented}


def test_cost_cap_aborts_once_cumulative_spend_exceeds_it():
    spend = judge_diag.Spend(1.0)
    spend.add(0.6)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stderr(buf):
            spend.add(0.5)
    except SystemExit as exc:
        assert exc.code == 1
        assert "cost cap exceeded" in buf.getvalue()
    else:
        raise AssertionError("expected the cap to abort")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
    print(f"{len(tests)} tests ok")
