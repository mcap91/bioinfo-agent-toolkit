#!/bin/bash
set -euo pipefail

# phoam_paint (kb-graph) — Uninstaller
# Removes ~/.local/bin/kb-graph
# Does NOT touch any project — run `kb-graph uninit .` first on each project

DST="$HOME/.local/bin/kb-graph"

# Colors
GREEN='\033[32m'
YELLOW='\033[33m'
CYAN='\033[36m'
RESET='\033[0m'

info()  { printf "${CYAN}[info]${RESET}  %s\n" "$1"; }
ok()    { printf "${GREEN}[ok]${RESET}    %s\n" "$1"; }
warn()  { printf "${YELLOW}[warn]${RESET}  %s\n" "$1"; }

# --- Remove binary ---

if [ -f "$DST" ]; then
    rm "$DST"
    ok "Removed $DST"
else
    warn "kb-graph not found at $DST (already removed?)"
fi

# --- Done ---

echo ""
info "kb-graph has been removed from your system."
info "Note: This does not remove kb-graph artifacts from any project."
info "Run 'kb-graph uninit .' in each project first if you want a full clean removal."
echo ""
