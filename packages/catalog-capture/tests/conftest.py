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


def ts_check_unfetchable(urls: list[str]) -> list[bool]:
    """Cross-check: run each URL through the real catalog-mcp `drainInbox()` via
    tsx (G1/WK-0080 parity test) — not a reimplementation of the TS rule."""
    tsx = REPO_ROOT / "node_modules" / ".bin" / "tsx"
    script = TESTS_DIR / "check_unfetchable.ts"
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
        assert result.returncode == 0, f"tsx check_unfetchable failed: {result.stderr}"
        return json.loads(result.stdout)
    finally:
        Path(list_path).unlink(missing_ok=True)
