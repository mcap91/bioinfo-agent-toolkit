source: https://www.reddit.com/r/LocalLLM/comments/1wxn8r7/daily_driving_qwen_38_flash_instead_of_claude/
captured: 2026-10-27
playwright: 1.64.1
chromium: 156.0.8078.4

Skip to main content
Daily driving Qwen 3.8 Flash instead of Claude. : r/LocalLLM
Sign Up
Log In
Expand user menu
Go to LocalLLM
r/LocalLLM
•
22d ago
u/deepu105
Daily driving Qwen 3.8 Flash instead of Claude.
Discussion

Even 6 months ago, I wouldn't have thought I would be replacing Claude with a local LLM. But here we are. All these PRs are done by Qwen 3.8 (mostly flash, some 27b) running locally on my laptop (strix halo 138gb). And its perfectly acceptable speed (1200+ prefil, 40t/s decode) and Opus 4.8 level quality 🤯🤯🤯

I also have some interesting stories were Qwen 3.8 flash won over Opus 5.5 in a coding task 😅 stay tuned.

https://github.com/llamastash/llamastash/pulls?q=is%3Apr+state%3Aclosed+label%3AQwen

Also here is the prompt if anyone wanna recreate my setup: https://gist.github.com/deepu105/d0b321f3256edf67ebd85e747c0010b9

Share
subaru_usa
•
Ad
Built for all kinds of adventure. The 2026 Subaru Outback Wilderness. Love of adventure, elevated.
Learn More
subaru.com
Collapse video player
Sort by:
Comments Section
txoixoegosi
•
22d ago

What kind of tasks and problems do you solve and on par with Opus 4.8?

Reply
Share
deepu105
•
22d ago

See the PRs, real engineering tasks on a complex Rust repo. Most tasks are medium or high complexity. One of the PRs there was better than the same prompt done by Opus 5.5 at medium effort.

letsbefrds
•
22d ago
 Top 1% Commenter

Opus 5.5 is crazy good, if Qwen 4 is like 90% of it I would be super happy

7 more replies
makkalot
•
22d ago

I’ve been using 3.8 flash on open code go and quality is really bad. Goes into loops not communicating back when stuck etc. wondering if it’s a config thing on inference since people here report good results with it.

deepu105
•
22d ago

I have not experienced such issue so far so could be a harness or setup issue

3 more replies
jagauthier
•
22d ago

Context window size?

deepu105
•
22d ago

full 256k

u/XeroGlobal
•
Ad
Late payments are a growing problem for businesses and they have a detrimental impact on cashflow – here’s what you can do about it with Xero.
Durian881
•
22d ago

Do you get good cache hit with gufo and halogen?

deepu105
•
22d ago

yup works excellent

1 more reply
Individual-Round2767
•
22d ago

How do you know it's opus 4.8 level quality? And can this run on my laptop rtx5080 16gb vram, 32gb ddr5 ram and 2tb ssd

deepu105
•
21d ago

A lot of public benchmarks put it close to 4.8 and alos I ahve used 4.8 extensively and this feels the same.

2 more replies
Fluid_Ad8452
•
22d ago

Opus 4.8 like models running locally on somewhat not extraordinarily expensive consumer hardware. Bonkers. And to think Qwen 4 is coming soon. :)

5 more replies
victoriggy
•
22d ago
•
Edited 22d ago

Same here, purchased a MacBook Pro m5 max 128gb for 4.8k before price increases to 7k for the same config. The flash model with the smaller active 6b parameter count is really optimized for Mac unified memory hardware. Runs like a dream, have done side by side comparisons of how flash next and opus implement the story I am working on. Quality is up to par for the most part though sometimes opus does produce the more optimized implementation, where the flash next implementation had to make 10 calls while opus only a single since it batched everything up front. Real dev work here. What a time to be alive. Keep the $20 sub for frontier intelligence for complex planning and everything else local.  

Edit: clarification by calls made I meant that the implementation delivered was more optimized by opus. 

3 more replies
Last_Bad_2687
•
22d ago

Canceled my Claude Max sub, replaced with Strix Halo box running Halogen Flash.

Slightly slower but overall not noticible 

3 more replies
u/Shane_Company
•
Ad
Hey Bay Area! We buy your diamond directly at the source, hand-picking the most beautiful ones. Shop your way & visit us in the South Bay in Cupertino & San Mateo, or in the East Bay in Walnut Creek.
Shop Now
shaneco.com
Collapse video player
feelspeaceman
•
22d ago

