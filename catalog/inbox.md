# Catalog inbox

Drop URLs (one per line, optional ` — note`) or fenced ```text blocks here, then run the drain (`/catalog-intake`). Blocked items are marked `⚠ needs-link` and stay until resolved.

https://www.llamaindex.ai/blog/llamaindex-and-kaggle-launch-a-document-extraction-leaderboard-for-ai-agents

https://blog.modelcontextprotocol.io/posts/mcp-roadmap/

```text
First real project I've built, a multi-agent "personal executive AI" instead of one big assistant. Would love feedback.
Discussion
This is the first project I’ve actually finished and felt comfortable enough to share, so go easy on me. That said, please poke holes in it. That’s half the reason I’m posting.

I’ve been messing around with the idea of having multiple AI agents, but I didn’t really want the usual setup where a bunch of agents talk to each other and you’re never quite sure who did what. So I ended up building something closer to a small org chart.

There’s one lead agent I call Master Control. Everything starts there. It decides who should handle the request, delegates it, and then reports the result back to me. The other agents don’t really “talk to me” directly, which has made the whole thing way easier to follow.

Under that I have a few specialists for different things like research, coding, and general day-to-day stuff. I’ve tried pretty hard not to give every agent access to everything. If an agent doesn’t need a tool or a piece of data for its job, it doesn’t get it.

The part I probably spent the most time thinking about was oversight. There’s a separate watcher/audit agent that can flag things independently. The lead agent can’t edit its findings, silence it, or override what it reports. The watcher reports to me separately.

I also put hard approval gates in front of anything I’d consider difficult or impossible to undo. Spending money, sending something externally, deleting data, changing credentials, that kind of thing. The agents can prepare the action, but they can’t actually cross that line until I approve it.

There’s also some persistent memory so I’m not starting from zero all the time.

I’ve been using it for a few weeks now for normal stuff like research, drafting, and light ops. The thing I didn’t expect is that the biggest improvement hasn’t really been “more powerful AI.” It’s just calmer to use. I know that sounds weird, but knowing there’s a defined chain of command and that nothing irreversible happens without me approving it makes me much more comfortable letting the system do things on its own.

And just to get this out of the way: I’m definitely not claiming I invented multi-agent systems.

CrewAI, AutoGen, LangGraph, Google ADK, etc. already cover a lot of the orchestration side of this. I’m building mine on top of OpenClaw. What I wanted was a slightly different emphasis. Most of what I found treated governance as something you add once you’ve figured out the agents. I wanted to start with the governance and build the agents inside it.

So the rules were basically:

One agent is accountable for reporting back to me. Specialists only get the access they actually need. The auditor is independent of the agent it’s auditing. And irreversible actions always come back to the human.

LangGraph’s human-in-the-loop checkpoints are probably the closest thing I found conceptually, but I wanted those controls to behave more like system policy than something I remembered to add to individual workflows.

I’m also aiming this mostly at personal/solo use rather than enterprise automation or coding swarms, which seems to be where a lot of the examples live. Still early, and I’m sure there are holes I haven’t found yet.

Happy to talk architecture, approval gates, the watcher setup, or anything that looks dumb from the outside. Built on an open agent framework. Nothing particularly exotic underneath it.

For anyone who wants the actual breakdown instead of just vibes, here’s how it’s tiered:

Tier 0, Lead Agent (Master Control): intakes every request, classifies it by objective/priority/risk, decides who handles it, and is the only one that reports back to me. It also enforces the approval gates.

Tier 1, Specialist sub-agents (least-privilege, scoped per role): research/analysis does read-only lookups and drafting with no side effects, ops/comms handles scheduling and message drafting but can’t fire off a send on its own, and build/technical stays sandboxed to its own environment with no reach into other agents’ tools or data.

Tier 2, Audit/Watcher (independent): cross-checks the other agents’ actions against policy and flags problems straight to me. It can’t be edited, delayed, or silenced by the Lead Agent. No task-execution role, oversight only.

Tier 3, Owner (me): final sign-off on anything irreversible, and the only one who can approve remediation after the watcher flags something.

Quick version of what needs my sign-off vs. what doesn’t: research, summarizing, and drafting run freely. Anything that leaves the system (sending externally), costs money, deletes data, or touches credentials stops and waits for me. No exceptions, and no agent can self-approve its way around that.

