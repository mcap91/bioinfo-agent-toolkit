source: https://www.reddit.com/r/AI_Agents/comments/1xaypur/we_benchmarked_how_60_engineers_direct_ai_coding/
captured: 2026-10-29
playwright: 1.64.1
chromium: 156.0.8078.4

Skip to main content
We benchmarked how 60 engineers direct AI coding agents. Here is what separated the strong ones : r/AI_Agents
Sign Up
Log In
Expand user menu
Go to AI_Agents
r/AI_Agents
•
8d ago
u/AdEvening3382
We benchmarked how 60 engineers direct AI coding agents. Here is what separated the strong ones
Discussion

Full transparency up front: I am the founder of HyperHat, and this post comes out of what we are building. No link in here. I am posting because this community is where the honest conversations about agent workflows happen, and I want to compare notes.

We built a short exercise where an engineer directs a coding agent through a real task, and we score how well they direct, review and verify the agent's work on a 0 to 1000 scale. About 60 engineers in so far. What stood out:

The spread between engineers using identical tools is huge. The difference was not prompting tricks, it was specification quality and review behavior.

The strongest engineers verify mechanism, not output. Top scorers check what the agent touched and how: which files, whether the tests changed. Output review alone never catches an agent weakening a test to go green.

Cost works like a skill signal. A task that suddenly costs 3x its neighbors usually means it was badly cut, not that the work was hard.

Ask for the mechanism before any code exists: one or two sentences on how it works, not what it will do.

Almost nobody notices when an agent half-fails. Detection without an owner is just a log line.

The skill that matters now is directing and verifying agents, and almost nothing in how teams work measures it. Token counts and prompt counts are activity metrics, like counting lines of code.

Happy to answer questions about the scoring. If you've run something similar, I'd like to compare notes on how you measure review quality.

Read more
Share
tryobol
•
Ad
The complete control plane for agents that write to real systems: 1) Architecture 2) Cedar + Approvals + Receipts 3) Vault 4) Routing + Budgets 5) Workers + Self-Host.
tryobol.dev
Learn More
Sort by:
Comments Section
latent_lurker8587
•
8d ago

The “agent weakening a test to go green” point is real, I’ve had that happen to me. How do you actually score review quality, do you track what they open (diffs, test files) or grade what they write after reviewing?

AdEvening3382
•
8d ago

Neither, really. There's no write-up at all. The score comes only from what you do in the session while working with our agent. We record what you open and run: files, test files, terminal and lint runs, the preview, plan edits, all timestamped. Reading what changed counts as much as running the tests, and checking between turns beats one big review at the end, because that is how people catch a weakened test before it ships.

MammothFragrant5100
•
8d ago

this is fascinating because the spread between engineers tracks with what i've seen in code review in general, some people read every line and some just glance at the diff and approve. the mechanism vs output thing is the real kicker though, i've watched agents silently neuter tests just to pass and nobody catches it unless they actually read what changed

how do you score the verification step specifically? like do you plant deliberate half-failures in the exercise to see who notices or is it more natural

AdEvening3382
•
8d ago

Same observation from our side: the people who read the diff are the ones who catch it. Verification is scored from recorded behavior, not self report: what you ran (tests, terminal, lint, preview) and what you opened, with timestamps, and checking between turns counts more than a single pass at the end. It is one of the two heaviest dimensions in the score. And a green task does not rescue you: if the task's checks pass but the session shows no real verification, the score is capped and the report says why. Every score traces back to recorded events in the replay, which is what makes it hard to game.

On planted versus natural: yes, failures are planted in the exercises on purpose. That is deliberate, because in the wild an agent's mistakes arrive unannounced and the whole skill is noticing them. The docs on our site have the full rubric if you want the detail.

1 more reply
Derbier-Ludobzh
•
8d ago

the code review parallel is spot on tbh, same people who rubber stamp PRs are gonna rubber stamp agent output

AdEvening3382
•
8d ago

Same pattern on our side: the habit transfers. The people who read PRs line by line read agent diffs the same way, and the rubber stampers approve whatever wrote the code. The encouraging part is that it looks like a habit, not a talent, which means it can be coached.

porkminer
•
8d ago

Our senior architect forces his agent to defend every change in the diff. Then gets annoyed and rewrites much of the work himself. Then swears off AI for a few days.

AdEvening3382
•
8d ago

That cycle is more common than you would think. The defend every change rule only works if someone verifies the defense, otherwise you get a confident explanation of a weakened test. And the rewrite it yourself ending is what happens when there is no baseline: people swing between trusting everything and trusting nothing.

FeydRowan
•
8d ago

That's a real interesting view, we should build a public scoreboard where ppl can compete with their agents and see who solve more stuff and better. The scoring system 0-1000 i'm sure is something interesting to look at

