"""Failure markers (R8): a capture failure keeps the line blocked as
`⚠ capture-failed <url> — <error>`; a PDF download event becomes `⚠ pdf <url>`
(WK-0054 probe: `Page.goto: Download is starting`, own-pdf.log). Neither is
silently dropped, and both still match inbox.ts's ⚠-url pattern so a re-drain
keeps them blocked."""

from pathlib import Path

from catalog_capture.capture import CaptureFailedError, CaptureResult, PdfDownloadError
from catalog_capture.rewrite import process_needs_link

from conftest import ts_parse_inbox

URL = "https://www.reddit.com/r/LocalLLaMA/s/JNjEe87YeN"


def test_capture_failure_becomes_capture_failed_marker(tmp_path: Path):
    def failing_capture(url: str):
        raise CaptureFailedError("net::ERR_NAME_NOT_RESOLVED")

    inbox = f"⚠ needs-link {URL}\n"
    out_text, results = process_needs_link(
        inbox, sources_dir=tmp_path / "sources", capture_fn=failing_capture, delay_s=0
    )
    assert results[0].status == "failed"
    assert out_text == f"⚠ capture-failed {URL} — net::ERR_NAME_NOT_RESOLVED\n"

    items = ts_parse_inbox(_write(tmp_path, out_text))
    assert items[0] == {
        "kind": "url",
        "url": URL,
        "note": "net::ERR_NAME_NOT_RESOLVED",
        "blocked": True,
        "reason": "capture-failed",
        "raw": out_text.strip(),
        "startLine": 0,
        "endLine": 0,
    }


def test_pdf_download_event_becomes_pdf_marker(tmp_path: Path):
    def pdf_capture(url: str):
        raise PdfDownloadError(url)

    inbox = f"⚠ needs-link {URL}\n"
    out_text, results = process_needs_link(
        inbox, sources_dir=tmp_path / "sources", capture_fn=pdf_capture, delay_s=0
    )
    assert results[0].status == "pdf"
    assert out_text == f"⚠ pdf {URL}\n"

    items = ts_parse_inbox(_write(tmp_path, out_text))
    assert items[0]["kind"] == "url"
    assert items[0]["url"] == URL
    assert items[0]["blocked"] is True
    assert items[0]["reason"] == "pdf"


def test_no_source_file_written_on_failure_or_pdf(tmp_path: Path):
    sources_dir = tmp_path / "sources"

    def failing_capture(url: str):
        raise CaptureFailedError("boom")

    process_needs_link(f"⚠ needs-link {URL}\n", sources_dir=sources_dir, capture_fn=failing_capture, delay_s=0)
    assert not sources_dir.exists()


def _write(tmp_path: Path, text: str) -> Path:
    p = tmp_path / "inbox.md"
    p.write_text(text, encoding="utf-8")
    return p


# S3: a stalled JS challenge or block page must not be accepted as success. Each
# case below mutates the real golden fixture (final_url and/or body_text), per
# evidence discipline — not hand-invented capture shapes.


def test_stalled_wait_marks_capture_failed(golden_capture, tmp_path: Path):
    """wait_matched=False means the per-site wait-table selector (shreddit-post)
    never appeared on the page — the stalled-JS-challenge shape WK-0054's
    evidence log describes for probe.py's default-UA run (empty title,
    0 comments)."""
    final_url, body_text = golden_capture

    def stalled_capture(url: str) -> CaptureResult:
        return CaptureResult(
            final_url=final_url,
            title="",  # matches the WK-0054 evidence: empty title on a stall
            body_text=body_text,
            playwright_version="1.64.1",
            chromium_version="156.0.8078.4",
            wait_matched=False,
        )

    out_text, results = process_needs_link(
        f"⚠ needs-link {URL}\n", sources_dir=tmp_path / "sources", capture_fn=stalled_capture, delay_s=0
    )
    assert results[0].status == "failed"
    assert "stalled" in results[0].error
    assert out_text.startswith(f"⚠ capture-failed {URL} — ")
    assert not (tmp_path / "sources").exists()  # no source file for a failed capture


