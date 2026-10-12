import json
from pathlib import Path

import pytest

ENTRY_TEMPLATE = """---
name: {name}
title: {title}
category: {category}
summary: "{summary}"
tags: [{tags}]
---

{body}
"""


def write_entry(entries_dir: Path, name: str, title: str, category: str, summary: str, tags: list[str], body: str) -> None:
    content = ENTRY_TEMPLATE.format(
        name=name,
        title=title,
        category=category,
        summary=summary,
        tags=", ".join(tags),
        body=body,
    )
    (entries_dir / f"{name}.md").write_text(content, encoding="utf-8")


@pytest.fixture
def catalog_dir(tmp_path: Path) -> Path:
    entries_dir = tmp_path / "catalog" / "entries"
    entries_dir.mkdir(parents=True)
    (tmp_path / "catalog" / "taxonomy.json").write_text(json.dumps({"canonical": {}}), encoding="utf-8")
    return tmp_path
