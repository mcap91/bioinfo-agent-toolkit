"""Generate eval/recall_vs_alpha.png from eval/sweep_results.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_sweep(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def plot_sweep(data: dict[str, Any], output_path: Path) -> None:
    sweep = data.get("sweep")
    if sweep is None:
        raise ValueError("input file has no 'sweep' key — run `python run_eval.py --sweep` first")

    alphas: list[float] = sweep["alphas"]
    results: dict[str, Any] = sweep["results"]

    tier_ids = sorted({tier for a in alphas for tier in results[str(a)]["tiers"]}, key=int)

    fig, ax = plt.subplots(figsize=(8, 6))

    for tier in tier_ids:
        y = [results[str(a)]["tiers"][tier]["aggregate"]["recall@5"] for a in alphas]
        topics = results[str(alphas[0])]["tiers"][tier].get("topics")
        label = f"tier {tier} ({topics} topics)" if topics else f"tier {tier}"
        ax.plot(alphas, y, marker="o", label=label)

    overall_by_alpha = {a: results[str(a)]["overall"]["recall@5"] for a in alphas}
    baseline = overall_by_alpha.get(0.0)
    best_alpha = max(overall_by_alpha, key=overall_by_alpha.get)
    best_recall = overall_by_alpha[best_alpha]

    rrf = data.get("rrf")
    if rrf is not None:
        rrf_recall = rrf["overall"]["recall@5"]
        ax.axhline(rrf_recall, color="black", linestyle="--", linewidth=1.5, label=f"RRF (k=60): {rrf_recall:.3f}")

    if baseline is not None and baseline > 0:
        improvement_pct = (best_recall - baseline) / baseline * 100
        annotation = (
            f"best alpha={best_alpha:.2f}: recall@5={best_recall:.3f}\n"
            f"{improvement_pct:+.1f}% vs lexical-only (alpha=0.0)"
        )
        ax.annotate(
            annotation,
            xy=(best_alpha, best_recall),
            xytext=(0.5, 0.05),
            textcoords="axes fraction",
            ha="center",
            fontsize=9,
            bbox=dict(boxstyle="round", fc="white", ec="gray", alpha=0.9),
            arrowprops=dict(arrowstyle="->", color="gray"),
        )

    ax.set_xlabel("alpha (0.0 = lexical only, 1.0 = semantic only)")
    ax.set_ylabel("recall@5")
    ax.set_title("Recall@5 vs blend weight (alpha)")
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(0, 1.05)
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)


def main(argv: list[str] | None = None) -> int:
    default_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        prog="plot.py",
        description="Plot recall@5 vs alpha from eval/sweep_results.json",
    )
    parser.add_argument("--input", type=Path, default=default_dir / "sweep_results.json", help="Path to sweep_results.json")
    parser.add_argument("--output", type=Path, default=default_dir / "recall_vs_alpha.png", help="Path to write the PNG")
    args = parser.parse_args(argv)

    if not args.input.exists():
        print(f"error: {args.input} not found — run `python run_eval.py --sweep` first", file=sys.stderr)
        return 1

    data = load_sweep(args.input)
    plot_sweep(data, args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