Can confirm, I'm getting 50t/s decode 1200-1700t/s prefill with gufo, the intelligence is definitely Opus 4.8 easily, it solves a lot of complex non-academic problems, giving it a task to maintain existing projects and it's performing with high chance of success, only 1 failure per 108 tasks, this is beyond exceptional to me.

In latest halogen people are pushing to 2000t/s prefill: https://www.reddit.com/r/StrixHalo/comments/1wxiwad/halogen_0162_on_windowswsl2_qwen38flashnext_at/

illhaveubent
•
22d ago

50t/s decode at what context size?

3 more replies
Distinct-Pie2389
•
22d ago

yeah pretty much same, really close. I’m looking for better results till it’s 100% but yeah I’ll be canceling likely in the next year

VarietyOk443
•
22d ago

What is this dashboard

3 more replies
9 more replies
WyattTheSkid
•
22d ago

Ive been saying the same thing. I compared it to somewhere in between Opus 4.6 and Opus 4.8 while beating 4.8 on a few benchmarks too. I have been using Qwen 3.8 Flash Next non stop for so much shit it’s unreal. I don’t even get mad when my codex and claude usage limits are exhausted anymore, I have had no problem getting genuinely complex work done with this model with reasonable speeds and excellent quality. It’s been running autonomously for like 10 days straight right now and it’s gotten so much done!

2C-Banana
•
22d ago

with 27b been getting about 120t/s avg with my 40gb cmp 170hx and after paring it with deepseek harness i barely use claude anymore

niagalacigolliwon
•
22d ago

What laptop is that?

deepu105
•
22d ago

Asus ROG Flow z13

1 more reply
Creative-Pay9521
•
21d ago

For someone new to the world of running local models, where could I learn more about this? I've seen terms like quants, gguf, etc.

Would Claude/ChatGPT be the best resource or would you suggest something else altogether?

deepu105
•
21d ago

Ya you could start with what you already use and ask it to setup local stack for you. thats how I started

1 more reply
1 more reply
vaxufo
•
22d ago

You make me think I actually did not touch my Claude code subscription for 5 months, probably time to cancel it. .

3.6 27b mostly closed the gap, but 3.8b 27b did it for real.

