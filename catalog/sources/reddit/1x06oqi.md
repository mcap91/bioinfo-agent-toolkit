source: https://www.reddit.com/r/LowEndLocalAI/comments/1x06oqi/short_review_local_lm_on_gtx_1060_3_gb_amd_e22000/
captured: 2026-10-27
playwright: 1.64.1
chromium: 156.0.8078.4

Skip to main content
Short review: Local LM on GTX 1060 3 GB • AMD E2-2000 • 8 GB DDR3 : r/LowEndLocalAI
Sign Up
Log In
Expand user menu
Go to LowEndLocalAI
r/LowEndLocalAI
•
19d ago
u/MattV0
Short review: Local LM on GTX 1060 3 GB • AMD E2-2000 • 8 GB DDR3
Benchmark

I guess, this is a real LowEnd station, so I thought I share this here:

Overview of all models with speed test.

This is a pretty old I PC I'm testing out just for fun and honestly, it's somehow fine. I'm running some of the smaller models and they give me between 20 and 30tps. Prefill is between 200 and 600 tps with longer inputs up to 1200.

Of course, the capabilities are far from typical Qwen 27B, butI think it's pretty good for a system with 10-15 year old components.

Using claude I did a simple PI-Benchmark:

Results without thinking (✅ pass with time; ❌ fail; ⏱ hit the 6-min limit; benchmark and tables created by Claude):

Task	Qwen3.5-2B	Granite 4.1 3B	Ministral 3 3B	MiniCPM5-2B	Qwen3.5-4B	NeoHorse-1-4B

fizzbuzz	✅ 217 s	✅ 50 s	✅ 29 s	✅ 108 s	✅ 40 s	✅ 42 s
binsearch-bug	✅ 22 s	✅ 22 s	✅ 32 s	✅ 146 s	✅ 57 s	✅ 112 s
roman	⏱	❌	✅ 27 s	⏱	✅ 52 s	❌
duration	⏱	❌	❌	❌	❌	✅ 264 s
wordfreq-cli	⏱	✅ 47 s	❌	✅ 32 s	✅ 23 s	✅ 110 s
inventory	⏱	❌	✅ 41 s	✅ 38 s	✅ 50 s	✅ 51 s
csv-two-bugs	⏱	❌	✅ 51 s	✅ 31 s	✅ 66 s	✅ 159 s
spiral	✅ 21 s	✅ 60 s	✅ 21 s	✅ 13 s	✅ 21 s	⏱
Score	3/8	4/8	6/8	6/8	7/8	6/8
Total time	~34 min	6 min	5 min	15 min	10 min	24 min

Results with thinking:

Task	MiniCPM5-2B	Qwen3.5-4B	NeoHorse-1-4B	Ministral 3 3B Reasoning

fizzbuzz	✅ 28 s	✅ 55 s	✅ 43 s	❌
binsearch-bug	✅ 38 s	⏱	❌	✅ 29 s
roman	⏱	✅ 227 s	❌	❌
duration	✅ 153 s	❌	❌	❌
wordfreq-cli	✅ 85 s	✅ 69 s	✅ 175 s	✅ 35 s
inventory	✅ 65 s	✅ 73 s	✅ 164 s	❌
csv-two-bugs	⏱	✅ 58 s	❌	❌
spiral	✅ 85 s	✅ 41 s	✅ 56 s	❌
Score	6/8	6/8	4/8	2/8
Total time	19 min	19 min	25 min	7 min

Setup: GTX 1060 3 GB, AMD E2-2000 (2 cores, no AVX), 2×4 GB DDR3-800, llama.cpp (CUDA). All layers on the GPU (-ngl 99, batch 256, q8_0 KV cache); any CPU offload is unusable on this CPU.

The 8 tasks (each starts in an empty folder with a unit-test file; the agent may read, write and run tests until they pass; 6 min limit; tests are restored before grading):

#	Task	What the agent has to do

