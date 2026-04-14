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

# --- Find jq ---

find_jq() {
    # 1. Already on PATH — works on Linux, macOS, and Windows if configured
    if command -v jq >/dev/null 2>&1; then
        command -v jq
        return 0
    fi

    # 2. Windows: check common package manager install locations
    if [[ "$OSTYPE" == msys* || "$OSTYPE" == cygwin* || "$OSTYPE" == mingw* ]]; then
        local local_appdata="${LOCALAPPDATA:-$USERPROFILE/AppData/Local}"
        local program_data="${PROGRAMDATA:-/c/ProgramData}"
        local win_locations=(
            # winget
            "$local_appdata/Microsoft/WinGet/Packages"/jqlang.jq_*/jq.exe
            # chocolatey
            "$program_data/chocolatey/bin/jq.exe"
            # scoop
            "${USERPROFILE:-$HOME}/scoop/shims/jq.exe"
        )
        for loc in "${win_locations[@]}"; do
            # glob may expand to multiple matches — take the first
            for match in $loc; do
                if [ -f "$match" ]; then
                    echo "$match"
                    return 0
                fi
            done
        done
    fi

    return 1
}

JQ_PATH=$(find_jq) || err "jq is required but not found.
  Install it:
    macOS:   brew install jq
    Linux:   sudo apt install jq  (or yum, pacman, etc.)
    Windows: winget install jqlang.jq
  Then re-run this installer."

info "Using jq at: $JQ_PATH"

# --- Preflight checks ---

[ -f "$SCRIPT_SRC" ] || err "statusline.sh not found at $SCRIPT_SRC — run this script from the repo"

# --- Install script ---

mkdir -p "$CLAUDE_DIR"

# Copy statusline.sh, embedding the resolved jq path if it's not simply "jq"
if command -v jq >/dev/null 2>&1; then
    # jq is on PATH — use the generic default (JQ="${JQ:-jq}")
    cp "$SCRIPT_SRC" "$SCRIPT_DST"
else
    # jq found but not on PATH — embed the full path into the installed copy
    # Escape backslashes (Windows paths) so sed doesn't mangle them
    escaped_jq=$(printf '%s' "$JQ_PATH" | sed 's/\\/\\\\/g')
    sed "s|^JQ=\"\${JQ:-jq}\"|JQ=\"$escaped_jq\"|" "$SCRIPT_SRC" > "$SCRIPT_DST"
    warn "jq is not on shell PATH — embedded full path into statusline.sh"
fi

ok "statusline.sh installed to $SCRIPT_DST"
chmod +x "$SCRIPT_DST"

# --- Configure settings.json ---

STATUS_LINE_CONFIG='{"type":"command","command":"bash ~/.claude/statusline.sh"}'

if [ -f "$SETTINGS_FILE" ]; then
    # Check if statusLine is already configured
    existing=$("$JQ_PATH" -r '.statusLine.command // empty' "$SETTINGS_FILE" 2>/dev/null)
    if [ "$existing" = "bash ~/.claude/statusline.sh" ]; then
        ok "settings.json already configured"
    else
        # Merge statusLine into existing settings, preserving all other keys
        tmp=$(mktemp)
        "$JQ_PATH" --argjson sl "$STATUS_LINE_CONFIG" '.statusLine = $sl' "$SETTINGS_FILE" > "$tmp"
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
