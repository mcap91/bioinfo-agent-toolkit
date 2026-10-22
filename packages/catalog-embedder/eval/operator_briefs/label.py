"""Build operator_briefs/answer_key.json: a no-tools model labels every catalog entry
against every operator brief, with roles, in two passes plus a tie-break.

Run: `.venv/bin/python eval/operator_briefs/label.py --dir <repo>`. The model only
classifies; everything else (corpus selection, batching, response parsing, the
post-parse re-checks, and the tie-break majority vote) is deterministic. Any shape
drift or re-check failure prints a named reason and exits 1.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

EVAL_DIR = Path(__file__).parent
BRIEFS_PATH = EVAL_DIR / "briefs.json"
RAW_DIR = EVAL_DIR / "raw"

MODEL = "claude-opus-5-5"
BATCH_CHUNK_SIZE = 40
SEED = 76

ROLE_ENUM = ("use", "similar", "same-problem", "guide")

SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "labels": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "relevant": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "object",
                            "properties": {
                                "roles": {
                                    "type": "array",
                                    "items": {"type": "string", "enum": list(ROLE_ENUM)},
                                    "minItems": 1,
                                },
                                "quote": {"type": "string", "minLength": 1},
                                "reason": {"type": "string", "minLength": 1},
                            },
                            "required": ["roles", "quote", "reason"],
                        },
                    },
                },
                "required": ["name", "relevant"],
            },
        }
    },
    "required": ["labels"],
}

PROMPT_INSTRUCTION = (
    "Label each catalog entry below against every brief, using the rule and roles. For each entry "
    "return its name and an object mapping each brief id it is relevant to (per the rule) to: "
    "roles (one or more of the role names), quote (a phrase copied exactly from that entry's text "
    "that shows why it is relevant), and reason (one line). Use an empty object if the entry is "
    "relevant to no brief."
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


def make_batches(names: list[str]) -> list[list[str]]:
    return [names[i : i + BATCH_CHUNK_SIZE] for i in range(0, len(names), BATCH_CHUNK_SIZE)]


def build_prompt(briefs_text: str, batch_entries: list[tuple[str, str]]) -> str:
    parts = [PROMPT_INSTRUCTION, "BRIEFS:", briefs_text]
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
    131072-byte MAX_ARG_STRLEN.
    """
    command = build_command()
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            command, cwd=tmp, input=prompt, capture_output=True, text=True, check=True
        )
    return json.loads(result.stdout)


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def raw_cache_path(pass_name: str, batch_index: int) -> Path:
    return RAW_DIR / f"{pass_name}-{batch_index:02d}.json"


def raw_followup_cache_path(pass_name: str, batch_index: int) -> Path:
    return RAW_DIR / f"{pass_name}-{batch_index:02d}-missing.json"


def cached_call_claude(prompt: str, pass_name: str, batch_index: int) -> tuple[dict[str, Any], bool]:
    """Call claude once per (pass, batch), persisting the raw response keyed by prompt sha256.

    A cached file whose prompt_sha256 does not match the current prompt means the batch
    contents changed since the cache was written; that is a stale cache (operator decides),
    not something to silently re-pay or silently reuse.
    """
    return _cached_call_claude_at(prompt, raw_cache_path(pass_name, batch_index))


def raw_retry_cache_path(pass_name: str, batch_index: int) -> Path:
    return RAW_DIR / f"{pass_name}-{batch_index:02d}-retry.json"


def cached_retry_call_claude(prompt: str, pass_name: str, batch_index: int) -> tuple[dict[str, Any], bool]:
    """The one whole-batch re-call for a structurally invalid batch response, cached at
    raw/<pass>-<batch>-retry.json under the same prompt_sha256 rules as batch files.
    """
    return _cached_call_claude_at(prompt, raw_retry_cache_path(pass_name, batch_index))


def cached_missing_call_claude(prompt: str, pass_name: str, batch_index: int) -> tuple[dict[str, Any], bool]:
    """The missing-names follow-up of a batch, cached at raw/<pass>-<batch>-missing.json
    under the same prompt_sha256 rules as batch files: written right after the call and
    before parse/check, a matching sha reuses without calling, a mismatched sha fails loud
    naming the file (never overwritten, never reused).
    """
    return _cached_call_claude_at(prompt, raw_followup_cache_path(pass_name, batch_index))


