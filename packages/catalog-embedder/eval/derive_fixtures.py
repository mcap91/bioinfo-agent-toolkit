"""Derive golden lexical-member arrays for survey_fixtures.json from the live corpus.

Run manually: `uv run python eval/derive_fixtures.py --dir <repo>`. Output is reviewed
against the pinned anchors in WK-0067 6.1 and committed — not re-derived automatically.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from catalog_embedder.search import lexical_members

# Decision-capture reference sizes (WK-0067 6.1) — flag deviations > +10%.
REFERENCE_SIZES = {
    "ocr": 32,
    "rag": 66,
    "mcp": 147,
    "memory": 123,
    "sandbox": 62,
    "vector": 91,
    "graph": 87,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=Path, required=True)
    args = parser.parse_args()

    fixtures_path = Path(__file__).parent / "survey_fixtures.json"
    fixtures = json.loads(fixtures_path.read_text(encoding="utf-8"))

    entries_dir = args.dir / "catalog" / "entries"
    names = [p.stem for p in entries_dir.glob("*.md")]

    for query in fixtures["queries"]:
        members, _ = lexical_members(entries_dir, names, query["terms"])
        query["golden"] = sorted(members.keys())
        ref = REFERENCE_SIZES.get(query["id"])
        ref_note = f" (reference {ref})" if ref is not None else ""
        print(f"{query['id']}: {len(query['golden'])}{ref_note}")

    fixtures["captured"] = date.today().isoformat()
    fixtures_path.write_text(json.dumps(fixtures, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