he org chart approach is smart, especially for solo use. Most multi-agent setups I've tried end up feeling like a committee meeting where nobody's really in charge, so having a clear chain of command actually makes trust way easier to build

Your watcher being truly independent is the part that caught my attention. Too many systems bolt on oversight as an afterthought and then let the same agent it's watching just dismiss the flags, which defeats the whole point

Appreciate that. The "committee meeting" thing is exactly what pushed me toward this, tried a few setups where everyone chimes in and nobody's actually accountable for the final call, so I wanted one clear chain of command instead. The watcher independence was the part I cared about most, honestly more than raw capability. An oversight layer that the thing it's watching can quietly override isn't oversight, it's decoration. Mine can flag something and there's no path for the lead agent to edit it, delay it, or make it disappear, only I can act on what it flags. Took extra work to get that separation actually enforced instead of just documented, but it's the one piece I wasn't willing to cut corners on.
```

```text
this was sued to make a video game demo. i have a video game repo. file under 3d modleing, video game, etc. there migh be useful principles in this prompt stucture:

hat's the entire Prompt:

# Goal

Build a Cities: Skylines II–class city builder in Three.js (latest release) + Vite, plain ES modules, from this empty folder. The bar is AAA: photographic PBR materials, physically plausible sun/sky/shadows, atmospheric depth, a living city at night, believable roads and traffic. Never programmer art.

# How to work

1. Architecture first. Before any feature code, write ARCHITECTURE.md: one folder per subsystem (terrain, environment, roads, zoning, buildings, props, traffic, effects, simulation, tools, ui, audio, demo city), a shared world data model, the public API each module must expose, the events it emits, units (metres, +Y up), determinism (seeded RNG only), a performance budget (≥50 fps at 1080p, ≤1500 draw calls) and an asset policy (CC0 only: Poly Haven, ambientCG, or procedural). Isolate module failures so one broken module never takes the game down.

2. Build the verification loop before the game. A headless-Chrome screenshot tool that loads the app, waits until ready, sets a camera preset and time of day, and writes PNG + a JSON log (console errors, fps, draw calls). Every module also ships a "showcase" mode that stages a representative scene of just that module. No agent may claim anything it hasn't screenshotted and looked at.

3. Fan out. Use multi-agent orchestration ("ultracode"). One builder agent per module, each owning only its folder. Run in waves ordered by dependency: (1) terrain, sky/weather, roads, simulation, UI, audio, effects; (2) zoning, buildings, props, traffic, build tools; (3) demo city. Between waves, one integrator agent (the only one allowed to touch core) applies builders' core-change requests and fixes the seams.

4. Gauntlet every module. After each builder round, a separate critic agent (a brutal AAA art director who writes no code) takes its own screenshots at several times of day and zoom levels, checks the API contract, console errors and perf, and scores 0–10 against real Cities: Skylines II reference screenshots: 10 = indistinguishable, 8.5 = AAA with nits, 7 = good indie, 5 = programmer art. Pass = ≥8.5 with zero errors. Below that, the builder gets the ranked issue list and goes again, up to 4 rounds.

5. Final gate. A whole-game critic scores the demo city. Then blind judges get pairs of screenshots labelled only A and B (ours vs. Cities: Skylines II, order shuffled) and say which looks better and why.

6. /loop until every critic passes. Persist scores and open issues to docs/STATUS.json so each iteration resumes from the weakest module, not from scratch.

# Rules

- Never inflate scores. Report real numbers, failed rounds and what is still missing.
- Never edit another module's folder. Core changes go through the integrator.
- Keep the dev server running and the app loadable at all times; other agents are screenshotting it.
- Do not ask me questions. Make routine decisions yourself, state assumptions, keep going.


```

```text
graph rag

Regular RAG gave the model your documents to answer from — then fell apart on "what are these documents even about?" It can find any sentence. It can't tell you what they add up to.

GraphRAG changes what's stored. Text units keep provenance so answers cite the exact passage. A model extracts entities and relationships into a knowledge graph. The Leiden algorithm groups it into a nested hierarchy of communities, and each community gets a summary report written up front — that's what answers a broad question without re-reading the corpus.

Quick lookup: plain RAG is fine. Sensemaking across the whole corpus: this is the machine that does it.
```
