source: https://www.reddit.com/r/LocalLLM/comments/1x5ozas/nvidias_nemotron_35_bolt_74b_brings_74b_ai_models/
captured: 2026-10-27
playwright: 1.64.1
chromium: 156.0.8078.4

Skip to main content
NVIDIA's Nemotron 3.5 Bolt 74B Brings 74B AI Models to Local Hardware : r/LocalLLM
Sign Up
Log In
Expand user menu
Go to LocalLLM
r/LocalLLM
•
13d ago
u/Loco_AI
NVIDIA's Nemotron 3.5 Bolt 74B Brings 74B AI Models to Local Hardware
Model
maraissoftware.co.za

NVIDIA introduces Nemotron 3.5 Bolt 74B, a 74 billion parameter model designed for local AI agents, alongside PAIR, an open source tool for distributing AI workloads across multiple computers.

Open

NVIDIA introduces Nemotron 3.5 Bolt 74B, a 74 billion parameter model designed for local AI agents, alongside PAIR, an open source tool for distributing AI workloads across multiple computers.

Share
Shane_Company
•
Ad
Hey Bay Area! We have the widest selection of high-quality engagement rings & diamonds in stock for you to see. Visit us in the South Bay in Cupertino & San Mateo, or in the East Bay in Walnut Creek.
Shop Now
shaneco.com
Collapse video player
Sort by:
Comments Section
MoralityAuction
•
13d ago

2 bit? Brave for agentic work, but we'll see the stats tomorrow.

silenceimpaired
•
13d ago

It is QAT so very promising. I have wondered why all QAT models were 4 bit.

MrHumanist
•
13d ago
 Top 1% Commenter

4 bit is a sweet spot for performance to size. Lower than 4 bit, performance degrades fast.

3 more replies
rrrrex
•
13d ago

For me Nemotron is nothing, but tech demo, it's far from real usage. I doubt the next iteration will be good.

Cupakov
•
13d ago

IIRC they are meant to be fine tune base models really, not the finished end product 

15 more replies
ForsookComparison
•
12d ago

They have had models that entered the "meta" a few times.

Notably:

Nemotron Nano 30B was a workhorse that ran faster and did better at general agent work than the qwens at the time. Not so much a great coder but a greater worker.

Nemotron Ultra 550B was the top western open model for a good while. Anyone dealing with compliance constraints or hard sells upstream got some good use out of this

No reason that Nvidia will commit to releasing uncompetitive models. Every one is worth checking.

4 more replies
mister2d
•
13d ago
 Top 1% Commenter

The competition must be close to releasing models again.

vdek
•
13d ago

The rtx spark is about to release and they need a model for people to play with on them.

3 more replies
HonkaiStarRails
•
13d ago

damn a 74b A6B MoE will def be good alt for qwen 3.8 flash next!

KissMyShinyArse
•
13d ago

They say A9B.

Nemotron-3.5-Lightning-30B-A3B was rather stupid, so I don't know.

1 more reply
Dodgy_Past
•
12d ago

Here's hoping for a 4bit version, I really need something modern that targets 48gb.

u/AltaLabs
•
Ad
Looking for a Cambium Alternative? Meet Alta Labs.
alta.inc
Learn More
muggy8
•
13d ago

this is very very interesting. it's not for everything but i'm definitely going to take a look at it for large repetitive menial tasks that doesn't require as much intelligence.

JLeonsarmiento
•
13d ago

Oh wow. 🤩

Valie-Girl
•
13d ago

previous nemotron models where subpar, this would be ideal for me but nvidia has not produced competitive models in the past, not going to bother hoping its better now

Soggy_Consequence1
•
13d ago

I found that they did really well immediately, but they lost their way on longer chains of thought. That's likely due to their attention.

I quite liked nemotron 120b for interactive work, but you had to be done quickly due to the above mentioned issue, even @ 6bit or 8bit.

RWOverdijk
•
13d ago
 Top 1% Commenter

Nemotron diarizer is great though. Haven’t found anything better

5 more replies
2 more replies
Teht
•
12d ago

Sounds like a Strata candidate.

Keats852
•
12d ago

If you give this the strata treatment it would be able to run on like a 4GB laptop!

norenEnmotalen
•
13d ago

Available tomorrow. Interesting 

AggregationLinker
•
13d ago

When you want news headlines but no benchmarks

1 more reply
1 more reply
silenceimpaired
•
13d ago
•
Edited 13d ago

About to be happy then saw it is not dense :P hopefully it’s Apache 2.0 or MIT… but I doubt it. Another custom license no doubt.

