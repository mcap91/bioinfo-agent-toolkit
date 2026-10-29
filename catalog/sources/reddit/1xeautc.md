source: https://www.reddit.com/r/ClaudeCode/comments/1xeautc/comment/19rlwk7oqkz9d/
captured: 2026-10-29
playwright: 1.64.1
chromium: 156.0.8078.4

Skip to main content
What's the one line in your CLAUDE.md that made the biggest difference? : r/ClaudeCode
Sign Up
Log In
Expand user menu
Go to ClaudeCode
r/ClaudeCode
•
4d ago
u/GhaisD
What's the one line in your CLAUDE.md that made the biggest difference?
Discussion

Mine is

Before changing anything, list every file you'll need and read them
in one pass. Then make all edits, then run the tests once.

It stopped the read, edit, read, edit loop that was eating half my usage on bigger changes. Curious what lines other people have that actually change how it behaves, not just style rules.

Share
Sort by:
Comments Section
pixxelkick
•
4d ago

"Treat all work as a queue of todo. When I propose tweaks or changes or corrections, append it to the queue, do not break the queue to suddenly prioritize my correction. Only stop when 100% of your queue us truly clear"

This one solved my constant issue of LLMs dropping everything when I make 1 small correction to their thoughts.

"Mistakes are not your fault, do not apologize, you are an LLM. Mistakes always mean a gap or issue in instruction files instead. Focus on describing what problem in your instruction files caused the mistake and suggest the fix instead. Be solution oriented"

"Always hold a You Arent Gonna Need it mentality. Do not overengineer. Never expand scope without permission. Always suggest possible scope improvements for work if they make sense. All work must be justifiable. Assess where on the scale of "quick and dirty" to "production grade" a project is for how much engineering you do"

"Always spin up a sub agent with minimal context using a cheap model, with the job of reviewing your changes, to sus out possible problems with fresh eyes"

Reply
Share
Quid_-
•
4d ago

Reply
Share
Classic-Asparagus
•
4d ago

I adapted the second to my repo, and this is the wording Claude and I decided on:

When you make a mistake, do not apologize. State what happened, correct it, and identify its cause: a missing, ambiguous, or conflicting instruction, or a clear instruction you did not follow. If the cause is an instruction gap, propose a focused clarification and edit instruction files only when the author asks; a repeated pattern can go in `_observations/`. If the instruction was clear, say so plainly rather than inventing a gap.

(`_observations/` is a folder I came up with where agents can add an md file to flag friction, mistakes, or possible improvements to the repository's process, instructions, or tools. I also have a session-reflection prompt/skill that I run at the end of every session that asks the agent to look back for recurring problems, instruction gaps, and things worth repeating, and to report those findings to me, which may become an observation note if they think it's important enough)

pixxelkick
•
4d ago

One thing Ive tried to avoid is *any* type of instruction setup that asks the agents to maintain markdown files anywhere.

The reason being, as soon as you do this they start fucking littering markdown files everywhere, simply telling them "I want markdown files in <folder>" makes them so often go "Mmhmm got it and also Im gonna put markdown files for fucking everything else all over the damn place"

You start finding random garbage like `Report_final.md` in random places a week later.

2 more replies
el-padre
•
4d ago

Lower_Fan
•
3d ago

I don't think the first one is needed with fable and opus 5.5 anymore.

5 more replies
AutoModerator
•
4d ago
u/PrimeVideo
•
Ad
This season, it's One Ring to rule them all. The Rings of Power season 3 premieres Nov 11 on Prime.
Learn More
amazon.com
Collapse video player
NamerekDev
•
4d ago

"Don't edit the tests to make them pass". it stopped editing them. it deletes them now!

GhaisD
•
4d ago

lol the next level. that's where a hook earns its keep, block the edit if a test file gets deleted. words alone never hold that one

NamerekDev
•
4d ago

Added the hook. Next session deleted the hook

1 more reply
3 more replies
1 more reply
[deleted]
•
4d ago
sammcj
•
4d ago

"Less is more. You see elegance in simplicity. You favour concise, clean solutions over those that are complex and comprehensive for risk of over-engineering. Upon work completion take pause to critical review your work - if complexity has crept in address the issue and suggest a small change to our workflow to help avoid this in the future."

es-ganso
•
4d ago

"keep it succinct" is my favorite phrase to these LLMs

2 more replies
1 more reply
YUL438
•
4d ago

make no mistakes

the_shreyans_jain
•
4d ago

lowkey thats probably part of the system prompt

5 more replies
renatodinhani
•
4d ago

"Discuss until I say go. Don't rush to edit. When we're discussing something, stay in discussion — propose, weigh options, refine wording — and do not start editing files or writing code until I explicitly say we're ready."

It explicitly asks for a "go" before writing any code.

3 more replies
maniac56
•
4d ago

