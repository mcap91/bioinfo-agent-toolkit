# /plan-me-this Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the `/plan-me-this` Claude Code skill — a plan packager that breaks an approved spec into self-contained phase docs and a living `readme_this_current_task.md`.

**Architecture:** A single SKILL.md defines the agent workflow (7 steps: read spec, propose phases, generate phase docs, generate open_issues.md, generate readme_this_current_task.md, fidelity check, present result). install.sh and uninstall.sh handle project-level installation following the existing handoff skill pattern.

**Tech Stack:** Bash (installers), Markdown with YAML frontmatter (SKILL.md)

**Spec:** `docs/plan-me-this-spec.md`

---

### Task 1: Create install.sh

**Files:**
- Create: `skills/plan-me-this/install.sh`
- Reference: `skills/handoff/install.sh` (template to follow)

- [ ] **Step 1: Create the installer script**

```bash
#!/bin/bash
set -euo pipefail

# plan-me-this Skill — Installer
# Copies SKILL.md into the target project's .claude/skills/plan-me-this/
# Receives PROJECT_DIR from the top-level install.sh (defaults to pwd)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_SRC="$SCRIPT_DIR/SKILL.md"

: "${PROJECT_DIR:=$(pwd)}"
SKILL_DST="$PROJECT_DIR/.claude/skills/plan-me-this/SKILL.md"

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
        ok "plan-me-this skill already installed and up to date"
    else
        cp "$SKILL_SRC" "$SKILL_DST"
        ok "plan-me-this skill updated"
    fi
else
    cp "$SKILL_SRC" "$SKILL_DST"
    ok "plan-me-this skill installed to $SKILL_DST"
fi

info "/plan-me-this is now available in $PROJECT_DIR"
```

- [ ] **Step 2: Make it executable**

Run: `chmod +x skills/plan-me-this/install.sh`

- [ ] **Step 3: Verify the top-level installer discovers it**

Run: `./install.sh --list`
Expected: `plan-me-this` appears in the list alongside `handoff` and `statusline`

- [ ] **Step 4: Commit**

```bash
git add skills/plan-me-this/install.sh
git commit -m "feat: add plan-me-this installer"
```

---

### Task 2: Create uninstall.sh

**Files:**
- Create: `skills/plan-me-this/uninstall.sh`
- Reference: `skills/handoff/uninstall.sh` (template to follow)

- [ ] **Step 1: Create the uninstaller script**

```bash
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
```

- [ ] **Step 2: Make it executable**

Run: `chmod +x skills/plan-me-this/uninstall.sh`

- [ ] **Step 3: Verify the top-level uninstaller discovers it**

Run: `./uninstall.sh --list`
Expected: `plan-me-this` appears in the list

- [ ] **Step 4: Commit**

```bash
git add skills/plan-me-this/uninstall.sh
git commit -m "feat: add plan-me-this uninstaller"
```

---

### Task 3: Create SKILL.md

This is the core deliverable — the skill definition that tells the agent what to do when a user invokes `/plan-me-this`.

**Files:**
- Create: `skills/plan-me-this/SKILL.md`
- Reference: `skills/handoff/SKILL.md` (frontmatter format)
- Reference: `docs/plan-me-this-spec.md` (spec — sections 5, 6, 7, 8)

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: plan-me-this
description: Package an approved spec into self-contained phase docs and a living readme_this_current_task.md. Use when the user says "/plan-me-this", has a plan or spec ready to break into phases, or wants to set up a multi-session task package. Takes a spec file path and optional output directory.
---

# Plan Me This

Package an approved spec into self-contained phase docs and a living handoff
document (`readme_this_current_task.md`). This is a plan packager — it does
not plan for you. The input is a spec the user has already discussed and
approved.

## Invocation

Parse the arguments after `/plan-me-this`:

| Argument | Required | Description |
|---|---|---|
| Spec file path | Yes | Path to the approved plan, spec, or notes |
| Output directory | No | Where to write output. Defaults to the spec file's parent directory |

## Workflow

### 1. Read the spec

Read the input file. Understand what needs to be built — goals, constraints,
design decisions, technical details. Do not skim — read the entire document.
You need to fully understand the content to rewrite it faithfully.

