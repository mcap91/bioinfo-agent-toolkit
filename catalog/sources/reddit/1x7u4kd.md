source: https://www.reddit.com/r/Qwen_AI/comments/1x7u4kd/self_hosted_qwen_38_27b_for_real_work_my_1_month/
captured: 2026-10-27
playwright: 1.64.1
chromium: 156.0.8078.4

Skip to main content
Self hosted Qwen 3.8 27b for real work: my 1 month experience : r/Qwen_AI
Sign Up
Log In
Expand user menu
Go to Qwen_AI
r/Qwen_AI
•
10d ago
u/Fragrant-Piglet4638
Self hosted Qwen 3.8 27b for real work: my 1 month experience
Discussion

My experience with Qwen 3.8 27b (fp8) on a self-hosted GPU. I run Qwen on a single GPU with 48GB of VRAM (Nvidia L40s). At work, I also have unlimited tokens on any Anthropic model through Amazon Bedrock.

I recently started a new position at my company. I'm a senior java developer, and the project is a fork of Open WebUI. My job is to fix bugs and above all, to analyze the application's usage analytics with Databricks. I worked as a data engineer 5 years ago ... so I was a complete beginner with this technical stack.

To quickly understand the business logic, learn Databricks, and pick up the basics of data science and data engineering, I use Opus 4.8 heavily, with Cline as the harness. I also use Qwen 3.8 with a harness I optimized: Zed, Qwen Code, and a SearXNG MCP server, always at xhigh effort. With Qwen, tasks take from a few minutes to almost an hour. I get an average of 28 tokens/s, using vLLM, batch size 4 and multi-token prediction 3. For the same task, Opus 4.8 and Qwen 3.8 gave me similarly good results. But because Qwen is slower and I often have to deliver quickly, I mostly use Opus 4.8. I skipped Opus 5 because I didn't find its answers better than 4.8's, and its reasoning seemed to overthink. When I got access to Opus 5.5, it was very different. It is as fast as Opus 4.8, and it gives better answers and better analysis of large amounts of data. It is also very smart: on its own, it read my QWEN.md rules file and used the SearXNG MCP server instead of Cline's basic HTTP fetch.

Conclusion after one month With a well-adapted harness, Qwen is really impressive and can compete, to a certain extent, with the best frontier models.

A few examples:

- Tool use: given a PDF, it wrote and executed a Python script to extract and read the text.

- Rule following: it reliably respects the project rules in QWEN.md and AGENTS.md.

- Web research: it is far more effective than Opus 4.8 with its basic HTTP fetch.

- Trust: I needed to estimate the latency of several queries on our database, but I was short on time because of an urgent bug fix. I gave it read-only credentials, the database URL, and my instructions. On its own, it connected to the database (using Docker, I think), ran the queries with EXPLAIN ANALYZE, and gave me a report.

I still use Opus mostly because my company pays for it (sometimes up to $250 per day!). But self-hosted models have made amazing progress, and it is now realistic to work with them.

Read more
Share
Shane_Company
•
Ad
Hey Bay Area! Our engagement rings are ready in days, not weeks. No appointment needed! Shop your way & visit us in the South Bay in Cupertino & San Mateo, or in the East Bay in Walnut Creek.
Shop Now
shaneco.com
Collapse video player
Sort by:
Comments Section
rootdood
•
10d ago

Try Strata with Qwen 3.8 Flash Next IQ3_S. I’m getting about 160tps on a single 48GB GPU, with around 60GB of RAM used.

i_wayyy_over_think
•
10d ago

try the swift version too (already supported by strata), uses less thinking tokens so feels even faster

whitespades
•
10d ago

Isn't it hallucinating?

2 more replies
AnonymerKebab
•
10d ago

It is ok for private use, but not commercial… Check their license

9 more replies
2 more replies
TheWaffleKingg
•
10d ago

Ive been doing that after using 27b q8 for a while. Love the speed but so far its been kind of a disaster. Every other thing it does it messes up

