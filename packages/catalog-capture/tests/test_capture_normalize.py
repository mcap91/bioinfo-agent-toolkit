"""normalize_reddit_url (G1/WK-0080): before Playwright navigates, any Reddit
host variant collapses to https://www.reddit.com<path> so `_host()`/WAIT_TABLE
("reddit.com") and the Chrome UA always see the host Reddit's own web client
uses. Mirrors the host rule in drain.ts `urlUnfetchable` and this package's
`rewrite.NEEDS_LINK_RE`. URL is real (toolkit-workbench/web-capture/results.csv
row 1, query string stripped per R3); host/scheme variants are derived from it.
"""

import pytest

from catalog_capture.stages.browser import normalize_reddit_url

PATH = "/r/LocalLLaMA/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/"
CANONICAL = f"https://www.reddit.com{PATH}"


@pytest.mark.parametrize(
    "variant",
    [
        CANONICAL,
        f"https://old.reddit.com{PATH}",
        f"https://new.reddit.com{PATH}",
        f"https://np.reddit.com{PATH}",
        f"https://m.reddit.com{PATH}",
        f"https://reddit.com{PATH}",
        f"www.reddit.com{PATH}",  # scheme-less, as drain.ts can write it back
        f"old.reddit.com{PATH}",
    ],
)
def test_reddit_host_variants_normalize_to_www_https(variant: str):
    assert normalize_reddit_url(variant) == CANONICAL


def test_non_reddit_url_is_returned_unchanged():
    url = "https://github.com/org/tool"
    assert normalize_reddit_url(url) == url


def test_non_reddit_host_containing_reddit_substring_is_unchanged():
    # Guards against a sloppy "contains reddit.com" check matching a lookalike host.
    url = "https://notreddit.com/r/sub/comments/abc/"
    assert normalize_reddit_url(url) == url
