"""Golden + mutated-copy tests for label.py's response parser and post-parse re-checks.

Stdlib only, no pytest import, so this runs both under pytest locally
(`pytest eval/operator_briefs/test_label.py`) and via a plain loop over module-level
`test_*` functions where pytest isn't available.
"""

from __future__ import annotations

import contextlib
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import label  # noqa: E402

CAPTURE_DIR = Path(__file__).parent / "captures"
CAPTURE_PATH = CAPTURE_DIR / "claude_print_label_roles.json"
META_PATH = CAPTURE_DIR / "claude_print_label_roles.meta.json"

REPO_ROOT = Path(__file__).resolve().parents[4]

BRIEF_IDS = {
    "local-llm",
    "hybrid-memory",
    "vibe-game",
    "agent-viz",
    "ocr-bench",
    "wiki-scale",
    "organize",
}


def _load_capture() -> dict:
    return json.loads(CAPTURE_PATH.read_text(encoding="utf-8"))


def _load_meta() -> dict:
    return json.loads(META_PATH.read_text(encoding="utf-8"))


def _read_entry_text(name: str) -> str:
    meta = _load_meta()
    return label.run_git(["show", f"{meta['corpus_commit']}:catalog/entries/{name}.md"], REPO_ROOT)


def _parse_expecting_exit(func, *args) -> tuple[int | None, str]:
    buf = io.StringIO()
    try:
        with contextlib.redirect_stderr(buf):
            func(*args)
    except SystemExit as exc:
        return exc.code, buf.getvalue()
    return None, buf.getvalue()


def test_golden_capture_zoetrope_agent_viz_roles_and_all_quotes_verify():
    raw = _load_capture()
    labels = label.parse_response(raw)
    by_name = {entry["name"]: entry["relevant"] for entry in labels}
    assert by_name["zoetrope"]["agent-viz"]["roles"] == ["use", "similar"]

    checked = 0
    for entry in labels:
        name = entry["name"]
        relevant = entry["relevant"]
        if not relevant:
            continue
        entry_text = _read_entry_text(name)
        label.check_label_entry(name, relevant, BRIEF_IDS, entry_text)
        checked += len(relevant)
    assert checked == 8


def test_is_error_true_exits_naming_field():
    raw = _load_capture()
    raw["is_error"] = True
    code, stderr = _parse_expecting_exit(label.parse_response, raw)
    assert code == 1
    assert "is_error" in stderr


def test_missing_structured_output_exits_naming_field():
    raw = _load_capture()
    del raw["structured_output"]
    code, stderr = _parse_expecting_exit(label.parse_response, raw)
    assert code == 1
    assert "structured_output" in stderr


def test_subtype_not_success_exits_naming_field():
    raw = _load_capture()
    raw["subtype"] = "error_max_turns"
    code, stderr = _parse_expecting_exit(label.parse_response, raw)
    assert code == 1
    assert "subtype" in stderr


def test_quote_not_in_entry_exits_naming_quote():
    raw = _load_capture()
    labels = label.parse_response(raw)
    by_name = {entry["name"]: entry["relevant"] for entry in labels}
    relevant = json.loads(json.dumps(by_name["zoetrope"]))
    relevant["agent-viz"]["quote"] = "this phrase is nowhere in the entry text"
    entry_text = _read_entry_text("zoetrope")
    code, stderr = _parse_expecting_exit(
        label.check_label_entry, "zoetrope", relevant, BRIEF_IDS, entry_text
    )
    assert code == 1
    assert "quote" in stderr


def test_unknown_role_exits_naming_roles():
    raw = _load_capture()
    labels = label.parse_response(raw)
    by_name = {entry["name"]: entry["relevant"] for entry in labels}
    relevant = json.loads(json.dumps(by_name["zoetrope"]))
    relevant["agent-viz"]["roles"] = ["invented-role"]
    entry_text = _read_entry_text("zoetrope")
    code, stderr = _parse_expecting_exit(
        label.check_label_entry, "zoetrope", relevant, BRIEF_IDS, entry_text
    )
    assert code == 1
    assert "roles" in stderr


def test_duplicate_batch_name_exits_naming_duplicates():
    raw = _load_capture()
    labels = label.parse_response(raw)
    batch_names = [entry["name"] for entry in labels]
    duped = labels + [labels[0]]
    code, stderr = _parse_expecting_exit(label.check_batch_names, duped, batch_names)
    assert code == 1
    assert "duplicate" in stderr


def test_call_claude_sends_prompt_on_stdin_not_argv():
    """Batch prompts reach ~200 KB, above Linux's 131072-byte MAX_ARG_STRLEN single-
    argument limit, so the prompt must travel as subprocess input, never as an argv
    element.
    """
    prompt = "x" * (131072 + 1)
    recorded = {}

    class _Recorder:
        def __init__(self, *args, **kwargs):
            recorded["args"] = args[0]
            recorded["kwargs"] = kwargs
            self.stdout = json.dumps({"ok": True})

    original_run = label.subprocess.run
    label.subprocess.run = _Recorder
    try:
        label.call_claude(prompt)
    finally:
        label.subprocess.run = original_run

    assert recorded["kwargs"].get("input") == prompt
    assert prompt not in recorded["args"]


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
    print(f"{len(tests)} tests ok")
