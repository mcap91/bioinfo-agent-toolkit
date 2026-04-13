#!/bin/bash
set -euo pipefail

# plan-me-this Skill — Uninstaller
# Removes the skill from the target project's .claude/skills/plan-me-this/
# Receives PROJECT_DIR from the top-level uninstall.sh (defaults to pwd)

: "${PROJECT_DIR:=$(pwd)}"
SKILL_DIR="$PROJECT_DIR/.claude/skills/plan-me-this"

GREEN='\033[32m'
YELLOW='\033[33m'
CYAN='\033[36m'
RESET='\033[0m'

ok()   { printf "${GREEN}[ok]${RESET}    %s\n" "$1"; }
warn() { printf "${YELLOW}[warn]${RESET}  %s\n" "$1"; }
info() { printf "${CYAN}[info]${RESET}  %s\n" "$1"; }

if [ -d "$SKILL_DIR" ]; then
    rm -rf "$SKILL_DIR"
    ok "Removed $SKILL_DIR"
else
    warn "plan-me-this skill not found at $SKILL_DIR (already removed?)"
fi

info "/plan-me-this removed from $PROJECT_DIR"
