"""Stage 3 diagnostic: why does the judge drop relevant entries the search surfaced?

Run: `.venv/bin/python eval/operator_briefs/judge_diag.py --dir <repo>`. Uses the saved
baseline search responses (score_expansion_v1_baseline.json) and judge.py's JUDGE prompt,
schema, command, and checks, on two briefs:
  J0  baseline judge, 2 more samples (single-sample noise)
  J1  results in response order, chunks of 50, each judged alone; kept = union (volume)
  J2  J1 plus each result's full entry text at the answer key's corpus commit (information)
A J1/J2 chunk is sent as {"results": [...]} — the parent's totals would misstate the chunk.
Every raw response is written on return; cumulative cost above COST_CAP_USD aborts.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import judge
from score import agreed_key_names

EVAL_DIR = Path(__file__).parent
SCORE_PATH = EVAL_DIR / "score_expansion_v1_baseline.json"
OUTPUT_PATH = EVAL_DIR / "judge_diag_expansion_v1_baseline.json"
RAW_DIR = EVAL_DIR / "raw"

BRIEF_IDS = ("local-llm", "hybrid-memory")
J0_SAMPLES = 2
CHUNK_SIZE = 50
COST_CAP_USD = 25.0


def fail(reason: str) -> None:
    print(f"FAIL: {reason}", file=sys.stderr)
    sys.exit(1)


def chunk_results(results: list[dict[str, Any]], size: int) -> list[list[dict[str, Any]]]:
    return [results[i : i + size] for i in range(0, len(results), size)]


def with_entry_text(results: list[dict[str, Any]], texts: dict[str, str]) -> list[dict[str, Any]]:
    return [{**result, "entry_text": texts[result["name"]]} for result in results]


def chunk_response_text(results: list[dict[str, Any]]) -> str:
    return json.dumps({"results": results}, indent=2, ensure_ascii=False)


class Spend:
    def __init__(self, cap: float) -> None:
        self.cap = cap
        self.total = 0.0

    def add(self, cost: Any) -> None:
        self.total += float(cost or 0.0)
        if self.total > self.cap:
            fail(f"cost cap exceeded: ${self.total:.2f} > ${self.cap:.2f}")


def judge_once(question: str, response_text: str, response_names: set[str], brief_id: str, raw_name: str, spend: Spend) -> dict[str, Any]:
    raw_path = RAW_DIR / f"{raw_name}.json"
    if raw_path.exists():
        fail(f"refusing to overwrite existing {raw_path}")
    prompt = judge.build_prompt(question, response_text)
    raw = judge.call_claude(prompt)
    raw_path.write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")
    spend.add(raw.get("total_cost_usd"))
    kept = judge.parse_response(raw)
    judge.check_kept(brief_id, kept, response_names)
    return {"kept": {item["name"] for item in kept}, "cost_usd": raw.get("total_cost_usd"), "prompt_bytes": len(prompt.encode("utf-8"))}


def summarize(kept: set[str], key: set[str], agreed: set[str], cost: float, calls: int) -> dict[str, Any]:
    return {
        "kept_count": len(kept),
        "recall": judge.stage3_recall(kept, key),
        "agreed_recall": judge.stage3_recall(kept, agreed),
        "cost_usd": cost,
        "calls": calls,
        "kept": sorted(kept),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=Path, required=True)
    dir = parser.parse_args().dir.resolve()
    if OUTPUT_PATH.exists():
        fail(f"refusing to overwrite existing {OUTPUT_PATH}")
    RAW_DIR.mkdir(exist_ok=True)

    score_results = json.loads(SCORE_PATH.read_text(encoding="utf-8"))
    answer_key = json.loads(judge.ANSWER_KEY_PATH.read_text(encoding="utf-8"))
    questions = {b["id"]: b["question"] for b in json.loads(judge.BRIEFS_PATH.read_text(encoding="utf-8"))["briefs"]}
    commit = answer_key["corpus_commit"]
    spend = Spend(COST_CAP_USD)
    out: dict[str, Any] = {}

    for brief_id in BRIEF_IDS:
        response_text = score_results["briefs"][brief_id]["raw_response"]
        results = json.loads(response_text)["results"]
        names = {r["name"] for r in results}
        key = set(answer_key["relevant"][brief_id])
        agreed = agreed_key_names(answer_key, brief_id)
        question = questions[brief_id]
        out[brief_id] = {"returned": len(results)}

        j0 = []
        for sample in range(J0_SAMPLES):
            r = judge_once(question, response_text, names, brief_id, f"diag-J0-{brief_id}-{sample}", spend)
            j0.append(summarize(r["kept"], key, agreed, r["cost_usd"], 1))
        out[brief_id]["J0"] = j0

        texts = {
            name: subprocess.run(
                ["git", "show", f"{commit}:catalog/entries/{name}.md"], cwd=dir, capture_output=True, text=True, check=True
            ).stdout
            for name in names
        }
        for variant, with_text in (("J1", False), ("J2", True)):
            kept: set[str] = set()
            cost = 0.0
            chunks = chunk_results(results, CHUNK_SIZE)
            for index, chunk in enumerate(chunks):
                payload = with_entry_text(chunk, texts) if with_text else chunk
                chunk_names = {r["name"] for r in chunk}
                r = judge_once(question, chunk_response_text(payload), chunk_names, brief_id, f"diag-{variant}-{brief_id}-{index:02d}", spend)
                kept |= r["kept"]
                cost += float(r["cost_usd"] or 0.0)
            out[brief_id][variant] = summarize(kept, key, agreed, cost, len(chunks))
        print(f"{brief_id}: done, cumulative ${spend.total:.2f}", file=sys.stderr)

    out["total_cost_usd"] = spend.total
    OUTPUT_PATH.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
