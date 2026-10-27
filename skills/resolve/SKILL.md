---
name: resolve
description: Re-orient an agent that asked the operator a question the evidence could answer. Runs the resolution chain (records, rules, code, reference systems, web), makes the call, records it, and keeps working. Use when the user says "/resolve", "resolve it yourself", "you could have figured this out", or "why are you asking me".
---

# Resolve

You put a question to the operator that you could have answered yourself. Stop waiting.
Resolve it from evidence, record what you chose and why, and continue the work.

The operator reviews your choices **after** you make them, by asking questions about your
record — not before, by answering yours. A clear record is the deliverable; a list of
options is not.

## Invocation

```
/resolve [question]
```

With no argument, resolve the last question, option list, or "Approve?" you put to the
operator. If you asked several, resolve each one.

## Workflow

### 1. Name the question

One sentence. Then one line: what changes in the work depending on the answer.

### 2. Look

Search until the answer is clear. The order is your choice; skip what cannot help.

- **Records** — the repo's wiki or tracker (kb-wiki `search` if available), `docs/`,
  decision records, the work item itself.
- **Rules** — the repo's rules file, `AGENTS.md` / `CLAUDE.md`, accepted decisions. A rule
  that answers the question ends the search. When rules leave a tie, the simplest option
  with the smallest blast radius wins.
- **Code** — read it. For a broad sweep, use a read-only explore subagent.
- **Reference systems** — any comparable codebase or catalog the repo names as a
  reference. Check what it does for the same problem.
- **Web** — only when the answer depends on external facts (library behavior, versions,
  APIs).

Every claim carries a citation: `file:line`, a record id, or a URL. Subagent prompts state
the question, the output fields you need, and "cite every claim". Subagents are read-only.
Budget: at most four search subagents.

### 3. Choose

Pick what the evidence supports. If the evidence is split, pick the simplest, most
reversible option and say that is why.

### 4. Cold check

Give one fresh read-only subagent only the choice and its evidence — not your reasoning —
and ask it to refute the choice, citing file:line. Apply its amendments. If it refutes the
choice, choose again once and check again; if the second check also refutes, the item
goes to the operator (below).

### 5. Record

One row per question:

```
| # | date | seat | question | looked (cite) | evidence | options | choice | reason | cold check |
```

If the work item has a `## Resolutions` section and your role may edit it, append the row
there. Otherwise put it in your reply. Then one line: `Resolved: <choice>. Continuing with <next step>.`
Then continue.

## What still goes to the operator

Only these:

- an action that is irreversible or outward-facing (publish, push, delete, send, spend
  beyond a stated budget);
- a change to the approved spec's objective, scope, or acceptance criteria;
- what the operator wants (intent, priority, taste) when no record states it;
- a choice that failed two cold checks.

For each, write one statement:

1. `Operator action needed: yes — <why it is one of the four above>`
2. The question, in one plain sentence.
3. What you searched and what you found.
4. Two or three options, one recommended.
5. The single choice you need.

Resolve everything else in the same turn and keep working.

## Do not

- Present options for a question you can resolve.
- Write or change rules. You record resolutions; humans write rules.
- Hide a resolution. Every choice made under this skill is recorded.
