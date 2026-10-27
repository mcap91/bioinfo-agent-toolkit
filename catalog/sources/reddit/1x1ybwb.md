source: https://www.reddit.com/r/ClaudeCode/comments/1x1ybwb/best_way_to_handle_cold_cache_hits_you_overpay_5x/
captured: 2026-10-27
playwright: 1.64.1
chromium: 156.0.8078.4

Skip to main content
Best way to handle Cold Cache hits - You overpay 5x for typing "Continue" : r/ClaudeCode
Sign Up
Log In
Expand user menu
Go to ClaudeCode
r/ClaudeCode
•
17d ago
u/EagleApprehensive
Best way to handle Cold Cache hits - You overpay 5x for typing "Continue"
Tips & Workflows

I'm a meta-harness developer. For few months already I'm working on the most token-efficient AI workspace there is. Based on my benchmarks (run with Opus 5.5 XHigh), if you resume cold-cache session just by typing "Continue", you're overpaying 5x in tokens for that turn.

Obviously it's best to prevent cold caches in first place - by good UX (notifications and nice UI showing you session is about to hit cold cache), automatic cache-warming and so on. But sometimes, cold cache hits are inevitable, so I was researching best possible solutions to handle that as well.

So far I've had a very aggressive trimming mechanism that didn't invoke any model call (that would increase cost) and in purely deterministic algorithm was trimming parts of conversation to carry on without the bloat.

As Haiku 5.5 shown up with much cheaper cost, I decided to revisit topic.

Based on benchmarks and tests I settled on 150k context as meaningful breaking point for distinguishing between short/long sessions. Below 150k - "Continue" is totally cool. After 150k, things get complicated.

Trimming (replacing older tool results with one-line stubs, stripping thinking blocks etc. without extra model call) is actually best. But it does not work for cross-provider handling, because formats that different providers use for session recordings are incompatible.

So the rule of thumb becomes:

Prefer trim on same-provider because you can resume a trimmed Claude session and it beat seed/compact on memory of the work.

Prefer compact on cross-provider because trim is not available.

Hopefully it helps those of you who build harnesses/CLI tools.

Read more
Share
anthropic-ai
•
Ad
Reclaim your mornings for the work that matters with Claude.
Learn More
claude.com
Collapse video player
Sort by:
Comments Section
AutoModerator
•
17d ago
puts_on_rddt
•
17d ago

I'm a meta-harness developer. For few months already I'm working on the most token-efficient AI workspace there is.

buddy get in line lol

5 more replies
herzkerl
•
17d ago

I had Claude write a mod that automatically calculates whether or not a specific session should clear itself, depending on model, total tokens, number of turns, and cache age.

The session will then write a handover, clear itself, and read the handover, then continue.

It also keeps the session warm by pinging every 58 minutes when I’m not in ‘away mode’.

3 more replies
Wrong-Expression-669
•
17d ago

typing "Continue" isnt what costs you 5x, the cold cache is. you pay the same re-read of 400k tokens if you type "refactor the auth module" or a single period. the word has nothing to do with it and framing it like the magic phrase matters just makes it sound like you can whisper the right incantation at the model

and 10.68 for carry everything on ONE turn. at 400-700k you're basicly paying a dollar per 50k of your own history back, thats not a harness problem thats a "why is there 700k of stuff in here" problem. honestly /clear and re paste beats that, its manual and it sucks and you lose the thread, i know, i do it

the part that gets me tho is the table, your deterministic trimmer that you built over months and that calls no model comes out at 3.61 while two cents of Haiku plus the last 2 exchanges is 2.48 and one of those also gives you something readable at the top of the window. so all that machinery to avoid a model call is losing to the model call. be honest, how much of the last few months went into the trimmer wich the cheap summary just beat

EagleApprehensive
•
17d ago

Yeah, obviously it's not about typing "Continue", but about leaving session unattended for >1h.

Doing trimmer was the same amount of work as would be doing the "cheap Haiku summary" work. Coding is nowadays more about pointing AI in a smart way to various issues and grinding better UX, so wasn't that much of effort.

The biggest win is UX, that user does not need to think or know about /clear, /compact or repaste, because GUI guides him to best options in smart way. Also it won't beat that, model will not have enough context and will likely search the past session to get enough, which will cost you extra. I could benchmark that for you but good benchmarks are really expensive.

2 more replies
Scared-Letterhead949
•
17d ago

Opus 5.5 is so cheap I don't think it matters anymore.

Downtown-Pear-6509
•
17d ago

it does in a corporate setting with limited claude budget

vAPIdTygr
•
17d ago

Took me 36 hours with Opus/Sonnet to blow through my 20x weekly usage.

But that was it running nonstop overnight, building about 1,000 highly researched html pages. That research is a huge part of the budget.

7 more replies
6 more replies
cafesamp
•
17d ago

or just have an orchestrator agent keep track of your last message times and send pings to sessions that are about to go cold. really easy to build

EagleApprehensive
•
17d ago

I already have that, but the issue is that you need to reserve like 1% of usage limit to stay saved for pings and I also don't hard-block users from spending that last 1% or disabling auto-pings.

