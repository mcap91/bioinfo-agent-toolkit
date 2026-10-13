"""Eval harness for catalog-embedder hybrid search.

Runs the golden fixtures (tier1.json..tier5.json) against the `catalog_embedder search`
CLI via subprocess, computing recall@3/5/10 and MRR. Supports an alpha sweep
(--sweep) and a reciprocal-rank-fusion comparison (--rrf). Does not import
catalog_embedder — all interaction with the search logic goes through the CLI.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

DEFAULT_ALPHA = 0.5
DEFAULT_LIMIT = 200
DEFAULT_TIMEOUT = 300.0
SWEEP_ALPHAS = [0.0, 0.25, 0.5, 0.75, 1.0]
RRF_K = 60


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
    alpha: float,
    limit: int,
    timeout: float,
) -> tuple[dict[str, Any], float]:
    cmd = [
        "uv", "run", "python", "-m", "catalog_embedder", "search",
        "--query", query,
        "--dir", str(repo_dir),
        "--alpha", str(alpha),
        "--limit", str(limit),
    ]
    start = time.perf_counter()
    proc = subprocess.run(cmd, cwd=pkg_dir, capture_output=True, text=True, timeout=timeout)
    elapsed = time.perf_counter() - start
    if proc.returncode != 0:
        raise RuntimeError(
            f"search CLI failed (exit {proc.returncode}) for query {query!r} alpha={alpha}:\n{proc.stderr}"
        )
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"search CLI produced invalid JSON for query {query!r} alpha={alpha}: {exc}\nstdout: {proc.stdout!r}"
        ) from exc
    return data, elapsed


def get_search_result(
    cache: dict[tuple[str, float], tuple[dict[str, Any], float]],
    pkg_dir: Path,
    repo_dir: Path,
    query: str,
    alpha: float,
    limit: int,
    timeout: float,
) -> tuple[dict[str, Any], float]:
    key = (query, alpha)
    if key not in cache:
        cache[key] = call_search(pkg_dir, repo_dir, query, alpha, limit, timeout)
    return cache[key]


def recall_at_k(ranked: list[str], expected: list[str], k: int) -> float:
    if not expected:
        return 0.0
    top_k = set(ranked[:k])
    hits = sum(1 for e in expected if e in top_k)
    return hits / len(expected)


def mrr(ranked: list[str], expected: list[str]) -> float:
    expected_set = set(expected)
    for i, name in enumerate(ranked, start=1):
        if name in expected_set:
            return 1.0 / i
    return 0.0


def rrf_fuse(lexical_ranked: list[str], semantic_ranked: list[str], k: int = RRF_K) -> list[str]:
    scores: dict[str, float] = {}
    for ranked in (lexical_ranked, semantic_ranked):
        for rank, name in enumerate(ranked, start=1):
            scores[name] = scores.get(name, 0.0) + 1.0 / (k + rank)
    return sorted(scores, key=lambda name: scores[name], reverse=True)


def score_query(query: str, topic: str | None, expected: list[str], ranked: list[str], wall_time_s: float) -> dict[str, Any]:
    return {
        "query": query,
        "topic": topic,
        "expected": expected,
        "recall@3": recall_at_k(ranked, expected, 3),
        "recall@5": recall_at_k(ranked, expected, 5),
        "recall@10": recall_at_k(ranked, expected, 10),
        "mrr": mrr(ranked, expected),
        "wall_time_s": wall_time_s,
    }


def aggregate(query_results: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(query_results)
    if n == 0:
        return {"recall@3": 0.0, "recall@5": 0.0, "recall@10": 0.0, "mrr": 0.0, "wall_time_s": 0.0, "n_queries": 0}
    return {
        "recall@3": sum(r["recall@3"] for r in query_results) / n,
        "recall@5": sum(r["recall@5"] for r in query_results) / n,
        "recall@10": sum(r["recall@10"] for r in query_results) / n,
        "mrr": sum(r["mrr"] for r in query_results) / n,
        "wall_time_s": sum(r["wall_time_s"] for r in query_results) / n,
        "n_queries": n,
    }


def run_eval_alpha(
    pkg_dir: Path,
    repo_dir: Path,
    fixtures: list[dict[str, Any]],
    alpha: float,
    limit: int,
    timeout: float,
    cache: dict[tuple[str, float], tuple[dict[str, Any], float]],
) -> dict[str, Any]:
    tiers_out: dict[str, Any] = {}
    all_results: list[dict[str, Any]] = []
    for fixture in fixtures:
        tier = str(fixture["tier"])
        tier_results = []
        for q in fixture["queries"]:
            data, elapsed = get_search_result(cache, pkg_dir, repo_dir, q["query"], alpha, limit, timeout)
            ranked = [r["name"] for r in data.get("results", [])]
            tier_results.append(score_query(q["query"], q.get("topic"), q["expected"], ranked, elapsed))
        tiers_out[tier] = {
            "topics": fixture.get("topics"),
            "queries": tier_results,
            "aggregate": aggregate(tier_results),
        }
        all_results.extend(tier_results)
    return {"alpha": alpha, "tiers": tiers_out, "overall": aggregate(all_results)}


def run_eval_rrf(
    pkg_dir: Path,
    repo_dir: Path,
    fixtures: list[dict[str, Any]],
    limit: int,
    timeout: float,
    cache: dict[tuple[str, float], tuple[dict[str, Any], float]],
) -> dict[str, Any]:
    tiers_out: dict[str, Any] = {}
    all_results: list[dict[str, Any]] = []
    for fixture in fixtures:
        tier = str(fixture["tier"])
        tier_results = []
        for q in fixture["queries"]:
            lexical_data, lex_time = get_search_result(cache, pkg_dir, repo_dir, q["query"], 0.0, limit, timeout)
            semantic_data, sem_time = get_search_result(cache, pkg_dir, repo_dir, q["query"], 1.0, limit, timeout)
            lexical_ranked = [r["name"] for r in lexical_data.get("results", [])]
            semantic_ranked = [r["name"] for r in semantic_data.get("results", [])]
            fused = rrf_fuse(lexical_ranked, semantic_ranked)
            tier_results.append(score_query(q["query"], q.get("topic"), q["expected"], fused, lex_time + sem_time))
        tiers_out[tier] = {
            "topics": fixture.get("topics"),
            "queries": tier_results,
            "aggregate": aggregate(tier_results),
        }
        all_results.extend(tier_results)
    return {"tiers": tiers_out, "overall": aggregate(all_results)}


def print_block(label: str, result: dict[str, Any], file: Any) -> None:
    print(f"\n=== {label} ===", file=file)
    print(f"{'tier':<10}{'n':>5}{'recall@3':>10}{'recall@5':>10}{'recall@10':>11}{'mrr':>8}{'avg_s':>8}", file=file)
    for tier, data in sorted(result["tiers"].items(), key=lambda kv: int(kv[0])):
        agg = data["aggregate"]
        print(
            f"{tier:<10}{agg['n_queries']:>5}{agg['recall@3']:>10.3f}{agg['recall@5']:>10.3f}"
            f"{agg['recall@10']:>11.3f}{agg['mrr']:>8.3f}{agg['wall_time_s']:>8.3f}",
            file=file,
        )
    agg = result["overall"]
    print(
        f"{'overall':<10}{agg['n_queries']:>5}{agg['recall@3']:>10.3f}{agg['recall@5']:>10.3f}"
        f"{agg['recall@10']:>11.3f}{agg['mrr']:>8.3f}{agg['wall_time_s']:>8.3f}",
        file=file,
    )


def print_summary(output: dict[str, Any], file: Any) -> None:
    if "sweep" in output:
        for a in output["sweep"]["alphas"]:
            print_block(f"alpha={a}", output["sweep"]["results"][str(a)], file)
    if "alpha_run" in output:
        print_block(f"alpha={output['alpha_run']['alpha']}", output["alpha_run"], file)
    if "rrf" in output:
        print_block(f"RRF (k={RRF_K})", output["rrf"], file)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="run_eval.py",
        description="Eval harness for catalog-embedder hybrid search: recall@k, MRR, alpha sweep, RRF comparison.",
    )
    parser.add_argument("--dir", required=True, help="Path to the repo root (passed to the search CLI's --dir)")
    parser.add_argument("--tier", type=int, choices=range(1, 6), default=None, help="Run only this tier (default: all tiers 1-5)")
    parser.add_argument("--alpha", type=float, default=DEFAULT_ALPHA, help="Blend weight for a single-alpha run (ignored with --sweep)")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="--limit passed to the search CLI")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="Per-search-call subprocess timeout in seconds")
    parser.add_argument("--sweep", action="store_true", help=f"Run the alpha sweep {SWEEP_ALPHAS} and save eval/sweep_results.json")
    parser.add_argument("--rrf", action="store_true", help="Also compute the RRF (lexical + semantic fusion) comparison")
    args = parser.parse_args(argv)

    eval_dir = Path(__file__).resolve().parent
    pkg_dir = eval_dir.parent
    repo_dir = Path(args.dir).resolve()

    tiers = [args.tier] if args.tier else None
    fixtures = load_fixtures(eval_dir, tiers)
    if not fixtures:
        print(f"no fixture files found in {eval_dir}", file=sys.stderr)
        return 1

    cache: dict[tuple[str, float], tuple[dict[str, Any], float]] = {}
    output: dict[str, Any] = {}

    if args.sweep:
        per_alpha = {}
        for a in SWEEP_ALPHAS:
            print(f"running sweep alpha={a}...", file=sys.stderr)
            per_alpha[str(a)] = run_eval_alpha(pkg_dir, repo_dir, fixtures, a, args.limit, args.timeout, cache)
        output["sweep"] = {"alphas": SWEEP_ALPHAS, "results": per_alpha}
    else:
        output["alpha_run"] = run_eval_alpha(pkg_dir, repo_dir, fixtures, args.alpha, args.limit, args.timeout, cache)

    if args.rrf:
        print("running RRF comparison...", file=sys.stderr)
        output["rrf"] = run_eval_rrf(pkg_dir, repo_dir, fixtures, args.limit, args.timeout, cache)

    print_summary(output, file=sys.stderr)

    if args.sweep:
        sweep_path = eval_dir / "sweep_results.json"
        sweep_path.write_text(json.dumps(output, indent=2))
        print(f"\nsweep results written to {sweep_path}", file=sys.stderr)

    json.dump(output, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
