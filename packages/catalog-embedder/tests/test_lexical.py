from pathlib import Path

from catalog_embedder.search import lexical_members, resolve_terms


def _write(d: Path, name: str, text: str) -> None:
    (d / f"{name}.md").write_text(text, encoding="utf-8")


def test_prefix_matches_morphology(tmp_path):
    _write(tmp_path, "a", "---\nname: a\n---\nagents love sandboxing here")
    members, hits = lexical_members(tmp_path, ["a"], ["sandbox"])
    assert "a" in members and hits["sandbox"] == 1


def test_prefix_rejects_midword(tmp_path):
    _write(tmp_path, "s", "---\nname: s\n---\nthe socratic method")
    members, hits = lexical_members(tmp_path, ["s"], ["ocr"])
    assert members == {} and hits["ocr"] == 0


def test_multiword_term_is_and_of_tokens(tmp_path):
    _write(tmp_path, "m", "---\nname: m\n---\nagentic memoryless systems for all")
    _write(tmp_path, "n", "---\nname: n\n---\nagentic things only")
    members, _ = lexical_members(tmp_path, ["m", "n"], ["agent memory"])
    assert "m" in members and "n" not in members  # prefix: agent->agentic, memory->memoryless


def test_regex_metacharacters_escaped(tmp_path):
    _write(tmp_path, "c", "---\nname: c\n---\nwe use c++ tooling")
    members, _ = lexical_members(tmp_path, ["c"], ["c++"])
    assert "c" in members


def test_punctuation_leading_term(tmp_path):
    """'.net' matches standalone '.NET' but not 'asp.net'."""
    _write(tmp_path, "yes", "---\nname: yes\n---\nuse the .NET sdk")
    _write(tmp_path, "no", "---\nname: no\n---\nhosted on asp.net only")
    members, hits = lexical_members(tmp_path, ["yes", "no"], [".net"])
    assert "yes" in members and "no" not in members and hits[".net"] == 1


def test_case_insensitive(tmp_path):
    _write(tmp_path, "o", "---\nname: o\n---\nPaddleOCR does OCR")
    members, _ = lexical_members(tmp_path, ["o"], ["ocr"])
    assert "o" in members


def test_resolve_terms_explicit_dedupe():
    assert resolve_terms(["  OCR ", "ocr", ""], "ignored") == ["ocr"]  # dedupe, no silent truncation


def test_resolve_terms_fallback_is_single_and_term():
    """Query-only falls back to ONE AND term with deduped tokens."""
    assert resolve_terms([], "parsing PDFs? parsing") == ["parsing pdfs"]
    assert resolve_terms(None, "") == []
    assert resolve_terms([], "日本語") == []  # non-ASCII tokenizes to nothing
