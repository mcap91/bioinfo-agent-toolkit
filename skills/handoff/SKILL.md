---
name: handoff
description: Generate a self-contained prompt to hand off current work to a fresh CLI agent or a subagent. Use when the user says "/handoff", wants to continue work in a new conversation, delegate tasks to a subagent, split a workflow, or pass context to a fresh agent after a milestone. Supports two modes — "fresh" (new CLI conversation) and "sub" (Agent tool subagent).
---

# Handoff

Generate a complete, copy-pasteable prompt that gives a fresh agent everything it needs to pick up work from the current conversation.

## Modes

Parse the argument after `/handoff`:

| Invocation | Mode | Output |
|---|---|---|
| `/handoff` or `/handoff fresh` | **fresh** | Prompt for a new CLI conversation |
| `/handoff sub` | **sub** | Prompt + Agent tool call(s) ready to execute |

If the user adds extra instructions after the mode keyword (e.g. `/handoff sub fix the 3 bugs we identified`), incorporate them as the task focus.

## Workflow

### 1. Gather context

Before generating the prompt, silently collect:

- **What was done**: key decisions, completed steps, and commits in this conversation.
- **What's next**: remaining tasks, open items, or the specific work the user wants handed off.
- **Relevant files**: paths to source files, configs, scripts, test files, and data directories that the new agent will need to read or modify. Use absolute paths.
- **Tracking docs**: any Markdown checklists, phase docs, or task lists being maintained (e.g. `docs/pipeline_deployment.md`). The new agent should update these after completing work.
- **Constraints**: environment details (conda env name, Python/R versions), branch name, anything the new agent must not break.

If context is ambiguous (e.g. multiple possible next tasks), ask the user one short clarifying question before generating.

### 2. Generate the prompt

#### Fresh mode (`/handoff fresh`)

Output a fenced Markdown block the user can copy-paste into a new `claude` CLI session. Structure:

~~~
```
## Context

<What was accomplished, key decisions, current branch, relevant commits>

## Relevant files

<Bulleted list of absolute paths the agent should read first>

## Task

<Clear description of what to do next — numbered steps if multiple>

## Tracking

After completing work, update the checklist in `<path/to/tracking_doc.md>`:
- Mark completed items with `[x]`
- Add new items if scope changed

## Constraints

<Env, branch, things not to break>
```
~~~

Keep the prompt concise but complete — a fresh agent has zero prior context. Include enough detail that it can start working immediately without asking clarifying questions.

#### Sub mode (`/handoff sub`)

Output one or more Agent tool calls the user can approve. Each call should have:

- A short `description` (3-5 words)
- A `prompt` containing the same context structure as fresh mode, but written as direct instructions (imperative voice, no headers needed — just dense, actionable text)
- Use `subagent_type: "general-purpose"` unless the task is pure exploration

If there are multiple independent tasks, generate parallel Agent calls. If tasks depend on each other, generate them sequentially with a note about ordering.

Also print the prompt text above the tool call so the user can review it before approving.

### 3. Verify completeness

Before outputting, check:

- [ ] Every file the agent needs to touch is listed with its absolute path
- [ ] The task description is specific enough to act on without follow-up questions
- [ ] Tracking doc path is included (if one exists in the conversation)
- [ ] No assumptions about conversation history — everything is explicit
