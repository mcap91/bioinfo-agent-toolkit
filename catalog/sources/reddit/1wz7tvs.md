source: https://www.reddit.com/r/LocalLLaMA/comments/1wz7tvs/i_gave_a_21m_model_a_64bparameter_lookup_table_it/
captured: 2026-10-27
playwright: 1.64.1
chromium: 156.0.8078.4

Skip to main content
I gave a 21M model a 6.4B-parameter lookup table. It matches a 114M dense model and runs with the table on an SSD (RX 9070) : r/LocalLLaMA
Sign Up
Log In
Expand user menu
Go to LocalLLaMA
r/LocalLLaMA
•
20d ago
u/fechyyy
I gave a 21M model a 6.4B-parameter lookup table. It matches a 114M dense model and runs with the table on an SSD (RX 9070)
I Built A Thing

I spent the last few weeks on a hobby research project and just made it public.

The idea isn't new (product-key memory, Lample et al. 2019, and Meta's "Memory Layers at Scale"): give a model a huge table of learned vectors and let it read only a few hundred of them per token. I wanted to know what that's actually worth on a small model, what it costs, and whether the table even has to sit in VRAM.

What came out:

- A 21M model with a 16.8M-row table (6.4B parameters in the table, 33M used per token) is about as good as a 114M dense model trained on the same 500M Wikipedia tokens.

- The table doesn't need VRAM. With the 4-bit table memory-mapped from an NVMe SSD the model still writes ~140 tok/s on my RX 9070, using 0.4 GB of VRAM. Reading long prompts from the SSD is slow though, every missed row costs a whole 4 KB page.

- I wrote Triton kernels for it. They run unchanged on my Radeon, an MI350X and H100/H200.

- Bolting a table onto a finished model (Qwen3.5-0.8B) didn't work: no better than a small dense add-on with the same compute.

Caveats: it's tiny, one seed for the big runs, and the text it writes is fluent Wikipedia English with made-up facts. I wrote down the success criteria before every run, and the stuff that didn't work is in there too.

