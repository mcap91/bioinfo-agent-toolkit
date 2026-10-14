import json
from pathlib import Path

from catalog_embedder.taxonomy import build_index, load_taxonomy


def test_load_taxonomy_reads_canonical_groups(tmp_path: Path):
    taxonomy_dir = tmp_path / "catalog"
    taxonomy_dir.mkdir()
    (taxonomy_dir / "taxonomy.json").write_text(
        json.dumps({"canonical": {"meta-skill": ["skill-generation", "skill-loader"]}}),
        encoding="utf-8",
    )
    canonical = load_taxonomy(tmp_path)
    assert canonical == {"meta-skill": ["skill-generation", "skill-loader"]}


def test_load_taxonomy_missing_file_returns_empty(tmp_path: Path):
    assert load_taxonomy(tmp_path) == {}
