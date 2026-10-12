from pathlib import Path

import pytest

from catalog_embedder import embeddings
from catalog_embedder.build import run_build
from catalog_embedder.search import run_search
from conftest import write_entry


def fake_embed_texts(texts: list[str]) -> list[list[float]]:
    # Deterministic 2-dim stand-in: presence of "pdf" dominates the vector.
    return [[1.0, 0.0] if "pdf" in t.lower() else [0.0, 1.0] for t in texts]


@pytest.fixture(autouse=True)
def patch_embeddings(monkeypatch):
    monkeypatch.setattr(embeddings, "embed_texts", fake_embed_texts)


def test_search_output_shape_and_types(catalog_dir: Path):
    entries_dir = catalog_dir / "catalog" / "entries"
    write_entry(entries_dir, "pdf-tool", "PDF Tool", "cli-tool", "parses pdf files", ["pdf", "ocr"], "pdf body")
    write_entry(entries_dir, "spreadsheet-tool", "Spreadsheet Tool", "cli-tool", "excel things", ["excel"], "excel body")

    run_build(catalog_dir)
    response = run_search(catalog_dir, "pdf")

    assert set(response.keys()) == {"results", "total", "truncated"}
    assert isinstance(response["total"], int)
    assert isinstance(response["truncated"], bool)
    assert isinstance(response["results"], list)

    assert response["total"] == 1  # spreadsheet-tool has lexical score 0, filtered out
    result = response["results"][0]
    assert result["name"] == "pdf-tool"
    assert result["title"] == "PDF Tool"
    assert result["category"] == "cli-tool"
    assert result["decision_status"] == "open"  # defaulted, absent from frontmatter
    assert isinstance(result["summary"], str)
    assert isinstance(result["tags"], list)
    assert isinstance(result["score"], float)
    assert "url" not in result  # omitted when absent from frontmatter


def test_results_sorted_by_score_desc_then_title_then_name(catalog_dir: Path):
    entries_dir = catalog_dir / "catalog" / "entries"
    # Both match "pdf" lexically in title (equal lexical score); same semantic bucket too.
    write_entry(entries_dir, "zzz-pdf", "Zzz Pdf Tool", "cli-tool", "pdf", [], "pdf")
    write_entry(entries_dir, "aaa-pdf", "Aaa Pdf Tool", "cli-tool", "pdf", [], "pdf")

    run_build(catalog_dir)
    response = run_search(catalog_dir, "pdf")

    names = [r["name"] for r in response["results"]]
    assert names == ["aaa-pdf", "zzz-pdf"]  # tie broken by title alphabetically


def test_truncated_true_when_total_exceeds_limit(catalog_dir: Path):
    entries_dir = catalog_dir / "catalog" / "entries"
    for i in range(5):
        write_entry(entries_dir, f"pdf-tool-{i}", f"Pdf Tool {i}", "cli-tool", "pdf", [], "pdf")

    run_build(catalog_dir)
    response = run_search(catalog_dir, "pdf", limit=2)

    assert response["total"] == 5
    assert response["truncated"] is True
    assert len(response["results"]) == 2


def test_decision_status_filter(catalog_dir: Path):
    entries_dir = catalog_dir / "catalog" / "entries"
    (entries_dir / "pdf-open.md").write_text(
        "---\n"
        "name: pdf-open\n"
        "title: Pdf Open\n"
        "category: cli-tool\n"
        'summary: "pdf"\n'
        "tags: []\n"
        "decision_status: adopted\n"
        "---\n\npdf\n",
        encoding="utf-8",
    )

    run_build(catalog_dir)
    response = run_search(catalog_dir, "pdf", decision_status="adopted")

    assert response["total"] == 1
    assert response["results"][0]["decision_status"] == "adopted"


def test_category_filter(catalog_dir: Path):
    entries_dir = catalog_dir / "catalog" / "entries"
    write_entry(entries_dir, "pdf-cli", "Pdf Cli", "cli-tool", "pdf", [], "pdf")
    write_entry(entries_dir, "pdf-lib", "Pdf Lib", "library", "pdf", [], "pdf")

    run_build(catalog_dir)
    response = run_search(catalog_dir, "pdf", category="library")

    assert response["total"] == 1
    assert response["results"][0]["name"] == "pdf-lib"
