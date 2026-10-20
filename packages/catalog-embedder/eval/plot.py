"""Render the search eval figure from results.json.

One axis: % of the relevant entries each engine surfaced, pooled over the queries of each
style (found / should have found), labeled with the counts. For name queries the one
relevant entry is the named tool.

Run: `uv run python eval/plot.py` (after `run_eval.py` has written results.json).
Regenerates eval/search_eval.png in place.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

EVAL_DIR = Path(__file__).parent

GROUPS = ("name", "keyword", "description", "keyword_list")
GROUP_TITLES = {"name": "Exact name", "keyword": "Keyword", "description": "Plain-language", "keyword_list": "Keyword list"}
ENGINES = ("substring", "lexical", "lexical+semantic")
ENGINE_LABELS = {"substring": "substring", "lexical": "lexical", "lexical+semantic": "lexical +\nsemantic"}

# Reference palette: categorical slots 1-2 (validated), muted ink for the baseline.
SURFACE = "#fcfcfb"
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRIDLINE = "#e1e0d9"
AXIS = "#c3c2b7"
LEXICAL_COLOR = "#2a78d6"
SEMANTIC_COLOR = "#eb6834"
ENGINE_COLORS = {"substring": INK_MUTED, "lexical": LEXICAL_COLOR, "lexical+semantic": LEXICAL_COLOR}

BAR_WIDTH = 0.24
BAR_SPACING = 0.3


def _segments(group: str, engine: str, stats: dict) -> tuple[int, int, int]:
    """(found by lexical-or-solid, found by semantic, should have found), summed over the group."""
    engine_stats = stats[group]["engines"][engine]
    total = engine_stats["relevant_total_sum"]
    if engine != "lexical+semantic":
        return engine_stats["relevant_found_sum"], 0, total
    channel = engine_stats["relevant_found_by_channel_sum"]
    return channel["lexical"], channel["semantic"], total


def main() -> None:
    results = json.loads((EVAL_DIR / "results.json").read_text(encoding="utf-8"))
    stats = results["aggregate_by_type_engine"]

    fig, ax = plt.subplots(figsize=(10, 5), dpi=150, facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    axis_transform = ax.get_xaxis_transform()

    for g, group in enumerate(GROUPS):
        for i, engine in enumerate(ENGINES):
            x = g + (i - 1) * BAR_SPACING
            lexical, semantic, total = _segments(group, engine, stats)
            found = lexical + semantic
            ax.bar(x, lexical / total, BAR_WIDTH, color=ENGINE_COLORS[engine], edgecolor=SURFACE, linewidth=1.5)
            if semantic:
                ax.bar(x, semantic / total, BAR_WIDTH, bottom=lexical / total, color=SEMANTIC_COLOR, hatch="//",
                       edgecolor=SURFACE, linewidth=1.5)
            ax.text(x, found / total + 0.01, f"{found / total * 100:.0f}%", ha="center", va="bottom", fontsize=9,
                    fontweight="bold", color=INK_PRIMARY)
            ax.text(x, found / total + 0.065, f"{found}/{total}", ha="center", va="bottom", fontsize=7,
                    color=INK_SECONDARY)
            ax.text(x, -0.02, ENGINE_LABELS[engine], ha="center", va="top", fontsize=7.5, color=INK_SECONDARY,
                    transform=axis_transform)
        ax.text(g, -0.13, GROUP_TITLES[group], ha="center", va="top", fontsize=10, fontweight="bold",
                color=INK_PRIMARY, transform=axis_transform)

    ax.set_xticks([])
    ax.set_xlim(-0.55, len(GROUPS) - 0.45)
    ax.set_ylim(0, 1.15)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0], ["0%", "25%", "50%", "75%", "100%"])
    ax.set_ylabel("Relevant entries surfaced", color=INK_SECONDARY, fontsize=9)
    ax.tick_params(axis="y", colors=INK_MUTED, labelsize=8, length=0)
    ax.grid(axis="y", color=GRIDLINE, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)

    ax.set_title("Catalog search vs. plain substring search", loc="left", fontsize=13, fontweight="bold",
                 color=INK_PRIMARY, pad=28)
    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=INK_MUTED, label="substring search (baseline)"),
        plt.Rectangle((0, 0), 1, 1, color=LEXICAL_COLOR, label="lexical match"),
        plt.Rectangle((0, 0), 1, 1, facecolor=SEMANTIC_COLOR, edgecolor=SURFACE, hatch="//", label="semantic match"),
    ]
    ax.legend(handles=legend_handles, loc="lower left", bbox_to_anchor=(0, 1.0), ncol=3, fontsize=8, frameon=False,
              labelcolor=INK_SECONDARY)

    fig.subplots_adjust(left=0.08, right=0.98, top=0.84, bottom=0.2)
    fig.savefig(EVAL_DIR / "search_eval.png", facecolor=SURFACE)
    print(f"wrote {EVAL_DIR / 'search_eval.png'}")


if __name__ == "__main__":
    main()
