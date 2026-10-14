"""Eval harness for catalog-embedder semantic + BM25 rescue search.

Runs the golden fixtures (tier1.json..tier5.json) against the `catalog_embedder search`
CLI via subprocess, measuring threshold-based full recall and precision. Supports a
threshold sweep (--sweep) comparing three methods: fusion (default), semantic, and bm25.
Does not import catalog_embedder — all interaction with the search logic goes through
the CLI.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

DEFAULT_LIMIT = 10000
DEFAULT_TIMEOUT = 300.0
SWEEP_THRESHOLDS = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]
METHODS = ["fusion", "semantic", "bm25"]


def load_fixtures(eval_dir: Path, tiers: list[int] | None) -> list[dict[str, Any]]:
    fixtures = []
    for t in tiers or range(1, 6):
        path = eval_dir / f"tier{t}.json"
        if path.exists():
            fixtures.append(json.loads(path.read_text()))
    return fixtures


def call_search(
    pkg_dir: Path,
    repo_dir: Path,
    query: str,
    method: str,
    limit: int,
    timeout: float,
) -> tuple[dict[str, Any], float]:
    cmd = [
        "uv", "run", "python", "-m", "catalog_embedder", "search",
        "--query", query,
        "--dir", str(repo_dir),
        "--method", method,
        "--threshold", "0.0",
        "--limit", str(limit),
    ]
    start = time.perf_counter()
    proc = subprocess.run(cmd, cwd=pkg_dir, capture_output=True, text=True, timeout=timeout)
    elapsed = time.perf_counter() - start
    if proc.returncode != 0:
        raise RuntimeError(
            f"search CLI failed (exit {proc.returncode}) for query {query!r} method={method}:\n{proc.stderr}"
        )
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"search CLI produced invalid JSON for query {query!r} method={method}: {exc}\nstdout: {proc.stdout!r}"
        ) from exc
    return data, elapsed


def get_search_result(
    cache: dict[tuple[str, str], tuple[dict[str, Any], float]],
    pkg_dir: Path,
    repo_dir: Path,
    query: str,
    method: str,
    limit: int,
    timeout: float,
) -> tuple[dict[str, Any], float]:
    key = (query, method)
    if key not in cache:
        cache[key] = call_search(pkg_dir, repo_dir, query, method, limit, timeout)
    return cache[key]


def metrics_at_threshold(scored: list[tuple[str, float]], expected: list[str], threshold: float) -> dict[str, Any]:
    above = [name for name, score in scored if score > threshold]
    above_set = set(above)
    expected_set = set(expected)
    hits = len(expected_set & above_set)
    recall = hits / len(expected_set) if expected_set else 0.0
    precision = hits / len(above_set) if above_set else 0.0
    return {
        "recall": recall,
        "precision": precision,
        "n_results": len(above),
        "perfect": 1 if recall == 1.0 else 0,
    }


def score_query(
    query: str,
    topic: str | None,
    expected: list[str],
    scored: list[tuple[str, float]],
    wall_time_s: float,
    thresholds: list[float],
) -> dict[str, Any]:
    by_threshold = {str(t): metrics_at_threshold(scored, expected, t) for t in thresholds}
    return {
        "query": query,
        "topic": topic,
        "expected": expected,
        "by_threshold": by_threshold,
        "wall_time_s": wall_time_s,
    }


def aggregate(query_results: list[dict[str, Any]], thresholds: list[float]) -> dict[str, Any]:
    n = len(query_results)
    agg: dict[str, Any] = {"n_queries": n}
    for t in thresholds:
        key = str(t)
        if n == 0:
            agg[key] = {"recall": 0.0, "precision": 0.0, "n_results": 0.0, "perfect": 0.0}
            continue
        agg[key] = {
            "recall": sum(r["by_threshold"][key]["recall"] for r in query_results) / n,
            "precision": sum(r["by_threshold"][key]["precision"] for r in query_results) / n,
            "n_results": sum(r["by_threshold"][key]["n_results"] for r in query_results) / n,
            "perfect": sum(r["by_threshold"][key]["perfect"] for r in query_results) / n,
        }
    agg["wall_time_s"] = sum(r["wall_time_s"] for r in query_results) / n if n else 0.0
    return agg


def run_eval_method(
    pkg_dir: Path,
    repo_dir: Path,
    fixtures: list[dict[str, Any]],
    method: str,
    limit: int,
    timeout: float,
    thresholds: list[float],
    cache: dict[tuple[str, str], tuple[dict[str, Any], float]],
) -> dict[str, Any]:
    tiers_out: dict[str, Any] = {}
    all_results: list[dict[str, Any]] = []
    for fixture in fixtures:
        tier = str(fixture["tier"])
        tier_results = []
        for q in fixture["queries"]:
            data, elapsed = get_search_result(cache, pkg_dir, repo_dir, q["query"], method, limit, timeout)
            scored = [(r["name"], r["score"]) for r in data.get("results", [])]
            tier_results.append(score_query(q["query"], q.get("topic"), q["expected"], scored, elapsed, thresholds))
        tiers_out[tier] = {
            "topics": fixture.get("topics"),
            "queries": tier_results,
            "aggregate": aggregate(tier_results, thresholds),
        }
        all_results.extend(tier_results)
    return {"method": method, "tiers": tiers_out, "overall": aggregate(all_results, thresholds)}


def print_block(label: str, result: dict[str, Any], threshold: float, file: Any) -> None:
    key = str(threshold)
    print(f"\n=== {label} (threshold={threshold}) ===", file=file)
    print(f"{'tier':<10}{'n':>5}{'recall':>10}{'precision':>11}{'n_results':>11}{'perfect':>9}", file=file)
    for tier, data in sorted(result["tiers"].items(), key=lambda kv: int(kv[0])):
        agg = data["aggregate"][key]
        print(
            f"{tier:<10}{data['aggregate']['n_queries']:>5}{agg['recall']:>10.3f}{agg['precision']:>11.3f}"
            f"{agg['n_results']:>11.2f}{agg['perfect']:>9.3f}",
            file=file,
        )
    agg = result["overall"][key]
    print(
        f"{'overall':<10}{result['overall']['n_queries']:>5}{agg['recall']:>10.3f}{agg['precision']:>11.3f}"
        f"{agg['n_results']:>11.2f}{agg['perfect']:>9.3f}",
        file=file,
    )


def print_summary(output: dict[str, Any], thresholds: list[float], file: Any) -> None:
    if "sweep" in output:
        for method in output["sweep"]["methods"]:
            result = output["sweep"]["results"][method]
            print_block(f"method={method}", result, thresholds[0], file)
    if "run" in output:
        print_block(f"method={output['run']['method']}", output["run"], thresholds[0], file)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="run_eval.py",
        description="Eval harness for catalog-embedder semantic + BM25 rescue search: threshold-based recall/precision, 3-method comparison.",
    )
    parser.add_argument("--dir", required=True, help="Path to the repo root (passed to the search CLI's --dir)")
    parser.add_argument("--tier", type=int, choices=range(1, 6), default=None, help="Run only this tier (default: all tiers 1-5)")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="--limit passed to the search CLI")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="Per-search-call subprocess timeout in seconds")
    parser.add_argument("--sweep", action="store_true", help=f"Run the threshold sweep {SWEEP_THRESHOLDS} across methods {METHODS} and save eval/threshold_sweep_results.json")
    args = parser.parse_args(argv)

    eval_dir = Path(__file__).resolve().parent
    pkg_dir = eval_dir.parent
    repo_dir = Path(args.dir).resolve()

    tiers = [args.tier] if args.tier else None
    fixtures = load_fixtures(eval_dir, tiers)
    if not fixtures:
        print(f"no fixture files found in {eval_dir}", file=sys.stderr)
        return 1

    cache: dict[tuple[str, str], tuple[dict[str, Any], float]] = {}
    output: dict[str, Any] = {}
    thresholds = SWEEP_THRESHOLDS if args.sweep else [0.0]

    if args.sweep:
        per_method = {}
        for method in METHODS:
            print(f"running sweep method={method}...", file=sys.stderr)
            per_method[method] = run_eval_method(pkg_dir, repo_dir, fixtures, method, args.limit, args.timeout, thresholds, cache)
        output["sweep"] = {"thresholds": thresholds, "methods": METHODS, "results": per_method}
    else:
        output["run"] = run_eval_method(pkg_dir, repo_dir, fixtures, "fusion", args.limit, args.timeout, thresholds, cache)

    print_summary(output, thresholds, file=sys.stderr)

    if args.sweep:
        sweep_path = eval_dir / "threshold_sweep_results.json"
        sweep_path.write_text(json.dumps(output, indent=2))
        print(f"\nsweep results written to {sweep_path}", file=sys.stderr)

    json.dump(output, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
