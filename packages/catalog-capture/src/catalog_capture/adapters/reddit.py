"""Reddit post/share-link adapter (WK-0094 Phase B; formerly `rewrite.py` +
`sources.py`'s Reddit half). Needs-link URL rule, id parse, capture (via the
shared `stages.browser` page-capture stage), block body, and sources-file
body/artifacts all live here — the registry and the shared renderer/writer
know nothing Reddit-specific.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from ..canonical import canonical_url, post_id
from ..registry import BaseAdapter, CaptureFailedError, CaptureOutcome, NeedsLinkSoftMarker
from ..stages import browser

# Reddit post/share hosts + path shapes (G1/WK-0080). Scheme is optional — a
# needs-link line can be written back scheme-less (drain.ts's `ensureMarker`
# preserves the original raw text, and a bare "www.reddit.com/..." line parses
# fine as a url). Host is www/old/new/np/m.reddit.com or bare reddit.com,
# case-insensitive (drain.ts gets this for free — WHATWG URL lowercases the
# parsed hostname — so this regex is compiled with re.IGNORECASE to match).
# Path is /r/<sub>/s/<id>, /r/<sub>/comments/<id>(/...), /user/<u>/comments/<id>
# (/...), or bare /comments/<id>(/...); the id itself is `[^/\s?#]+` (anything
# but a slash/whitespace/query/fragment — same permissiveness as drain.ts's
# `[^/]+`, so an id with an underscore or a trailing `/`, `?...`, or `#...`
# still matches). This must stay mirrored with `urlUnfetchable` in
# packages/catalog-mcp/src/core/drain.ts, or a line one side blocks and the
# other can't resolve stays `⚠ needs-link` forever (tests/test_parity.py).
NEEDS_LINK_RE = re.compile(
    r"^⚠ needs-link ("
    r"(?:https?://)?(?:(?:www|old|new|np|m)\.)?reddit\.com"
    r"(?:/r/[^/\s]+/s/[^/\s?#]+(?:[/?#]\S*)?"
    r"|/r/[^/\s]+/comments/[^/\s?#]+(?:[/?#]\S*)?"
    r"|/user/[^/\s]+/comments/[^/\s?#]+(?:[/?#]\S*)?"
    r"|/comments/[^/\s?#]+(?:[/?#]\S*)?)"
    r")(?:\s+—\s+[^\n]*)?$",
    re.MULTILINE | re.IGNORECASE,
)

# Broader than NEEDS_LINK_RE: any needs-link line that mentions reddit.com at
# all, matched or not, so a malformed/unexpected shape is surfaced instead of
# silently left in the inbox with no explanation. Case-insensitive to match
# NEEDS_LINK_RE (a line this misses as "unmatched" would never get flagged).
BROAD_REDDIT_NEEDS_LINK_LINE = re.compile(r"^⚠ needs-link [^\n]*reddit\.com[^\n]*$", re.MULTILINE | re.IGNORECASE)


@dataclass
class _RedditRaw:
    cap: browser.CaptureResult
    canonical: str
    pid: str


class RedditAdapter(BaseAdapter):
    name = "reddit"
    platform_dir = "reddit"
    # WK-0094 Phase B review fix-up: one shared default (`BaseAdapter.
    # DEFAULT_DELAY_S`), not a `DEFAULT_DELAY_S = 3.0` literal copied into
    # this module.
    delay_s = BaseAdapter.DEFAULT_DELAY_S
    line_re = NEEDS_LINK_RE
    broad_re = BROAD_REDDIT_NEEDS_LINK_LINE
    broad_hint = "/s/ pattern"
    # The PDF soft-marker status this adapter can produce — declared so the
    # needs-link summary line always shows a "pdf" count (even 0) whenever
    # this adapter participates in a run (cli.py).
    status_buckets = ("pdf",)

    def __init__(self, capture_fn: Callable[[str], browser.CaptureResult] = browser.capture_page):
        self._capture_fn = capture_fn

    def capture(self, url: str) -> _RedditRaw:
        try:
            cap = self._capture_fn(url)
        except browser.PdfDownloadError:
            raise NeedsLinkSoftMarker(f"pdf {url}", "pdf") from None
        except Exception as e:  # noqa: BLE001 - fail loud, keep the line blocked
            raise CaptureFailedError(" ".join(str(e).split())) from e

        canonical = canonical_url(cap.final_url)
        pid = post_id(canonical)

        # S3: a stalled JS challenge / block page must not be accepted as success.
        # WK-0054 evidence log: probe.py's default-UA run on these same links
        # stalled with an empty title and 0 comments — i.e. the wait-table
        # selector never appeared. Treat that shape, a blank body, or an
        # unresolvable post id as a capture failure, not a silent bad write.
        failure_reason: str | None = None
        if not cap.body_text.strip():
            failure_reason = "blank page body"
        elif not cap.wait_matched:
            failure_reason = "stalled: shreddit-post never loaded (JS challenge or block page, WK-0054 evidence)"
        elif pid is None:
            failure_reason = f"no Reddit post id in canonical url {canonical}"

        if failure_reason is not None:
            raise CaptureFailedError(failure_reason)

        return _RedditRaw(cap=cap, canonical=canonical, pid=pid)

    def build_outcome(self, raw: _RedditRaw, *, captured_at: str) -> CaptureOutcome:
        return CaptureOutcome(
            id=raw.pid,
            source=raw.canonical,
            block_sections=[raw.cap.body_text],  # defused once, by the shared renderer
            source_header_lines=[
                f"source: {raw.canonical}",
                f"captured: {captured_at}",
                f"playwright: {raw.cap.playwright_version}",
                f"chromium: {raw.cap.chromium_version}",
            ],
            source_body=f"{raw.cap.body_text}\n",  # R8: sources file gets the verbatim capture, never defused
        )

    # -- review (WK-0094): rebuild review sections from an already-written
    # sources .md, so `review build` can run anytime against catalog/sources/
    # without needing a live capture or the gitignored workbench. --------

    def review_items(self, sources_dir: Path):
        from ..review import ReviewItem

        out_dir = Path(sources_dir) / self.platform_dir
        items = []
        if not out_dir.is_dir():
            return items
        for md_path in sorted(out_dir.glob("*.md")):
            text = md_path.read_text(encoding="utf-8")
            lines = text.split("\n")
            url = ""
            if lines and lines[0].startswith("source: "):
                url = lines[0][len("source: "):]
            body = text.split("\n\n", 1)[1] if "\n\n" in text else ""
            items.append(ReviewItem(
                adapter=self.name,
                item_id=md_path.stem,
                url=url,
                sections=[("What we captured", f"<details>\n<summary>Full captured page text</summary>\n\n```\n{body.strip()}\n```\n\n</details>")],
            ))
        return items
