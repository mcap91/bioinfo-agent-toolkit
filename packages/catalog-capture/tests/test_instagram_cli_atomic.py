"""Instagram counterpart of test_cli_atomic.py (S2): the shared `run_needs_link`
reads the inbox once and writes it once, atomically, and aborts without
writing if the file changed on disk mid-run — same contract as the Reddit
path, exercised here through the Instagram reel adapter's own (injected)
capture function."""

from __future__ import annotations

import time
from pathlib import Path

from catalog_capture.adapters.instagram_reel import InstagramCaptureResult, InstagramReelAdapter
from catalog_capture.cli import run_needs_link

URL_A = "https://www.instagram.com/reel/De5smNojeZm/"


def _fake_capture(url: str) -> InstagramCaptureResult:
    return InstagramCaptureResult(
        reel_id="De5smNojeZm",
        reel_url=url,
        info_json_text='{"description": "cap"}',
        caption="cap",
        transcript_text="[   0.0] hi",
        sheet_path=Path("/dev/null"),
        on_screen_text="",
        tools=[],
        read_raw_stdout="{}",
    )


def test_successful_run_writes_atomically_via_tmp_file_and_replace(tmp_path: Path):
    inbox_path = tmp_path / "inbox.md"
    inbox_path.write_text(f"⚠ needs-link {URL_A}\n", encoding="utf-8")
    sources_dir = tmp_path / "sources"

    adapters = [InstagramReelAdapter(capture_fn=_fake_capture)]
    code = run_needs_link(inbox_path, sources_dir, adapters=adapters, delay_s=0)

    assert code == 0
    assert f"source: {URL_A}" in inbox_path.read_text(encoding="utf-8")  # OR-3: source is always the reel URL
    assert not (tmp_path / "inbox.md.tmp").exists()
    assert (sources_dir / "instagram" / "De5smNojeZm.md").exists()


def test_aborts_without_writing_when_inbox_changed_during_the_run(tmp_path: Path, capsys):
    inbox_path = tmp_path / "inbox.md"
    original = f"⚠ needs-link {URL_A}\n"
    inbox_path.write_text(original, encoding="utf-8")
    sources_dir = tmp_path / "sources"
    concurrent_edit = original + "\nsomeone appended a line mid-run\n"

    def capture_that_races(url: str) -> InstagramCaptureResult:
        time.sleep(0.01)
        inbox_path.write_text(concurrent_edit, encoding="utf-8")
        return _fake_capture(url)

    adapters = [InstagramReelAdapter(capture_fn=capture_that_races)]
    code = run_needs_link(inbox_path, sources_dir, adapters=adapters, delay_s=0)

    assert code == 1
    assert inbox_path.read_text(encoding="utf-8") == concurrent_edit  # not overwritten
    assert (sources_dir / "instagram" / "De5smNojeZm.md").exists()  # already-captured source kept

    captured = capsys.readouterr()
    assert "ABORTED" in captured.err
    assert URL_A in captured.err
