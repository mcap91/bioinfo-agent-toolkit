"""Golden fixture (I8): the real golden-reel (De5smNojeZm) artifacts fed
through this package's own code, plus this slice's own real OR-1 read
response (I3) fed through the real stream-json parser. Nothing here is
hand-written — every assertion is against a byte-for-byte copy of a real
capture (AGENTS 22-24)."""

from __future__ import annotations

import json
import re

from catalog_capture.stages.read import parse_claude_stream_result


def test_probe_json_has_the_real_caption_and_github_urls(golden_instagram_artifacts):
    # Why: the probe stage reads `description` straight out of yt-dlp's -j
    # output — this proves that field is where the two repo URLs actually
    # live in a real capture, not an assumed shape.
    data = json.loads(golden_instagram_artifacts["info_json_text"])
    caption = data["description"]
    assert "github.com/Gathin23/cleanyourtv" in caption
    assert "github.com/humblemuzzu/dumbtv" in caption


def test_transcript_fixture_is_the_real_small_cpu_int8_shape(golden_instagram_artifacts):
    # Why: I4 pins faster-whisper `small` CPU int8 as the only transcribe path
    # this package runs (no CUDA deps) — this is the real output of that
    # exact contender on the golden reel, not a bench GPU run.
    text = golden_instagram_artifacts["transcript_text"]
    assert text.startswith("[   0.0]")
    assert "restore script" in text  # spoken mention (on-screen text is the sheet, not this file)
    words = len(re.sub(r"^\[.*?\]", "", text, flags=re.MULTILINE).split())
    assert words >= 438  # WK-0079 AC-1: >= 95% of the proof's 461 content words


def test_sheet_fixture_is_a_real_jpeg(golden_instagram_artifacts):
    # Why: confirms the copied fixture is the actual binary contact sheet
    # (JPEG magic bytes), not a placeholder or a text file with the wrong
    # extension.
    data = golden_instagram_artifacts["sheet_path"].read_bytes()
    assert data[:3] == b"\xff\xd8\xff"  # JPEG SOI marker


def test_real_read_response_parses_and_has_the_i3_fields(golden_instagram_artifacts):
    # Why: I3's `tools`/`on_screen_text` shape is new this slice — this is the
    # actual captured response (not invented), proving the shape this
    # package's parser depends on is real.
    parsed = parse_claude_stream_result(golden_instagram_artifacts["read_response_text"])
    assert parsed is not None
    assert parsed["model"] == "claude-sonnet-5"
    assert all(parsed[k] is not None for k in ("input_tokens", "output_tokens", "cache_read_tokens", "cache_creation_tokens"))

    m = re.search(r"\{.*\}", parsed["result_text"], re.DOTALL)
    assert m is not None
    obj = json.loads(m.group(0))
    assert isinstance(obj["tools"], list) and len(obj["tools"]) >= 1
    assert isinstance(obj["on_screen_text"], str)
    assert isinstance(obj["key_claims"], list)
    assert obj["info_channel"] in ("spoken", "on-screen", "caption")


def test_golden_read_names_restore_sh(golden_instagram_artifacts):
    # Why: the WK-0080 acceptance criterion — "the golden reel's capture md
    # contains ... the on-screen restore.sh step" — checked against the real
    # captured response, not assumed.
    parsed = parse_claude_stream_result(golden_instagram_artifacts["read_response_text"])
    m = re.search(r"\{.*\}", parsed["result_text"], re.DOTALL)
    obj = json.loads(m.group(0))
    named_in_on_screen_text = "restore.sh" in obj["on_screen_text"]
    named_in_claims = any("restore.sh" in c or "restore script" in c for c in obj["key_claims"])
    assert named_in_on_screen_text or named_in_claims


def test_real_read_tools_include_the_caption_named_repos(golden_instagram_artifacts):
    # Why: route 1 (I1) — the reel names two repos in its caption; the read
    # must surface at least one of them so GitHub-URL normalization +
    # verification have something real to act on.
    parsed = parse_claude_stream_result(golden_instagram_artifacts["read_response_text"])
    m = re.search(r"\{.*\}", parsed["result_text"], re.DOTALL)
    obj = json.loads(m.group(0))
    tool_urls = " ".join(str(t.get("url") or "") for t in obj["tools"])
    assert "cleanyourtv" in tool_urls or "dumbtv" in tool_urls
