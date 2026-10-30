"""USD pricing for a read call (OR-1.4), against kb's vendored, pinned
LiteLLM table (WK-0094 Phase B: the table path is now configurable — CLI
option and/or env var — with the current kb checkout path kept only as the
*documented default*, never a hardcoded sole path or a substitute rate)."""

from __future__ import annotations

import json
import os
from pathlib import Path

# Documented default (kb `pricing.ts:32`'s pin) — overridable via `--prices-path`
# (cli.py) or the env var below. A missing table at whichever path is resolved
# still yields `(None, reason)` from `price_usage`, never a substitute rate.
DEFAULT_LITELLM_PRICES_PATH = Path("/home/mcap91/projects/kb/packages/wiki-core/src/pricing/litellm-prices.json")
LITELLM_TABLE_PIN = "BerriAI/litellm@94a29e07085dd9d8f2269ee93e899ef0e374cdc7"  # pricing.ts:32
ENV_VAR = "CATALOG_CAPTURE_LITELLM_PRICES_PATH"


def resolve_prices_path(cli_value: str | os.PathLike | None = None) -> Path:
    """CLI option > env var > the documented kb-checkout default."""
    if cli_value:
        return Path(cli_value)
    env = os.environ.get(ENV_VAR)
    if env:
        return Path(env)
    return DEFAULT_LITELLM_PRICES_PATH


def load_pricing_table(path: Path) -> dict:
    try:
        return json.loads(Path(path).read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def price_usage(usage: dict, *, prices_path: Path | None = None) -> tuple[float | None, str | None]:
    """kb `pricing.ts` formula against the resolved LiteLLM table (OR-1.4):
    exact model-id key match only, else `(None, reason)` — never a substitute
    rate. `total_cost_usd` is never used."""
    model = usage.get("model")
    if not model:
        return None, "no model id resolved from modelUsage"
    path = prices_path if prices_path is not None else resolve_prices_path()
    table = load_pricing_table(path)
    entry = table.get(model)
    if entry is None:
        return None, f'no LiteLLM price row for model "{model}" ({LITELLM_TABLE_PIN}, table path {path})'
    usd = (
        (usage.get("input_tokens") or 0) * entry.get("input_cost_per_token", 0)
        + (usage.get("output_tokens") or 0) * entry.get("output_cost_per_token", 0)
        + (usage.get("cache_creation_tokens") or 0) * entry.get("cache_creation_input_token_cost", 0)
        + (usage.get("cache_read_tokens") or 0) * entry.get("cache_read_input_token_cost", 0)
    )
    return usd, None