1	fizzbuzz	Write fizzbuzz(n) from a one-sentence spec
2	binsearch-bug	Find and fix an off-by-one bug in an existing binary search
3	roman	Write to_roman / from_roman for 1–3999 incl. error handling (round-trip tested for all 3999 numbers)
4	duration	Write a parser for "1h30m", "2h5s" … with strict validation (wrong order, duplicates, u
5	wordfreq-cli	Write a command-line tool that prints the top N words of a file (case-insensitive, ties alphabetical)
6	inventory	Extend an existing 3-file package: remove() with 3 error cases + total_value() using
7	csv-two-bugs	Fix a CSV summary function that has two separate bugs (skips a data row, truncates floats)
8	spiral	Write spiral_order(matrix) incl. edge cases (single column, empty)Model	Quant	Size	Gen tok/s	Prefill tok/s (>500 tok)	Context

Qwen3.5-2B	UD-Q5_K_XL	1.5 GB	36.5	1210	128k
MiniCPM5-2B	Q6_K	2.1 GB	34.4	876	16k
Granite 4.1 3B	Q4_K_M	2.1 GB	33.7	615	8k
Ministral 3 3B	UD-Q4_K_XL	2.2 GB	29.4	622	8k
Qwen3-4B-2507	Q4_K_M	2.5 GB	28.8	509	4k
Qwen3.5-4B	IQ4_XS	2.5 GB	26.7	549	16k
Gemma 4 E2B	Q3_K_M	2.5 GB	23.3	746	64k
NeoHorse-1-4B	i1-IQ3_M	2.2 GB	23.3	508	16k

Takeaways:

Qwen3.5-4B (no thinking) solved the most (7/8). Ministral 3 3B is the efficiency winner: 6/8 in 5 minutes.

MiniCPM5-2B reaches 6/8 at only 2B parameters and is one of the fastest models on this card (34 tok/s).

Thinking didn't pay off for these small models in agent use: the same or worse scores at about twice the time. NeoHorse even dropped from 6/8 to 4/8.

Caveat: these are 8 small tasks with one run each, so a difference of one task is noise. Real projects (bigger codebases, vague requirements) would be harder, especially with only 8–16k of context.

Read more
Share
Sort by:
Comments Section
sleekstrike
•
19d ago

I've had excellent results with LFM2.5 2.6B on my 1060 6GB running entirely on GPU with 128k context.

Reply
Share
MattV0
•
19d ago

Thank you, I will check it out.

Reply
Share
bkfliplee
•
19d ago

A model you might be interested in is bartowski/FrogNano-4B-2609-GGUF in my own personal testing it matched qwen3.5-4b at SWE (agentic coding tasks), produced better results with less tokens generated in NoLiMa and MRCRv2 (info retrieval from context, one tests long context, and the other tests trickier contexts). I have yet to try using it in day to day stuff so it just might be good at benchmarks and not real work but I dont see the model mentioned much (admittedly it is newer).

MattV0
•
19d ago

Thanks. I will look into this one tomorrow.

mamonu
•
19d ago

I had good results on a cpu only macmini2012 with not even avx2 (so truly low end!!)
with Ling 3 Tiny q6 . Would be interested to see where Ling3Tiny lies in your benchmarks

MattV0
•
19d ago

Oh great for this recommendation. I'll add it to my tomorrow list.

james_pic
•
19d ago

FYI, Granite 4.2 is the latest version of Granite. Also, I can't see the results for Gemma 4 E2B in the tables.

MattV0
•
19d ago

Oh I totally missed that one. I'll do another round.

Gemma was not that good but I can add this.

Also I guess I should improve the benchmark to be a bit more serious and reliable. Thanks for your input.

james_pic
•
19d ago
•
Edited 19d ago

TBH, there are enough serious benchmarks, and half the models are overfitted to them. A benchmark that more-or-less matches what you do with the model in your use case has value for you and anyone else with the same use case.

3 more replies
MattV0
•
17d ago

Great hint! granite 4.2 is on easy tasks much much better than granite 4.1.

More posts you may like
Related posts
Spent ₹30,000 on an RTX 5060 thinking local LLMs would finally set me free. Reality hit so hard I’m questioning every “just run it locally” post I’ve ever upvoted.
r/LocalLLaMA
•
21d ago
Spent ₹30,000 on an RTX 5060 thinking local LLMs would finally set me free. Reality hit so hard I’m questioning every “just run it locally” post I’ve ever upvoted.
72 comments
3x RTX Pro 6000s + 32GB DDR5 + AMD 9945WX + Etc. = 36K
r/LocalLLM
•
15d ago
3x RTX Pro 6000s + 32GB DDR5 + AMD 9945WX + Etc. = 36K
13 upvotes · 89 comments
If you had ~10k to spend on local LLM hardware right now, what would you actually build?
r/LocalLLM
•
7mo ago
If you had ~10k to spend on local LLM hardware right now, what would you actually build?
24 upvotes · 92 comments
[USA-OR] [H] INwin AM5 Ryzen 5 8600G APU PC, AM5 Mini ITX Bundle, G.Skill Ripjaws 64GB (2x32GB) DDR4-3200 SODIMM, 2.5GbE A+E Key Adapter, Intel i3-9100T + 8GB DDR4 RAM [W] Paypal
r/hardwareswap
•
2mo ago
[USA-OR] [H] INwin AM5 Ryzen 5 8600G APU PC, AM5 Mini ITX Bundle, G.Skill Ripjaws 64GB (2x32GB) DDR4-3200 SODIMM, 2.5GbE A+E Key Adapter, Intel i3-9100T + 8GB DDR4 RAM [W] Paypal
3 comments
Local LLM on a GTX 1080, any suggestions ?
r/AI_Agents
•
2mo ago
Local LLM on a GTX 1080, any suggestions ?
4 upvotes · 6 comments
Just upgraded my local llm hardware
r/LocalLLM
•
6mo ago
Just upgraded my local llm hardware
275 upvotes · 47 comments
Local LLM with RX 9060 16GB?
r/SelfHostedAI
•
3mo ago
Local LLM with RX 9060 16GB?
12 upvotes · 19 comments
The time to buy hardware for local AI is NOW
r/LocalLLM
•
2mo ago
The time to buy hardware for local AI is NOW
67 upvotes · 223 comments
[USA-NJ][H] iPhone 14 Pro 256GB, E16 AMD Gen 2, 2x E16 AMD Gen 3 BNIB, 3060 Ti, DDR4 2x16 3200MHZ SODIMM [W] Verified PayPal, Local Cash
r/hardwareswap
•
3mo ago
[USA-NJ][H] iPhone 14 Pro 256GB, E16 AMD Gen 2, 2x E16 AMD Gen 3 BNIB, 3060 Ti, DDR4 2x16 3200MHZ SODIMM [W] Verified PayPal, Local Cash
2 upvotes · 14 comments
[ selling ][ Brand New ] Gaming PC. AMD Ryzen 7 7800X3D | 32GB Patriot DDR5 6000Mhz | RTX 5070 12GB | 1TB SSD NVME
r/BangaloreMarketplace
•
23d ago
[ selling ][ Brand New ] Gaming PC. AMD Ryzen 7 7800X3D | 32GB Patriot DDR5 6000Mhz | RTX 5070 12GB | 1TB SSD NVME
34 upvotes · 38 comments
[FS][US-TN] Enterprise Server RAM Clearout - 64GB DDR5 4800 RDIMM, 64GB DDR4 2666 LRDIMM, 32GB DDR4 2666 RDIMM (Cisco)
r/homelabsales
•
3mo ago
[FS][US-TN] Enterprise Server RAM Clearout - 64GB DDR5 4800 RDIMM, 64GB DDR4 2666 LRDIMM, 32GB DDR4 2666 RDIMM (Cisco)
28 upvotes · 25 comments
Which is the best local LLM in April 2026 for a 16 GB GPU? I'm looking for an ultimate model for some chat, light coding, and experiments with agent building.
r/LocalLLM
•
7mo ago
Which is the best local LLM in April 2026 for a 16 GB GPU? I'm looking for an ultimate model for some chat, light coding, and experiments with agent building.
87 upvotes · 85 comments
Local LLM performance on AMD Ryzen AI 9 HX 370 iGPU (Radeon 890M) or NPU
r/LocalLLaMA
•
1y ago
Local LLM performance on AMD Ryzen AI 9 HX 370 iGPU (Radeon 890M) or NPU
16 upvotes · 31 comments
Seeking local ai hardware buying advice
r/LocalLLM
•
1mo ago
Seeking local ai hardware buying advice
8 upvotes · 28 comments
[FS] [US-NJ] HP EliteDesk 800 G6 Mini i7 w/ GTX 1060 ti, Intel NUC11PAQ, 64GB (2x32) 5600 DDR5 SODIMM, 64GB (2x32) 3200 DDR4 SODIMM, Gen 4x4 2TB NVME's,
r/homelabsales
•
3mo ago
[FS] [US-NJ] HP EliteDesk 800 G6 Mini i7 w/ GTX 1060 ti, Intel NUC11PAQ, 64GB (2x32) 5600 DDR5 SODIMM, 64GB (2x32) 3200 DDR4 SODIMM, Gen 4x4 2TB NVME's,
4 upvotes · 10 comments
[PC] [USA-AZ] DDR5/DDR4 32/64GB RDIMMs
r/homelabsales
•
1mo ago
[PC] [USA-AZ] DDR5/DDR4 32/64GB RDIMMs
3 upvotes · 3 comments
Best GPU for running local LLMs
r/LocalLLaMA
•
1y ago
Best GPU for running local LLMs
10 upvotes · 57 comments
Local LLM Coding Model Comparison — RTX 3060 (12GB)
r/LocalLLM
•
3mo ago
Local LLM Coding Model Comparison — RTX 3060 (12GB)
15 upvotes · 13 comments
Picked up an AMD Ryzen Max +395 with 128GB
r/LocalLLM
•
4mo ago
Picked up an AMD Ryzen Max +395 with 128GB
53 upvotes · 36 comments
[FS] [USA-OR] G.Skill Ripjaws 64GB (2x32GB) DDR4-3200 SODIMM, 2.5GbE A+E Key Adapter
r/homelabsales
•
2mo ago
[FS] [USA-OR] G.Skill Ripjaws 64GB (2x32GB) DDR4-3200 SODIMM, 2.5GbE A+E Key Adapter
1 upvote · 4 comments
Should I spend $1,000 on an RTX 4060 Ti 16GB PC for local AI, or wait for something better?
r/LocalLLM
•
16d ago
Should I spend $1,000 on an RTX 4060 Ti 16GB PC for local AI, or wait for something better?
2 upvotes · 43 comments
Built a GPU-first local LLM rig… turns out the CPU is why it actually works
r/LocalLLaMA
•
10mo ago
Built a GPU-first local LLM rig… turns out the CPU is why it actually works
1 upvote · 33 comments
Which would be a cost efficient GPU for running local LLMs
r/LocalLLaMA
•
9mo ago
Which would be a cost efficient GPU for running local LLMs
3 upvotes · 44 comments
Guys what’s the best local LLM out there rn for a rtx 2060 6GB vram i58500 and 40gb RAM?
r/LocalLLM
•
6mo ago
Guys what’s the best local LLM out there rn for a rtx 2060 6GB vram i58500 and 40gb RAM?
2 upvotes · 13 comments
[FS] [US-NJ] HP EliteDesk 8 Mini G1i Ultra 7 265T, 32GB (4x8) 3200 DDR4 UDIMM Kit, 64GB (2x32) 5600 DDR5 SODIMM Kit.
r/homelabsales
•
1mo ago
[FS] [US-NJ] HP EliteDesk 8 Mini G1i Ultra 7 265T, 32GB (4x8) 3200 DDR4 UDIMM Kit, 64GB (2x32) 5600 DDR5 SODIMM Kit.
4 upvotes · 6 comments
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