def _cached_call_claude_at(prompt: str, path: Path) -> tuple[dict[str, Any], bool]:
    prompt_sha256 = sha256_hex(prompt)
    if path.exists():
        cached = json.loads(path.read_text(encoding="utf-8"))
        if cached.get("prompt_sha256") != prompt_sha256:
            fail(f"stale cache: {path} prompt_sha256 does not match current prompt")
        return cached["response"], True
    raw = call_claude(prompt)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"prompt_sha256": prompt_sha256, "response": raw}, indent=2) + "\n", encoding="utf-8"
    )
    return raw, False


def parse_labels(raw: Any) -> tuple[list[dict[str, Any]] | None, str | None]:
    """Extract structured_output.labels, or name the structural problem.

    Drift detector: re-capture and update the golden fixture — never accept both shapes.
    """
    if not isinstance(raw, dict):
        return None, "response is not an object"
    if raw.get("is_error") is not False:
        return None, f"unexpected is_error: {raw.get('is_error')!r}"
    if raw.get("subtype") != "success":
        return None, f"unexpected subtype: {raw.get('subtype')!r}"
    structured_output = raw.get("structured_output")
    if not isinstance(structured_output, dict) or not isinstance(structured_output.get("labels"), list):
        return None, "missing field: structured_output.labels"
    labels = structured_output["labels"]
    for item in labels:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            return None, f"label item without a string name: {item!r}"
    return labels, None


def parse_response(raw: dict[str, Any]) -> list[dict[str, Any]]:
    """parse_labels, exiting 1 naming the field on any shape drift."""
    labels, problem = parse_labels(raw)
    if problem is not None:
        fail(problem)
    return labels


def clean_labels(
    labels: list[dict[str, Any]], expected: list[str], pass_name: str, batch_index: int
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str | None]:
    """Deterministic cleanup of one response: drop an extra name (not in `expected`) whose
    `relevant` is empty — it asserts nothing — and keep one copy of identical duplicates.
    Returns (kept labels, cleanup records, structural problem or None). An extra name that
    carries labels, or duplicates that differ, is a structural problem, not a cleanup.
    """
    expected_set = set(expected)
    kept: list[dict[str, Any]] = []
    seen: dict[str, dict[str, Any]] = {}
    cleanups: list[dict[str, Any]] = []
    for item in labels:
        name = item["name"]
        if name not in expected_set:
            if item.get("relevant") == {}:
                cleanups.append({"pass": pass_name, "batch": batch_index, "kind": "dropped_extra", "name": name})
                continue
            return labels, [], f"extra name carrying labels: {name!r}"
        if name in seen:
            if seen[name] == item:
                cleanups.append({"pass": pass_name, "batch": batch_index, "kind": "deduped", "name": name})
                continue
            return labels, [], f"conflicting duplicates: {name!r}"
        seen[name] = item
        kept.append(item)
    return kept, cleanups, None


def structural_labels(
    raw: Any, expected: list[str], pass_name: str, batch_index: int
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str | None]:
    labels, problem = parse_labels(raw)
    if problem is not None:
        return [], [], problem
    return clean_labels(labels, expected, pass_name, batch_index)


def new_records() -> dict[str, list[dict[str, Any]]]:
    return {"followup_calls": [], "cleanups": [], "retries": []}


