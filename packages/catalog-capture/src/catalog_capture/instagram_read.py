"""The OR-1 Claude read call (I3): caption + transcript + contact-sheet image,
no tools, stream-json in and out — same command/message/parse shape as
`toolkit-workbench/reel/scripts/run_bench.py` `build_claude_command` /
`build_stream_message` / `parse_claude_stream_result` (verified against the
real `claude --print` invocations captured in
`toolkit-workbench/reel/fixtures/or1/*.cmd.txt` — this module is a fresh
implementation against that same evidence, not an import from the gitignored
workbench, R9).

I3's new response shape (`tools: [{name, url}]`, `on_screen_text`) did not
exist before this slice — `build_read_prompt` below is this slice's own
prompt, and the shape it asks for was captured for real against the golden
reel's contact sheet before this parser was written (evidence discipline,
AGENTS 22-24); see `tests/fixtures/instagram/read_response.json`.
"""

from __future__ import annotations

import base64
import json
import re
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

CLAUDE_FLAGS = [
    "--print", "--setting-sources", "project", "--tools", "", "--strict-mcp-config",
    "--no-session-persistence", "--input-format", "stream-json", "--output-format",
    "stream-json", "--verbose", "--model", "sonnet",
]
CLAUDE_BUDGET_FLAGS = ["--max-budget-usd", "0.50"]


def build_claude_command() -> list[str]:
    return ["claude"] + CLAUDE_FLAGS + CLAUDE_BUDGET_FLAGS


def build_stream_message(text_blocks: list[str], image_path: Path | None = None) -> str:
    """One stream-json stdin line: a single `type: "user"` message whose
    `content` is the given text block(s) followed by an optional base64 image
    block — exact shape verified against `fixtures/or1/*.cmd.txt`."""
    content: list[dict] = [{"type": "text", "text": t} for t in text_blocks]
    if image_path is not None:
        data = base64.b64encode(image_path.read_bytes()).decode("ascii")
        content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": data}})
    msg = {"type": "user", "message": {"role": "user", "content": content}, "parent_tool_use_id": None}
    return json.dumps(msg) + "\n"


def parse_claude_stream_result(stdout_text: str) -> dict | None:
    """Scan stdout as JSON-lines for the final `type: "result"` event and pull
    the OR-1 usage fields — written against `tests/fixtures/instagram/
    read_response.json` and `fixtures/or1/*.json` (real captures), not memory."""
    result_event = None
    for line in stdout_text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and obj.get("type") == "result":
            result_event = obj
    if result_event is None:
        return None
    usage = result_event.get("usage", {}) or {}
    model_usage = result_event.get("modelUsage", {}) or {}
    model_id = next(iter(model_usage.keys()), None)
    return {
        "is_error": result_event.get("is_error"),
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens"),
        "cache_read_tokens": usage.get("cache_read_input_tokens"),
        "cache_creation_tokens": usage.get("cache_creation_input_tokens"),
        "model": model_id,
        "result_text": result_event.get("result", ""),
        "raw": result_event,
    }


def build_read_prompt(caption: str | None, transcript_text: str) -> str:
    """This slice's read prompt (I3): extends the WK-0079 read prompt from a
    single tool/URL guess to a *list* of named tools (G2: one reel can name
    several, e.g. DeIm-UyIzbz's 7 CLI tools) plus the on-screen text itself
    (not just whether it carried the key info) — used to list each tool as an
    unverified hint (OR-3 — never verified at capture time) and to fill the
    sources file's "on-screen text" field."""
    caption_block = caption or "(no caption captured)"
    return f"""You are shown the caption posted with an Instagram reel, a transcript of its spoken audio, and an attached contact sheet image tiling keyframes extracted from the reel's video.

Caption (posted with the reel):
\"\"\"
{caption_block}
\"\"\"

Transcript (spoken audio, timestamps in seconds):
\"\"\"
{transcript_text}
\"\"\"

Based on the attached contact sheet image, the caption, and the transcript, answer:
1. List every distinct tool, repo, or named project this reel is about or demonstrates. For each one, give its name and its URL if the URL is visible on screen in the contact sheet, spoken aloud in the transcript, or given in the caption — otherwise null for that tool's url. If the reel names no tool/repo/project, return an empty list.
2. Transcribe any text visible on screen in the contact sheet image (filenames, shell commands, URLs, step labels, UI labels, etc.) into one string, in reading order. Empty string if no text is visible.
3. List the key claims made in the reel.
4. Which channel carried the key information: "spoken" (the transcript), "on-screen" (visible in the contact sheet image), or "caption" (the posted caption text)?

Respond with ONLY a JSON object matching this exact shape, no other text before or after it:
{{
  "tools": [{{"name": "<string>", "url": "<string or null>"}}],
  "on_screen_text": "<string>",
  "key_claims": ["<string>", "<string>", "..."],
  "info_channel": "spoken" | "on-screen" | "caption"
}}"""


