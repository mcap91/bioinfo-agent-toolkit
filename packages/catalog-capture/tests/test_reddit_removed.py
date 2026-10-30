"""OR-10 (WK-0097 prep c): removed-post hard check, post+comments slice,
surviving-link salvage — all derived from the real tracked Reddit captures
under catalog/sources/reddit/ (27 files, read 2026-10-30), never synthesized
chrome. The oxynote capture (1x2856v.md) is the golden fixture named by the
handoff: a post removed by Reddit's filters, with one surviving comment
linking github.com/oxynote/oxynote.

Captures are read in place from catalog/sources/reddit/ rather than copied
into tests/fixtures/ (WK-0096 moves real captures out of the public repo) —
a test whose source file is absent skips cleanly instead of failing.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from catalog_capture.adapters.reddit import RedditAdapter
from catalog_capture.registry import CaptureFailedError
from catalog_capture.rendering import render_block
from catalog_capture.stages.browser import CaptureResult

TESTS_DIR = Path(__file__).parent
PACKAGE_DIR = TESTS_DIR.parent
REPO_ROOT = PACKAGE_DIR.parent.parent
SOURCES_DIR = REPO_ROOT / "catalog" / "sources" / "reddit"

OXYNOTE_PATH = SOURCES_DIR / "1x2856v.md"
OXYNOTE_URL = "https://www.reddit.com/r/SATNA_PROJECT/comments/1x2856v/the_500mo_stack_for_0_5_new_opensource_ai/"
OXYNOTE_REPO_LINK = "https://github.com/oxynote/oxynote"

HARNESS2_PATH = SOURCES_DIR / "1x9gfnb.md"
HARNESS2_URL = (
    "https://www.reddit.com/r/LocalLLaMA/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/"
)

PLAYWRIGHT_VERSION = "1.64.1"
CHROMIUM_VERSION = "156.0.8078.4"


def _body_text_from_source_md(path: Path) -> str:
    """Recover the raw captured `body_text` from a written sources .md:
    header lines, a blank line, then the verbatim body (R8 /
    `sources_writer.render_source_md` — the same split `RedditAdapter.
    review_items` already uses to read these files back)."""
    text = path.read_text(encoding="utf-8")
    return text.split("\n\n", 1)[1]


def _require_real_capture(path: Path) -> str:
    if not path.is_file():
        pytest.skip(f"real capture missing: {path} (WK-0096 moves captures out of the public repo)")
    return _body_text_from_source_md(path)


def _fake_capture_fn(body_text: str, final_url: str):
    def _capture(url: str) -> CaptureResult:
        return CaptureResult(
            final_url=final_url,
            title="t",
            body_text=body_text,
            playwright_version=PLAYWRIGHT_VERSION,
            chromium_version=CHROMIUM_VERSION,
        )

    return _capture


# --------------------------------------------------------------------------
# Golden fixture: the real oxynote capture (removed post, one surviving
# comment with a GitHub repo link).
# --------------------------------------------------------------------------


def test_oxynote_removed_post_is_detected_and_salvages_the_repo_link():
    body_text = _require_real_capture(OXYNOTE_PATH)
    adapter = RedditAdapter(capture_fn=_fake_capture_fn(body_text, OXYNOTE_URL))

    raw = adapter.capture(OXYNOTE_URL)
    assert raw.removed is True
    assert raw.salvaged_links == [OXYNOTE_REPO_LINK]

    outcome = adapter.build_outcome(raw, captured_at="2026-10-30")
    block = render_block(source=outcome.source, sections=outcome.block_sections)

    # Block starts with a deterministic removed-post note naming the
    # salvaged link as the subject, then the sliced post+comments.
    assert outcome.block_sections[0].startswith("Reddit removed this post.")
    assert OXYNOTE_REPO_LINK in outcome.block_sections[0]
    assert outcome.block_sections[1] == raw.sliced_text

    assert "busters1" in block
    assert "collaboration platform that lets engineering teams" in block
    assert OXYNOTE_REPO_LINK in block

    assert "Skip to main content" not in block
    assert "Roblox" not in block
    assert "Forget mindless scrolling" not in block  # the Roblox ad's own copy
    assert "More posts you may like" not in block
    assert "Related posts" not in block

    # R8: the sources .md body stays the verbatim, unsliced capture.
    assert "Skip to main content" in outcome.source_body
    assert "More posts you may like" in outcome.source_body


# --------------------------------------------------------------------------
# Live (not removed) post: a real capture whose own body must survive the
# slice unchanged, with only the header/ad/sidebar chrome sliced away.
# --------------------------------------------------------------------------


def test_live_post_body_survives_the_slice_and_sidebar_is_gone():
    body_text = _require_real_capture(HARNESS2_PATH)
    adapter = RedditAdapter(capture_fn=_fake_capture_fn(body_text, HARNESS2_URL))

    raw = adapter.capture(HARNESS2_URL)
    assert raw.removed is False
    assert raw.salvaged_links == []

    outcome = adapter.build_outcome(raw, captured_at="2026-10-30")
    assert outcome.block_sections == [raw.sliced_text]
    block = render_block(source=outcome.source, sections=outcome.block_sections)

    # The post's own text, unchanged, including its own repo link.
    assert "Google just released Harness2 as open source." in block
    assert "GitHub https://github.com/google-research/harness2" in block
    # A real, unedited comment, unchanged.
    assert "I am a bot and this action was performed automatically." in block

    # Header chrome, the pre-comments ad, and the footer/sidebar are gone.
    assert "Skip to main content" not in block
    assert "anthropic-ai" not in block
    assert "More posts you may like" not in block
    assert "Related posts" not in block
    assert "Reddit Rules" not in block


# --------------------------------------------------------------------------
# Removed + no surviving link to salvage -> fail loud, naming the marker.
# Derived by editing the real oxynote capture (dropping the one comment's
# link), not a hand-made page.
# --------------------------------------------------------------------------


def test_removed_post_with_no_salvageable_link_fails_loud():
    body_text = _require_real_capture(OXYNOTE_PATH)
    no_link_body = body_text.replace(f"{OXYNOTE_REPO_LINK}\n", "")
    assert OXYNOTE_REPO_LINK not in no_link_body  # the edit actually removed the only link

    adapter = RedditAdapter(capture_fn=_fake_capture_fn(no_link_body, OXYNOTE_URL))

    with pytest.raises(CaptureFailedError) as exc_info:
        adapter.capture(OXYNOTE_URL)

    message = str(exc_info.value)
    assert "removed post" in message
    assert "Sorry, this post was removed by Reddit" in message
