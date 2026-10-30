"""Inbox line replacement on a copy of the real catalog/inbox.md: only the 18
Reddit `⚠ needs-link /s/` lines change, every other byte stays identical, and
the output still parses under the real inbox.ts (not a reimplementation)."""

import re
from pathlib import Path

import pytest

from catalog_capture.adapters.reddit import NEEDS_LINK_RE, RedditAdapter
from catalog_capture.registry import process_needs_link
from catalog_capture.stages.browser import CaptureResult

from conftest import ts_parse_inbox


@pytest.fixture
def fake_capture(golden_capture):
    """A capture stand-in whose body is the real golden-fixture text (rule 24),
    tagged per share id so each of the 18 synthetic captures is distinguishable."""
    _, real_body_text = golden_capture

    def _capture(url: str) -> CaptureResult:
        share_id = url.rsplit("/", 1)[-1]
        sub = re.search(r"/r/([^/]+)/s/", url).group(1)
        return CaptureResult(
            final_url=f"https://www.reddit.com/r/{sub}/comments/post{share_id}/some_title/?solution=x",
            title="t",
            body_text=f"{real_body_text}\n[share:{share_id}]",
            playwright_version="1.64.1",
            chromium_version="156.0.8078.4",
        )

    return _capture


def _process(text, *, sources_dir, fake_capture, limit=None):
    adapters = [RedditAdapter(capture_fn=fake_capture)]
    return process_needs_link(text, sources_dir=sources_dir, adapters=adapters, limit=limit, delay_s=0)


def test_only_reddit_needs_link_lines_change(real_inbox_text: str, fake_capture, tmp_path: Path):
    target_lines = NEEDS_LINK_RE.findall(real_inbox_text)
    assert len(target_lines) == 18  # WK-0054/WK-0080 corpus size

    out_text, results = _process(real_inbox_text, sources_dir=tmp_path / "sources", fake_capture=fake_capture)
    assert len(results) == 18
    assert all(r.status == "ok" for r in results)

    before_lines = real_inbox_text.split("\n")
    after_lines = out_text.split("\n")

    # Diff line-by-line: changed lines must be exactly the 18 original marker
    # lines (now expanded to multi-line blocks) — everything else is untouched.
    changed_originals = [ln for ln in before_lines if ln not in after_lines]
    needs_link_prefix = "⚠ needs-link https://www.reddit.com/r/"
    assert len(changed_originals) == 18
    assert all(ln.startswith(needs_link_prefix) for ln in changed_originals)

    # Every unrelated line (prose, headers, other urls) survives byte-for-byte.
    unrelated_before = [ln for ln in before_lines if not ln.startswith(needs_link_prefix)]
    for ln in unrelated_before:
        assert ln in after_lines

    # 18 new fenced blocks were added (the inbox already has 1 unrelated ```text block).
    before_fences = real_inbox_text.count("```text\n")
    assert out_text.count("```text\n") == before_fences + 18


def test_rewritten_inbox_still_parses_under_the_real_ts_parser(real_inbox_text: str, fake_capture, tmp_path: Path):
    out_text, _ = _process(real_inbox_text, sources_dir=tmp_path / "sources", fake_capture=fake_capture)
    inbox_path = tmp_path / "inbox.md"
    inbox_path.write_text(out_text, encoding="utf-8")

    items = ts_parse_inbox(inbox_path)
    text_items = [i for i in items if i["kind"] == "text" and i.get("source", "").startswith("https://www.reddit.com/")]
    assert len(text_items) == 18
    share_ids = set()
    for item in text_items:
        assert item["blocked"] is False  # unblocked — R6, ready to drain
        assert item["content"].startswith("Skip to main content")  # real golden-fixture text, not invented prose
        m = re.search(r"\[share:([^\]]+)\]$", item["content"])
        assert m is not None
        share_ids.add(m.group(1))
    assert len(share_ids) == 18  # each of the 18 captures is distinguishable


def test_limit_caps_how_many_lines_are_processed(real_inbox_text: str, fake_capture, tmp_path: Path):
    out_text, results = _process(real_inbox_text, sources_dir=tmp_path / "sources", fake_capture=fake_capture, limit=1)
    assert len(results) == 1
    # 17 needs-link lines remain untouched.
    assert len(NEEDS_LINK_RE.findall(out_text)) == 17


def test_source_files_written_for_every_captured_item(real_inbox_text: str, fake_capture, tmp_path: Path):
    sources_dir = tmp_path / "sources"
    _process(real_inbox_text, sources_dir=sources_dir, fake_capture=fake_capture)
    written = sorted(p.name for p in (sources_dir / "reddit").glob("*.md"))
    assert len(written) == 18


# G1 (WK-0080): one blocking rule must cover every Reddit post/share host+path
# shape drain.ts's `urlUnfetchable` can block — a line blocked there but
# unmatched here would stay `⚠ needs-link` forever. URL is real
# (toolkit-workbench/web-capture/results.csv row 1, query string stripped per
# R3); host/scheme variants are derived from it. The /user/ and bare /comments/
# cases keep the same real post id in the other path shapes the unified rule
# documents.
CANONICAL_COMMENTS_URL = (
    "https://www.reddit.com/r/LocalLLaMA/comments/1x9gfnb/"
    "google_open_sources_harness2_for_self_improving/"
)
_COMMENTS_PATH = "/r/LocalLLaMA/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/"


@pytest.mark.parametrize(
    "line_url",
    [
        CANONICAL_COMMENTS_URL,
        f"https://old.reddit.com{_COMMENTS_PATH}",
        f"https://new.reddit.com{_COMMENTS_PATH}",
        f"https://np.reddit.com{_COMMENTS_PATH}",
        f"https://m.reddit.com{_COMMENTS_PATH}",
        f"https://reddit.com{_COMMENTS_PATH}",
        f"www.reddit.com{_COMMENTS_PATH}",  # scheme-less, as drain.ts can write it back
        "https://www.reddit.com/user/someuser/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/",
        "https://www.reddit.com/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/",
    ],
)
def test_canonical_comments_needs_link_line_is_captured(line_url, golden_capture, tmp_path: Path):
    _, real_body_text = golden_capture

    def fake_capture(url: str) -> CaptureResult:
        assert url == line_url
        return CaptureResult(
            final_url=CANONICAL_COMMENTS_URL,
            title="t",
            body_text=real_body_text,
            playwright_version="1.64.1",
            chromium_version="156.0.8078.4",
        )

    inbox = f"⚠ needs-link {line_url}\n"
    out_text, results = _process(inbox, sources_dir=tmp_path / "sources", fake_capture=fake_capture)
    assert len(results) == 1
    assert results[0].status == "ok"
    assert out_text == f"```text\nsource: {CANONICAL_COMMENTS_URL}\n{real_body_text}\n```\n"
