# catalog-capture

Resolves `⚠ needs-link` lines in `catalog/inbox.md` into catalog-ready text, with no manual
copy-paste: Reddit `/s/` share links (WK-0080 Reddit slice) and Instagram reels (WK-0080
Instagram slice).

uv only — never base Python.

## Setup

```
cd packages/catalog-capture
uv sync --extra dev
```

Chromium must already be available to Playwright (shared download cache, or
`uv run playwright install chromium` if not) for the Reddit path.

## Reddit

Engine: headless Playwright Chromium with a Chrome user agent (clears Reddit's JS challenge),
one capture module with a per-site wait table (`reddit.com` → poll for `shreddit-post`, soft —
on timeout it keeps the page text anyway). This is the WK-0054 ENGINE CHOICE ("own script"),
copied from `toolkit-workbench/web-capture/own/capture.py`. See `wiki/issues/WK-0054.md` and
`wiki/issues/WK-0080.md` ("Spec check — Reddit slice") for the evidence and rulings this
package follows.

Capture one URL and print its record:

```
uv run python -m catalog_capture capture <url>
uv run python -m catalog_capture capture <url> --out catalog/sources/reddit/<post-id>.md
```

Resolve every Reddit needs-link line in an inbox file in place:

```
uv run python -m catalog_capture needs-link --inbox catalog/inbox.md --sources catalog/sources
```

Options:
- `--limit N` — process at most N items (useful for a dry run on one link).
- `--delay SECONDS` — seconds between loads, sequential, not applied before the first
  (default 3s; avoids tripping Reddit's rate limits by hitting it concurrently).

Each matched line is replaced in place with a fenced block (`inbox.ts`'s existing
`source:`-prefixed `\`\`\`text` format) and a `catalog/sources/reddit/<post-id>.md` file is
written with the canonical URL, capture date, tool versions, and full page text. A capture
failure (including a stalled JS challenge, a blank page, or a block/login redirect with no
resolvable post id) becomes `⚠ capture-failed <url> — <error>`; a PDF download event becomes
`⚠ pdf <url>` — neither is silently dropped, and both stay blocked on redrain. Everything else
in the inbox is left byte-identical. Exits non-zero (after printing a summary) if any item
failed.

**Retrying a `capture-failed` or `pdf` line.** `needs-link` only matches
`⚠ needs-link <reddit /s/ url>` lines. To retry, manually edit the line back to
`⚠ needs-link <url>` (drop the `capture-failed`/`pdf` reason and any trailing error text) before
running `needs-link` again — there is no automatic retry.

## Instagram

Pipeline (WK-0079's recommended default stack, I4): yt-dlp `-j` anonymous caption probe →
yt-dlp bestaudio download → ffmpeg (imageio-ffmpeg, never a system ffmpeg) decode to 16 kHz mono
→ faster-whisper `small` CPU int8, VAD off → yt-dlp bestvideo download → ffmpeg keyframes
(`select='eq(n\,0)+gt(scene\,0.3)'`) + a PIL contact sheet → one Claude read (stream-json, no
tools, caption + transcript + sheet image) naming every tool/repo the reel shows plus any
on-screen text. Per OR-3 (operator ruling, 2026-10-26): the capture never verifies a URL or
decides what the reel is "about" — it hands the processing agent everything the read spotted,
labeled as unverified hints, and the agent decides what goes into the catalog. See
`wiki/issues/WK-0080.md` ("OR-3 Operator ruling: capture captures, the processing agent
decides") for the evidence and rulings.

Capture one reel URL and print its inbox block(s):

```
uv run python -m catalog_capture instagram-capture <url>
uv run python -m catalog_capture instagram-capture <url> --sources catalog/sources
```

Resolve every Instagram `/reel/` needs-link line in an inbox file in place:

```
uv run python -m catalog_capture instagram-needs-link --inbox catalog/inbox.md --sources catalog/sources
```

Options: same `--limit`/`--delay` as `needs-link` (default delay 3s between reels).

Each matched line becomes exactly **one** fenced block per reel (OR-3) — its `source:` is always
the reel URL itself. The body carries the caption, transcript, on-screen text, key claims, and a
"Mentioned (unverified hints)" list of every tool/URL the read spotted — never HTTP-checked or
GitHub-normalized at capture time; deciding what each hint becomes (a new entry, an
`annotate-entry` call, or nothing) is the processing agent's job, not this package's. Every
record also gets a full `catalog/sources/instagram/<reel-id>.md` (reel URL, capture date, tool
versions, caption, transcript, on-screen text, key claims, the same unverified hints) plus raw
artifacts beside it (`info.json`, `transcript.txt`, `sheet.jpg`, `read_response.jsonl` — no
audio/video). A pipeline failure at any stage becomes `⚠ capture-failed <url> — <stage>:
<error>` — never a silent drop. Instagram carousels (`/p/`) are out of scope for this slice (a
separate WK-0080 checklist item) and are left untouched.

## Concurrent edits (both platforms)

A full run can take several minutes (one capture per item, with a delay between them). The
inbox is read once at the start and written once at the end via a tmp file + atomic rename; if
the file's mtime or size changed on disk in between (someone edited it mid-run), the run
aborts without writing and reports which items it had already captured — their source files are
not lost, but the inbox lines for them are not updated, so run it again after resolving the
conflict.

## Tests

```
uv run pytest -v
```

The Reddit golden fixture (`tests/fixtures/JNjEe87YeN.txt`) is a real, unedited WK-0054
own-engine capture — not hand-written. The fence-break edge case is derived by mutating it.

The Instagram golden fixtures (`tests/fixtures/instagram/`) are the real golden reel
(`De5smNojeZm`) artifacts copied byte-for-byte from `toolkit-workbench/reel/outputs/De5smNojeZm/`
(`probe_ytdlp.json`, `transcript_small_cpu_int8.txt`, `sheet_t0.3.jpg`), plus this slice's own
real Claude read response (`read_response.jsonl`) captured against that exact sheet/transcript/
caption with this slice's own prompt (I3's new `tools`/`on_screen_text` shape).