class ReadCallFailedError(RuntimeError):
    """The claude subprocess failed, timed out, or returned no result event."""


class ReadResponseUnparsableError(RuntimeError):
    """The result event's text did not contain the expected JSON object."""


@dataclass
class ReadResult:
    tools: list[dict]  # [{"name": str, "url": str | None}, ...]
    on_screen_text: str
    key_claims: list[str]
    info_channel: str
    raw_stdout: str  # full stream-json stdout, verbatim (goes beside the sources file)
    usage: dict  # input/output/cache_read/cache_creation tokens + model, for reporting


def run_claude_read(prompt: str, sheet_path: Path, *, timeout: int = 300) -> ReadResult:
    """One OR-1 claude call (I3): fresh empty temp cwd, prompt + sheet image on
    stdin as stream-json, usage read from the final result event."""
    msg = build_stream_message([prompt], sheet_path)
    with tempfile.TemporaryDirectory() as tmp:
        proc = subprocess.run(
            build_claude_command(), input=msg, capture_output=True, text=True, timeout=timeout, cwd=tmp,
        )
    parsed = parse_claude_stream_result(proc.stdout) if proc.stdout else None
    if parsed is None or proc.returncode != 0:
        raise ReadCallFailedError(proc.stderr.strip()[-800:] or "no result event in claude stdout")
    if parsed["is_error"]:
        raise ReadCallFailedError(f"claude returned is_error=true: {parsed['result_text'][:400]}")

    m = re.search(r"\{.*\}", parsed["result_text"], re.DOTALL)
    if not m:
        raise ReadResponseUnparsableError(f"no JSON object in result text: {parsed['result_text'][:400]}")
    try:
        obj = json.loads(m.group(0))
    except json.JSONDecodeError as e:
        raise ReadResponseUnparsableError(f"result text JSON did not parse: {e}") from e

    tools = obj.get("tools")
    if not isinstance(tools, list):
        raise ReadResponseUnparsableError(f'"tools" missing or not a list: {obj.get("tools")!r}')

    return ReadResult(
        tools=[{"name": t.get("name"), "url": t.get("url")} for t in tools if isinstance(t, dict) and t.get("name")],
        on_screen_text=str(obj.get("on_screen_text") or ""),
        key_claims=[str(c) for c in obj.get("key_claims") or []],
        info_channel=str(obj.get("info_channel") or ""),
        raw_stdout=proc.stdout,
        usage={
            "input_tokens": parsed["input_tokens"],
            "output_tokens": parsed["output_tokens"],
            "cache_read_tokens": parsed["cache_read_tokens"],
            "cache_creation_tokens": parsed["cache_creation_tokens"],
            "model": parsed["model"],
        },
    )


# --------------------------------------------------------------------------
# USD pricing (OR-1.4) — kb's vendored, pinned LiteLLM table.
# --------------------------------------------------------------------------

LITELLM_PRICES_PATH = Path(
    "/home/mcap91/projects/kb/packages/wiki-core/src/pricing/litellm-prices.json"
)
LITELLM_TABLE_PIN = "BerriAI/litellm@94a29e07085dd9d8f2269ee93e899ef0e374cdc7"  # pricing.ts:32

_PRICING_TABLE: dict | None = None


def _load_pricing_table() -> dict:
    global _PRICING_TABLE
    if _PRICING_TABLE is None:
        try:
            _PRICING_TABLE = json.loads(LITELLM_PRICES_PATH.read_text())
        except OSError:
            _PRICING_TABLE = {}
    return _PRICING_TABLE


def price_usage(usage: dict) -> tuple[float | None, str | None]:
    """kb `pricing.ts` formula against the pinned LiteLLM table (OR-1.4):
    exact model-id key match only, else `(None, reason)` — never a substitute
    rate. `total_cost_usd` is never used."""
    model = usage.get("model")
    if not model:
        return None, "no model id resolved from modelUsage"
    table = _load_pricing_table()
    entry = table.get(model)
    if entry is None:
        return None, f'no LiteLLM price row for model "{model}" ({LITELLM_TABLE_PIN})'
    usd = (
        (usage.get("input_tokens") or 0) * entry.get("input_cost_per_token", 0)
        + (usage.get("output_tokens") or 0) * entry.get("output_cost_per_token", 0)
        + (usage.get("cache_creation_tokens") or 0) * entry.get("cache_creation_input_token_cost", 0)
        + (usage.get("cache_read_tokens") or 0) * entry.get("cache_read_input_token_cost", 0)
    )
    return usd, None


def timed_read(prompt: str, sheet_path: Path, *, timeout: int = 300) -> tuple[ReadResult, float]:
    t0 = time.perf_counter()
    result = run_claude_read(prompt, sheet_path, timeout=timeout)
    return result, time.perf_counter() - t0