Declwn
•
17d ago

I don’t want anthropic to patch this but it’s really not that complicated, this mod keeps the cache warm without any messaging and costs almost nothing github.com/declanbx/keepwarm

1 more reply
u/flydotio
•
Ad
Give your agents real computers that remember, and only pay when they're awake.
Learn More
fly.io
wea8675309
•
17d ago

This is only for the initial turn. Not saying that doesn’t matter, but opening a cold cache only knocks you once, and after that it’s the normal rate with perfect context, which can save you tokens in the long run. Not always, but worth considering.

So you’re saying if I want to open a session from yesterday, I can have haiku summarize it and pass that summary to a new opus session instead? And that’s 90%+ accurate and beats whatever state management solution you have tried? That’s very interesting, thank you.

I have found that a simple SDLC process using GH issues and comments beats anything else I’ve tried. Intentionally tracking your work through plan -> design -> build -> test -> deploy phases and sorting all of the important stuff from each phase on GH issues not only saves state and manages your context across sessions, but it also forces you as the human to organize your work into shorter sessions.

But there are still times where something comes up in the middle of a session and starting a cold session would be very inconvenient, so this will be very helpful later I’m sure!

EagleApprehensive
•
17d ago
•
Edited 17d ago

In a nutshell yes, cheap-model summary wins. Minor exception is smaller context sizes, where trimming wins. Model generally prefers to continue on a log it has written itself before than summary, but above 150k context it stops being economically feasible (in cold sessions).

I generally run my work on kanban - just with 3 columns: attention / active / finished, balancing CPU/memory and available model usages. PR's, logs from environments (posthog, sentry, komodo, PC-access) etc., are just sources of extra data that model collects into session. But the session is my main point of focus.

I don't stick to strict Plan -> Design -> Build -> Test process - I let model figure out what's the best process, what models from what providers to use for what and orchestrate that as architect.

But I do have some automated checks, for example if model has changed UI and in entire session he didn't run browser to see if it doesn't glitch/look good, I have a hook to prompt him to verify the work - these kind of things highly improve efficiency and quality of work delivered, especially by weaker models than Opus 5.5 or when you choose lower effort than suitable for task.

2 more replies
Downtown-Pear-6509
•
17d ago

i do  a local compact by grabbing the jsonl and rhen removing thinking and tool output, doing a /clear  and pasting it back in

works for me!

and i can do this while hopping to another llm like clsude to openai and back

leemic
•
17d ago

what local model do you use to compact? or just removing thinking and tool output?

1 more reply
17 more replies
Substantial-Thing303
•
17d ago

subagents use a 5 minutes cache. less expensive until you ask subagents to run tests or any kind of compute, where they constantly hit a cold cache. I asked my agent to monitor any compute they intend to do that could extend to more then 5 minutes, and wake up every 4 minutes. And also, if the compute is expected to take more than 12 minutes and tokens over 200k, to write a handoff, so another agent starts fresh and run the script.

Odd_Antelope9098
•
17d ago

What? Just /export and have GPT chat give you a handoff summary with key file locations, completed/active/pending work, and important execution details.

2 more replies
Dapper_Profession
•
17d ago

the cache is prefix based though, so trimming something out of the middle invalidates every turn after it, you pay a fresh write of the whole tail instead of just the cold read. dropping from the tail keeps the prefix intact. thats why a summary spliced into the middle usually costs more than it saves

EagleApprehensive
•
17d ago

Yes, that's why this flow only makes sense for cold cache hits. Doing such on warm cache would increase costs.

brahmin_baniya
•
17d ago
Downtown-Pear-6509
•
17d ago

another top tip is for your meta harness to freeze a session when the cache cools to stop accidentally billing yourself in the foot

here's my commit in my actual harness, plus a bunch lster too

https://github.com/PetePeter/helm/commit/01a490a36cfa1377b8edf202330e251340c9cb79

EagleApprehensive
•
17d ago

What do you mean by "freeze"? Generally when user has session that went cold, he just gets buttons as options:

Trim cold session and continue

Compact with Haiku 5.5 (or other model) and Continue

Continue from full transcript (expensive)

The default is set in options, so typing and sending next message on for example old session, without explicit choice will also apply best hand-off mechanism.

2 more replies
MillerBurnsUnit
•
15d ago

Couldn't you just use a plug in to create a "heartbeat" every X seconds to prevent cold cache?

1 more reply
Ctbhatia
•
17d ago

the api also has a 1 hour cache ttl, 2x on the write instead of 1.25x for the 5 minute one. if your gaps are longer than 5 minutes but under an hour, paying the 2x once beats re-reading the whole thing at full price.

