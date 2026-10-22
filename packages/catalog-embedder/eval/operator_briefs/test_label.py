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


def test_unmatched_bracket_does_not_swallow_text_up_to_next_real_link():
    """Root cause of a review block: line 28's `t∈[0,1)` has no closing `]`, so the
    old regex's cross-line negated classes started a 'link' there that ran through the
    real link on line 51, erasing everything in between. Normalizing the whole entry
    must leave the line-28 fragment and the span between it and line 51 intact, while
    the real line-51 link still reduces to its text."""
    entry_text = _read_entry_text_at_head("ann-index-methods")
    normalized = label.normalize_quote_text(entry_text)
    assert "a threshold t∈[0,1))" in normalized
    assert "direct computation is already fast enough and exact" in normalized
    assert "Guidelines to choose an index — FAISS wiki (facebookresearch/faiss)" in normalized
    assert "[Guidelines to choose an index" not in normalized


def test_nested_bracket_in_link_text_is_not_treated_as_link():
    """Mutate the real line-51 link so its text contains a nested `[...]` that isn't
    itself immediately followed by `(`. Per the ruled definition (link text has no `[`
    or `]`), this no longer matches as a link from either bracket, so the markup must
    pass through untouched rather than being partially or fully stripped."""
    entry_text = _read_entry_text_at_head("ann-index-methods")
    real_line = (
        "- [Guidelines to choose an index — FAISS wiki (facebookresearch/faiss)]"
        "(https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index)"
        " — memory formulas, scale brackets, nlist/training-sample guidance (fetched directly)."
    )
    assert real_line in entry_text
    mutated_line = real_line.replace(
        "(facebookresearch/faiss)", "([facebookresearch]/faiss)"
    )
    assert mutated_line != real_line
    mutated_text = entry_text.replace(real_line, mutated_line)
    normalized = label.normalize_quote_text(mutated_text)
    assert "[facebookresearch]/faiss" in normalized
    assert "https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index" in normalized


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


def _names_asked(prompt: str) -> list[str]:
    """Entry names a built prompt asks about, in order.

    The real briefs.json text ends with a newline, so the first ENTRY block in the
    joined prompt starts on a line of its own ("\nENTRY name=...") after the split —
    strip before matching so the parser sees every entry.
    """
    return [
        part.lstrip().split("ENTRY name=", 1)[1].split(":", 1)[0]
        for part in prompt.split("\n\n")
        if part.lstrip().startswith("ENTRY name=")
    ]


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
            result, stats, followups = label.run_pass(Path("."), "deadbeef", "pass1", batches, "briefs", set())
        finally:
            label.read_entry_text = original_read_entry_text
            label.call_claude = original_call_claude
        assert stats == {"cached": 1, "called": 1}
        assert followups == []
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


def test_missing_names_triggers_exactly_one_followup_with_only_missing_entries():
    with _temp_raw_dir():
        original_read_entry_text = label.read_entry_text
        original_call_claude = label.call_claude
        label.read_entry_text = lambda dir, commit, name: f"text for {name}"
        calls = []

        def _call(prompt):
            calls.append(prompt)
            names = _names_asked(prompt)
            returned = [n for n in names if n != "b"] if len(calls) == 1 else names
            return {
                "is_error": False,
                "subtype": "success",
                "structured_output": {"labels": [{"name": n, "relevant": {}} for n in returned]},
            }

        label.call_claude = _call
        try:
            result, stats, followups = label.run_pass(
                Path("."), "deadbeef", "pass1", [["a", "b", "c"]], "briefs", set()
            )
        finally:
            label.read_entry_text = original_read_entry_text
            label.call_claude = original_call_claude
        assert len(calls) == 2
        assert _names_asked(calls[0]) == ["a", "b", "c"]
        assert _names_asked(calls[1]) == ["b"]
        assert calls[1].startswith(label.PROMPT_INSTRUCTION)
        assert "BRIEFS:\n\nbriefs" in calls[1]
        assert stats == {"cached": 0, "called": 2}
        assert followups == [{"pass": "pass1", "batch": 0, "names": ["b"]}]
        assert set(result) == {"a", "b", "c"}


