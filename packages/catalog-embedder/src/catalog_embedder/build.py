"""`build` command: embed all catalog entries and write the vector file."""

from __future__ import annotations

import sys
from pathlib import Path

from . import embeddings
from .frontmatter import read_all_entries
from .vectors import write_vectors


def build_embedding_text(name: str, frontmatter: dict, body: str) -> str:
    title = frontmatter.get("title") or ""
    summary = frontmatter.get("summary") or ""
    tags = frontmatter.get("tags") or []
    tags_str = " ".join(str(t) for t in tags)
    return f"{title} {name} {summary} {tags_str} {body}"


def run_build(dir: Path) -> None:
    entries_dir = dir / "catalog" / "entries"
    entries = read_all_entries(entries_dir)
    print(f"catalog-embedder: found {len(entries)} entries in {entries_dir}", file=sys.stderr)

    if not entries:
        write_vectors(dir, {})
        print("catalog-embedder: no entries found, wrote empty vector file", file=sys.stderr)
        return

    names = list(entries.keys())
    texts = [build_embedding_text(name, fm, body) for name, (fm, body) in entries.items()]

    print(f"catalog-embedder: embedding {len(texts)} entries with fastembed...", file=sys.stderr)
    vectors = embeddings.embed_texts(texts)

    entries_out = dict(zip(names, vectors))
    write_vectors(dir, entries_out)
    print(f"catalog-embedder: wrote vectors for {len(entries_out)} entries", file=sys.stderr)
