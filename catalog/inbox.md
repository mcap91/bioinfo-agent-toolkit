# Catalog inbox

Drop URLs (one per line, optional ` — note`) or fenced ```text blocks here, then run the drain (`/catalog-intake`). Blocked items are marked `⚠ needs-link` and stay until resolved.

https://github.com/diegosouzapw/OmniRoute

```text
TITLE: Claude API pre-filter false-positive — bio/destruction-adjacent phrasing triggers whole-session block
TAGS: claude-code, fable-5, opus, safety-classifier, false-positive, troubleshooting, fix-recipe

PROBLEM
-------
Claude Code sessions can become completely blocked — every turn returns a
synthetic refusal record (stop_reason:"refusal", category:"bio" or similar) —
with no useful error message. It looks like workspace corruption but is not.

There are TWO independent trigger surfaces, and they stack:

  1. INJECTED CONTEXT (CLAUDE.md / memory / git-status commit subjects)
     The project's CLAUDE.md, auto-memory index, and recent-commit subjects are
     injected into every API request as system context. If the combined text
     pattern-matches bio/destruction-adjacent language, the API pre-filter
     blocks the entire session. /clear, new session, VS Code restart — none
     help, because each one re-injects the same triggering context.

     First observed: 2026-07-06, localllm repo under Fable 5.
     Trigger cluster: "guardrail incubator for local open-source LLMs" +
       "guarded agent; never free-styles" + "bioinfo-agent-toolkit"
     Classifier read: "stripping safety off a local model for bio work."
     Opus 4.8 did NOT trip on the same context — only Fable 5 did.

  2. USER PROMPT WORDING
     The API pre-filter also runs on the user's message text. Prompts
     containing destruction-adjacent phrasing in an infrastructure context
     ("completely wiped and disconnected," "kick off the cellranger pipeline
     on the dedicated VM," "everything lost," "clear local disk") can
     independently trigger the block, even with a clean CLAUDE.md.

     This layer fires BEFORE any file read, before any reasoning. No edit
     to CLAUDE.md, settings.json, or a hook changes it. Only prompt wording
     changes its output.

  Either trigger alone is sufficient to block. Both can be active at once.

DIAGNOSIS
---------
Symptoms:
  - Every turn in the session returns a refusal. Not one turn — ALL turns.
  - New session / /clear / restart does NOT fix it (if trigger is in
    injected context).
  - The .jsonl transcripts are structurally valid — this is NOT file
    corruption.

Confirm via transcript grep:
  grep -r '"stop_reason":"refusal"' ~/.claude/projects/<slug>/*.jsonl
  grep -r '"category":"bio"' ~/.claude/projects/<slug>/*.jsonl

If you find a synthetic record with model:"<synthetic>", isApiErrorMessage:true,
stop_reason:"refusal", stop_details.category:"bio" — you have the false
positive. The workspace is fine.

FIX
---
QUICK FIX — wipe auto-memory (confirmed 2026-07-20):
  The auto-memory directory is the #1 trigger. Memory files accumulate
  terms (model names, repo names, prior-fix descriptions, "injection,"
  "security," "block") that stack with bio-domain project context to
  cross the classifier threshold. Individual terms may grep clean but
  the combined density triggers the filter.

  Quick clear:
    mv ~/.claude/projects/<slug>/memory ~/.claude/projects/<slug>/memory.bak

  Then start a fresh session and type "hi". If it clears, you're done.
  If the user doesn't rely on auto-memory (e.g. uses a wiki instead),
  ask if they want to delete it permanently rather than rewording files
  one by one. The memory system keeps writing new trigger material over
  time, so rewrites are a recurring maintenance burden.

DEEP FIX — if quick fix is insufficient or memory must be preserved:

  Trigger 1 (injected context — CLAUDE.md / memory / hooks):
    - Bisect by renaming surfaces one at a time (memory dir, global
      CLAUDE.md, project CLAUDE.md, hook scripts), testing a fresh
      session + "hi" after each rename. This isolates which surface
      carries the trigger.
    - Common trigger clusters: bio-domain project names + model-steering
      language ("governor," "constrained agent," "lockdown"); prior-fix
      descriptions that reference the classifier itself; terms like
      "injection," "hardening," "safeguard" in memory files.
    - Reword to neutral ops language. Do NOT delete .jsonl transcripts.
    - Global CLAUDE.md and UserPromptSubmit hooks are injected into
      EVERY project — a trigger there blocks all repos, not just one.

  Trigger 2 (user prompt wording):
    - Reword the prompt to avoid stacking destruction-adjacent phrases.
      Use neutral infrastructure language:
        BEFORE: "completely wiped and disconnected"
        AFTER:  "the EFS mount is empty; the instance has no network path
                 to the old storage"
        BEFORE: "everything was lost"
        AFTER:  "the previous run's outputs are not on this volume"
    - This layer cannot be fixed by any config/file edit — only by prompt
      rewording.

VALIDATION
----------
  1. Apply the fix (memory wipe or reword).
  2. Start a FRESH session (the old session still has the old preamble
     cached — testing in the same session proves nothing).
  3. Use a non-blocking prompt for the first test (so you're not
     conflating trigger 1 and trigger 2).
  4. Confirm the session accepts turns normally.
  5. THEN test prompts that previously blocked, reworded neutrally.

IMPORTANT: the agent in a blocked session may confidently misdiagnose
this. Common wrong claims from a blocked agent:
  - "The API pre-filter runs before any file, so CLAUDE.md edits can't
     help" — WRONG for trigger 1. CLAUDE.md IS the injected context that
     the pre-filter reads. Editing it directly changes what the filter sees.
  - "Only prompt wording changes the filter's output" — WRONG. The filter
     sees the full request payload: system prompt (which includes CLAUDE.md)
     + user message + conversation history. All three are trigger surfaces.
  - "This session can validate the fix" — WRONG. The global CLAUDE.md is
     read at session start. The current session runs the OLD preamble.
     A fresh session is required.

The agent's self-diagnosis is unreliable here because it is reasoning
from inside the blocked state and may not have correct information about
what the API pre-filter actually inspects.

CROSS-REFERENCES
----------------
  - localllm wiki memory: fable5-bio-false-positive-on-injected-context
  - bioinfo-agent-toolkit WK-0033: Fable 5 lockdown/re-pin
  - First occurrence: 2026-07-06, localllm repo, Fable 5
  - Second occurrence: 2026-07-20, separate VM, bioinformatics project,
    destruction-adjacent prompt language in disaster-recovery context
  - Third occurrence: 2026-07-20, same day, local machine after Fable 5
    Max plan rollout. Classifier tightened — old CLAUDE.md reword no
    longer sufficient. Auto-memory confirmed as primary trigger via
    bisection across localllm + bioinfo-agent-toolkit. Memory wipe
    clears the block; deep reword of global CLAUDE.md + hook also
    needed for belt-and-suspenders resilience.
```