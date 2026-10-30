"""Shared review module (WK-0094 Phase B), exercised against the real Reddit
and reel golden fixtures — not hand-written fixtures. `review build`
replaces the reel-only `make_review.py` for every adapter; this file proves
it renders sheets, the index, and a verdict tally for both, and that it
never pre-fills a verdict (WK-0079 OR-2: finder != verifier)."""

from __future__ import annotations

from pathlib import Path

from catalog_capture import review
from catalog_capture.adapters.instagram_reel import InstagramCaptureResult, InstagramReelAdapter
from catalog_capture.adapters.reddit import RedditAdapter
from catalog_capture.registry import process_needs_link
from catalog_capture.stages.browser import CaptureResult

REDDIT_SHARE_URL = "https://www.reddit.com/r/LocalLLaMA/s/JNjEe87YeN"
REDDIT_FINAL_URL = (
    "https://www.reddit.com/r/LocalLLaMA/comments/1x9gfnb/"
    "google_open_sources_harness2_for_self_improving/"
)
REEL_URL = "https://www.instagram.com/reel/De5smNojeZm/"


def _write_real_sources(tmp_path: Path, golden_capture, golden_instagram_artifacts) -> Path:
    """Runs the real registry pipeline (not hand-built sources files) for one
    real Reddit capture and one real reel capture, so the review module is
    exercised against what the pipeline actually writes."""
    import json
    import re

    from catalog_capture.stages.read import parse_claude_stream_result

    _, reddit_body = golden_capture

    def reddit_capture(url: str) -> CaptureResult:
        return CaptureResult(
            final_url=REDDIT_FINAL_URL,
            title="t",
            body_text=reddit_body,
            playwright_version="1.64.1",
            chromium_version="156.0.8078.4",
        )

    info = json.loads(golden_instagram_artifacts["info_json_text"])
    parsed = parse_claude_stream_result(golden_instagram_artifacts["read_response_text"])
    m = re.search(r"\{.*\}", parsed["result_text"], re.DOTALL)
    obj = json.loads(m.group(0))
    ig_cap = InstagramCaptureResult(
        reel_id="De5smNojeZm",
        reel_url=REEL_URL,
        info_json_text=golden_instagram_artifacts["info_json_text"],
        caption=info["description"],
        transcript_text=golden_instagram_artifacts["transcript_text"],
        sheet_path=golden_instagram_artifacts["sheet_path"],
        on_screen_text=obj["on_screen_text"],
        key_claims=[str(c) for c in obj["key_claims"]],
        info_channel=obj["info_channel"],
        tools=[{"name": t.get("name"), "url": t.get("url")} for t in obj["tools"]],
        read_raw_stdout=golden_instagram_artifacts["read_response_text"],
        versions={"yt-dlp": "2026.10.26"},
        sheet_is_temp=False,
    )

    def instagram_capture(url: str) -> InstagramCaptureResult:
        return ig_cap

    sources_dir = tmp_path / "sources"
    adapters = [RedditAdapter(capture_fn=reddit_capture), InstagramReelAdapter(capture_fn=instagram_capture)]
    inbox = f"⚠ needs-link {REDDIT_SHARE_URL}\n⚠ needs-link {REEL_URL}\n"
    _, results = process_needs_link(inbox, sources_dir=sources_dir, adapters=adapters, delay_s=0)
    assert [r.status for r in results] == ["ok", "ok"]
    return sources_dir


