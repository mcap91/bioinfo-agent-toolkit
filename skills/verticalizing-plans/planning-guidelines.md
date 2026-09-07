# Planning Guidelines — Slice-First Scoping

Forward-looking companion to `SKILL.md` (which converts existing phase-shaped
plans). Read this BEFORE scoping a multi-stage build, so the plan is born
sliced and never needs converting. Rules are shared with SKILL.md; it is the
authority if they ever disagree.

## Before writing any plan

1. **Draw the spine first.** The runtime pipeline the finished system will
   execute, as stations (`validate → acquire → transform → deliver → record`).
   If there is no spine — content work, a single component, a one-off task —
   don't slice; a simple task list or deliberate phases are fine.
2. **Ask what the first live proof is.** The first increment should run the
   whole spine, thin, and end with something an owner can watch work. If your
   draft's first milestone is "foundation laid" or "contracts defined", reshape
   before writing more.

## Sequencing rules

- **Skeleton first, widen after.** Increment 1 = thinnest path through every
  station, riskiest integrations included. Later increments widen one
  dimension each and still run end-to-end.
- **Break false dependencies with named interims** — a hardcoded entry, an
  env-var passthrough, a hand-authored input file. Each interim names the
  increment that retires it. "X must exist before Y" is usually "a thin X must
  exist" — build the thin X.
- **Freeze late.** Schemas, contracts, and registries lock after real runs have
  exercised them, not in increment 1.
- **Delete late.** If a working system is being replaced, it stays live — tests
  green — until a final cutover increment proves the replacement covers its jobs.
- **Gates are live proofs.** Every increment ends with a demonstration of the
  spine an owner ratifies. "Code complete" and component demos are not gates.
- **Deferrals carry triggers, checked at every gate.** Anything cut from scope
  gets a written re-open condition, revisited at each gate — not at plan end.
- **Conservation.** Late-discovered work gets its own named task, added
  explicitly. Nothing enters or leaves scope silently.

## When phases are the right call

Choose phases deliberately — and write down why — when:

- an external dependency forces waiting (hardware, third party, approvals);
- stages share no runtime spine (truly independent deliverables);
- the work is small enough that slicing is ceremony;
- a real precondition blocks any end-to-end run until it exists.

A plan may also mix shapes: sliced core build, phased external-dependency track.

## Smell test for a draft plan

Read your stage list and ask: "after each stage, what runs end-to-end that
didn't before?" If the honest answer for the first several stages is
"nothing yet", the plan is horizontal — apply `SKILL.md` Step 4 before it lands.
