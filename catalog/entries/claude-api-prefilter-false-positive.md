---
name: claude-api-prefilter-false-positive
title: Claude API Pre-Filter False-Positive Troubleshooting
url: "https://docs.anthropic.com/en/docs/about-claude/models"
category: reference
tags: [claude-code, safety-classifier, false-positive, troubleshooting, api, context-injection, auto-memory]
reviewed: 2026-07-21
summary: ">-"
acquired: 2026-07-22
---

## What it covers

A field-tested diagnosis and fix recipe for Claude Code sessions that become
completely blocked — every turn returns a synthetic refusal record — due to
the API pre-filter pattern-matching bio- or security-adjacent language across
the combined request payload.

### Four trigger surfaces

1. **Injected context** (CLAUDE.md, auto-memory, hooks, skill descriptions):
   global and project CLAUDE.md, auto-memory files, and UserPromptSubmit hook
   output are injected into every API request. Bio-domain project names
   combined with model-steering language can cross the threshold.

2. **Git commit subjects**: the ~15 most recent commit subjects are injected
   at session start. Commits describing classifier fixes in explicit terms
   add to density and can re-trigger the block.

3. **User prompt wording**: destruction-adjacent phrasing in infrastructure
   contexts ("completely wiped and disconnected," "everything lost") can
   independently trigger the block before any file read or reasoning.

4. **Auto-memory directory**: memory files accumulate trigger terms over time
   (model names, repo names, prior-fix descriptions). The density grows
   silently across sessions. This is the most common practical trigger.

### Diagnosis

Confirmed via transcript grep for `"stop_reason":"refusal"` and
`"category":"bio"` in `.jsonl` files under `~/.claude/projects/<slug>/`.
A synthetic record with `model:"<synthetic>"` and `isApiErrorMessage:true`
confirms the false positive.

### Fix protocol

**Quick fix**: quarantine the auto-memory directory
(`mv ~/.claude/projects/<slug>/memory ~/.claude/projects/<slug>/memory.bak`),
start a fresh session, test with "hi".

**Deep fix**: bisect by renaming surfaces one at a time; reword to neutral
ops language; squash commit subjects to bland descriptions; reword prompts
to avoid stacking destruction-adjacent phrases. A fresh session is required
for validation — the old session has the old preamble cached.

### Key pitfalls

- The blocked agent's self-diagnosis is unreliable (reasoning from inside
  the blocked state with incorrect assumptions about what the filter inspects)
- Fix commits can become the next trigger if their subjects are explicit
- `/clear` and new sessions do not help if the trigger is in injected context
- All four surfaces stack — individually safe terms can cross the threshold
  in combination