def test_complete_batch_records_no_followup_call():
    with _temp_raw_dir():
        original_read_entry_text = label.read_entry_text
        original_call_claude = label.call_claude
        label.read_entry_text = lambda dir, commit, name: f"text for {name}"
        calls = []

        def _call(prompt):
            calls.append(prompt)
            names = _names_asked(prompt)
            return {
                "is_error": False,
                "subtype": "success",
                "structured_output": {"labels": [{"name": n, "relevant": {}} for n in names]},
            }

        label.call_claude = _call
        try:
            result, stats, followups = label.run_pass(
                Path("."), "deadbeef", "pass2", [["a", "b", "c"]], "briefs", set()
            )
        finally:
            label.read_entry_text = original_read_entry_text
            label.call_claude = original_call_claude
        assert len(calls) == 1
        assert stats == {"cached": 0, "called": 1}
        assert followups == []
        assert set(result) == {"a", "b", "c"}


def test_batch_response_with_duplicate_names_aborts_without_followup():
    with _temp_raw_dir():
        original_read_entry_text = label.read_entry_text
        original_call_claude = label.call_claude
        label.read_entry_text = lambda dir, commit, name: f"text for {name}"
        call_count = {"n": 0}

        def _call(prompt):
            call_count["n"] += 1
            return {
                "is_error": False,
                "subtype": "success",
                "structured_output": {
                    "labels": [
                        {"name": "a", "relevant": {}},
                        {"name": "a", "relevant": {}},
                        {"name": "c", "relevant": {}},
                    ]
                },
            }

        label.call_claude = _call
        try:
            code, stderr = _parse_expecting_exit(
                label.run_pass, Path("."), "deadbeef", "pass1", [["a", "b", "c"]], "briefs", set()
            )
        finally:
            label.read_entry_text = original_read_entry_text
            label.call_claude = original_call_claude
        assert code == 1
        assert "duplicate" in stderr
        assert call_count["n"] == 1


def test_batch_response_with_extra_names_aborts_without_followup():
    with _temp_raw_dir():
        original_read_entry_text = label.read_entry_text
        original_call_claude = label.call_claude
        label.read_entry_text = lambda dir, commit, name: f"text for {name}"
        call_count = {"n": 0}

        def _call(prompt):
            call_count["n"] += 1
            names = _names_asked(prompt)
            returned = names + ["z"]
            return {
                "is_error": False,
                "subtype": "success",
                "structured_output": {"labels": [{"name": n, "relevant": {}} for n in returned]},
            }

        label.call_claude = _call
        try:
            code, stderr = _parse_expecting_exit(
                label.run_pass, Path("."), "deadbeef", "pass1", [["a", "b", "c"]], "briefs", set()
            )
        finally:
            label.read_entry_text = original_read_entry_text
            label.call_claude = original_call_claude
        assert code == 1
        assert "name mismatch" in stderr
        assert call_count["n"] == 1


def test_followup_raw_file_written_with_prompt_sha256_before_returning():
    with _temp_raw_dir():
        original_read_entry_text = label.read_entry_text
        original_call_claude = label.call_claude
        label.read_entry_text = lambda dir, commit, name: f"text for {name}"
        calls = []

        def _call(prompt):
            calls.append(prompt)
            names = _names_asked(prompt)
            returned = [n for n in names if n != "b"] if len(calls) == 1 else names
            return {
                "is_error": False,
                "subtype": "success",
                "structured_output": {"labels": [{"name": n, "relevant": {}} for n in returned]},
            }

        label.call_claude = _call
        try:
            label.run_pass(Path("."), "deadbeef", "pass1", [["a", "b", "c"]], "briefs", set())
        finally:
            label.read_entry_text = original_read_entry_text
            label.call_claude = original_call_claude
        saved = json.loads(label.raw_followup_cache_path("pass1", 0).read_text(encoding="utf-8"))
        followup_prompt = label.build_prompt("briefs", [("b", "text for b")])
        assert saved["prompt_sha256"] == label.sha256_hex(followup_prompt)
        assert saved["response"]["structured_output"]["labels"] == [{"name": "b", "relevant": {}}]


