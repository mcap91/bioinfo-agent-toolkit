"""Stage 3: a model keeps the surfaced results someone doing the brief would want to
see, judged from the search response exactly as returned. One call per brief.

Run: `.venv/bin/python eval/operator_briefs/judge.py --score-results
score_expansion_v1_baseline.json`. Any shape drift or re-check failure prints a named
reason and exits 1.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

EVAL_DIR = Path(__file__).parent
ANSWER_KEY_PATH = EVAL_DIR / "answer_key.json"
BRIEFS_PATH = EVAL_DIR / "briefs.json"

MODEL = "claude-opus-5-5"

JUDGE = (
    "The search response below was returned for the brief. Keep every result that someone doing "
    "that work would want to see: one they could use directly, one that does something close, one "
    "that hit the same problem, or a strategy or lesson that applies. Return each kept result's "
    "name and a one-line reason."
)

SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "kept": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "reason": {"type": "string", "minLength": 1},
                },
                "required": ["name", "reason"],
            },
        }
    },
    "required": ["kept"],
}


def fail(reason: str) -> None:
    print(f"FAIL: {reason}", file=sys.stderr)
    sys.exit(1)


def get_cli_version() -> str:
    result = subprocess.run(["claude", "--version"], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def build_prompt(question: str, raw_response: dict[str, Any]) -> str:
    return "\n\n".join([JUDGE, "BRIEF:", question, "SEARCH RESPONSE:", json.dumps(raw_response)])


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


def parse_response(raw: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract structured_output.kept; exit 1 naming the field on any shape drift."""
    if raw.get("is_error") is not False:
        fail(f"unexpected is_error: {raw.get('is_error')!r}")
    if raw.get("subtype") != "success":
        fail(f"unexpected subtype: {raw.get('subtype')!r}")
    structured_output = raw.get("structured_output")
    if not isinstance(structured_output, dict) or not isinstance(structured_output.get("kept"), list):
        fail("missing field: structured_output.kept")
    return structured_output["kept"]


def check_kept(brief_id: str, kept: list[dict[str, Any]], response_names: set[str]) -> None:
    bad = sorted({item["name"] for item in kept} - response_names)
    if bad:
        fail(f"brief {brief_id!r}: kept name(s) not in search response: {bad}")


def stage3_recall(kept_names: set[str], key_names: set[str]) -> float:
    return (len(kept_names & key_names) / len(key_names)) if key_names else 0.0


def judge_brief(brief_id: str, question: str, raw_response: dict[str, Any]) -> dict[str, Any]:
    response_names = {r["name"] for r in raw_response["results"]}
    prompt = build_prompt(question, raw_response)
    raw = call_claude(prompt)
    kept = parse_response(raw)
    check_kept(brief_id, kept, response_names)

    answer_key = json.loads(ANSWER_KEY_PATH.read_text(encoding="utf-8"))
    key_names = set(answer_key["relevant"].get(brief_id, {}).keys())
    kept_names = {item["name"] for item in kept}
    recall = stage3_recall(kept_names, key_names)
    return {"kept": kept, "stage3_recall": recall}


def run_judging(score_results: dict[str, Any], briefs: dict[str, str]) -> dict[str, Any]:
    out_briefs: dict[str, Any] = {}
    for brief_id, brief_result in score_results["briefs"].items():
        out_briefs[brief_id] = judge_brief(brief_id, briefs[brief_id], brief_result["raw_response"])
    return {
        "expansion": score_results["expansion"],
        "model": MODEL,
        "cli_version": get_cli_version(),
        "briefs": out_briefs,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--score-results", required=True, help="score results file name, e.g. score_expansion_v1_baseline.json"
    )
    args = parser.parse_args()

    score_results_path = EVAL_DIR / args.score_results
    score_results = json.loads(score_results_path.read_text(encoding="utf-8"))

    briefs_data = json.loads(BRIEFS_PATH.read_text(encoding="utf-8"))["briefs"]
    briefs = {b["id"]: b["question"] for b in briefs_data}

    output_path = score_results_path.with_name(
        "judge_" + score_results_path.name.removeprefix("score_")
    )
    if output_path.exists():
        fail(f"refusing to overwrite existing {output_path}")

    results = run_judging(score_results, briefs)

    output_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
