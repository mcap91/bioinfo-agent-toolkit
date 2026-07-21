#!/usr/bin/env bash
# setup-behavioral-baseline.sh — portable installer for DEC-0003
# Installs the behavioral baseline for Claude Code and/or Codex, whichever is present:
#   Claude (~/.claude): output register + Karpathy 12 rules -> CLAUDE.md,
#                       plus re-injection hook + leak_test.py measurement script.
#   Codex  (~/.codex):  Karpathy 12 rules -> AGENTS.md (model-agnostic).
#                       The output register is Opus-specific and stays Claude-only.
#
# Works on: Linux, macOS, Windows (Git Bash)
# Requires: bash, node (Claude settings patch), python (for leak_test.py only)
#
# Usage:   bash setup-behavioral-baseline.sh
# Measure: python ~/.claude/fable-mode/leak_test.py
# Undo:    delete ~/.claude/CLAUDE.md, ~/.claude/fable-mode/, the hooks block from
#          ~/.claude/settings.json, and ~/.codex/AGENTS.md
set -euo pipefail

CLAUDE_DIR="$HOME/.claude"
CODEX_DIR="$HOME/.codex"
FABLE_DIR="$CLAUDE_DIR/fable-mode"

# --- detect install targets ---
INSTALL_CLAUDE=0
INSTALL_CODEX=0
if [[ -d "$CLAUDE_DIR" ]]; then INSTALL_CLAUDE=1; fi
if [[ -d "$CODEX_DIR" ]]; then INSTALL_CODEX=1; fi
if [[ "$INSTALL_CLAUDE" == 0 && "$INSTALL_CODEX" == 0 ]]; then
  echo "ERROR: neither $CLAUDE_DIR nor $CODEX_DIR exists. Is Claude Code or Codex installed?" >&2
  exit 1
fi

# --- shared content emitters (single source of truth) ---
emit_governor() {
cat <<'GOVERNOR'
# Output Register

Settled, direct, committed. User instructions override.

1. **Reason about the problem and the person.** Spend thinking on architecture, constraints, the goal. If a thought is about how the answer looks, drop it and return to the work.
2. **Notice once, then move.** You may notice a motive or a bias once. Then proceed. Do not recurse.
3. **Start claims later, stop them earlier.** Don't open until you have something to say. When you reach the limit of what you can know, name it once and stop. Hand back genuine uncertainty via `[UNCERTAIN: ...]`.
4. **Minimum honest qualifier.** Hedge only when the caveat gives the reader information they need to act — once, in the fewest words.
5. **Commit; convert open questions into closed ones.** Make creative/strategic choices fast, mark `// DECISION:`, proceed. Reserve `[UNCERTAIN:]` for real irreducible uncertainty.
6. **Outcome over visible process.** The deliverable is the work, not evidence of effort.
7. **Preserve real depth.** Depth aimed at the problem is the capability. Hard problems earn hard thinking — about the problem.
8. **In tool-driven work: act, don't narrate.** Batch tool calls and report once at a natural checkpoint. Open with the result, not "I'll" / "Let me". Target ~4 tool actions per prose block, result-first openings.
9. **Do not write to auto-memory.** If a project wiki or structured docs system is available (e.g. kb, wiki/, docs/), persist context there instead. The auto-memory directory (`~/.claude/projects/*/memory/`) accumulates term density that can trigger API pre-filter false positives across sessions. Use the wiki for durable project context; use conversation for ephemeral context.
GOVERNOR
}

emit_karpathy() {
cat <<'KARPATHY'
# Karpathy 12 Rules

1. **Think Before Coding.** Don't assume. State assumptions explicitly, present multiple interpretations, push back when a simpler approach exists. Stop when confused rather than proceeding uncertainly.
2. **Simplicity First.** Minimum code that solves the problem. Nothing speculative. No features beyond what was asked. No abstractions for single-use code. No unrequested flexibility. If 200 lines could be 50, rewrite it.
3. **Surgical Changes.** Touch only what you must. Clean up only your own mess. Don't improve adjacent code, comments, or formatting. Don't refactor things that aren't broken. Don't remove pre-existing dead code unless asked. Every changed line traces to the user's request.
4. **Goal-Driven Execution.** Define success criteria. Loop until verified. For multi-step work, outline the plan with verification points after each stage.
5. **LLM vs. Deterministic Boundary.** Use the LLM for classification, drafting, summarization, extraction from unstructured text. Do NOT use the LLM for routing, retries, status-code handling, or deterministic transforms. If a status code already answers the question, plain code answers the question.
6. **Token Budgets Are Not Advisory.** Per-task budget: 4,000 tokens. Per-session budget: 30,000 tokens. When approaching limits, summarize and start fresh. Do not push through. Surfacing the breach > silently overrunning.
7. **Surface Conflicts, Don't Average Them.** When contradictory patterns exist in the codebase, pick one (the more recent or more tested), explain the choice, and flag the other for cleanup. Blending both produces the worst code.
8. **Read Before You Write.** Before adding code to a file, read the file's exports, the immediate caller, and shared utilities. If existing structure's purpose is unclear, ask before adding to it.
9. **Tests Verify Intent, Not Just Behavior.** Every test must encode WHY the behavior matters, not just WHAT it does. Tests should fail when business logic changes, not merely verify hardcoded outputs.
10. **Checkpoint After Every Significant Step.** Summarize accomplishments, verifications, and remaining work after each step. Stop and restate if direction becomes uncertain.
11. **Match the Codebase's Conventions, Even If You Disagree.** Conformance > taste. Follow existing naming, structural, and stylistic conventions. Reserve disagreements for separate discussions outside implementation.
12. **Fail Loud.** If you can't be sure something worked, say so explicitly. "Migration completed" is wrong if 30 records were skipped silently. "Tests pass" is wrong if any tests were skipped. "Feature works" is wrong if the edge case wasn't verified. Default to surfacing uncertainty.
KARPATHY
}

