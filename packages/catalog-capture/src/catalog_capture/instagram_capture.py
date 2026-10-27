"""Top-level Instagram reel capture (WK-0080 Instagram slice, OR-3): probe
caption -> audio -> transcribe -> video -> frames/contact sheet -> one OR-1
read. OR-3 (operator ruling, supersedes G1/G2/I1/I2/I9): the capture never
verifies a tool's URL or decides what the reel is "about" — it hands the
processing agent the caption, transcript, on-screen text, and whatever
tools/URLs the read spotted, labeled as unverified hints, and the agent
decides what goes into the catalog. Combines `instagram_probe` and
`instagram_read` into one call so the CLI/rewrite layer has a single
`capture_fn(url) -> InstagramCaptureResult` to inject (real in production,
fake in tests — same shape as `capture.py`'s `capture_page` for Reddit)."""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from . import instagram_probe as probe
from . import versions as ver
from .instagram_read import build_read_prompt, price_usage, run_claude_read


class InstagramCaptureError(RuntimeError):
    """Any stage of the Instagram pipeline failed. Carries the stage name and
    the original error text, so the inbox marker can say which stage broke."""

    def __init__(self, stage: str, original: BaseException | str):
        self.stage = stage
        self.original_text = str(original)
        super().__init__(f"{stage}: {self.original_text}")


@dataclass
class InstagramCaptureResult:
    reel_id: str
    reel_url: str
    info_json_text: str
    caption: str | None
    transcript_text: str
    sheet_path: Path
    on_screen_text: str
    key_claims: list[str] = field(default_factory=list)
    info_channel: str = ""
    # Raw `{"name": str, "url": str | None}` entries straight from the read
    # (OR-3: "Mentioned (unverified hints)" — never HTTP-checked or
    # GitHub-normalized at capture time; the processing agent decides what,
    # if anything, each one becomes).
    tools: list[dict] = field(default_factory=list)
    read_raw_stdout: str = ""
    read_usd: float | None = None
    read_usd_reason: str | None = None
    versions: dict[str, str] = field(default_factory=dict)
    # True when `sheet_path` is a loose OS tempfile this call created (the
    # `workdir=None` default) that nothing else owns — the caller must delete
    # it once done reading it (after copying it into the sources dir), even on
    # a failure path, or it leaks in /tmp forever. False when `sheet_path`
    # lives inside a caller-supplied `workdir`, whose lifecycle is the
    # caller's to manage.
    sheet_is_temp: bool = False


def _tool_versions() -> dict[str, str]:
    return {
        "yt-dlp": ver.yt_dlp_version(),
        "ffmpeg": ver.ffmpeg_version(),
        "faster-whisper": ver.faster_whisper_version(),
        "ctranslate2": ver.ctranslate2_version(),
        "claude": ver.claude_version(),
    }


def capture_instagram_reel(url: str, *, workdir: Path | None = None) -> InstagramCaptureResult:
    """Run the full pipeline against a live Instagram reel URL. Raises
    `InstagramCaptureError` naming the stage that failed — callers (the
    rewrite layer) turn that into `⚠ capture-failed <url> — <stage>: <error>`,
    never a silent drop."""
    reel_id = probe.reel_id_from_url(url)
    if reel_id is None:
        raise InstagramCaptureError("probe", f"could not parse a reel id from {url!r}")

    own_tmp = workdir is None
    tmp_ctx = tempfile.TemporaryDirectory() if own_tmp else None
    outdir = Path(tmp_ctx.name) if own_tmp else Path(workdir)
    outdir.mkdir(parents=True, exist_ok=True)

    try:
        try:
            probe_result = probe.probe_caption(url)
        except Exception as e:  # noqa: BLE001 - fail loud, name the stage
            raise InstagramCaptureError("probe", e) from e

        try:
            audio_path = probe.download_audio(url, outdir)
        except Exception as e:  # noqa: BLE001
            raise InstagramCaptureError("audio", e) from e

        try:
            pcm_path = probe.decode_to_pcm(audio_path, outdir)
            transcribed = probe.transcribe_small_cpu_int8(pcm_path)
        except Exception as e:  # noqa: BLE001
            raise InstagramCaptureError("transcribe", e) from e

        try:
            video_path = probe.download_video(url, outdir)
            sheet_path = probe.extract_contact_sheet(video_path, outdir)
        except Exception as e:  # noqa: BLE001
            raise InstagramCaptureError("frames", e) from e

        prompt = build_read_prompt(probe_result.caption, transcribed.text)
        try:
            read_result = run_claude_read(prompt, sheet_path)
        except Exception as e:  # noqa: BLE001
            raise InstagramCaptureError("read", e) from e

        usd, usd_reason = price_usage(read_result.usage)

        # The contact sheet file must outlive a self-owned tmpdir, since the
        # caller reads it after this function returns (to copy it into the
        # sources dir). Persist it under the caller-visible workdir path when
        # we created our own tempdir, by reading the bytes now.
        sheet_bytes = sheet_path.read_bytes()
        persisted_sheet = outdir / "sheet.jpg" if not own_tmp else None

        return InstagramCaptureResult(
            reel_id=reel_id,
            reel_url=url,
            info_json_text=probe_result.info_json_text,
            caption=probe_result.caption,
            transcript_text="\n".join(transcribed.transcript_lines),
            sheet_path=persisted_sheet or _write_temp_sheet(sheet_bytes),
            on_screen_text=read_result.on_screen_text,
            key_claims=read_result.key_claims,
            info_channel=read_result.info_channel,
            tools=read_result.tools,
            read_raw_stdout=read_result.raw_stdout,
            read_usd=usd,
            read_usd_reason=usd_reason,
            versions=_tool_versions(),
            sheet_is_temp=own_tmp,
        )
    finally:
        if tmp_ctx is not None:
            # Keep the tempdir alive only long enough to read the sheet bytes
            # above; _write_temp_sheet() has already persisted a copy.
            tmp_ctx.cleanup()


def cleanup_sheet(cap: InstagramCaptureResult) -> None:
    """Delete the loose OS tempfile `capture_instagram_reel` created for
    `cap.sheet_path` (`sheet_is_temp=True`), once the caller is done reading
    it (normally right after `write_instagram_source_files` copies it into
    the sources dir). Call this in a `finally`, so it runs even if the copy
    step raises — a no-op when the sheet lives in a caller-supplied
    `workdir` instead."""
    if cap.sheet_is_temp:
        Path(cap.sheet_path).unlink(missing_ok=True)


def _write_temp_sheet(data: bytes) -> Path:
    """The caller's own tempdir is about to be cleaned up (capture_instagram_reel
    did not receive a `workdir`) — persist the sheet bytes to a fresh tempfile
    that outlives this call, so the result's `sheet_path` stays valid."""
    fd, name = tempfile.mkstemp(suffix=".jpg", prefix="ig-sheet-")
    try:
        os.write(fd, data)
    finally:
        os.close(fd)
    return Path(name)