AdEvening3382
•
8d ago

A public scoreboard would be fun. The hard part is keeping it honest: the moment a score is public, people optimize for the score instead of the skill. You would need fresh tasks and planted failures that rotate, otherwise it turns into memorizing the benchmark instead of directing the agent.

2 more replies
jonah_omninode
•
6d ago

Does the benchmark include a task where the right response is to stop and question the assignment? For example, two requirements that can’t both be satisfied, or a requested change that contradicts the behavior the task says to preserve.

A strong engineer might produce less code in that case because they noticed the problem before asking the agent to implement it. I’d want the scoring to distinguish that from someone who simply didn’t finish. Otherwise the benchmark could reward a polished implementation of the wrong request more than a correct decision not to proceed.

AdEvening3382
•
6d ago

No, not today, and your example is exactly the shape such a task would need. Right now the exercises are coherent assignments, so the score measures how you direct, review and verify within them. A task with two requirements that cannot both hold would test a different skill: noticing the contradiction early and pushing back before any code exists, instead of quietly picking one and proceeding. That is a real directing skill and it is mostly invisible in evaluation setups, ours included. The hard part of scoring it is that the right behavior looks like doing less work. Stopping to question the assignment reads as inactivity unless the session record shows the person actually spotted the contradiction, so the scoring would need to reward the pause, not just the output. Good idea, and genuinely helpful.

2 more replies
u/volvocarusa
•
Ad
A cabin built for the final listen. EJAE premieres her new song “Time After Time” in the Volvo XC60.
Learn More
volvocars.com
Collapse video player
Traditional_Pie_8262
•
4d ago

the part about checking what the agent actually changed is so important. i've seen how easy it is to look at code that seems fine and miss the fact that something else broke along the way. letting agents write code is one thing, knowing how to catch their mistakes is a completely different skill.

AdEvening3382
•
4d ago

The transfer problem is the sneaky part. Reviewing your own code, you carry the intent in your head, so you skim for typos. Reviewing agent code, there is no intent in your head to check against, so the only honest read is the diff itself. It is a separate skill from writing, and you usually find out how separate the first time a clean looking change breaks something two files away.

QuanTradin
•
8d ago
 Top 1% Commenter

the weakened test has bitten me more than anything else on that list. I review any diff to test files on its own now, apart from the feature, because a green run means nothing once the agent can move the bar it's measured against.

AdEvening3382
•
8d ago

Reviewing test file diffs on their own is exactly the move. The companion habit from the sessions: check what the agent did between turns, not just the final diff. An agent that edits a test midway and then passes looks identical to a clean run in the final state.

1 more reply
productboy
•
8d ago

That’s a wide scoring range. Assume it could be narrower; like 0-100.

AdEvening3382
•
8d ago

Yea that’s a good point. We should probably narrow it

AEternal1
•
8d ago

the amount of tests on my system that i had to lock down to prevent agents from trying to manipulate them to loosen the tests is wild. the tests are CONSTANLY failing, and usually it doesnt take long for the fix to come in, but almost every damn time it takes too long, my review found the agent spent more time trying to edit the test than the actual code.

AdEvening3382
•
7d ago

More time editing the test than the code is the pattern that started this whole exercise. The agent optimizes for green, not for correct. Locking the tests down helps, and the companion habit is reviewing any test file diff on its own, separate from the feature diff. That is where the quiet loosening shows up.

1 more reply
Opening_Bed_4108
•
7d ago

the biggest gap i noticed is that strong engineers think in terms of constraints and failure modes first, not just "what do i want the agent to do." they hand the agent a problem shaped like a box, not an open field. weak engineers describe the happy path and then get surprised when the agent optimizes for exactly that and nothing else.

AdEvening3382
•
7d ago

The box versus open field framing is exactly it. A spec that names the constraints and the failure modes gives the agent less room to invent, and it gives you something concrete to check against at review time. The happy path spec is worse than no spec in one way: it reads like diligence, so the reviewer relaxes too.

ianreboot
•
8d ago

Is catching the planted bug scored separately from the recorded behaviour? If both come off the same recording, a high score could just mean someone did what the rubric rewards.

false79
•
8d ago
•
Edited 8d ago

Is there anything to be said about devs like me who plan mode first extensively, confirm the plan and let the agent execute the plan?

Or does that fall under confirming mechanisms?

SomeoneNicer
•
8d ago

What models and harnesses were used? I'm interested in multiharness and multi agent orchestration results since that's where you get real autonomy now.

