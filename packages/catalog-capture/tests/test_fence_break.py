"""Fence-break edge case: a captured line that is exactly ``` would end the
inbox's ```text block early. The edge case fixture here is the real golden
fixture with one line mutated to a bare ``` — not hand-written prose."""

from pathlib import Path

from catalog_capture.adapters.reddit import RedditAdapter
from catalog_capture.canonical import canonical_url
from catalog_capture.fence import _ZWSP, defuse_fence_breaks
from catalog_capture.registry import process_needs_link
from catalog_capture.stages.browser import CaptureResult

from conftest import ts_parse_inbox

MARKER_BEFORE = "Google Open Sources Harness2 for Self Improving AI Agents"
MARKER_AFTER = "AFTER-THE-STRAY-FENCE-MARKER"


def test_defuse_neutralizes_a_bare_triple_backtick_line():
    mutated = "line one\n```\nline two"
    out = defuse_fence_breaks(mutated)
    assert "\n```\n" not in out
    assert "line one" in out and "line two" in out
    # Visually still three backticks once the ZWSP is stripped back out.
    assert out.replace(_ZWSP, "").count("```") == 1


def test_defuse_neutralizes_whitespace_padded_variants():
    for variant in ["```", "  ```", "```  ", "\t```\t"]:
        mutated = f"before\n{variant}\nafter"
        out = defuse_fence_breaks(mutated)
        assert "before" in out and "after" in out
        lines = out.split("\n")
        assert lines[1] != variant  # the stray-close line itself was changed


def test_mutated_golden_fixture_block_survives_the_real_ts_parser(golden_capture, tmp_path: Path):
    _, body_text = golden_capture
    # Mutate the real capture: inject a bare ``` line partway through, plus an
    # end-of-text marker after it, so truncation (vs. correct handling) is visible.
    lines = body_text.split("\n")
    mid = len(lines) // 2
    mutated_body = "\n".join(lines[:mid] + ["```"] + lines[mid:] + [MARKER_AFTER])
    assert MARKER_BEFORE in mutated_body

    final_url = (
        "https://www.reddit.com/r/LocalLLaMA/comments/1x9gfnb/"
        "google_open_sources_harness2_for_self_improving/?solution=x"
    )

    def fake_capture(url: str) -> CaptureResult:
        return CaptureResult(
            final_url=final_url,
            title="t",
            body_text=mutated_body,
            playwright_version="1.64.1",
            chromium_version="156.0.8078.4",
        )

    inbox = "⚠ needs-link https://www.reddit.com/r/LocalLLaMA/s/JNjEe87YeN\n"
    adapters = [RedditAdapter(capture_fn=fake_capture)]
    out_text, results = process_needs_link(inbox, sources_dir=tmp_path / "sources", adapters=adapters, delay_s=0)
    assert results[0].status == "ok"

    # R8: the sources file gets the verbatim capture (the bare ``` line intact);
    # only the inbox block gets the defused text.
    source_md = next((tmp_path / "sources" / "reddit").glob("*.md")).read_text(encoding="utf-8")
    assert "\n```\n" in source_md
    assert mutated_body.strip() in source_md

    # Only one real closing fence line should remain in the whole output.
    fence_close_lines = [ln for ln in out_text.split("\n") if ln.strip() == "```"]
    assert len(fence_close_lines) == 1

    inbox_path = tmp_path / "inbox.md"
    inbox_path.write_text(out_text, encoding="utf-8")
    items = ts_parse_inbox(inbox_path)
    assert len(items) == 1
    item = items[0]
    assert item["kind"] == "text"
    assert item["source"] == canonical_url(final_url)
    # Both sides of the stray fence line made it into the single parsed block.
    assert MARKER_BEFORE in item["content"]
    assert MARKER_AFTER in item["content"]


def test_bom_plus_backticks_survives_the_real_ts_parser(golden_capture, tmp_path: Path):
    """S5: a BOM (U+FEFF) passes JS `\\s` but not Python's — a line that is just
    a BOM followed by ``` would evade a naive Python-\\s-only check and still
    close the fence early under the real TS parser."""
    _, body_text = golden_capture
    bom = chr(0xFEFF)
    lines = body_text.split("\n")
    mid = len(lines) // 2
    mutated_body = "\n".join(lines[:mid] + [bom + "```"] + lines[mid:] + [MARKER_AFTER])
    assert MARKER_BEFORE in mutated_body

    final_url = (
        "https://www.reddit.com/r/LocalLLaMA/comments/1x9gfnb/"
        "google_open_sources_harness2_for_self_improving/?solution=x"
    )

    def fake_capture(url: str) -> CaptureResult:
        return CaptureResult(
            final_url=final_url,
            title="t",
            body_text=mutated_body,
            playwright_version="1.64.1",
            chromium_version="156.0.8078.4",
        )

    inbox = "⚠ needs-link https://www.reddit.com/r/LocalLLaMA/s/JNjEe87YeN\n"
    adapters = [RedditAdapter(capture_fn=fake_capture)]
    out_text, results = process_needs_link(inbox, sources_dir=tmp_path / "sources", adapters=adapters, delay_s=0)
    assert results[0].status == "ok"

    inbox_path = tmp_path / "inbox.md"
    inbox_path.write_text(out_text, encoding="utf-8")
    items = ts_parse_inbox(inbox_path)
    assert len(items) == 1  # the real inbox.ts FENCE_CLOSE regex did not fire on the BOM line
    item = items[0]
    assert item["kind"] == "text"
    assert MARKER_BEFORE in item["content"]
    assert MARKER_AFTER in item["content"]