People also ask about section
People also ask about
Local LLM community recommendations
Best local LLM for daily use
Qwen 3.8 performance comparison
Flash model advantages
LLM setup tips for beginners
More posts you may like
Related posts
OK, fine, Qwen 3.8 Flash Next is nice
r/LocalLLaMA
•
6d ago
OK, fine, Qwen 3.8 Flash Next is nice
443 upvotes · 195 comments
subaru_usa
•
Ad
With a striking new exterior plus available 19-inch wheels and Nappa leather-trimmed upholstery, every angle of the 2026 Outback is a sight worth seeing.
subaru.com
Learn More
Impressed about qwen 3.8 Flash
r/LocalLLM
•
28d ago
Impressed about qwen 3.8 Flash
33 upvotes · 19 comments
Qwen 3.8 Flash Next day 0 support from unsloth
r/LocalLLaMA
•
2mo ago
Qwen 3.8 Flash Next day 0 support from unsloth
744 upvotes · 185 comments
Qwen 3.8 Flash Next Q3 S - Benchmark creation
r/LocalLLaMA
•
14d ago
Qwen 3.8 Flash Next Q3 S - Benchmark creation
58 upvotes · 33 comments
Why doesn't anyone use Qwen 3.8 Flash even though it performs great within a $30 budget?
r/opencode
•
2mo ago
Why doesn't anyone use Qwen 3.8 Flash even though it performs great within a $30 budget?
32 upvotes · 21 comments
Did someone use/try the Qwen flash 3.8 next "coder" model on some work?
r/LocalLLaMA
•
12d ago
Did someone use/try the Qwen flash 3.8 next "coder" model on some work?
30 upvotes · 20 comments
I don't get the qwen 3.8 flash next hype
r/LocalLLaMA
•
10d ago
I don't get the qwen 3.8 flash next hype
123 upvotes · 315 comments
Qwen 3.8 Flash Next: drastically faster and much more precise in reaching the result.
r/LocalLLaMA
•
7d ago
Qwen 3.8 Flash Next: drastically faster and much more precise in reaching the result.
87 upvotes · 29 comments
an unscientific qwen 3.8 flash next and glm 5.3 flash comparison
r/LocalLLaMA
•
2mo ago
an unscientific qwen 3.8 flash next and glm 5.3 flash comparison
156 upvotes · 49 comments
Qwen 3.8 Flash Next
r/LocalLLM
•
2mo ago
Qwen 3.8 Flash Next
417 upvotes · 202 comments
running qwen3.8 flash next models entirely on 24gb gpu
r/unsloth
•
2mo ago
running qwen3.8 flash next models entirely on 24gb gpu
71 upvotes · 17 comments
Qwen 3.8 Flash Next, DeepSeekV4 Flash and Time
r/LocalLLaMA
•
12d ago
Qwen 3.8 Flash Next, DeepSeekV4 Flash and Time
73 upvotes · 46 comments
Qwen3.8-Flash-Next. This architecture could be surprisingly local-friendly once the weights drop. 👀
r/LocalLLaMA
•
2mo ago
Qwen3.8-Flash-Next. This architecture could be surprisingly local-friendly once the weights drop. 👀
951 upvotes · 296 comments
I ran Qwen 3.8 Flash-Next on my AMD 7900 XTX at 500k context. All local and what a shift it has been.
r/LocalLLaMA
•
15d ago
I ran Qwen 3.8 Flash-Next on my AMD 7900 XTX at 500k context. All local and what a shift it has been.
59 upvotes · 77 comments
Qwen3.8 Flash Next vs Qwen3.8 27B - The hype vs the truth.
r/LocalLLM
•
14d ago
Qwen3.8 Flash Next vs Qwen3.8 27B - The hype vs the truth.
240 upvotes · 240 comments
Qwen 3.8 Flash Next-GSQ-RCO-IQ2_XS at ~21 tok/s on just an RTX 3060 12GB + 16GB DDR4 RAM(No gate pruning, 100% bit-exact)
r/LocalLLaMA
•
17d ago
Qwen 3.8 Flash Next-GSQ-RCO-IQ2_XS at ~21 tok/s on just an RTX 3060 12GB + 16GB DDR4 RAM(No gate pruning, 100% bit-exact)
139 upvotes · 39 comments
I ran claude vs Qwen 3.8 Flash Next
r/LocalLLM
•
1mo ago
I ran claude vs Qwen 3.8 Flash Next
12 upvotes · 23 comments
Story time: Qwen3.8-Flash-Next on my Strix Halo laptop vs Claude Opus 5.5 on the same feature
r/Qwen_AI
•
21d ago
Story time: Qwen3.8-Flash-Next on my Strix Halo laptop vs Claude Opus 5.5 on the same feature
22 upvotes · 32 comments
I am impressed and I owe you one, Qwen 3.8 flash next (vision)!
r/LocalLLaMA
•
1mo ago
I am impressed and I owe you one, Qwen 3.8 flash next (vision)!
61 upvotes · 26 comments
Qwen/Qwen-Drive-1.0-4B · Hugging Face
r/SelfDrivingCars
•
2mo ago
Qwen/Qwen-Drive-1.0-4B · Hugging Face
15 upvotes · 2 comments
Qwen 3.8 Flash Next - every which way and how
r/Qwen_AI
•
24d ago
Qwen 3.8 Flash Next - every which way and how
58 upvotes · 30 comments
Story time: Qwen3.8-Flash-Next on my Strix Halo laptop vs Claude Opus 5.5 on the same feature
r/LocalLLaMA
•
21d ago
Story time: Qwen3.8-Flash-Next on my Strix Halo laptop vs Claude Opus 5.5 on the same feature
59 upvotes · 86 comments
Daily Driving Qwen 3.8 Flash-Next MoE (NVFP4) on RTX 5090 + 128GB RAM — Telemetry & Impressions
r/LocalLLM
•
18d ago
Daily Driving Qwen 3.8 Flash-Next MoE (NVFP4) on RTX 5090 + 128GB RAM — Telemetry & Impressions
49 upvotes · 40 comments
I would like to run Qwen 3.8 Flash Next.
r/LocalLLM
•
23d ago
I would like to run Qwen 3.8 Flash Next.
3 upvotes · 33 comments
Benefits of using bigger models than Qwen 3.8 flash next?
r/LocalLLaMA
•
16d ago
Benefits of using bigger models than Qwen 3.8 flash next?
33 upvotes · 89 comments
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
