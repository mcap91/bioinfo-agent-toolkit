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
