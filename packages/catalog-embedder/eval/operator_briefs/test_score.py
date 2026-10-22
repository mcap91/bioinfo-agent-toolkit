"""Golden + mutated-copy tests for score.py's pure metric scorer.

Only `score_brief` is exercised here — it needs no fastembed, only the saved search
response capture and a key.
"""

from __future__ import annotations

import contextlib
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).parent))
import score  # noqa: E402

CAPTURE_PATH = Path(__file__).parent / "captures" / "search_agent-viz.json"
CORPUS_SIZE = 581


def _load_response() -> dict:
    return json.loads(CAPTURE_PATH.read_text(encoding="utf-8"))


def _corpus() -> set[str]:
    response = _load_response()
    names = {r["name"] for r in response["results"]}
    filler = {f"filler-{i}" for i in range(CORPUS_SIZE - len(names))}
    return names | filler


def _parse_expecting_exit(func, *args) -> tuple[int | None, str]:
    buf = io.StringIO()
    try:
        with contextlib.redirect_stderr(buf):
            func(*args)
    except SystemExit as exc:
        return exc.code, buf.getvalue()
    return None, buf.getvalue()


def test_golden_capture_combined_lexical_semantic_and_random_pick_counts():
    response = _load_response()
    corpus = _corpus()
    metrics = score.score_brief("agent-viz", response, {"zoetrope"}, corpus)
    assert metrics["returned"] == 326
    assert metrics["lexical_returned"] == 316
    assert metrics["semantic_returned"] == 10
    assert metrics["random_pick_recall"] == 326 / 581
    assert metrics["n"] == 1
    assert metrics["combined_relevant"] == 1
    assert metrics["lexical_relevant"] == 1
    assert metrics["semantic_relevant"] == 0


def test_result_name_not_in_corpus_exits_naming_brief():
    response = _load_response()
    mutated = json.loads(json.dumps(response))
    mutated["results"].append(
        {
            "name": "not-a-real-entry",
            "title": "x",
            "category": "x",
            "decision_status": "open",
            "summary": "x",
            "tags": [],
            "match": {"type": "lexical", "terms": [], "fields": []},
        }
    )
    corpus = _corpus()
    code, stderr = _parse_expecting_exit(score.score_brief, "agent-viz", mutated, set(), corpus)
    assert code == 1
    assert "agent-viz" in stderr
    assert "not-a-real-entry" in stderr


def test_empty_key_gives_zero_recall():
    response = _load_response()
    corpus = _corpus()
    metrics = score.score_brief("agent-viz", response, set(), corpus)
    assert metrics["surfaced_recall"] == 0.0
    assert metrics["lexical_recall"] == 0.0


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
    print(f"{len(tests)} tests ok")
