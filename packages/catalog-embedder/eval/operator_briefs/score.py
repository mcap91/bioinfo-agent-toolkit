"""Stage 2, zero model calls: run `run_search` in-process with each brief's frozen
expansion, then score the surfaced results against operator_briefs/answer_key.json.

Run: `.venv/bin/python eval/operator_briefs/score.py --dir <repo> --expansion
expansion_v1 --run-label baseline [--semantic-n 10]`. Each raw search response is
saved alongside its metrics (judge.py reads it verbatim). Any corpus mismatch prints a
named reason and exits 1.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from catalog_embedder.search import run_search
from catalog_embedder.vectors import read_vectors

EVAL_DIR = Path(__file__).parent
ANSWER_KEY_PATH = EVAL_DIR / "answer_key.json"


def fail(reason: str) -> None:
    print(f"FAIL: {reason}", file=sys.stderr)
    sys.exit(1)


def score_brief(
    brief_id: str, response: dict[str, Any], key_names: set[str], corpus: set[str]
) -> dict[str, Any]:
    """Pure: depends only on the search response and the answer key, no fastembed."""
    results = response["results"]
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


def run_scoring(dir: Path, expansion_name: str, semantic_n: int) -> dict[str, Any]:
    answer_key = json.loads(ANSWER_KEY_PATH.read_text(encoding="utf-8"))
    expansion = json.loads((EVAL_DIR / f"{expansion_name}.json").read_text(encoding="utf-8"))
    corpus = set(answer_key["corpus"])

    vector_data = read_vectors(dir)
    if vector_data is None:
        fail("catalog/.vectors.json not found — run `build` first")

    briefs: dict[str, Any] = {}
    for brief_id, brief_expansion in expansion["expansions"].items():
        response = run_search(
            dir,
            brief_expansion["query"],
            terms=brief_expansion["terms"],
            semantic_n=semantic_n,
        )
        key_names = set(answer_key["relevant"].get(brief_id, {}).keys())
        metrics = score_brief(brief_id, response, key_names, corpus)
        briefs[brief_id] = {"metrics": metrics, "raw_response": response}

    return {
        "expansion": expansion_name,
        "semantic_n": semantic_n,
        "corpus_size": len(corpus),
        "vectors": {"model": vector_data.get("model"), "count": vector_data.get("count")},
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

    output_path = EVAL_DIR / f"score_{args.expansion}_{args.run_label}.json"
    if output_path.exists():
        fail(f"refusing to overwrite existing {output_path}")

    results = run_scoring(dir, args.expansion, args.semantic_n)

    output_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
