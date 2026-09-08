---
name: spec-check
description: Read doc(s) and surface open design decisions that need operator input before the work can be handed off for autonomous execution. Use when the user says "/spec-check", asks "are there open decisions", "is this ready for handoff", or "is this mechanical".
---

# Spec Check

Read the target doc(s). Determine whether a low-effort execution agent could
run the work autonomously, or whether open design decisions need operator
input first.

## Invocation

Parse the arguments after `/spec-check`:

```
/spec-check <path> [path...] [slice or scope hint]
```

Examples:
- `/spec-check wiki/plans/PLN-0004/execution/tracker.md S3`
- `/spec-check wiki/issues/WK-0059.md`
- `/spec-check docs/spec.md docs/design.md`

The slice/scope hint (e.g. `S3`) is optional — it narrows the check to a
subset of the doc if the doc covers multiple phases or stages.

## Workflow

### 1. Read the target doc(s)

Read every file the user pointed at, in full. If a scope hint was given,
focus on the sections relevant to that scope but still read the whole doc
for cross-references.

### 2. Follow references (lightweight, not mandatory)

If the doc references other files (specs, rulings, issues, phase docs),
read those too — they may resolve questions that look open in the target
doc alone. If a wiki is available and a reference points to a wiki record,
search for it. Do not run a full wiki retrieval pass — only chase
references the doc itself names.

### 3. Assess each design point

For every design point, technical choice, or behavioral specification in
scope, classify it:

- **Closed**: the doc states a clear decision, rationale, or concrete
  implementation detail. No ambiguity an execution agent would need to
  resolve.
- **Open**: the doc presents alternatives without choosing, marks something
  TBD/TODO, leaves behavior unspecified that an execution agent would need
  to decide, or describes a goal without enough detail to implement it
  mechanically.

Trust the text. If the doc reads as decided, it is decided. If it reads as
ambiguous, it is open. Do not infer closure from naming conventions, file
structure, or the existence of other files.

### 4. Return the verdict

**If open decisions exist:**

```markdown
# BLOCKED — N open decisions

1. **Decision name** — One sentence: what is unspecified or ambiguous. [source:line]
2. **Decision name** — One sentence. [source:line]
```

Rules:
- One sentence per decision. No sub-questions, no "also" clauses, no
  embedded options lists. If a decision has sub-parts, each sub-part is
  its own numbered item.
- Include a `[file:line]` reference.
- No paragraphs. No elaboration. The operator will ask if they need more.

**If no open decisions exist:**

```markdown
# CLEAR — <one sentence saying why this is mechanical>
```

The CLEAR sentence is a positive assertion, not "I found nothing." Examples:
- `CLEAR — all five S3 tasks have concrete inputs, outputs, and verification commands; an execution agent makes zero design calls.`
- `CLEAR — WK-0059 specifies the exact schema change, migration SQL, and rollback; turnkey.`
- `CLEAR — spec.md defines every endpoint, payload shape, and error code; nothing left to decide.`

The point: if you handed this to a low-effort agent, would it need to make
design decisions? If yes, list them. If no, say why you're confident.

**Formatting:** Output must use markdown headers (`#`) and blank lines
between items so it renders cleanly in a terminal. No inline walls of text.

## What this skill does NOT do

- Modify any file
- Propose answers to open decisions
- Generate rulings or specs
- Run a mandatory wiki/retrieval pass — it reads what you point it at and chases references the doc names
- Grade doc quality — it only checks decision completeness