rootdood
•
10d ago

Interesting. I’ve been using it to great effect. I did some coreviews back and forth and maybe it’s a bit more chatty, but it was trying to be honest that no, it wouldn’t have done as well as the 27B Q8. But at 160tps, it just goes and takes way more initiative, and as long as I’m in the loop I can steer it. The only problem I’m having is it takes 10 times as long running tests that writing code.

1 more reply
1 more reply
Fragrant-Piglet4638
•
10d ago

I've always been disappointed with self-hosted MoE models. Even at moderate context lengths (around 50k tokens), I get imprécise answers and hallucinations. The only impressive thing is the generation speed on a 48 GB GPU.

I've also read many user reports saying that Qwen3.8-Flash-Next at aggressive quantization hallucinates more than the dense Qwen3.8 27b. For professional work, accuracy matters more than speed.

Have you compared them on the same tasks?

lex_sander
•
10d ago

I left everything below q4 behind it has done too many mistakes, my nvfp4 is doing it’s job fine.

MCCmp_DEV
•
6d ago

*Swift 1.5 Q3_S is the best for me. What gpu are you Running? Also what prefill?

4 more replies
JamesGooning
•
10d ago

48Vram? Use qwen flash next. It is as good as Opus 4.8 and faster. Unfortunately, 5.5 series, especially Sonnet put Qwen in the dust. Finger crossed for Qwen4. If it just fable with uncensored, I will switch back to my local stack. More cost effective to use sonnet 5.5 right now due to time cost

mattjcoles
•
10d ago

I've got a blackwell 5000 48gb but was worried quantisation would cause issues and i couldnt do 256k context window. whats your setup like?

JamesGooning
•
10d ago

Strata works well even on 24/32 GB vram. You just need more ram and good ssd. It can do full 256k context easily. I use cloud rtx6000 to get 200 token/s 7k prefill. That only because all expert fits. Its 512k context too.

1 more reply
mattjcoles
•
10d ago

I’d give this version of qwen ago - it overthinks much less but makes good decisions: https://huggingface.co/ukisai/Swift-1.5-Qwen3.8-27b

Made a good difference for me in terms of getting a bit more competitive to claudes completion timed

4 more replies
u/anthropic-ai
•
Ad
A new model, smarter Claude Code, and a redesigned voice mode. Everything we shipped last month.
claude.com
Sign Up
Bagelsarenakeddonuts
•
10d ago

Don't fall into the flash next trap. it hallucinates regardless of quant. The numbers are impressive but reality crashes into it hard, and 27B is far more reliable. it ends up delivering results faster and more consistently.

shapic
•
10d ago

Probably because most try it via strata and that has really questionable sampling parameters

Bagelsarenakeddonuts
•
10d ago

Yeah thats what I thought, but i tried it on llama, strata, basalt and API. its has some serious reliability issues if left unattended. I think the people that like it are using it in direct chat prompts, not as an autonomous tool.

1 more reply
Nomski88
•
6d ago

I found flash next to excel past 27b only at 4bit and higher quants, anything less and it performs worse.

PinotGroucho
•
10d ago

I agree to a degree, but in large scale thinking it exceeds the 27B imo . It also self corrects well, redirecting when confronted with incorrectly interpreted findings by faulty tool calling. I have both running and use them both extensively.

Bagelsarenakeddonuts
•
10d ago

I mentioned in other responses, but I think it does well in interactive chat, which is why there is such a split on it. But for totally hands-off operation those little hiccups are critical and dealbreakers.

JoaoPFSimoes
•
10d ago
•
Edited 9d ago

I honestly think people that doubt local models right now don't know how to properly setup their agents.
It does basically anything I want on a daily basis.
My use of Opus 5.5 is mainly to plan and ensure everything is being architected and correctly done.

