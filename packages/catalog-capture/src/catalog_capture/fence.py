"""Neutralize captured text that would break the inbox's ```text fence.

`inbox.ts` closes a fenced block on any line matching the JS regex
`^\\s*```\\s*$` (FENCE_CLOSE). JS `\\s` matches more codepoints than Python's
`\\s` - e.g. a BOM (U+FEFF) passes JS `\\s` but not Python's, so a captured
line that is just a BOM plus a triple backtick would evade a naive Python
check and still close the fence early.

The codepoint list below (25 characters) was enumerated by running
`/^\\s$/.test(String.fromCharCode(cp))` over every UTF-16 code unit from
0x0000 to 0xFFFF in `node` - not assumed from memory. Built from integer
codepoints (not literal characters) so nothing invisible lives in this file.

We insert a zero-width space (U+200B - not in the list above) into the
triple-backtick run so the line no longer matches FENCE_CLOSE, while
remaining visually identical when rendered.
"""

from __future__ import annotations

import re

# Node evidence: node -e "for (cp=0; cp<=0xFFFF; cp++) if (/^\s$/.test(String.fromCharCode(cp))) print(cp)"
_JS_WHITESPACE_CODEPOINTS = [
    0x0009, 0x000A, 0x000B, 0x000C, 0x000D, 0x0020, 0x00A0, 0x1680,
    0x2000, 0x2001, 0x2002, 0x2003, 0x2004, 0x2005, 0x2006, 0x2007,
    0x2008, 0x2009, 0x200A, 0x2028, 0x2029, 0x202F, 0x205F, 0x3000, 0xFEFF,
]
_JS_WHITESPACE = "".join(chr(cp) for cp in _JS_WHITESPACE_CODEPOINTS)
_ZWSP = chr(0x200B)

_FENCE_CLOSE_LINE = re.compile("^[" + _JS_WHITESPACE + "]*```[" + _JS_WHITESPACE + "]*$")


def defuse_fence_breaks(text: str) -> str:
    """Insert a ZWSP into any line that is exactly a (possibly whitespace-padded,
    using JS's wider whitespace set) triple-backtick, so it no longer matches
    inbox.ts's FENCE_CLOSE."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if _FENCE_CLOSE_LINE.match(line):
            lines[i] = line.replace("```", "`" + _ZWSP + "``", 1)
    return "\n".join(lines)
