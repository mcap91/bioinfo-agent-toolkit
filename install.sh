#!/bin/bash
set -euo pipefail

# bioinf-agent-toolkit — Installer
# Usage:
#   ./install.sh --list                              Show available components
#   ./install.sh handoff statusline                  Install to current directory
#   ./install.sh handoff --project ~/projects/my-app Install skills to a specific project
#   ./install.sh --all                               Install everything
#
# Skills (directories under skills/ with a SKILL.md) are copied directly by
# this script. Tools with custom install logic (their own install.sh) are
# delegated to that script.

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
CYAN='\033[36m'
BOLD='\033[1m'
RESET='\033[0m'

err()  { printf "${RED}[error]${RESET} %s\n" "$1" >&2; exit 1; }
ok()   { printf "${GREEN}[ok]${RESET}    %s\n" "$1"; }
info() { printf "${CYAN}[info]${RESET}  %s\n" "$1"; }

# Find all installable components:
#   - skills/ subdirectories containing a SKILL.md
#   - any other directory with its own install.sh
find_components() {
    {
        # Skills (SKILL.md in skills/<name>/)
        find "$REPO_DIR/skills" -mindepth 2 -maxdepth 2 -name "SKILL.md" 2>/dev/null | while read -r f; do
            basename "$(dirname "$f")"
        done

        # Tools with custom install.sh (exclude skills/ — handled above)
        find "$REPO_DIR" -mindepth 2 -maxdepth 2 -name "install.sh" \
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

    # Check for a directory with its own install.sh
    local found=""
    while IFS= read -r script; do
        dir="$(dirname "$script")"
        if [ "$(basename "$dir")" = "$name" ]; then
            found="$dir"
            break
        fi
    done < <(find "$REPO_DIR" -mindepth 2 -maxdepth 2 -name "install.sh" \
        -not -path "*/skills/*" -not -path "*/.git/*")
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
    component_dir=$(resolve_component_dir "$name")
    if [ -z "$component_dir" ]; then
        printf "${RED}[error]${RESET} Unknown component: %s\n" "$name"
        failed=1
        continue
    fi

    printf "${BOLD}Installing %s...${RESET}\n" "$name"

    if [ -f "$component_dir/install.sh" ]; then
        # Tool with custom install logic — delegate
        PROJECT_DIR="$PROJECT_DIR" bash "$component_dir/install.sh"
    elif [ -f "$component_dir/SKILL.md" ]; then
        # Skill — standard copy to project's .claude/skills/
        dst="$PROJECT_DIR/.claude/skills/$name/SKILL.md"
        mkdir -p "$(dirname "$dst")"
        if [ -f "$dst" ]; then
            if cmp -s "$component_dir/SKILL.md" "$dst"; then
                ok "$name skill already installed and up to date"
            else
                cp "$component_dir/SKILL.md" "$dst"
                ok "$name skill updated"
            fi
        else
            cp "$component_dir/SKILL.md" "$dst"
            ok "$name skill installed to $dst"
        fi
        info "/$name is now available in $PROJECT_DIR"
    fi
    echo ""
done

if [ $failed -ne 0 ]; then
    info "Some components failed. Run ./install.sh --list to see available components."
    exit 1
fi
