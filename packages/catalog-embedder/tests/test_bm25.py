from pathlib import Path

import pytest

from catalog_embedder import embeddings
from catalog_embedder.build import run_build
from catalog_embedder.search import _bm25_tokenize, bm25_score_all, run_search
from conftest import write_entry


def test_exact_name_scores_highest():
    entries = [
        ("markitdown", {"title": "MarkItDown", "name": "markitdown", "summary": "converts docs", "tags": []}, "body"),
        ("other-tool", {"title": "Other Tool", "name": "other-tool", "summary": "markdown converter", "tags": []}, "body"),
    ]
    scores = bm25_score_all(entries, ["markitdown"])
    assert scores["markitdown"] > scores["other-tool"]


def test_rare_term_scores_higher_than_common():
    entries = [
        ("tool-a", {"title": "chandra OCR", "name": "tool-a", "summary": "ocr tool", "tags": []}, "body"),
        ("tool-b", {"title": "general tool", "name": "tool-b", "summary": "a tool", "tags": ["tool"]}, "body"),
    ]
    scores = bm25_score_all(entries, ["chandra"])
    assert scores["tool-a"] > 0
    assert scores["tool-b"] == 0


def test_empty_query_returns_zeros():
    entries = [("x", {"title": "X", "name": "x", "summary": "s", "tags": []}, "")]
    scores = bm25_score_all(entries, [])
    assert scores["x"] == 0.0


def test_no_entries_returns_empty():
    scores = bm25_score_all([], ["pdf"])
    assert scores == {}


def test_punctuated_query_matches():
    """F4 fix: query tokenizer strips punctuation like document tokenizer."""
    entries = [
        ("markitdown", {"title": "MarkItDown", "name": "markitdown", "summary": "converts", "tags": []}, ""),
    ]
    scores = bm25_score_all(entries, _bm25_tokenize("markitdown?"))
    assert scores["markitdown"] > 0


def test_hyphenated_query_splits():
    """F4 fix: 'chandra-ocr' becomes ['chandra', 'ocr']."""
    entries = [
        ("chandra", {"title": "chandra OCR", "name": "chandra-ocr", "summary": "ocr", "tags": []}, ""),
    ]
    scores = bm25_score_all(entries, _bm25_tokenize("chandra-ocr"))
    assert scores["chandra"] > 0


def fake_embed_texts(texts: list[str]) -> list[list[float]]:
    # Deterministic 2-dim stand-in: presence of "pdf" dominates the vector.
    return [[1.0, 0.0] if "pdf" in t.lower() else [0.0, 1.0] for t in texts]


@pytest.fixture(autouse=True)
def patch_embeddings(monkeypatch):
    monkeypatch.setattr(embeddings, "embed_texts", fake_embed_texts)


def test_empty_query_lists_all_entries(catalog_dir: Path):
    entries_dir = catalog_dir / "catalog" / "entries"
    write_entry(entries_dir, "one", "One", "cli-tool", "summary", [], "body")
    write_entry(entries_dir, "two", "Two", "cli-tool", "summary", [], "body")

    run_build(catalog_dir)
    response = run_search(catalog_dir, "")

    assert response["total"] == 2
    assert response["swept_terms"] == []
    assert response["lexical_total"] == 0
    for r in response["results"]:
        assert r["match"] == {"type": "listing"}
        assert "score" not in r
