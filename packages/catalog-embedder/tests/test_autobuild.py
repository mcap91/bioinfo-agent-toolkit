import json
from pathlib import Path

import pytest

from catalog_embedder import embeddings
from catalog_embedder.search import run_search
from catalog_embedder.vectors import MODEL_NAME, vectors_path
from conftest import write_entry


def fake_embed_texts(texts: list[str]) -> list[list[float]]:
    return [[1.0, 0.0] for _ in texts]


@pytest.fixture(autouse=True)
def patch_embeddings(monkeypatch):
    monkeypatch.setattr(embeddings, "embed_texts", fake_embed_texts)


def test_search_triggers_build_when_vector_file_missing(catalog_dir: Path):
    entries_dir = catalog_dir / "catalog" / "entries"
    write_entry(entries_dir, "pdf-tool", "PDF Tool", "cli-tool", "pdf", [], "pdf")

    assert not vectors_path(catalog_dir).exists()

    response = run_search(catalog_dir, "pdf")

    assert vectors_path(catalog_dir).exists()
    assert response["total"] == 1


def test_search_triggers_rebuild_on_model_mismatch(catalog_dir: Path):
    entries_dir = catalog_dir / "catalog" / "entries"
    write_entry(entries_dir, "pdf-tool", "PDF Tool", "cli-tool", "pdf", [], "pdf")

    vectors_path(catalog_dir).write_text(
        json.dumps({"model": "some-other-model", "dims": 10, "count": 0, "entries": {}}),
        encoding="utf-8",
    )

    run_search(catalog_dir, "pdf")

    data = json.loads(vectors_path(catalog_dir).read_text(encoding="utf-8"))
    assert data["model"] == MODEL_NAME
    assert "pdf-tool" in data["entries"]