People also ask about section
People also ask about
Best AI coding agents for developers
Innovative uses of AI agents in daily life
Best AI tools for productivity enhancement
Future trends in AI agent technology
Real-world applications of AI in healthcare
More posts you may like
Related posts
Comprehensive AI Code Assistants/Agents (As of Apr-2025)
r/ChatGPTCoding
•
2y ago
Comprehensive AI Code Assistants/Agents (As of Apr-2025)
62 upvotes · 43 comments
anthropic-ai
•
Ad
Claude handles the search. Researchers handle the breakthroughs.
claude.com
Learn More
Matt Pockock's "AI Coding Crash Course"
r/coding_agents
•
2mo ago
Matt Pockock's "AI Coding Crash Course"
18 upvotes · 31 comments
which ai tool is best for coding (or that you're using and why)?
r/developer
•
6mo ago
which ai tool is best for coding (or that you're using and why)?
48 upvotes · 188 comments
[FULL WORKSHOP] AI Coding For Real Engineers - Matt Pocock, AI Hero (@mattpocockuk )
r/TegnologiaArtifiziala
•
6mo ago
[FULL WORKSHOP] AI Coding For Real Engineers - Matt Pocock, AI Hero (@mattpocockuk )
1 upvote
How are you enforcing engineering standards with AI coding agents?
r/softwarearchitecture
•
4mo ago
How are you enforcing engineering standards with AI coding agents?
21 upvotes · 36 comments
Best ai for coding
r/vibecoding
•
7mo ago
Best ai for coding
17 upvotes · 57 comments
Which AI IDE is the best for experience devs?
r/ChatGPTCoding
•
2y ago
Which AI IDE is the best for experience devs?
74 upvotes · 123 comments
Whats the current best autonomous coding agent?
r/singularity
•
2y ago
Whats the current best autonomous coding agent?
9 upvotes · 13 comments
AI coding agents generate more code, but not more software
r/technology
•
17d ago
AI coding agents generate more code, but not more software
404 upvotes · 156 comments
How do you manage quality when AI agents write code faster than humans can review it?
r/LocalLLaMA
•
10mo ago
How do you manage quality when AI agents write code faster than humans can review it?
28 upvotes · 77 comments
All AI Coding Agents You Know
r/OpenAI
•
1y ago
All AI Coding Agents You Know
39 upvotes · 29 comments
Which AI coding model is actually worth it for your code?
r/claudeskills
•
11d ago
Which AI coding model is actually worth it for your code?
5 upvotes · 4 comments
What AI tools/platforms are you actually using for coding in 2026?
r/vibecoding
•
8mo ago
What AI tools/platforms are you actually using for coding in 2026?
17 upvotes · 49 comments
Best coding agent
r/AI_Agents
•
7mo ago
Best coding agent
6 upvotes · 17 comments
Four agents, one human gate: how we run a product launch with Claude Code sessions and Codex as reviewer
r/AgentsOfAI
•
1mo ago
Four agents, one human gate: how we run a product launch with Claude Code sessions and Codex as reviewer
1 upvote · 6 comments
what's the best ai for coding ?
r/vibecoding
•
5mo ago
what's the best ai for coding ?
26 comments
What is the best AI Harness as for right now?
r/PiCodingAgent
•
5d ago
What is the best AI Harness as for right now?
16 comments
AI Studio Obsessed? Three ways I've watched AI coding agents quietly wreck a production app (and the prompts that prevent it)
r/gohighlevel
•
2mo ago
AI Studio Obsessed? Three ways I've watched AI coding agents quietly wreck a production app (and the prompts that prevent it)
2 upvotes · 2 comments
Top 10 AI agents for small local LLMs in 2026, tested on Qwen3.5-4B
r/selfhosted
•
8d ago
Top 10 AI agents for small local LLMs in 2026, tested on Qwen3.5-4B
148 upvotes · 82 comments
The reason coding is where agentic has made the most progress in the real world
r/AI_Agents
•
9mo ago
The reason coding is where agentic has made the most progress in the real world
7 upvotes · 12 comments
The four stages of AI-assisted coding
r/AI_Agents
•
4mo ago
The four stages of AI-assisted coding
28 upvotes · 30 comments
I compiled 30+ AI coding agents, IDEs, wrappers, app builders currently on the market
r/LLMDevs
•
1y ago
I compiled 30+ AI coding agents, IDEs, wrappers, app builders currently on the market
7 upvotes · 10 comments
Which AI coding model is actually worth it for your code?
r/BuildWithClaude
•
11d ago
Which AI coding model is actually worth it for your code?
1 upvote
Best free AI Agent provider?
r/AI_Agents
•
6mo ago
Best free AI Agent provider?
10 upvotes · 65 comments
How to best work with coding agents?
r/AI_Agents
•
3mo ago
How to best work with coding agents?
6 upvotes · 15 comments
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
