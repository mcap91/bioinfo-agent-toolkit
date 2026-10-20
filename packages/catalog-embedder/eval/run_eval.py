"""Search eval: run 40 engineered queries through substring/lexical/lexical+semantic search
on a sealed copy of the catalog, scored against answer_key.json.

Run: `.venv/bin/python eval/run_eval.py --dir <repo>` (after `label.py` has written
answer_key.json). Any gate failure prints a named reason and exits 1. On success, writes
eval/results.json. The eval never asserts which engine wins — gates check inputs only.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from catalog_embedder.build import run_build
from catalog_embedder.frontmatter import read_all_entries
from catalog_embedder.search import run_search

EVAL_DIR = Path(__file__).parent

QUERY_TYPES = ("name", "keyword", "description", "keyword_list")
ENGINES = ("substring", "lexical", "lexical+semantic")


def fail(reason: str) -> None:
    print(f"FAIL: {reason}", file=sys.stderr)
    sys.exit(1)


def run_git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True)
    return result.stdout


def corpus_at_commit(dir: Path, commit: str) -> list[str]:
    output = run_git(["ls-tree", "-r", "--name-only", commit, "catalog/entries/"], dir)
    names = [Path(line.strip()).stem for line in output.splitlines() if line.strip().endswith(".md")]
    return sorted(names)


def seal_corpus(dir: Path, commit: str, names: list[str], tmp_entries: Path) -> None:
    """Write every corpus entry's content at `commit` into `tmp_entries` — never the working tree."""
    tmp_entries.mkdir(parents=True, exist_ok=True)
    for name in names:
        content = run_git(["show", f"{commit}:catalog/entries/{name}.md"], dir)
        (tmp_entries / f"{name}.md").write_text(content, encoding="utf-8")


def gate_1_corpus_matches(dir: Path, commit: str, corpus: list[str]) -> None:
    live = corpus_at_commit(dir, commit)
    expected = sorted(corpus)
    if live != expected:
        fail(
            "gate 1: corpus mismatch — "
            f"git ls-tree has {sorted(set(live) - set(expected))} not in answer_key, "
            f"answer_key has {sorted(set(expected) - set(live))} not in git ls-tree"
        )


def gate_2_relevant_keys(answer_key: dict, topic_ids: set[str], corpus: list[str]) -> None:
    relevant = answer_key["relevant"]
    if set(relevant.keys()) != topic_ids:
        fail(f"gate 2: relevant keys {sorted(relevant.keys())} != topics.json ids {sorted(topic_ids)}")
    corpus_set = set(corpus)
    for topic_id, names in relevant.items():
        bad = sorted(set(names.keys()) - corpus_set)
        if bad:
            fail(f"gate 2: relevant[{topic_id!r}] names not in corpus: {bad}")


def gate_3_parse_check(parsed: dict, corpus: list[str]) -> None:
    if len(parsed) != len(corpus):
        missing = sorted(set(corpus) - set(parsed.keys()))
        fail(f"gate 3: read_all_entries parsed {len(parsed)}/{len(corpus)} entries; missing {missing}")


def gate_4_queries_schema(queries: list[dict], topic_ids: set[str], corpus: list[str]) -> None:
    ids = [q["id"] for q in queries]
    if len(ids) != 40 or len(set(ids)) != len(ids):
        fail(f"gate 4: expected 40 unique query ids, got {len(ids)} ({len(set(ids))} unique)")
    corpus_set = set(corpus)
    for q in queries:
        if q["topic"] not in topic_ids:
            fail(f"gate 4: query {q['id']!r} has unknown topic {q['topic']!r}")
        if q["type"] not in QUERY_TYPES:
            fail(f"gate 4: query {q['id']!r} has unknown type {q['type']!r}")
        if q["type"] == "name":
            bad = [a for a in q["answer"] if a not in corpus_set]
            if bad:
                fail(f"gate 4: query {q['id']!r} answer(s) not in corpus: {bad}")