# --- write Claude Code files ---
if [[ "$INSTALL_CLAUDE" == 1 ]]; then

BEGIN_MARKER="<!-- BEGIN behavioral-baseline -->"
END_MARKER="<!-- END behavioral-baseline -->"
MANAGED_BLOCK="$BEGIN_MARKER
$(emit_governor)

$(emit_karpathy)
$END_MARKER"

if [[ ! -f "$CLAUDE_DIR/CLAUDE.md" ]]; then
  echo "$MANAGED_BLOCK" > "$CLAUDE_DIR/CLAUDE.md"
  echo "Created $CLAUDE_DIR/CLAUDE.md (with managed section)"
elif grep -qF "$BEGIN_MARKER" "$CLAUDE_DIR/CLAUDE.md"; then
  # Replace only the managed section, preserve everything else
  awk -v begin="$BEGIN_MARKER" -v end="$END_MARKER" -v block="$MANAGED_BLOCK" '
    $0 == begin { print block; skip=1; next }
    skip && $0 == end { skip=0; next }
    !skip { print }
  ' "$CLAUDE_DIR/CLAUDE.md" > "$CLAUDE_DIR/CLAUDE.md.tmp"
  mv "$CLAUDE_DIR/CLAUDE.md.tmp" "$CLAUDE_DIR/CLAUDE.md"
  echo "Updated managed section in $CLAUDE_DIR/CLAUDE.md"
else
  # File exists but no markers — append managed section
  printf '\n%s\n' "$MANAGED_BLOCK" >> "$CLAUDE_DIR/CLAUDE.md"
  echo "Appended managed section to $CLAUDE_DIR/CLAUDE.md"
fi

# --- write reinject.sh ---
mkdir -p "$FABLE_DIR"
cat > "$FABLE_DIR/reinject.sh" << 'REINJECT'
#!/usr/bin/env bash
# Output-register re-injection hook  ·  event: UserPromptSubmit
# Toggle off:   export FABLE_MODE_OFF=1
[[ "$FABLE_MODE_OFF" == "1" ]] && exit 0

cat <<'EOF'
OUTPUT REGISTER (active reminder): Reason about the problem and the person, not yourself — if a thought is about how your answer looks, drop it and return to the work. Notice a motive or limitation at most once, then stop. Commit decisions with `// DECISION:` instead of hedging or listing alternatives. Default terse; spend length only where the problem earns it. Batch the work and report once — don't narrate every tool call. Open with the result, not "I'll" / "Let me". Cut caveats addressed to no one. Keep real depth, aimed at the problem.
EOF
exit 0
REINJECT
chmod +x "$FABLE_DIR/reinject.sh"
echo "Wrote $FABLE_DIR/reinject.sh"

# --- write leak_test.py ---
cat > "$FABLE_DIR/leak_test.py" << 'LEAKTEST'
#!/usr/bin/env python3
"""
Fable-mode leak test — measures whether governed Opus is converging toward
Fable's behavioral signature using local Claude Code session logs.

Usage:
  python leak_test.py
  python leak_test.py --since 2026-06-17 --project myproject
  python leak_test.py --cap 20000
"""
import json, os, glob, argparse, statistics, sys, io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

CAVEAT = ["to be fair", "that said", "it's worth noting", "it's worth flagging",
          "i should flag", "i should note", "one caveat", "caveat:", "i could be wrong",
          "i might be wrong", "grain of salt", "for what it's worth", "to be clear",
          "honest caveat", "with the caveat", "i want to be careful", "honestly,"]
SELF_OPENERS = ("i'll", "let me", "i will", "let's", "i'm going to", "i can ", "i'd ", "i am going")

DEFAULT_CUTOFF = "2026-06-17"

