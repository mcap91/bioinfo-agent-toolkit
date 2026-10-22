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
import tempfile
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


def _read_entry_text_at_head(name: str) -> str:
    return label.run_git(["show", f"HEAD:catalog/entries/{name}.md"], REPO_ROOT)


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


FAILING_QUOTE = "Forgetting is a feature — context graphs must know when things have changed"


def test_real_asterisk_emphasis_quote_passes_check():
    """The entry's real line is `**Forgetting is a feature** — ...`; the model's quote
    dropped the `**`. Root cause of the step 4 abort this fix addresses."""
    entry_text = _read_entry_text_at_head("context-graphs-trillion-dollar-elephant")
    relevant = {"hybrid-memory": {"roles": ["guide"], "quote": FAILING_QUOTE, "reason": "x"}}
    label.check_label_entry("context-graphs-trillion-dollar-elephant", relevant, BRIEF_IDS, entry_text)


def test_same_quote_with_one_word_changed_fails_named_fail():
    entry_text = _read_entry_text_at_head("context-graphs-trillion-dollar-elephant")
    mutated_quote = FAILING_QUOTE.replace("Forgetting", "Remembering")
    relevant = {"hybrid-memory": {"roles": ["guide"], "quote": mutated_quote, "reason": "x"}}
    code, stderr = _parse_expecting_exit(
        label.check_label_entry, "context-graphs-trillion-dollar-elephant", relevant, BRIEF_IDS, entry_text
    )
    assert code == 1
    assert "quote not found in entry text" in stderr


def test_markdown_link_text_quote_passes_check():
    """Entry has `[Guidelines ... (facebookresearch/faiss)](https://...)`; the model
    quoted the rendered link text without the `[...]()` wrapper."""
    entry_text = _read_entry_text_at_head("ann-index-methods")
    quote = "Guidelines to choose an index — FAISS wiki (facebookresearch/faiss)"
    relevant = {"local-llm": {"roles": ["guide"], "quote": quote, "reason": "x"}}
    label.check_label_entry("ann-index-methods", relevant, BRIEF_IDS, entry_text)


def test_backtick_code_span_quote_passes_check():
    """Entry has `` `claude --print` `` inline; the model quoted the plain words."""
    entry_text = _read_entry_text_at_head("adeptly")
    quote = "it uses the local claude --print CLI to draft a structured plan"
    relevant = {"local-llm": {"roles": ["use"], "quote": quote, "reason": "x"}}
    label.check_label_entry("adeptly", relevant, BRIEF_IDS, entry_text)


def test_curly_apostrophe_quote_passes_check():
    """Entry has a straight apostrophe ('session's own timestamps'); the model wrote a
    curly apostrophe when quoting it."""
    entry_text = _read_entry_text_at_head("zoetrope")
    quote = "paced by the session’s own timestamps"
    relevant = {"agent-viz": {"roles": ["use"], "quote": quote, "reason": "x"}}
    label.check_label_entry("zoetrope", relevant, BRIEF_IDS, entry_text)


def test_underscore_emphasis_quote_passes_check():
    """Real entry text with a plausible underscore-emphasized word injected (no catalog
    entry currently uses `_word_` emphasis); the model quoted the plain word."""
    base_entry_text = _read_entry_text_at_head("zoetrope")
    entry_text = base_entry_text.replace(
        "indexed by event (not wall-clock)", "indexed by event (not _wall-clock_)"
    )
    assert entry_text != base_entry_text
    quote = "Scrubbable timeline indexed by event (not wall-clock)"
    relevant = {"agent-viz": {"roles": ["use"], "quote": quote, "reason": "x"}}
    label.check_label_entry("zoetrope", relevant, BRIEF_IDS, entry_text)


def test_whitespace_run_in_quote_collapses_to_match_check():
    """The model inserted a line break where the real entry text has a single space."""
    entry_text = _read_entry_text_at_head("zoetrope")
    quote = "paced   by the session's\nown timestamps"
    relevant = {"agent-viz": {"roles": ["use"], "quote": quote, "reason": "x"}}
    label.check_label_entry("zoetrope", relevant, BRIEF_IDS, entry_text)


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


@contextlib.contextmanager
def _temp_raw_dir():
    with tempfile.TemporaryDirectory() as tmp:
        original = label.RAW_DIR
        label.RAW_DIR = Path(tmp)
        try:
            yield Path(tmp)
        finally:
            label.RAW_DIR = original