def gate_5_in_out_examples(topics: dict, relevant: dict) -> None:
    for topic in topics["topics"]:
        topic_id = topic["id"]
        labeled = set(relevant.get(topic_id, {}).keys())
        missing_in = [n for n in topic["in"] if n not in labeled]
        if missing_in:
            fail(f"gate 5: topic {topic_id!r} in-examples not labeled relevant: {missing_in}")
        wrong_out = [n for n in topic["out"] if n in labeled]
        if wrong_out:
            fail(f"gate 5: topic {topic_id!r} out-examples labeled relevant: {wrong_out}")


def run_substring_engine(repo_dir: Path, tmp_dir: Path, query: str) -> list[str]:
    tsx_bin = repo_dir / "node_modules" / ".bin" / "tsx"
    substring_search_ts = EVAL_DIR / "substring_search.ts"
    result = subprocess.run(
        [str(tsx_bin), str(substring_search_ts), "--dir", str(tmp_dir), "--query", query],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def run_lexical_engines(tmp_dir: Path, query: str) -> list[tuple[str, str]]:
    """All combined (lexical + semantic) results, in order, as (name, match_type)."""
    response = run_search(tmp_dir, query=query)
    return [(r["name"], r["match"]["type"]) for r in response["results"]]


def compute_metrics_for_query(
    query: dict, answer_key: dict, engine_returns: dict[str, list[tuple[str, str | None]]]
) -> dict[str, Any]:
    is_name = query["type"] == "name"
    if is_name:
        target = set(query["answer"])
    else:
        target = set(answer_key["relevant"].get(query["topic"], {}).keys())

    metrics: dict[str, Any] = {}
    for engine in ENGINES:
        pairs = engine_returns[engine]
        names = [name for name, _ in pairs]
        r_set = set(names)
        inter = r_set & target
        size_r = len(names)

        engine_metrics: dict[str, Any] = {
            "size": size_r,
            "topic_recall": (len(inter) / len(target)) if target else 0.0,
            "topic_precision": (len(inter) / size_r) if size_r else 0.0,
            "relevant_found": len(inter),
            "empty": size_r == 0,
        }

        if is_name:
            found_at_1 = bool(names) and names[0] in target
            engine_metrics["found"] = any(n in target for n in names)
            engine_metrics["found_at_1"] = found_at_1
            if engine == "lexical+semantic":
                engine_metrics["found_at_1_match_type"] = pairs[0][1] if found_at_1 and pairs else None

        if engine == "lexical+semantic":
            lexical_names = {n for n, t in pairs if t == "lexical"}
            semantic_names = {n for n, t in pairs if t == "semantic"}
            engine_metrics["recall_by_channel"] = {
                "lexical": (len(target & lexical_names) / len(target)) if target else 0.0,
                "semantic": (len(target & semantic_names) / len(target)) if target else 0.0,
            }
            engine_metrics["relevant_found_by_channel"] = {
                "lexical": len(target & lexical_names),
                "semantic": len(target & semantic_names),
            }

        metrics[engine] = engine_metrics
    return metrics


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def aggregate_group(rows: list[dict], query_type: str) -> dict[str, Any]:
    lexical_candidates_mean = mean([row["lexical_candidates"] for row in rows])
    engines_agg: dict[str, Any] = {}
    for engine in ENGINES:
        engine_rows = [row["metrics"][engine] for row in rows]
        agg: dict[str, Any] = {
            "topic_recall_mean": mean([m["topic_recall"] for m in engine_rows]),
            "topic_precision_mean": mean([m["topic_precision"] for m in engine_rows]),
            "size_mean": mean([m["size"] for m in engine_rows]),
            "relevant_found_mean": mean([m["relevant_found"] for m in engine_rows]),
            "empty_rate": mean([1.0 if m["empty"] else 0.0 for m in engine_rows]),
        }
        if query_type == "name":
            agg["found_rate"] = mean([1.0 if m["found"] else 0.0 for m in engine_rows])
            agg["found_at_1_rate"] = mean([1.0 if m["found_at_1"] else 0.0 for m in engine_rows])
            if engine == "lexical+semantic":
                total = len(engine_rows)
                agg["found_at_1_by_match_type"] = {
                    "lexical": (
                        sum(1 for m in engine_rows if m["found_at_1_match_type"] == "lexical") / total
                        if total
                        else 0.0
                    ),
                    "semantic": (
                        sum(1 for m in engine_rows if m["found_at_1_match_type"] == "semantic") / total
                        if total
                        else 0.0
                    ),
                }
        if engine == "lexical+semantic":
            agg["recall_by_channel_mean"] = {
                "lexical": mean([m["recall_by_channel"]["lexical"] for m in engine_rows]),
                "semantic": mean([m["recall_by_channel"]["semantic"] for m in engine_rows]),
            }
            agg["relevant_found_by_channel_mean"] = {
                "lexical": mean([m["relevant_found_by_channel"]["lexical"] for m in engine_rows]),
                "semantic": mean([m["relevant_found_by_channel"]["semantic"] for m in engine_rows]),
            }
        engines_agg[engine] = agg
    return {"lexical_candidates_mean": lexical_candidates_mean, "engines": engines_agg}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=Path, required=True)
    args = parser.parse_args()
    dir = args.dir.resolve()

    topics = json.loads((EVAL_DIR / "topics.json").read_text(encoding="utf-8"))
    topic_ids = {t["id"] for t in topics["topics"]}
    queries = json.loads((EVAL_DIR / "queries.json").read_text(encoding="utf-8"))["queries"]
    answer_key = json.loads((EVAL_DIR / "answer_key.json").read_text(encoding="utf-8"))

    commit = answer_key["corpus_commit"]
    corpus = answer_key["corpus"]

    gate_1_corpus_matches(dir, commit, corpus)
    print("gate 1 (corpus matches git ls-tree at corpus_commit): passed")

    gate_2_relevant_keys(answer_key, topic_ids, corpus)
    print("gate 2 (relevant keys match topics.json, names in corpus): passed")

    gate_4_queries_schema(queries, topic_ids, corpus)
    print("gate 4 (queries.json: 40 unique ids, valid topics/types/answers): passed")

    gate_5_in_out_examples(topics, answer_key["relevant"])
    print("gate 5 (topic in/out examples labeled correctly): passed")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        tmp_entries = tmp_dir / "catalog" / "entries"
        seal_corpus(dir, commit, corpus, tmp_entries)

        parsed = read_all_entries(tmp_entries)
        gate_3_parse_check(parsed, corpus)
        print("gate 3 (production read_all_entries parses every corpus entry): passed")

        run_build(tmp_dir)

        rows = []
        for query in queries:
            substring_names = run_substring_engine(dir, tmp_dir, query["query"])
            combined_pairs = run_lexical_engines(tmp_dir, query["query"])
            lexical_pairs = [(n, t) for n, t in combined_pairs if t == "lexical"]
            engine_returns = {
                "substring": [(n, None) for n in substring_names],
                "lexical": lexical_pairs,
                "lexical+semantic": combined_pairs,
            }
            metrics = compute_metrics_for_query(query, answer_key, engine_returns)
            rows.append(
                {
                    "id": query["id"],
                    "topic": query["topic"],
                    "type": query["type"],
                    "lexical_candidates": metrics["lexical"]["size"],
                    "metrics": metrics,
                }
            )

    aggregate_by_type_engine = {
        qtype: aggregate_group([r for r in rows if r["type"] == qtype], qtype) for qtype in QUERY_TYPES
    }
    aggregate_by_topic_type_engine: dict[str, dict[str, Any]] = {}
    for topic_id in sorted(topic_ids):
        per_type = {}
        for qtype in QUERY_TYPES:
            group_rows = [r for r in rows if r["topic"] == topic_id and r["type"] == qtype]
            if group_rows:
                per_type[qtype] = aggregate_group(group_rows, qtype)
        aggregate_by_topic_type_engine[topic_id] = per_type

    results = {
        "corpus_commit": commit,
        "calibration_unanimous_rate": answer_key["calibration"]["unanimous_rate"],
        "queries": {row["id"]: row for row in rows},
        "aggregate_by_type_engine": aggregate_by_type_engine,
        "aggregate_by_topic_type_engine": aggregate_by_topic_type_engine,
    }

    results_path = EVAL_DIR / "results.json"
    results_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {results_path}")


if __name__ == "__main__":
    main()