### 2. Propose phase breakdown

The spec may or may not contain explicit phases. Either way, analyze the full
scope of work and propose a breakdown into manageable phases. Present as a
numbered list with one-line descriptions:

> "Here's how I'd break this into phases:
> 1. Core engine — file discovery, parsers, graph data structure, output
> 2. Mutation tests — verify rebuild detects changes
> 3. Query commands — neighbors, traverse, path, orphans, analyze
> ..."

Each phase should be:
- **Self-contained** — an agent can complete it in one session without
  needing context from other phases beyond what the phase doc provides
- **Sequentially buildable** — each phase builds on what prior phases
  produced
- **Verifiable** — there's a concrete way to confirm the phase is done

**Wait for user approval or adjustment before proceeding.**

### 3. Generate phase docs

For each approved phase, write a self-contained document to the output
directory as `phase-N-{slug}.md` (e.g., `phase-1-core-engine.md`).

An agent reading **only** that file must have everything it needs to work.
Each phase doc contains:

- **Goal** — one or two sentences: what this phase produces when complete
- **Context** — what prior phases built that this phase depends on. Include
  key file paths, data structures, interfaces, and commands the agent needs
  to know about. For Phase 1, this is project-level context instead.
- **Tasks** — what to build, with enough detail to implement. Include file
  paths, expected behaviors, edge cases, and technical specifics from the
  spec. Do not water down the spec's detail — preserve it.
- **Verification** — how to confirm the phase is complete. Exact commands
  to run and expected output where possible.
- **Scope boundary** — what NOT to touch. Name specific later-phase work
  that an eager agent might be tempted to start.

**Do not reference other phase docs.** Each phase doc stands alone. If a
phase needs to know what Phase 1 built, describe it directly — don't say
"see phase-1-core-engine.md."

### 4. Generate `open_issues.md`

Scan the spec for TBDs, open questions, unresolved notes, deferred decisions,
or anything marked as uncertain. Extract them into `open_issues.md` in the
output directory.

If there are no open issues, **skip this file entirely** — do not create an
empty one.

### 5. Generate `readme_this_current_task.md`

Write the bridge document to the output directory. This is the one file every
agent reads first when picking up this project cold. It contains:

**What this is** — 2-3 sentences describing the project or feature being
built.

**Status table** — one row per phase:

```markdown
| Phase | Status | Doc |
|-------|--------|-----|
| 1. Core Engine | NOT STARTED | [phase-1-core-engine.md](phase-1-core-engine.md) |
| 2. Query Commands | NOT STARTED | [phase-2-query-commands.md](phase-2-query-commands.md) |
```

Valid statuses: `NOT STARTED`, `IN PROGRESS`, `DONE`

**Current phase** — which phase is active and what to do next. For a fresh
package, this points to Phase 1.

**Key files** — paths to the most important files in the project that an
agent will need to read or modify.

**Ground rules** — project conventions, verification commands, and pointers
back to design decisions in the original spec. Include the line: "Design
decisions are documented in [spec filename] — don't re-litigate these."

**Open issues** — link to `open_issues.md` if it was generated.

**Update instruction** — include this line at the bottom: "Update this file
when you finish a phase or reach a milestone."

### 6. Fidelity check

Re-read the original input spec from disk. Cross-reference against all
generated phase docs collectively. Check for:

- **Gaps** — anything in the spec not captured in any phase doc. Missing
  requirements, dropped constraints, lost technical detail.
- **Hallucinations** — anything in the phase docs not grounded in the spec.
  Invented requirements, fabricated technical details, made-up constraints.
- **Distortions** — content that is present but misrepresented. Wrong values,
  swapped behaviors, changed constraints.

If issues found: fix them in the affected phase docs and report what was
fixed. If clean: report "Fidelity check passed — all spec content captured,
no additions."

### 7. Present result

List all generated files with one-line summaries so the user can review:

```
Generated files in {output-directory}/:
  readme_this_current_task.md  — bridge document (status, key files, ground rules)
  phase-1-core-engine.md       — goal, tasks, verification for Phase 1
  phase-2-query-commands.md    — goal, tasks, verification for Phase 2
  open_issues.md               — 3 open questions extracted from spec
```