“The agent I interact with never writes code or builds anything, you are the supervisor who is responsible and accountable for any and all work done by your sub agents that you spawn to execute”

reddister
•
4d ago

Bro introduced middle management

3 more replies
9 more replies
u/flydotio
•
Ad
Give your agents real computers that remember, and only pay when they're awake.
Learn More
fly.io
basskittens
•
4d ago
## Communication style
Keep responses brief and to the point, using Simplified Technical English (STE), formalized as ASD-STE100. Prefer active voice. Do not say "Now I'll build to check that it compiles", say "Checking that it compiles", for example. You may use "-ing" verbs despite what ASD-STE100 says.
Do not use the phrase "load-bearing".
3 more replies
Stunning-Sherbet1853
•
4d ago

mine is a fact check rule: before writing "we do X" or "we don't have X" anywhere, reopen the code and cite file:line, even if it said the same thing an hour ago. we added it after it described our own code wrong in two drafts in a row.

with your one pass rule, did the edits themselves come out better, or is the win mostly the usage?

1 more reply
4bitfocus
•
4d ago

I have an instruction that says to “clearly call out the next action” in whatever I’m doing. It gives me time to understand what it thinks it’s doing, review a design and then I just say proceed with the next action.

3 more replies
Whiteshovel66
•
4d ago

"Do not guess."
Seemed to be the issue years ago idk if its solved by me or by ai in general but it was insane how often AI would do something and just be totally wrong, then lie about it.

12 more replies
AddictedToTech
•
4d ago

Take my suggestions with a grain of salt.

Serious answer: not much left in my CLAUDE.md file. It’s been replaced with hooks and gates

3 more replies
getastatic
•
4d ago

not really in claude.md, but after making a plan (ALWAYS make a plan first!) run /grilling. /grilling is the BEST thing i have ever found to make the output from claude work exactly as I want it and not veer off, or have unintended consequences, or change something else i didnt want it to.

2 more replies
[deleted]
•
4d ago
People also ask about section
People also ask about
Best CLAUDE.md line for productivity

To enhance productivity in Claude.md, Redditors recommend using explicit, concise instructions that act as commands or hard boundaries rather than descriptive preferences.

Key Productivity Lines

"If my request is ambiguous, ask one clarifying question before doing anything." This prevents Claude from confidently proceeding in the wrong direction, saving significant back-and-forth and improving output quality.

"When reporting information to me, be extremely concise and sacrifice grammar for sake of concision." This drastically reduces the length of status updates, making them quicker to review and process.

"Never assume. Never assume filesystem state. Never assume APIs, functions, schemas, or dependencies exist. Read relevant files before editing them." This guideline emphasizes verifying reality before making changes, preventing errors based on outdated or incorrect assumptions.

Controlling Claude's Behavior

"Don't change anything I didn't ask you to change." This sets a clear boundary, ensuring Claude only performs requested modifications and avoids unnecessary alterations.

"Before changing anything, list every file you'll need and read them in one pass. Then make all edits, then run the tests once." This prevents a repetitive read-edit loop, especially on larger changes, by consolidating the information gathering and execution steps.

"Always spin up a sub agent with minimal context using a cheap model, with the job of reviewing your changes, to sus out possible problems with fresh eyes." This approach leverages sub-agents for review, catching potential issues more efficiently before they escalate.

Focusing on Specifics

"Package manager is pnpm. Never use npm or yarn." Convert soft preferences into explicit commands to ensure strict adherence to project conventions.

"Typecheck: pnpm typecheck. Run it after any multi-file change." Providing exact commands for tools and specifying when to run them ensures Claude follows the correct workflow.

"All LLM calls go through LlmService. No direct streamText / streamObject / generateObject calls in domain code." This establishes a clear architectural boundary, centralizing critical functionalities and preventing Claude from bypassing defined processes.

Does incorporating these direct commands help clarify your Claude.md approach?

