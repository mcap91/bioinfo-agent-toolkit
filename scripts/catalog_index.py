#!/usr/bin/env python3
"""Regenerate catalog/index.md from catalog/entries/*.md frontmatter."""

import sys
from pathlib import Path

import yaml

VERDICT_ORDER = ["adopt", "pilot", "watch", "note", "skip"]


def parse_entry(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{path.name}: missing YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{path.name}: malformed YAML frontmatter")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: frontmatter is not a mapping")
    return data


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    entries_dir = repo_root / "catalog" / "entries"
    index_path = repo_root / "catalog" / "index.md"

    if not entries_dir.is_dir():
        print(f"Error: {entries_dir} does not exist or is not a directory", file=sys.stderr)
        sys.exit(1)

    entry_files = sorted(entries_dir.glob("*.md"))
    if not entry_files:
        print(f"Error: no .md files found in {entries_dir}", file=sys.stderr)
        sys.exit(1)

    entries = []
    for f in entry_files:
        data = parse_entry(f)
        data.setdefault("workflows", None)
        data.setdefault("overlaps", None)
        data.setdefault("tags", [])
        if data["workflows"] is None:
            data["workflows"] = []
        if data["overlaps"] is None:
            data["overlaps"] = []
        if data["tags"] is None:
            data["tags"] = []
        entries.append(data)

    lines = []

    # Header
    lines.append("# Catalog Index")
    lines.append("")
    lines.append(
        f"Generated from {len(entries)} entries in `catalog/entries/`."
        " Regenerate with `/catalog index`."
    )
    lines.append("")

    # --- By Verdict ---
    lines.append("## By Verdict")
    lines.append("")
    lines.append("| Item | Category | Verdict | Reason | Tags |")
    lines.append("|---|---|---|---|---|")

    def verdict_key(e):
        vi = VERDICT_ORDER.index(e["verdict"]) if e["verdict"] in VERDICT_ORDER else len(VERDICT_ORDER)
        return (vi, e["title"].lower())

    for e in sorted(entries, key=verdict_key):
        tags_str = ", ".join(e["tags"])
        link = f'[{e["title"]}](entries/{e["name"]}.md)'
        lines.append(f"| {link} | {e['category']} | {e['verdict']} | {e['verdict_reason']} | {tags_str} |")

    lines.append("")

    # --- By Workflow ---
    lines.append("## By Workflow")
    lines.append("")

    workflow_map: dict[str, list[dict]] = {}
    for e in entries:
        wfs = e["workflows"]
        if wfs:
            for wf in wfs:
                workflow_map.setdefault(wf, []).append(e)
        else:
            workflow_map.setdefault("General", []).append(e)

    wf_keys = sorted(k for k in workflow_map if k != "General")
    if "General" in workflow_map:
        wf_keys.append("General")

    for wf in wf_keys:
        lines.append(f"### {wf}")
        lines.append("")
        for e in sorted(workflow_map[wf], key=lambda x: x["title"].lower()):
            link = f'[{e["title"]}](entries/{e["name"]}.md)'
            lines.append(f"- {link} — {e['verdict']} — {e['verdict_reason']}")
        lines.append("")

    # --- By Category ---
    lines.append("## By Category")
    lines.append("")

    cat_map: dict[str, list[dict]] = {}
    for e in entries:
        cat_map.setdefault(e["category"], []).append(e)

    for cat in sorted(cat_map.keys()):
        lines.append(f"### {cat}")
        lines.append("")
        for e in sorted(cat_map[cat], key=lambda x: x["title"].lower()):
            link = f'[{e["title"]}](entries/{e["name"]}.md)'
            lines.append(f"- {link} — {e['verdict']} — {e['verdict_reason']}")
        lines.append("")

    output = "\n".join(lines)
    index_path.write_text(output, encoding="utf-8")
    print(f"Wrote {index_path} ({len(entries)} entries)")


if __name__ == "__main__":
    main()
