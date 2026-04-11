#!/bin/bash
set -euo pipefail

# bioinf-agent-toolkit — Installer
# Usage:
#   ./install.sh --list                              Show available components
#   ./install.sh handoff statusline                  Install to current directory
#   ./install.sh handoff --project ~/projects/my-app Install skills to a specific project
#   ./install.sh --all                               Install everything

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
CYAN='\033[36m'
BOLD='\033[1m'
RESET='\033[0m'

err()  { printf "${RED}[error]${RESET} %s\n" "$1" >&2; exit 1; }
info() { printf "${CYAN}[info]${RESET}  %s\n" "$1"; }

# Find all installable components (any directory with an install.sh)
find_components() {
    find "$REPO_DIR" -mindepth 2 -name "install.sh" -not -path "*/.git/*" | while read -r script; do
        dir="$(dirname "$script")"
        basename "$dir"
    done | sort
}

# Resolve a component name to its install.sh path
resolve_component() {
    local name="$1"
    local found=""
    while IFS= read -r script; do
        dir="$(dirname "$script")"
        if [ "$(basename "$dir")" = "$name" ]; then
            found="$script"
            break
        fi
    done < <(find "$REPO_DIR" -mindepth 2 -name "install.sh" -not -path "*/.git/*")
    echo "$found"
}

# --- Parse arguments ---

PROJECT_DIR=""
components=()
show_list=false
install_all=false

while [ $# -gt 0 ]; do
    case "$1" in
        --project)
            [ $# -ge 2 ] || err "--project requires a path argument"
            PROJECT_DIR="$(cd "$2" 2>/dev/null && pwd)" || err "Directory not found: $2"
            shift 2
            ;;
        --list)
            show_list=true
            shift
            ;;
        --all)
            install_all=true
            shift
            ;;
        --help|-h)
            echo ""
            printf "${BOLD}bioinf-agent-toolkit installer${RESET}\n"
            echo ""
            echo "Usage:"
            echo "  ./install.sh --list                          Show available components"
            echo "  ./install.sh handoff statusline              Install components"
            echo "  ./install.sh handoff --project ~/my-app      Install skills into a specific project"
            echo "  ./install.sh --all                           Install everything"
            echo ""
            echo "Skills install into the project's .claude/skills/ directory."
            echo "Tools (like statusline) install into ~/.claude/ (user-global)."
            echo ""
            echo "Options:"
            echo "  --project <path>   Target project for skills (default: current directory)"
            echo "  --list             Show available components"
            echo "  --all              Install all components"
            echo ""
            exit 0
            ;;
        *)
            components+=("$1")
            shift
            ;;
    esac
done

# Default project dir to current working directory
: "${PROJECT_DIR:=$(pwd)}"

if $show_list; then
    echo ""
    printf "${BOLD}Available components:${RESET}\n"
    echo ""
    for name in $(find_components); do
        printf "  %s\n" "$name"
    done
    echo ""
    echo "Install with: ./install.sh <name> [<name> ...]"
    echo ""
    exit 0
fi

if $install_all; then
    while IFS= read -r name; do
        components+=("$name")
    done < <(find_components)
fi

if [ ${#components[@]} -eq 0 ]; then
    err "No components specified. Run ./install.sh --list to see available components."
fi

# --- Install components ---

echo ""
info "Project directory: $PROJECT_DIR"
echo ""

failed=0
for name in "${components[@]}"; do
    script=$(resolve_component "$name")
    if [ -z "$script" ]; then
        printf "${RED}[error]${RESET} Unknown component: %s\n" "$name"
        failed=1
        continue
    fi
    printf "${BOLD}Installing %s...${RESET}\n" "$name"
    PROJECT_DIR="$PROJECT_DIR" bash "$script"
    echo ""
done

if [ $failed -ne 0 ]; then
    info "Some components failed. Run ./install.sh --list to see available components."
    exit 1
fi
