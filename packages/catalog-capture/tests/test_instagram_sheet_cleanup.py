"""Temp-sheet leak fix: `capture_instagram_reel(workdir=None)` (the default)
persists its contact sheet to a loose OS tempfile because the rewrite/cli
layer reads it after the call returns (to copy it into the sources dir) —
nothing else owns that file, so it must be deleted once that copy is done,
even if the copy step itself raises. `cleanup_sheet()` is the single place
that happens; the registry's rewrite loop calls `adapter.cleanup()` (which
delegates to it) after every successful capture from this adapter."""

from __future__ import annotations

from pathlib import Path

from catalog_capture.adapters.instagram_reel import InstagramCaptureResult, InstagramReelAdapter, cleanup_sheet
from catalog_capture.registry import process_needs_link

REEL_URL = "https://www.instagram.com/reel/De5smNojeZm/"


def _fake_result_with_temp_sheet(tmp_path: Path) -> InstagramCaptureResult:
    sheet = tmp_path / "ig-sheet-fake.jpg"
    sheet.write_bytes(b"\xff\xd8\xff fake")
    return InstagramCaptureResult(
        reel_id="De5smNojeZm", reel_url=REEL_URL, info_json_text="{}", caption="c",
        transcript_text="t", sheet_path=sheet, on_screen_text="", tools=[],
        read_raw_stdout="{}", sheet_is_temp=True,  # mimics capture_instagram_reel(workdir=None)
    )


def test_cleanup_sheet_deletes_a_temp_sheet():
    # Why: the direct unit contract cleanup_sheet relies on.
    sheet_path = Path(__file__).parent / "_scratch_sheet_for_cleanup_test.jpg"
    sheet_path.write_bytes(b"x")
    cap = InstagramCaptureResult(
        reel_id="r", reel_url="u", info_json_text="{}", caption=None, transcript_text="",
        sheet_path=sheet_path, on_screen_text="", sheet_is_temp=True,
    )
    cleanup_sheet(cap)
    assert not sheet_path.exists()


def test_cleanup_sheet_is_a_noop_for_a_caller_managed_workdir_sheet(tmp_path: Path):
    # Why: when `workdir` was supplied, the sheet lives inside the caller's
    # own directory tree — cleanup_sheet must never delete something it
    # doesn't own.
    sheet_path = tmp_path / "sheet.jpg"
    sheet_path.write_bytes(b"x")
    cap = InstagramCaptureResult(
        reel_id="r", reel_url="u", info_json_text="{}", caption=None, transcript_text="",
        sheet_path=sheet_path, on_screen_text="", sheet_is_temp=False,
    )
    cleanup_sheet(cap)
    assert sheet_path.exists()


def test_needs_link_rewrite_deletes_the_temp_sheet_after_a_successful_capture(tmp_path: Path):
    sheet_holder: list[Path] = []

    def fake_capture(url: str) -> InstagramCaptureResult:
        cap = _fake_result_with_temp_sheet(tmp_path)
        sheet_holder.append(cap.sheet_path)
        return cap

    inbox = f"⚠ needs-link {REEL_URL}\n"
    adapters = [InstagramReelAdapter(capture_fn=fake_capture)]
    process_needs_link(inbox, sources_dir=tmp_path / "sources", adapters=adapters, delay_s=0)

    assert sheet_holder and not sheet_holder[0].exists()  # deleted once the sources write is done


def test_needs_link_rewrite_deletes_the_temp_sheet_even_if_the_source_write_raises(tmp_path, monkeypatch):
    # Why: a crash while writing one item's sources file must not leak that
    # item's loose tempfile, AND must not abort the rest of the batch — one
    # bad write must not cost the rest of the batch (re.sub would otherwise
    # propagate the exception and drop every other item's capture).
    import catalog_capture.registry as registry_mod

    sheet_holder: list[Path] = []

    def fake_capture(url: str) -> InstagramCaptureResult:
        cap = _fake_result_with_temp_sheet(tmp_path)
        sheet_holder.append(cap.sheet_path)
        return cap

    def raising_write(*args, **kwargs):
        raise OSError("disk full (simulated)")

    monkeypatch.setattr(registry_mod, "write_source_file", raising_write)

    inbox = f"⚠ needs-link {REEL_URL}\n"
    adapters = [InstagramReelAdapter(capture_fn=fake_capture)]
    out_text, results = process_needs_link(inbox, sources_dir=tmp_path / "sources", adapters=adapters, delay_s=0)

    assert results[0].status == "failed"
    assert out_text == f"⚠ capture-failed {REEL_URL} — write: disk full (simulated)\n"
    assert sheet_holder and not sheet_holder[0].exists()
