---
name: bmad-skill-forge
title: "BMAD Skill Forge"
url: https://github.com/armelhbobdad/bmad-module-skill-forge
category: skill-generator
verdict: pilot
verdict_reason: "strong fit for bioinformatics tool skill generation; start with Brief tier on samtools"
install: "npx bmad-module-skill-forge install"
tags: [skill-generation, provenance, ast, cli-tools]
workflows: [scRNA-seq, spatial]
reviewed: 2026-05-25
acquired: 2026-05-25
supersedes: []
---

## What it does

Transforms code repos and documentation into verified, version-pinned AI skill files. Uses AST parsing to extract real function signatures, so generated skills reference actual API shapes rather than guessed ones. Every claim traces back to source via a provenance-map.json (file:line at pinned commit for code, `[EXT:{url}]` citations for docs-only skills). Produces two outputs: a full `SKILL.md` with signatures, parameters, types, and inline provenance citations like `[AST:file.py:L27]`; and a `context-snippet.md` (80-120 token compressed index) for passive injection into CLAUDE.md. The workflow `@Ferris forge <library>` chains Brief → Create → Test → Export steps, each clearing context before the next.

**Three capability tiers**:
1. **Brief** — documentation/discourse analysis only, no AST. Immediately usable, no extra tooling.
2. **Forge** — adds AST extraction via `ast-grep`.
3. **Forge+/Deep** — adds semantic search (`cocoindex-code`) and hybrid indexing.

Lifecycle operations (Rename, Drop, Update, Export) are all transactional. Validation includes skill-check for agentskills.io format compliance and optional Snyk agent scan for prompt injection and data exposure.

## Why this verdict

For bioinformatics CLIs (samtools, bedtools, nextflow), hand-writing skill definitions risks hallucinated flag names and wrong parameter types. Skill Forge prevents this by grounding every claim in a parsed source. The provenance model is the key differentiator — no other skill generator in the current stack provides file:line:commit traceability. Brief tier requires only Node.js >= 22 and no AST setup, making it the lowest-friction entry point.

## Mechanical details

Requirements: Node.js >= 22, Python >= 3.10, `uv`. For Forge and above: `ast-grep`. Install via `npx bmad-module-skill-forge install`. Start with Brief tier on samtools — no AST setup needed, works from docs and man pages alone. The `.autoharness/` analog here is the provenance-map.json generated per skill file.
