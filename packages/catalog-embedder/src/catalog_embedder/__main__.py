"""CLI entry point: `python -m catalog_embedder build|search ...`"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .build import run_build
from .search import DEFAULT_ALPHA, DEFAULT_LIMIT, run_search


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m catalog_embedder")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build", help="Embed all catalog entries and write the vector file")
    build_parser.add_argument("--dir", required=True, help="Path to the repo root")

    search_parser = subparsers.add_parser("search", help="Hybrid lexical + semantic search")
    search_parser.add_argument("--query", required=True)
    search_parser.add_argument("--dir", required=True, help="Path to the repo root")
    search_parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    search_parser.add_argument("--alpha", type=float, default=DEFAULT_ALPHA)
    search_parser.add_argument("--decision-status", dest="decision_status", default=None)
    search_parser.add_argument("--category", dest="category", default=None)

    args = parser.parse_args(argv)

    if args.command == "build":
        run_build(Path(args.dir))
        return 0

    if args.command == "search":
        response = run_search(
            Path(args.dir),
            args.query,
            limit=args.limit,
            alpha=args.alpha,
            decision_status=args.decision_status,
            category=args.category,
        )
        json.dump(response, sys.stdout)
        sys.stdout.write("\n")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
