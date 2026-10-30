"""Golden fixture (R9): the real WK-0054 own-engine capture of the r/LocalLLaMA
Harness2 post, fed through our code with assertions on the extracted facts."""

from pathlib import Path

from catalog_capture.canonical import canonical_url, post_id
from catalog_capture.fence import defuse_fence_breaks
from catalog_capture.sources_writer import render_source_md, write_source_file


def test_fixture_shape_matches_the_real_capture(golden_capture):
    final_url, body_text = golden_capture
    assert final_url.startswith("https://www.reddit.com/r/LocalLLaMA/comments/1x9gfnb/")
    assert "Google Open Sources Harness2 for Self Improving AI Agents" in body_text


def test_canonical_url_and_post_id_from_the_real_capture(golden_capture):
    final_url, _ = golden_capture
    canonical = canonical_url(final_url)
    assert canonical == (
        "https://www.reddit.com/r/LocalLLaMA/comments/1x9gfnb/"
        "google_open_sources_harness2_for_self_improving/"
    )
    assert post_id(canonical) == "1x9gfnb"


def test_source_md_carries_full_text_and_tool_versions(golden_capture, tmp_path: Path):
    final_url, body_text = golden_capture
    canonical = canonical_url(final_url)
    safe_text = defuse_fence_breaks(body_text)
    md = render_source_md(
        header_lines=[
            f"source: {canonical}",
            "captured: 2026-10-26",
            "playwright: 1.64.1",
            "chromium: 156.0.8078.4",
        ],
        body=f"{safe_text}\n",
    )
    out = write_source_file(tmp_path, "reddit", "1x9gfnb", md)
    written = out.read_text(encoding="utf-8")

    assert written.startswith(f"source: {canonical}\n")
    assert "captured: 2026-10-26" in written
    assert "playwright: 1.64.1" in written
    assert "chromium: 156.0.8078.4" in written
    # Full page text preserved (comments included, per WK-0054 Results).
    assert "Google Open Sources Harness2 for Self Improving AI Agents" in written
    assert body_text.strip() in written or safe_text.strip() in written
