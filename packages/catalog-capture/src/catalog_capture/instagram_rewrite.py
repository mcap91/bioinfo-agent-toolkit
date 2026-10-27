"""Rewrite `⚠ needs-link <instagram.com/reel/... url>` inbox lines in place
(WK-0080 Instagram slice, OR-3).

OR-3 (operator ruling, supersedes G1/G2/I1/I2/I9): "reel -> transcript and
capture of images etc -> agent decides what goes into the catalog ... the
agent should be the one making the call." The capture never verifies a
tool's URL or decides what the reel is "about" — it produces exactly **one**
fenced block per reel, `source: <reel url>`, carrying the caption,
transcript, on-screen text, key claims, and whatever tools/URLs the read
spotted, labeled as unverified hints. Reddit already emits one block per
post (`rewrite.py`); this mirrors that.

Only `/reel/` URLs are matched — Instagram carousels (`/p/`) are a separate,
not-yet-built WK-0080 checklist item (operator-supplied golden carousel
capture pending); a `/p/` needs-link line is left untouched by this module,
same as any other unmatched line.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from .fence import defuse_fence_breaks
from .instagram_capture import InstagramCaptureError, InstagramCaptureResult, cleanup_sheet
from .instagram_sources import render_instagram_source_md, write_instagram_source_files

# Mirrors the host rule this package and drain.ts would need for Instagram —
# but drain.ts already blocks every instagram.com URL unconditionally via
# `hostBlocked()` + `catalog/config.json`'s `blocked_domains` entry (no
# `allow_paths`), regardless of path (I7: confirmed by reading drain.ts —
# `urlUnfetchable` is Reddit-only and does not need an Instagram rule; a
# fenced *text* item's `source` is never re-checked against either rule,
# R6's existing precedent). So this regex only needs to match what this
# package can itself resolve: `/reel/<id>` needs-link lines.
INSTAGRAM_NEEDS_LINK_RE = re.compile(
    r"^⚠ needs-link ("
    r"(?:https?://)?(?:www\.)?instagram\.com/reel/[^/\s?#]+/?(?:[?#]\S*)?"
    r")(?:\s+—\s+[^\n]*)?$",
    re.MULTILINE | re.IGNORECASE,
)

DEFAULT_DELAY_S = 3.0


@dataclass
class InstagramItemResult:
    url: str
    status: str  # 'ok' | 'failed'
    reel_id: str | None = None
    mentioned_count: int = 0
    error: str | None = None


CaptureFn = Callable[[str], InstagramCaptureResult]


def _hint_line(tool: dict) -> str:
    url = tool.get("url")
    return f"- {tool.get('name')}: {url if url else '(no url)'}"


def render_instagram_block(*, reel_url: str, caption: str | None, transcript_text: str,
                            on_screen_text: str, key_claims: list[str], tools: list[dict]) -> str:
    """OR-3: one block per reel, `source:` is always the reel URL itself —
    there is no separate repo `source:` and no per-tool block anymore."""
    claims_block = "\n".join(f"- {c}" for c in key_claims) if key_claims else "(none)"
    hints_block = "\n".join(_hint_line(t) for t in tools) if tools else "(none mentioned)"
    body = (
        f"Caption:\n{caption or '(no caption captured)'}\n"
        "\n"
        f"Transcript:\n{transcript_text}\n"
        "\n"
        f"On-screen text:\n{on_screen_text or '(none)'}\n"
        "\n"
        f"Key claims:\n{claims_block}\n"
        "\n"
        f"Mentioned (unverified hints):\n{hints_block}"
    )
    safe_body = defuse_fence_breaks(body)
    return f"```text\nsource: {reel_url}\n{safe_body}\n```"


def process_instagram_needs_link(
    text: str,
    *,
    sources_dir: Path,
    capture_fn: CaptureFn,
    limit: int | None = None,
    delay_s: float = DEFAULT_DELAY_S,
) -> tuple[str, list[InstagramItemResult]]:
    """Replace every Instagram `/reel/` needs-link line (up to `limit`) with
    its outcome: exactly one fenced block per reel (OR-3), `source:` the reel
    URL — or, on any pipeline failure, `⚠ capture-failed <url> — <stage>:
    <error>` (no silent drops, mirroring the Reddit failure path, R8)."""
    results: list[InstagramItemResult] = []
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
        except InstagramCaptureError as e:
            results.append(InstagramItemResult(url=url, status="failed", error=str(e)))
            return f"⚠ capture-failed {url} — {str(e)}"
        except Exception as e:  # noqa: BLE001 - fail loud, keep the line blocked
            err = " ".join(str(e).split())
            results.append(InstagramItemResult(url=url, status="failed", error=err))
            return f"⚠ capture-failed {url} — {err}"

        stage = "render"
        try:
            block = render_instagram_block(
                reel_url=cap.reel_url, caption=cap.caption, transcript_text=cap.transcript_text,
                on_screen_text=cap.on_screen_text, key_claims=cap.key_claims, tools=cap.tools,
            )

            captured_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            md = render_instagram_source_md(
                reel_url=cap.reel_url, captured_at=captured_at, versions=cap.versions,
                caption=cap.caption, transcript_text=cap.transcript_text,
                on_screen_text=cap.on_screen_text, key_claims=cap.key_claims,
                info_channel=cap.info_channel, tools=cap.tools,
            )
            stage = "write"
            write_instagram_source_files(
                sources_dir, cap.reel_id, md,
                info_json_text=cap.info_json_text, transcript_text=cap.transcript_text,
                sheet_path=cap.sheet_path, read_response_text=cap.read_raw_stdout,
            )
        except OSError as e:
            # One bad write must not cost the rest of the batch: mark this
            # item capture-failed and let `re.sub` move on to the next line.
            err = " ".join(str(e).split())
            results.append(InstagramItemResult(url=url, status="failed", error=f"{stage}: {err}"))
            return f"⚠ capture-failed {url} — {stage}: {err}"
        finally:
            # Delete the loose OS tempfile once we're done reading it (the
            # copy above, or nothing, if that raised) — even on a failure
            # path, so a capture-failed-after-the-fact item never leaks it.
            cleanup_sheet(cap)

        results.append(InstagramItemResult(
            url=url, status="ok", reel_id=cap.reel_id, mentioned_count=len(cap.tools),
        ))
        return block

    out = INSTAGRAM_NEEDS_LINK_RE.sub(repl, text)
    return out, results
