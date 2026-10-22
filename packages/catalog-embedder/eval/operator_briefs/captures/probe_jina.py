"""WK-0076 step 2b(d): capture what fastembed 0.9.0 does with jina-embeddings-v2-small-en.

Run: `.venv/bin/python eval/operator_briefs/captures/probe_jina.py --dir <repo>` (from
packages/catalog-embedder). Writes probe_jina.json beside this file. Probe only — not used by
the engine. bge-small is run through the same append test as the control.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import fastembed
from fastembed import TextEmbedding

from catalog_embedder.build import build_embedding_text
from catalog_embedder.frontmatter import read_all_entries

JINA = "jinaai/jina-embeddings-v2-small-en"
BGE = "BAAI/bge-small-en-v1.5"
APPEND = (
    "\n\nAppended probe paragraph: this tool also ships a live terminal dashboard that shows "
    "every running coding agent, what it is doing, and flags any agent that has hung."
)
OUT = Path(__file__).with_name("probe_jina.json")


def cosine(a, b) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


def append_test(model: TextEmbedding, text: str) -> dict:
    base, appended = list(model.embed([text, text + APPEND]))
    return {"cosine_base_vs_appended": cosine(base, appended), "changed": cosine(base, appended) < 1.0 - 1e-9}


def tokenizer_info(model: TextEmbedding, text: str) -> dict:
    info: dict = {}
    try:
        info["token_count"] = model.token_count(text)
    except Exception as exc:  # record, don't hide: the capture is the evidence
        info["token_count_error"] = repr(exc)
    tok = getattr(getattr(model, "model", None), "tokenizer", None)
    info["tokenizer_truncation"] = getattr(tok, "truncation", "unavailable") if tok else "unavailable"
    return info


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=Path, required=True)
    args = parser.parse_args()
    entries = read_all_entries(args.dir.resolve() / "catalog" / "entries")
    texts = {name: build_embedding_text(name, fm, body) for name, (fm, body) in entries.items()}
    jive = texts["jive"]
    brief = next(
        b["question"]
        for b in json.loads(Path(__file__).parents[1].joinpath("briefs.json").read_text())["briefs"]
        if b["id"] == "agent-viz"
    )

    desc = next(m for m in TextEmbedding.list_supported_models() if m["model"] == JINA)
    t0 = time.time()
    jina = TextEmbedding(model_name=JINA)
    load_s = time.time() - t0

    q_embed = list(jina.embed([brief]))[0]
    q_query = list(jina.query_embed(brief))[0]

    # fastembed's default batch_size (256) fails on whole entries: one attention buffer of
    # ~51 GB (first run, 2026-10-21). Record that failure, then time explicit batch sizes.
    try:
        list(jina.embed(list(texts.values())))
        default_batch = "ok"
    except Exception as exc:
        default_batch = repr(exc)[:400]
    embed_all = {"default_batch_size_256": default_batch}
    for batch_size in (8, 32):
        t0 = time.time()
        vectors = list(jina.embed(list(texts.values()), batch_size=batch_size))
        embed_all[f"batch_size_{batch_size}_cpu_wall_s"] = round(time.time() - t0, 2)
    embed_all.update(entries=len(vectors), dims=len(vectors[0]))

    bge = TextEmbedding(model_name=BGE)
    result = {
        "fastembed_version": fastembed.__version__,
        "model_description": desc,
        "cache_dir": str(getattr(jina, "cache_dir", "unavailable")),
        "load_s": round(load_s, 2),
        "append_test": {"entry": "jive", "jina": append_test(jina, jive), "bge_small_control": append_test(bge, jive)},
        "query_rule": {
            "brief": "agent-viz",
            "cosine_embed_vs_query_embed": cosine(q_embed, q_query),
            "differ": cosine(q_embed, q_query) < 1.0 - 1e-9,
        },
        "tokenizer": {"jina_on_jive": tokenizer_info(jina, jive), "bge_on_jive": tokenizer_info(bge, jive)},
        "embed_all": embed_all,
    }
    OUT.write_text(json.dumps(result, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
