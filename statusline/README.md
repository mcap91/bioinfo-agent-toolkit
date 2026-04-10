# Claude Code Status Line

A persistent status bar for the Claude Code CLI that shows model name, context window usage, and token counts in real time.

```
Opus 4.6 | Context: [▓▓▓▓░░░░░░░░░░░░░░░░] 18.3% | Tokens: 183421/1000000
```

- **Model name** in cyan
- **Progress bar** with Unicode block characters (20 chars wide)
- **Percentage** in yellow
- **Token counts** in green

## Why

Context window exhaustion triggers automatic conversation compression, which can lose important details. This bar gives you immediate visibility into how much context you've consumed so you can decide when to start fresh.

## Install

### Quick install (from this repo)

```bash
git clone https://github.com/mcap91/bioinf-agent-toolkit.git
cd bioinf-agent-toolkit
./statusline/install.sh
```

### Quick install (standalone)

```bash
curl -fsSL https://raw.githubusercontent.com/mcap91/bioinf-agent-toolkit/main/statusline/statusline.sh -o ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh
```

Then add to `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/statusline.sh"
  }
}
```

### Prerequisites

- [jq](https://jqlang.github.io/jq/) (`sudo apt install jq` / `brew install jq`)
- A terminal with ANSI color and Unicode support (most modern terminals)

## How it works

Claude Code pipes a JSON blob to the script's stdin after each assistant message. The script:

1. Extracts model name and context window size via `jq`
2. Sums all token categories (input, output, cache creation, cache read) for true context occupancy
3. Computes a percentage and renders a 20-character progress bar
4. Outputs a colored string that Claude Code displays as the status line

## Customization

Edit `~/.claude/statusline.sh` to add more fields. The full JSON schema is documented in [`docs/claude_code_statusline_spec.md`](../docs/claude_code_statusline_spec.md).

**Add cost tracking:**
```bash
cost=$(echo "$input" | jq -r '.cost.total_cost_usd // 0' | xargs printf "%.4f")
# Append to printf: | Cost: $X.XXXX
```

**Color the bar by usage level:**
```bash
if (( $(echo "$used > 80" | bc -l) )); then
    bar_color="\033[31m"   # Red above 80%
elif (( $(echo "$used > 50" | bc -l) )); then
    bar_color="\033[33m"   # Yellow above 50%
else
    bar_color="\033[32m"   # Green below 50%
fi
```

## Uninstall

```bash
rm ~/.claude/statusline.sh
```

Then remove the `"statusLine"` block from `~/.claude/settings.json`.
