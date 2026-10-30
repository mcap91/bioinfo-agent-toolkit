"""Registers the two shipped adapters (Reddit, Instagram reel) into the
shared registry on import. `cli.py` imports this package before building any
adapter list; a test that wants the real registered pair does the same."""

from __future__ import annotations

from ..registry import register
from .instagram_reel import InstagramReelAdapter
from .reddit import RedditAdapter

reddit = RedditAdapter()
instagram_reel = InstagramReelAdapter()

register(reddit)
register(instagram_reel)

__all__ = ["InstagramReelAdapter", "RedditAdapter", "instagram_reel", "reddit"]