def test_cached_call_claude_hits_cache_and_makes_zero_calls_on_sha256_match():
    with _temp_raw_dir():
        prompt = "same prompt"
        cached_response = {"is_error": False, "subtype": "success", "structured_output": {"labels": []}}
        path = label.raw_cache_path("pass1", 0)
        path.write_text(
            json.dumps({"prompt_sha256": label.sha256_hex(prompt), "response": cached_response}),
            encoding="utf-8",
        )

        def _boom(*args, **kwargs):
            raise AssertionError("call_claude must not run on a cache hit")

        original_call = label.call_claude
        label.call_claude = _boom
        try:
            raw, from_cache = label.cached_call_claude(prompt, "pass1", 0)
        finally:
            label.call_claude = original_call
        assert from_cache is True
        assert raw == cached_response


def test_cached_call_claude_fails_loud_on_sha256_mismatch_naming_file():
    with _temp_raw_dir():
        path = label.raw_cache_path("pass1", 0)
        path.write_text(json.dumps({"prompt_sha256": "deadbeef", "response": {}}), encoding="utf-8")
        code, stderr = _parse_expecting_exit(label.cached_call_claude, "a different prompt", "pass1", 0)
        assert code == 1
        assert str(path) in stderr


def test_cached_call_claude_writes_raw_file_with_prompt_sha256_before_returning():
    with _temp_raw_dir():
        prompt = "fresh prompt"
        response = {"is_error": False, "subtype": "success", "structured_output": {"labels": []}}
        original_call = label.call_claude
        label.call_claude = lambda p: response
        try:
            raw, from_cache = label.cached_call_claude(prompt, "pass2", 3)
        finally:
            label.call_claude = original_call
        assert from_cache is False
        assert raw == response
        saved = json.loads(label.raw_cache_path("pass2", 3).read_text(encoding="utf-8"))
        assert saved["prompt_sha256"] == label.sha256_hex(prompt)
        assert saved["response"] == response


def test_run_pass_reports_cache_hits_and_calls_and_skips_cached_batches():
    with _temp_raw_dir():
        original_read_entry_text = label.read_entry_text
        original_call_claude = label.call_claude
        label.read_entry_text = lambda dir, commit, name: f"text for {name}"
        call_count = {"n": 0}

        def _call(prompt):
            call_count["n"] += 1
            names = [
                part.split("ENTRY name=", 1)[1].split(":", 1)[0]
                for part in prompt.split("\n\n")
                if part.startswith("ENTRY name=")
            ]
            return {
                "is_error": False,
                "subtype": "success",
                "structured_output": {"labels": [{"name": n, "relevant": {}} for n in names]},
            }

        label.call_claude = _call
        try:
            batches = [["a", "b"], ["c", "d"]]
            cached_batch_entries = [(name, f"text for {name}") for name in batches[0]]
            cached_prompt = label.build_prompt("briefs", cached_batch_entries)
            cached_response = {
                "is_error": False,
                "subtype": "success",
                "structured_output": {"labels": [{"name": n, "relevant": {}} for n in batches[0]]},
            }
            label.raw_cache_path("pass1", 0).write_text(
                json.dumps({"prompt_sha256": label.sha256_hex(cached_prompt), "response": cached_response}),
                encoding="utf-8",
            )
            result, stats = label.run_pass(Path("."), "deadbeef", "pass1", batches, "briefs", set())
        finally:
            label.read_entry_text = original_read_entry_text
            label.call_claude = original_call_claude
        assert stats == {"cached": 1, "called": 1}
        assert call_count["n"] == 1
        assert set(result) == {"a", "b", "c", "d"}


def test_refuses_to_overwrite_existing_answer_key_before_any_claude_call():
    with tempfile.TemporaryDirectory() as tmp:
        existing = Path(tmp) / "answer_key.json"
        existing.write_text("{}", encoding="utf-8")

        def _boom(*args, **kwargs):
            raise AssertionError("build_answer_key must not run when the answer key already exists")

        original = label.build_answer_key
        label.build_answer_key = _boom
        try:
            code, stderr = _parse_expecting_exit(label.run_label, REPO_ROOT, existing)
        finally:
            label.build_answer_key = original
        assert code == 1
        assert "refusing to overwrite" in stderr
        assert str(existing) in stderr


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
