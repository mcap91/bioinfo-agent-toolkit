"""Render the four-group search eval figure from results.json.

Run: `uv run python eval/plot.py` (after `run_eval.py` has written results.json).
Regenerates eval/search_eval.png in place.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

EVAL_DIR = Path(__file__).parent

GROUPS = ("name", "keyword", "description", "keyword_list")
ENGINES = ("old", "lexical", "lexical+semantic")
ENGINE_COLORS = {"old": "#718096", "lexical": "#2b6cb0", "lexical+semantic": "#2b6cb0"}
SEMANTIC_COLOR = "#ed8936"

BAR_WIDTH = 0.25
GROUP_GAP = 1.0


def _bar_segments(group: str, engine: str, stats: dict) -> tuple[float, float]:
    """(solid segment, hatched-semantic segment) for one bar; they sum to the bar."""
    engine_stats = stats[group]["engines"][engine]
    if group == "name":
        if engine != "lexical+semantic":
            return engine_stats["found_at_1_rate"], 0.0
        split = engine_stats["found_at_1_by_match_type"]
        return split["lexical"], split["semantic"]
    if engine != "lexical+semantic":
        return engine_stats["topic_recall_mean"], 0.0
    channel = engine_stats["recall_by_channel_mean"]
    return channel["lexical"], channel["semantic"]


def main() -> None:
    results = json.loads((EVAL_DIR / "results.json").read_text(encoding="utf-8"))
    stats = results["aggregate_by_type_engine"]

    fig, ax = plt.subplots(figsize=(11, 5), dpi=150)
    x_ticks = []
    x_labels = []

    for group_index, group in enumerate(GROUPS):
        base_x = group_index * GROUP_GAP
        for engine_index, engine in enumerate(ENGINES):
            x = base_x + (engine_index - 1) * BAR_WIDTH
            base_segment, semantic_segment = _bar_segments(group, engine, stats)
            ax.bar(x, base_segment, BAR_WIDTH, color=ENGINE_COLORS[engine])
            if semantic_segment:
                ax.bar(x, semantic_segment, BAR_WIDTH, bottom=base_segment, color=SEMANTIC_COLOR, hatch="//")
            if group != "name":
                precision = stats[group]["engines"][engine]["topic_precision_mean"]
                ax.text(x, base_segment + semantic_segment + 0.02, f"{precision:.2f}", ha="center", fontsize=7)
        x_ticks.append(base_x)
        candidates = stats[group]["lexical_candidates_mean"]
        x_labels.append(f"{group}\n(lexical candidates: {candidates:.1f})")

    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels)
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("found@1 (name group) / topic recall (other groups)")
    ax.set_title("Search eval: old vs lexical vs lexical+semantic")

    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=ENGINE_COLORS["old"], label="old"),
        plt.Rectangle((0, 0), 1, 1, color=ENGINE_COLORS["lexical"], label="lexical"),
        plt.Rectangle((0, 0), 1, 1, color=SEMANTIC_COLOR, hatch="//", label="semantic (lexical+semantic)"),
    ]
    ax.legend(handles=legend_handles, loc="upper right", fontsize=8)
    ax.grid(axis="y", alpha=0.2)

    fig.tight_layout()
    fig.savefig(EVAL_DIR / "search_eval.png")
    print(f"wrote {EVAL_DIR / 'search_eval.png'}")


if __name__ == "__main__":
    main()
