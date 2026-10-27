"""Canonical URL + post id derivation (R3).

Evidence: toolkit-workbench/web-capture/results.csv (own contender, first run) — all
18 corpus links resolve `/s/<id>` to a final URL of the shape
`https://www.reddit.com/r/<sub>/comments/<post_id>/<slug>/?solution=...&js_challenge=...`,
or, when the share targets a comment,
`https://www.reddit.com/r/<sub>/comments/<post_id>/comment/<comment_id>/?...`.
The canonical URL is the final URL with the query string (and fragment) removed;
the `/comment/<id>/` suffix is kept when present.
"""

from __future__ import annotations

import re
from urllib.parse import urlsplit, urlunsplit

POST_ID_RE = re.compile(r"/comments/([A-Za-z0-9]+)/")


def canonical_url(final_url: str) -> str:
    """Strip the query string and fragment from a resolved Reddit URL, and
    lowercase the host (G1/WK-0080 review: the unified host rule is
    case-insensitive end to end)."""
    parts = urlsplit(final_url)
    return urlunsplit((parts.scheme, parts.netloc.lower(), parts.path, "", ""))


def post_id(canonical: str) -> str | None:
    """Extract the Reddit post id (the segment right after `/comments/`)."""
    m = POST_ID_RE.search(canonical)
    return m.group(1) if m else None
