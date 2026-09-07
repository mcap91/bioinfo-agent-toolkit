---
name: verticalizing-plans
description: Use when scoping a multi-stage build, or when holding a plan, tracker, roadmap, or spec organized as sequential phases or layers (foundation → features → hardening) — especially if early stages produce no runnable end-to-end output, stage gates quietly depend on later-stage machinery, a working system gets torn down before its replacement is proven, or a schema/contract freezes before first real use. Also when asked to make a plan "more incremental" or "capture feedback earlier". Not for small or one-off tasks, single-component work, or plans that are already incremental.
---

# Verticalizing Plans

## Overview

A phase plan builds one machine in horizontal layers; feedback arrives when the
layers finally meet — near the end. A vertical-slice plan builds the whole
machine thin in the first increment and widens it, so every increment ends with
a live end-to-end proof. This skill (a) diagnoses whether a plan is harmfully
phase-shaped and (b) converts it without dropping scope.

Phases are sometimes the right shape. The diagnostics decide — not dogma.

**Scoping something new (no plan exists yet)?** Read `planning-guidelines.md`
in this skill directory instead — the same rules, stated forward.

## Step 1 — Inventory (the conservation law)

From the input — a tracker, spec, plan.md, roadmap, or loose notes, any format —
list: the goal, every stage, every task/item (keep their IDs), every gate/proof,
the out-of-scope list, and every deferred item WITH its re-open trigger.
Everything on this list must reappear in your output. Nothing is dropped,
merged away, or silently absorbed.

## Step 2 — Find the spine

Write down the runtime pipeline the FINISHED system executes, as stations —
e.g. `validate → acquire → transform → deliver → record`. This is the dataflow
at runtime, **not the build-dependency order**. The single most common failure
is organizing slices by "what depends on what to build" — that reproduces the
phase plan. Dependencies are satisfied by *thinning* (Step 4), not sequencing.

If you cannot draw a spine (pure content/document work, one-station tasks),
STOP and say slicing doesn't apply.

## Step 3 — Diagnose (convert only what fails)

| Signal of harmful horizontality | Check |
|---|---|
| A stage's own gate needs machinery scheduled in a later stage | trace each gate's prerequisites |
| First runnable end-to-end output arrives after >⅓ of the work | find the earliest full-spine proof |
| A working/incumbent system is deleted before its replacement is proven | look for teardown tasks in early stages |
| A schema, contract, or API freezes before anything real exercises it | look for "contract/registry/types first" stages |
| One stage breaks a large test corpus at once | estimate test blast radius of deletions |
| Deferred items have usage triggers, revisited only at plan end | read the deferral list |

**Legitimate phases — leave them alone:** waiting on an external dependency
(hardware, a third party, an approval stage-gate), stages that share no runtime
spine, or work small enough that slicing is ceremony. If the plan passes the
table, say so and stop; don't restructure a healthy plan.

## Step 4 — Construct slices

1. **S0 = walking skeleton:** the THINNEST path through EVERY station, with the
   riskiest integrations included — risk goes first, not last. Break false
   dependencies with **named interims** (a hardcoded config entry, an env-var
   passthrough, a hand-authored input file instead of the generator); every
   interim states which later slice retires it.
2. Each later slice **widens one dimension** (full validation, credentials,
   enforcement, more modes, …) and still runs end-to-end.
3. **Freeze late:** contracts/schemas lock only after real runs have shaped
   them. Contract/schema/registry/type tasks default OUT of the skeleton even
   when they look load-bearing — a hand-authored instance of the record or
   config almost always substitutes, and the freeze moves to the slice after
   the first live proofs have exercised the shape.
4. **Delete late:** the incumbent system stays live — and its tests stay green —
   until a final cutover slice.
5. Every slice ends in a gate that is a **live proof of the spine** someone can
   watch and ratify. Never "code complete", never a component demo.
6. Re-check the deferred-trigger list at every gate.

## Step 5 — Verify conservation

Build a coverage matrix: every inventoried task and gate → at least one slice.
Original gates survive as slice gates. New work you discovered is ADDED
explicitly (new task IDs), never done silently. If the host tooling validates
required section headings, keep the literal headings and re-label semantically
(a "Phase" column can read "Slice (phase)").

## Step 6 — Outputs and ratification

Emit three artifacts: (a) the restructured plan/tracker; (b) a one-page flow
map — spine diagram, slice ladder with gates, station×slice matrix — headed
"illustrative, not normative"; (c) a delta summary: what moved, what's new,
what's interim and when it retires. Do NOT overwrite the source plan until the
plan's owner ratifies the delta summary.

## Red flags — you're still horizontal

- A "slice" that cannot run end-to-end (that's a layer with better branding)
- Checkpoints *inside* a stage instead of proofs of the whole spine
- The first increment starts with contract/schema/registry work "because
  everything depends on it" — thin it with an interim instead
- Merged phases presented as slices (thicker layers are still layers)
- Teardown of a working system anywhere before the final slice
- Feedback ceremony (demo tiers, feedback logs) added onto an unchanged shape
- Any inventoried item missing from the coverage matrix

## Common mistakes

| Mistake | Fix |
|---|---|
| Organizing by build-dependency order | Organize by runtime spine; thin, don't sequence |
| "Can't verify independence, keeping original order" | Independence is created: name an interim and move on |
| First "checkpoint" demos one component | Every gate runs the spine, however thin |
| Slicing a plan that passed Step 3 | Leave good phases alone; say why they're fine |
