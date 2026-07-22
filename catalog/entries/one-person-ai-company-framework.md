---
name: one-person-ai-company-framework
title: One-Person AI Company Framework
url: "https://www.reddit.com/"
category: agent-pattern
tags: [agent-pattern, solo-founder, automation, approval-queue, taste-loop, reversibility, operations]
reviewed: 2026-07-21
summary: ">-"
acquired: 2026-07-22
---

## What it is

A practitioner's framework distilled from operating a real business
(growth consulting for agencies/startups) almost entirely on AI agents
for six months, from a single git repo. Each principle includes both
what held up and where it broke.

### The 10 parts

1. **Context as code**: move the company to plain files in one repo where
   the AI reads/writes well; load context on demand to avoid context rot

2. **Routing brain**: one root file routes tasks to department folders,
   each with a plain-English playbook; single generalist + good playbooks
   beats a fleet of brittle specialists for most work

3. **Own core tools**: rebuild internal SaaS as small apps; hard daily
   caps in code (not prompts); verify every send by checking DOM before/
   after; never trust a platform's "success" response

4. **Senses**: nightly Scout (survey + brief), digesters (HN/Instagram/
   X/communities), hourly inbox monitors, signal farming; the company
   perceives the world through standing flows, not manual scrolling

5. **Copilot not autopilot**: nothing goes out unseen; fleet of proposers
   draft into one approval queue; human reviews via desktop or phone tap;
   every applied action logs back to CRM

6. **Draft ≠ touch**: every queue needs a live consumer, a depth
   indicator, and a backlog alarm shipped in the same change; a queue
   with no running consumer is worse than no queue

7. **Runner loop**: local scheduler fires proposers, drains queues,
   stamps heartbeat; needs failure markers, back-off, and a health
   check that goes red when the loop dies

8. **Reversibility discipline**: agents propose, deterministic gates
   decide; bots pull before working, never force-push main; add-only
   automations (follow, subscribe, enrol) need periodic prune + blacklist

9. **Taste loop**: document as you go, capture every decline with the
   reason written back into the producing playbook; edits-per-draft
   metric falls week over week — the difference between "I have
   automations" and "the company gets sharper without me"

10. **Deciding > building**: flip to ship-mode when the unshipped pile
    crosses a line; denominate daily loop in taps (scarce) not ideas;
    before building software to make something visible, check whether
    it is invisible or just unwanted

### Key failure modes documented

- Signal farming self-selects for sellers, not buyers
- A dead runner was invisible for days with no failure marker
- An agent acting on a stale checkout force-pushed main backwards
- Auto-follow without quality gate accumulated 481 irrelevant accounts
- 54 drafts, 1 published — building machinery > shipping