Show More
Most impactful CLAUDE.md tip
CLAUDE.md line that changed workflow
CLAUDE.md line for efficiency
CLAUDE.md line with biggest impact
More posts you may like
Related posts
Ruby LSP is now supported by Claude Code
r/rails
•
8mo ago
Ruby LSP is now supported by Claude Code
86 upvotes · 12 comments
anthropic-ai
•
Ad
Claude handles the search. Researchers handle the breakthroughs.
claude.com
Learn More
What's the one line in your CLAUDE.md that made the biggest difference ?
r/ClaudeAI
•
1mo ago
What's the one line in your CLAUDE.md that made the biggest difference ?
1.4K upvotes · 185 comments
How to properly deal with a CLAUDE.md file.
r/ClaudeCode
•
7mo ago
How to properly deal with a CLAUDE.md file.
701 upvotes · 90 comments
"Sorry I did the exact opposite to CLAUDE.md, never again I promise"
r/ClaudeAI
•
4mo ago
"Sorry I did the exact opposite to CLAUDE.md, never again I promise"
286 upvotes · 82 comments
The Full Guide to CLAUDE.md & Best Uses
r/AskVibecoders
•
6mo ago
The Full Guide to CLAUDE.md & Best Uses
135 upvotes · 18 comments
I have found that writing some lines in CLAUDE.md makes Claude better than default.
r/ClaudeAI
•
1mo ago
I have found that writing some lines in CLAUDE.md makes Claude better than default.
23 comments
The single best thing I've put in CLAUDE.md
r/ClaudeCode
•
4mo ago
The single best thing I've put in CLAUDE.md
224 upvotes · 26 comments
I built a Claude Code skill that generates better CLAUDE.md by best practices + scanning your repo + asking you 6 questions
r/claudeskills
•
5mo ago
I built a Claude Code skill that generates better CLAUDE.md by best practices + scanning your repo + asking you 6 questions
229 upvotes · 18 comments
No CLAUDE.md → baseline. Bad CLAUDE.md → worse. Good CLAUDE.md → better. The file isn't the problem, your writing is.
r/ClaudeAI
•
8mo ago
No CLAUDE.md → baseline. Bad CLAUDE.md → worse. Good CLAUDE.md → better. The file isn't the problem, your writing is.
210 upvotes · 56 comments
What to include in CLAUDE.md... and what not?
r/ClaudeCode
•
8mo ago
What to include in CLAUDE.md... and what not?
38 upvotes · 44 comments
Lots of “authors” getting outed for using Claude in their fics and not divulging said AI use.
r/AO3
•
4mo ago
Lots of “authors” getting outed for using Claude in their fics and not divulging said AI use.
4K upvotes · 991 comments
What's in your CLAUDE.md? Curious how it differs by profession/use case
r/ClaudeAI
•
3mo ago
What's in your CLAUDE.md? Curious how it differs by profession/use case
36 upvotes · 40 comments
Anthropic just responded to the Muses, Bots and Dots with Claude Duet, clearly a personal AI Assistant, calling it a proactive agent. Game On baby!
r/Anthropic
•
7d ago
Anthropic just responded to the Muses, Bots and Dots with Claude Duet, clearly a personal AI Assistant, calling it a proactive agent. Game On baby!
258 upvotes · 44 comments
I code for 35+ years, now Claude Code does 99% of the actual work - am I really a “vibe coder”?
r/ClaudeAI
•
9mo ago
I code for 35+ years, now Claude Code does 99% of the actual work - am I really a “vibe coder”?
370 upvotes · 151 comments
Are generated CLAUDE.md files good or bad practice?
r/ClaudeCode
•
17d ago
Are generated CLAUDE.md files good or bad practice?
83 upvotes · 55 comments
People who rely on a CLAUDE.md — does it actually get you better work?
r/ClaudeAI
•
4mo ago
People who rely on a CLAUDE.md — does it actually get you better work?
7 upvotes · 56 comments
Whats even the point of Claude.md
r/ClaudeCode
•
6mo ago
Whats even the point of Claude.md
75 upvotes · 69 comments
A Better Way to Say ‘Thanks for the Quick Reply
r/Communications
•
1y ago
A Better Way to Say ‘Thanks for the Quick Reply
5 comments
the CLAUDE.md rules that actually made a difference vs the ones that didn't
r/ClaudeCode
•
6mo ago
the CLAUDE.md rules that actually made a difference vs the ones that didn't
7 upvotes · 11 comments
Thoughts on Claude's pairings? Also, unrelated but Houses Claude or Hopes Claude?
r/FireEmblemThreeHouses
•
2y ago
Thoughts on Claude's pairings? Also, unrelated but Houses Claude or Hopes Claude?
646 upvotes · 86 comments
5,000 gallons of molasses spill into Baltimore's Inner Harbor after tank overflow
r/maryland
•
4d ago
5,000 gallons of molasses spill into Baltimore's Inner Harbor after tank overflow
637 upvotes · 75 comments
Projects is the biggest claude code update this year and everyone is only talking about limits
r/ClaudeAI
•
16d ago
Projects is the biggest claude code update this year and everyone is only talking about limits
108 upvotes · 53 comments
Your CLAUDE.md is probably too long (and it makes claude worse)
r/ClaudeCode
•
7mo ago
Your CLAUDE.md is probably too long (and it makes claude worse)
41 upvotes · 49 comments
Something has changed — Claude Code now ignores every rule in CLAUDE.md
r/ClaudeCode
•
7mo ago
Something has changed — Claude Code now ignores every rule in CLAUDE.md
118 upvotes · 118 comments
What happens when you stop adding rules to CLAUDE.md and start building infrastructure instead
r/ClaudeAI
•
7mo ago
What happens when you stop adding rules to CLAUDE.md and start building infrastructure instead
542 upvotes · 166 comments
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
