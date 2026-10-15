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

    assert set(response.keys()) == {"results", "swept_terms", "lexical_total", "total"}
    assert response["lexical_total"] == 1
    # spreadsheet-tool has cosine 0 under the fake embedder, so no semantic suggestion
    assert response["total"] == 1
    result = response["results"][0]
    assert "score" not in result
    assert result["match"]["type"] == "lexical"
    assert "pdf" in result["match"]["terms"]
    assert "title" in result["match"]["fields"]
    assert response["swept_terms"] == [{"term": "pdf", "hits": 1}]


def test_lexical_ties_break_by_title(catalog_dir: Path):
    entries_dir = catalog_dir / "catalog" / "entries"
    # Both match "pdf" lexically in title (equal lexical score); same semantic bucket too.
    write_entry(entries_dir, "zzz-pdf", "Zzz Pdf Tool", "cli-tool", "pdf", [], "pdf")
    write_entry(entries_dir, "aaa-pdf", "Aaa Pdf Tool", "cli-tool", "pdf", [], "pdf")

    run_build(catalog_dir)
    response = run_search(catalog_dir, "pdf")

    names = [r["name"] for r in response["results"]]
    assert names == ["aaa-pdf", "zzz-pdf"]  # tie broken by title alphabetically


def test_lexical_set_is_never_truncated(catalog_dir: Path):
    entries_dir = catalog_dir / "catalog" / "entries"
    for i in range(5):
        write_entry(entries_dir, f"pdf-tool-{i}", f"Pdf Tool {i}", "cli-tool", "pdf", [], "pdf")

    run_build(catalog_dir)
    response = run_search(catalog_dir, "pdf")

    assert response["lexical_total"] == 5
    assert len(response["results"]) == 5


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

    assert response["lexical_total"] == 1
    assert response["results"][0]["decision_status"] == "adopted"


def test_category_filter(catalog_dir: Path):
    entries_dir = catalog_dir / "catalog" / "entries"
    write_entry(entries_dir, "pdf-cli", "Pdf Cli", "cli-tool", "pdf", [], "pdf")
    write_entry(entries_dir, "pdf-lib", "Pdf Lib", "library", "pdf", [], "pdf")

    run_build(catalog_dir)
    response = run_search(catalog_dir, "pdf", category="library")

    assert response["lexical_total"] == 1
    assert response["results"][0]["name"] == "pdf-lib"


def test_empty_query_with_category_filter_lists_only_that_category(catalog_dir: Path):
    entries_dir = catalog_dir / "catalog" / "entries"
    write_entry(entries_dir, "pdf-cli", "Pdf Cli", "cli-tool", "pdf", [], "pdf")
    write_entry(entries_dir, "pdf-lib", "Pdf Lib", "library", "pdf", [], "pdf")

    run_build(catalog_dir)
    response = run_search(catalog_dir, "", category="library")

    assert response["total"] == 1
    assert response["results"][0]["name"] == "pdf-lib"
    assert response["results"][0]["match"] == {"type": "listing"}
    assert response["swept_terms"] == []


def test_miss_returns_semantic_suggestions(catalog_dir: Path):
    entries_dir = catalog_dir / "catalog" / "entries"
    write_entry(entries_dir, "pdf-tool", "PDF Tool", "cli-tool", "parses pdf files", ["pdf", "ocr"], "pdf body")

    run_build(catalog_dir)
    response = run_search(catalog_dir, "pdf", terms=["xylophone"])

    assert response["lexical_total"] == 0
    assert response["swept_terms"] == [{"term": "xylophone", "hits": 0}]
    assert response["results"][0]["match"] == {"type": "semantic", "rank": 1}
    assert response["results"][0]["name"] == "pdf-tool"


def test_miss_with_no_positive_cosine_returns_empty_results(catalog_dir: Path):
    entries_dir = catalog_dir / "catalog" / "entries"
    write_entry(entries_dir, "spreadsheet-tool", "Spreadsheet Tool", "cli-tool", "excel things", ["excel"], "excel body")

    run_build(catalog_dir)
    response = run_search(catalog_dir, "pdf", terms=["xylophone"])

    assert response["results"] == []
    assert response["lexical_total"] == 0
    assert response["swept_terms"] != []


def test_nonempty_query_tokenizing_to_nothing_is_miss_with_semantic(catalog_dir: Path):
    entries_dir = catalog_dir / "catalog" / "entries"
    write_entry(entries_dir, "spreadsheet-tool", "Spreadsheet Tool", "cli-tool", "excel things", ["excel"], "excel body")

    run_build(catalog_dir)
    response = run_search(catalog_dir, "!!!")

    assert response["lexical_total"] == 0
    assert response["swept_terms"] == [{"term": "!!!", "hits": 0}]
    assert response["results"][0]["match"] == {"type": "semantic", "rank": 1}
    assert response["results"][0]["name"] == "spreadsheet-tool"


def test_run_search_rejects_out_of_bounds_inputs(catalog_dir: Path):
    entries_dir = catalog_dir / "catalog" / "entries"
    write_entry(entries_dir, "pdf-tool", "PDF Tool", "cli-tool", "parses pdf files", ["pdf"], "pdf body")
    run_build(catalog_dir)

    with pytest.raises(ValueError):
        run_search(catalog_dir, "pdf", terms=["t"] * 51)
    with pytest.raises(ValueError):
        run_search(catalog_dir, "pdf", terms=["x" * 201])
    with pytest.raises(ValueError):
        run_search(catalog_dir, "p" * 2001)
    with pytest.raises(ValueError):
        run_search(catalog_dir, "pdf", semantic_n=0)
    with pytest.raises(ValueError):
        run_search(catalog_dir, "pdf", semantic_n=51)


def test_semantic_excludes_lexical_members_and_zero_cosine(catalog_dir: Path):
    entries_dir = catalog_dir / "catalog" / "entries"
    write_entry(entries_dir, "pdf-tool", "PDF Tool", "cli-tool", "parses pdf files", ["pdf"], "pdf body")
    write_entry(entries_dir, "spreadsheet-tool", "Spreadsheet Tool", "cli-tool", "excel things", ["excel"], "excel body")

    run_build(catalog_dir)
    response = run_search(catalog_dir, "pdf", terms=["pdf"])

    assert response["total"] == 1
    names = [r["name"] for r in response["results"]]
    assert "spreadsheet-tool" not in names


def test_semantic_n_bounds_suggestions(catalog_dir: Path):
    entries_dir = catalog_dir / "catalog" / "entries"
    for i in range(3):
        write_entry(entries_dir, f"pdf-tool-{i}", f"Pdf Tool {i}", "cli-tool", "pdf stuff", [], "pdf body")

    run_build(catalog_dir)
    response = run_search(catalog_dir, "pdf", terms=["xylophone"], semantic_n=2)

    assert response["total"] == 2
    ranks = [r["match"]["rank"] for r in response["results"]]
    assert ranks == [1, 2]


def test_semantic_n_out_of_range_raises(catalog_dir: Path):
    entries_dir = catalog_dir / "catalog" / "entries"
    write_entry(entries_dir, "pdf-tool", "PDF Tool", "cli-tool", "parses pdf files", ["pdf"], "pdf body")
    run_build(catalog_dir)

    with pytest.raises(ValueError):
        run_search(catalog_dir, "pdf", semantic_n=0)
    with pytest.raises(ValueError):
        run_search(catalog_dir, "pdf", semantic_n=51)
