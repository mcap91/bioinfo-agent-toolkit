source: https://www.reddit.com/r/vibecoding/comments/1wyxpef/look_what_i_built/
captured: 2026-10-27
playwright: 1.64.1
chromium: 156.0.8078.4

Skip to main content
Look what I built 😃 : r/vibecoding
Sign Up
Log In
Expand user menu
Go to vibecoding
r/vibecoding
•
21d ago
u/Ok_Violinist9366
Look what I built 😃
Showcase/Project

I do everything in it now. Every doc, every project, all in one place. And when I switch from Claude to Codex, Codex already knows what Claude did.

How I made it: mostly Claude Code, sometimes Codex. I built salt.md inside salt.md. Every task gets a page, the agent reads the rules there, does the work and leaves notes on the page. When I switch tools, the next one reads the notes and just keeps going.

Biggest lesson: make the agents write down why they did something, not just what.

Even the video is made with Claude Code (HyperFrames + ElevenLabs).

https://github.com/saltmd/salt.md

https://salt.md

Share
anthropic-ai
•
Ad
Claude can help you take whatever's in your imagination—however strange or specific—and actually build it. Not just a version of the idea, but the thing itself, brought into the real world the way you originally pictured it.
claude.com
Collapse video player
Sort by:
Comments Section
OkCommunity6018
•
21d ago

You’re out here making shared markdown notes look like Tony Stark initializing the Jarvis core 😂 it looks very interesting, but I am not gonna lie, I came strictly for the animation. How did you build it? Did you use HyperFrames, and can you drop the prompts?

Ok_Violinist9366
•
21d ago

Yes, HyperFrames 😃 Built it with Claude Code Opus 5.5. The first prompt was just this (translated, I wrote it in German):

> Make a HyperFrames marketing video. Use ElevenLabs for music and voiceover, everything in English, and if possible use Jev from TypeSafe to check how the script lands. 30-45 seconds is enough, it has to be modern with a wow effect.

Then three rounds of feedback, like "needs more action, the cube should explode like in the hero on my website". That's it.

IAmFitzRoy
•
20d ago

Can you expand about the use of Jev on this?

2 more replies
4 more replies
1 more reply
FIGHT_and_WIN
•
21d ago

Watching the video, i thought it was going to change my life.
Then go to the comments and it's just markdown notes 😅

Ok_Violinist9366
•
21d ago

😂

TheOwlHypothesis
•
21d ago

The video is pretty. I watched without sound.

You need to fix it because this does NOT tell me what the fuck this is. I saw "all this for notes" and could infer this is probably some obsidian competitor but nothing else told me that and then I saw a kanban board and said "wtf?"

Ok_Violinist9366
•
21d ago

Fair point.

Lazy_Cattle3149
•
21d ago

I still don't understand what it does even scrolling trough the website. 

Ok_Violinist9366
•
21d ago

Fair 😃 Simply put: it's a markdown tool with MCP. You write your notes and docs in it, and your AI (Claude, Codex, Cursor...) can read and write the same pages. So when I switch from Claude to Codex, Codex just reads what Claude already did.

7 more replies
1 more reply
u/ClickUp_App
•
Ad
My boss thinks I got more organized. I just found one app that does everything.
View More
clickup.com
Sprinkles-Pitiful
•
21d ago

Is this a video or 3d animation?

Ok_Violinist9366
•
21d ago

Both. It's a video, but made from code. The exploding cube is real 3D (three.js, same as on my website), the rest is HTML with real screenshots of the app. HyperFrames renders it all into an mp4, and Claude Code wrote all of it.

LordUSB
•
21d ago

Great design! I like the idea.

Is it possible to use some kind of mobile app - do you plan to build it?

You should add serach in https://salt.md/wiki/.

Ok_Violinist9366
•
21d ago

Thanks 😃 Good idea. Right now you can only search the wiki through an agent, but a normal search would make sense too. On mobile it already works as a PWA, so just add it to your home screen. A native iOS app in Swift is the next step. Android I don't have much experience with yet.

ahmadparizaad
•
21d ago

O have been using CHANGELOG.md and DECISIONS.md

But for bigger projects these are not sufficient

Ok_Violinist9366
•
21d ago

Same here, that's exactly why I built it 😃 Instead of one big CHANGELOG.md, every task gets its own page and the agents leave notes on it. So the next session or the next agent just reads the page and knows what happened and why.

xebelah
•
21d ago

I often give truth advice (following concepts like this) to token abusers, AI abusers and other abusers who are looking for free tokens with many accounts and Yep they are never productive even though they have many AI tokens 😹😹

Ok_Violinist9366
•
21d ago

😂 true. More tokens don't help if every session starts from zero.

SnooBananas8485
•
19d ago

Man! This presentation is killer!!! Im a founder and I'll respectfully use your approach and mention you! Heck, you did an amazing job. I was sold before even understanding the product.

Ok_Violinist9366
•
19d ago

Thanks 😊

PeachScary413
•
21d ago

Obsidian at home 🤌👌

1 more reply
grokcodile
•
20d ago
•
Edited 20d ago

I like this, but I’m not sure why I would need it?

How is this really any better than just having a /documentation folder or git submodule where you can keep all this kind of stuff in each project/repo you are working on?

