"""Build answer_key.json: a no-tools model labels every catalog entry against every topic.

Run: `.venv/bin/python eval/label.py --dir <repo>`. The model only classifies; everything
else (corpus selection, batching, response parsing, the per-batch consistency check, and
the calibration majority vote) is deterministic. Any shape drift or consistency failure
prints a named reason and exits 1.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

EVAL_DIR = Path(__file__).parent
TOPICS_PATH = EVAL_DIR / "topics.json"

MODEL = "claude-opus-5-5"
BATCH_CHUNK_SIZE = 40

# None of these are topics.json examples — included in every batch for cross-batch
# consistency measurement.
CALIBRATION_NAMES = [
    "book-to-skill",
    "awesome-harness-engineering",
    "context-graphs-trillion-dollar-elephant",
    "agent-dispatcher",
    "cartographer",
    "understand-anything",
    "memstack",
    "scheduled-multi-agent-coordinator",
    "amazon-textract-textractor",
    "ai-engineering-project-ideas",
]

SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "labels": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "relevant": {"type": "object", "additionalProperties": {"type": "string"}},
                },
                "required": ["name", "relevant"],
            },
        }
    },
    "required": ["labels"],
}

PROMPT_INSTRUCTION = (
    "Label each catalog entry below against every topic. For each entry return its "
    "name and an object mapping each topic id it is relevant to (per the rule) to a "
    "one-line reason; use an empty object if none."
)


def fail(reason: str) -> None:
    print(f"FAIL: {reason}", file=sys.stderr)
    sys.exit(1)


def run_git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True)
    return result.stdout


def get_corpus_commit(dir: Path) -> str:
    return run_git(["rev-parse", "HEAD"], dir).strip()


def get_corpus(dir: Path, commit: str) -> list[str]:
    """Sorted entry names from `git ls-tree` at `commit` — never the working tree."""
    output = run_git(["ls-tree", "-r", "--name-only", commit, "catalog/entries/"], dir)
    names = [Path(line.strip()).stem for line in output.splitlines() if line.strip().endswith(".md")]
    return sorted(names)


def read_entry_text(dir: Path, commit: str, name: str) -> str:
    """Entry file content at `commit` — never the working tree."""
    return run_git(["show", f"{commit}:catalog/entries/{name}.md"], dir)


def get_cli_version() -> str:
    result = subprocess.run(["claude", "--version"], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def make_batches(corpus: list[str], calibration: list[str]) -> list[list[str]]:
    """Other entries sorted by name, chunked, each chunk + the calibration set."""
    calibration_set = set(calibration)
    rest = sorted(n for n in corpus if n not in calibration_set)
    batches = []
    for i in range(0, len(rest), BATCH_CHUNK_SIZE):
        chunk = rest[i : i + BATCH_CHUNK_SIZE]
        batches.append(chunk + list(calibration))
    return batches


def build_prompt(topics_text: str, batch_entries: list[tuple[str, str]]) -> str:
    parts = [PROMPT_INSTRUCTION, "TOPICS:", topics_text]
    parts.extend(f"ENTRY name={name}:\n{text}" for name, text in batch_entries)
    return "\n\n".join(parts)


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
    """Run the labeler from an empty temp dir, so no repo CLAUDE.md or config can load.

    Prompt goes on stdin, never argv: batch prompts reach ~200 KB, above Linux's
    131072-byte MAX_ARG_STRLEN (see captures/claude_print_stdin_batch.json).
    """
    command = build_command()
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            command, cwd=tmp, input=prompt, capture_output=True, text=True, check=True
        )
    return json.loads(result.stdout)


def parse_response(raw: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract structured_output.labels; exit 1 naming the field on any shape drift.

    Drift detector: re-capture and update the golden fixture — never accept both shapes.
    """
    if raw.get("is_error") is not False:
        fail(f"unexpected is_error: {raw.get('is_error')!r}")
    if raw.get("subtype") != "success":
        fail(f"unexpected subtype: {raw.get('subtype')!r}")
    structured_output = raw.get("structured_output")
    if not isinstance(structured_output, dict) or not isinstance(structured_output.get("labels"), list):
        fail("missing field: structured_output.labels")
    return structured_output["labels"]


def check_batch(labels: list[dict[str, Any]], batch_names: list[str], topic_ids: set[str]) -> None:
    returned_names = [label["name"] for label in labels]
    counts = Counter(returned_names)
    duplicates = sorted(name for name, count in counts.items() if count > 1)
    if duplicates:
        fail(f"batch returned duplicate names: {duplicates}")
    missing = sorted(set(batch_names) - set(returned_names))
    extra = sorted(set(returned_names) - set(batch_names))
    if missing or extra:
        fail(f"batch name mismatch: missing={missing} extra={extra}")
    for label in labels:
        for topic_id in label.get("relevant", {}):
            if topic_id not in topic_ids:
                fail(f"unknown topic id {topic_id!r} in label for {label['name']!r}")


def build_answer_key(dir: Path) -> dict[str, Any]:
    corpus_commit = get_corpus_commit(dir)
    corpus = get_corpus(dir, corpus_commit)

    topics = json.loads(TOPICS_PATH.read_text(encoding="utf-8"))
    topics_text = TOPICS_PATH.read_text(encoding="utf-8")
    topic_ids = {topic["id"] for topic in topics["topics"]}

    batches = make_batches(corpus, CALIBRATION_NAMES)
    relevant: dict[str, dict[str, str]] = {topic_id: {} for topic_id in topic_ids}
    calibration_votes: dict[tuple[str, str], list[tuple[bool, str | None]]] = {}

    for batch in batches:
        batch_entries = [(name, read_entry_text(dir, corpus_commit, name)) for name in batch]
        prompt = build_prompt(topics_text, batch_entries)
        raw = call_claude(prompt)
        labels = parse_response(raw)
        check_batch(labels, batch, topic_ids)

        by_name = {label["name"]: label["relevant"] for label in labels}
        for name in batch:
            label_map = by_name[name]
            if name in CALIBRATION_NAMES:
                for topic_id in topic_ids:
                    is_relevant = topic_id in label_map
                    calibration_votes.setdefault((name, topic_id), []).append(
                        (is_relevant, label_map.get(topic_id))
                    )
            else:
                for topic_id, reason in label_map.items():
                    if topic_id in topic_ids:
                        relevant[topic_id][name] = reason

    disagreements: list[dict[str, Any]] = []
    unanimous_count = 0
    for (name, topic_id), votes in calibration_votes.items():
        flags = [flag for flag, _ in votes]
        if len(set(flags)) > 1:
            disagreements.append({"name": name, "topic": topic_id, "votes": flags})
        else:
            unanimous_count += 1
        if sum(flags) * 2 > len(flags):
            reason = next(r for flag, r in votes if flag)
            relevant[topic_id][name] = reason
    unanimous_rate = unanimous_count / len(calibration_votes) if calibration_votes else 0.0

    return {
        "captured": date.today().isoformat(),
        "corpus_commit": corpus_commit,
        "model": MODEL,
        "cli_version": get_cli_version(),
        "corpus": corpus,
        "relevant": relevant,
        "calibration": {
            "names": CALIBRATION_NAMES,
            "batches": len(batches),
            "unanimous_rate": unanimous_rate,
            "disagreements": disagreements,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=Path, required=True)
    args = parser.parse_args()
    dir = args.dir.resolve()

    answer_key = build_answer_key(dir)

    output_path = EVAL_DIR / "answer_key.json"
    output_path.write_text(json.dumps(answer_key, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
