#!/usr/bin/env python3
"""Stop hook: log the word count of each Claude Code reply. Logger only; it never blocks.

Pairs with the `direct` output style (target 200-300 words). After a week of data, pick a
blocking ceiling from the log, not from a guess.

Writes to ~/.claude/reply-length/:
  log.jsonl                 one line per reply: ts, session_id, cwd, words, source
  capture-stop-input.json   the first raw Stop-hook input seen (evidence for the input shape)

Words are counted over every assistant text block since the last real user prompt (what the
reader sees in that turn). Fenced code blocks are not counted. The hook always exits 0.
"""
import json, os, re, sys, time

OUT = os.path.expanduser("~/.claude/reply-length")
FENCE = re.compile(r"```.*?```", re.S)


def words(text):
    return len(FENCE.sub(" ", text).split())


def turn_text(transcript_path):
    entries = []
    with open(transcript_path) as f:
        for line in f:
            try:
                entries.append(json.loads(line))
            except ValueError:
                continue
    texts = []
    for e in reversed(entries):
        content = (e.get("message") or {}).get("content")
        if e.get("type") == "user":
            is_prompt = isinstance(content, str) or any(
                isinstance(c, dict) and c.get("type") == "text" for c in (content or []))
            if is_prompt:
                break
        elif e.get("type") == "assistant":
            for c in content or []:
                if isinstance(c, dict) and c.get("type") == "text":
                    texts.append(c.get("text", ""))
    return "\n".join(reversed(texts))


def main():
    raw = sys.stdin.read()
    os.makedirs(OUT, exist_ok=True)
    cap = os.path.join(OUT, "capture-stop-input.json")
    if not os.path.exists(cap):
        with open(cap, "w") as f:
            f.write(raw)
    data = json.loads(raw)
    if isinstance(data.get("last_assistant_message"), str):
        text, source = data["last_assistant_message"], "last_assistant_message"
    else:
        text, source = turn_text(data["transcript_path"]), "transcript"
    row = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "session_id": data.get("session_id"),
           "cwd": data.get("cwd"), "words": words(text), "source": source}
    with open(os.path.join(OUT, "log.jsonl"), "a") as f:
        f.write(json.dumps(row) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # a logger must never break a session
        try:
            with open(os.path.join(OUT, "errors.log"), "a") as f:
                f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {exc!r}\n")
        except OSError:
            pass
    sys.exit(0)
