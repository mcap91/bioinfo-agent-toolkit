#!/bin/bash
set -euo pipefail

# Claude Code Status Line — Uninstaller
# Removes the statusline script and the statusLine key from settings.json
# Does not remove settings.json itself or any other keys in it

CLAUDE_DIR="$HOME/.claude"
SETTINGS_FILE="$CLAUDE_DIR/settings.json"
SCRIPT_DST="$CLAUDE_DIR/statusline.sh"

# Colors
GREEN='\033[32m'
YELLOW='\033[33m'
CYAN='\033[36m'
RESET='\033[0m'

info()  { printf "${CYAN}[info]${RESET}  %s\n" "$1"; }
ok()    { printf "${GREEN}[ok]${RESET}    %s\n" "$1"; }
warn()  { printf "${YELLOW}[warn]${RESET}  %s\n" "$1"; }

# --- Remove script ---

if [ -f "$SCRIPT_DST" ]; then
    rm "$SCRIPT_DST"
    ok "Removed $SCRIPT_DST"
else
    warn "statusline.sh not found at $SCRIPT_DST (already removed?)"
fi

# --- Remove statusLine key from settings.json ---

if [ -f "$SETTINGS_FILE" ]; then
    if command -v jq >/dev/null 2>&1; then
        has_key=$(jq 'has("statusLine")' "$SETTINGS_FILE" 2>/dev/null || echo "false")
        if [ "$has_key" = "true" ]; then
            tmp=$(mktemp)
            jq 'del(.statusLine)' "$SETTINGS_FILE" > "$tmp"
            mv "$tmp" "$SETTINGS_FILE"
            ok "Removed statusLine from $SETTINGS_FILE"
        else
            warn "No statusLine key in $SETTINGS_FILE (already removed?)"
        fi
    else
        warn "jq not found — could not clean settings.json automatically"
        info "Manually remove the \"statusLine\" block from $SETTINGS_FILE"
    fi
else
    warn "No settings.json found at $SETTINGS_FILE"
fi

# --- Done ---

echo ""
info "Restart Claude Code to apply. The status bar will no longer appear."
echo ""
