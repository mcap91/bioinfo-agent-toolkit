"""Parity test (G1/WK-0080 review): drain.ts's `urlUnfetchable` (exercised via
the real `drainInbox()`) and this package's `NEEDS_LINK_RE` must agree on
every URL, or a line one side blocks and the other can't resolve stays
`⚠ needs-link` forever.

Shared URL list: the host/scheme/path variants already covered elsewhere in
this suite, plus the 5 mismatches the reviewer found by feeding 23 URLs
through both real implementations — a trailing slash after a share id, a
query string on a share id, a query string on a comments id, an uppercase
host, and an id containing an underscore — all real shapes a pasted or
redirected Reddit URL can take.
"""

from catalog_capture.adapters.reddit import NEEDS_LINK_RE

from conftest import ts_check_unfetchable

_PATH = "/r/LocalLLaMA/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/"

PARITY_URLS = [
    # blocked: share link + host/scheme/path variants
    "https://www.reddit.com/r/AI_Agents/s/kClxACXOyp",
    f"https://www.reddit.com{_PATH}",
    f"https://old.reddit.com{_PATH}",
    f"https://new.reddit.com{_PATH}",
    f"https://np.reddit.com{_PATH}",
    f"https://m.reddit.com{_PATH}",
    f"https://reddit.com{_PATH}",
    f"www.reddit.com{_PATH}",  # scheme-less
    "https://www.reddit.com/r/LocalLLM/comments/1x1rv5k/comment/pew7oqh/",  # comment-target
    "https://www.reddit.com/user/someuser/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/",
    "https://www.reddit.com/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/",  # bare /comments/
    # blocked: the 5 mismatches the reviewer found against the real implementations
    "https://www.reddit.com/r/AI_Agents/s/kClxACXOyp/",  # trailing slash
    "https://www.reddit.com/r/AI_Agents/s/kClxACXOyp?utm_source=share",  # query on a share id
    "https://www.reddit.com/r/LocalLLaMA/comments/1x9gfnb?utm=1",  # query on a comments id
    f"https://WWW.Reddit.com{_PATH}",  # uppercase host
    "https://www.reddit.com/r/AI_Agents/comments/hh_9/some_title/",  # underscore in the id
    # unblocked: no post id to capture, or not Reddit at all
    "https://www.reddit.com/r/LocalLLaMA/",
    "https://www.reddit.com/r/LocalLLaMA/wiki/index",
    "https://github.com/org/tool",
    "https://notreddit.com/r/sub/comments/abc/",
]


def test_drain_and_needs_link_re_agree_on_every_url():
    ts_blocked = ts_check_unfetchable(PARITY_URLS)
    assert len(ts_blocked) == len(PARITY_URLS)

    mismatches = []
    for url, blocked_by_drain in zip(PARITY_URLS, ts_blocked):
        matched_by_regex = bool(NEEDS_LINK_RE.match(f"⚠ needs-link {url}"))
        if blocked_by_drain != matched_by_regex:
            mismatches.append((url, blocked_by_drain, matched_by_regex))
    assert not mismatches, f"drain/regex verdict mismatch (url, ts_blocked, py_matched): {mismatches}"

    # Sanity: both outcomes actually occur, or this test would pass trivially.
    assert any(ts_blocked)
    assert not all(ts_blocked)
