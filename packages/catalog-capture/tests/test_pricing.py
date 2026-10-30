"""Tests for `pricing.py` (WK-0094 Phase B review fix-up): the CLI-value >
env-var > documented-default precedence `resolve_prices_path` implements, and
`price_usage`'s "a missing table or an unknown model id yields `(None,
reason)`, never a substitute rate" contract (OR-1.4).

The "real row prices tokens with the kb formula" test does not invent a row
shape: it reads the real, vendored kb LiteLLM table at
`pricing.DEFAULT_LITELLM_PRICES_PATH` and copies one real row (every field,
verbatim) that happens to carry all four token-cost fields `price_usage`
reads, into a tiny table file under `tmp_path`. If that real file is absent
on this machine, the test is skipped rather than faking a row — report this
if it happens, don't invent field names.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from catalog_capture import pricing

REQUIRED_FIELDS = (
    "input_cost_per_token",
    "output_cost_per_token",
    "cache_creation_input_token_cost",
    "cache_read_input_token_cost",
)


def _find_real_row() -> tuple[str, dict] | None:
    """Returns (model_id, row) for the first real table entry that carries
    all four fields `price_usage` reads, or None if the real table is
    missing/unreadable/has no such row."""
    try:
        table = json.loads(pricing.DEFAULT_LITELLM_PRICES_PATH.read_text())
    except OSError:
        return None
    for model_id, row in table.items():
        if isinstance(row, dict) and all(f in row for f in REQUIRED_FIELDS):
            return model_id, row
    return None


# --------------------------------------------------------------------------
# resolve_prices_path: CLI value > env var > documented default.
# --------------------------------------------------------------------------


def test_resolve_prices_path_cli_value_beats_env_var(monkeypatch):
    monkeypatch.setenv(pricing.ENV_VAR, "/env/table.json")
    assert pricing.resolve_prices_path("/cli/table.json") == Path("/cli/table.json")


def test_resolve_prices_path_env_var_beats_default(monkeypatch):
    monkeypatch.setenv(pricing.ENV_VAR, "/env/table.json")
    assert pricing.resolve_prices_path(None) == Path("/env/table.json")


def test_resolve_prices_path_falls_back_to_documented_default(monkeypatch):
    monkeypatch.delenv(pricing.ENV_VAR, raising=False)
    assert pricing.resolve_prices_path(None) == pricing.DEFAULT_LITELLM_PRICES_PATH


def test_resolve_prices_path_empty_cli_value_does_not_win(monkeypatch):
    """`cli_value` is falsy-checked (`if cli_value:`), so an empty string
    (argparse's "flag not passed" default) falls through to the env var,
    same as None — not a change in behavior, pinned here so a future edit
    to the truthiness check is deliberate."""
    monkeypatch.setenv(pricing.ENV_VAR, "/env/table.json")
    assert pricing.resolve_prices_path("") == Path("/env/table.json")


# --------------------------------------------------------------------------
# price_usage: missing table / unknown model id -> (None, reason), never a
# substitute rate.
# --------------------------------------------------------------------------


def test_price_usage_missing_table_file_returns_none_and_reason(tmp_path: Path):
    missing_path = tmp_path / "does-not-exist.json"
    usd, reason = pricing.price_usage(
        {"model": "any-model", "input_tokens": 100, "output_tokens": 50},
        prices_path=missing_path,
    )
    assert usd is None
    assert reason is not None
    assert "any-model" in reason


def test_price_usage_model_with_no_row_returns_none_and_reason(tmp_path: Path):
    table_path = tmp_path / "prices.json"
    table_path.write_text(json.dumps({"some-other-model": {"input_cost_per_token": 1.0}}), encoding="utf-8")
    usd, reason = pricing.price_usage(
        {"model": "not-in-table", "input_tokens": 100, "output_tokens": 50},
        prices_path=table_path,
    )
    assert usd is None
    assert reason is not None
    assert "not-in-table" in reason


def test_price_usage_no_model_id_returns_none_and_reason(tmp_path: Path):
    usd, reason = pricing.price_usage({"input_tokens": 100}, prices_path=tmp_path / "unused.json")
    assert usd is None
    assert reason is not None


def test_price_usage_real_row_prices_tokens_with_kb_formula(tmp_path: Path):
    found = _find_real_row()
    if found is None:
        pytest.skip(
            f"real kb LiteLLM table not found/usable at {pricing.DEFAULT_LITELLM_PRICES_PATH} "
            "(or it has no row with all of input/output/cache_creation/cache_read cost fields) "
            "— cannot build a non-invented row shape on this machine"
        )
    model_id, real_row = found

    table_path = tmp_path / "prices.json"
    table_path.write_text(json.dumps({model_id: real_row}), encoding="utf-8")

    usage = {
        "model": model_id,
        "input_tokens": 1000,
        "output_tokens": 200,
        "cache_creation_tokens": 50,
        "cache_read_tokens": 25,
    }
    usd, reason = pricing.price_usage(usage, prices_path=table_path)

    assert reason is None
    expected = (
        usage["input_tokens"] * real_row["input_cost_per_token"]
        + usage["output_tokens"] * real_row["output_cost_per_token"]
        + usage["cache_creation_tokens"] * real_row["cache_creation_input_token_cost"]
        + usage["cache_read_tokens"] * real_row["cache_read_input_token_cost"]
    )
    assert usd == expected


def test_price_usage_missing_token_counts_default_to_zero(tmp_path: Path):
    found = _find_real_row()
    if found is None:
        pytest.skip(
            f"real kb LiteLLM table not found/usable at {pricing.DEFAULT_LITELLM_PRICES_PATH} "
            "— cannot build a non-invented row shape on this machine"
        )
    model_id, real_row = found

    table_path = tmp_path / "prices.json"
    table_path.write_text(json.dumps({model_id: real_row}), encoding="utf-8")

    usd, reason = pricing.price_usage({"model": model_id}, prices_path=table_path)

    assert reason is None
    assert usd == 0
