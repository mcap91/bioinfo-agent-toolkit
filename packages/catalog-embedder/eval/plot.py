"""Render the search eval figure from results.json.

Two panels: exact-name queries (% with the named tool ranked first) and topic queries
(relevant results returned per query). Recall and precision are reported in the README.

Run: `uv run python eval/plot.py` (after `run_eval.py` has written results.json).
Regenerates eval/search_eval.png in place.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

EVAL_DIR = Path(__file__).parent

TOPIC_GROUPS = ("keyword", "description", "keyword_list")
GROUP_TITLES = {"keyword": "Keyword", "description": "Plain-language", "keyword_list": "Keyword list"}
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


def _name_segments(engine: str, stats: dict) -> tuple[float, float]:
    """(lexical-or-solid, semantic) share of name queries with the named tool ranked first."""
    engine_stats = stats["name"]["engines"][engine]
    if engine != "lexical+semantic":
        return engine_stats["found_at_1_rate"], 0.0
    split = engine_stats["found_at_1_by_match_type"]
    return split["lexical"], split["semantic"]


def _count_segments(group: str, engine: str, stats: dict) -> tuple[float, float]:
    """(lexical-or-solid, semantic) relevant results returned per query."""
    engine_stats = stats[group]["engines"][engine]
    if engine != "lexical+semantic":
        return engine_stats["relevant_found_mean"], 0.0
    channel = engine_stats["relevant_found_by_channel_mean"]
    return channel["lexical"], channel["semantic"]


def _draw_bar(ax, x: float, engine: str, solid: float, semantic: float, label: str) -> None:
    ax.bar(x, solid, BAR_WIDTH, color=ENGINE_COLORS[engine], edgecolor=SURFACE, linewidth=1.5)
    if semantic:
        ax.bar(x, semantic, BAR_WIDTH, bottom=solid, color=SEMANTIC_COLOR, hatch="//", edgecolor=SURFACE, linewidth=1.5)
    ax.text(x, solid + semantic, label, ha="center", va="bottom", fontsize=9, fontweight="bold", color=INK_PRIMARY)
    ax.text(x, -0.02, ENGINE_LABELS[engine], ha="center", va="top", fontsize=7.5, color=INK_SECONDARY,
            transform=ax.get_xaxis_transform())


def _style(ax, title: str) -> None:
    ax.set_facecolor(SURFACE)
    ax.set_title(title, fontsize=10, fontweight="bold", color=INK_PRIMARY, pad=10)
    ax.set_xticks([])
    ax.tick_params(axis="y", colors=INK_MUTED, labelsize=8, length=0)
    ax.grid(axis="y", color=GRIDLINE, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)


def main() -> None:
    results = json.loads((EVAL_DIR / "results.json").read_text(encoding="utf-8"))
    stats = results["aggregate_by_type_engine"]

    fig, (ax_name, ax_topic) = plt.subplots(
        1, 2, figsize=(10, 5), dpi=150, facecolor=SURFACE, gridspec_kw={"width_ratios": [1, 3]}
    )

    for i, engine in enumerate(ENGINES):
        solid, semantic = _name_segments(engine, stats)
        _draw_bar(ax_name, (i - 1) * BAR_SPACING, engine, solid, semantic, f"{(solid + semantic) * 100:.0f}%")
    ax_name.set_ylim(0, 1.1)
    ax_name.set_yticks([0, 0.25, 0.5, 0.75, 1.0], ["0%", "25%", "50%", "75%", "100%"])
    ax_name.set_xlim(-0.55, 0.55)
    _style(ax_name, "Exact tool name\n% ranked first")

    top = 0.0
    for g, group in enumerate(TOPIC_GROUPS):
        for i, engine in enumerate(ENGINES):
            solid, semantic = _count_segments(group, engine, stats)
            top = max(top, solid + semantic)
            _draw_bar(ax_topic, g + (i - 1) * BAR_SPACING, engine, solid, semantic, f"{solid + semantic:.1f}")
        ax_topic.text(g, -0.13, GROUP_TITLES[group], ha="center", va="top", fontsize=10, fontweight="bold",
                      color=INK_PRIMARY, transform=ax_topic.get_xaxis_transform())
    ax_topic.set_ylim(0, top * 1.15)
    ax_topic.set_yticks(range(0, int(top * 1.15) + 1, 5))
    ax_topic.set_xlim(-0.55, len(TOPIC_GROUPS) - 0.45)
    _style(ax_topic, "Topic searches\nrelevant results returned per query")

    fig.suptitle("Catalog search vs. plain substring search", x=0.06, ha="left", fontsize=13, fontweight="bold",
                 color=INK_PRIMARY)
    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=INK_MUTED, label="substring search (baseline)"),
        plt.Rectangle((0, 0), 1, 1, color=LEXICAL_COLOR, label="lexical match"),
        plt.Rectangle((0, 0), 1, 1, facecolor=SEMANTIC_COLOR, edgecolor=SURFACE, hatch="//", label="semantic match"),
    ]
    fig.legend(handles=legend_handles, loc="upper right", ncol=3, fontsize=8, frameon=False, labelcolor=INK_SECONDARY,
               bbox_to_anchor=(0.98, 0.985))

    fig.subplots_adjust(left=0.06, right=0.98, top=0.8, bottom=0.2, wspace=0.12)
    fig.savefig(EVAL_DIR / "search_eval.png", facecolor=SURFACE)
    print(f"wrote {EVAL_DIR / 'search_eval.png'}")


if __name__ == "__main__":
    main()