Most of it ran on my gaming PC, the big runs cost about 70 dollars on Runpod. I built it together with Claude Code (you'll see it in the commits), the ideas, decisions and money were mine.

Repo: https://github.com/re133/sparse-memory-lm

Click a word and see which table entries the model reads: https://re133.github.io/sparse-memory-lm/explorer/

Model: https://huggingface.co/fechyy/sparse-memory-lm-B-16M

Feedback welcome, especially if I got something wrong. And if anyone has bigger GPUs to spare, I'd love to try this at 1B scale.

Read more
Share
Roblox
•
Ad
Show off your skills, outplay tough rivals, and dominate the competitive leaderboards.
Play Now
roblox.com
Collapse video player
Sort by:
Comments Section
Scared-Tip7914
•
20d ago

Cant add anything constructive to this, just wishing you good luck with this project, a gem among the sea of harness posts :D

fechyyy
•
20d ago

Thanks a lot, that means a lot! Took a while to get here, so it's nice to hear it stands out a bit :D

dbenc
•
20d ago
 Top 1% Commenter

what if you used like a 27b model and big honking lookup table

fechyyy
•
20d ago

That's the thing I want to try, but I need a big honking amount of compute haha

dbenc
•
19d ago
 Top 1% Commenter

someone give this person money!

1 more reply
Party_9001
•
20d ago

Presumably they don't have the hardware for that

DataCraftsman
•
19d ago

You really need to pretrain models to do architecture changes like this, so it would require Trillion of tokens of training to work. I tried making a qwen 3.8 27b with the Flash Next PLE table bolted on.

Open-Adhesiveness-86
•
20d ago

the 4KB page cost per missed row is mostly a layout problem, not an SSD one. if you reorder rows so co-activated keys land in the same page (cheap offline clustering on the product-key halves, or just periodic reordering by co-occurrence counts during training), one fault pulls in several useful rows instead of one. also worth checking whether you're actually getting 4KB reads or read-ahead inflating it to 128KB, since mmap faults often trigger readahead. madvise RANDOM on that mapping can change your prefill numbers a lot.

fechyyy
•
20d ago

Good points, thanks! Readahead is already off: the mapping uses MADV_RANDOM, and for misses I issue MADV_WILLNEED on exactly the pages needed. The block stats agree: 128k reads for 571 MiB during prefill, so ~4.5 KB per read, no 128 KB readahead.

The layout part I haven't done, and I think you're right that it's the bigger lever. A 4-bit row is 192 bytes, so 21 rows share a page, but right now they just sit in product-key order. Reordering by co-occurrence should cut the pages per token a lot, mostly for prefill. I'll test it offline on the recorded lookups first.

u/UnstoppableWeb
•
Ad
Still waiting for one coding agent to finish? Run a whole team of Claude and Codex agents in parallel in Unstoppable Code.
Download
app.unstoppable.ai
keepthepace
•
20d ago

Sorry for the dumb question but isn't it the same as engrams?

I do love small models experiments though! Do you know of any community playing with that sort of stuff?

fechyyy
•
20d ago

They're close relatives :D Both put a big lookup table next to the model and read only a few rows per token. The difference is how the rows get picked: Engram hashes the last few input tokens (n-grams), so you know which rows you'll need before the layer even runs and can prefetch them. Product keys pick rows from the hidden state, so you only know once you get there. That's also why reading long prompts from the SSD is harder for my version.

Communities I know: EleutherAI's Discord for the research side, the GPU MODE Discord for kernels, and the nanoGPT speedrun crowd for small-model training tricks. If anyone knows more, I'd love to hear about them.

keepthepace
•
20d ago

I see, thanks! I understand better the problem with the SSD cache missing: you need to get a new read on every layer at every token, that's not especially SSD friendly.

nanoGPT speedrun crowd

Where do you find those? Good to know Eleuther is still around.

sn2006gy
•
20d ago
 Top 1% Commenter

awesome work!

Are you going to try and scale up your experiment?

fechyyy
•
20d ago

Absolutely!!!! I am currently looking for partners with more GPU power to scale it up :D

theone_2099
•
20d ago

How will you mitigate the hallucinations?

fechyyy
•
20d ago

Not yet. B-16M is the first step: 21M parameters plus the table, trained on 500M tokens of Wikipedia, no instruction tuning. At that size it writes fluent Wikipedia-style text and makes up most facts, so hallucinations aren't something this model can fix. This round was about whether the table is worth it at all (perplexity vs. dense models, cost, offloading), and it is.

The goal is a much bigger model with a much bigger table, and that's where it gets interesting for hallucinations. Meta's Memory Layers at Scale paper saw the biggest gains on factual tasks. And a table has one property dense weights don't: knowledge sits in rows you can find, inspect and in principle update one by one. My plan for that stage:

- measure factual recall directly with fact tests, not just perplexity

- see whether wrong facts can be fixed by updating only the rows that get read for them

The honest caveat: when I bolted a table onto a finished Qwen3.5-0.8B, it barely helped with recall (+2.4 points over a dense add-on). So I think the table has to be there from the start of training, and that's what I'd like to test at scale.

Asleep_Document9811
•
20d ago

i just wanted to comment to say that i am a huge fan of there being more ready-made vector embedding databases out there. they are super interesting to experiment with.

8 more replies
remind_me_later
•
20d ago

Below 1B params, hallucinations are effectively a guarantee. There's simply not enough space at that level to fit both the normal training & the anti-hallucination training.

u/Shane_Company
•
Ad
Hey Bay Area! How do we get the prettiest natural & lab-grown diamonds at the best prices? We inspect each one & negotiate the price on your behalf. Visit us in Cupertino, San Mateo, & Walnut Creek.
Shop Now
shaneco.com
Collapse video player
asssuber
•
20d ago

u/fendermoon was working on reproducing ngram findings. I pointed Meta's "Memory layers at Scale" to them and they seemed interested too. Maybe you two can cooperate. It's a very interesting research direction for local AI.

FenderMoon
•
20d ago

Thank for the shoutout! Been a bit of a busy week but I'll take a deeper look into this tomorrow. I'm excited to see.

Funds ran a bit short so I had to take a break on spending thousands of dollars per month in compute. 😂

krystof24
•
20d ago

How much VRAM does this need for training? And what's the memory complexity in relation to model size?

fechyyy
•
20d ago

About 16 bytes per table parameter (fp32 values, a gradient accumulator and Adam's two moments), plus ~4.5 GiB for the small dense model and activations. Measured peaks:

B-1M (0.4B table params): 10.4 GiB

B-4M (1.6B): 28.5 GiB

B-16M (6.4B): 101 GiB

So memory grows linearly with the table, while compute per token barely changes (it always reads 384 rows). For inference you only need the table itself, and that can stay in RAM or on an SSD: B-16M in 4-bit is 3.2 GB.

croqaz
•
19d ago

I love these kinds of small experimental models! Thanks for sharing!

hackint0shh
•
17d ago

You could create a mem drive if you have enough RAM, place the table on there, should speed things up even more.

[deleted]
•
20d ago
People also ask about section
People also ask about
How to create a lookup table
Benefits of lookup tables
Model parameter efficiency
SSD performance optimization
AI model hosting tips
More posts you may like
Related posts
I trained a 1B-parameter LLM from scratch on 20B tokens for about $200
r/LocalLLaMA
•
3mo ago
I trained a 1B-parameter LLM from scratch on 20B tokens for about $200
460 upvotes · 58 comments
AMDOfficial
•
Ad
Build local AI workflows in minutes, not weekends.
amd.com
Learn More
I trained a 1.57B-parameter Dreamer 4 World Model from scratch for under $150
r/LocalLLaMA
•
2mo ago
I trained a 1.57B-parameter Dreamer 4 World Model from scratch for under $150
81 upvotes · 10 comments
I measured the "personality" of 6 open-source LLMs (7B-9B) by probing their hidden states. Here's what I found.
r/LocalLLaMA
•
9mo ago
I measured the "personality" of 6 open-source LLMs (7B-9B) by probing their hidden states. Here's what I found.
218 upvotes · 46 comments
The Best Open-Source 8B-Parameter LLM Built in the USA
r/LocalLLaMA
•
1y ago
The Best Open-Source 8B-Parameter LLM Built in the USA
456 upvotes · 91 comments
Honest question, why are we throwing trillion-parameter models at tasks that barely need a search engine?
r/LocalLLM
•
4mo ago
Honest question, why are we throwing trillion-parameter models at tasks that barely need a search engine?
135 upvotes · 85 comments
I benchmarked 8 local LLMs for phone-to-home chat: the 4B model won. Here's why the larger ones lost
r/LocalLLaMA
•
8mo ago
I benchmarked 8 local LLMs for phone-to-home chat: the 4B model won. Here's why the larger ones lost
5 comments
60-82% accuracy swing on 4B model classification task: the only variable was harness design
r/LocalLLaMA
•
3mo ago
60-82% accuracy swing on 4B model classification task: the only variable was harness design
90 upvotes · 16 comments
Attention Survey July 2026: 23 Model Open Weight 20B-500B Architecture Analysis
r/LocalLLaMA
•
3mo ago
Attention Survey July 2026: 23 Model Open Weight 20B-500B Architecture Analysis
34 upvotes · 10 comments
In your opinion, which LLM in the 6–9B parameter range is the smartest?
r/LocalLLM
•
2mo ago
In your opinion, which LLM in the 6–9B parameter range is the smartest?
18 upvotes · 35 comments
Top 10 AI agents for small local LLMs in 2026, tested on Qwen3.5-4B
r/selfhosted
•
6d ago
Top 10 AI agents for small local LLMs in 2026, tested on Qwen3.5-4B
146 upvotes · 78 comments
Are there any (small, ~10B) models that you would say are a good collaborator?
r/LocalLLaMA
•
2mo ago
Are there any (small, ~10B) models that you would say are a good collaborator?
57 upvotes · 54 comments
Built a healthcare SaaS template in Framer
r/framer
•
2mo ago
Built a healthcare SaaS template in Framer
1 upvote · 3 comments
I tested 14 "decision models" against local LLMs on 56 real triage tasks. Qwen3.5-9B beat every one of them.
r/LocalLLM
•
16d ago
I tested 14 "decision models" against local LLMs on 56 real triage tasks. Qwen3.5-9B beat every one of them.
20 upvotes · 35 comments
Best vision models under 6B?
r/LocalLLaMA
•
2mo ago
Best vision models under 6B?
14 upvotes · 13 comments
All currently popular local models in one table + Opus 4.8 results
r/LocalLLaMA
•
2mo ago
All currently popular local models in one table + Opus 4.8 results
48 upvotes · 33 comments
Thoughts on recent small (under 20B) models
r/LocalLLaMA
•
10mo ago
Thoughts on recent small (under 20B) models
71 upvotes · 25 comments
Best <4B dense models today?
r/LocalLLaMA
•
9mo ago
Best <4B dense models today?
32 upvotes · 36 comments
I tested 12 small LLMs (1B-35B) on a 15-question reasoning test. Here are the results. (Qwen, Ministral, Nemotron, Gemma, Phi, Llama, lfm, GPT-OSS)
r/LocalLLM
•
5mo ago
I tested 12 small LLMs (1B-35B) on a 15-question reasoning test. Here are the results. (Qwen, Ministral, Nemotron, Gemma, Phi, Llama, lfm, GPT-OSS)
93 upvotes · 22 comments
I use a ~322M local model to judge every tool call my coding agents make (about 90 ms on CPU, no API)
r/LLMDevs
•
16d ago
I use a ~322M local model to judge every tool call my coding agents make (about 90 ms on CPU, no API)
37 upvotes · 14 comments
The minimum size of an LLM to generate a little meaningful convo
r/LocalLLaMA
•
2d ago
The minimum size of an LLM to generate a little meaningful convo
44 upvotes · 78 comments
Simple and easy 3DGS importer in Blender - Showcase
r/blender
•
3mo ago
Simple and easy 3DGS importer in Blender - Showcase
25 upvotes · 10 comments
I built version control for financial models and would love feedback.
r/glazeapp
•
3mo ago
I built version control for financial models and would love feedback.
1 upvote
I Build a Personal Detailed Weather Report Skill with Hermes and Qwen3.8-27b
r/hermesagent
•
2mo ago
I Build a Personal Detailed Weather Report Skill with Hermes and Qwen3.8-27b
23 upvotes · 2 comments
Custom waveform and driver package for all SPI eink minimal ghosting 20 fps video
r/eink
•
2mo ago
Custom waveform and driver package for all SPI eink minimal ghosting 20 fps video
3 upvotes · 2 comments
Local LLM model provider
r/homelab
•
5d ago
Local LLM model provider
9 upvotes · 25 comments
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
