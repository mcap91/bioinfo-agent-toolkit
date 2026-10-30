"""CLI entry point: `python -m catalog_capture capture|needs-link|review ...`

WK-0094 Phase B: one `needs-link` command (replacing the old `needs-link` +
`instagram-needs-link` pair), one `capture` command that works for any
registered adapter, and a `review build`/`review tally` pair.
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import adapters as _adapters  # noqa: F401 - registers the default adapters on import
from . import pricing, registry, review as review_mod
from .rendering import render_block
from .sources_writer import render_source_md, write_source_file


def _resolve_adapters(only: str | None) -> list[registry.SourceAdapter] | None:
    """Returns None (error already printed) or the adapter list to use."""
    all_adapters = registry.registered_adapters()
    if only is None:
        return all_adapters
    adapter = registry.get_adapter(only)
    if adapter is None:
        names = [a.name for a in all_adapters]
        print(f"unknown adapter {only!r} — registered adapters: {names}", file=sys.stderr)
        return None
    return [adapter]


def _cmd_capture(args: argparse.Namespace) -> int:
    adapters = registry.registered_adapters()
    adapter = None
    url_for_match = f"⚠ needs-link {args.url}"
    if args.adapter:
        adapter = registry.get_adapter(args.adapter)
        if adapter is None:
            print(f"unknown adapter {args.adapter!r} — registered adapters: {[a.name for a in adapters]}", file=sys.stderr)
            return 1
    else:
        for cand in adapters:
            if cand.line_re.match(url_for_match):
                adapter = cand
                break
        if adapter is None:
            print(f"no registered adapter matches {args.url!r} — pass --adapter NAME", file=sys.stderr)
            return 1

    try:
        raw = adapter.capture(args.url)
    except (registry.CaptureFailedError, registry.NeedsLinkSoftMarker) as e:
        print(f"capture failed: {e}", file=sys.stderr)
        return 1

    try:
        captured_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        outcome = adapter.build_outcome(raw, captured_at=captured_at)
        out_text = render_block(source=outcome.source, sections=outcome.block_sections) + "\n"
        if args.sources:
            md = render_source_md(header_lines=outcome.source_header_lines, body=outcome.source_body)
            write_source_file(Path(args.sources), adapter.platform_dir, outcome.id, md, artifacts=outcome.artifacts)
            print(f"wrote {args.sources}/{adapter.platform_dir}/{outcome.id}.md")
    finally:
        adapter.cleanup(raw)

    if args.out:
        Path(args.out).write_text(out_text, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        sys.stdout.write(out_text)
    return 0


def run_needs_link(
    inbox_path: Path,
    sources_dir: Path,
    *,
    adapters: list[registry.SourceAdapter] | None = None,
    limit: int | None = None,
    delay_s: float | None = None,
) -> int:
    """Read, process, and write back `inbox_path`. A multi-minute run reads
    the file once and writes once (S2): write to a tmp file then
    `os.replace` (atomic on POSIX), and before writing, compare mtime+size
    against the values at read time. If the file changed underneath us
    (someone edited it mid-run), abort without writing — the
    already-captured source files still exist on disk, and we print which
    URLs they belong to so nothing is silently lost."""
    adapters = adapters if adapters is not None else registry.registered_adapters()
    text = inbox_path.read_text(encoding="utf-8")
    stat_before = inbox_path.stat()

    unmatched = registry.unmatched_needs_link_lines(text, adapters)

    out_text, results = registry.process_needs_link(
        text, sources_dir=sources_dir, adapters=adapters, limit=limit, delay_s=delay_s
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
            print(f"  captured, not written to inbox: {r.url} -> {r.id}", file=sys.stderr)
        return 1

    tmp_path = inbox_path.with_name(inbox_path.name + ".tmp")
    tmp_path.write_text(out_text, encoding="utf-8")
    os.replace(tmp_path, inbox_path)

    ok = sum(1 for r in results if r.status == "ok")
    failed = sum(1 for r in results if r.status == "failed")
    # Each participating adapter may declare extra status buckets it can
    # produce (e.g. the Reddit adapter's "pdf" soft marker) — shown even at
    # zero, same as the pre-refactor Reddit-only summary line always showed
    # "0 pdf". An adapter that declares none (the reel adapter) adds nothing.
    status_counts: dict[str, int] = {}
    for r in results:
        if r.status not in ("ok", "failed"):
            status_counts[r.status] = status_counts.get(r.status, 0) + 1
    extra_buckets = sorted({b for a in adapters for b in a.status_buckets})
    extra = "".join(f", {status_counts.get(b, 0)} {b}" for b in extra_buckets)
    print(f"needs-link: {len(results)} processed — {ok} captured{extra}, {failed} failed")
    for r in results:
        if r.status == "failed":
            print(f"  capture-failed: {r.url} — {r.error}")
        elif r.status == "ok":
            adapter = registry.get_adapter(r.adapter) if r.adapter else None
            text = adapter.describe_ok(r) if adapter is not None else None
            if text:
                print(f"  {text}")
        else:
            print(f"  {r.status}: {r.url}")
    for adapter, line in unmatched:
        print(f"  not matched by the {adapter.broad_hint} (manual check needed): {line}")
    if failed:
        print(f"FAILED: {failed} item(s) could not be captured (see above).", file=sys.stderr)
    return 1 if failed else 0


def _cmd_needs_link(args: argparse.Namespace) -> int:
    if args.prices_path:
        os.environ[pricing.ENV_VAR] = args.prices_path
    adapters = _resolve_adapters(args.only)
    if adapters is None:
        return 1
    return run_needs_link(
        Path(args.inbox),
        Path(args.sources),
        adapters=adapters,
        limit=args.limit,
        delay_s=args.delay,
    )


def _cmd_review_build(args: argparse.Namespace) -> int:
    adapters = _resolve_adapters(args.only)
    if adapters is None:
        return 1
    adapters_by_name = {a.name: a for a in adapters}
    items: list[review_mod.ReviewItem] = []
    for adapter in adapters:
        items.extend(adapter.review_items(Path(args.sources)))
    out_dir = Path(args.out)
    index_path = review_mod.build_review(items, out_dir, adapters=adapters_by_name, cap=args.sample_cap)
    print(f"wrote {len(items)} sheet(s) + {index_path}")
    return 0


def _cmd_review_tally(args: argparse.Namespace) -> int:
    result = review_mod.tally(Path(args.out))
    counts = result["counts"]
    checked = result["n"] - counts.get("unchecked", 0)
    print(f"n = {result['n']} sheets, {checked} checked, {counts.get('unchecked', 0)} unchecked")
    for key in ("yes", "good enough", "wrong", "no", "missed"):
        print(f"  {key}: {counts.get(key, 0)}")
    if result["unrecognized"]:
        print("FAIL-LOUD: unrecognized verdict values (not yes/good enough/wrong/no/missed <x>):", file=sys.stderr)
        for name, value in result["unrecognized"]:
            print(f"  {name}: {value!r}", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m catalog_capture")
    subparsers = parser.add_subparsers(dest="command", required=True)

    capture_parser = subparsers.add_parser("capture", help="Capture one URL and print/write its record")
    capture_parser.add_argument("url")
    capture_parser.add_argument("--out", default=None, help="Write the inbox block here instead of stdout")
    capture_parser.add_argument(
        "--sources", default=None, help="catalog/sources/ directory to also write the full source record into"
    )
    capture_parser.add_argument(
        "--adapter", default=None, help="Registered adapter name to use (default: auto-detect from the URL)"
    )

    needs_link_parser = subparsers.add_parser(
        "needs-link", help="Resolve every ⚠ needs-link line any registered adapter owns, in an inbox file"
    )
    needs_link_parser.add_argument("--inbox", required=True, help="Path to the inbox.md to rewrite in place")
    needs_link_parser.add_argument("--sources", required=True, help="catalog/sources/ directory to write into")
    needs_link_parser.add_argument("--limit", type=int, default=None, help="Process at most N items")
    needs_link_parser.add_argument(
        "--delay", type=float, default=None,
        help="Seconds between captures, sequential, not applied before the first item overall "
        "(default: each matched adapter's own delay)",
    )
    needs_link_parser.add_argument(
        "--only", default=None, help="Only process lines the named adapter owns (e.g. 'reddit', 'instagram_reel')"
    )
    needs_link_parser.add_argument(
        "--prices-path", default=None,
        help=f"LiteLLM price table path (default: {pricing.DEFAULT_LITELLM_PRICES_PATH}, "
        f"or the {pricing.ENV_VAR} env var)",
    )

    review_parser = subparsers.add_parser("review", help="Build or tally operator review sheets")
    review_sub = review_parser.add_subparsers(dest="review_command", required=True)

    review_build_parser = review_sub.add_parser(
        "build", help="Render one review sheet per captured item plus REVIEW.md"
    )
    review_build_parser.add_argument("--sources", required=True, help="catalog/sources/ directory to read from")
    review_build_parser.add_argument("--out", required=True, help="Directory to write sheets + REVIEW.md into")
    review_build_parser.add_argument("--only", default=None, help="Only build sheets for the named adapter")
    review_build_parser.add_argument(
        "--sample-cap", type=int, default=review_mod.SAMPLE_CAP, help="Cap on the suggested spot-check sample (OR-5)"
    )

    review_tally_parser = review_sub.add_parser("tally", help="Count operator verdicts in already-built sheets")
    review_tally_parser.add_argument("--out", required=True, help="Directory containing the review sheets")

    args = parser.parse_args(argv)

    if args.command == "capture":
        return _cmd_capture(args)
    if args.command == "needs-link":
        return _cmd_needs_link(args)
    if args.command == "review":
        if args.review_command == "build":
            return _cmd_review_build(args)
        if args.review_command == "tally":
            return _cmd_review_tally(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