This is a serious question... because the website does not do a good job of explaining the problem this solves. All the website does is talk about all of its functions and way too much about how it works. I think you can sum up the entire website with:

Salt.md is a self-contained documentation server for your team dev projects, with a bundled native desktop app for easy editing, and first-class support for working alongside AI agents efficiently.

Is that even close to correct? If so... you can delete half of the stuff on the homepage by just stating that and explicitly outline what problems this really solves and what benefit it offers. Also... how it compares to other options... because that is what people are doing when finding or evaluating a solution, and seeing content outlined this way really helps people understand the value in terms that are relevant to them in a transparent way without having to discern it themselves based on features and descriptions of how it works. This is all still informative and useful... but only if that first question is answered.

u/OpenAI
•
Ad
Meet your new collaborator. Whether you’re analyzing, brainstorming, or drafting, you can do it all with ChatGPT Business.
Sign Up
chatgpt.com
bara_tone
•
21d ago

Why does your "back to basics" note service need a 3D animated trailer? 🫠

Ok_Violinist9366
•
21d ago

Why not 😂 We're all in this sub because we code with AI, so why not show your experiments too. The tool stays simple, the trailer was just me testing what's possible.

3 more replies
kilopeter
•
20d ago

The exploding prismatic dispersion shows the light spectrum backwards, with red light erroneously bending the most, and violet light bending the least.

Literally unwatchable /s

bryanr29
•
21d ago

The real sauce is how to make a nice video like this using HyperFrames.

People also ask about section
People also ask about
Overview of Claude Code and Codex integration
Best alternatives to Hyperframes
Comparison of Remotion and Hyperframes
Innovative AI tools for creative coding
Unique programming languages to explore
More posts you may like
Related posts
This is the way.
r/vibecoding
•
8mo ago
This is the way.
154 upvotes · 6 comments
anthropic-ai
•
Ad
Claude handles the search. Researchers handle the breakthroughs.
claude.com
Learn More
In a nutshell
r/vibecoding
•
4mo ago
In a nutshell
234 upvotes · 9 comments
yep
r/vibecoding
•
2mo ago
yep
939 upvotes · 43 comments
Lol fr
r/vibecoding
•
3mo ago
Lol fr
101 upvotes · 11 comments
amazing! wow! so good!
r/vibecoding
•
4mo ago
amazing! wow! so good!
737 upvotes · 47 comments
Look at what my friend made me 🥹
r/JazminBean
•
3mo ago
Look at what my friend made me 🥹
46 upvotes · 2 comments
Do y'all do this?
r/vibecoding
•
2mo ago
Do y'all do this?
214 upvotes · 45 comments
Is this same for you??
r/vibecoding
•
5mo ago
Is this same for you??
908 upvotes · 35 comments
Welp…
r/vibecoding
•
8mo ago
Welp…
2.3K upvotes · 33 comments
Just going to keep this here
r/vibecoding
•
7mo ago
Just going to keep this here
103 upvotes · 12 comments
I love how serious Tony was in iron man 1
r/ironman
•
2mo ago
I love how serious Tony was in iron man 1
2.6K upvotes · 39 comments
💔💔
r/vibecoding
•
8mo ago
💔💔
655 upvotes · 20 comments
Finally
r/vibecoding
•
4mo ago
Finally
2.3K upvotes · 65 comments
It's been a long way to get to this level of detail
r/vibecoding
•
7d ago
It's been a long way to get to this level of detail
289 upvotes · 145 comments
Soooo…Tony Stark is definitely linked to Doom, but how much?
r/MCUTheories
•
1mo ago
Soooo…Tony Stark is definitely linked to Doom, but how much?
50 upvotes · 99 comments
this week has been wild
r/vibecoding
•
4mo ago
this week has been wild
69 upvotes · 7 comments
Just sat through The AI Doc.
r/netflix
•
1mo ago
Just sat through The AI Doc.
4 upvotes · 1 comment
Guys we might be cooked
r/vibecodingcommunity
•
2mo ago
Guys we might be cooked
64 upvotes · 106 comments
Finally!
r/vibecoding
•
5mo ago
Finally!
198 upvotes · 114 comments
That's how I code now
r/vibecoding
•
20d ago
That's how I code now
91 upvotes · 34 comments
What I also liked about this scene is how Tony Stark aurafarms by using some magnetic force to pull his helmet up towards him when he literally could just bend down and pick it up lol
r/ironman
•
26d ago
What I also liked about this scene is how Tony Stark aurafarms by using some magnetic force to pull his helmet up towards him when he literally could just bend down and pick it up lol
4.1K upvotes · 99 comments
Please, I beg you guys
r/vibecoding
•
3mo ago
Please, I beg you guys
189 upvotes · 143 comments
My bsf made an entire website for me🥹
r/PataHaiAajKyaHua
•
3mo ago
My bsf made an entire website for me🥹
72 comments
Tell me how I did!
r/GeometryDashGameplay
•
3mo ago
Tell me how I did!
4 upvotes · 5 comments
Oh, look what I found
r/UmamusumeFFS
•
23d ago
Oh, look what I found
6 upvotes · 15 comments
VIEW POST IN
Français
Português (Brasil)
简体中文
繁體中文
日本語
हिन्दी
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
