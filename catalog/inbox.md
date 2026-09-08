# Catalog inbox

Drop URLs (one per line, optional ` — note`) or fenced ```text blocks here, then run the drain (`/catalog-intake`). Blocked items are marked `⚠ needs-link` and stay until resolved.
https://huggingface.co/spaces/TIGER-Lab/MMEB-Leaderboard
https://github.com/BuilderIO/skills
https://github.com/BuilderIO/skills#visual-plan
https://github.com/BuilderIO/skills#visual-recap
https://github.com/Aider-AI/aider
https://github.com/netblue30/firejail
https://grigio.org/docker-alternatives-for-ai-agents-podman-bwrap-and-firejail/
```text
I compared sandbox options for AI agents. Here’s my ranking.
It’s pretty clear by now that if you’re letting AI agents run code, browse the web, touch files, or use tools, you should probably not run them directly on your own machine.

I went through a bunch of open-source sandbox options and ranked them mostly for my own use case. Sharing here in case it helps others evaluating the space.

My criteria were:

easy to get started

snapshotting

fork/clone

pause/resume

cross-OS support (Linux + macOS)

support for computer-use agents / full desktop environments

This ranking is biased toward people building AI agents, not just generic isolated code execution.

Full disclosure: I work on CelestoAI/SmolVM, so take that into account. I still tried to make this useful.

1. SmolVM
Why I ranked it first:

easy local setup

supports Linux and macOS

supports snapshotting, pause/resume, and persistent sandbox workflows

supports browser sessions and full desktop-style computer-use workflows

For my use case, it feels like the most complete mix of developer experience + agent-focused features.

2. Microsandbox
This one looks promising if you want something local-first and lightweight.

What I like:

local-first feel

simple developer experience

good fit for isolated execution without a ton of setup

Why it’s lower for me:

I’m less confident yet on snapshotting / clone semantics

computer-use / full desktop support seems less clear than the top entries

3. OpenSandbox
This feels more like a broader sandbox platform than just a local dev tool.

What stands out:

supports GUI agents

desktop / VNC-style workflows

more platform-level ambition

Why I ranked it lower:

heavier mental model

for my use case, I care a lot about tight DX and fast setup

4. E2B
Probably the most well-known option in this category.

What stands out:

easy to get started

pause/resume support

desktop sandbox support for computer-use agents

solid hosted experience

Why I ranked it lower for my use case:

I’m personally more biased toward local/open infrastructure and tighter control

My takeaway
The biggest thing I noticed is that a lot of “AI sandbox” discussions mix together very different products:

some are basically isolated code runners

some are full agent sandboxes

some support browser / desktop / computer-use

some are more like platform/control planes

So “best sandbox” really depends on what you need.

If your agent needs to:

write files and come back later

keep state between turns

run a browser

use a desktop environment

recover from interruptions

…then the feature set matters a lot more than just “can it run code?”

Curious what others here are using. Especially interested if I missed any sandbox that has:

real snapshotting

fast clone/fork from saved state

pause/resume

Linux + macOS support

proper computer-use support
```

https://github.com/landlock-lsm

```text

thedailyai.news
 
2d
AI coding agents don’t usually fail because the task is “too hard.” In this clip, Matt Pocock points at a simpler failure mode: we hand agents horizontal plans—database first, API next, frontend last—and they code layer by layer without an integrated feedback loop.

His fix is an old software idea from The Pragmatic Programmer: tracer bullets, or vertical slices. Instead of asking the agent to build one layer at a time, create thin tasks that cross the database, service/API, and frontend enough to prove the whole flow works.

That changes the job from “complete phase 1” to “ship one visible, testable slice.” The agent gets feedback earlier, humans can review something real sooner, and the Kanban backlog becomes easier for agents to grab independently.
```
