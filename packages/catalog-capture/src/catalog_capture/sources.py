"""Write catalog/sources/reddit/<post-id>.md (R8)."""

from __future__ import annotations

from pathlib import Path


def render_source_md(
    *, canonical: str, captured_at: str, playwright_version: str, chromium_version: str, text: str
) -> str:
    return (
        f"source: {canonical}\n"
        f"captured: {captured_at}\n"
        f"playwright: {playwright_version}\n"
        f"chromium: {chromium_version}\n"
        "\n"
        f"{text}\n"
    )


def write_source_file(sources_dir: Path, post_id: str, content: str) -> Path:
    out_dir = Path(sources_dir) / "reddit"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{post_id}.md"
    out_path.write_text(content, encoding="utf-8")
    return out_path
