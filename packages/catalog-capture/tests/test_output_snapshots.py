"""Byte-exact output snapshots (WK-0094 Phase B): "snapshot the rendered
blocks, sources files and inbox rewrite for the existing Reddit and reel
golden fixtures ... After [the adapter-layer refactor], the outputs are
byte-identical." These tests pin today's exact bytes so that refactor can
prove — not just claim — it changed nothing observable.

Public entry points this file depends on by name (the refactor WILL rename
or move these; it must update the call sites *in this file*, but must never
touch the recorded files under tests/fixtures/snapshots/ — if a snapshot
file needs to change, behavior changed, and that's a Phase B regression):

  catalog_capture.rewrite            .process_needs_link, .NEEDS_LINK_RE
  catalog_capture.sources            .render_source_md, .write_source_file
  catalog_capture.instagram_rewrite  .process_instagram_needs_link,
                                      .render_instagram_block
  catalog_capture.instagram_sources  .render_instagram_source_md,
                                      .write_instagram_source_files
  catalog_capture.capture            .CaptureResult, .CaptureFailedError
  catalog_capture.instagram_capture  .InstagramCaptureResult,
                                      .InstagramCaptureError
  catalog_capture.canonical          .canonical_url
  catalog_capture.fence              .defuse_fence_breaks
  catalog_capture.instagram_read     .parse_claude_stream_result
  catalog_capture.cli                .run_needs_link, .run_instagram_needs_link

Also depended on (module-level attribute, monkeypatched below, not called
directly): `rewrite.datetime` and `instagram_rewrite.datetime` — both
modules do `from datetime import datetime` as a plain module global, so
`monkeypatch.setattr(<module>, "datetime", ...)` pins `captured_at` without
touching src/.

Regeneration: run `UPDATE_SNAPSHOTS=1 uv run pytest -q test_output_snapshots.py`
to (re)write every snapshot file from the current code. Run it again without
the env var afterwards and confirm the suite passes — that second run is the
proof the snapshots are deterministic, not hand-typed. Never hand-edit a
file under tests/fixtures/snapshots/.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime as _real_datetime
from datetime import timezone as _real_timezone
from pathlib import Path

import pytest

import catalog_capture.instagram_rewrite as instagram_rewrite_mod
import catalog_capture.rewrite as rewrite_mod
from catalog_capture.canonical import canonical_url
from catalog_capture.capture import CaptureFailedError, CaptureResult
from catalog_capture.cli import run_instagram_needs_link, run_needs_link
from catalog_capture.fence import defuse_fence_breaks
from catalog_capture.instagram_capture import InstagramCaptureError, InstagramCaptureResult
from catalog_capture.instagram_read import parse_claude_stream_result
from catalog_capture.instagram_rewrite import process_instagram_needs_link, render_instagram_block
from catalog_capture.instagram_sources import render_instagram_source_md, write_instagram_source_files
from catalog_capture.rewrite import process_needs_link
from catalog_capture.sources import render_source_md, write_source_file

# --------------------------------------------------------------------------
# Snapshot I/O: compare-or-update against tests/fixtures/snapshots/.
# --------------------------------------------------------------------------

SNAPSHOT_DIR = Path(__file__).parent / "fixtures" / "snapshots"
UPDATE_SNAPSHOTS = os.environ.get("UPDATE_SNAPSHOTS") == "1"


def _snapshot(relpath: str, actual: str | bytes) -> None:
    """Compare `actual` byte-for-byte against `fixtures/snapshots/<relpath>`.
    With `UPDATE_SNAPSHOTS=1` set, (re)writes the file from `actual` instead
    of comparing — the only sanctioned way to create or refresh a snapshot,
    so every recorded file is a product of running the current code, never
    hand-typed."""
    path = SNAPSHOT_DIR / relpath
    actual_bytes = actual.encode("utf-8") if isinstance(actual, str) else bytes(actual)
    if UPDATE_SNAPSHOTS:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(actual_bytes)
        return
    if not path.exists():
        pytest.fail(
            f"missing snapshot fixtures/snapshots/{relpath} — regenerate with "
            f"`UPDATE_SNAPSHOTS=1 uv run pytest -q test_output_snapshots.py`"
        )
    expected_bytes = path.read_bytes()
    assert actual_bytes == expected_bytes, f"snapshot mismatch: fixtures/snapshots/{relpath}"


def _hash_snapshot(relpath: str, data: bytes) -> None:
    """Same contract as `_snapshot`, but for a large binary artifact (the
    ~220KB contact-sheet jpeg) — compare a recorded sha256 instead of
    duplicating the already-committed fixture bytes a second time."""
    _snapshot(relpath, hashlib.sha256(data).hexdigest() + "\n")


# --------------------------------------------------------------------------
# Fixed clock: pin `captured_at` (rewrite.py / instagram_rewrite.py both
# stamp `datetime.now(timezone.utc)` into the record) without touching src/.
# --------------------------------------------------------------------------

_FIXED_NOW = _real_datetime(2026, 10, 29, 12, 0, 0, tzinfo=_real_timezone.utc)


class _FixedDatetime:
    @classmethod
    def now(cls, tz=None):  # noqa: ARG003 - match datetime.now's signature
        return _FIXED_NOW


@pytest.fixture
def fixed_capture_clock(monkeypatch):
    """Pin `datetime.now()` inside rewrite.py and instagram_rewrite.py to a
    fixed instant, so the `captured:`/`captured_at` stamp these modules write
    never drifts with wall-clock time — required for a byte-exact snapshot."""
    monkeypatch.setattr(rewrite_mod, "datetime", _FixedDatetime)
    monkeypatch.setattr(instagram_rewrite_mod, "datetime", _FixedDatetime)
    return _FIXED_NOW.strftime("%Y-%m-%d")


FIXED_DATE = _FIXED_NOW.strftime("%Y-%m-%d")

# --------------------------------------------------------------------------
# Reddit fixtures: the real WK-0054 golden capture (via conftest.golden_capture),
# a fixed final_url/post id, and fixed tool versions (not read off the live
# environment — pinned literals, same as test_inbox_rewrite.py's fakes).
# --------------------------------------------------------------------------

REDDIT_SHARE_URL = "https://www.reddit.com/r/LocalLLaMA/s/JNjEe87YeN"
REDDIT_FINAL_URL = (
    "https://www.reddit.com/r/LocalLLaMA/comments/1x9gfnb/"
    "google_open_sources_harness2_for_self_improving/?solution=abc123"
)
REDDIT_POST_ID = "1x9gfnb"
PLAYWRIGHT_VERSION = "1.64.1"
CHROMIUM_VERSION = "156.0.8078.4"


def _reddit_fake_capture(body_text: str):
    def _capture(url: str) -> CaptureResult:
        return CaptureResult(
            final_url=REDDIT_FINAL_URL,
            title="Google Open Sources Harness2 for Self Improving AI Agents",
            body_text=body_text,
            playwright_version=PLAYWRIGHT_VERSION,
            chromium_version=CHROMIUM_VERSION,
        )

    return _capture


def test_reddit_inbox_block_snapshot(golden_capture, fixed_capture_clock, tmp_path):
    """Phase B pins behavior unchanged: the exact byte shape (````text`
    fence, `source:` line, verbatim body) one successful Reddit needs-link
    capture rewrites its inbox line to, built from the real WK-0054 golden
    capture text. If the adapter-layer refactor changes a single byte of
    this shape, this test must fail before anything else notices."""
    _, body_text = golden_capture
    out_text, results = process_needs_link(
        f"⚠ needs-link {REDDIT_SHARE_URL}\n",
        sources_dir=tmp_path / "sources",
        capture_fn=_reddit_fake_capture(body_text),
        delay_s=0,
    )
    assert results[0].status == "ok"
    _snapshot("reddit_inbox_block.txt", out_text)


def test_reddit_source_file_snapshot(golden_capture, tmp_path):
    """Phase B pins behavior unchanged: catalog/sources/reddit/<post-id>.md
    (render_source_md + write_source_file), byte-for-byte, against the real
    golden capture text — independent of the rewrite loop above, since the
    refactor's "one sources writer" must still produce this exact file."""
    _, body_text = golden_capture
    canonical = canonical_url(REDDIT_FINAL_URL)
    safe_text = defuse_fence_breaks(body_text)
    md = render_source_md(
        canonical=canonical,
        captured_at=FIXED_DATE,
        playwright_version=PLAYWRIGHT_VERSION,
        chromium_version=CHROMIUM_VERSION,
        text=safe_text,
    )
    out_path = write_source_file(tmp_path, REDDIT_POST_ID, md)
    assert out_path == tmp_path / "reddit" / f"{REDDIT_POST_ID}.md"
    _snapshot("reddit_source_md.md", out_path.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------
# Instagram fixtures: a real, non-degenerate InstagramCaptureResult built
# entirely from the committed golden-reel fixtures (I8) plus this slice's
# own real OR-1 read response — nothing hand-invented, same evidence
# discipline as test_instagram_golden_fixture.py.
# --------------------------------------------------------------------------


@pytest.fixture
def golden_instagram_capture_result(golden_instagram_artifacts) -> InstagramCaptureResult:
    """`sheet_is_temp=False` so `cleanup_sheet()` never deletes the committed
    fixture jpeg (same default the existing fake-capture tests rely on)."""
    info = json.loads(golden_instagram_artifacts["info_json_text"])
    parsed = parse_claude_stream_result(golden_instagram_artifacts["read_response_text"])
    m = re.search(r"\{.*\}", parsed["result_text"], re.DOTALL)
    obj = json.loads(m.group(0))
    return InstagramCaptureResult(
        reel_id="De5smNojeZm",
        reel_url="https://www.instagram.com/reel/De5smNojeZm/",
        info_json_text=golden_instagram_artifacts["info_json_text"],
        caption=info["description"],
        transcript_text=golden_instagram_artifacts["transcript_text"],
        sheet_path=golden_instagram_artifacts["sheet_path"],
        on_screen_text=obj["on_screen_text"],
        key_claims=[str(c) for c in obj["key_claims"]],
        info_channel=obj["info_channel"],
        tools=[{"name": t.get("name"), "url": t.get("url")} for t in obj["tools"]],
        read_raw_stdout=golden_instagram_artifacts["read_response_text"],
        versions={
            # Fixed literals, not read off the live environment — same
            # choice test_instagram_rewrite.py's `_fake_result` makes, so a
            # uv.lock bump never perturbs this snapshot.
            "yt-dlp": "2026.10.26",
            "ffmpeg": "7.0.2-static",
            "faster-whisper": "1.2.1",
            "ctranslate2": "4.7.0",
            "claude": "2.1.0 (Claude Code)",
        },
        sheet_is_temp=False,
    )


def test_instagram_inbox_block_snapshot(golden_instagram_capture_result):
    """Phase B pins behavior unchanged: the exact OR-3 one-block-per-reel
    shape (caption, transcript, on-screen text, key claims, tool hints)
    rendered for the real golden reel, byte-for-byte. `render_instagram_block`
    returns the block with no trailing newline — that's a separate snapshot
    from the rewrite-loop one below, which keeps the original line's
    trailing `\\n` after substitution."""
    cap = golden_instagram_capture_result
    block = render_instagram_block(
        reel_url=cap.reel_url,
        caption=cap.caption,
        transcript_text=cap.transcript_text,
        on_screen_text=cap.on_screen_text,
        key_claims=cap.key_claims,
        tools=cap.tools,
    )
    _snapshot("instagram_inbox_block_rendered.txt", block)


def test_instagram_needs_link_rewrite_produces_the_same_block(golden_instagram_capture_result, tmp_path):
    """Same contract as the renderer test above, but through the full
    `process_instagram_needs_link` rewrite loop instead of calling
    `render_instagram_block` directly — pins that the loop's wiring doesn't
    change the byte shape it hands back to the inbox (including the
    original line's trailing newline, which `NEEDS_LINK_RE.sub` leaves
    after the substituted span)."""
    cap = golden_instagram_capture_result

    def fake_capture(url: str) -> InstagramCaptureResult:
        return cap

    out_text, results = process_instagram_needs_link(
        f"⚠ needs-link {cap.reel_url}\n",
        sources_dir=tmp_path / "sources",
        capture_fn=fake_capture,
        delay_s=0,
    )
    assert results[0].status == "ok"
    _snapshot("instagram_inbox_block.txt", out_text)


def test_instagram_source_files_snapshot(golden_instagram_capture_result, tmp_path):
    """Phase B pins behavior unchanged: catalog/sources/instagram/<reel-id>.md
    plus its raw-artifact sibling directory (info.json, transcript.txt,
    sheet.jpg, read_response.jsonl) — the sources-writer half of the
    pipeline, independent of the rewrite loop."""
    cap = golden_instagram_capture_result
    md = render_instagram_source_md(
        reel_url=cap.reel_url,
        captured_at=FIXED_DATE,
        versions=cap.versions,
        caption=cap.caption,
        transcript_text=cap.transcript_text,
        on_screen_text=cap.on_screen_text,
        key_claims=cap.key_claims,
        info_channel=cap.info_channel,
        tools=cap.tools,
    )
    out_path = write_instagram_source_files(
        tmp_path,
        cap.reel_id,
        md,
        info_json_text=cap.info_json_text,
        transcript_text=cap.transcript_text,
        sheet_path=cap.sheet_path,
        read_response_text=cap.read_raw_stdout,
    )
    artifacts = tmp_path / "instagram" / cap.reel_id
    assert sorted(p.name for p in artifacts.iterdir()) == [
        "info.json",
        "read_response.jsonl",
        "sheet.jpg",
        "transcript.txt",
    ]
    _snapshot("instagram_source_md.md", out_path.read_text(encoding="utf-8"))
    _snapshot("instagram_source_info.json", (artifacts / "info.json").read_text(encoding="utf-8"))
    _snapshot("instagram_source_transcript.txt", (artifacts / "transcript.txt").read_text(encoding="utf-8"))
    _snapshot(
        "instagram_source_read_response.jsonl",
        (artifacts / "read_response.jsonl").read_text(encoding="utf-8"),
    )
    _hash_snapshot("instagram_source_sheet.jpg.sha256", (artifacts / "sheet.jpg").read_bytes())


# --------------------------------------------------------------------------
# Full inbox rewrite: both platforms, both outcomes (ok / capture-failed),
# plus two lines neither rewrite pass should touch — a plain github.com url
# and an Instagram `/p/` carousel line (no adapter handles `/p/` yet, WK-0094
# Phase A). Derived from the shape of tests/fixtures/inbox_2026-10-26.md
# (same header line, same `⚠ needs-link` line format, a real non-needs-link
# github.com url from that fixture) rather than the full 83-line file, so
# the forced-failure cases below are legible instead of buried.
# --------------------------------------------------------------------------

_REDDIT_FAIL_URL = "https://www.reddit.com/r/AI_Agents/s/forcedFailure1"
_INSTAGRAM_FAIL_URL = "https://www.instagram.com/reel/forcedFailure2/"
_UNTOUCHED_GITHUB_LINE = "https://github.com/karpathy/llm-council"
_UNTOUCHED_CAROUSEL_LINE = "⚠ needs-link https://www.instagram.com/p/DeCarousel/"


def _build_fixture_inbox(instagram_ok_url: str) -> str:
    return (
        "# Catalog inbox\n\n"
        f"{_UNTOUCHED_GITHUB_LINE}\n"
        f"⚠ needs-link {REDDIT_SHARE_URL} — Google Open Sources Harness2 for Self Improving AI Agents\n"
        f"⚠ needs-link {_REDDIT_FAIL_URL} — forced failure case\n"
        f"⚠ needs-link {instagram_ok_url}\n"
        f"⚠ needs-link {_INSTAGRAM_FAIL_URL}\n"
        f"{_UNTOUCHED_CAROUSEL_LINE}\n"
    )


def test_full_inbox_rewrite_snapshot_both_platforms(
    golden_capture, golden_instagram_capture_result, fixed_capture_clock, tmp_path
):
    """The Phase B acceptance line verbatim: "snapshot the rendered blocks,
    sources files and inbox rewrite for the existing Reddit and reel golden
    fixtures ... After [the refactor], the outputs are byte-identical."
    This is the inbox-rewrite half: one Reddit success, one Reddit
    capture-failed, one Instagram success, one Instagram capture-failed, a
    plain github.com url, and an Instagram `/p/` carousel line — the last
    two must come out byte-identical to how they went in, through *both*
    rewrite passes (today's two separate loops; tomorrow's one adapter
    registry)."""
    _, reddit_body = golden_capture
    ig_cap = golden_instagram_capture_result
    inbox_text = _build_fixture_inbox(ig_cap.reel_url)

    def reddit_capture(url: str) -> CaptureResult:
        if url == _REDDIT_FAIL_URL:
            raise CaptureFailedError("net::ERR_NAME_NOT_RESOLVED (forced, snapshot test)")
        return CaptureResult(
            final_url=REDDIT_FINAL_URL,
            title="t",
            body_text=reddit_body,
            playwright_version=PLAYWRIGHT_VERSION,
            chromium_version=CHROMIUM_VERSION,
        )

    def instagram_capture(url: str) -> InstagramCaptureResult:
        if url == _INSTAGRAM_FAIL_URL:
            raise InstagramCaptureError("audio", "yt-dlp bestaudio exit 1 (forced, snapshot test)")
        return ig_cap

    sources_dir = tmp_path / "sources"
    after_reddit, reddit_results = process_needs_link(
        inbox_text, sources_dir=sources_dir, capture_fn=reddit_capture, delay_s=0
    )
    after_both, instagram_results = process_instagram_needs_link(
        after_reddit, sources_dir=sources_dir, capture_fn=instagram_capture, delay_s=0
    )

    assert [r.status for r in reddit_results] == ["ok", "failed"]
    assert [r.status for r in instagram_results] == ["ok", "failed"]
    assert _UNTOUCHED_GITHUB_LINE in after_both.splitlines()
    assert _UNTOUCHED_CAROUSEL_LINE in after_both.splitlines()

    _snapshot("full_inbox_rewrite.md", after_both)


# --------------------------------------------------------------------------
# CLI-level entry points: run_needs_link / run_instagram_needs_link. These
# are the names the Phase B acceptance criteria call out directly ("one
# `needs-link` command") — snapshotting through them, not just the inner
# rewrite functions, pins the atomic-write-plus-stdout-summary contract too.
# --------------------------------------------------------------------------


def test_cli_run_needs_link_snapshot(golden_capture, fixed_capture_clock, tmp_path, capsys):
    """Phase B pins behavior unchanged at the CLI entry point named in the
    acceptance criteria: the rewritten inbox file, the written source file,
    and the stdout/stderr summary `run_needs_link` prints — one ok item, one
    capture-failed item."""
    _, body_text = golden_capture
    inbox_path = tmp_path / "inbox.md"
    inbox_path.write_text(
        f"⚠ needs-link {REDDIT_SHARE_URL} — Google Open Sources Harness2 for Self Improving AI Agents\n"
        f"⚠ needs-link {_REDDIT_FAIL_URL} — forced failure case\n",
        encoding="utf-8",
    )
    sources_dir = tmp_path / "sources"

    def reddit_capture(url: str) -> CaptureResult:
        if url == _REDDIT_FAIL_URL:
            raise CaptureFailedError("net::ERR_NAME_NOT_RESOLVED (forced, snapshot test)")
        return CaptureResult(
            final_url=REDDIT_FINAL_URL,
            title="t",
            body_text=body_text,
            playwright_version=PLAYWRIGHT_VERSION,
            chromium_version=CHROMIUM_VERSION,
        )

    code = run_needs_link(inbox_path, sources_dir, capture_fn=reddit_capture, delay_s=0)
    out, err = capsys.readouterr()

    assert code == 1  # one item failed
    assert not (tmp_path / "inbox.md.tmp").exists()
    ok_source = sources_dir / "reddit" / f"{REDDIT_POST_ID}.md"
    assert ok_source.exists()

    _snapshot("cli_reddit_needs_link_inbox.md", inbox_path.read_text(encoding="utf-8"))
    _snapshot("cli_reddit_needs_link_source.md", ok_source.read_text(encoding="utf-8"))
    _snapshot("cli_reddit_needs_link_stdout.txt", out)
    _snapshot("cli_reddit_needs_link_stderr.txt", err)


def test_cli_run_instagram_needs_link_snapshot(golden_instagram_capture_result, fixed_capture_clock, tmp_path, capsys):
    """Instagram counterpart of the test above, against `run_instagram_needs_link`
    — the command the Phase B acceptance criteria say gets removed and folded
    into the one `needs-link` command. Whatever call site replaces it must
    still produce these exact bytes for the same inputs."""
    cap = golden_instagram_capture_result
    inbox_path = tmp_path / "inbox.md"
    inbox_path.write_text(
        f"⚠ needs-link {cap.reel_url}\n⚠ needs-link {_INSTAGRAM_FAIL_URL}\n",
        encoding="utf-8",
    )
    sources_dir = tmp_path / "sources"

    def instagram_capture(url: str) -> InstagramCaptureResult:
        if url == _INSTAGRAM_FAIL_URL:
            raise InstagramCaptureError("audio", "yt-dlp bestaudio exit 1 (forced, snapshot test)")
        return cap

    code = run_instagram_needs_link(inbox_path, sources_dir, capture_fn=instagram_capture, delay_s=0)
    out, err = capsys.readouterr()

    assert code == 1  # one item failed
    assert not (tmp_path / "inbox.md.tmp").exists()
    ok_md = sources_dir / "instagram" / f"{cap.reel_id}.md"
    assert ok_md.exists()

    _snapshot("cli_instagram_needs_link_inbox.md", inbox_path.read_text(encoding="utf-8"))
    _snapshot("cli_instagram_needs_link_source.md", ok_md.read_text(encoding="utf-8"))
    _snapshot("cli_instagram_needs_link_stdout.txt", out)
    _snapshot("cli_instagram_needs_link_stderr.txt", err)
