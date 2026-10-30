"""Shared audio-decode + transcribe stage (WK-0094 Phase B; formerly half of
`instagram_probe.py`): ffmpeg (imageio-ffmpeg) decode to 16 kHz mono PCM, then
faster-whisper `small` CPU int8 with VAD off (I4 default stack).

Decode with ffmpeg -> soundfile, never PyAV (faster-whisper #1589). CPU
instead of GPU: same words, ~7s vs ~3s per reel, and no CUDA libraries — this
package never installs CUDA deps, so CPU int8 is not a fallback here, it is
the only path.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from .media import FFMPEG_EXE


class TranscribeFailedError(RuntimeError):
    """ffmpeg decode or faster-whisper transcription failed."""


def decode_to_pcm(audio_path: Path, outdir: Path, *, timeout: int = 120) -> Path:
    """ffmpeg -> 16 kHz mono PCM wav."""
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
    words, ~7s vs ~3s per reel, and no CUDA libraries")."""
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
