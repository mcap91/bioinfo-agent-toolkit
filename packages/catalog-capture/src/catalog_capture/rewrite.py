"""Rewrite `⚠ needs-link <reddit /s/ or /comments/ url>` inbox lines in place (R2/R3/R4/R8, G1).

Only lines matching NEEDS_LINK_RE are touched; every other byte in the inbox
(prose, headers, other ⚠ reasons, non-Reddit urls) is left untouched because
`re.sub` only replaces matched spans. A successful capture becomes a fenced
```text block whose first line is `source: <canonical url>` — the exact shape
`inbox.ts` parses (FENCE_OPEN/FENCE_CLOSE/SOURCE_LINE). A capture failure becomes
`⚠ capture-failed <url> — <error>`; a PDF download event becomes `⚠ pdf <url>`
(both still match inbox.ts's ⚠-url pattern, so drain keeps them blocked, R8).
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from .canonical import canonical_url, post_id
from .capture import CaptureResult, PdfDownloadError
from .fence import defuse_fence_breaks
from .sources import render_source_md, write_source_file

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
# other can't resolve stays `⚠ needs-link` forever. (Review, 2026-10-26: a
# 23-URL parity run against both real implementations found 5 mismatches —
# trailing slash, a query string on a share/comments id, an uppercase host,
# and an underscore in the id — all fixed by this version; see test_parity.py.)
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

DEFAULT_DELAY_S = 3.0


@dataclass
class ItemResult:
    url: str
    status: str  # 'ok' | 'pdf' | 'failed'
    canonical: str | None = None
    post_id: str | None = None
    error: str | None = None


CaptureFn = Callable[[str], CaptureResult]


def process_needs_link(
    text: str,
    *,
    sources_dir: Path,
    capture_fn: CaptureFn,
    limit: int | None = None,
    delay_s: float = DEFAULT_DELAY_S,
) -> tuple[str, list[ItemResult]]:
    """Replace every Reddit needs-link line (up to `limit`) with its outcome.

    Capture happens sequentially, with `delay_s` between loads (not before the
    first), per the WK-0054 session-state decision to avoid tripping Reddit's
    rate limits by running concurrently.
    """
    results: list[ItemResult] = []
    count = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        url = m.group(1)
        if limit is not None and count >= limit:
            return m.group(0)
        if count > 0 and delay_s:
            time.sleep(delay_s)
        count += 1

        try:
            cap = capture_fn(url)
        except PdfDownloadError:
            results.append(ItemResult(url=url, status="pdf"))
            return f"⚠ pdf {url}"
        except Exception as e:  # noqa: BLE001 - fail loud, keep the line blocked
            err = " ".join(str(e).split())
            results.append(ItemResult(url=url, status="failed", error=err))
            return f"⚠ capture-failed {url} — {err}"

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
            results.append(ItemResult(url=url, status="failed", error=failure_reason))
            return f"⚠ capture-failed {url} — {failure_reason}"

        safe_text = defuse_fence_breaks(cap.body_text)
        captured_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        md = render_source_md(
            canonical=canonical,
            captured_at=captured_at,
            playwright_version=cap.playwright_version,
            chromium_version=cap.chromium_version,
            text=cap.body_text,  # R8: sources file gets the verbatim capture.
        )
        write_source_file(sources_dir, pid, md)
        results.append(ItemResult(url=url, status="ok", canonical=canonical, post_id=pid))
        return f"```text\nsource: {canonical}\n{safe_text}\n```"

    out = NEEDS_LINK_RE.sub(repl, text)
    return out, results
