"""Generate eval/search_eval.png from eval/threshold_sweep_results.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

METHOD_STYLE: dict[str, dict[str, Any]] = {
    "fusion": {"color": "tab:blue", "linestyle": "-", "linewidth": 2.5},
    "semantic": {"color": "tab:orange", "linestyle": "--", "linewidth": 1.5},
    "bm25": {"color": "tab:green", "linestyle": ":", "linewidth": 1.5},
}

RECALL_TARGET = 0.95


def load_sweep(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _recommended_threshold(thresholds: list[float], recalls: list[float]) -> tuple[float, float, bool]:
    """Highest threshold where recall >= RECALL_TARGET, else the threshold with the best recall."""
    qualifying = [(t, r) for t, r in zip(thresholds, recalls) if r >= RECALL_TARGET]
    if qualifying:
        t, r = max(qualifying, key=lambda tr: tr[0])
        return t, r, True
    t, r = max(zip(thresholds, recalls), key=lambda tr: tr[1])
    return t, r, False


def plot_sweep(data: dict[str, Any], output_path: Path) -> None:
    sweep = data.get("sweep")
    if sweep is None:
        raise ValueError("input file has no 'sweep' key — run `python run_eval.py --sweep` first")

    thresholds: list[float] = sweep["thresholds"]
    methods: list[str] = sweep["methods"]
    results: dict[str, Any] = sweep["results"]

    fig, (ax_recall, ax_noise) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    for method in methods:
        overall = results[method]["overall"]
        recalls = [overall[str(t)]["recall"] for t in thresholds]
        n_results = [overall[str(t)]["n_results"] for t in thresholds]
        style = METHOD_STYLE.get(method, {})
        ax_recall.plot(thresholds, recalls, marker="o", label=method, **style)
        ax_noise.plot(thresholds, n_results, marker="o", label=method, **style)

    ax_recall.axhline(1.0, color="lightgray", linestyle="-", linewidth=1, label="perfect")

    fusion_recalls = [results["fusion"]["overall"][str(t)]["recall"] for t in thresholds]
    rec_t, rec_r, met_target = _recommended_threshold(thresholds, fusion_recalls)
    label = f"T={rec_t:g}" if met_target else f"best: T={rec_t:g}, recall={rec_r:.2f}"
    for ax in (ax_recall, ax_noise):
        ax.axvline(rec_t, color="gray", linestyle="--", linewidth=1)
    ax_recall.annotate(
        label,
        xy=(rec_t, rec_r),
        xytext=(5, -5),
        textcoords="offset points",
        fontsize=9,
        color="gray",
    )

    ax_recall.set_ylabel("Recall (fraction of expected tools found)")
    ax_recall.set_ylim(0, 1.05)
    ax_recall.grid(True, alpha=0.2)
    ax_recall.legend(loc="best", fontsize=8)
    ax_recall.set_title("Catalog search: recall vs noise at each score cutoff")

    ax_noise.set_xlabel("Score threshold")
    ax_noise.set_ylabel("Mean results per query")
    ax_noise.grid(True, alpha=0.2)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)


def main(argv: list[str] | None = None) -> int:
    default_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        prog="plot.py",
        description="Plot recall and result-count by score threshold from eval/threshold_sweep_results.json",
    )
    parser.add_argument("--input", type=Path, default=default_dir / "threshold_sweep_results.json", help="Path to threshold_sweep_results.json")
    parser.add_argument("--output", type=Path, default=default_dir / "search_eval.png", help="Path to write the PNG")
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
