"""catalog/sources/instagram/<reel-id>.md rendering + raw artifacts beside it
(build step 2, mirroring sources.py's role for Reddit, R8).

OR-3: tools are listed as unverified hints (raw `{name, url}` dicts straight
from the read) — there is no verified/unverified status, because the
capture never checks a URL at all anymore."""

from __future__ import annotations

from pathlib import Path

from catalog_capture.instagram_sources import render_instagram_source_md, write_instagram_source_files


def test_source_md_has_every_required_field():
    tools = [
        {"name": "Clean Your TV", "url": "https://github.com/Gathin23/cleanyourtv"},
        {"name": "Claude Code", "url": "code.claude.com"},
    ]
    md = render_instagram_source_md(
        reel_url="https://www.instagram.com/reel/De5smNojeZm/",
        captured_at="2026-10-26",
        versions={"yt-dlp": "2026.10.26", "faster-whisper": "1.2.1"},
        caption="a caption",
        transcript_text="[   0.0] hi",
        on_screen_text="restore.sh",
        key_claims=["claim one"],
        info_channel="spoken",
        tools=tools,
    )
    assert md.startswith("reel: https://www.instagram.com/reel/De5smNojeZm/\n")
    assert "captured: 2026-10-26" in md
    assert "yt-dlp: 2026.10.26" in md
    assert "a caption" in md
    assert "[   0.0] hi" in md
    assert "restore.sh" in md
    assert "claim one" in md
    assert "spoken" in md
    # Why: OR-3 — hints, not verification status.
    assert "## Mentioned (unverified hints)" in md
    assert "- Clean Your TV: https://github.com/Gathin23/cleanyourtv" in md
    assert "- Claude Code: code.claude.com" in md
    assert " — verified" not in md and " — unverified" not in md  # no leftover per-tool status wording


def test_no_tools_mentioned_renders_as_none():
    md = render_instagram_source_md(
        reel_url="x", captured_at="2026-10-26", versions={}, caption=None,
        transcript_text="t", on_screen_text="", key_claims=[], info_channel="", tools=[],
    )
    assert "## Mentioned (unverified hints)\n\n(none mentioned)" in md


def test_tool_with_no_url_renders_as_no_url_hint():
    md = render_instagram_source_md(
        reel_url="x", captured_at="2026-10-26", versions={}, caption=None,
        transcript_text="t", on_screen_text="", key_claims=[], info_channel="",
        tools=[{"name": "some CLI", "url": None}],
    )
    assert "- some CLI: (no url)" in md


def test_write_source_files_writes_md_and_raw_artifacts_no_audio_video(tmp_path: Path):
    sheet = tmp_path / "sheet.jpg"
    sheet.write_bytes(b"\xff\xd8\xff fake jpeg")

    out_path = write_instagram_source_files(
        tmp_path / "sources", "De5smNojeZm", "reel: x\n",
        info_json_text='{"description": "x"}', transcript_text="[0.0] hi",
        sheet_path=sheet, read_response_text='{"type":"result"}',
    )
    assert out_path == tmp_path / "sources" / "instagram" / "De5smNojeZm.md"
    assert out_path.read_text(encoding="utf-8") == "reel: x\n"

    artifacts = tmp_path / "sources" / "instagram" / "De5smNojeZm"
    assert (artifacts / "info.json").read_text(encoding="utf-8") == '{"description": "x"}'
    assert (artifacts / "transcript.txt").read_text(encoding="utf-8") == "[0.0] hi"
    assert (artifacts / "sheet.jpg").read_bytes() == b"\xff\xd8\xff fake jpeg"
    assert (artifacts / "read_response.jsonl").read_text(encoding="utf-8") == '{"type":"result"}'
    # Why: build step 2 explicitly excludes audio/video from the raw artifacts.
    assert not (artifacts / "audio.m4a").exists()
    assert not (artifacts / "video.mp4").exists()
    assert set(p.name for p in artifacts.iterdir()) == {"info.json", "transcript.txt", "sheet.jpg", "read_response.jsonl"}
