"""Query-term expansion via synonym groups (ported from taxonomy.ts)."""

from __future__ import annotations

import json
import re
from pathlib import Path

TOKEN_RE = re.compile(r"[^a-z0-9]+")


def tokenize(s: str) -> list[str]:
    return [t for t in TOKEN_RE.split(s.lower()) if t]


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


def expand_term(term: str, index: TaxonomyIndex) -> list[str]:
    t = term.lower()
    group = index.groups.get(t)
    return list(group) if group else [t]


def canonical_for_tag(tag: str, index: TaxonomyIndex) -> str | None:
    return index.canonical_of.get(tag.lower())


def unclassified_tags(tags: list[str], index: TaxonomyIndex) -> list[str]:
    return [t for t in tags if t.lower() not in index.known_terms]