def test_blank_body_marks_capture_failed(golden_capture, tmp_path: Path):
    final_url, _ = golden_capture

    def blank_capture(url: str) -> CaptureResult:
        return CaptureResult(
            final_url=final_url,
            title="t",
            body_text="   \n   ",  # mutation: the real body, truncated to whitespace-only
            playwright_version="1.64.1",
            chromium_version="156.0.8078.4",
        )

    out_text, results = process_needs_link(
        f"⚠ needs-link {URL}\n", sources_dir=tmp_path / "sources", capture_fn=blank_capture, delay_s=0
    )
    assert results[0].status == "failed"
    assert "blank" in results[0].error
    assert out_text.startswith(f"⚠ capture-failed {URL} — ")


def test_source_write_failure_becomes_capture_failed_marker_and_batch_continues(
    golden_capture, tmp_path: Path, monkeypatch
):
    # Why: write_source_file does real file I/O (OSError is possible — disk
    # full, permissions) and used to run outside the capture try/except, so
    # one bad write propagated out of `repl()` through `re.sub` and aborted
    # the whole batch, silently dropping every other item in the same run.
    # One bad write must not cost the rest of the batch.
    import catalog_capture.rewrite as rewrite_mod

    _, body_text = golden_capture
    url_a = "https://www.reddit.com/r/LocalLLaMA/s/JNjEe87YeN"
    url_b = "https://www.reddit.com/r/LocalLLaMA/s/other00id"

    def fake_capture(url: str) -> CaptureResult:
        share_id = url.rsplit("/", 1)[-1]
        return CaptureResult(
            final_url=f"https://www.reddit.com/r/LocalLLaMA/comments/post{share_id}/t/",
            title="t",
            body_text=body_text,
            playwright_version="1.64.1",
            chromium_version="156.0.8078.4",
        )

    real_write = rewrite_mod.write_source_file
    calls = {"n": 0}

    def flaky_write(sources_dir, post_id, content):
        calls["n"] += 1
        if calls["n"] == 1:
            raise OSError("disk full (simulated)")
        return real_write(sources_dir, post_id, content)

    monkeypatch.setattr(rewrite_mod, "write_source_file", flaky_write)

    inbox = f"⚠ needs-link {url_a}\n⚠ needs-link {url_b}\n"
    out_text, results = process_needs_link(
        inbox, sources_dir=tmp_path / "sources", capture_fn=fake_capture, delay_s=0
    )

    assert [r.status for r in results] == ["failed", "ok"]
    out_lines = out_text.splitlines()
    assert out_lines[0] == f"⚠ capture-failed {url_a} — write: disk full (simulated)"
    assert out_lines[1] == "```text"  # the second item still becomes a fenced block
    written = sorted(p.name for p in (tmp_path / "sources" / "reddit").glob("*.md"))
    assert len(written) == 1  # only the second item's source file survives


def test_missing_post_id_marks_capture_failed(golden_capture, tmp_path: Path):
    _, body_text = golden_capture

    def blocked_page_capture(url: str) -> CaptureResult:
        # Mutation: real body text, but the final url is a block/login redirect
        # with no /comments/<id>/ segment — canonical_url -> post_id is None.
        return CaptureResult(
            final_url="https://www.reddit.com/login",
            title="Reddit - Log In",
            body_text=body_text,
            playwright_version="1.64.1",
            chromium_version="156.0.8078.4",
        )

    out_text, results = process_needs_link(
        f"⚠ needs-link {URL}\n", sources_dir=tmp_path / "sources", capture_fn=blocked_page_capture, delay_s=0
    )
    assert results[0].status == "failed"
    assert "post id" in results[0].error
    assert out_text.startswith(f"⚠ capture-failed {URL} — ")
