"""Tool version strings for the capture record (R8)."""

from __future__ import annotations

import importlib.metadata


def playwright_version() -> str:
    return importlib.metadata.version("playwright")
