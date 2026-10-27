"""Instagram reel capture: caption, audio/transcript, keyframe contact sheet.

Logic ported from `toolkit-workbench/reel/scripts/run_bench.py` stage1 (probe),
stage2 (audio), stage3 (transcribe), stage4 (frames) — reduced from the bench's
multi-contender comparison down to the single WK-0079 "Results — run 2"
recommended default stack (I4): yt-dlp `-j` anonymous probe, yt-dlp bestaudio
download, ffmpeg (imageio-ffmpeg) decode to 16 kHz mono PCM, faster-whisper
`small` CPU int8 with VAD off, yt-dlp bestvideo download, ffmpeg keyframes
(`select='eq(n\\,0)+gt(scene\\,0.3)'`, S11's frame-0-always-included fix) +
PIL contact sheet (cols=6, JPEG q=90). Not imported from the workbench (it is
gitignored and not a dependency of this package, R9/I8) — the logic is
re-implemented here against this package's own yt-dlp/ffmpeg/faster-whisper.
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import imageio_ffmpeg

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

# S11 (WK-0079 run 1 orchestrator ruling): frame 0 is always selected alongside
# scene changes, so a static-video reel still yields at least one frame.
FRAME_SELECT_FILTER = "select='eq(n\\,0)+gt(scene\\,0.3)',scale=270:-1"
CONTACT_SHEET_COLS = 6
CONTACT_SHEET_JPEG_QUALITY = 90

REEL_ID_RE = re.compile(r"/reel/([A-Za-z0-9_-]+)/?")


class ProbeFailedError(RuntimeError):
    """yt-dlp -j produced no usable info JSON."""


class AudioDownloadFailedError(RuntimeError):
    """yt-dlp bestaudio download failed."""


class TranscribeFailedError(RuntimeError):
    """ffmpeg decode or faster-whisper transcription failed."""


class VideoDownloadFailedError(RuntimeError):
    """yt-dlp bestvideo download failed."""


class FramesFailedError(RuntimeError):
    """ffmpeg keyframe extraction or contact-sheet assembly failed."""


def reel_id_from_url(url: str) -> str | None:
    m = REEL_ID_RE.search(url)
    return m.group(1) if m else None


@dataclass
class ProbeResult:
    info_json_text: str  # raw yt-dlp -j stdout (one JSON object), verbatim
    caption: str | None


def probe_caption(url: str, *, timeout: int = 120) -> ProbeResult:
    """yt-dlp `-j` anonymous (I4/WK-0079 S6: `--sleep-requests 2`, curl-cffi
    impersonation via the `yt-dlp[curl-cffi]` extra already installed)."""
    proc = subprocess.run(
        ["yt-dlp", "-j", "--no-warnings", "--sleep-requests", "2", url],
        capture_output=True, text=True, timeout=timeout,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        raise ProbeFailedError(proc.stderr.strip()[-800:] or f"yt-dlp -j exit {proc.returncode}, no output")
    info_line = proc.stdout.splitlines()[0]
    data = json.loads(info_line)
    return ProbeResult(info_json_text=info_line, caption=data.get("description"))


def download_audio(url: str, outdir: Path, *, timeout: int = 180) -> Path:
    """yt-dlp bestaudio DASH download (I4: "video-only DASH: audio comes from
    the separate bestaudio download"). `--ffmpeg-location` pins this package's
    own imageio-ffmpeg binary, never a system ffmpeg."""
    proc = subprocess.run(
        ["yt-dlp", "-f", "bestaudio", "--sleep-requests", "2", "--no-warnings",
         "--ffmpeg-location", FFMPEG_EXE, "-o", str(outdir / "audio.%(ext)s"), url],
        capture_output=True, text=True, timeout=timeout,
    )
    found = [p for p in outdir.glob("audio.*") if p.suffix != ".log"]
    if proc.returncode != 0 or not found:
        raise AudioDownloadFailedError(proc.stderr.strip()[-800:] or f"yt-dlp bestaudio exit {proc.returncode}")
    return found[0]


def download_video(url: str, outdir: Path, *, timeout: int = 180) -> Path:
    proc = subprocess.run(
        ["yt-dlp", "-f", "bestvideo", "--sleep-requests", "2", "--no-warnings",
         "--ffmpeg-location", FFMPEG_EXE, "-o", str(outdir / "video.%(ext)s"), url],
        capture_output=True, text=True, timeout=timeout,
    )
    found = [p for p in outdir.glob("video.*") if p.suffix != ".log"]
    if proc.returncode != 0 or not found:
        raise VideoDownloadFailedError(proc.stderr.strip()[-800:] or f"yt-dlp bestvideo exit {proc.returncode}")
    return found[0]


def decode_to_pcm(audio_path: Path, outdir: Path, *, timeout: int = 120) -> Path:
    """ffmpeg -> 16 kHz mono PCM wav. Decoding via ffmpeg first (never PyAV,
    I4: faster-whisper #1589, `av>=19` breaks `metadata_errors`) before handing
    the samples to faster-whisper as an in-memory array via soundfile."""
    pcm_path = outdir / "audio16k.wav"
    proc = subprocess.run(
        [FFMPEG_EXE, "-y", "-i", str(audio_path), "-ar", "16000", "-ac", "1", "-f", "wav", str(pcm_path)],
        capture_output=True, text=True, timeout=timeout,
    )
    if proc.returncode != 0 or not pcm_path.exists():
        raise TranscribeFailedError(f"ffmpeg decode to 16kHz PCM failed: {proc.stderr.strip()[-800:]}")
    return pcm_path


@dataclass
class TranscribeResult:
    text: str  # bracket-free, joined segment text
    transcript_lines: list[str]  # "[  12.3] segment text" lines, for the sources file
    language: str
    words: int


def transcribe_small_cpu_int8(pcm_path: Path) -> TranscribeResult:
    """faster-whisper `small` CPU int8, VAD off (I4: "CPU instead of GPU: same
    words, ~7s vs ~3s per reel, and no CUDA libraries" — this package never
    installs CUDA deps, so CPU int8 is not a fallback here, it is the only
    path)."""
    try:
        import soundfile as sf
        from faster_whisper import WhisperModel
    except ImportError as e:
        raise TranscribeFailedError(f"missing dependency: {e}") from e

    try:
        audio, _sr = sf.read(str(pcm_path), dtype="float32")
    except Exception as e:  # noqa: BLE001 - fail loud with context
        raise TranscribeFailedError(f"soundfile read of 16kHz PCM failed: {type(e).__name__}: {e}") from e

    try:
        model = WhisperModel("small", device="cpu", compute_type="int8")
        segments, info = model.transcribe(audio, vad_filter=False)
        segs = list(segments)
    except Exception as e:  # noqa: BLE001
        raise TranscribeFailedError(f"faster-whisper transcription failed: {type(e).__name__}: {e}") from e

    text = " ".join(s.text.strip() for s in segs)
    lines = [f"[{s.start:6.1f}] {s.text.strip()}" for s in segs]
    return TranscribeResult(text=text, transcript_lines=lines, language=info.language, words=len(text.split()))


def build_contact_sheet(frame_paths: list[Path], sheet_path: Path, cols: int = CONTACT_SHEET_COLS) -> None:
    """Tiled contact sheet, as `run_bench.py:599` (same cols, same JPEG q=90)."""
    from PIL import Image

    imgs = [Image.open(p) for p in frame_paths]
    w, h = imgs[0].size
    rows = -(-len(imgs) // cols)  # ceil
    sheet = Image.new("RGB", (w * cols, h * rows), "black")
    for i, im in enumerate(imgs):
        x = (i % cols) * w
        y = (i // cols) * h
        sheet.paste(im, (x, y))
    sheet.save(sheet_path, quality=CONTACT_SHEET_JPEG_QUALITY)


def extract_contact_sheet(video_path: Path, outdir: Path, *, timeout: int = 120) -> Path:
    frame_dir = outdir / "frames"
    frame_dir.mkdir(exist_ok=True)
    proc = subprocess.run(
        [FFMPEG_EXE, "-y", "-i", str(video_path),
         "-vf", FRAME_SELECT_FILTER, "-fps_mode", "vfr", str(frame_dir / "frame_%03d.jpg")],
        capture_output=True, text=True, timeout=timeout,
    )
    frames = sorted(frame_dir.glob("frame_*.jpg"))
    if proc.returncode != 0 or not frames:
        raise FramesFailedError(f"ffmpeg keyframe extraction failed: {proc.stderr.strip()[-800:]}")
    sheet_path = outdir / "sheet.jpg"
    build_contact_sheet(frames, sheet_path)
    return sheet_path
