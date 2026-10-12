"""Field-weighted lexical scorer, ported from search.ts. Must match TS ranking exactly."""

from __future__ import annotations

from .taxonomy import TaxonomyIndex, expand_term, tokenize

DEFAULT_TEXT_FIELDS = ["title", "summary", "name", "body"]

FIELD_WEIGHT: dict[str, int] = {
    "title": 10,
    "name": 5,
    "summary": 3,
    "body": 1,
}
TAG_WEIGHT = 5


def _field_text(field: str, frontmatter: dict, body: str) -> str:
    if field == "body":
        return body
    val = frontmatter.get(field)
    if isinstance(val, list):
        return " ".join(str(v) for v in val)
    return "" if val is None else str(val)


def score_entry(
    frontmatter: dict,
    body: str,
    query_terms: list[str],
    tax_index: TaxonomyIndex,
    text_fields: list[str] | None = None,
) -> int:
    fields = text_fields if text_fields is not None else DEFAULT_TEXT_FIELDS

    field_tokens: dict[str, set[str]] = {
        f: set(tokenize(_field_text(f, frontmatter, body))) for f in fields
    }

    tags = frontmatter.get("tags") or []
    tag_tokens: set[str] = set()
    for tag in tags:
        tag_tokens.add(str(tag).lower())
        tag_tokens.update(tokenize(str(tag)))

    score = 0
    for term in query_terms:
        candidates = set(expand_term(term, tax_index)) | set(tokenize(term))

        for field, tokens in field_tokens.items():
            if any(c in tokens for c in candidates):
                score += FIELD_WEIGHT.get(field, 1)

        if any(c in tag_tokens for c in candidates):
            score += TAG_WEIGHT

    return score
