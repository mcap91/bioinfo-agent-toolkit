#!/bin/bash
set -euo pipefail

# phoam_paint (kb-graph) — Installer
# Copies kb_graph.py to ~/.local/bin/kb-graph and makes it executable

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="$SCRIPT_DIR/kb_graph.py"
DST="$HOME/.local/bin/kb-graph"

# Colors for installer output
GREEN='\033[32m'
YELLOW='\033[33m'
CYAN='\033[36m'
RED='\033[31m'
RESET='\033[0m'

info()  { printf "${CYAN}[info]${RESET}  %s\n" "$1"; }
ok()    { printf "${GREEN}[ok]${RESET}    %s\n" "$1"; }
warn()  { printf "${YELLOW}[warn]${RESET}  %s\n" "$1"; }
err()   { printf "${RED}[error]${RESET} %s\n" "$1" >&2; exit 1; }

# --- Preflight checks ---

[ -f "$SRC" ] || err "kb_graph.py not found at $SRC — run this script from the repo"

# --- Install ---

mkdir -p "$HOME/.local/bin"

if [ -f "$DST" ]; then
    if cmp -s "$SRC" "$DST"; then
        ok "kb-graph already installed and up to date"
    else
        cp "$SRC" "$DST"
        ok "kb-graph updated"
    fi
else
    cp "$SRC" "$DST"
    ok "kb-graph installed to $DST"
fi

chmod +x "$DST"

# --- Verify PATH ---

if ! echo "$PATH" | tr ':' '\n' | grep -qx "$HOME/.local/bin"; then
    warn "$HOME/.local/bin is not on your PATH"
    info "Add this to your shell profile:  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

# --- Done ---

echo ""
info "Usage: kb-graph init /path/to/repo"
echo ""
