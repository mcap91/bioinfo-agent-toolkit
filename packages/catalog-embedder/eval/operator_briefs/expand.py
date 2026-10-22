"""Capture stage 1: a model reads one operator brief plus the search tool's
description and writes the query + terms it would send.

Run: `.venv/bin/python eval/operator_briefs/expand.py --dir <repo> --out expansion_v1`.
One `claude --print` call per brief; zero other model calls. Any shape drift or
re-check failure prints a named reason and exits 1.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

EVAL_DIR = Path(__file__).parent
BRIEFS_PATH = EVAL_DIR / "briefs.json"
TOOLS_TS_PATH = "packages/catalog-mcp/src/tools.ts"

MODEL = "claude-opus-5-5"

ARTIFACT_NAME_RE = re.compile(r"^[A-Za-z0-9_-]+$")

EXPAND = (
    "You are about to call the catalog search tool described below to answer the brief. "
    "Write the query and terms you would send."
)
LIMITS_LINE = "LIMITS: query <= 2000 chars; terms: up to 50, each 1-200 chars."

SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "query": {"type": "string", "minLength": 1, "maxLength": 2000},
        "terms": {
            "type": "array",
            "items": {"type": "string", "minLength": 1, "maxLength": 200},
            "maxItems": 50,
        },
    },
    "required": ["query", "terms"],
}

SEARCH_TOOL_RE = re.compile(r"name:\s*'search',\s*description:\s*'((?:[^'\\]|\\.)*)'", re.DOTALL)


def fail(reason: str) -> None:
    print(f"FAIL: {reason}", file=sys.stderr)
    sys.exit(1)


def validate_bare_name(value: str, arg_name: str) -> None:
    if not ARTIFACT_NAME_RE.match(value):
        fail(f"{arg_name} {value!r} must be a bare name matching [A-Za-z0-9_-]+")


def resolve_under_eval_dir(path: Path, arg_name: str) -> Path:
    resolved = path.resolve()
    if resolved.parent != EVAL_DIR.resolve():
        fail(f"{arg_name} resolves outside operator_briefs/: {path}")
    return resolved


def run_git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True)
    return result.stdout


def get_commit(dir: Path) -> str:
    return run_git(["rev-parse", "HEAD"], dir).strip()


def unescape_js_single_quoted(raw: str) -> str:
    return raw.replace("\\\\", "\\").replace("\\'", "'")


def extract_tool_description(tools_ts_text: str) -> str:
    """The search tool's `description` string; fail loud unless exactly one is found."""
    matches = SEARCH_TOOL_RE.findall(tools_ts_text)
    if len(matches) != 1:
        fail(f"expected exactly one search tool description, found {len(matches)}")
    return unescape_js_single_quoted(matches[0])


def get_tool_description(dir: Path, commit: str) -> str:
    text = run_git(["show", f"{commit}:{TOOLS_TS_PATH}"], dir)
    return extract_tool_description(text)


def get_cli_version() -> str:
    result = subprocess.run(["claude", "--version"], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def build_prompt(tool_description: str, question: str) -> str:
    return "\n\n".join([EXPAND, "TOOL:", tool_description, LIMITS_LINE, "BRIEF:", question])


def build_command() -> list[str]:
    return [
        "claude",
        "--print",
        "--setting-sources",
        "project",
        "--tools",
        "",
        "--strict-mcp-config",
        "--no-session-persistence",
        "--output-format",
        "json",
        "--model",
        MODEL,
        "--json-schema",
        json.dumps(SCHEMA, separators=(",", ":")),
    ]


def call_claude(prompt: str) -> dict[str, Any]:
    """Run from an empty temp dir, so no repo CLAUDE.md or config can load; prompt on stdin."""
    command = build_command()
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            command, cwd=tmp, input=prompt, capture_output=True, text=True, check=True
        )
    return json.loads(result.stdout)


def parse_response(raw: dict[str, Any]) -> dict[str, Any]:
    """Extract structured_output {query, terms}; exit 1 naming the field on any shape drift."""
    if raw.get("is_error") is not False:
        fail(f"unexpected is_error: {raw.get('is_error')!r}")
    if raw.get("subtype") != "success":
        fail(f"unexpected subtype: {raw.get('subtype')!r}")
    structured_output = raw.get("structured_output")
    if not isinstance(structured_output, dict):
        fail("missing field: structured_output")
    if not isinstance(structured_output.get("query"), str):
        fail("missing field: structured_output.query")
    if not isinstance(structured_output.get("terms"), list):
        fail("missing field: structured_output.terms")
    return structured_output


def check_expansion(brief_id: str, expansion: dict[str, Any]) -> None:
    query = expansion["query"]
    if not 1 <= len(query) <= 2000:
        fail(f"brief {brief_id!r}: query length {len(query)} outside 1-2000 chars")
    terms = expansion["terms"]
    if len(terms) > 50:
        fail(f"brief {brief_id!r}: {len(terms)} terms exceeds 50")
    for term in terms:
        if not isinstance(term, str) or not 1 <= len(term) <= 200:
            fail(f"brief {brief_id!r}: term {term!r} outside 1-200 chars")


def build_expansions(dir: Path) -> dict[str, Any]:
    commit = get_commit(dir)
    tool_description = get_tool_description(dir, commit)
    briefs = json.loads(BRIEFS_PATH.read_text(encoding="utf-8"))["briefs"]

    expansions: dict[str, Any] = {}
    for brief in briefs:
        prompt = build_prompt(tool_description, brief["question"])
        raw = call_claude(prompt)
        expansion = parse_response(raw)
        check_expansion(brief["id"], expansion)
        expansions[brief["id"]] = {"query": expansion["query"], "terms": expansion["terms"]}

    return {
        "model": MODEL,
        "cli_version": get_cli_version(),
        "main_commit": commit,
        "tool_description": tool_description,
        "expansions": expansions,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=Path, required=True)
    parser.add_argument("--out", required=True, help="Expansion name, e.g. expansion_v1")
    args = parser.parse_args()
    dir = args.dir.resolve()

    validate_bare_name(args.out, "--out")
    output_path = resolve_under_eval_dir(EVAL_DIR / f"{args.out}.json", "--out")
    if output_path.exists():
        fail(f"refusing to overwrite existing {output_path}")

    expansions = build_expansions(dir)

    output_path.write_text(json.dumps(expansions, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
