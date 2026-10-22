"""Golden + mutated-copy tests for score.py's pure metric scorer and validators.

Only pure functions are exercised here — no fastembed, no subprocess, no filesystem
writes: score_brief, validate_response_shape, validate_vectors, validate_bare_name,
and the CLI-argument guard path in main().
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
REPO_ROOT = Path(__file__).resolve().parents[4]
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
    metrics = score.score_brief("agent-viz", response, {"zoetrope"}, {"zoetrope"}, corpus)
    assert metrics["returned"] == 326
    assert metrics["lexical_returned"] == 316
    assert metrics["semantic_returned"] == 10
    assert metrics["random_pick_recall"] == 326 / 581
    assert metrics["n"] == 1
    assert metrics["combined_relevant"] == 1
    assert metrics["lexical_relevant"] == 1
    assert metrics["semantic_relevant"] == 0


def test_agreed_subset_is_key_minus_tiebroken_pairs_on_the_real_answer_key():
    """Agreed = pairs both labeling passes marked relevant. In the committed key, a pair
    in agreement.disagreements reached the key only through the tie-break."""
    answer_key = json.loads(score.ANSWER_KEY_PATH.read_text(encoding="utf-8"))
    differs = 0
    for brief_id, entries in answer_key["relevant"].items():
        key_names = set(entries)
        contested = {
            d["name"] for d in answer_key["agreement"]["disagreements"] if d["brief"] == brief_id
        }
        agreed = score.agreed_key_names(answer_key, brief_id)
        assert agreed == key_names - contested
        assert agreed <= key_names
        differs += key_names != agreed
    assert differs > 0


def test_agreed_recall_is_reported_separately_from_full_key_recall():
    response = _load_response()
    corpus = _corpus()
    unreturned = sorted(corpus - {r["name"] for r in response["results"]})[0]
    metrics = score.score_brief("agent-viz", response, {"zoetrope", unreturned}, {"zoetrope"}, corpus)
    assert metrics["n"] == 2 and metrics["surfaced_recall"] == 0.5
    assert metrics["agreed_n"] == 1 and metrics["agreed_surfaced_recall"] == 1.0
    assert metrics["agreed_lexical_recall"] == 1.0


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
    code, stderr = _parse_expecting_exit(score.score_brief, "agent-viz", mutated, set(), set(), corpus)
    assert code == 1
    assert "agent-viz" in stderr
    assert "not-a-real-entry" in stderr


def test_empty_key_gives_zero_recall():
    response = _load_response()
    corpus = _corpus()
    metrics = score.score_brief("agent-viz", response, set(), set(), corpus)
    assert metrics["surfaced_recall"] == 0.0
    assert metrics["lexical_recall"] == 0.0


def test_unknown_match_type_exits_naming_reason():
    response = _load_response()
    mutated = json.loads(json.dumps(response))
    mutated["results"][0]["match"]["type"] = "fuzzy"
    code, stderr = _parse_expecting_exit(score.score_brief, "agent-viz", mutated, {"zoetrope"}, {"zoetrope"}, _corpus())
    assert code == 1
    assert "agent-viz" in stderr
    assert "match.type" in stderr
    assert "fuzzy" in stderr


def test_missing_results_key_exits_naming_reason():
    response = _load_response()
    mutated = json.loads(json.dumps(response))
    del mutated["results"]
    code, stderr = _parse_expecting_exit(score.score_brief, "agent-viz", mutated, {"zoetrope"}, {"zoetrope"}, _corpus())
    assert code == 1
    assert "agent-viz" in stderr
    assert "results" in stderr


def test_vectors_missing_one_name_exits_naming_missing():
    response = _load_response()
    corpus = _corpus()
    full_entries = {name: [0.0] for name in corpus}
    missing_name = sorted(corpus)[0]
    mutated_entries = dict(full_entries)
    del mutated_entries[missing_name]
    vector_data = {"model": "BAAI/bge-small-en-v1.5", "dims": 384, "entries": mutated_entries}
    code, stderr = _parse_expecting_exit(
        score.validate_vectors, vector_data, corpus, Path("catalog/.vectors.json")
    )
    assert code == 1
    assert missing_name in stderr


def test_vectors_file_missing_exits_naming_rebuild():
    corpus = _corpus()
    code, stderr = _parse_expecting_exit(
        score.validate_vectors, None, corpus, Path("catalog/.vectors.json")
    )
    assert code == 1
    assert "not found" in stderr
    assert "catalog_embedder build" in stderr


def test_vectors_matching_corpus_records_model_and_count():
    corpus = _corpus()
    entries = {name: [0.0] for name in corpus}
    vector_data = {"model": "BAAI/bge-small-en-v1.5", "dims": 384, "entries": entries}
    result = score.validate_vectors(vector_data, corpus, Path("catalog/.vectors.json"))
    assert result == {"model": "BAAI/bge-small-en-v1.5", "count": len(corpus)}


def test_run_label_name_escaping_dir_exits_before_any_search():
    original_argv = sys.argv
    sys.argv = [
        "score.py",
        "--dir",
        str(REPO_ROOT),
        "--expansion",
        "expansion_v1",
        "--run-label",
        "../x",
    ]
    try:
        code, stderr = _parse_expecting_exit(score.main)
    finally:
        sys.argv = original_argv
    assert code == 1
    assert "../x" in stderr
    assert "--run-label" in stderr


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
    print(f"{len(tests)} tests ok")
