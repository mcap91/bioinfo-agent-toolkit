"""CLI entry point: `python -m catalog_capture capture|needs-link|instagram-capture|instagram-needs-link ...`"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from .canonical import canonical_url, post_id
from .capture import capture_page
from .instagram_capture import capture_instagram_reel, cleanup_sheet
from .instagram_rewrite import (
    DEFAULT_DELAY_S as INSTAGRAM_DEFAULT_DELAY_S,
)
from .instagram_rewrite import (
    INSTAGRAM_NEEDS_LINK_RE,
    process_instagram_needs_link,
    render_instagram_block,
)
from .instagram_sources import render_instagram_source_md, write_instagram_source_files
from .rewrite import DEFAULT_DELAY_S, NEEDS_LINK_RE, process_needs_link
from .sources import render_source_md

# Broader than NEEDS_LINK_RE: any needs-link line that mentions reddit.com at
# all, matched or not, so a malformed/unexpected shape is surfaced instead of
# silently left in the inbox with no explanation. Case-insensitive to match
# NEEDS_LINK_RE (a line this misses as "unmatched" would never get flagged).
BROAD_REDDIT_NEEDS_LINK_LINE = re.compile(r"^⚠ needs-link [^\n]*reddit\.com[^\n]*$", re.MULTILINE | re.IGNORECASE)


def _unmatched_reddit_needs_link_lines(text: str) -> list[str]:
    return [ln for ln in BROAD_REDDIT_NEEDS_LINK_LINE.findall(text) if not NEEDS_LINK_RE.match(ln)]


# Same idea as BROAD_REDDIT_NEEDS_LINK_LINE, for Instagram: any needs-link line
# mentioning instagram.com, matched or not — so a carousel (`/p/...`, not yet
# built, WK-0080 checklist) or any other unhandled Instagram shape is surfaced
# by name instead of silently staying `⚠ needs-link` forever with no
# explanation of why this tool skipped it.
BROAD_INSTAGRAM_NEEDS_LINK_LINE = re.compile(r"^⚠ needs-link [^\n]*instagram\.com[^\n]*$", re.MULTILINE | re.IGNORECASE)


def _unmatched_instagram_needs_link_lines(text: str) -> list[str]:
    return [ln for ln in BROAD_INSTAGRAM_NEEDS_LINK_LINE.findall(text) if not INSTAGRAM_NEEDS_LINK_RE.match(ln)]


def _cmd_capture(args: argparse.Namespace) -> int:
    cap = capture_page(args.url)
    canonical = canonical_url(cap.final_url)
    pid = post_id(canonical) or "capture"
    captured_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    md = render_source_md(
        canonical=canonical,
        captured_at=captured_at,
        playwright_version=cap.playwright_version,
        chromium_version=cap.chromium_version,
        text=cap.body_text,
    )
    if args.out:
        Path(args.out).write_text(md, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        sys.stdout.write(md)
    return 0


def run_needs_link(
    inbox_path: Path,
    sources_dir: Path,
    *,
    capture_fn=capture_page,
    limit: int | None = None,
    delay_s: float = DEFAULT_DELAY_S,
) -> int:
    """Read, process, and write back `inbox_path`. A multi-minute run reads the
    file once and writes once (S2): write to a tmp file then `os.replace` (atomic
    on POSIX), and before writing, compare mtime+size against the values at read
    time. If the file changed underneath us (someone edited it mid-run), abort
    without writing — the already-captured source files still exist on disk, and
    we print which URLs they belong to so nothing is silently lost."""
    text = inbox_path.read_text(encoding="utf-8")
    stat_before = inbox_path.stat()

    unmatched = _unmatched_reddit_needs_link_lines(text)

    out_text, results = process_needs_link(
        text, sources_dir=sources_dir, capture_fn=capture_fn, limit=limit, delay_s=delay_s
    )

    stat_after = inbox_path.stat()
    if (stat_before.st_mtime_ns, stat_before.st_size) != (stat_after.st_mtime_ns, stat_after.st_size):
        print(
            f"ABORTED: {inbox_path} changed on disk during this run — not written back.",
            file=sys.stderr,
        )
        captured = [r for r in results if r.status == "ok"]
        print(
            f"{len(captured)} item(s) were captured before the abort "
            f"(their source files remain in {sources_dir}):",
            file=sys.stderr,
        )
        for r in captured:
            print(f"  captured, not written to inbox: {r.url} -> {r.canonical}", file=sys.stderr)
        return 1

    tmp_path = inbox_path.with_name(inbox_path.name + ".tmp")
    tmp_path.write_text(out_text, encoding="utf-8")
    os.replace(tmp_path, inbox_path)

    ok = sum(1 for r in results if r.status == "ok")
    pdf = sum(1 for r in results if r.status == "pdf")
    failed = sum(1 for r in results if r.status == "failed")
    print(f"needs-link: {len(results)} processed — {ok} captured, {pdf} pdf, {failed} failed")
    for r in results:
        if r.status == "failed":
            print(f"  capture-failed: {r.url} — {r.error}")
        elif r.status == "pdf":
            print(f"  pdf: {r.url}")
    for ln in unmatched:
        print(f"  not matched by the /s/ pattern (manual check needed): {ln}")
    if failed:
        print(f"FAILED: {failed} item(s) could not be captured (see above).", file=sys.stderr)
    return 1 if failed else 0


def _cmd_needs_link(args: argparse.Namespace) -> int:
    return run_needs_link(
        Path(args.inbox),
        Path(args.sources),
        capture_fn=capture_page,
        limit=args.limit,
        delay_s=args.delay,
    )


def _cmd_instagram_capture(args: argparse.Namespace) -> int:
    cap = capture_instagram_reel(args.url)
    try:
        captured_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        if args.sources:
            md = render_instagram_source_md(
                reel_url=cap.reel_url, captured_at=captured_at, versions=cap.versions,
                caption=cap.caption, transcript_text=cap.transcript_text,
                on_screen_text=cap.on_screen_text, key_claims=cap.key_claims,
                info_channel=cap.info_channel, tools=cap.tools,
            )
            write_instagram_source_files(
                Path(args.sources), cap.reel_id, md,
                info_json_text=cap.info_json_text, transcript_text=cap.transcript_text,
                sheet_path=cap.sheet_path, read_response_text=cap.read_raw_stdout,
            )
            print(f"wrote {args.sources}/instagram/{cap.reel_id}.md")

        # OR-3: exactly one block per reel, source: the reel URL itself.
        out_text = render_instagram_block(
            reel_url=cap.reel_url, caption=cap.caption, transcript_text=cap.transcript_text,
            on_screen_text=cap.on_screen_text, key_claims=cap.key_claims, tools=cap.tools,
        ) + "\n"
    finally:
        cleanup_sheet(cap)

    if args.out:
        Path(args.out).write_text(out_text, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        sys.stdout.write(out_text)
    return 0


def run_instagram_needs_link(
    inbox_path: Path,
    sources_dir: Path,
    *,
    capture_fn=capture_instagram_reel,
    limit: int | None = None,
    delay_s: float = INSTAGRAM_DEFAULT_DELAY_S,
) -> int:
    """Instagram counterpart of `run_needs_link` — same read-once/write-once
    atomic protocol (S2) and same conflict-abort behaviour, applied to
    `INSTAGRAM_NEEDS_LINK_RE` lines instead of Reddit's."""
    text = inbox_path.read_text(encoding="utf-8")
    stat_before = inbox_path.stat()

    unmatched = _unmatched_instagram_needs_link_lines(text)

    out_text, results = process_instagram_needs_link(
        text, sources_dir=sources_dir, capture_fn=capture_fn, limit=limit, delay_s=delay_s
    )

    stat_after = inbox_path.stat()
    if (stat_before.st_mtime_ns, stat_before.st_size) != (stat_after.st_mtime_ns, stat_after.st_size):
        print(
            f"ABORTED: {inbox_path} changed on disk during this run — not written back.",
            file=sys.stderr,
        )
        captured = [r for r in results if r.status == "ok"]
        print(
            f"{len(captured)} item(s) were captured before the abort "
            f"(their source files remain in {sources_dir}):",
            file=sys.stderr,
        )
        for r in captured:
            print(f"  captured, not written to inbox: {r.url} -> reel {r.reel_id}", file=sys.stderr)
        return 1

    tmp_path = inbox_path.with_name(inbox_path.name + ".tmp")
    tmp_path.write_text(out_text, encoding="utf-8")
    os.replace(tmp_path, inbox_path)

    ok = sum(1 for r in results if r.status == "ok")
    failed = sum(1 for r in results if r.status == "failed")
    print(f"instagram-needs-link: {len(results)} processed — {ok} captured, {failed} failed")
    for r in results:
        if r.status == "failed":
            print(f"  capture-failed: {r.url} — {r.error}")
        elif r.status == "ok":
            print(f"  captured reel {r.reel_id}: {r.mentioned_count} tool(s) mentioned (unverified)")
    for ln in unmatched:
        print(f"  not matched by the /reel/ pattern (manual check needed): {ln}")
    if failed:
        print(f"FAILED: {failed} item(s) could not be captured (see above).", file=sys.stderr)
    return 1 if failed else 0


