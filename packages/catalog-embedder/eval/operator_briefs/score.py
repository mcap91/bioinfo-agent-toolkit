"""Stage 2, zero model calls: run the catalog_embedder search CLI with each brief's
frozen expansion exactly as the step 2b(b) capture did, then score the surfaced
results against operator_briefs/answer_key.json.

Run: `.venv/bin/python eval/operator_briefs/score.py --dir <repo> --expansion
expansion_v1 --run-label baseline [--semantic-n 10]`. Each raw search response is
saved as the search CLI's exact stdout text (judge.py reads it verbatim). Any corpus
mismatch, vector-file drift, or response-shape drift prints a named reason and exits 1.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from catalog_embedder.vectors import read_vectors, vectors_path

EVAL_DIR = Path(__file__).parent
ANSWER_KEY_PATH = EVAL_DIR / "answer_key.json"

ARTIFACT_NAME_RE = re.compile(r"^[A-Za-z0-9_-]+$")
VALID_MATCH_TYPES = {"lexical", "semantic"}


def fail(reason: str) -> None:
    print(f"FAIL: {reason}", file=sys.stderr)
    sys.exit(1)


def validate_bare_name(value: str, arg_name: str) -> None:
    if not ARTIFACT_NAME_RE.match(value):
        fail(f"{arg_name} {value!r} must be a bare name matching [A-Za-z0-9_-]+")


def resolve_under_eval_dir(path: Path, arg_name: str) -> Path:
    resolved = path.resolve()
    if resolved.parent != EVAL_DIR.resolve():
        fail(f"{arg_name} resolves outside operator_briefs/: {path}")
    return resolved


def run_search_cli(dir: Path, query: str, terms: list[str], semantic_n: int) -> str:
    """Invoke the catalog_embedder search CLI exactly as the 2b(b) capture did; returns
    its stdout text verbatim — the byte-for-byte text judge.py must read back.
    """
    command = [
        sys.executable,
        "-m",
        "catalog_embedder",
        "search",
        "--dir",
        str(dir),
        "--query",
        query,
        "--semantic-n",
        str(semantic_n),
    ]
    for term in terms:
        command.extend(["--term", term])
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return result.stdout


def validate_vectors(
    vector_data: dict[str, Any] | None, corpus: set[str], vectors_file: Path
) -> dict[str, Any]:
    """Fail loud unless the vector file exists, its entries match the corpus exactly,
    and its model is recorded. score.py never rebuilds — the orchestrator rebuilds
    before scoring runs.
    """
    if vector_data is None:
        fail(f"vector file {vectors_file} not found — rebuild with python -m catalog_embedder build")
    entries = vector_data.get("entries")
    if not isinstance(entries, dict):
        fail(f"vector file {vectors_file} missing entries — rebuild with python -m catalog_embedder build")
    entry_names = set(entries)
    if entry_names != corpus:
        missing = sorted(corpus - entry_names)
        extra = sorted(entry_names - corpus)
        fail(
            f"vector file {vectors_file} entries do not match corpus "
            f"(missing={missing} extra={extra}) — rebuild with python -m catalog_embedder build"
        )
    model = vector_data.get("model")
    if not model:
        fail(f"vector file {vectors_file} missing model — rebuild with python -m catalog_embedder build")
    return {"model": model, "count": len(entries)}


def validate_response_shape(brief_id: str, response: Any) -> list[dict[str, Any]]:
    """Fail loud on result-shape/channel drift; accept only lexical/semantic match types."""
    if not isinstance(response, dict) or not isinstance(response.get("results"), list):
        fail(f"brief {brief_id!r}: response missing results list")
    results = response["results"]
    for result in results:
        if not isinstance(result, dict) or not result.get("name"):
            fail(f"brief {brief_id!r}: result missing name")
        match = result.get("match")
        match_type = match.get("type") if isinstance(match, dict) else None
        if match_type not in VALID_MATCH_TYPES:
            fail(f"brief {brief_id!r}: result {result['name']!r} has unknown match.type {match_type!r}")
    return results


def score_brief(
    brief_id: str, response: dict[str, Any], key_names: set[str], corpus: set[str]
) -> dict[str, Any]:
    """Pure: depends only on the search response and the answer key, no fastembed."""
    results = validate_response_shape(brief_id, response)
    result_names = {r["name"] for r in results}
    bad = sorted(result_names - corpus)
    if bad:
        fail(f"brief {brief_id!r}: result name(s) not in corpus: {bad}")

    lexical_names = {r["name"] for r in results if r["match"]["type"] == "lexical"}
    semantic_names = {r["name"] for r in results if r["match"]["type"] == "semantic"}

    n = len(key_names)
    returned = len(results)
    lexical_relevant = len(lexical_names & key_names)
    semantic_relevant = len(semantic_names & key_names)
    combined_relevant = len(result_names & key_names)

    return {
        "n": n,
        "returned": returned,
        "lexical_returned": len(lexical_names),
        "semantic_returned": len(semantic_names),
        "lexical_relevant": lexical_relevant,
        "semantic_relevant": semantic_relevant,
        "combined_relevant": combined_relevant,
        "surfaced_recall": (combined_relevant / n) if n else 0.0,
        "lexical_recall": (lexical_relevant / n) if n else 0.0,
        "random_pick_recall": (returned / len(corpus)) if corpus else 0.0,
    }


def run_scoring(dir: Path, expansion_path: Path, expansion_name: str, semantic_n: int) -> dict[str, Any]:
    answer_key = json.loads(ANSWER_KEY_PATH.read_text(encoding="utf-8"))
    expansion = json.loads(expansion_path.read_text(encoding="utf-8"))
    corpus = set(answer_key["corpus"])

    vectors = validate_vectors(read_vectors(dir), corpus, vectors_path(dir))

    briefs: dict[str, Any] = {}
    for brief_id, brief_expansion in expansion["expansions"].items():
        response_text = run_search_cli(
            dir, brief_expansion["query"], brief_expansion["terms"], semantic_n
        )
        response = json.loads(response_text)
        key_names = set(answer_key["relevant"].get(brief_id, {}).keys())
        metrics = score_brief(brief_id, response, key_names, corpus)
        briefs[brief_id] = {"metrics": metrics, "raw_response": response_text}

    return {
        "expansion": expansion_name,
        "semantic_n": semantic_n,
        "corpus_size": len(corpus),
        "vectors": vectors,
        "briefs": briefs,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=Path, required=True)
    parser.add_argument("--expansion", required=True, help="Expansion file name, e.g. expansion_v1")
    parser.add_argument("--run-label", required=True, help="Distinguishes baseline vs each engine fix")
    parser.add_argument("--semantic-n", dest="semantic_n", type=int, default=10)
    args = parser.parse_args()
    dir = args.dir.resolve()

    validate_bare_name(args.expansion, "--expansion")
    validate_bare_name(args.run_label, "--run-label")
    expansion_path = resolve_under_eval_dir(EVAL_DIR / f"{args.expansion}.json", "--expansion")
    output_path = resolve_under_eval_dir(
        EVAL_DIR / f"score_{args.expansion}_{args.run_label}.json", "--run-label"
    )
    if output_path.exists():
        fail(f"refusing to overwrite existing {output_path}")

    results = run_scoring(dir, expansion_path, args.expansion, args.semantic_n)

    output_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
