# Golden carousel fixtures (WK-0094)

Source: the WK-0094 Phase A probe, run 2026-10-29/30 (UTC) against the 12 real Instagram `/p/`
links listed in WK-0087, captured anonymously (no login, no cookies) and recorded unedited to
`toolkit-workbench/carousel/probe/<tool>/<shortcode>/` (gitignored workbench). The operator ruled
on the probe recommendation in `wiki/issues/WK-0094.md` (OR-6, 2026-10-30): instaloader is the
Instagram-post fetcher, and these two shortcodes are the approved goldens.

Each `<shortcode>/` directory here is an unedited copy (`cp`, no re-encoding, no edits) of:

- `toolkit-workbench/carousel/probe/instaloader/<shortcode>/` — `cmd.txt`, `stdout.txt`,
  `stderr.txt`, `exit_code.txt`, and `dl/` (instaloader's own download directory: the post's
  JSON metadata, a `.txt` caption file, and one `.jpg` per carousel slide, largest
  `image_versions2.candidates` size).
- `toolkit-workbench/carousel/probe/yt-dlp/<shortcode>/` (as this fixture's `yt-dlp/` subdir) —
  `cmd.txt`, `stdout.json`, `stderr.txt`, `exit_code.txt` (yt-dlp `-J`, used only as the
  independent slide-count cross-check; it returns no slide images for Instagram posts).

Shortcodes and content (WK-0094 probe table):

- `De9SalRGOhy` — 20-slide spec-style carousel ("Build an Agent That Writes Its Own Playbook —
  ACE (Agentic Context Engineering) in 45 Minutes").
- `DeCKnW0DAGc` — 11-slide one-repo-per-slide carousel ("8 GitHub Repos Hiding in Plain Sight").

Tool versions at capture time (`toolkit-workbench/carousel/probe/versions.txt`): yt-dlp 2026.10.26
(package pin), instaloader 4.16 (scratch uv env), Playwright Chromium 156.0.8078.4.

These are real, unedited captures — not hand-written or re-encoded. Integrity was verified at
copy time with `diff -r` against the workbench originals (byte-identical). WK-0087 (carousel
adapter) is the consumer of these fixtures; this commit does not add carousel capture code.
