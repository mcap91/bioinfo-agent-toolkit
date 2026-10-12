"""Read/write the precomputed embedding vector file (catalog/.vectors.json)."""

from __future__ import annotations

import json
import math
from pathlib import Path

MODEL_NAME = "BAAI/bge-small-en-v1.5"
DIMS = 384


def vectors_path(dir: Path) -> Path:
    return dir / "catalog" / ".vectors.json"


def read_vectors(dir: Path) -> dict | None:
    path = vectors_path(dir)
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def is_valid(data: dict | None) -> bool:
    return (
        isinstance(data, dict)
        and data.get("model") == MODEL_NAME
        and data.get("dims") == DIMS
        and isinstance(data.get("entries"), dict)
    )


def write_vectors(dir: Path, entries: dict[str, list[float]]) -> None:
    data = {
        "model": MODEL_NAME,
        "dims": DIMS,
        "count": len(entries),
        "entries": entries,
    }
    vectors_path(dir).write_text(json.dumps(data), encoding="utf-8")


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)
