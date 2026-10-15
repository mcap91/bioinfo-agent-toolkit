"""Survey-search eval: drift gate, coverage gate, lookup regression, compound backstop.

Run: `uv run python eval/run_eval.py --dir <repo>`. Any gate failure prints a named
reason and exits 1. On success, writes eval/coverage_results.json.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from catalog_embedder.build import run_build
from catalog_embedder.search import lexical_members, run_search

LOOKUP_NAMES = [
    "markitdown", "olmocr", "paddleocr", "qdrant", "lancedb",
    "firecrawl", "ripgrep", "duckdb", "gromacs", "textual",
]

SYNTHETIC_NAME = "synthetic-paddleocr-compound"


def fail(reason: str) -> None:
    print(f"FAIL: {reason}", file=sys.stderr)
    sys.exit(1)


def drift_gate(fixtures: dict, entries_dir: Path) -> None:
    names = [p.stem for p in entries_dir.glob("*.md")]
    for query in fixtures["queries"]:
        members, _ = lexical_members(entries_dir, names, query["terms"])
        live = sorted(members.keys())
        golden = query["golden"]
        if live != golden:
            added = sorted(set(live) - set(golden))
            removed = sorted(set(golden) - set(live))
            print(f"drift on '{query['id']}': added={added} removed={removed}", file=sys.stderr)
            fail("corpus drifted — review and re-run derive_fixtures.py")


def coverage_gate(fixtures: dict, dir: Path) -> list[dict]:
    report = []
    for query in fixtures["queries"]:
        response = run_search(dir, query=query["id"], terms=query["terms"])
        lexical_names = {
            r["name"] for r in response["results"] if r["match"]["type"] == "lexical"
        }
        golden = set(query["golden"])
        if not golden <= lexical_names:
            fail(f"coverage gap on '{query['id']}': missing {sorted(golden - lexical_names)}")
        semantic_added = sum(1 for r in response["results"] if r["match"]["type"] == "semantic")
        report.append({
            "id": query["id"],
            "golden_size": len(golden),
            "lexical_returned": len(lexical_names),
            "coverage": 1.0,
            "semantic_added": semantic_added,
        })
    return report


def lookup_regression_gate(dir: Path) -> None:
    for name in LOOKUP_NAMES:
        response = run_search(dir, query=name)
        lexical_results = [r for r in response["results"] if r["match"]["type"] == "lexical"]
        if not lexical_results or lexical_results[0]["name"] != name:
            first = lexical_results[0]["name"] if lexical_results else None
            fail(f"lookup regression: '{name}' did not rank first (got {first})")


def compound_backstop_gate(dir: Path) -> int | None:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        tmp_entries = tmpdir / "catalog" / "entries"
        shutil.copytree(dir / "catalog" / "entries", tmp_entries)
        fixture_src = Path(__file__).parent / "fixtures" / f"{SYNTHETIC_NAME}.md"
        shutil.copy(fixture_src, tmp_entries / f"{SYNTHETIC_NAME}.md")

        run_build(tmpdir)
        response = run_search(tmpdir, query="ocr", terms=["ocr"], semantic_n=50)

        lexical_names = {r["name"] for r in response["results"] if r["match"]["type"] == "lexical"}
        if SYNTHETIC_NAME in lexical_names:
            fail(f"compound backstop: '{SYNTHETIC_NAME}' is a lexical member (should not be)")

        rank = None
        for r in response["results"]:
            if r["name"] == SYNTHETIC_NAME and r["match"]["type"] == "semantic":
                rank = r["match"]["rank"]
                break
        if rank is None:
            fail(f"compound backstop: '{SYNTHETIC_NAME}' did not appear among semantic suggestions")
        return rank


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=Path, required=True)
    args = parser.parse_args()
    dir = args.dir.resolve()

    fixtures_path = Path(__file__).parent / "survey_fixtures.json"
    fixtures = json.loads(fixtures_path.read_text(encoding="utf-8"))
    entries_dir = dir / "catalog" / "entries"

    drift_gate(fixtures, entries_dir)
    print("drift gate: passed")

    report = coverage_gate(fixtures, dir)
    print("coverage gate: passed (coverage 1.0 for all fixtures)")

    lookup_regression_gate(dir)
    print("lookup regression gate: passed")

    compound_backstop_rank = compound_backstop_gate(dir)
    print(f"compound backstop gate: passed (rank {compound_backstop_rank})")

    results_path = Path(__file__).parent / "coverage_results.json"
    results_path.write_text(
        json.dumps({"queries": report, "compound_backstop_rank": compound_backstop_rank}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {results_path}")


if __name__ == "__main__":
    main()