5 more replies
EbbNorth7735
•
13d ago

Just to be clear this is a 74B A9B model it looks like with QAT training... possibly at 2bit.

u/anthropic-ai
•
Ad
Hand Claude the whole social post, landing page, or layout. It does the work. You keep, edit, or steer any piece.
Learn More
claude.com
Collapse video player
aimark42
•
12d ago

It is 24GB. Many RTX Spark machines being sold this week have 24GB of RAM and won't be able to run this.

Buy fancy $2500+ machine, and you can't run the thing it's sold for.

TapAggressive9530
•
9d ago

It’s terrible . Shameful coming from Nvidia …

Big_Log_2108
•
6d ago

Bonjour, suite à votre fil de discussion nous avons fait un test cette nuit sur de vrais workflow

https://www.mdminformatique.fr/blog/tests-outils/nvidia-nemotron-3-5-rtx-5090-test-ia-locale

People also ask about section
People also ask about
Overview of NVIDIA's Nemotron 3.5 Bolt 74B
Comparison of Nemotron models
Best use cases for Nemotron AI
NVIDIA's new AI model recommendations
Nemotron 3.5 Bolt 74B vs other models
More posts you may like
Related posts
NVIDIA releases Nemotron 3.5 Super VL (120B-A12B, open weights, 1M ctx, image + video) and Bolt 74B-A9B that fits in 24GB
r/machinelearningnews
•
11d ago
NVIDIA releases Nemotron 3.5 Super VL (120B-A12B, open weights, 1M ctx, image + video) and Bolt 74B-A9B that fits in 24GB
37 upvotes · 5 comments
LincolnFinancial
•
Ad
TL;DW: You don’t just need a retirement plan. You need an action plan.
lincolnfinancial.com
Learn More
Experience with Nemotron 3.5 lightning?
r/LocalLLaMA
•
2mo ago
Experience with Nemotron 3.5 lightning?
16 upvotes · 27 comments
NVIDIA Rolls Out Nemotron 3.5 Lightning Open Model Built for Speedy AI Agents
r/aicuriosity
•
3mo ago
NVIDIA Rolls Out Nemotron 3.5 Lightning Open Model Built for Speedy AI Agents
54 upvotes · 12 comments
nvidia/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-24GB · Hugging Face
r/LocalLLaMA
•
12d ago
nvidia/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-24GB · Hugging Face
518 upvotes · 251 comments
Nemotron-3.5-Bolt-74-A9B and Nemotron-3.5-Super-VL Tests
r/LocalLLaMA
•
11d ago
Nemotron-3.5-Bolt-74-A9B and Nemotron-3.5-Super-VL Tests
14 upvotes · 18 comments
NVIDIA releases Nemotron 3 Nano, a new 30B hybrid reasoning model!
r/LocalLLaMA
•
1y ago
NVIDIA releases Nemotron 3 Nano, a new 30B hybrid reasoning model!
859 upvotes · 177 comments
Add Nemotron Super 3.5 VL and Nemotron Bolt 74B A9B support by frozenblade1224 · Pull Request #30520 · ggml-org/llama.cpp
r/LocalLLaMA
•
12d ago
Add Nemotron Super 3.5 VL and Nemotron Bolt 74B A9B support by frozenblade1224 · Pull Request #30520 · ggml-org/llama.cpp
38 upvotes · 3 comments
Nemotron-3.5-Lightning at 11.77 GiB, a 16 GB option for a model that didn't have one
r/LocalLLaMA
•
2mo ago
Nemotron-3.5-Lightning at 11.77 GiB, a 16 GB option for a model that didn't have one
21 upvotes · 6 comments
Nemotron 3.5 Bolt 74B (NVIDIA’s 2-bit GGUF) vs Qwen3.8 27B Q4_K_M on a 3090 and a 5090: 2x the tok/s, fewer tasks passed, and the gap is almost all tool calling (480 trials, data included)
r/LocalLLM
•
11d ago
Nemotron 3.5 Bolt 74B (NVIDIA’s 2-bit GGUF) vs Qwen3.8 27B Q4_K_M on a 3090 and a 5090: 2x the tok/s, fewer tasks passed, and the gap is almost all tool calling (480 trials, data included)
21 comments
Nemotron 3.5 Bolt vs Nemo 3.5 Super vs Qwen 3.8 27B/FN
r/LocalLLaMA
•
11d ago
Nemotron 3.5 Bolt vs Nemo 3.5 Super vs Qwen 3.8 27B/FN
21 upvotes · 46 comments
Nemotron 3.5 Bolt is okayish for small multiuser setups
r/LocalLLaMA
•
8d ago
Nemotron 3.5 Bolt is okayish for small multiuser setups
45 upvotes · 31 comments
All NVIDIA Nemotron 3.5 Bolt Unsloth GGUFs are up!
r/unsloth
•
11d ago
All NVIDIA Nemotron 3.5 Bolt Unsloth GGUFs are up!
188 upvotes · 35 comments
NVIDIA releases Nemotron 3.5 Bolt E4B - Runs locally on 6GB RAM.
r/LocalLLM
•
3d ago
NVIDIA releases Nemotron 3.5 Bolt E4B - Runs locally on 6GB RAM.
51 upvotes · 11 comments
Nemotron 3 Nano 4B: A Compact Hybrid Model for Efficient Local AI
r/LocalLLaMA
•
7mo ago
Nemotron 3 Nano 4B: A Compact Hybrid Model for Efficient Local AI
54 upvotes · 9 comments
Nemotron 3.5 Bolt Evaluation using real-world tasks
r/LocalLLaMA
•
10d ago
Nemotron 3.5 Bolt Evaluation using real-world tasks
11 upvotes · 9 comments
nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B model family released (base, NVFP4, BF16, and LiLiCorr speculative decoding)
r/LocalLLaMA
•
12d ago
nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B model family released (base, NVFP4, BF16, and LiLiCorr speculative decoding)
258 upvotes · 73 comments
Nvidia is no longer just selling the shovels. Nemotron 3 Nano Omni is the company’s most aggressive move into AI models.
r/ArtificialInteligence
•
6mo ago
Nvidia is no longer just selling the shovels. Nemotron 3 Nano Omni is the company’s most aggressive move into AI models.
56 upvotes · 19 comments
Nvidia updated the Nemotron Super 3 122B A12B license to remove the rug-pull clauses
r/LocalLLaMA
•
8mo ago
Nvidia updated the Nemotron Super 3 122B A12B license to remove the rug-pull clauses
295 upvotes · 79 comments
Don't sleep on Nemotron 3.5 Super VL
r/LocalLLaMA
•
8d ago
Don't sleep on Nemotron 3.5 Super VL
116 upvotes · 75 comments
Nemotron 3.5 Bolt 74B-A9B, NVIDIA's own IQ2_XXS 24GB GGUF, on an RTX 5090 with llama.cpp b11750 at 32K and 64K context: tok/s with and without the LiLiCorr drafter, VRAM measured, and 33 DevOps tool-use tasks next to 8 open models (Q4) measured the same day
r/LocalLLM
•
7d ago
Nemotron 3.5 Bolt 74B-A9B, NVIDIA's own IQ2_XXS 24GB GGUF, on an RTX 5090 with llama.cpp b11750 at 32K and 64K context: tok/s with and without the LiLiCorr drafter, VRAM measured, and 33 DevOps tool-use tasks next to 8 open models (Q4) measured the same day
5 upvotes · 5 comments
Nemotron - King of the Deep? Comparison of 4 models <=120B
r/LocalLLaMA
•
4mo ago
Nemotron - King of the Deep? Comparison of 4 models <=120B
61 upvotes · 45 comments
nvidia/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-24GB-GGUF results on 16GB VRAM with llama.cpp, strata style tuning (IQ2_XSS Official Nvidia Quant)
r/LocalLLaMA
•
10d ago
nvidia/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-24GB-GGUF results on 16GB VRAM with llama.cpp, strata style tuning (IQ2_XSS Official Nvidia Quant)
7 upvotes · 4 comments
NVIDIA releases 2 models: Nemotron-3.5 Bolt and Super-VL!
r/unsloth
•
12d ago
NVIDIA releases 2 models: Nemotron-3.5 Bolt and Super-VL!
241 upvotes · 63 comments
How to Run NVIDIA Nemotron 3.5 Lightning (Free): 4 Methods from Local GPU to Zero-Code Agent
r/LocalLLaMA
•
3mo ago
How to Run NVIDIA Nemotron 3.5 Lightning (Free): 4 Methods from Local GPU to Zero-Code Agent
6 comments
NVIDIA Nemotron — does anyone actually use it?
r/LocalLLM
•
6mo ago
NVIDIA Nemotron — does anyone actually use it?
49 upvotes · 54 comments
VIEW POST IN
Français
Português (Brasil)
Русский
Tiếng Việt
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
