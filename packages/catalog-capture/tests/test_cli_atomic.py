"""S2: a 5-8 minute needs-link run reads the inbox once and writes it once.
Write via tmp-file + os.replace (atomic on POSIX), and abort without writing if
the file changed on disk during the run (mtime/size mismatch at read vs. just
before write) — print which items were captured, exit non-zero."""

import time
from pathlib import Path

from catalog_capture.capture import CaptureResult
from catalog_capture.cli import run_needs_link

URL_A = "https://www.reddit.com/r/LocalLLaMA/s/JNjEe87YeN"


def _fake_capture(url: str) -> CaptureResult:
    share_id = url.rsplit("/", 1)[-1]
    return CaptureResult(
        final_url=f"https://www.reddit.com/r/LocalLLaMA/comments/post{share_id}/t/",
        title="t",
        body_text=f"captured text for {share_id}",
        playwright_version="1.64.1",
        chromium_version="156.0.8078.4",
    )


def test_successful_run_writes_atomically_via_tmp_file_and_replace(tmp_path: Path):
    inbox_path = tmp_path / "inbox.md"
    inbox_path.write_text(f"⚠ needs-link {URL_A}\n", encoding="utf-8")
    sources_dir = tmp_path / "sources"

    code = run_needs_link(inbox_path, sources_dir, capture_fn=_fake_capture, delay_s=0)

    assert code == 0
    assert "source: https://www.reddit.com/r/LocalLLaMA/comments/" in inbox_path.read_text(encoding="utf-8")
    # No leftover tmp file.
    assert not (tmp_path / "inbox.md.tmp").exists()


def test_aborts_without_writing_when_inbox_changed_during_the_run(tmp_path: Path, capsys):
    inbox_path = tmp_path / "inbox.md"
    original = f"⚠ needs-link {URL_A}\n"
    inbox_path.write_text(original, encoding="utf-8")
    sources_dir = tmp_path / "sources"

    concurrent_edit = original + "\nsomeone appended a line mid-run\n"

    def capture_that_races(url: str) -> CaptureResult:
        # Simulate an operator editing the inbox while this multi-minute run is
        # still in flight — mtime+size will differ from what we read at start.
        time.sleep(0.01)
        inbox_path.write_text(concurrent_edit, encoding="utf-8")
        return _fake_capture(url)

    code = run_needs_link(inbox_path, sources_dir, capture_fn=capture_that_races, delay_s=0)

    assert code == 1
    # The inbox was NOT overwritten — the concurrent edit is what's on disk.
    assert inbox_path.read_text(encoding="utf-8") == concurrent_edit
    # The source file for the item captured before the abort still exists.
    written = list((sources_dir / "reddit").glob("*.md"))
    assert len(written) == 1

    captured = capsys.readouterr()
    assert "ABORTED" in captured.err
    assert URL_A in captured.err  # names which item was captured
