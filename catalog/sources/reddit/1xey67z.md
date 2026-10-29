source: https://www.reddit.com/r/ollama/comments/1xey67z/comment/19rmojt7579uq/
captured: 2026-10-29
playwright: 1.64.1
chromium: 156.0.8078.4

Skip to main content
I Thought SKILLs Were a Waste of Tokens Until I Wrote My Own : r/ollama
Sign Up
Log In
Expand user menu
Go to ollama
r/ollama
•
4d ago
u/ievkz
 Top 1% Poster
I Thought SKILLs Were a Waste of Tokens Until I Wrote My Own

I'll be honest, I didn't understand why LLM agents need SKILLs. MCP was clear to me: it's a useful thing that lets you give an LLM access to a database or to Figma. The only downside is that, to avoid spending too many tokens, it's better not to connect 30 MCP servers at once. And in general, it's better to turn off the unnecessary ones and connect only those that are really needed for the task. In this light, SKILLs seemed like useless overhead to me, eating tokens like crazy. On TikTok, I often saw tales along the lines of: connect this SKILL, or a whole bunch of them, and happiness is yours. My first thought was, if I connect them all, my subscription limits will run out not by lunchtime, but already in the morning.

So why are SKILLs useful and needed after all? Well, first, compared to MCP, SKILLs do not inflate the context: each connected SKILL adds not tens of thousands of tokens, but one or two hundred. Since only the name and description of a SKILL go into the context at first, you can add 30 of your own SKILLs without much pain. When it becomes necessary to use a SKILL, the LLM agent will load its description on its own, if it understands from the task context that this is needed, or the user can simply tell it to use this SKILL for the job.

Secondly, LLM models are trained on the most popular and well-known things. For example, everybody knows that an LLM can work with Git without any problems or write a program in Python. But if you developed a program yourself, or your work requires some little-known tool or technology, then a SKILL is simply irreplaceable. It is enough to create a SKILL.md file and describe how to work with this program or technology. This makes life easier for the LLM: while doing your tasks, it will not have to search the internet for documentation and wander around websites to understand how to use it. And especially if there is nothing on the internet, because your program is closed to public access.

Thirdly, an LLM model usually does not know how your development process is organized. For example, an agent knows how to use Git, run tests, build a project, and create releases. You do not need to teach it these things. But it does not know how releases are usually made in your company. A Skill can describe the sequence of actions: check the changes, run tests, update CHANGELOG.md, increase the version, build a package, create a Git tag, and publish a release. So, a Skill helps the agent learn not a technology, but a specific business process.

Fourthly, a SKILL is not just an instruction, but a whole set of tools. Besides SKILL.md, you can put ready-made scripts, documentation, templates, and other files into it. And the most interesting thing is, these files are not loaded into the context automatically. The agent reads them only when there is a need, and can simply run the ready-made scripts without spending tokens on generating code. So, a SKILL lets you combine instructions, documentation, and executable code in one package without inflating the LLM context. For example, the structure can look like this:

my-skill/
├── SKILL.md
├── scripts/
│   ├── generate.py
│   └── validate.py
├── references/
│   └── api.md
└── assets/
    └── template.html

The funniest thing is, I started to appreciate SKILLs exactly when I wrote my own program, blueprint4llm. The idea for creating it came after I asked an LLM agent to generate a plan.md file describing a task. Usually it produces a huge wall of text, which you have to read slowly and with sadness. I wanted to make the text shorter and add more flowcharts, tables, diagrams, and user interface prototypes. As we know, in .md (Markdown) files the only visualization tools available are tables and Mermaid diagrams. There are no charts, plots, histograms, full UML diagrams, or UI prototypes. In the end, with blueprint4llm, I added support for formats such as PlantUML, draw.io, Pencil, Balsamiq, Graphviz, Figma, OpenAPI, Excalidraw, Vega-Lite, ECharts, and D2 to .md files.

With the blueprint4llm SKILL connected, you will get plan.md not as a kilometer-long text, but as flowcharts, prototypes, charts, and so on. By the way, blueprint4llm does not have to be used only for creating plan.md. For example, I used this SKILL to add an illustration to every paragraph of the article and make it more fun to read. This SKILL is also useful when you ask an agent to put together a full dossier on some company, technology, or person and format the resulting result.md file with blueprint4llm. You can then convert it to HTML or PDF, or ask the agent to show it right away in a browser with charts.

This is how you can install the blueprint4llm SKILL.

# Codex
npx skills add evgenyigumnov/blueprint4llm --skill blueprint4llm --agent codex

# Claude Code
npx skills add evgenyigumnov/blueprint4llm --skill blueprint4llm --agent claude-code

# Pi
npx skills add evgenyigumnov/blueprint4llm --skill blueprint4llm --agent pi

If you are interested in looking at the source code of blueprint4llm, the tool that generates all this beauty, or sending a pull request, welcome: https://github.com/evgenyigumnov/blueprint4llm

Read more
Share
Sort by:
Comments Section
codeprimate
•
4d ago

Now, organize them into domains, and skills for given domains reference the specific skills.

make post task skill revision a part of your core agents, and now you have a mostly self refining agent that focuses on task specific expertise.

Reply
Share
ievkz
•
4d ago
•
Edited 3d ago
 Top 1% Poster

Good idea! Especially the post-task skill revision part. The agent could gradually build its own expertise based on actual experience. I'd probably add a review step before applying changes, though. Otherwise, it might start reinforcing its own mistakes :)

Reply
Share
u/anthropic-ai
•
Ad
The kind of partnership that makes you feel like you’ve leveled up. Try Claude Code and start building your next project.
Download
claude.com
iAlexandreS
•
3d ago