def test_followup_served_from_cache_on_matching_sha_makes_no_second_call():
    with _temp_raw_dir():
        original_read_entry_text = label.read_entry_text
        original_call_claude = label.call_claude
        label.read_entry_text = lambda dir, commit, name: f"text for {name}"
        call_count = {"n": 0}

        def _call(prompt):
            call_count["n"] += 1
            names = _names_asked(prompt)
            returned = [n for n in names if n != "b"] if call_count["n"] == 1 else names
            return {
                "is_error": False,
                "subtype": "success",
                "structured_output": {"labels": [{"name": n, "relevant": {}} for n in returned]},
            }

        followup_prompt = label.build_prompt("briefs", [("b", "text for b")])
        followup_response = {
            "is_error": False,
            "subtype": "success",
            "structured_output": {"labels": [{"name": "b", "relevant": {}}]},
        }
        label.raw_followup_cache_path("pass1", 0).write_text(
            json.dumps({"prompt_sha256": label.sha256_hex(followup_prompt), "response": followup_response}),
            encoding="utf-8",
        )
        label.call_claude = _call
        try:
            result, stats, followups = label.run_pass(
                Path("."), "deadbeef", "pass1", [["a", "b", "c"]], "briefs", set()
            )
        finally:
            label.read_entry_text = original_read_entry_text
            label.call_claude = original_call_claude
        assert call_count["n"] == 1
        assert stats == {"cached": 1, "called": 1}
        assert followups == [{"pass": "pass1", "batch": 0, "names": ["b"]}]
        assert set(result) == {"a", "b", "c"}


def test_followup_cache_mismatched_sha_fails_named_and_never_overwritten():
    with _temp_raw_dir():
        path = label.raw_followup_cache_path("pass1", 0)
        payload = json.dumps({"prompt_sha256": "deadbeef", "response": {}})
        path.write_text(payload, encoding="utf-8")

        def _boom(*args, **kwargs):
            raise AssertionError("call_claude must not run on a stale follow-up cache")

        original_call = label.call_claude
        label.call_claude = _boom
        try:
            code, stderr = _parse_expecting_exit(
                label.cached_missing_call_claude, "a different prompt", "pass1", 0
            )
        finally:
            label.call_claude = original_call
        assert code == 1
        assert str(path) in stderr
        assert path.read_text(encoding="utf-8") == payload


def test_still_missing_after_followup_aborts_with_only_one_followup():
    with _temp_raw_dir():
        original_read_entry_text = label.read_entry_text
        original_call_claude = label.call_claude
        label.read_entry_text = lambda dir, commit, name: f"text for {name}"
        call_count = {"n": 0}

        def _call(prompt):
            call_count["n"] += 1
            names = _names_asked(prompt)
            returned = [n for n in names if n != "b"]
            return {
                "is_error": False,
                "subtype": "success",
                "structured_output": {"labels": [{"name": n, "relevant": {}} for n in returned]},
            }

        label.call_claude = _call
        try:
            code, stderr = _parse_expecting_exit(
                label.run_pass, Path("."), "deadbeef", "pass1", [["a", "b", "c"]], "briefs", set()
            )
        finally:
            label.read_entry_text = original_read_entry_text
            label.call_claude = original_call_claude
        assert code == 1
        assert "follow-up name mismatch" in stderr
        assert call_count["n"] == 2


def test_followup_response_with_extra_name_aborts():
    with _temp_raw_dir():
        original_read_entry_text = label.read_entry_text
        original_call_claude = label.call_claude
        label.read_entry_text = lambda dir, commit, name: f"text for {name}"
        call_count = {"n": 0}

        def _call(prompt):
            call_count["n"] += 1
            names = _names_asked(prompt)
            returned = [n for n in names if n != "b"] if call_count["n"] == 1 else names + ["z"]
            return {
                "is_error": False,
                "subtype": "success",
                "structured_output": {"labels": [{"name": n, "relevant": {}} for n in returned]},
            }

        label.call_claude = _call
        try:
            code, stderr = _parse_expecting_exit(
                label.run_pass, Path("."), "deadbeef", "pass1", [["a", "b", "c"]], "briefs", set()
            )
        finally:
            label.read_entry_text = original_read_entry_text
            label.call_claude = original_call_claude
        assert code == 1
        assert "follow-up name mismatch" in stderr
        assert call_count["n"] == 2


def test_followup_response_with_duplicate_name_aborts():
    with _temp_raw_dir():
        original_read_entry_text = label.read_entry_text
        original_call_claude = label.call_claude
        label.read_entry_text = lambda dir, commit, name: f"text for {name}"
        call_count = {"n": 0}

        def _call(prompt):
            call_count["n"] += 1
            names = _names_asked(prompt)
            returned = [n for n in names if n != "b"] if call_count["n"] == 1 else ["b", "b"]
            return {
                "is_error": False,
                "subtype": "success",
                "structured_output": {"labels": [{"name": n, "relevant": {}} for n in returned]},
            }

        label.call_claude = _call
        try:
            code, stderr = _parse_expecting_exit(
                label.run_pass, Path("."), "deadbeef", "pass1", [["a", "b", "c"]], "briefs", set()
            )
        finally:
            label.read_entry_text = original_read_entry_text
            label.call_claude = original_call_claude
        assert code == 1
        assert "follow-up returned duplicate names" in stderr
        assert call_count["n"] == 2


