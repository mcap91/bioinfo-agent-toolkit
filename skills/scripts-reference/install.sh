#!/bin/bash
set -euo pipefail

# Scripts Reference Skill — Installer
# Copies SKILL.md into the target project's .claude/skills/scripts-reference/
# Receives PROJECT_DIR from the top-level install.sh (defaults to pwd)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_SRC="$SCRIPT_DIR/SKILL.md"

: "${PROJECT_DIR:=$(pwd)}"
SKILL_DST="$PROJECT_DIR/.claude/skills/scripts-reference/SKILL.md"

GREEN='\033[32m'
CYAN='\033[36m'
RED='\033[31m'
RESET='\033[0m'

ok()   { printf "${GREEN}[ok]${RESET}    %s\n" "$1"; }
info() { printf "${CYAN}[info]${RESET}  %s\n" "$1"; }
err()  { printf "${RED}[error]${RESET} %s\n" "$1" >&2; exit 1; }

[ -f "$SKILL_SRC" ] || err "SKILL.md not found at $SKILL_SRC — run this script from the repo"

mkdir -p "$(dirname "$SKILL_DST")"

if [ -f "$SKILL_DST" ]; then
    if cmp -s "$SKILL_SRC" "$SKILL_DST"; then
        ok "scripts-reference skill already installed and up to date"
    else
        cp "$SKILL_SRC" "$SKILL_DST"
        ok "scripts-reference skill updated"
    fi
else
    cp "$SKILL_SRC" "$SKILL_DST"
    ok "scripts-reference skill installed to $SKILL_DST"
fi

info "/scripts-reference is now available in $PROJECT_DIR"
