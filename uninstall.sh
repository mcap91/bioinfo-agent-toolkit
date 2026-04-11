#!/bin/bash
set -euo pipefail

# bioinf-agent-toolkit — Uninstaller
# Usage:
#   ./uninstall.sh handoff statusline              Uninstall from current directory
#   ./uninstall.sh handoff --project ~/my-app      Uninstall skills from a specific project
#   ./uninstall.sh --all                           Uninstall everything

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

RED='\033[31m'
CYAN='\033[36m'
BOLD='\033[1m'
RESET='\033[0m'

err()  { printf "${RED}[error]${RESET} %s\n" "$1" >&2; exit 1; }
info() { printf "${CYAN}[info]${RESET}  %s\n" "$1"; }

# Find all uninstallable components
find_components() {
    find "$REPO_DIR" -mindepth 2 -name "uninstall.sh" -not -path "*/.git/*" | while read -r script; do
        dir="$(dirname "$script")"
        basename "$dir"
    done | sort
}

# Resolve a component name to its uninstall.sh path
resolve_component() {
    local name="$1"
    local found=""
    while IFS= read -r script; do
        dir="$(dirname "$script")"
        if [ "$(basename "$dir")" = "$name" ]; then
            found="$script"
            break
        fi
    done < <(find "$REPO_DIR" -mindepth 2 -name "uninstall.sh" -not -path "*/.git/*")
    echo "$found"
}

# --- Parse arguments ---

PROJECT_DIR=""
components=()
uninstall_all=false

while [ $# -gt 0 ]; do
    case "$1" in
        --project)
            [ $# -ge 2 ] || err "--project requires a path argument"
            PROJECT_DIR="$(cd "$2" 2>/dev/null && pwd)" || err "Directory not found: $2"
            shift 2
            ;;
        --all)
            uninstall_all=true
            shift
            ;;
        --help|-h)
            echo ""
            printf "${BOLD}bioinf-agent-toolkit uninstaller${RESET}\n"
            echo ""
            echo "Usage:"
            echo "  ./uninstall.sh handoff statusline              Uninstall components"
            echo "  ./uninstall.sh handoff --project ~/my-app      Uninstall skills from a specific project"
            echo "  ./uninstall.sh --all                           Uninstall everything"
            echo ""
            echo "Options:"
            echo "  --project <path>   Target project for skills (default: current directory)"
            echo "  --all              Uninstall all components"
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

if $uninstall_all; then
    while IFS= read -r name; do
        components+=("$name")
    done < <(find_components)
fi

if [ ${#components[@]} -eq 0 ]; then
    err "No components specified. Usage: ./uninstall.sh <name> [<name> ...]"
fi

# --- Uninstall components ---

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
    printf "${BOLD}Uninstalling %s...${RESET}\n" "$name"
    PROJECT_DIR="$PROJECT_DIR" bash "$script"
    echo ""
done

if [ $failed -ne 0 ]; then
    info "Some components failed. Available: $(find_components | tr '\n' ' ')"
    exit 1
fi
