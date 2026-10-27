"""Canonical URL + post id derivation (R3).

Final URLs below are copied verbatim from toolkit-workbench/web-capture/results.csv
(own contender, run=first) — not invented. They cover both the plain-post case and
the share-targets-a-comment case (`/comment/<id>/` kept, R3).
"""

from catalog_capture.canonical import canonical_url, post_id

# own,https://www.reddit.com/r/LocalLLaMA/s/JNjEe87YeN,first,<final_url>,...
JNJEE87YEN_FINAL = (
    "https://www.reddit.com/r/LocalLLaMA/comments/1x9gfnb/"
    "google_open_sources_harness2_for_self_improving/"
    "?solution=a4165de0094a7ecca4165de0094a7ecc&js_challenge=1"
    "&jsc_token=2824be10929bdc604753c70a67a1c331e0333fda4750d7afb2ada3b0f6998192"
    "&jsc_orig_r=&share_id=n02JeGeg0GpR3to3J9kb-&utm_content=1"
    "&utm_medium=android_app&utm_name=androidcss&utm_source=share&utm_term=10"
)

# own,https://www.reddit.com/r/LocalLLM/s/SuMGmAmj6L,first,<final_url>,... (targets a comment)
SUMGMAMJ6L_FINAL = (
    "https://www.reddit.com/r/LocalLLM/comments/1x1rv5k/comment/pew7oqh/"
    "?solution=8853d9eae953b49b8853d9eae953b49b&js_challenge=1"
    "&jsc_token=2824be10929bdc604753c70a67a1c3312c11ed0c6d7d6c75505680d7ee3a04ca"
    "&jsc_orig_r=&share_id=PIfOHi7BSogLiy4mvEjbI&utm_content=2"
    "&utm_medium=android_app&utm_name=androidcss&utm_source=share&utm_term=10"
)


def test_strips_query_string_from_plain_post():
    assert canonical_url(JNJEE87YEN_FINAL) == (
        "https://www.reddit.com/r/LocalLLaMA/comments/1x9gfnb/"
        "google_open_sources_harness2_for_self_improving/"
    )


def test_keeps_comment_path_when_share_targets_a_comment():
    assert canonical_url(SUMGMAMJ6L_FINAL) == "https://www.reddit.com/r/LocalLLM/comments/1x1rv5k/comment/pew7oqh/"


def test_post_id_extracted_from_canonical_url():
    assert post_id(canonical_url(JNJEE87YEN_FINAL)) == "1x9gfnb"
    assert post_id(canonical_url(SUMGMAMJ6L_FINAL)) == "1x1rv5k"


def test_post_id_is_none_without_a_comments_segment():
    assert post_id("https://www.reddit.com/r/LocalLLaMA/") is None
