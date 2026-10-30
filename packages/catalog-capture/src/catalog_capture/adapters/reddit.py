"""Reddit post/share-link adapter (WK-0094 Phase B; formerly `rewrite.py` +
`sources.py`'s Reddit half). Needs-link URL rule, id parse, capture (via the
shared `stages.browser` page-capture stage), block body, and sources-file
body/artifacts all live here — the registry and the shared renderer/writer
know nothing Reddit-specific.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
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

# -- Removed-post hard check + post+comments slice (WK-0097 OR-10) --------
#
# Every marker string below is quoted verbatim from a real tracked capture
# under catalog/sources/reddit/ (27 files, read 2026-10-30) — none invented.
#
# Every capture's body opens with the same seven-line header chrome, e.g.
# catalog/sources/reddit/1x9gfnb.md:6-12 and .../1x2856v.md:6-12:
#   "Skip to main content"
#   "<title> : r/<sub>"
#   "Sign Up"
#   "Log In"
#   "Expand user menu"
#   "Go to <sub>"
#   "r/<sub>"
# the 7th line (always starting "r/") is the header/post boundary in all 27.
#
# The post's own "Share" button is the first line literally "Share" after
# the header (1x2856v.md:18; 1x9gfnb.md:32). Everything from there through
# "Comments Section" is pre-comments chrome: an ad block (1x2856v.md:19-24,
# "Roblox" / "Ad" / ... / "roblox.com"; 1x9gfnb.md:33-37, "anthropic-ai" /
# "Ad" / ... / "claude.com"), an optional "Collapse video player" line, then
# the fixed "Sort by:" / "Comments Section" pair that opens every file's
# comment thread (1x2856v.md:25-26; 1x9gfnb.md:39-40).
_SHARE_LINE = "Share"
_COMMENTS_SECTION_LINE = "Comments Section"

# Comments end where footer/sidebar chrome begins. "More posts you may
# like" (immediately followed by "Related posts") opens that footer in all
# 27 files (1x2856v.md:37-38; 1x9gfnb.md:276-277). Where present, "People
# also ask about section" (1x9gfnb.md:269) starts a few lines earlier and is
# itself sidebar/SEO chrome, not a real comment — treated as an equally
# valid, earlier footer start.
_FOOTER_MARKERS = ("People also ask about section", "More posts you may like")

# Reddit's two post-removal shapes seen in these captures: the community-
# filter removal (1x2856v.md:17, "Sorry, this post was removed by Reddit's
# filters.") and the author's own deletion (1x5mrkq.md:17, "Sorry, this post
# was deleted by the person who originally posted it."). Both share the
# "Sorry, this post was " prefix right after the repeated post-title line —
# that prefix is the hard, deterministic removed-post check (OR-10).
_REMOVED_POST_RE = re.compile(r"^Sorry, this post was .*$", re.MULTILINE)

# Any http(s) link surviving in the sliced post+comments text is a salvage
# candidate (OR-10: "if we can capture the repo, that is the whole point")
# — e.g. 1x2856v.md:33, "https://github.com/oxynote/oxynote", inside the
# one surviving comment.
_LINK_RE = re.compile(r"https?://\S+")


def _slice_post_and_comments(body_text: str) -> str:
    """Strip header, pre-comments ad, and footer/sidebar chrome, keeping
    only the post and its comments (WK-0097 OR-10). Falls back to leaving a
    region untouched when an expected marker is missing, rather than
    raising — an odd/short capture should degrade to "keep more text", not
    lose content."""
    lines = body_text.split("\n")

    header_end = next((i for i, line in enumerate(lines) if line.startswith("r/")), None)
    start = header_end + 1 if header_end is not None else 0

    share_idx = next((i for i in range(start, len(lines)) if lines[i] == _SHARE_LINE), None)
    post_end = share_idx if share_idx is not None else len(lines)

    comments_start = post_end
    if share_idx is not None:
        comments_idx = next(
            (i for i in range(share_idx, len(lines)) if lines[i] == _COMMENTS_SECTION_LINE), None
        )
        if comments_idx is not None:
            comments_start = comments_idx + 1

    footer_idx = len(lines)
    for marker in _FOOTER_MARKERS:
        try:
            footer_idx = min(footer_idx, lines.index(marker, comments_start))
        except ValueError:
            continue

    sliced_lines = lines[start:post_end] + lines[comments_start:footer_idx]
    return "\n".join(sliced_lines).strip("\n")


def _salvage_links(text: str) -> list[str]:
    """Distinct http(s) links in `text`, in first-seen order, with trailing
    sentence punctuation stripped."""
    seen: dict[str, None] = {}
    for match in _LINK_RE.finditer(text):
        link = match.group(0).rstrip(".,;:)]>")
        seen.setdefault(link, None)
    return list(seen)


@dataclass
class _RedditRaw:
    cap: browser.CaptureResult
    canonical: str
    pid: str
    sliced_text: str
    removed: bool = False
    salvaged_links: list[str] = field(default_factory=list)


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

        # OR-10 hard check: a removed/deleted post with no surviving,
        # salvageable comment link is not worth capturing at all — fail
        # loud and keep the needs-link line blocked, instead of writing
        # 175 lines of page chrome around one removal sentence (the
        # oxynote evidence this check exists for).
        sliced_text = _slice_post_and_comments(cap.body_text)
        removed_match = _REMOVED_POST_RE.search(sliced_text)
        salvaged_links: list[str] = []
        if removed_match is not None:
            salvaged_links = _salvage_links(sliced_text)
            if not salvaged_links:
                raise CaptureFailedError(
                    f"removed post (marker: {removed_match.group(0)!r}) — no surviving comment links to salvage"
                )

        return _RedditRaw(
            cap=cap,
            canonical=canonical,
            pid=pid,
            sliced_text=sliced_text,
            removed=removed_match is not None,
            salvaged_links=salvaged_links,
        )

    def build_outcome(self, raw: _RedditRaw, *, captured_at: str) -> CaptureOutcome:
        if raw.removed:
            salvage_note = (
                "Reddit removed this post. Salvaging the surviving comment link(s) as the subject(s):\n"
                + "\n".join(f"- {link}" for link in raw.salvaged_links)
            )
            sections = [salvage_note, raw.sliced_text]
        else:
            sections = [raw.sliced_text]

        return CaptureOutcome(
            id=raw.pid,
            source=raw.canonical,
            block_sections=sections,  # defused once, by the shared renderer
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