def _cmd_instagram_needs_link(args: argparse.Namespace) -> int:
    return run_instagram_needs_link(
        Path(args.inbox),
        Path(args.sources),
        capture_fn=capture_instagram_reel,
        limit=args.limit,
        delay_s=args.delay,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m catalog_capture")
    subparsers = parser.add_subparsers(dest="command", required=True)

    capture_parser = subparsers.add_parser("capture", help="Capture one URL and print/write its record")
    capture_parser.add_argument("url")
    capture_parser.add_argument("--out", default=None, help="Write the capture markdown here instead of stdout")

    needs_link_parser = subparsers.add_parser(
        "needs-link", help="Resolve every ⚠ needs-link Reddit /s/ line in an inbox file"
    )
    needs_link_parser.add_argument("--inbox", required=True, help="Path to the inbox.md to rewrite in place")
    needs_link_parser.add_argument("--sources", required=True, help="catalog/sources/ directory to write into")
    needs_link_parser.add_argument("--limit", type=int, default=None, help="Process at most N items")
    needs_link_parser.add_argument(
        "--delay", type=float, default=DEFAULT_DELAY_S, help="Seconds between loads (sequential, not before the first)"
    )

    ig_capture_parser = subparsers.add_parser(
        "instagram-capture", help="Capture one Instagram reel URL and print/write its inbox block(s)"
    )
    ig_capture_parser.add_argument("url")
    ig_capture_parser.add_argument("--out", default=None, help="Write the inbox block(s) here instead of stdout")
    ig_capture_parser.add_argument(
        "--sources", default=None, help="catalog/sources/ directory to also write the full source record into"
    )

    ig_needs_link_parser = subparsers.add_parser(
        "instagram-needs-link", help="Resolve every ⚠ needs-link Instagram /reel/ line in an inbox file"
    )
    ig_needs_link_parser.add_argument("--inbox", required=True, help="Path to the inbox.md to rewrite in place")
    ig_needs_link_parser.add_argument("--sources", required=True, help="catalog/sources/ directory to write into")
    ig_needs_link_parser.add_argument("--limit", type=int, default=None, help="Process at most N items")
    ig_needs_link_parser.add_argument(
        "--delay", type=float, default=INSTAGRAM_DEFAULT_DELAY_S,
        help="Seconds between captures (sequential, not before the first)",
    )

    args = parser.parse_args(argv)

    if args.command == "capture":
        return _cmd_capture(args)
    if args.command == "instagram-capture":
        return _cmd_instagram_capture(args)
    if args.command == "instagram-needs-link":
        return _cmd_instagram_needs_link(args)
    if args.command == "needs-link":
        return _cmd_needs_link(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