def classify(model, ts, cutoff):
    m = str(model)
    if m.startswith("claude-fable-5"):
        return "fable"
    if m.startswith(("claude-opus-4-8", "claude-opus-4-7", "claude-opus-4-6")):
        return "opus_post" if (ts and ts[:10] >= cutoff) else "opus_pre"
    return None

def new_acc():
    return dict(n=0, prose=0, words=[], tool=0, text=0, caveat=0, selfopen=0)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default=DEFAULT_CUTOFF, help="governor cutoff date YYYY-MM-DD")
    ap.add_argument("--project", default=None, help="only scan project folders containing this substring")
    ap.add_argument("--cap", type=int, default=15000, help="max messages per bucket (runtime bound)")
    args = ap.parse_args()

    base = os.path.expanduser("~/.claude/projects")
    files = glob.glob(os.path.join(base, "*", "**", "*.jsonl"), recursive=True) + \
            glob.glob(os.path.join(base, "*", "*.jsonl"))
    files = sorted(set(files))
    if args.project:
        files = [f for f in files if args.project.lower() in f.lower()]

    B = {k: new_acc() for k in ("opus_pre", "opus_post", "fable")}
    for f in files:
        if all(B[k]["n"] >= args.cap for k in B):
            break
        try:
            fh = open(f, errors="ignore")
        except OSError:
            continue
        for line in fh:
            try:
                o = json.loads(line)
            except Exception:
                continue
            msg = o.get("message") or {}
            if msg.get("role") != "assistant":
                continue
            b = classify(msg.get("model", ""), o.get("timestamp", ""), args.since)
            if not b or B[b]["n"] >= args.cap:
                continue
            d = B[b]; d["n"] += 1
            c = msg.get("content"); text = ""
            if isinstance(c, str):
                text = c
            elif isinstance(c, list):
                for blk in c:
                    if not isinstance(blk, dict):
                        continue
                    t = blk.get("type")
                    if t == "text":
                        d["text"] += 1; text += blk.get("text", "")
                    elif t == "tool_use":
                        d["tool"] += 1
            if text.strip():
                d["prose"] += 1
                low = text.lower()
                d["words"].append(len(text.split()))
                if any(p in low for p in CAVEAT):
                    d["caveat"] += 1
                if low.lstrip().startswith(SELF_OPENERS):
                    d["selfopen"] += 1

    def med(w, p=50):
        if not w:
            return 0
        if p == 50:
            return int(statistics.median(w))
        return int(statistics.quantiles(w, n=100)[p - 1]) if len(w) > 1 else w[0]

    def metrics(d):
        prose = d["prose"] or 1
        return dict(
            msgs=d["n"], prose=d["prose"],
            p25=med(d["words"], 25), p50=med(d["words"], 50), p75=med(d["words"], 75),
            ttr=d["tool"] / (d["text"] or 1),
            cav=100 * d["caveat"] / prose,
            so=100 * d["selfopen"] / prose,
        )

    M = {k: metrics(v) for k, v in B.items()}
    pre, post, fab = M["opus_pre"], M["opus_post"], M["fable"]

    proj_note = f", project~={args.project}" if args.project else ""
    print(f"\n  Fable-mode leak test   (cutoff {args.since}{proj_note})")
    print("  " + "-" * 74)
    print(f"  {'metric':24}{'opus_pre':>12}{'opus_post':>12}{'FABLE(target)':>16}")
    print("  " + "-" * 74)
    print(f"  {'assistant msgs':24}{pre['msgs']:>12}{post['msgs']:>12}{fab['msgs']:>16}")
    print(f"  {'  w/ prose':24}{pre['prose']:>12}{post['prose']:>12}{fab['prose']:>16}")
    print(f"  {'median words/msg':24}{pre['p50']:>12}{post['p50']:>12}{fab['p50']:>16}")
    print(f"  {'  (p25 / p75)':24}{str(pre['p25'])+'/'+str(pre['p75']):>12}"
          f"{str(post['p25'])+'/'+str(post['p75']):>12}{str(fab['p25'])+'/'+str(fab['p75']):>16}")
    print(f"  {'tool:text ratio':24}{pre['ttr']:>12.2f}{post['ttr']:>12.2f}{fab['ttr']:>16.2f}")
    print(f"  {'unsolicited-caveat %':24}{pre['cav']:>12.1f}{post['cav']:>12.1f}{fab['cav']:>16.1f}")
    so_label = "I'll/Let me opener %"
    print(f"  {so_label:24}{pre['so']:>12.1f}{post['so']:>12.1f}{fab['so']:>16.1f}")
    print("  " + "-" * 74)

    INSUFF = post["prose"] < 30
    def arrow(pre_v, post_v, fab_v, lower_is_better):
        if INSUFF:
            return "—  (insufficient post-governor data; accumulates as you work)"
        toward = (post_v < pre_v) if lower_is_better else (post_v > pre_v)
        closed = abs(post_v - fab_v) < abs(pre_v - fab_v)
        mark = "✓ converging" if (toward and closed) else ("✗ not converging" if not toward else "~ moved, check")
        return f"{pre_v:.1f} → {post_v:.1f}  (target {fab_v:.1f})   {mark}"

    print("\n  VERDICT (is governed Opus moving toward Fable?)")
    print(f"    median words   {arrow(pre['p50'], post['p50'], fab['p50'], True)}")
    print(f"    tool:text      {arrow(pre['ttr'], post['ttr'], fab['ttr'], False)}")
    print(f"    caveat %       {arrow(pre['cav'], post['cav'], fab['cav'], True)}")
    print(f"    self-opener %  {arrow(pre['so'], post['so'], fab['so'], True)}")
    if INSUFF:
        print(f"\n  NOTE: only {post['prose']} governed prose msgs so far. Re-run after more"
              f" Opus work for a real verdict.")
    print()