def resolve_batch(
    pass_name: str,
    batch_index: int,
    batch: list[str],
    batch_entries: list[tuple[str, str]],
    briefs_text: str,
    cache_stats: dict[str, int],
    records: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    """Name-check rule, per batch: cleanup → (structural problem → ONE whole-batch retry,
    which replaces the response and goes back through cleanup) → missing names → ONE
    follow-up. At most 3 calls per batch. Re-calls depend only on structural validity,
    never on what the labels say.
    """
    prompt = build_prompt(briefs_text, batch_entries)
    raw, from_cache = cached_call_claude(prompt, pass_name, batch_index)
    cache_stats["cached" if from_cache else "called"] += 1
    labels, cleanups, problem = structural_labels(raw, batch, pass_name, batch_index)
    if problem is not None:
        records["retries"].append({"pass": pass_name, "batch": batch_index, "reason": problem})
        raw, from_cache = cached_retry_call_claude(prompt, pass_name, batch_index)
        cache_stats["cached" if from_cache else "called"] += 1
        labels, cleanups, problem = structural_labels(raw, batch, pass_name, batch_index)
        if problem is not None:
            fail(f"{pass_name} batch {batch_index}: retry still structurally invalid: {problem}")
    records["cleanups"].extend(cleanups)
    return maybe_label_followup(
        pass_name, batch_index, batch, batch_entries, labels, briefs_text, cache_stats, records
    )


def check_batch_names(labels: list[dict[str, Any]], batch_names: list[str]) -> None:
    returned_names = [label["name"] for label in labels]
    counts = Counter(returned_names)
    duplicates = sorted(name for name, count in counts.items() if count > 1)
    if duplicates:
        fail(f"batch returned duplicate names: {duplicates}")
    missing = sorted(set(batch_names) - set(returned_names))
    extra = sorted(set(returned_names) - set(batch_names))
    if missing or extra:
        fail(f"batch name mismatch: missing={missing} extra={extra}")


def maybe_label_followup(
    pass_name: str,
    batch_index: int,
    batch: list[str],
    batch_entries: list[tuple[str, str]],
    labels: list[dict[str, Any]],
    briefs_text: str,
    cache_stats: dict[str, int],
    records: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    """Resolve a cleaned batch response that is missing names with at most ONE follow-up.

    The follow-up sends only the missing entries, in batch order, built with the same
    build_prompt (same INSTRUCTION, briefs, schema); its raw stdout is cached at
    raw/<pass>-<batch>-missing.json under the same prompt_sha256 rules as batch files
    (before parse/check). The follow-up response gets the same cleanup; if it is still
    structurally invalid, or a name is still missing, the run aborts (follow-ups get no
    retry). The merged set runs the normal name and per-label checks.
    """
    returned_names = {label["name"] for label in labels}
    missing = [name for name in batch if name not in returned_names]
    if not missing:
        return labels

    missing_set = set(missing)
    missing_entries = [(name, text) for name, text in batch_entries if name in missing_set]
    followup_prompt = build_prompt(briefs_text, missing_entries)
    followup_raw, from_cache = cached_missing_call_claude(followup_prompt, pass_name, batch_index)
    cache_stats["cached" if from_cache else "called"] += 1
    records["followup_calls"].append({"pass": pass_name, "batch": batch_index, "names": sorted(missing)})

    followup_labels, cleanups, problem = structural_labels(followup_raw, missing, pass_name, batch_index)
    if problem is not None:
        fail(f"{pass_name} batch {batch_index}: follow-up structurally invalid: {problem}")
    records["cleanups"].extend(cleanups)
    still_missing = sorted(missing_set - {flabel["name"] for flabel in followup_labels})
    if still_missing:
        fail(f"follow-up name mismatch: missing={still_missing}")

    merged = labels + followup_labels
    check_batch_names(merged, batch)
    return merged


_CURLY_QUOTES = {0x2018: ord("'"), 0x2019: ord("'"), 0x201C: ord('"'), 0x201D: ord('"')}

# A real single-line markdown link: text has no `[`, `]`, or newline; url has no `)`,
# whitespace, or newline. Excluding `\n` from both classes keeps this from spanning lines
# (character classes match newline by default, unlike `.`).
_LINK_RE = re.compile(r"\[([^\[\]\n]*)\]\([^)\s]*\)")


def normalize_quote_text(text: str) -> str:
    """Normalize a quote and the entry text identically before the substring check.

    Markdown markup is cosmetic to what the model is quoting: it may copy the rendered
    words without the `[text](url)` link wrapper, the `*`/`_`/backtick emphasis marks, or
    with curly quotes swapped in for straight ones. Case is folded too: a quote that starts
    mid-sentence gets capitalized, and case never changes which words appear. Nothing else
    is normalized (no fuzzy match).
    """
    text = _LINK_RE.sub(r"\1", text)
    text = re.sub(r"[*_`]", "", text)
    text = text.translate(_CURLY_QUOTES)
    return re.sub(r"\s+", " ", text).strip().casefold()


def check_relevant_value(name: str, brief_id: str, value: Any, brief_ids: set[str], entry_text: str) -> None:
    if brief_id not in brief_ids:
        fail(f"unknown brief id {brief_id!r} in label for entry {name!r}")
    if not isinstance(value, dict):
        fail(f"entry {name!r} brief {brief_id!r}: relevant value is not an object")
    roles = value.get("roles")
    if not isinstance(roles, list) or not roles:
        fail(f"entry {name!r} brief {brief_id!r}: roles empty or missing")
    if len(set(roles)) != len(roles):
        fail(f"entry {name!r} brief {brief_id!r}: roles has duplicates: {roles}")
    bad_roles = sorted(set(roles) - set(ROLE_ENUM))
    if bad_roles:
        fail(f"entry {name!r} brief {brief_id!r}: roles not in enum: {bad_roles}")
    quote = value.get("quote")
    if not isinstance(quote, str) or not quote:
        fail(f"entry {name!r} brief {brief_id!r}: quote empty or missing")
    reason = value.get("reason")
    if not isinstance(reason, str) or not reason:
        fail(f"entry {name!r} brief {brief_id!r}: reason empty or missing")
    if normalize_quote_text(quote) not in normalize_quote_text(entry_text):
        fail(f"entry {name!r} brief {brief_id!r}: quote not found in entry text: {quote!r}")


def check_label_entry(name: str, relevant: Any, brief_ids: set[str], entry_text: str) -> None:
    if not isinstance(relevant, dict):
        fail(f"entry {name!r}: relevant is not an object")
    for brief_id, value in relevant.items():
        check_relevant_value(name, brief_id, value, brief_ids, entry_text)


def run_pass(
    dir: Path, commit: str, pass_name: str, batches: list[list[str]], briefs_text: str, brief_ids: set[str]
) -> tuple[dict[str, dict[str, Any]], dict[str, int], dict[str, list[dict[str, Any]]]]:
    """Run every batch of one pass; returns {name: relevant} over the batched names, plus
    {"cached": n, "called": n} counting responses read from the raw cache vs sent to
    claude (retries and follow-ups included), plus the follow-up/cleanup/retry records."""
    pass_result: dict[str, dict[str, Any]] = {}
    cache_stats = {"cached": 0, "called": 0}
    records = new_records()
    for batch_index, batch in enumerate(batches):
        batch_entries = [(name, read_entry_text(dir, commit, name)) for name in batch]
        labels = resolve_batch(pass_name, batch_index, batch, batch_entries, briefs_text, cache_stats, records)
        entry_text_by_name = dict(batch_entries)
        by_name = {label["name"]: label.get("relevant") for label in labels}
        for name in batch:
            relevant = by_name[name]
            check_label_entry(name, relevant, brief_ids, entry_text_by_name[name])
            pass_result[name] = relevant
    return pass_result, cache_stats, records


def run_tiebreak(
    dir: Path,
    commit: str,
    disputed_by_name: dict[str, set[str]],
    briefs_text: str,
    brief_ids: set[str],
) -> tuple[list[list[str]], dict[str, dict[str, Any]], dict[str, int], dict[str, list[dict[str, Any]]]]:
    """Batch the disputed names; only the disputed (name, brief) pairs are read back."""
    batches = make_batches(sorted(disputed_by_name))
    tiebreak_result: dict[str, dict[str, Any]] = {}
    cache_stats = {"cached": 0, "called": 0}
    records = new_records()
    for batch_index, batch in enumerate(batches):
        batch_entries = [(name, read_entry_text(dir, commit, name)) for name in batch]
        labels = resolve_batch("tiebreak", batch_index, batch, batch_entries, briefs_text, cache_stats, records)
        entry_text_by_name = dict(batch_entries)
        by_name = {label["name"]: label.get("relevant") for label in labels}
        for name in batch:
            relevant = by_name[name]
            if not isinstance(relevant, dict):
                fail(f"entry {name!r}: relevant is not an object")
            disputed_relevant: dict[str, Any] = {}
            for brief_id in disputed_by_name[name]:
                if brief_id in relevant:
                    value = relevant[brief_id]
                    check_relevant_value(name, brief_id, value, brief_ids, entry_text_by_name[name])
                    disputed_relevant[brief_id] = value
            tiebreak_result[name] = disputed_relevant
    return batches, tiebreak_result, cache_stats, records


def build_answer_key(dir: Path) -> dict[str, Any]:
    corpus_commit = get_corpus_commit(dir)
    corpus = get_corpus(dir, corpus_commit)

    briefs = json.loads(BRIEFS_PATH.read_text(encoding="utf-8"))
    briefs_text = BRIEFS_PATH.read_text(encoding="utf-8")
    brief_ids = {brief["id"] for brief in briefs["briefs"]}

    pass1_order = sorted(corpus)
    pass2_order = list(corpus)
    random.Random(SEED).shuffle(pass2_order)

    pass1_batches = make_batches(pass1_order)
    pass2_batches = make_batches(pass2_order)

    pass1_result, pass1_cache, pass1_records = run_pass(
        dir, corpus_commit, "pass1", pass1_batches, briefs_text, brief_ids
    )
    pass2_result, pass2_cache, pass2_records = run_pass(
        dir, corpus_commit, "pass2", pass2_batches, briefs_text, brief_ids
    )

    disputed_by_name: dict[str, set[str]] = {}
    for name in corpus:
        for brief_id in brief_ids:
            p1 = brief_id in pass1_result.get(name, {})
            p2 = brief_id in pass2_result.get(name, {})
            if p1 != p2:
                disputed_by_name.setdefault(name, set()).add(brief_id)

    tiebreak_batches, tiebreak_result, tiebreak_cache, tiebreak_records = run_tiebreak(
        dir, corpus_commit, disputed_by_name, briefs_text, brief_ids
    )

    relevant_out: dict[str, dict[str, dict[str, Any]]] = {brief_id: {} for brief_id in brief_ids}
    disagreements: list[dict[str, Any]] = []
    agree_count = 0
    both_relevant = 0
    either_relevant = 0
    role_match_count = 0

    for name in corpus:
        for brief_id in brief_ids:
            p1_val = pass1_result.get(name, {}).get(brief_id)
            p2_val = pass2_result.get(name, {}).get(brief_id)
            p1 = p1_val is not None
            p2 = p2_val is not None

            if p1 == p2:
                is_relevant = p1
                kept_val = p1_val if p1 else None
            else:
                tb_val = tiebreak_result.get(name, {}).get(brief_id)
                tb = tb_val is not None
                disagreements.append({"name": name, "brief": brief_id, "votes": [p1, p2, tb]})
                is_relevant = sum([p1, p2, tb]) >= 2
                kept_val = p1_val if p1 else (p2_val if p2 else tb_val)

            if p1 or p2:
                either_relevant += 1
            if p1 and p2:
                both_relevant += 1
                if set(p1_val["roles"]) == set(p2_val["roles"]):
                    role_match_count += 1
            if p1 == p2:
                agree_count += 1

            if is_relevant and kept_val is not None:
                relevant_out[brief_id][name] = {
                    "roles": kept_val["roles"],
                    "quote": kept_val["quote"],
                    "reason": kept_val["reason"],
                }

    pairs = len(corpus) * len(brief_ids)
    agreement = {
        "pairs": pairs,
        "agreement_rate": (agree_count / pairs) if pairs else 0.0,
        "positive_agreement": (both_relevant / either_relevant) if either_relevant else 0.0,
        "role_match_rate": (role_match_count / both_relevant) if both_relevant else 0.0,
        "disagreements": disagreements,
    }

    return {
        "captured": date.today().isoformat(),
        "corpus_commit": corpus_commit,
        "model": MODEL,
        "cli_version": get_cli_version(),
        "seed": SEED,
        "corpus": corpus,
        "relevant": relevant_out,
        "agreement": agreement,
        "batches": {
            "pass1": len(pass1_batches),
            "pass2": len(pass2_batches),
            "tiebreak": len(tiebreak_batches),
            "cache_hits": pass1_cache["cached"] + pass2_cache["cached"] + tiebreak_cache["cached"],
            "cache_calls": pass1_cache["called"] + pass2_cache["called"] + tiebreak_cache["called"],
            **{
                kind: pass1_records[kind] + pass2_records[kind] + tiebreak_records[kind]
                for kind in ("followup_calls", "cleanups", "retries")
            },
        },
    }


def run_label(dir: Path, output_path: Path) -> dict[str, Any]:
    """Refuse to overwrite an existing answer key before any Claude call."""
    if output_path.exists():
        fail(f"refusing to overwrite existing {output_path}")
    return build_answer_key(dir)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=Path, required=True)
    args = parser.parse_args()
    dir = args.dir.resolve()

    output_path = EVAL_DIR / "answer_key.json"
    answer_key = run_label(dir, output_path)

    output_path.write_text(json.dumps(answer_key, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
