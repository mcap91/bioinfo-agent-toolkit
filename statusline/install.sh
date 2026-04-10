#!/bin/bash
set -euo pipefail

# Claude Code Status Line — Installer
# Copies the statusline script to ~/.claude/ and configures settings.json

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
SETTINGS_FILE="$CLAUDE_DIR/settings.json"
SCRIPT_SRC="$SCRIPT_DIR/statusline.sh"
SCRIPT_DST="$CLAUDE_DIR/statusline.sh"

# Colors for installer output
RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
CYAN='\033[36m'
RESET='\033[0m'

info()  { printf "${CYAN}[info]${RESET}  %s\n" "$1"; }
ok()    { printf "${GREEN}[ok]${RESET}    %s\n" "$1"; }
warn()  { printf "${YELLOW}[warn]${RESET}  %s\n" "$1"; }
err()   { printf "${RED}[error]${RESET} %s\n" "$1" >&2; exit 1; }

# --- Preflight checks ---

command -v jq >/dev/null 2>&1 || err "jq is required but not installed. Install it with: sudo apt install jq (or brew install jq)"

[ -f "$SCRIPT_SRC" ] || err "statusline.sh not found at $SCRIPT_SRC — run this script from the repo"

# --- Install script ---

mkdir -p "$CLAUDE_DIR"

if [ -f "$SCRIPT_DST" ]; then
    if cmp -s "$SCRIPT_SRC" "$SCRIPT_DST"; then
        ok "statusline.sh already installed and up to date"
    else
        cp "$SCRIPT_SRC" "$SCRIPT_DST"
        ok "statusline.sh updated"
    fi
else
    cp "$SCRIPT_SRC" "$SCRIPT_DST"
    ok "statusline.sh installed to $SCRIPT_DST"
fi

chmod +x "$SCRIPT_DST"

# --- Configure settings.json ---

STATUS_LINE_CONFIG='{"type":"command","command":"bash ~/.claude/statusline.sh"}'

if [ -f "$SETTINGS_FILE" ]; then
    # Check if statusLine is already configured
    existing=$(jq -r '.statusLine.command // empty' "$SETTINGS_FILE" 2>/dev/null)
    if [ "$existing" = "bash ~/.claude/statusline.sh" ]; then
        ok "settings.json already configured"
    else
        # Merge statusLine into existing settings, preserving all other keys
        tmp=$(mktemp)
        jq --argjson sl "$STATUS_LINE_CONFIG" '.statusLine = $sl' "$SETTINGS_FILE" > "$tmp"
        mv "$tmp" "$SETTINGS_FILE"
        ok "statusLine added to $SETTINGS_FILE"
    fi
else
    # Create new settings file
    printf '{\n  "statusLine": {\n    "type": "command",\n    "command": "bash ~/.claude/statusline.sh"\n  }\n}\n' > "$SETTINGS_FILE"
    ok "Created $SETTINGS_FILE with statusLine config"
fi

# --- Done ---

echo ""
info "Restart Claude Code (or start a new session) to see the status line."
info "It will appear after the first assistant message."
echo ""
printf "  ${CYAN}Opus 4.6${RESET} | Context: [▓▓▓▓░░░░░░░░░░░░░░░░] ${YELLOW}18.3%%${RESET} | Tokens: ${GREEN}183421${RESET}/${GREEN}1000000${RESET}\n"
echo ""
