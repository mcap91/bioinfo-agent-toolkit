"""Shared keyframes + contact-sheet stage (WK-0094 Phase B; formerly half of
`instagram_probe.py`): ffmpeg keyframe extraction (`select='eq(n\\,0)+gt(scene\\,0.3)'`,
S11's frame-0-always-included fix) + a PIL contact sheet (cols=6, JPEG q=90,
as `run_bench.py:599`)."""

from __future__ import annotations

import subprocess
from pathlib import Path

from .media import FFMPEG_EXE

# S11 (WK-0079 run 1 orchestrator ruling): frame 0 is always selected alongside
# scene changes, so a static-video reel still yields at least one frame.
FRAME_SELECT_FILTER = "select='eq(n\\,0)+gt(scene\\,0.3)',scale=270:-1"
CONTACT_SHEET_COLS = 6
CONTACT_SHEET_JPEG_QUALITY = 90


class FramesFailedError(RuntimeError):
    """ffmpeg keyframe extraction or contact-sheet assembly failed."""


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
