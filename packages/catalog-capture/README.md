# catalog-capture

WK-0080 Reddit slice: resolves `⚠ needs-link https://www.reddit.com/r/<sub>/s/<id>` lines in
`catalog/inbox.md` into catalog-ready text, with no manual copy-paste.

Engine: headless Playwright Chromium with a Chrome user agent (clears Reddit's JS challenge),
one capture module with a per-site wait table (`reddit.com` → poll for `shreddit-post`, soft —
on timeout it keeps the page text anyway). This is the WK-0054 ENGINE CHOICE ("own script"),
copied from `toolkit-workbench/web-capture/own/capture.py`. See `wiki/issues/WK-0054.md` and
`wiki/issues/WK-0080.md` ("Spec check — Reddit slice") for the evidence and rulings this
package follows.

uv only — never base Python.

## Setup

```
cd packages/catalog-capture
uv sync --extra dev
```

Chromium must already be available to Playwright (shared download cache, or
`uv run playwright install chromium` if not).

## Usage

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

**Concurrent edits.** A full run can take several minutes (one page load per item, with a
delay between them). The inbox is read once at the start and written once at the end via a
tmp file + atomic rename; if the file's mtime or size changed on disk in between (someone
edited it mid-run), the run aborts without writing and reports which items it had already
captured — their `catalog/sources/reddit/*.md` files are not lost, but the inbox lines for
them are not updated, so run it again after resolving the conflict.

## Tests

```
uv run pytest -v
```

The golden fixture (`tests/fixtures/JNjEe87YeN.txt`) is a real, unedited WK-0054 own-engine
capture — not hand-written. The fence-break edge case is derived by mutating it.
