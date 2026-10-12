"""Parse catalog entry markdown files (YAML frontmatter + body)."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

FRONTMATTER_RE = re.compile(r"^---\n([\s\S]*?)\n---\n([\s\S]*)$")


def parse_frontmatter(content: str) -> tuple[dict, str]:
    normalized = content.replace("\r\n", "\n")
    match = FRONTMATTER_RE.match(normalized)
    if not match:
        raise ValueError("No YAML frontmatter found")
    yaml_str, body = match.group(1), match.group(2)
    frontmatter = yaml.safe_load(yaml_str) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError("Frontmatter did not parse to a mapping")
    return frontmatter, body


def read_all_entries(entries_dir: Path) -> dict[str, tuple[dict, str]]:
    """Returns {entry_name: (frontmatter, body)}, skipping unparseable files."""
    entries: dict[str, tuple[dict, str]] = {}
    if not entries_dir.is_dir():
        return entries
    for file in sorted(entries_dir.iterdir(), key=lambda p: p.name):
        if file.suffix != ".md":
            continue
        content = file.read_text(encoding="utf-8")
        try:
            entries[file.stem] = parse_frontmatter(content)
        except ValueError:
            continue
    return entries