The user reviews and approves or requests changes.

## What This Skill Does NOT Do

- **Plan for you** — input is an already-discussed, approved spec
- **Execute anything** — no code, no commands, no implementation
- **Modify the input spec** — the original file is never edited
- **Impose methodology** — no forced TDD, worktrees, or execution workflow
- **Hardcode paths** — spec location and output directory are user-provided
```

- [ ] **Step 2: Verify SKILL.md has valid frontmatter**

Run: `head -5 skills/plan-me-this/SKILL.md`
Expected: YAML frontmatter block with `name: plan-me-this` and `description: ...`

- [ ] **Step 3: Test install round-trip**

Run:
```bash
PROJECT_DIR=$(pwd) bash skills/plan-me-this/install.sh
```
Expected: `[ok]    plan-me-this skill installed to .../.claude/skills/plan-me-this/SKILL.md`

Then verify the file was copied:
```bash
cat .claude/skills/plan-me-this/SKILL.md | head -5
```
Expected: same frontmatter as the source

Then clean up (don't leave test artifacts in the repo):
```bash
rm -rf .claude/skills/plan-me-this
```

- [ ] **Step 4: Commit**

```bash
git add skills/plan-me-this/SKILL.md
git commit -m "feat: add plan-me-this skill definition"
```

---

### Task 4: Update README.md and roadmap

**Files:**
- Modify: `README.md:30` (skills table, plan-me-this row)
- Modify: `docs/roadmap.md:33-40` (plan-me-this entry)

- [ ] **Step 1: Update README.md skills table**

Change the plan-me-this row from:

```markdown
| /plan-me-this | Scaffold a multi-phase task package from a plan | Planned |
```

to:

```markdown
| [/plan-me-this](skills/plan-me-this/) | Package a spec into phase docs + readme_this_current_task.md | `./install.sh plan-me-this` |
```

- [ ] **Step 2: Update docs/roadmap.md**

Move `/plan-me-this` from the "Planned — Skills" section to the "Completed" section. Change the entry to:

```markdown
### /plan-me-this
Package an approved spec into self-contained phase docs and a living
`readme_this_current_task.md` handoff document. Takes a spec file path and
optional output directory.
```

- [ ] **Step 3: Commit**

```bash
git add README.md docs/roadmap.md
git commit -m "docs: mark plan-me-this as complete in README and roadmap"
```

---

### Task 5: End-to-end install/uninstall test

**Files:**
- No files created or modified — this is a verification-only task

- [ ] **Step 1: Test full install via top-level script**

Run:
```bash
./install.sh plan-me-this --project /tmp/test-plan-me-this-project
```
Expected: `[ok]    plan-me-this skill installed to /tmp/test-plan-me-this-project/.claude/skills/plan-me-this/SKILL.md`

- [ ] **Step 2: Verify installed file matches source**

Run:
```bash
cmp -s skills/plan-me-this/SKILL.md /tmp/test-plan-me-this-project/.claude/skills/plan-me-this/SKILL.md && echo "MATCH" || echo "MISMATCH"
```
Expected: `MATCH`

- [ ] **Step 3: Test idempotent re-install**

Run:
```bash
./install.sh plan-me-this --project /tmp/test-plan-me-this-project
```
Expected: `[ok]    plan-me-this skill already installed and up to date`

- [ ] **Step 4: Test uninstall**

Run:
```bash
./uninstall.sh plan-me-this --project /tmp/test-plan-me-this-project
```
Expected: `[ok]    Removed /tmp/test-plan-me-this-project/.claude/skills/plan-me-this`

- [ ] **Step 5: Verify clean removal**

Run:
```bash
ls /tmp/test-plan-me-this-project/.claude/skills/plan-me-this 2>&1
```
Expected: `No such file or directory`

- [ ] **Step 6: Test uninstall when already removed**

Run:
```bash
./uninstall.sh plan-me-this --project /tmp/test-plan-me-this-project
```
Expected: `[warn]  plan-me-this skill not found at ... (already removed?)`

- [ ] **Step 7: Clean up**

Run:
```bash
rm -rf /tmp/test-plan-me-this-project
```
