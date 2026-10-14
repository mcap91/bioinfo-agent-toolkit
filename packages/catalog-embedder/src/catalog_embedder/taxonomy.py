"""Canonical synonym groups (ported from taxonomy.ts)."""

from __future__ import annotations

import json
from pathlib import Path


class TaxonomyIndex:
    def __init__(self) -> None:
        self.groups: dict[str, set[str]] = {}
        self.canonical_of: dict[str, str] = {}
        self.known_terms: set[str] = set()


def load_taxonomy(dir: Path) -> dict[str, list[str]]:
    taxonomy_path = dir / "catalog" / "taxonomy.json"
    try:
        raw = taxonomy_path.read_text(encoding="utf-8")
        data = json.loads(raw)
        canonical = data.get("canonical", {})
        if not isinstance(canonical, dict):
            return {}
        return canonical
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def build_index(canonical: dict[str, list[str]]) -> TaxonomyIndex:
    index = TaxonomyIndex()
    for canonical_raw, aliases_raw in canonical.items():
        canon = canonical_raw.lower()
        members = {canon, *(a.lower() for a in aliases_raw)}
        for member in members:
            index.groups[member] = members
            index.canonical_of[member] = canon
            index.known_terms.add(member)
    return index