The 100-200 token line only holds while the skill stays closed. Once the model opens SKILL.md and a reference, that body is in the context anyway, so thirty descriptions that all say "use me" cost more than thirty short ones that almost never match. The saving that actually shows up is the script the agent runs instead of pasting it into the prompt. A line in the description that says when not to load the skill is the part most indexes skip.

Sakura010826
•
2d ago

Yeah ..i get it now,making your own skills for specific workflows is actually pretty useful

FragrantArt8270
•
5h ago

This is an ad.

More posts you may like
Related posts
I Thought SKILLs Were a Waste of Tokens Until I Wrote My Own
r/ChatGPTCoding
•
4d ago
I Thought SKILLs Were a Waste of Tokens Until I Wrote My Own
35 comments
1PasswordOfficial
•
Ad
“The orgs that successfully navigate this transition will treat it as an architectural reset.” Read 451 Research on how AI is redefining identity.
1password.com
Learn More
The best skill in the game.
r/gotlegends
•
7mo ago
The best skill in the game.
141 upvotes · 55 comments
Finally, a proper UI for skills
r/ollama
•
2mo ago
Finally, a proper UI for skills
29 upvotes · 8 comments
The new subscription model is bad.. really bad
r/ollama
•
2mo ago
The new subscription model is bad.. really bad
76 upvotes · 69 comments
I built a fully local AI voice assistant that responds in ~230ms — no cloud, no subscriptions
r/hermesagent
•
4d ago
I built a fully local AI voice assistant that responds in ~230ms — no cloud, no subscriptions
12 upvotes
After 10+ years of Dota I started playing LoL, and my friend recommended me OP.GG for guides. I have an uncomfortable question…
r/leagueoflegends
•
5mo ago
After 10+ years of Dota I started playing LoL, and my friend recommended me OP.GG for guides. I have an uncomfortable question…
1K upvotes · 191 comments
Claude Code blocked a legit task, so I tried the open source side. Not going back for now.
r/ClaudeCode
•
3d ago
Claude Code blocked a legit task, so I tried the open source side. Not going back for now.
165 upvotes · 65 comments
Lure-TTS and Lure-Turbo: 600M voice models to run 4x faster than real time, with inline (tags), direction, and voice cloning. Trained for under $200.
r/LocalLLaMA
•
4d ago
Lure-TTS and Lure-Turbo: 600M voice models to run 4x faster than real time, with inline (tags), direction, and voice cloning. Trained for under $200.
75 upvotes · 14 comments
I guess it's safe to say, APA was the problem.
r/leagueoflegends
•
1mo ago
I guess it's safe to say, APA was the problem.
91 comments
Some of you might remember me (I posted this and took down my ranked analysis tool because the dev API couldn't keep up) but I finally got approved for production key, so should be able to handle more traffic. Looking for feedback!
r/leagueoflegends
•
7mo ago
Some of you might remember me (I posted this and took down my ranked analysis tool because the dev API couldn't keep up) but I finally got approved for production key, so should be able to handle more traffic. Looking for feedback!
73 upvotes · 71 comments
What are the most undodgeable abilities in the game?
r/leagueoflegends
•
1mo ago
What are the most undodgeable abilities in the game?
640 upvotes · 418 comments
Finally broke Lemures
r/magicTCG
•
1mo ago
Finally broke Lemures
1.9K upvotes · 98 comments
OpenAI and Anthropic blocked the reverse engineering of smart TVs spying on us
r/LocalLLaMA
•
4d ago
OpenAI and Anthropic blocked the reverse engineering of smart TVs spying on us
3.9K upvotes · 586 comments
"League of Legends is all about mechanics. If you master the mechanics, you climb the ranks." The support I get matched with in ranked...
r/SamiraMains
•
3mo ago
"League of Legends is all about mechanics. If you master the mechanics, you climb the ranks." The support I get matched with in ranked...
139 upvotes · 50 comments
People who didn't like All the Skills, what didn't you like? And if you dropped it, when?
r/litrpg
•
28d ago
People who didn't like All the Skills, what didn't you like? And if you dropped it, when?
43 upvotes · 76 comments
It feels like a lot of skill in this game comes from having patience to wait for right situation
r/leagueoflegends
•
7mo ago
It feels like a lot of skill in this game comes from having patience to wait for right situation
337 upvotes · 72 comments
I couldn't tell what my own swing was doing, so I spent a year building a dataset to find out
r/squash
•
2mo ago
I couldn't tell what my own swing was doing, so I spent a year building a dataset to find out
24 upvotes · 26 comments
Empower in a nutshell
r/MagicArena
•
12d ago
Empower in a nutshell
1.1K upvotes · 42 comments
Is All The Skills a rip off?
r/litrpg
•
1y ago
Is All The Skills a rip off?
14 comments
I built an MCP server that turns your AI conversations into a versioned knowledge base (open source)
r/mcp
•
3d ago
I built an MCP server that turns your AI conversations into a versioned knowledge base (open source)
4 upvotes · 12 comments
Which model has been the best prompt engineer for you?
r/PromptEngineering
•
1y ago
Which model has been the best prompt engineer for you?
41 upvotes · 42 comments
Does anyone use ollama?
r/vibecoding
•
7mo ago
Does anyone use ollama?
7 upvotes · 19 comments
What's a League skill that sounds simple, but took you ages to actually learn?
r/leagueoflegends
•
5mo ago
What's a League skill that sounds simple, but took you ages to actually learn?
409 upvotes · 292 comments
Throwback to Idra at MLG
r/starcraft
•
2mo ago
Throwback to Idra at MLG
143 upvotes · 36 comments
I built my own agent framework and it's awesome
r/AI_Agents
•
4d ago
I built my own agent framework and it's awesome
18 upvotes · 49 comments
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
