"""catalog/sources/instagram/<reel-id>.md rendering + raw artifacts beside it
(the Instagram reel adapter's `build_outcome` plus the shared
`sources_writer`, mirroring the Reddit adapter's role, R8).

OR-3: tools are listed as unverified hints (raw `{name, url}` dicts straight
from the read) — there is no verified/unverified status, because the
capture never checks a URL at all anymore."""

from __future__ import annotations

from pathlib import Path

from catalog_capture.adapters.instagram_reel import InstagramCaptureResult, InstagramReelAdapter
from catalog_capture.sources_writer import render_source_md, write_source_file

ADAPTER = InstagramReelAdapter()


def _build_outcome(**overrides) -> tuple:
    defaults = dict(
        reel_id="De5smNojeZm",
        reel_url="https://www.instagram.com/reel/De5smNojeZm/",
        info_json_text="{}",
        caption=None,
        transcript_text="t",
        sheet_path=Path("/dev/null"),
        on_screen_text="",
        key_claims=[],
        info_channel="",
        tools=[],
        read_raw_stdout="{}",
        versions={},
    )
    defaults.update(overrides)
    raw = InstagramCaptureResult(**defaults)
    outcome = ADAPTER.build_outcome(raw, captured_at="2026-10-26")
    md = render_source_md(header_lines=outcome.source_header_lines, body=outcome.source_body)
    return outcome, md


def test_source_md_has_every_required_field():
    tools = [
        {"name": "Clean Your TV", "url": "https://github.com/Gathin23/cleanyourtv"},
        {"name": "Claude Code", "url": "code.claude.com"},
    ]
    _, md = _build_outcome(
        reel_url="https://www.instagram.com/reel/De5smNojeZm/",
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
    _, md = _build_outcome(reel_url="x", transcript_text="t", tools=[])
    assert "## Mentioned (unverified hints)\n\n(none mentioned)" in md


def test_tool_with_no_url_renders_as_no_url_hint():
    _, md = _build_outcome(reel_url="x", transcript_text="t", tools=[{"name": "some CLI", "url": None}])
    assert "- some CLI: (no url)" in md


def test_write_source_files_writes_md_and_raw_artifacts_no_audio_video(tmp_path: Path):
    sheet = tmp_path / "sheet.jpg"
    sheet.write_bytes(b"\xff\xd8\xff fake jpeg")

    outcome, md = _build_outcome(
        reel_id="De5smNojeZm", reel_url="x", info_json_text='{"description": "x"}',
        transcript_text="[0.0] hi", sheet_path=sheet, read_raw_stdout='{"type":"result"}',
    )
    assert md == "reel: x\ncaptured: 2026-10-26\n\n## Caption\n\n(no caption captured)\n\n## Transcript\n\n[0.0] hi\n\n## On-screen text\n\n(none)\n\n## Key claims\n\n(none)\n\n## Info channel\n\n(unknown)\n\n## Mentioned (unverified hints)\n\n(none mentioned)\n"

    out_path = write_source_file(tmp_path / "sources", "instagram", outcome.id, md, artifacts=outcome.artifacts)
    assert out_path == tmp_path / "sources" / "instagram" / "De5smNojeZm.md"
    assert out_path.read_text(encoding="utf-8") == md

    artifacts = tmp_path / "sources" / "instagram" / "De5smNojeZm"
    assert (artifacts / "info.json").read_text(encoding="utf-8") == '{"description": "x"}'
    assert (artifacts / "transcript.txt").read_text(encoding="utf-8") == "[0.0] hi"
    assert (artifacts / "sheet.jpg").read_bytes() == b"\xff\xd8\xff fake jpeg"
    assert (artifacts / "read_response.jsonl").read_text(encoding="utf-8") == '{"type":"result"}'
    # Why: build step 2 explicitly excludes audio/video from the raw artifacts.
    assert not (artifacts / "audio.m4a").exists()
    assert not (artifacts / "video.mp4").exists()
    assert set(p.name for p in artifacts.iterdir()) == {"info.json", "transcript.txt", "sheet.jpg", "read_response.jsonl"}
