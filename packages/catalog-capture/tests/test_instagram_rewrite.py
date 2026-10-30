"""Instagram needs-link rewrite (OR-3): one fenced block per reel, and the
capture-failed path. Uses a fake `capture_fn` returning a real
`InstagramCaptureResult` shape (no network, no subprocess) — the shape
itself is exercised for real in test_instagram_golden_fixture.py.

OR-3 (operator ruling, supersedes G1/G2/I1/I2/I9): the capture never
verifies a tool's URL or picks what the reel is "about" — `source:` is
always the reel URL, and whatever the read spotted is listed in the block as
unverified hints for the processing agent to judge."""

from __future__ import annotations

from pathlib import Path

import pytest

from catalog_capture.adapters.instagram_reel import (
    INSTAGRAM_NEEDS_LINK_RE,
    InstagramCaptureError,
    InstagramCaptureResult,
    InstagramReelAdapter,
)
from catalog_capture.registry import process_needs_link

from conftest import ts_parse_inbox

REEL_URL = "https://www.instagram.com/reel/De5smNojeZm/"


def _fake_result(reel_id: str = "De5smNojeZm", tools: list[dict] | None = None) -> InstagramCaptureResult:
    return InstagramCaptureResult(
        reel_id=reel_id,
        reel_url=REEL_URL,
        info_json_text='{"description": "cap"}',
        caption="a caption",
        transcript_text="[   0.0] a transcript",
        sheet_path=Path("/dev/null"),  # not read by the rewrite layer; sheet_is_temp defaults False
        on_screen_text="restore.sh",
        key_claims=["claim one"],
        info_channel="spoken",
        tools=tools or [],
        read_raw_stdout='{"type":"result"}',
        read_usd=0.01,
        versions={"yt-dlp": "2026.10.26"},
    )


def _process(text, *, sources_dir, capture_fn, limit=None):
    adapters = [InstagramReelAdapter(capture_fn=capture_fn)]
    return process_needs_link(text, sources_dir=sources_dir, adapters=adapters, limit=limit, delay_s=0)


# -- NEEDS_LINK_RE: what is/isn't matched ----------------------------------


@pytest.mark.parametrize(
    "line",
    [
        "⚠ needs-link https://www.instagram.com/reel/De5smNojeZm/",
        "⚠ needs-link https://instagram.com/reel/De5smNojeZm/",  # bare host
        "⚠ needs-link instagram.com/reel/De5smNojeZm/",  # scheme-less
        "⚠ needs-link https://www.instagram.com/reel/De5smNojeZm",  # no trailing slash
        "⚠ needs-link https://www.instagram.com/reel/De5smNojeZm/?utm_source=ig_web",  # query
    ],
)
def test_reel_line_variants_are_matched(line: str):
    # Why: these are the real shapes a pasted/redirected Instagram reel link
    # can take (WK-0080 corpus is 26/26 `/reel/` — WK-0079 media-type probe).
    assert INSTAGRAM_NEEDS_LINK_RE.match(line)


def test_carousel_line_is_not_matched():
    # Why: `/p/` carousels are a separate, not-yet-built adapter (WK-0087) —
    # this adapter must not silently mishandle one by matching it; it should
    # stay `⚠ needs-link` untouched.
    line = "⚠ needs-link https://www.instagram.com/p/DeCarousel/"
    assert not INSTAGRAM_NEEDS_LINK_RE.match(line)


# -- Block rendering: OR-3 one block per reel --------------------------------


def test_one_block_per_reel_with_source_as_the_reel_url():
    # Why: OR-3 — capture never decides what a reel is "about"; every reel
    # gets exactly one block, `source:` is always the reel URL itself, no
    # matter how many (or few) tools the read mentions.
    tools = [
        {"name": "Clean Your TV", "url": "github.com/Gathin23/cleanyourtv"},
        {"name": "Dumb TV", "url": "github.com/humblemuzzu/dumbtv"},
        {"name": "Claude Code", "url": "code.claude.com"},
        {"name": "ADB", "url": "developer.android.com"},
    ]

    def fake_capture(url: str) -> InstagramCaptureResult:
        return _fake_result(tools=tools)

    inbox = f"⚠ needs-link {REEL_URL}\n"
    out_text, results = _process(inbox, sources_dir=Path("/tmp/unused-sources"), capture_fn=fake_capture)
    assert results[0].status == "ok"
    assert results[0].mentioned_count == 4

    assert out_text.count("```text\n") == 1  # exactly one block, never N per tool
    assert out_text.startswith(f"```text\nsource: {REEL_URL}\n")
    # Why: every mentioned tool is a hint in the single block, not a source.
    assert "Mentioned (unverified hints):" in out_text
    assert "- Clean Your TV: github.com/Gathin23/cleanyourtv" in out_text
    assert "- Dumb TV: github.com/humblemuzzu/dumbtv" in out_text
    assert "- Claude Code: code.claude.com" in out_text
    assert "- ADB: developer.android.com" in out_text
    assert "source: https://github.com/Gathin23/cleanyourtv" not in out_text  # no per-tool source


