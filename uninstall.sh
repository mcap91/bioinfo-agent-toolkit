#!/bin/bash
set -euo pipefail

# bioinf-agent-toolkit — Uninstaller
# Usage:
#   ./uninstall.sh handoff statusline              Uninstall from current directory
#   ./uninstall.sh handoff --project ~/my-app      Uninstall skills from a specific project
#
# Skills are removed directly by this script. Tools with custom uninstall
# logic (their own uninstall.sh) are delegated to that script.
# Components must be named explicitly — no --all flag (too dangerous with
# mixed project/global components).

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
CYAN='\033[36m'
BOLD='\033[1m'
RESET='\033[0m'

err()  { printf "${RED}[error]${RESET} %s\n" "$1" >&2; exit 1; }
ok()   { printf "${GREEN}[ok]${RESET}    %s\n" "$1"; }
warn() { printf "${YELLOW}[warn]${RESET}  %s\n" "$1"; }
info() { printf "${CYAN}[info]${RESET}  %s\n" "$1"; }

# Find all uninstallable components (same discovery as install.sh)
find_components() {
    {
        # Skills (SKILL.md in skills/<name>/)
        find "$REPO_DIR/skills" -mindepth 2 -maxdepth 2 -name "SKILL.md" 2>/dev/null | while read -r f; do
            basename "$(dirname "$f")"
        done

        # Tools with custom uninstall.sh (exclude skills/)
        find "$REPO_DIR" -mindepth 2 -maxdepth 2 -name "uninstall.sh" \
            -not -path "*/skills/*" -not -path "*/.git/*" | while read -r script; do
            basename "$(dirname "$script")"
        done
    } | sort -u
}

# Resolve a component name to its directory
resolve_component_dir() {
    local name="$1"

    # Check skills/ first
    if [ -f "$REPO_DIR/skills/$name/SKILL.md" ]; then
        echo "$REPO_DIR/skills/$name"
        return
    fi

    # Check for a directory with its own uninstall.sh
    local found=""
    while IFS= read -r script; do
        dir="$(dirname "$script")"
        if [ "$(basename "$dir")" = "$name" ]; then
            found="$dir"
            break
        fi
    done < <(find "$REPO_DIR" -mindepth 2 -maxdepth 2 -name "uninstall.sh" \
        -not -path "*/skills/*" -not -path "*/.git/*")
    echo "$found"
}

# --- Parse arguments ---

PROJECT_DIR=""
components=()

while [ $# -gt 0 ]; do
    case "$1" in
        --project)
            [ $# -ge 2 ] || err "--project requires a path argument"
            PROJECT_DIR="$(cd "$2" 2>/dev/null && pwd)" || err "Directory not found: $2"
            shift 2
            ;;
        --help|-h)
            echo ""
            printf "${BOLD}bioinf-agent-toolkit uninstaller${RESET}\n"
            echo ""
            echo "Usage:"
            echo "  ./uninstall.sh handoff statusline              Uninstall components"
            echo "  ./uninstall.sh handoff --project ~/my-app      Uninstall skills from a specific project"
            echo ""
            echo "Options:"
            echo "  --project <path>   Target project for skills (default: current directory)"
            echo ""
            echo "Available components:"
            for name in $(find_components); do
                printf "  %s\n" "$name"
            done
            echo ""
            exit 0
            ;;
        *)
            components+=("$1")
            shift
            ;;
    esac
done

: "${PROJECT_DIR:=$(pwd)}"

if [ ${#components[@]} -eq 0 ]; then
    err "No components specified. Run ./uninstall.sh --help to see available components."
fi

# --- Uninstall components ---

echo ""
info "Project directory: $PROJECT_DIR"
echo ""

failed=0
for name in "${components[@]}"; do
    component_dir=$(resolve_component_dir "$name")
    if [ -z "$component_dir" ]; then
        printf "${RED}[error]${RESET} Unknown component: %s\n" "$name"
        failed=1
        continue
    fi

    printf "${BOLD}Uninstalling %s...${RESET}\n" "$name"

    if [ -f "$component_dir/uninstall.sh" ]; then
        # Tool with custom uninstall logic — delegate
        PROJECT_DIR="$PROJECT_DIR" bash "$component_dir/uninstall.sh"
    elif [ -f "$component_dir/SKILL.md" ]; then
        # Skill — remove from project's .claude/skills/
        skill_dir="$PROJECT_DIR/.claude/skills/$name"
        if [ -d "$skill_dir" ]; then
            rm -rf "$skill_dir"
            ok "Removed $skill_dir"
        else
            warn "$name skill not found at $skill_dir (already removed?)"
        fi
        info "/$name removed from $PROJECT_DIR"
    fi
    echo ""
done

if [ $failed -ne 0 ]; then
    info "Some components failed. Available: $(find_components | tr '\n' ' ')"
    exit 1
fi