def test_tiebreak_missing_names_triggers_followup_and_checks_disputed_pairs():
    with _temp_raw_dir():
        original_read_entry_text = label.read_entry_text
        original_call_claude = label.call_claude
        label.read_entry_text = lambda dir, commit, name: "entry text with a phrase for agent viz"
        calls = []

        def _call(prompt):
            calls.append(prompt)
            names = _names_asked(prompt)
            if len(calls) == 1:
                returned = []
            else:
                returned = names
            relevant = {"local-llm": {"roles": ["use"], "quote": "a phrase for agent viz", "reason": "x"}}
            return {
                "is_error": False,
                "subtype": "success",
                "structured_output": {
                    "labels": [{"name": n, "relevant": relevant if n == "a" else {}} for n in returned]
                },
            }

        label.call_claude = _call
        try:
            batches, result, stats, followups = label.run_tiebreak(
                Path("."), "deadbeef", {"a": {"local-llm"}}, "briefs", {"local-llm"}
            )
        finally:
            label.read_entry_text = original_read_entry_text
            label.call_claude = original_call_claude
        assert len(calls) == 2
        assert _names_asked(calls[1]) == ["a"]
        assert stats == {"cached": 0, "called": 2}
        assert followups == [{"pass": "tiebreak", "batch": 0, "names": ["a"]}]
        assert result["a"] == {"local-llm": {"roles": ["use"], "quote": "a phrase for agent viz", "reason": "x"}}


def test_capture_missing_label_is_completed_by_followup_and_rechecks_pass():
    meta = _load_meta()
    labels = label.parse_response(_load_capture())
    by_name = {entry["name"]: entry for entry in labels}
    batch = list(meta["names"])
    dropped = "zoetrope"
    assert dropped in by_name
    remaining = [by_name[n] for n in batch if n != dropped]

    with _temp_raw_dir():
        original_read_entry_text = label.read_entry_text
        original_call_claude = label.call_claude
        label.read_entry_text = lambda dir, commit, name: _read_entry_text(name)
        calls = []

        def _call(prompt):
            calls.append(prompt)
            asked = _names_asked(prompt)
            returned = remaining if len(calls) == 1 else [by_name[n] for n in asked]
            return {"is_error": False, "subtype": "success", "structured_output": {"labels": returned}}

        label.call_claude = _call
        try:
            result, stats, followups = label.run_pass(
                REPO_ROOT, "unused-commit", "pass1", [batch], "briefs", BRIEF_IDS
            )
        finally:
            label.read_entry_text = original_read_entry_text
            label.call_claude = original_call_claude
        assert len(calls) == 2
        assert _names_asked(calls[1]) == [dropped]
        assert followups == [{"pass": "pass1", "batch": 0, "names": [dropped]}]
        assert set(result) == set(batch)
        assert result[dropped]["agent-viz"]["roles"] == ["use", "similar"]


def test_answer_key_records_followup_calls_beside_cache_counts():
    with _temp_raw_dir():
        originals = {
            "get_corpus_commit": label.get_corpus_commit,
            "get_corpus": label.get_corpus,
            "read_entry_text": label.read_entry_text,
            "get_cli_version": label.get_cli_version,
            "call_claude": label.call_claude,
        }
        label.get_corpus_commit = lambda dir: "deadbeef"
        label.get_corpus = lambda dir, commit: ["a", "b", "c"]
        label.read_entry_text = lambda dir, commit, name: f"text for {name}"
        label.get_cli_version = lambda: "test-cli"
        call_count = {"n": 0}

        def _call(prompt):
            call_count["n"] += 1
            names = _names_asked(prompt)
            returned = [n for n in names if n != "c"] if call_count["n"] == 1 else names
            return {
                "is_error": False,
                "subtype": "success",
                "structured_output": {"labels": [{"name": n, "relevant": {}} for n in returned]},
            }

        label.call_claude = _call
        try:
            key = label.build_answer_key(Path("."))
        finally:
            for fn_name, fn in originals.items():
                setattr(label, fn_name, fn)
        batches = key["batches"]
        assert batches["pass1"] == 1
        assert batches["pass2"] == 1
        assert batches["tiebreak"] == 0
        assert batches["cache_hits"] == 0
        assert batches["cache_calls"] == 3
        assert batches["followup_calls"] == [{"pass": "pass1", "batch": 0, "names": ["c"]}]


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
    print(f"{len(tests)} tests ok")
