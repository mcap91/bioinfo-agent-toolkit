# Catalog inbox

https://github.com/karpathy/llm-council
```text
source: https://www.reddit.com/r/LocalLLaMA/comments/1x9gfnb/google_open_sources_harness2_for_self_improving/
Skip to main content
Google Open Sources Harness2 for Self Improving AI Agents : r/LocalLLaMA
Sign Up
Log In
Expand user menu
Go to LocalLLaMA
r/LocalLLaMA
•
8d ago
u/chemist_slime
Google Open Sources Harness2 for Self Improving AI Agents
Resources

Google just released Harness2 as open source. It turns any AI harness into a system that improves itself over time.

A harness is everything around the model. System prompt, tools, memory, skills, and subagents. Normally a person designs it once and the agent uses that fixed setup for every new task.

With Harness2 the agent itself refines the harness for each task. It proposes changes, runs a few candidate versions, and picks a better one by comparing how they perform. No correct answers or graders are needed. The model weights stay the same.

What it learns on one task carries over to the next. After finishing a task it saves the improved harness and useful lessons so future edits start smarter instead of from scratch.

Google tested it with Gemini 3.5 Flash and GLM-5 on legal, office, and professional work benchmarks. Even one round of edits beat the original harnesses. More rounds pushed scores higher.

GitHub https://github.com/google-research/harness2

Read more
Share
Colgate_US
•
Ad
Daily routine, big results. Colgate Optic White Pro Series—crowned “Best Toothpaste” by Allure.
Shop Now
shop.mikmak.ai
Sort by:
Comments Section
WithoutReason1729
•
8d ago
•
Edited 5d ago

Your post is getting popular and we just featured it on our Discord! Come check it out!

You've also been given a special flair for your contribution. We appreciate your post!

Stylome classified this post's text as human-written. View analysis

I am a bot and this action was performed automatically.

abhi91
•
8d ago

This is great in theory. Poetiq proved it makes benchmarks essentially useless as the harness can "overfit" to the task. Repetitive tasks like customer service are now exceptional for enterprise

Ylsid
•
7d ago
 Top 1% Commenter

But not for customers!

5 more replies
9 more replies
CoolConfusion434
•
8d ago

To paraphrase Mr Krabs: I got a bad feeling in the pit of me context.

All that "self-refinement" has to go somewhere, and that will be right into context. I'm sure it won't be an issue to the 1M context of cloud guys but us locals might be squeezed a little.

Other than that, glad to see another open-source harness, especially from giants like Google.

NineThreeTilNow
•
8d ago
 Top 1% Commenter

All that "self-refinement" has to go somewhere, and that will be right into context.

It runs parallel agents for this purpose. So really the self refinement comes from examining the tasks, seeing where the harness fell short, and then improving on the harness.

Did it need a new tool call? A better explanation of the tool call? Etc.

That will mildly bloat context but harnesses do this already. It's trying to find how it can improve the harness.

Will it increase total context? Probably, but not substantially over the existing harness.

FaceDeer
•
8d ago

It'd be changing the context, but not necessarily growing the context. Indeed, I expect part of its mandate would be to trim redundant or unnecessary stuff from it.

BannedGoNext
•
8d ago
 Top 1% Poster

Wouldn't that be like what the Hermes agent does?

1 more reply
typical-predditor
•
8d ago

I still don't trust LLMs to understand what is redundant or unnecessary. Or even what is, ahem, load bearing and necessary.

4 more replies
1 more reply
tossit97531
•
8d ago

I don't understand how this is any different than any other harness when you give an agent access to source, and I don't know why you wouldn't do that. I bolted on a whole persistent-session web UI on top of a harness core and ditched the stock CLI interface. I don't know how far I've strayed from upstream because I don't care, it's far more useful than upstream will ever be now (especially since the project kind of died).

4 more replies
catinterpreter
•
8d ago

It doesn't take much to stash the odd sentence on an SSD that encapsulates some key, formative insight. Very few words can have an immense impact.

6 more replies
u/adobe
•
Ad
Unleash your potential with Premiere, Illustrator, Photoshop & 20+ apps in Creative Cloud Pro
Learn More
adobe.com
acoolglassofwater
•
8d ago

Could someone with high LLM expertise (not just trust-me-bro) explain the significance of this? I get the general idea, but the comment section is always highly opinionated on self-improving agents. Is this release just a nothing-burger or does it represent something interesting and significant?

itsmebenji69
•
8d ago
•
Edited 8d ago

I’d say it’s mid interesting

The harness can limit the agent in tasks. So perpetually modifying the harness to make it better suited to a task is useful, it removes that ceiling (if harness was limiting the task, it won’t anymore after a few rounds of improvement).

The obvious problem is that better suited to task A may degrade performance in task B. Basically over fitting.

Simple example: task A is to compute x+y and task B is to compute x times y.

Harness version one just gives you x and y, and the llm has to do the calculation. After a few rounds of improvement on task A, the harness only gives the model x+y, and the llm just reads that result. But now it doesn’t know x and y. So it will be great at adding them, perfect even, it will be right every time. Because it will know the accurate result directly. For task A alone, this is a great harness, it ensures that the model will never be wrong about the result of x+y or hallucinate or whatever.

But now on task b, if you want to know x*y, say that’s 2 times 3, the harness will only show the model 5 (2+3, x+y), so it will miserably fail at giving you the multiplication result. It simply won’t be able to know what x and y were, so it won’t know what to do with the result of the A optimized harness. It will just see 5, and from that it can’t infer what x and y are, or infer what x times y is.

And vice versa if you start optimizing on task b

9 more replies
FoxSideOfTheMoon
•
8d ago

I can find no practical use for this FWIW

1 more reply
9 more replies
Paradigmind
•
8d ago

So if we use this on Hermes we get Inception?

1 more reply
HotAverage1749
•
8d ago

Used Qwen to make an extension for pi

1 more reply
Holiday_Point_603
•
8d ago
 Top 1% Commenter

Interesting that google uses models that are like half a year old to show off their new software lol

Spara-Extreme
•
8d ago

Google is a massive company so the team that did this isn’t the team that’s working on Gemini 4

5 more replies
-p-e-w-
•
8d ago
 Top 1% Commenter

Research takes time to prepare for publication. These experiments were likely conducted many months ago.

u/novasourcerenal
•
Ad
TIL: Novasource® Renal comes in Strawberry, Vanilla AND Café Mocha flavors. Try now at Amazon!
Learn More
amazon.com
_-mg-_
•
8d ago

anyone actually tried using this?

suhive
•
8d ago

Harness Self-benchmaxxxing lol

SnooPuppers7882
•
5d ago

Been playing with this and it's promising...

Have a 6 multitask corpus to calibrate Qwen 3.8 flash next as a coding worker...you need to know what you can reliably expect it to be able to do, everytime, so a coordinator model with a capabilities lookup index knows exactly how to split up a task assignment between a local model and a cheap, more capable cloud model.

Baseline (10 repeat runs), QFN would fail all tasks 100% of the time except task 5 (20% pass rate), with individual steps within a task (wide array of coding taxonomy chained in different orders and degrees of difficulty) solved around 50-60%.

After 3 loops under the methodology in Google's paper (Harness² is a LOOP orchestration, NOT an actual harness), Task 1 got 10%, task 3 10%, task 4 20%, task 5 100%, an average total steps increased to the 65 to 72% solve range.

Currently in runs of a modified methodology:

For one arm, QFN goes through claude code as the tester, sol 6.1 max reviews as a coach, opus 5.5 high reviews the coach recommendations to check bias gaps before auto-implementation of changes to the harness configuration. Arm 2 does the same except Opus is the coach and sol is the reviewer...tests are clones of the original t1 through t6 tests but with altered variables, files, and sequencing to maintain difficulty but not bias improvements to one benchmark.

Going through 10 runs each with both arms in parallel, then amalgamating the best changes that yielded the best scores, then the final trained setup run 10 times on the original test again.

Should take 2 days roughly for the results, I'll report back with detailed findings.

2 more replies
Limp_Classroom_2645
•
8d ago

Self refinements mean loss of consistency and control

TemporaryInk
•
8d ago

That’s great and all, but is anyone going to point out the prolific use of Comic Sans in the graphic? 😂

2 more replies
Dany0
•
8d ago
 Top 1% Commenter

Soooo autoresearch again

...

David23G1
•
8d ago

What the different from other harness e.g herems,openclaw,pi

3 more replies
People also ask about section
People also ask about
Best resources for Google Harness2 on GitHub
Features of Google Harness2 for AI systems
Best practices for hosting LLaMA locally
How to optimize LLaMA for specific tasks
Comparing LLaMA with other language models
More posts you may like
Related posts
Agents / Harnesses
r/LocalLLM
•
1mo ago
Agents / Harnesses
4 upvotes · 8 comments
Roblox
•
Ad
Forget mindless scrolling. Start solving instead. Crack cases, outsmart friends, and flex your brain in Roblox's best puzzle games — free to play.
roblox.com
Play Now
This is why we need local models and opensource harnesses
r/LocalLLaMA
•
4mo ago
This is why we need local models and opensource harnesses
3.5K upvotes · 446 comments
We built an open-source, model-neutral agent harness and compared it with claude managed agents - for the same model, got same accuracy, upto 75% lower cost
r/LocalLLaMA
•
2mo ago
We built an open-source, model-neutral agent harness and compared it with claude managed agents - for the same model, got same accuracy, upto 75% lower cost
49 upvotes · 57 comments
What are the best Agent harnesses right now?
r/AgentsOfAI
•
1mo ago
What are the best Agent harnesses right now?
71 upvotes · 76 comments
Google harness2
r/hermesagent
•
7d ago
Google harness2
19 upvotes · 10 comments
Google Open Sources Harness2 for Self Improving AI Agents
r/aicuriosity
•
9d ago
Google Open Sources Harness2 for Self Improving AI Agents
168 upvotes · 13 comments
Which agent harness do you use and why?
r/LocalLLaMA
•
2mo ago
Which agent harness do you use and why?
265 upvotes · 267 comments
Harness Engineering: Turning AI Agents Into Reliable Engineers
r/ArtificialInteligence
•
7mo ago
Harness Engineering: Turning AI Agents Into Reliable Engineers
40 upvotes · 17 comments
DOOMERS DERAILED: It's Definitive. A New Google DeepMind and Cambridge Paper Shows That An AI Agent Can Discover New Math
r/accelerate
•
4d ago
DOOMERS DERAILED: It's Definitive. A New Google DeepMind and Cambridge Paper Shows That An AI Agent Can Discover New Math
386 upvotes · 45 comments
Did you guys build your own agent harness?
r/AI_Agents
•
17d ago
Did you guys build your own agent harness?
36 upvotes · 59 comments
My experience with agent harness
r/AI_Agents
•
2mo ago
My experience with agent harness
4 upvotes · 8 comments
Everyone’s building harnesses
r/AgentsOfAI
•
1mo ago
Everyone’s building harnesses
1.6K upvotes · 194 comments
I built 6 agent harnesses in the last 6 months, they all need a database
r/AI_Agents
•
4mo ago
I built 6 agent harnesses in the last 6 months, they all need a database
29 upvotes · 58 comments
Agentic harness for small models
r/LocalLLaMA
•
2mo ago
Agentic harness for small models
41 upvotes · 52 comments
How does your agent harness work
r/AI_Agents
•
2mo ago
How does your agent harness work
11 upvotes · 28 comments
I spent 883 commits and 8 months building an LLM agent harness, overengineered it, and abandoned it - lol.
r/AI_Agents
•
2mo ago
I spent 883 commits and 8 months building an LLM agent harness, overengineered it, and abandoned it - lol.
104 upvotes · 94 comments
Google now tracks your SERP clicks even harder & makes it super easy to get scammed by obstructing real URLs
r/privacy
•
7d ago
Google now tracks your SERP clicks even harder & makes it super easy to get scammed by obstructing real URLs
519 upvotes · 65 comments
Introducing Gemini 4 Argon
r/singularity
•
26d ago
Introducing Gemini 4 Argon
896 upvotes · 191 comments
What is a harness ?
r/aicuriosity
•
21d ago
What is a harness ?
3 upvotes · 10 comments
Which agent harness do you use?
r/LocalLLM
•
2mo ago
Which agent harness do you use?
17 upvotes · 46 comments
Open-source self improving QA agent for software teams
r/vibecoding
•
3mo ago
Open-source self improving QA agent for software teams
1 upvote
The agent harness matters more than the model you pick
r/AI_Agents
•
3mo ago
The agent harness matters more than the model you pick
37 upvotes · 44 comments
[Riftbound] Seraphine Champion Unit
r/SeraphineMains
•
5mo ago
[Riftbound] Seraphine Champion Unit
50 upvotes · 6 comments
Lembram do Google+?
r/Nostalgia_Br
•
11d ago
Lembram do Google+?
196 upvotes · 59 comments
Google releases RRSI for Better Self Improving AI Agents
r/aicuriosity
•
1mo ago
Google releases RRSI for Better Self Improving AI Agents
22 upvotes · 4 comments
VIEW POST IN
Français
Português (Brasil)
简体中文
繁體中文
日本語
Русский
Tiếng Việt
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
```
⚠ capture-failed https://www.reddit.com/r/AI_Agents/s/forcedFailure1 — net::ERR_NAME_NOT_RESOLVED (forced, snapshot test)
```text
source: https://www.instagram.com/reel/De5smNojeZm/
Caption:
Your slow Android TV is probably full of apps you never asked for. Here's every step to fix it. 📺

People are using Claude Code to switch off bloat, ad rows and trackers on Android TV and Google TV over ADB, with no root. Everything is disabled, not deleted, so it can be undone. The catch: one user bricked a TV, you lose whatever you switch off, and 1 GB TVs may not speed up much.

Would you let an AI tune your TV, or never risk it? 👇
Comment PROMPT and I'll send you the exact one.

Sources: TechCrunch, It's FOSS, Tom's Hardware, github.com/Gathin23/cleanyourtv, github.com/humblemuzzu/dumbtv, developer.android.com, code.claude.com
Original animation. Not affiliated with Google, Anthropic or Amazon.

#AndroidTV #GoogleTV #ClaudeCode #SmartTV #TechTips #AI #LearnTech

Transcript:
[   0.0] People are letting Claude fix their slow Android TVs, and some say it's smoother than new.
[   5.6] Real speed up or risky hack, here's every step.
[   9.3] Many budget TVs have just one to two gigabytes of RAM, and ship full of pre-installed apps,
[  14.0] add rows and trackers.
[  15.0] Some even fingerprint your screen to sell ads.
[  18.2] You need a TV, a laptop on the same Wi-Fi, and 15 minutes.
[  22.3] It works on Android TV and Google TV, not Samsung, LG or Roku.
[  27.8] Step 1.
[  28.8] On the TV, open Settings, Device Preferences about.
[  32.5] Press OK on Build 7 times.
[  34.8] Your developer.
[  36.3] Step 2.
[  37.3] In Developer Options, turn on USB debugging, plus network debugging if you see it.
[  42.8] Step 3.
[  43.8] In your Wi-Fi settings, note the TV's IP address.
[  47.8] Step 4.
[  48.8] On your laptop, install Android's free platform tools.
[  52.1] That's ADB, Google's tool for sending commands to a device.
[  56.2] Then install Claude code and sign in.
[  58.8] Step 5.
[  59.8] Tell Claude your TV model and IP, and ask it to connect over ADB.
[  64.2] Be specific.
[  65.2] Hack my TV can get refused.
[  67.8] Step 6.
[  68.8] The TV asks, allow debugging.
[  70.7] Press Allow.
[  71.7] Only computers you approve get in.
[  73.8] Step 7.
[  74.8] Have Claude back up the full app list and settings and write a restore script.
[  78.5] That's your Undo button.
[  80.3] Step 8.
[  81.3] Claude sorts every app, tracking, ads, background extras, preloaded apps, and the app
[  86.2] you use.
[  87.2] You pick what stays.
[  88.7] Step 9.
[  89.7] It switches the extras off with PM Disable User.
[  92.9] Disabled, not deleted, so you can undo it anytime.
[  97.2] Step 10.
[  98.2] It presses remote buttons and screenshots the TV to check each change.
[ 103.2] On top of that, lower the animation scales in Developer Options.
[ 107.0] Lower means faster.
[ 108.9] Swap the heavy home screen.
[ 110.4] One user went from 192 megabyte launcher to an 83 megabyte one and disabled 25 bloat apps.
[ 117.7] Gathen built Clean Your TV with Claude code in an afternoon for his parents' TV, a light
[ 122.6] home screen made for 1 gigabyte TVs.
[ 126.2] On Fire TV, Dumb TV disables about 50 Amazon ad and tracking packages and blocks about
[ 132.4] 400 tracking addresses.
[ 134.1] One script undoes it all.
[ 136.2] You can also switch off Ad Tracking and Autoplay.
[ 139.6] To catch, one user bricked their TV.
[ 142.3] Uninstalling the wrong system app can break home or HDMI, so only disable and install the
[ 147.6] new launcher before removing the old one.
[ 150.3] Whatever you switch off is gone, like voice search or updates.
[ 153.6] On a 1 gigabyte TV, gains may be small and turn debugging off when you're done.
[ 159.3] Claude code asked before each command.
[ 161.5] Read it before you press yes.
[ 163.7] So would you let an AI tune your TV or never risk it?
[ 167.4] Comment below.
[ 168.6] What my exact prompt?
[ 170.1] Comment prompt and I'll reply.
[ 171.8] Save this and follow for one tech idea a day.

On-screen text:
SPONSORED | YOU NEED THE TV A LAPTOP ... 15 MINUTES WORKS ON ANDROID TV GOOGLE TV NOT SAMSUNG LG ROKU | 02 STEP 1 UNLOCK DEVELOPER Settings > Device Preferences Device name Android TV OS 12 Build tap Status You are now a developer! PRESS OK x7 you're a developer. | 03 STEP 2 TURN ON DEBUGGING Developer options Stay awake Home Wi-Fi USB debugging Network debugging Window animation scale 1x USB + NETWORK NO WIRELESS TOGGLE? USB MAY BE ENOUGH | 04 STEP 3 FIND THE TV'S IP Wi-Fi Network Signal strength Good IP address 192.168.1.42 Proxy settings 192.168.1.42 EXAMPLE · YOURS WILL DIFFER | 05 STEP 5 CONNECT · TELL CL... CLAUDE CODE > My TV is a [model]. Connect over ADB and back... adb connect 192.168.1.42:5... hack my TV CAN GET REFUSED BE SPECIFIC Step six | 06 STEP 6 APPROVE IT ON THE... Allow USB debugging backup only computers you approve. | 07 STEP 7 BACK UP FIRST restore.sh your undo button. | 10 STEP 10 CHECK EVERY CHANGE KEYEVENT → TV screen.png | ON TOP OF THAT LOW... ANIMATION SCALES ... 1x LOWER = FASTER | A LIGHTER HOME SCRE... 25 BLOAT APPS OFF OR: PROJECTIVY · FLAUNCHER · ATV | WHAT OTHERS BUILT 1 AFT... Good evening 8:42 FOR 1 GB TVS A DOCK · A GRID · NO VIDEO · NO BLUR | LET AI TUN... RI... Want my exact prompt?

Key claims:
- Claude Code can connect to Android TV/Google TV over ADB with no root to disable bloat, ad rows, and trackers.
- Works only on Android TV and Google TV, not Samsung, LG, or Roku.
- Budget TVs often have just 1-2GB RAM and come preloaded with apps, ad rows, and trackers, some of which fingerprint the screen to sell ads.
- Process requires a TV, a laptop on the same Wi-Fi, and about 15 minutes.
- Steps include: enabling developer options (tap Build 7x), turning on USB/network debugging, finding the TV's IP, installing ADB and Claude Code, connecting via ADB, approving the debugging prompt, backing up the full app list/settings with a restore script before changes, disabling apps with pm disable-user (disabled not deleted, so reversible), and verifying changes via remote key presses and screenshots.
- Lowering the animation scale in Developer Options makes the TV feel faster.
- One user went from a 192MB launcher to an 83MB one and disabled 25 bloat apps.
- Gathin built 'Clean Your TV' with Claude Code in an afternoon for his parents' TV, a lightweight home screen designed for 1GB TVs.
- 'Dumb TV' disables about 50 Amazon ad/tracking packages on Fire TV and blocks about 400 tracking addresses; one script undoes it all.
- Users can also disable ad tracking and autoplay.
- Risk: one user bricked their TV; uninstalling the wrong system app can break the home screen or HDMI, so only disable apps and install a new launcher before removing the old one.
- Whatever is switched off is lost (e.g., voice search or updates) unless restored.
- On 1GB TVs, speed gains may be small.
- Users should turn debugging off when finished.
- Claude Code asks for confirmation before each command, and users should read commands before approving.

Mentioned (unverified hints):
- Claude Code: code.claude.com
- ADB (Android Debug Bridge / Android platform tools): developer.android.com
- Clean Your TV: github.com/Gathin23/cleanyourtv
- Dumb TV: github.com/humblemuzzu/dumbtv
```
⚠ capture-failed https://www.instagram.com/reel/forcedFailure2/ — audio: yt-dlp bestaudio exit 1 (forced, snapshot test)
⚠ needs-link https://www.instagram.com/p/DeCarousel/
