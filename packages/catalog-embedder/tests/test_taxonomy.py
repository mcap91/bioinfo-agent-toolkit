import json
from pathlib import Path

from catalog_embedder.lexical import score_entry
from catalog_embedder.taxonomy import build_index, expand_term, load_taxonomy, tokenize


def test_tokenize_splits_on_non_alphanumeric():
    assert tokenize("PDF-Parsing_Tool!") == ["pdf", "parsing", "tool"]


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


def test_expand_term_returns_full_group_for_alias():
    index = build_index({"meta-skill": ["skill-generation", "skill-loader"]})
    expanded = set(expand_term("skill-loader", index))
    assert expanded == {"meta-skill", "skill-generation", "skill-loader"}


def test_expand_term_returns_full_group_for_canonical():
    index = build_index({"meta-skill": ["skill-generation", "skill-loader"]})
    expanded = set(expand_term("meta-skill", index))
    assert expanded == {"meta-skill", "skill-generation", "skill-loader"}


def test_expand_term_unknown_term_returns_itself():
    index = build_index({"meta-skill": ["skill-generation"]})
    assert expand_term("unrelated-term", index) == ["unrelated-term"]


def test_taxonomy_expansion_bridges_vocabulary_gap_in_scoring():
    index = build_index({"meta-skill": ["skill-loader"]})
    fm = {"title": "meta-skill framework", "summary": "", "tags": []}
    # Query uses the alias "skill-loader"; it must match via the canonical group.
    score = score_entry(fm, "", ["skill-loader"], index)
    assert score == 10  # title match only