People also ask about section
People also ask about
Understanding prompt cache warm in ClaudeCode
Innovative projects using Claude code
Best practices for coding with AI
Tips for troubleshooting Claude code issues
How to optimize workflows with Claude code
More posts you may like
Related posts
Any tips for typing with long nails?
r/Nails
•
4y ago
Any tips for typing with long nails?
259 upvotes · 70 comments
Roblox
•
Ad
Heroes aren't born. They're built here. Discover action games on Roblox.
roblox.com
Play Now
Sharing My Agy-Cli harness Setup
r/GoogleAntigravityCLI
•
2mo ago
Sharing My Agy-Cli harness Setup
25 upvotes · 10 comments
Good typing/learn to type games for beginners?
r/gamingsuggestions
•
3y ago
Good typing/learn to type games for beginners?
47 upvotes · 48 comments
What are good websites to use to practice typing?
r/typing
•
3y ago
What are good websites to use to practice typing?
41 upvotes · 58 comments
For anyone experiencing clumsy typing (especially if you’re a fast typer) Try turning off character preview, 80% increase in better typing
r/ios
•
16d ago
For anyone experiencing clumsy typing (especially if you’re a fast typer) Try turning off character preview, 80% increase in better typing
2.3K upvotes · 570 comments
Your Claude Code prompt cache drops from an hour to five minutes the second you pass your plan limit
r/ClaudeCode
•
11d ago
Your Claude Code prompt cache drops from an hour to five minutes the second you pass your plan limit
19 upvotes · 10 comments
Determining if attack hits?
r/DnD
•
3y ago
Determining if attack hits?
9 comments
Name your Top 3 favourite Typing Sites!
r/MechanicalKeyboards
•
9mo ago
Name your Top 3 favourite Typing Sites!
286 upvotes · 139 comments
Is magegee hot-swappable?
r/keyboards
•
4y ago
Is magegee hot-swappable?
1 upvote · 2 comments
Cachebeat – keep your Claude Code prompt cache warm while a session is idle
r/ClaudeAI
•
1mo ago
Cachebeat – keep your Claude Code prompt cache warm while a session is idle
142 upvotes · 41 comments
I built a Claude Code plugin that keeps your prompt cache warm, so you stop paying to rebuild it
r/ClaudeAI
•
13d ago
I built a Claude Code plugin that keeps your prompt cache warm, so you stop paying to rebuild it
29 upvotes · 13 comments
Claude Code Compacts Automatically Before Cache Expires, THANK YOU!
r/ClaudeAI
•
18d ago
Claude Code Compacts Automatically Before Cache Expires, THANK YOU!
222 upvotes · 28 comments
I am stuck. How to improve my typing speed?
r/learntyping
•
3y ago
I am stuck. How to improve my typing speed?
23 upvotes · 19 comments
Keep Claude Code’s 1-hour cache warm during breaks. On Fable 5.1, rewriting it costs 80x a cache read.
r/ClaudeCode
•
1mo ago
Keep Claude Code’s 1-hour cache warm during breaks. On Fable 5.1, rewriting it costs 80x a cache read.
235 upvotes · 61 comments
Ange Floette stretches the limits of what can be considered a Pokémon and our understanding of Pokémon biology
r/pokemonconspiracies
•
1y ago
Spoiler
Ange Floette stretches the limits of what can be considered a Pokémon and our understanding of Pokémon biology
109 upvotes · 20 comments
How to type fast (from someone who types 145 words per minute)
r/productivity
•
6y ago
How to type fast (from someone who types 145 words per minute)
558 upvotes · 74 comments
I built a free (and ad free) website for typing practice that targets your weaknesses
r/MechanicalKeyboards
•
1y ago
I built a free (and ad free) website for typing practice that targets your weaknesses
1.4K upvotes · 206 comments
Someone at Anthropic shared his tips on caching and I made it into a skill
r/ClaudeCode
•
8mo ago
Someone at Anthropic shared his tips on caching and I made it into a skill
108 upvotes · 23 comments
I completed 2300 races in Typeracer. Here's how my WPM changed over time. Thought some might be interested.
r/typing
•
2y ago
I completed 2300 races in Typeracer. Here's how my WPM changed over time. Thought some might be interested.
18 upvotes · 15 comments
Is type racer recommended?
r/typing
•
2y ago
Is type racer recommended?
9 upvotes · 12 comments
How's my typing method is called ?
r/typing
•
3y ago
How's my typing method is called ?
12 upvotes · 18 comments
Is there a name for when the ball hits the net, stops and drops over?
r/Pickleball
•
14d ago
Is there a name for when the ball hits the net, stops and drops over?
55 upvotes · 135 comments
I'm so genuinely cooked
r/typing
•
13d ago
I'm so genuinely cooked
49 upvotes · 87 comments
Ergonomics: Wrist Rest + Elbow Support?
r/ErgoMechKeyboards
•
2y ago
Ergonomics: Wrist Rest + Elbow Support?
124 upvotes · 34 comments
Help! Notebooks & typing
r/typewriters
•
6y ago
Help! Notebooks & typing
5 upvotes · 12 comments
VIEW POST IN
Français
Português (Brasil)
See more
Public
Home
Popular
News
Explore
Best of Reddit
Best of Reddit in Portuguese
Best of Reddit in German
Reddit Rules
Privacy Policy
User Agreement
Your Privacy Choices
Accessibility
Reddit, Inc. © 2026. All rights reserved.

Join the most real place on the internet

 Sign in with Apple
Continue with Phone Number
Continue with Email

By continuing, you agree to our User Agreement and acknowledge that you understand the Privacy Policy.
