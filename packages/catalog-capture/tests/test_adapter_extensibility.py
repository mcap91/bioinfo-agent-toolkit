"""WK-0094 Phase B's extensibility claim, tested: a brand-new source type is
one new adapter registered through the public `registry.register()` API,
with zero edits to `registry.py`, `cli.py`, `rendering.py`, or
`sources_writer.py`. This file only *uses* those modules; it never patches
their source.

WK-0094 Phase B review fix-up: `registry.py`'s engine/CLI/review call sites
now call every optional adapter hook directly (`adapter.cleanup(raw)`,
`adapter.broad_re`, ...) instead of `getattr(adapter, name, default)` — the
declared contract lives on `registry.BaseAdapter`. A bare `SourceAdapter`
Protocol implementation that skips `BaseAdapter` no longer satisfies those
call sites (it has no `cleanup`/`broad_re`/etc. to call), so `FakeAdapter`
below subclasses `BaseAdapter` like a real adapter would. It still defines
only the six *required* members itself (`name`, `platform_dir`, `delay_s`,
`line_re`, `capture`, `build_outcome`) and relies on `BaseAdapter`'s
defaults for every optional hook — proving the minimal-adapter path still
routes correctly."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from catalog_capture import registry
from catalog_capture.cli import main, run_needs_link

FAKE_LINE_RE = re.compile(r"^⚠ needs-link (https?://example\.test/item/[^\s?#]+)$", re.MULTILINE)


@dataclass
class _FakeRaw:
    item_id: str
    url: str


class FakeAdapter(registry.BaseAdapter):
    """A throwaway third source type — not Reddit, not Instagram — built
    only to prove the registry routes to *anything* that satisfies the
    `SourceAdapter` shape. Defines only the required members; every
    optional hook (cleanup, describe_ok, broad_re, ...) comes straight from
    `BaseAdapter`'s defaults, unmodified."""

    name = "fake_test_adapter"
    platform_dir = "fake_test"
    delay_s = 0.0
    line_re = FAKE_LINE_RE

    def capture(self, url: str) -> _FakeRaw:
        item_id = url.rsplit("/", 1)[-1]
        return _FakeRaw(item_id=item_id, url=url)

    def build_outcome(self, raw: _FakeRaw, *, captured_at: str) -> registry.CaptureOutcome:
        return registry.CaptureOutcome(
            id=raw.item_id,
            source=raw.url,
            block_sections=[f"fake captured body for {raw.item_id}"],
            source_header_lines=[f"source: {raw.url}", f"captured: {captured_at}"],
            source_body=f"fake body for {raw.item_id}\n",
        )


def test_fake_adapter_is_routed_to_when_passed_explicitly(tmp_path: Path):
    fake = FakeAdapter()
    inbox_path = tmp_path / "inbox.md"
    inbox_path.write_text("⚠ needs-link https://example.test/item/abc123\n", encoding="utf-8")
    sources_dir = tmp_path / "sources"

    code = run_needs_link(inbox_path, sources_dir, adapters=[fake], delay_s=0)

    assert code == 0
    out = inbox_path.read_text(encoding="utf-8")
    assert "fake captured body for abc123" in out
    assert "source: https://example.test/item/abc123" in out
    source_md = sources_dir / "fake_test" / "abc123.md"
    assert source_md.exists()
    source_text = source_md.read_text(encoding="utf-8")
    assert source_text.startswith("source: https://example.test/item/abc123\ncaptured: ")
    assert source_text.endswith("\n\nfake body for abc123\n")


def test_registering_a_fake_adapter_makes_the_needs_link_default_route_to_it(tmp_path: Path, clean_registry):
    """No `adapters=` override at all — this is exactly what the CLI's
    `needs-link` command does by default (`registry.registered_adapters()`),
    proving registration alone (no shared-code edit) is enough."""
    import catalog_capture.adapters  # noqa: F401 - registers the real Reddit/reel adapters too

    fake = FakeAdapter()
    registry.register(fake)

    inbox_path = tmp_path / "inbox.md"
    inbox_path.write_text(
        "⚠ needs-link https://example.test/item/zzz999\n",
        encoding="utf-8",
    )
    sources_dir = tmp_path / "sources"

    code = run_needs_link(inbox_path, sources_dir, delay_s=0)  # adapters=None -> registry.registered_adapters()

    assert code == 0
    assert "fake captured body for zzz999" in inbox_path.read_text(encoding="utf-8")
    assert (sources_dir / "fake_test" / "zzz999.md").exists()


def test_only_flag_routes_to_one_named_adapter(tmp_path: Path, clean_registry):
    """`--only <adapter-name>` (WK-0094 Required bullet) restricts a run to
    one registered adapter, leaving every other adapter's lines untouched —
    exercised here through the real `main()` argv parser with two
    *fake*, network-free adapters standing in for Reddit/Instagram so the
    test stays fast and offline."""
    one_re = re.compile(r"^⚠ needs-link (https?://one\.test/[^\s?#]+)$", re.MULTILINE)
    two_re = re.compile(r"^⚠ needs-link (https?://two\.test/[^\s?#]+)$", re.MULTILINE)

    class _OneAdapter(FakeAdapter):
        name = "one"
        platform_dir = "one"
        line_re = one_re

    class _TwoAdapter(FakeAdapter):
        name = "two"
        platform_dir = "two"
        line_re = two_re

    registry.register(_OneAdapter())
    registry.register(_TwoAdapter())

    inbox_path = tmp_path / "inbox.md"
    inbox_path.write_text(
        "⚠ needs-link https://one.test/item/aaa\n⚠ needs-link https://two.test/item/bbb\n",
        encoding="utf-8",
    )
    sources_dir = tmp_path / "sources"

    code = main([
        "needs-link",
        "--inbox", str(inbox_path),
        "--sources", str(sources_dir),
        "--only", "one",
        "--delay", "0",
    ])

    assert code == 0
    out_text = inbox_path.read_text(encoding="utf-8")
    assert "fake captured body for aaa" in out_text  # the "one" line was captured
    assert "⚠ needs-link https://two.test/item/bbb" in out_text  # the "two" line is untouched
    assert (sources_dir / "one" / "aaa.md").exists()
    assert not (sources_dir / "two").exists()


def test_only_flag_with_unknown_adapter_name_fails_without_writing(tmp_path: Path, clean_registry, capsys):
    inbox_path = tmp_path / "inbox.md"
    inbox_path.write_text("⚠ needs-link https://one.test/item/aaa\n", encoding="utf-8")
    sources_dir = tmp_path / "sources"

    code = main([
        "needs-link",
        "--inbox", str(inbox_path),
        "--sources", str(sources_dir),
        "--only", "no-such-adapter",
    ])

    assert code == 1
    assert inbox_path.read_text(encoding="utf-8") == "⚠ needs-link https://one.test/item/aaa\n"
    err = capsys.readouterr().err
    assert "no-such-adapter" in err
