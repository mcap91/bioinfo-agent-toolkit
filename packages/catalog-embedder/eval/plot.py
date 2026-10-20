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
ENGINES = ("substring", "lexical", "lexical+semantic")

# Group captions: what the query looks like (a real query from queries.json) and the metric.
GROUP_CAPTIONS = {
    "name": ("Exact tool name", 'e.g. "paddleocr"', "bar: named tool returned first"),
    "keyword": ("Keyword (1–2 words)", 'e.g. "document parsing"', "bar: topic recall"),
    "description": ("Plain-language need", 'e.g. "run a chatbot model entirely\non my own laptop with no internet"', "bar: topic recall"),
    "keyword_list": ("Keyword list (4–6 words)", 'e.g. "local llm inference gpu quantization"', "bar: topic recall"),
}

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
ENGINE_LABELS = {"substring": "substring", "lexical": "lexical", "lexical+semantic": "lexical\n+ semantic"}

BAR_WIDTH = 0.22
BAR_SPACING = 0.28
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


def _pct(value: float) -> str:
    return f"{value * 100:.0f}%"


def _bar_label(group: str, engine_stats: dict, height: float) -> tuple[str, str]:
    """(headline: the bar's value, detail: topic precision or an empty-result note)."""
    if engine_stats["empty_rate"] == 1.0:
        return _pct(height), "no results"
    if group == "name":
        return _pct(height), ""
    return _pct(height), f"{_pct(engine_stats['topic_precision_mean'])} relevant"


def main() -> None:
    results = json.loads((EVAL_DIR / "results.json").read_text(encoding="utf-8"))
    stats = results["aggregate_by_type_engine"]

    fig, ax = plt.subplots(figsize=(11, 6.4), dpi=150, facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    axis_transform = ax.get_xaxis_transform()

    for group_index, group in enumerate(GROUPS):
        base_x = group_index * GROUP_GAP
        for engine_index, engine in enumerate(ENGINES):
            x = base_x + (engine_index - 1) * BAR_SPACING
            base_segment, semantic_segment = _bar_segments(group, engine, stats)
            ax.bar(x, base_segment, BAR_WIDTH, color=ENGINE_COLORS[engine], edgecolor=SURFACE, linewidth=1.5)
            if semantic_segment:
                ax.bar(
                    x,
                    semantic_segment,
                    BAR_WIDTH,
                    bottom=base_segment,
                    color=SEMANTIC_COLOR,
                    hatch="//",
                    edgecolor=SURFACE,
                    linewidth=1.5,
                )
            height = base_segment + semantic_segment
            headline, detail = _bar_label(group, stats[group]["engines"][engine], height)
            ax.text(x, height + 0.015, headline, ha="center", va="bottom", fontsize=9, fontweight="bold", color=INK_PRIMARY)
            if detail:
                ax.text(x, height + 0.075, detail, ha="center", va="bottom", fontsize=7, color=INK_SECONDARY)
            ax.text(x, -0.02, ENGINE_LABELS[engine], ha="center", va="top", fontsize=7.5, color=INK_SECONDARY, transform=axis_transform)

        title, example, metric = GROUP_CAPTIONS[group]
        candidates = stats[group]["lexical_candidates_mean"]
        ax.text(base_x, -0.11, title, ha="center", va="top", fontsize=9.5, fontweight="bold", color=INK_PRIMARY, transform=axis_transform)
        ax.text(
            base_x,
            -0.155,
            f"{example}\n{metric}\navg. lexical matches per query: {candidates:.1f}",
            ha="center",
            va="top",
            fontsize=7.5,
            color=INK_SECONDARY,
            linespacing=1.35,
            transform=axis_transform,
        )

    ax.set_xticks([])
    ax.set_xlim(-0.55, (len(GROUPS) - 1) * GROUP_GAP + 0.55)
    ax.set_ylim(0, 1.15)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0], ["0%", "20%", "40%", "60%", "80%", "100%"])
    ax.tick_params(axis="y", colors=INK_MUTED, labelsize=8, length=0)
    ax.set_ylabel("Share of correct entries found", color=INK_SECONDARY, fontsize=9)
    ax.grid(axis="y", color=GRIDLINE, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)

    fig.text(0.06, 0.965, "This repo's catalog search vs. plain substring search", fontsize=13, fontweight="bold", color=INK_PRIMARY)
    fig.text(
        0.06,
        0.93,
        "40 test queries in 4 styles, scored against an answer key labeled blind by Claude Opus 5.5",
        fontsize=9,
        color=INK_SECONDARY,
    )

    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=INK_MUTED, label="Substring search (baseline: the repo's original lookup)"),
        plt.Rectangle((0, 0), 1, 1, color=LEXICAL_COLOR, label="This repo: found by lexical match"),
        plt.Rectangle((0, 0), 1, 1, facecolor=SEMANTIC_COLOR, edgecolor=SURFACE, hatch="//", label="This repo: added by semantic match"),
    ]
    ax.legend(handles=legend_handles, loc="upper right", fontsize=8, frameon=False, labelcolor=INK_SECONDARY)

    fig.text(
        0.06,
        0.025,
        "Bold % = the bar's height.  Topic recall: share of the topic's relevant entries (answer key) that the search returned; each query is "
        "scored against its whole topic list.\n\"NN% relevant\" = topic precision: share of the returned entries that are in the answer key.",
        fontsize=7,
        color=INK_MUTED,
    )

    fig.subplots_adjust(left=0.06, right=0.98, top=0.86, bottom=0.30)
    fig.savefig(EVAL_DIR / "search_eval.png", facecolor=SURFACE)
    print(f"wrote {EVAL_DIR / 'search_eval.png'}")


if __name__ == "__main__":
    main()
