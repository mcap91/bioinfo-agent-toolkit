"""`search` command: semantic scoring with BM25 keyword rescue over catalog entries."""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path
from typing import Any

from . import embeddings
from .build import run_build
from .frontmatter import read_all_entries
from .vectors import cosine_similarity, is_valid, read_vectors

DEFAULT_LIMIT = 200

BM25_K1 = 1.2
BM25_B = 0.75
BM25_RESCUE_CAP = 0.5  # max score BM25 can assign; prevents lexical from outranking strong semantic
BM25_TOKENIZE_RE = re.compile(r"[^a-z0-9]+")


def _bm25_tokenize(text: str) -> list[str]:
    return [t for t in BM25_TOKENIZE_RE.split(text.lower()) if t]


def _entry_text(frontmatter: dict, body: str) -> str:
    """Concatenate all searchable fields into one document string."""
    parts = [
        str(frontmatter.get("title") or ""),
        str(frontmatter.get("name") or ""),
        str(frontmatter.get("summary") or ""),
        body,
        " ".join(str(t) for t in (frontmatter.get("tags") or [])),
    ]
    return " ".join(parts)


def bm25_score_all(
    entries: list[tuple[str, dict, str]],  # [(name, frontmatter, body), ...]
    query_terms: list[str],
) -> dict[str, float]:
    """Compute BM25 scores for all entries against query terms. Returns {name: score}."""
    # Tokenize all documents
    docs: dict[str, list[str]] = {}
    for name, fm, body in entries:
        docs[name] = _bm25_tokenize(_entry_text(fm, body))

    N = len(docs)
    if N == 0:
        return {}

    avgdl = sum(len(d) for d in docs.values()) / N

    # Document frequency per query term
    df: dict[str, int] = {}
    for term in query_terms:
        df[term] = sum(1 for d in docs.values() if term in d)

    # Score each document
    scores: dict[str, float] = {}
    for name, tokens in docs.items():
        score = 0.0
        dl = len(tokens)
        for term in query_terms:
            tf = tokens.count(term)
            if tf == 0:
                continue
            idf = math.log((N - df[term] + 0.5) / (df[term] + 0.5) + 1)
            numerator = tf * (BM25_K1 + 1)
            denominator = tf + BM25_K1 * (1 - BM25_B + BM25_B * dl / avgdl)
            score += idf * numerator / denominator
        scores[name] = score
    return scores


def run_search(
    dir: Path,
    query: str,
    limit: int = DEFAULT_LIMIT,
    threshold: float = 0.0,
    method: str = "fusion",  # "fusion" | "semantic" | "bm25" — for eval baselines
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

        cosine = 0.0
        if query_vector is not None and name in entry_vectors:
            cosine = max(0.0, min(1.0, cosine_similarity(query_vector, entry_vectors[name])))

        candidates.append(
            {
                "name": name,
                "frontmatter": frontmatter,
                "status": status,
                "body": body,
                "cosine": cosine,
            }
        )

    def _build_result(c: dict[str, Any], score: float) -> dict[str, Any]:
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
        return result

    # Tokenize query with BM25 tokenizer (same as document tokenization)
    bm25_query_terms = _bm25_tokenize(query)

    # Empty query: return all entries with score=0 (filtered listing mode)
    if not bm25_query_terms:
        results = [_build_result(c, 0.0) for c in candidates]
        results.sort(key=lambda r: (-r["score"], (r["title"] or "").lower(), (r["name"] or "").lower()))
        total = len(results)
        truncated = total > limit
        return {
            "results": results[:limit],
            "total": total,
            "truncated": truncated,
        }

    bm25_scores = bm25_score_all(
        [(c["name"], c["frontmatter"], c["body"]) for c in candidates],
        bm25_query_terms,
    )
    max_bm25 = max(bm25_scores.values(), default=0.0)

    results: list[dict[str, Any]] = []
    for c in candidates:
        cosine = c["cosine"]
        capped_bm25 = (bm25_scores.get(c["name"], 0.0) / max_bm25 * BM25_RESCUE_CAP) if max_bm25 > 0 else 0.0

        if method == "semantic":
            score = cosine
        elif method == "bm25":
            score = capped_bm25
        else:  # fusion
            score = max(cosine, capped_bm25)

        if score <= threshold:
            continue

        results.append(_build_result(c, score))

    results.sort(key=lambda r: (-r["score"], (r["title"] or "").lower(), (r["name"] or "").lower()))

    total = len(results)
    truncated = total > limit

    return {
        "results": results[:limit],
        "total": total,
        "truncated": truncated,
    }
