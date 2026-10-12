"""`search` command: hybrid lexical + semantic scoring over catalog entries."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from . import embeddings
from .build import run_build
from .frontmatter import read_all_entries
from .lexical import score_entry
from .taxonomy import build_index, load_taxonomy
from .vectors import cosine_similarity, is_valid, read_vectors

DEFAULT_LIMIT = 200
DEFAULT_ALPHA = 0.5


def run_search(
    dir: Path,
    query: str,
    limit: int = DEFAULT_LIMIT,
    alpha: float = DEFAULT_ALPHA,
    decision_status: str | None = None,
    category: str | None = None,
) -> dict[str, Any]:
    vector_data = read_vectors(dir)
    if not is_valid(vector_data):
        print(
            "catalog-embedder: vector file missing or model mismatch — running build",
            file=sys.stderr,
        )
        run_build(dir)
        vector_data = read_vectors(dir)
    entry_vectors: dict[str, list[float]] = (vector_data or {}).get("entries", {})

    raw = read_all_entries(dir / "catalog" / "entries")
    tax_index = build_index(load_taxonomy(dir))

    query_terms = [t for t in query.lower().split() if t]

    query_vector: list[float] | None = None
    if query.strip():
        [query_vector] = embeddings.embed_texts([query])

    candidates: list[dict[str, Any]] = []
    for name, (frontmatter, body) in raw.items():
        status = frontmatter.get("decision_status") or "open"
        if decision_status and status != decision_status:
            continue
        if category and frontmatter.get("category") != category:
            continue

        lexical = 0
        if query_terms:
            lexical = score_entry(frontmatter, body, query_terms, tax_index)
            if lexical == 0:
                continue

        cosine = 0.0
        if query_vector is not None and name in entry_vectors:
            cosine = max(0.0, min(1.0, cosine_similarity(query_vector, entry_vectors[name])))

        candidates.append(
            {
                "name": name,
                "frontmatter": frontmatter,
                "status": status,
                "lexical": lexical,
                "cosine": cosine,
            }
        )

    max_lexical = max((c["lexical"] for c in candidates), default=0)

    results: list[dict[str, Any]] = []
    for c in candidates:
        if max_lexical > 0:
            score = (1 - alpha) * (c["lexical"] / max_lexical) + alpha * c["cosine"]
        else:
            score = c["cosine"]

        fm = c["frontmatter"]
        result: dict[str, Any] = {
            "name": c["name"],
            "title": fm.get("title"),
        }
        if fm.get("url"):
            result["url"] = fm["url"]
        result["category"] = fm.get("category")
        result["decision_status"] = c["status"]
        result["summary"] = fm.get("summary")
        result["tags"] = fm.get("tags") or []
        result["score"] = score
        results.append(result)

    results.sort(key=lambda r: (-r["score"], (r["title"] or "").lower(), (r["name"] or "").lower()))

    total = len(results)
    truncated = total > limit

    return {
        "results": results[:limit],
        "total": total,
        "truncated": truncated,
    }
