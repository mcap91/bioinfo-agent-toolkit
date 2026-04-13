---
name: blueprint
description: Create a portable, project-agnostic architecture reference document for a tool, module, or system. Use when the user says "/blueprint", wants to capture a system's architecture for reimplementation in another project, or needs to document how a tool works for porting. Takes free-form input — file/directory paths plus optional instructions.
---

# Blueprint

Create a single, portable architecture reference document that captures
everything needed to reimplement a tool, module, or system from scratch in a
different project — without access to the original source.

The blueprint captures the knowledge: math, algorithms, edge cases, design
decisions, critical code. Not a tutorial. Not a template. A framework
reference that a competent developer or coding agent can use to rebuild the
system in any project, with project-specific adaptations as needed.

## Invocation

Everything after `/blueprint` is free-form natural language. Parse out
file/directory paths and treat the rest as context and instructions.

| Invocation | Behavior |
|---|---|
| `/blueprint` | Ask the user what to blueprint |
| `/blueprint src/distances/` | Single path — scan and figure out scope |
| `/blueprint src/distances/ src/viz/plots.py` | Multiple paths |
| `/blueprint src/distances/ — be sure to capture the binning math` | Paths + instructions |
| `/blueprint src/distances/ -o docs/my_blueprint.md` | Custom output path |

Default output: `docs/{tool_name}_blueprint.md` in the current project.
Derive `{tool_name}` from the system being blueprinted (e.g.,
`cell_cell_distances_blueprint.md`). Override with `-o`.

The input can be any combination of: directories, individual source files
(any language), planning docs, design notes, or a concept spread across
docs and code.

If no paths are provided and you have conversational context about a
system, ask the user to confirm which files/directories to analyze.

## Workflow

### 1. Read and build structural map

Read all input paths. For directories, scan files relevant to the system
being blueprinted — code, docs, configs, tests that reveal behavior. If
the scope of a directory is ambiguous (e.g., a large `src/` with many
unrelated modules), ask one clarifying question before proceeding.

Build a structural map:

- What are the components/modules?
- How do they connect? (imports, data flow, dependency chain)
- What's the build order? (what to implement first, what's parallelizable)
- What does each component do at a high level?

If the user provided instructions ("be sure to capture X"), note these as
**coverage targets** to verify against later.

If you have conversational context about the system (you just built it,
discussed it, or debugged it), use it to inform the structural
understanding — especially the "why" behind decisions that may not be
evident from code alone.

**Scaling for large systems**: For systems with 4+ distinct components,
consider dispatching parallel subagents — one per component — to extract
detail in depth. Brief each subagent with the structural context it needs
and the specific component to analyze. Assemble results into the final
blueprint.

### 2. Guided inventory

Present the structural map to the user as an inventory, organized by
component. For each component, list what you plan to capture and at what
depth. Include cross-cutting concerns (shared data models, architectural
decisions, dependency info). Show coverage targets and whether they are
addressed.

**Wait for user approval or adjustment before proceeding.**

The user may say "you missed X" or "go deeper on Y" — adjust the plan
accordingly.

**Bias toward over-capturing**: When in doubt about whether something
warrants verbatim treatment or pattern-level description, default to
verbatim. It is better to capture too much than too little.

### 3. Write the blueprint

Write a single `.md` file. Structure follows the natural architecture of
the system — not a rigid template. Select and order sections based on
what the system actually contains.

#### Always-included sections

| Section | Contents |
|---|---|
| **Why This Exists** | The problem this solves, the gap it fills, why existing approaches don't work. Motivation, not description. |
| **Architecture Overview** | Component map, dependency chain, data flow. ASCII diagrams where helpful. Build order (what first, what's parallelizable). |
| **Component Specs** | One subsection per component. Algorithm steps, parameter tables with types and defaults, full function signatures, data contracts (input/output shapes, types, keys). Verbatim code for critical sections. |
| **Decisions Log** | Table: Decision / Choice / Rationale. Every non-obvious design choice. |
| **Dependencies** | Packages with version constraints and what uses them. |

#### Included when relevant

| Section | When to include |
|---|---|
| **Mathematical Foundation** | System involves math, formulas, statistical methods |
| **Error Handling Philosophy** | System has a deliberate error strategy (throw vs warn vs silent) |
| **Memory / Performance Patterns** | System handles large data, has OOM risks, or non-obvious performance patterns |
| **Composability / Integration** | System composes with other tools or has specific integration patterns |
| **Cost / Resource Estimates** | Compute time, storage size, cloud costs are relevant |
| **Gotchas & Non-Obvious Conventions** | Things that bite you if you don't know (API version changes, import quirks, etc.) |
| **Validated Results** | Structural correctness expectations from benchmarks, not project-specific numbers |
| **Glossary** | System uses domain-specific terminology the reader needs defined |

#### What gets verbatim code

Include full code — implementations, function signatures, working
snippets — for:

- Math and formula implementations
- Algorithms where the "obvious" approach is wrong
- Data contracts and schemas
- Edge case handlers
- Init/setup patterns hard to reconstruct from docs
- Memory/performance-critical patterns

Everything else described as patterns: architecture, glue logic, standard
IO, straightforward wrappers. A fresh agent reading the blueprint should
have every critical piece verbatim and enough structural description to
fill in the rest.

#### Stripping rules

Applied throughout the entire document:

- **No source-project file paths** — no absolute or relative paths from
  the original project
- **No proprietary names** — no specific markers, targets, dataset
  identifiers, or anything NDA/copyright sensitive
- **No project-specific config values** — no environment variables,
  bucket names, or API endpoints from the source project
- **Generic scientific vocabulary is fine** — T cell, macrophage, spatial
  coordinates, gene expression are domain terms, not project IP

No placeholder system. No substitution tables. The tool is inherently
portable — just don't leak project-specific content.

### 4. Fidelity check

After writing the blueprint, run three verification passes against the
original source files:

**Pass 1 — Gaps**: Re-read the source files. Cross-reference against the
blueprint. Is anything in the source not captured? Missing functions,
missing parameters, missing edge cases, missing math steps.

**Pass 2 — Hallucinations**: Is anything in the blueprint not grounded in
the source? Invented parameters, fabricated edge cases, made-up algorithm
steps, described behavior that doesn't exist in the code.

**Pass 3 — Code verification**: For every verbatim code block and formula
in the blueprint, diff against the actual source. Confirm nothing was
paraphrased, subtly altered, or has a wrong sign, index, or default
value. Math formulas get checked against their implementation.

Fix issues inline. Report what was fixed. If clean: "Fidelity check
passed — all source content captured, no additions."

### 5. Present result

Report:

- Where the file was written (absolute path)
- Summary of what was captured (component count, verbatim code sections,
  decisions logged)
- Fidelity check results
- Coverage targets and whether they were met

The user reviews the blueprint and can request changes.

## What This Skill Does NOT Do

- **Generate new code** — the blueprint contains code extracted from the
  source, but this skill does not scaffold projects or write
  implementation code for a target project
- **Execute anything** — no commands, no tests, no builds
- **Modify source files** — read-only against the input
- **Impose project structure** — no opinions on where code should live in
  the target project
- **Track tasks or phases** — no `/handoff` boundary, no `/plan-me-this`
  phase docs
- **Handle upgrade/diff between versions** — captures the current state
  only
- **Use placeholders or substitution tables** — written in plain language,
  not as a fill-in-the-blanks template
