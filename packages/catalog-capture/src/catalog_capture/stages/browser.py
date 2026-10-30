"""Shared browser-page-capture stage (WK-0094 Phase B; formerly `capture.py`).

The WK-0054 "own script" capture engine (ENGINE CHOICE, WK-0054 Results).

Evidence: toolkit-workbench/web-capture/own/capture.py — Chromium headless, Chrome
user agent (clears Reddit's JS challenge; the default UA stalls on it, WK-0054
2026-10-26 evidence log), `goto(wait_until="load", timeout=45000)`, then a soft poll
loop for a per-site selector (never raises on timeout — it keeps the page text
regardless, R1). A PDF `Page.goto: Download is starting` error is a distinct,
expected outcome (WK-0054 probe `own-pdf.log`), not a generic capture failure.

This module is a shared stage: any adapter that needs a real browser page load
(Reddit today; a future login-free page-based source tomorrow) calls into it —
the per-site `WAIT_TABLE` is already designed to hold more than one host.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass
from urllib.parse import urlsplit, urlunsplit

from playwright.sync_api import sync_playwright

from ..versions import playwright_version

CHROME_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
)
VIEWPORT = {"width": 1280, "height": 900}
GOTO_TIMEOUT_MS = 45_000
POLL_ITERATIONS = 10
POLL_INTERVAL_S = 2
DEFAULT_SOFT_WAIT_S = 2

# Per-site wait table (R1): host -> selector to poll for before reading innerText.
# Hosts with no entry get a short default soft wait instead.
WAIT_TABLE: dict[str, str] = {
    "reddit.com": "shreddit-post",
}


class PdfDownloadError(RuntimeError):
    """`goto` triggered a file download instead of loading a page (WK-0054 probe)."""


class CaptureFailedError(RuntimeError):
    """Any other capture failure. Carries the original error text."""


@dataclass
class CaptureResult:
    final_url: str
    title: str
    body_text: str
    playwright_version: str
    chromium_version: str
    # True when no selector was configured for this host, or the configured
    # selector was found before the poll loop gave up. False means the page
    # never rendered the wait-table element — the stalled-JS-challenge shape
    # WK-0054's evidence log describes for probe.py's default-UA run (empty
    # title, 0 comments). Defaults to True so existing success-path callers
    # that build a CaptureResult by hand don't need to set it.
    wait_matched: bool = True


def _host(url: str) -> str:
    h = urlsplit(url).hostname or ""
    return h[4:] if h.startswith("www.") else h


# www/old/new/np/m.reddit.com or bare reddit.com (G1/WK-0080). Mirrors the host
# rule in packages/catalog-mcp/src/core/drain.ts `urlUnfetchable` and the
# Reddit adapter's `NEEDS_LINK_RE` — keep all three in sync.
_REDDIT_HOST_RE = re.compile(r"^(?:(?:www|old|new|np|m)\.)?reddit\.com$", re.IGNORECASE)


def normalize_reddit_url(url: str) -> str:
    """Rewrite any www/old/new/np/m/bare reddit.com URL (scheme optional) to
    `https://www.reddit.com<path>` before navigating, so `_host()`/WAIT_TABLE
    (keyed on "reddit.com") and the JS-challenge-clearing Chrome UA always see
    the host Reddit serves its normal web client on. Non-Reddit URLs, and urls
    whose host isn't a reddit.com variant, are returned unchanged."""
    scheme_prefixed = url if re.match(r"^https?://", url, re.IGNORECASE) else f"https://{url}"
    parts = urlsplit(scheme_prefixed)
    if not _REDDIT_HOST_RE.match(parts.hostname or ""):
        return url
    return urlunsplit(("https", "www.reddit.com", parts.path, parts.query, parts.fragment))


def capture_page(url: str, *, headless: bool = True) -> CaptureResult:
    """Load `url` in headless Chromium and return its resolved URL, title, and
    full `document.body.innerText`. Raises PdfDownloadError or CaptureFailedError."""
    url = normalize_reddit_url(url)
    selector = WAIT_TABLE.get(_host(url))
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        try:
            ctx = browser.new_context(user_agent=CHROME_UA, viewport=VIEWPORT)
            page = ctx.new_page()
            page.goto(url, wait_until="load", timeout=GOTO_TIMEOUT_MS)

            wait_matched = True
            if selector:
                wait_matched = False
                for _ in range(POLL_ITERATIONS):
                    time.sleep(POLL_INTERVAL_S)
                    if page.evaluate(f"document.querySelectorAll({selector!r}).length"):
                        wait_matched = True
                        break
            else:
                time.sleep(DEFAULT_SOFT_WAIT_S)

            final_url = page.url
            title = page.title()
            body_text = page.evaluate("document.body ? document.body.innerText : ''")
            chromium_version = browser.version
        except Exception as e:  # noqa: BLE001 - distinguish PDF vs. everything else
            if "Download is starting" in str(e):
                raise PdfDownloadError(url) from e
            raise CaptureFailedError(str(e)) from e
        finally:
            browser.close()

    return CaptureResult(
        final_url=final_url,
        title=title,
        body_text=body_text,
        playwright_version=playwright_version(),
        chromium_version=chromium_version,
        wait_matched=wait_matched,
    )