if __name__ == "__main__":
    main()
LEAKTEST
chmod +x "$FABLE_DIR/leak_test.py"
echo "Wrote $FABLE_DIR/leak_test.py"

# --- patch settings.json ---
SETTINGS="$CLAUDE_DIR/settings.json"
if [[ ! -f "$SETTINGS" ]]; then
  echo '{}' > "$SETTINGS"
fi

if grep -q '"hooks"' "$SETTINGS"; then
  echo "WARNING: $SETTINGS already has a hooks block. Skipping patch."
  echo "Manually add this to hooks.UserPromptSubmit:"
  echo '  {"hooks":[{"type":"command","command":"bash ~/.claude/fable-mode/reinject.sh"}]}'
else
  SETTINGS_NODE="$SETTINGS"
  if command -v cygpath &>/dev/null; then
    SETTINGS_NODE="$(cygpath -w "$SETTINGS")"
  fi
  node -e "
    const fs = require('fs');
    const p = process.argv[1];
    const s = JSON.parse(fs.readFileSync(p, 'utf8'));
    s.hooks = s.hooks || {};
    s.hooks.UserPromptSubmit = [
      { hooks: [{ type: 'command', command: 'bash ~/.claude/fable-mode/reinject.sh' }] }
    ];
    fs.writeFileSync(p, JSON.stringify(s, null, 2) + '\n');
  " "$SETTINGS_NODE"
  echo "Patched $SETTINGS with UserPromptSubmit hook"
fi

fi  # end INSTALL_CLAUDE

# --- write Codex file ---
if [[ "$INSTALL_CODEX" == 1 ]]; then
  CODEX_BEGIN="<!-- BEGIN behavioral-baseline -->"
  CODEX_END="<!-- END behavioral-baseline -->"
  CODEX_BLOCK="$CODEX_BEGIN
$(emit_karpathy)
$CODEX_END"

  if [[ ! -f "$CODEX_DIR/AGENTS.md" ]]; then
    echo "$CODEX_BLOCK" > "$CODEX_DIR/AGENTS.md"
    echo "Created $CODEX_DIR/AGENTS.md (with managed section)"
  elif grep -qF "$CODEX_BEGIN" "$CODEX_DIR/AGENTS.md"; then
    awk -v begin="$CODEX_BEGIN" -v end="$CODEX_END" -v block="$CODEX_BLOCK" '
      $0 == begin { print block; skip=1; next }
      skip && $0 == end { skip=0; next }
      !skip { print }
    ' "$CODEX_DIR/AGENTS.md" > "$CODEX_DIR/AGENTS.md.tmp"
    mv "$CODEX_DIR/AGENTS.md.tmp" "$CODEX_DIR/AGENTS.md"
    echo "Updated managed section in $CODEX_DIR/AGENTS.md"
  else
    printf '\n%s\n' "$CODEX_BLOCK" >> "$CODEX_DIR/AGENTS.md"
    echo "Appended managed section to $CODEX_DIR/AGENTS.md"
  fi
fi

# --- summary ---
echo ""
echo "Done. Start a new session to activate."
if [[ "$INSTALL_CLAUDE" == 1 ]]; then
  echo "  Claude:  ~/.claude/CLAUDE.md + re-injection hook + leak_test.py"
  echo "  Disable output register temporarily:  export FABLE_MODE_OFF=1"
  echo "  Measure convergence:  python ~/.claude/fable-mode/leak_test.py"
else
  echo "  Claude:  ~/.claude not found — skipped (re-injection hook + leak_test are Claude-only)"
fi
if [[ "$INSTALL_CODEX" == 1 ]]; then
  echo "  Codex:   ~/.codex/AGENTS.md (Karpathy 12 rules only)"
else
  echo "  Codex:   ~/.codex not found — skipped"
fi