def test_review_build_renders_sheets_index_and_tally_for_reddit_and_reel(
    tmp_path: Path, golden_capture, golden_instagram_artifacts
):
    sources_dir = _write_real_sources(tmp_path, golden_capture, golden_instagram_artifacts)

    reddit_adapter = RedditAdapter()
    reel_adapter = InstagramReelAdapter()
    items = reddit_adapter.review_items(sources_dir) + reel_adapter.review_items(sources_dir)
    assert len(items) == 2
    assert {i.adapter for i in items} == {"reddit", "instagram_reel"}

    out_dir = tmp_path / "review"
    index_path = review.build_review(
        items, out_dir, adapters={"reddit": reddit_adapter, "instagram_reel": reel_adapter}
    )

    # One sheet per item, named <adapter>-<id>.md.
    sheet_paths = sorted(p for p in out_dir.glob("*.md") if p.name != "REVIEW.md")
    assert len(sheet_paths) == 2
    assert index_path == out_dir / "REVIEW.md"
    assert index_path.exists()

    index_text = index_path.read_text(encoding="utf-8")
    assert "## Suggested spot-check sample" in index_text
    assert "## All 2 items" in index_text
    for item in items:
        assert item.url in index_text

    # A sheet has the link, the empty Verdict/Notes lines, and its sections.
    for path in sheet_paths:
        text = path.read_text(encoding="utf-8")
        assert "**Verdict:**" in text
        assert "**Notes:**" in text
        assert "## What we captured" in text
        # Never pre-filled — WK-0079 OR-2 (finder != verifier).
        assert review.extract_verdict(text) == ""

    # Tally over freshly-built sheets: both unchecked.
    result = review.tally(out_dir)
    assert result["n"] == 2
    assert result["counts"] == {"unchecked": 2}
    assert result["unrecognized"] == []


def test_review_never_writes_a_verdict_even_with_a_small_sample_cap(tmp_path: Path, golden_capture, golden_instagram_artifacts):
    sources_dir = _write_real_sources(tmp_path, golden_capture, golden_instagram_artifacts)
    reddit_adapter = RedditAdapter()
    reel_adapter = InstagramReelAdapter()
    items = reddit_adapter.review_items(sources_dir) + reel_adapter.review_items(sources_dir)

    out_dir = tmp_path / "review"
    review.build_review(items, out_dir, cap=1)  # WK-0094 OR-5: cap <= 5

    for path in out_dir.glob("*.md"):
        if path.name == "REVIEW.md":
            continue
        assert review.extract_verdict(path.read_text(encoding="utf-8")) == ""


def test_sample_is_capped_at_five_even_with_more_items():
    # 12 distinct fake "adapters" so the default rule ("first item of each
    # adapter") would naturally pick all 12 absent the hard cap.
    items = [review.ReviewItem(adapter=f"fake{i}", item_id="x", url=f"https://x.test/{i}") for i in range(12)]
    sample = review.suggest_sample(items, cap=5)
    assert len(sample) <= review.SAMPLE_CAP
    assert len(sample) == 5


def test_sample_default_rule_does_not_invent_extra_picks_for_one_adapter():
    # 12 items from the *same* adapter, no bespoke sample_reason supplied —
    # the default rule picks one ("first captured"), not an arbitrary fill
    # up to the cap; OR-5's cap is a ceiling, not a target.
    items = [review.ReviewItem(adapter="fake", item_id=f"item{i}", url=f"https://x.test/{i}") for i in range(12)]
    sample = review.suggest_sample(items, cap=5)
    assert len(sample) == 1
    assert sample[0][1] == "first captured"


def test_tally_after_the_operator_fills_in_a_verdict(tmp_path: Path):
    out_dir = tmp_path / "review"
    out_dir.mkdir()
    item = review.ReviewItem(adapter="fake", item_id="x", url="https://x.test", sections=[("What we captured", "body")])
    review.write_sheets([item], out_dir)
    sheet_path = out_dir / review.sheet_filename(item)

    # Simulate the operator's own edit (never done by this module itself).
    text = sheet_path.read_text(encoding="utf-8")
    text = text.replace("**Verdict:** <!-- yes / good enough / wrong / no / missed <x> -->", "**Verdict:** yes")
    sheet_path.write_text(text, encoding="utf-8")

    result = review.tally(out_dir)
    assert result["n"] == 1
    assert result["counts"] == {"yes": 1}


def test_classify_verdict_recognizes_every_allowed_value_and_missed_x():
    for value in ["yes", "good enough", "wrong", "no"]:
        assert review.classify_verdict(value) == value
    assert review.classify_verdict("missed the repo link") == "missed"
    assert review.classify_verdict("") == "unchecked"
    assert review.classify_verdict("maybe?") == "unrecognized"