def test_no_tools_mentioned_still_produces_one_block():
    # Why: a reel with no tool/repo named (a technique-only reel) must still
    # resolve to exactly one block, not zero — no silent drop.
    def fake_capture(url: str) -> InstagramCaptureResult:
        return _fake_result(tools=[])

    inbox = f"⚠ needs-link {REEL_URL}\n"
    out_text, results = _process(inbox, sources_dir=Path("/tmp/unused-sources"), capture_fn=fake_capture)
    assert results[0].status == "ok"
    assert results[0].mentioned_count == 0
    assert out_text.count("```text\n") == 1
    assert f"source: {REEL_URL}" in out_text
    assert "Mentioned (unverified hints):\n(none mentioned)" in out_text


def test_tool_with_no_url_is_listed_as_a_hint_with_no_url():
    # Why: the read can name a tool it couldn't find a URL for (url: null) —
    # that must still appear as a hint, not be silently dropped from the list.
    tools = [{"name": "some unnamed CLI", "url": None}]

    def fake_capture(url: str) -> InstagramCaptureResult:
        return _fake_result(tools=tools)

    inbox = f"⚠ needs-link {REEL_URL}\n"
    out_text, _ = _process(inbox, sources_dir=Path("/tmp/unused-sources"), capture_fn=fake_capture)
    assert "- some unnamed CLI: (no url)" in out_text


def test_rewritten_block_parses_under_the_real_ts_inbox_parser(tmp_path: Path):
    def fake_capture(url: str) -> InstagramCaptureResult:
        return _fake_result(tools=[{"name": "Dumb TV", "url": "github.com/humblemuzzu/dumbtv"}])

    inbox = f"⚠ needs-link {REEL_URL}\n"
    out_text, _ = _process(inbox, sources_dir=tmp_path / "sources", capture_fn=fake_capture)
    inbox_path = tmp_path / "inbox.md"
    inbox_path.write_text(out_text, encoding="utf-8")
    items = ts_parse_inbox(inbox_path)
    assert len(items) == 1
    assert items[0]["kind"] == "text"
    assert items[0]["source"] == REEL_URL
    assert items[0]["blocked"] is False  # R6-equivalent: text items skip the url-only block rule
    assert "a caption" in items[0]["content"]
    assert "restore.sh" in items[0]["content"]
    assert "Dumb TV" in items[0]["content"]


# -- Capture failure path ----------------------------------------------------


def test_capture_failure_becomes_capture_failed_marker():
    # Why: no silent drops (build step 2) — every needs-link line ends as a
    # block or a ⚠ capture-failed line naming the stage and the error.
    def failing_capture(url: str) -> InstagramCaptureResult:
        raise InstagramCaptureError("audio", "yt-dlp bestaudio exit 1")

    inbox = f"⚠ needs-link {REEL_URL}\n"
    out_text, results = _process(inbox, sources_dir=Path("/tmp/unused-sources"), capture_fn=failing_capture)
    assert results[0].status == "failed"
    assert out_text == f"⚠ capture-failed {REEL_URL} — audio: yt-dlp bestaudio exit 1\n"


def test_unexpected_exception_also_becomes_capture_failed_marker():
    # Why: fail loud even on an exception type the pipeline didn't anticipate
    # — never let an unhandled error silently drop the line.
    def exploding_capture(url: str) -> InstagramCaptureResult:
        raise ValueError("boom")

    inbox = f"⚠ needs-link {REEL_URL}\n"
    out_text, results = _process(inbox, sources_dir=Path("/tmp/unused-sources"), capture_fn=exploding_capture)
    assert results[0].status == "failed"
    assert out_text == f"⚠ capture-failed {REEL_URL} — boom\n"


def test_limit_caps_how_many_lines_are_processed():
    calls = []

    def fake_capture(url: str) -> InstagramCaptureResult:
        calls.append(url)
        return _fake_result()

    inbox = (
        "⚠ needs-link https://www.instagram.com/reel/aaaaaaaaaaa/\n"
        "⚠ needs-link https://www.instagram.com/reel/bbbbbbbbbbb/\n"
    )
    out_text, results = _process(inbox, sources_dir=Path("/tmp/unused-sources"), capture_fn=fake_capture, limit=1)
    assert len(results) == 1
    assert len(calls) == 1
    assert len(INSTAGRAM_NEEDS_LINK_RE.findall(out_text)) == 1  # the second line stays untouched