I am running qwen 3.8 flash at home on a 9070xt and 64gb ddr4 (my motherboard is old - still pcie gen3), getting 50+ TPS at 262k context.
For home stuff that is awesome!
For work, at least 100TPS would be my sweet spot so I don't wait much.

I’m using 4x R9700 at work on a “small server” running qwen 3.8 flash, plus “big guns” running even bigger models.

All in all, I think I have a pretty good idea of each current local AI “tier”, therefore defending my initial sentence. Bigger models can do better architecture etc. Sure, but you can also provide a good pipeline on smaller ones to achieve the same. Plus, leaving it doing heavy stuff during the night is the way to go anyway. Even Opus 5.5 takes a long time on my daily work…

7 more replies
Mission_Wrongdoer786
•
10d ago

I have never used a "frontier" model. I am using Qwen 3.8 27B for about a month now too and I have not yet found any limit in its reasoning capabilities. The only limit is my my 25 token/s.

Where, if at all would you say that Qwen 3.8 27B falls evidently short compared to a "frontier" model?

mattjcoles
•
10d ago

Qwen just needs more detailed instructions with task breakdown to do. just as good a job. As well as web search and a good harness like pi / omp or deepseek harness.

I use Opus 5.5 ($20 plan) with a grill-me-with-docs agent + openspec once i have the shape of the feature defined to do the requirements gathering. Then do the heavy work through it on Qwen 3.8 atm

Fragrant-Piglet4638
•
10d ago

I gave the exact same tasks to Opus 4.8 and Qwen 3.8 27B. They included planning implementations and analyzing volumes of sql or spark query results. I then had Opus 5.5 review the outputs. According to the review reports, both models gave correct answers, or each one failed on some tasks in turn. However, Opus 5.5's analysis is significantly better than Opus 4.8.

irreverend_god
•
6d ago

PullMD is good for converting files and websites into markdown, I have it hosted on a Pi along with a Hermes agent which uses my main PC for inference over a LAN API.

Capable_Site8357
•
10d ago

My setup is claude pro with local qwen 3.8 27b for implementation, very smooth, almost on par with my opus 5.5 and sonnet for implementation

