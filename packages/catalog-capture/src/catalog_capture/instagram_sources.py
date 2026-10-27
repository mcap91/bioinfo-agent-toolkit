"""Write `catalog/sources/instagram/<reel-id>.md` + raw artifacts beside it
(info JSON, transcript, contact sheet, read response — no audio/video, to
keep the sources dir small), mirroring `sources.py`'s role for Reddit (R8).

OR-3 (operator ruling): the capture never verifies a tool's URL or decides
what the reel is "about" — the mentioned tools/URLs are listed as unverified
hints, same wording as the inbox block, and the processing agent decides
what (if anything) each one becomes."""

from __future__ import annotations

import shutil
from pathlib import Path


def _hint_line(tool: dict) -> str:
    url = tool.get("url")
    return f"- {tool.get('name')}: {url if url else '(no url)'}"


def render_instagram_source_md(
    *,
    reel_url: str,
    captured_at: str,
    versions: dict[str, str],
    caption: str | None,
    transcript_text: str,
    on_screen_text: str,
    key_claims: list[str],
    info_channel: str,
    tools: list[dict],
) -> str:
    version_lines = "\n".join(f"{name}: {v}" for name, v in versions.items())
    hints_block = "\n".join(_hint_line(t) for t in tools) if tools else "(none mentioned)"
    claims_block = "\n".join(f"- {c}" for c in key_claims) if key_claims else "(none)"
    return (
        f"reel: {reel_url}\n"
        f"captured: {captured_at}\n"
        f"{version_lines}\n"
        "\n"
        "## Caption\n\n"
        f"{caption or '(no caption captured)'}\n"
        "\n"
        "## Transcript\n\n"
        f"{transcript_text}\n"
        "\n"
        "## On-screen text\n\n"
        f"{on_screen_text or '(none)'}\n"
        "\n"
        "## Key claims\n\n"
        f"{claims_block}\n"
        "\n"
        f"## Info channel\n\n{info_channel or '(unknown)'}\n"
        "\n"
        "## Mentioned (unverified hints)\n\n"
        f"{hints_block}\n"
    )


def write_instagram_source_files(
    sources_dir: Path,
    reel_id: str,
    md_content: str,
    *,
    info_json_text: str | None = None,
    transcript_text: str | None = None,
    sheet_path: Path | None = None,
    read_response_text: str | None = None,
) -> Path:
    """Writes `<sources_dir>/instagram/<reel_id>.md` plus raw artifacts in a
    sibling `<sources_dir>/instagram/<reel_id>/` directory: `info.json`,
    `transcript.txt`, `sheet.jpg`, `read_response.jsonl`. No audio/video
    (build step 2: raw artifacts beside it, "no audio/video")."""
    out_dir = Path(sources_dir) / "instagram"
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"{reel_id}.md"
    md_path.write_text(md_content, encoding="utf-8")

    artifacts_dir = out_dir / reel_id
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    if info_json_text is not None:
        (artifacts_dir / "info.json").write_text(info_json_text, encoding="utf-8")
    if transcript_text is not None:
        (artifacts_dir / "transcript.txt").write_text(transcript_text, encoding="utf-8")
    if sheet_path is not None and Path(sheet_path).exists():
        shutil.copyfile(sheet_path, artifacts_dir / "sheet.jpg")
    if read_response_text is not None:
        (artifacts_dir / "read_response.jsonl").write_text(read_response_text, encoding="utf-8")

    return md_path
