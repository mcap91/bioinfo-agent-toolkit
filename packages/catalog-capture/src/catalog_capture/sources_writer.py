"""Shared sources-file writer (WK-0094 Phase B; formerly `sources.py` +
`instagram_sources.py`, unified). Writes `catalog/sources/<platform>/<id>.md`
(frontmatter-free: adapter-supplied header lines, a blank line, then the
adapter-supplied body) plus an optional sibling artifact directory. Adapters
supply sections and artifacts; this module owns the one format and the one
write path."""

from __future__ import annotations

import shutil
from pathlib import Path


def render_source_md(*, header_lines: list[str], body: str) -> str:
    """`header_lines` joined one per line, a blank line, then `body` —
    byte-identical composition to the pre-refactor Reddit and Instagram
    renderers (verified against their snapshots)."""
    return "\n".join(header_lines) + "\n\n" + body


def write_source_file(
    sources_dir: Path,
    platform: str,
    item_id: str,
    md_content: str,
    *,
    artifacts: dict[str, str | bytes | Path | None] | None = None,
) -> Path:
    """Writes `<sources_dir>/<platform>/<item_id>.md`. When `artifacts` is
    not None (even if empty), also creates a sibling `<item_id>/` directory
    and writes one file per non-None entry: a `str` value is written as
    text, `bytes` as binary, and a `Path` is copied from (skipped if it
    doesn't exist — mirrors the old sheet_path-optional-existence check)."""
    out_dir = Path(sources_dir) / platform
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{item_id}.md"
    out_path.write_text(md_content, encoding="utf-8")

    if artifacts is not None:
        artifacts_dir = out_dir / item_id
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        for name, value in artifacts.items():
            if value is None:
                continue
            dest = artifacts_dir / name
            if isinstance(value, Path):
                if value.exists():
                    shutil.copyfile(value, dest)
            elif isinstance(value, bytes):
                dest.write_bytes(value)
            else:
                dest.write_text(str(value), encoding="utf-8")

    return out_path
