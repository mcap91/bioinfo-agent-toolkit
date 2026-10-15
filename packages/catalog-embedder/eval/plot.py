"""Render the survey-search coverage demo plot from coverage_results.json.

Run: `uv run python eval/plot.py` (after `run_eval.py` has written coverage_results.json).
Regenerates eval/search_eval.png in place.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

EVAL_DIR = Path(__file__).parent


def main() -> None:
    results = json.loads((EVAL_DIR / "coverage_results.json").read_text(encoding="utf-8"))
    queries = results["queries"]

    ids = [q["id"] for q in queries]
    lexical = [q["lexical_returned"] for q in queries]
    semantic = [q["semantic_added"] for q in queries]

    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    y = range(len(ids))

    ax.barh(y, lexical, color="#2b6cb0", label="complete lexical set")
    ax.barh(y, semantic, left=lexical, color="#ed8936", hatch="//", label="semantic suggestions")

    ax.set_yticks(list(y))
    ax.set_yticklabels(ids)
    ax.set_xlabel("entries returned")
    ax.set_title("Survey search: the full named set, plus flagged semantic neighbors")
    ax.legend(loc="upper right")
    ax.grid(axis="x", alpha=0.2)
    ax.invert_yaxis()

    fig.tight_layout()
    fig.savefig(EVAL_DIR / "search_eval.png")
    print(f"wrote {EVAL_DIR / 'search_eval.png'}")


if __name__ == "__main__":
    main()