People also ask about section
People also ask about
Experience with self-hosted Qwen 3.8 27b
Is Qwen AI effective for real work?
Qwen 3.8 model release information
Qwen AI model sizes and specifications
Best programming languages for AI projects
More posts you may like
Related posts
Long Review: Qwen 3.8 27B is VERY good at tapping into it's real-world knowledge. It's "overthinking" brings it to Sonnet level performance with the potential for Opus level results.
r/LocalLLaMA
•
2mo ago
Long Review: Qwen 3.8 27B is VERY good at tapping into it's real-world knowledge. It's "overthinking" brings it to Sonnet level performance with the potential for Opus level results.
516 upvotes · 112 comments
Qwen 3.8 27B Released! Please Share Your Experience
r/LocalLLaMA
•
2mo ago
Qwen 3.8 27B Released! Please Share Your Experience
660 upvotes · 692 comments
Roblox
•
Ad
Skip the tutorial. Go straight to boss fights, blazing showdowns, epic combat.
roblox.com
Play Now
Qwen 3.8 27b is still enough for almost anything
r/Qwen_AI
•
5d ago
Qwen 3.8 27b is still enough for almost anything
425 upvotes · 182 comments
Qwen 3.8 27b !
r/Qwen_AI
•
2mo ago
Qwen 3.8 27b !
200 upvotes · 31 comments
"Qwen 3.8 isn't Opus level": I re-ran the test.
r/LocalLLM
•
2mo ago
"Qwen 3.8 isn't Opus level": I re-ran the test.
698 upvotes · 168 comments
Qwen 3.8 27b is a amazing model, for the first time I see a local model found its own away to open a browser and test
r/LocalLLaMA
•
1mo ago
Qwen 3.8 27b is a amazing model, for the first time I see a local model found its own away to open a browser and test
80 upvotes · 47 comments
Qwen 3.8 27B finetune did the lava lamp
r/LocalLLM
•
9d ago
Qwen 3.8 27B finetune did the lava lamp
27 upvotes · 4 comments
Qwen 3.8 27B is the moment I've been waiting for
r/LocalLLM
•
2mo ago
Qwen 3.8 27B is the moment I've been waiting for
198 upvotes · 121 comments
Qwen 3.8 27B coming next week! woo hoo!
r/LocalLLM
•
3mo ago
Qwen 3.8 27B coming next week! woo hoo!
518 upvotes · 125 comments
I benchmarked every Qwen 3.8 27B quant that fits in 16GB VRAM
r/LocalLLM
•
2mo ago
I benchmarked every Qwen 3.8 27B quant that fits in 16GB VRAM
679 upvotes · 218 comments
Tell me about what your experiences with Qwen 3.8 27B have been like?
r/Qwen_AI
•
25d ago
Tell me about what your experiences with Qwen 3.8 27B have been like?
40 upvotes · 66 comments
I ran Qwen 3.8 27B locally for 30 days, here are the results
r/LocalLLM
•
1mo ago
I ran Qwen 3.8 27B locally for 30 days, here are the results
669 upvotes · 220 comments
Qwen 3.8 27B
r/LocalLLM
•
3mo ago
Qwen 3.8 27B
307 upvotes · 108 comments
Final-year CS undergrad, on-campus placements are live — sharing what I built this year (3.66B MoE LLM, O(N) attention, BERT from scratch, C++ load balancer) and my resume, would love honest feedback
r/indianstartups
•
3mo ago
Final-year CS undergrad, on-campus placements are live — sharing what I built this year (3.66B MoE LLM, O(N) attention, BERT from scratch, C++ load balancer) and my resume, would love honest feedback
5 upvotes · 4 comments
Qwen 3.8 27B is a game changer.
r/LocalLLaMA
•
2mo ago
Qwen 3.8 27B is a game changer.
1.1K upvotes · 359 comments
Qwen 3.8 Flash Next: drastically faster and much more precise in reaching the result.
r/LocalLLaMA
•
7d ago
Qwen 3.8 Flash Next: drastically faster and much more precise in reaching the result.
87 upvotes · 29 comments
Qwen3.8-27B Released !
r/Qwen_AI
•
2mo ago
Qwen3.8-27B Released !
130 upvotes · 19 comments
Finally got Qwen 3.8 27b working with MTP ~60tps
r/MacLocalLLM
•
1mo ago
Finally got Qwen 3.8 27b working with MTP ~60tps
36 upvotes · 29 comments
A preliminary Qwen3.8-27B model card is live!
r/LocalLLaMA
•
2mo ago
A preliminary Qwen3.8-27B model card is live!
573 upvotes · 219 comments
Qwen will be the king?
r/LocalLLaMA
•
2mo ago
Qwen will be the king?
540 upvotes · 127 comments
Qwen 3.8 27B xhigh vs medium small comparison (+ others for fun)
r/LocalLLaMA
•
2mo ago
Qwen 3.8 27B xhigh vs medium small comparison (+ others for fun)
124 upvotes · 43 comments
Qwen 3.8 27B coming next week
r/Qwen_AI
•
3mo ago
Qwen 3.8 27B coming next week
369 upvotes · 71 comments
Qwen 3.8 27b is out. Big news for local AI
r/ArtificialInteligence
•
2mo ago
Qwen 3.8 27b is out. Big news for local AI
180 upvotes · 29 comments
Qwen 3.8 27b be like...
r/LocalLLaMA
•
1mo ago
Qwen 3.8 27b be like...
459 upvotes · 139 comments
Local Qwen 3.8 27b saved my project from a serious leak, I'm truly impressed
r/Qwen_AI
•
2mo ago
Local Qwen 3.8 27b saved my project from a serious leak, I'm truly impressed
60 upvotes · 19 comments
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
