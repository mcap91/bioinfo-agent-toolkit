import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).parent
PACKAGE_DIR = TESTS_DIR.parent
REPO_ROOT = PACKAGE_DIR.parent.parent
FIXTURE_TXT = TESTS_DIR / "fixtures" / "JNjEe87YeN.txt"
# Frozen byte-copy of the real catalog/inbox.md as it stood 2026-10-26 (S4) — tests
# must not depend on the live file, which changes as the catalog pipeline runs.
FIXTURE_INBOX = TESTS_DIR / "fixtures" / "inbox_2026-10-26.md"


def parse_raw_capture(raw: str) -> tuple[str, str]:
    """Parse the WK-0054 own-engine raw capture format (`final <url>` / `title ...` /
    `shreddit-post ... | comments ...` / `body text:` / <text>). Test-only: production
    code never reads this format, it comes straight out of Playwright."""
    lines = raw.split("\n")
    assert lines[0].startswith("final ")
    final_url = lines[0][len("final ") :]
    assert lines[3] == "body text:"
    body_text = "\n".join(lines[4:])
    return final_url, body_text


@pytest.fixture
def golden_capture() -> tuple[str, str]:
    """The real WK-0054 own-engine capture for r/LocalLLaMA Harness2 (R9)."""
    return parse_raw_capture(FIXTURE_TXT.read_text(encoding="utf-8"))


@pytest.fixture
def real_inbox_text() -> str:
    """Frozen copy (S4) of the real catalog/inbox.md, not the live file."""
    return FIXTURE_INBOX.read_text(encoding="utf-8")


INSTAGRAM_FIXTURES_DIR = TESTS_DIR / "fixtures" / "instagram"


@pytest.fixture
def golden_instagram_artifacts() -> dict:
    """Real, unedited golden-reel (De5smNojeZm) artifacts (I8): yt-dlp info
    JSON, the small/cpu/int8 transcript, and the T=0.3 contact sheet, copied
    byte-for-byte from toolkit-workbench/reel/outputs/De5smNojeZm/ (verified
    via md5sum at copy time) — plus this slice's own real OR-1 read response
    (`read_response.jsonl`), captured against this exact sheet/transcript/
    caption with this slice's own prompt (I3; not hand-written, not reused
    from the old WK-0079 read shape)."""
    return {
        "info_json_text": (INSTAGRAM_FIXTURES_DIR / "probe_ytdlp.json").read_text(encoding="utf-8"),
        "transcript_text": (INSTAGRAM_FIXTURES_DIR / "transcript_small_cpu_int8.txt").read_text(encoding="utf-8"),
        "sheet_path": INSTAGRAM_FIXTURES_DIR / "sheet_t0.3.jpg",
        "read_response_text": (INSTAGRAM_FIXTURES_DIR / "read_response.jsonl").read_text(encoding="utf-8"),
    }


def ts_parse_inbox(inbox_path: Path) -> list[dict]:
    """Cross-check: feed a file through the real catalog-mcp inbox.ts parser via tsx."""
    tsx = REPO_ROOT / "node_modules" / ".bin" / "tsx"
    script = TESTS_DIR / "parse_inbox.ts"
    result = subprocess.run(
        [str(tsx), str(script), str(inbox_path)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, f"tsx parse failed: {result.stderr}"
    return json.loads(result.stdout)


def _run_check_unfetchable_script(script_name: str, urls: list[str]) -> list[bool]:
    tsx = REPO_ROOT / "node_modules" / ".bin" / "tsx"
    script = TESTS_DIR / script_name
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(urls, f)
        list_path = f.name
    try:
        result = subprocess.run(
            [str(tsx), str(script), list_path],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        assert result.returncode == 0, f"tsx {script_name} failed: {result.stderr}"
        return json.loads(result.stdout)
    finally:
        Path(list_path).unlink(missing_ok=True)


def ts_check_unfetchable(urls: list[str]) -> list[bool]:
    """Cross-check: run each URL through the real catalog-mcp `drainInbox()` via
    tsx (G1/WK-0080 parity test) — not a reimplementation of the TS rule."""
    return _run_check_unfetchable_script("check_unfetchable.ts", urls)


def ts_check_unfetchable_real_config(urls: list[str]) -> list[bool]:
    """I7 evidence: same real `drainInbox()`, but seeded with this repo's real
    `catalog/config.json` `blocked_domains` (which blocks `instagram.com`
    unconditionally) instead of the Reddit parity harness's empty array."""
    return _run_check_unfetchable_script("check_unfetchable_real_config.ts", urls)
