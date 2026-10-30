"""I7 evidence: "Check whether drain.ts urlUnfetchable must change: Instagram
must still be marked needs-link by the drain." Answer, proven against the
real `drainInbox()` (not a reimplementation): no — `urlUnfetchable` is
Reddit-only, but the real `catalog/config.json` already has an unconditional
`{"host": "instagram.com"}` entry in `blocked_domains` (no `allow_paths`), so
`hostBlocked()` blocks every instagram.com URL regardless of path. A fenced
text block (the shape this package's rewrite produces) is a different
`InboxItem.kind` that the blocking check never applies to at all. Together,
these two facts are why packages/catalog-mcp/src/core/drain.ts needed no
change for this slice."""

from __future__ import annotations

from conftest import ts_check_unfetchable_real_config

INSTAGRAM_URLS_BLOCKED = [
    "https://www.instagram.com/reel/De5smNojeZm/",  # the shape this slice resolves
    "https://instagram.com/reel/De5smNojeZm/",  # bare host
    "https://www.instagram.com/p/DeCarousel/",  # carousel path (not yet built, still must be blocked)
    "https://www.instagram.com/",  # bare domain, no post id at all
    "https://www.instagram.com/someaccount/",  # a profile page
]
NON_INSTAGRAM_URL_UNBLOCKED = "https://github.com/org/tool"


def test_every_instagram_path_shape_is_blocked_by_the_real_config():
    results = ts_check_unfetchable_real_config(INSTAGRAM_URLS_BLOCKED + [NON_INSTAGRAM_URL_UNBLOCKED])
    assert results[:-1] == [True] * len(INSTAGRAM_URLS_BLOCKED)
    assert results[-1] is False  # sanity: the check can actually say "unblocked"


def test_fenced_text_block_with_an_instagram_source_is_ingested_not_blocked(tmp_path):
    # Why: this is the exact shape the Instagram reel adapter's no-verified-tool
    # fallback writes (source: <reel url>) — it must be ingested (R6's
    # existing precedent: text items skip the url-only block rule), or every
    # route-2 reel would loop forever as `⚠ needs-link`.
    import json
    import subprocess
    from pathlib import Path

    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    tsx = repo_root / "node_modules" / ".bin" / "tsx"
    script = Path(__file__).parent / "check_text_item_ingest.ts"
    reel_url = "https://www.instagram.com/reel/De5smNojeZm/"
    result = subprocess.run(
        [str(tsx), str(script), reel_url, "a caption and transcript"],
        capture_output=True, text=True, cwd=repo_root,
    )
    assert result.returncode == 0, result.stderr
    out = json.loads(result.stdout)
    assert out["result"]["ingested"] == 1
    assert out["result"]["blocked"] == 0
    assert out["queue"]["items"][0]["url"] == reel_url
