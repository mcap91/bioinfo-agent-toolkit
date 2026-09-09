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

- **Closed**: the doc states a clear decision, or references resolve it, or
  the choice is mechanical (one reasonable answer exists). No stop-and-ask
  moment for a cold agent.
- **Open**: a cold agent handed this spec would have to STOP and ASK the
  operator before proceeding. The spec does not tell the agent what to do,
  and no reasonable default exists.

A decision is open ONLY when all three conditions hold:

1. **No answer in the text or references.** The doc and anything it
   references (rulings, prior decisions, code, linked issues) do not state
   a decision. If a ruling, prior-slice decision, or code convention
   already answers the question, it is closed — even if the target doc
   does not repeat the answer.
2. **Not mechanical.** A competent agent would not all converge on the same
   answer. File naming, error message wording, import ordering, obvious
   data-structure choices — these have one reasonable path. An agent that
   picks the obvious path and moves on is not "making a design decision."
3. **Operator judgment required.** The choice involves a tradeoff the
   operator cares about: scope, cost, risk, user-facing behavior,
   compatibility, security posture. If the wrong pick wastes a build
   cycle or creates rework, it is open. If the wrong pick is a five-minute
   fix, it is closed.

Trust the text. If the doc reads as decided, it is decided. If it reads as
ambiguous, apply the three conditions above — most ambiguities are
mechanical and do not block a cold agent.

### 4. Return the verdict

**If open decisions exist:**

```markdown
# BLOCKED — N open decisions

1. **Decision name** — One sentence: what the agent cannot do without an answer. [source:line]
2. **Decision name** — One sentence. [source:line]
```

Rules:
- Each item must be something a cold agent would stop and ask about. If
  you cannot imagine the agent getting stuck, do not list it.
- One sentence per decision. No sub-questions, no "also" clauses, no
  embedded options lists. If a decision has sub-parts, each sub-part is
  its own numbered item.
- Include a `[file:line]` reference.
- No paragraphs. No elaboration. The operator will ask if they need more.
- Do not list decisions that are already ruled in referenced docs, prior
  slices, or code — even if the target doc still shows them as pending.

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
