from catalog_embedder.lexical import score_entry
from catalog_embedder.taxonomy import build_index


def make_index():
    return build_index({})


def test_title_match_weight_10():
    fm = {"title": "PDF Parser", "summary": "does stuff", "tags": []}
    score = score_entry(fm, "irrelevant body", ["pdf"], make_index())
    # "pdf" hits title (10) only
    assert score == 10


def test_matches_across_multiple_fields_sum_weights():
    fm = {
        "title": "pdf tool",
        "name": "pdf-tool",
        "summary": "a pdf summary",
        "tags": ["pdf"],
    }
    body = "pdf body text"
    score = score_entry(fm, body, ["pdf"], make_index())
    # title=10, name=5, summary=3, body=1, tags=5 -> 24
    assert score == 24


def test_one_match_per_field_per_term_no_double_counting():
    fm = {"title": "pdf pdf pdf", "summary": "", "tags": []}
    score = score_entry(fm, "", ["pdf"], make_index())
    assert score == 10


def test_no_match_returns_zero():
    fm = {"title": "spreadsheet tool", "summary": "excel things", "tags": ["excel"]}
    score = score_entry(fm, "no relevant content", ["pdf"], make_index())
    assert score == 0


def test_multiple_query_terms_sum_independently():
    fm = {"title": "pdf ocr tool", "summary": "", "tags": []}
    score = score_entry(fm, "", ["pdf", "ocr"], make_index())
    # each term matches title independently: 10 + 10
    assert score == 20


def test_tags_only_checked_once_per_term_weight_5():
    fm = {"title": "unrelated", "summary": "", "tags": ["machine-learning", "ml"]}
    score = score_entry(fm, "", ["ml"], make_index())
    assert score == 5
