source: https://www.reddit.com/r/unsloth/comments/1xdzfnf/for_qwen3635b_lovers_ud_q4_k_xl_now_runs_in/
captured: 2026-10-29
playwright: 1.64.1
chromium: 156.0.8078.4

Skip to main content
For Qwen3.6-35B Lovers, UD_Q4_K_XL now runs in Strata with up to 300 tok/s generation and 7000 tok/s prompt processing - 16GB VRAM (RTX 5080) : r/unsloth
Sign Up
Log In
Expand user menu
Go to unsloth
r/unsloth
•
5d ago
u/yehyakar
For Qwen3.6-35B Lovers, UD_Q4_K_XL now runs in Strata with up to 300 tok/s generation and 7000 tok/s prompt processing - 16GB VRAM (RTX 5080)
Resource

So, after jumping on the Strata train few days ago, it felt obvious that it does some pretty good magic on Flash Next Qwen model but its Qwen3.8-35B performance was less magical (though still better than llamacpp) - so worked over last day to bring any optimization possible for Qwen3.8-35B into Strata.

PRs are raised, but if you want to give it a shot and see benchmarks against llamacpp and vanilla Strata:

https://huggingface.co/ykarout/Strata-Qwen3.6-35B-A3B

Also, I posted about the Sage model released few days ago which is a fine-tune of the Qwen3.6-35B that am testing now and shows some promise so far (though emits much more thinking) - also benefits from inference optimizations - but is quality that much better? not sure yet, still testing, but worth giving a look

https://huggingface.co/ykarout/Strata-Sage-A1.5-GGUF

Share
AMDOfficial
•
Ad
Build local AI workflows in minutes, not weekends.
Learn More
amd.com
Collapse video player
Sort by:
Comments Section
10F1
•
5d ago

Strata needs to give amd some love, it keeps switching to cuda mid decoding.

yehyakar
•
5d ago

I wish I had an AMD card to play around with :(

10F1
•
5d ago

It pre fills fine, then once it tries to generate tokens it switches to cuda and crashes (since I obv don't have cuda)

3 more replies
couperd
•
5d ago

this is great!

Qwen3.6-35B-A3B (MoE, ~3B active) on a single Tesla V100 32GB

Setup: UD-Q4_K_XL MTP GGUF (22.9 GB) · Strata engine q36-r2 (CUDA 12, sm70) · AMD EPYC 7282 (8 vCPU) · 64 GB RAM · all 18.75 GB of experts resident in VRAM · 262K native context · MTP-2 speculative decoding · thinking off, temp 0.6

Workload	Prompt (tok)	Prefill (tok/s)	Decode (tok/s)	MTP acceptance

llama.cpp baseline, same model/quant	~500	~66	109	47%
Agent + tool call	~1.5K	2,713	193	100%
Prose, 1K decode	~1.3K	2,681	149	68%
Long-context QA	14,000	3,126	169	100%
Long-context QA	65,000	1,430	112	85%
Long-context QA	121,000	650	58	74%
Long-context QA	216,306	285	45	74%

Concurrent streams (2 × 65K, --parallel 2): serialized, not batched — the engine runs one resident sequence behind a FIFO. Stream 1: 46.5 s, stream 2: 93.3 s total (each stream at full single-stream speed; total ≈ sum of the two). Single-card throughput is unchanged, you just queue.

Notes:

Decode vs llama.cpp: +37–77%; MTP acceptance 47% → 68–100% (the main win).

Agent traffic (code/tools echoing context) is the best case — near-perfect MTP acceptance.

Prompt read is what collapses with length (3.1K → 285 tok/s at 216K); decode degrades gently (169 → 45).

VRAM peak ~29.6/32 GB at 65K context, 2-stream.

Required a one-line engine patch (missing ev_route event creation on the all-experts-in-VRAM path) — unpatched q36-r2 crashes on first prompt on any ≥32 GB card.

yehyakar
•
5d ago

amazing! glad it helps also on sm70 .. ill look up the patch u mentioned and fix it. thanks for the feedback. if u ask ur agent to profile an inference run using nvidia nsight and detect any bottlenecks, im sure it can push ur numbers even further with minor tuning. give it a try

couperd
•
4d ago

setting '--draft-vocab 16384` measured +4-12% decode

1 more reply
yehyakar
•
5d ago

ev_route issue fixed. thanks buddy

2 more replies
sirloindenial
•
5d ago

So this is the expert profiles? Can you do for other models or is this compatible with other fine tunes based on 3.6 35b? Or is it required to have different one for them?

yehyakar
•
5d ago

experts profile is one tuning which lends 1-5% performance boost, the others are kernels, memory optimizations, cpu/gpu resource optimizations which do more of the heavy lifting. The expert profiles can be used with other models (I tested with expert profile from qwen itself and from sage which is a fine-tune of it, both gave almost same results - so it should work with any fine-tune of the base model.) So you can basically load other fine-tunes but one thing I noticed is that for some layers, strata by default enforces specific layers to be quantized at specific levels so for example the UD Q8_K_XL couldn't run by default, I had to quantize some layers of it (very few) using llama-quantize to layers that strata accepts but this is straightforward, if the fine-tuned model failed to load just point ur agent at it, it will look which layer needs fixing and can quantize/dequantize it with llamacpp llama-quantize in no time, and it will work.

leonbollerup
•
5d ago

i have Ocammy running at a 5090M with aroune 360 tok/sek and 8700 in prefill :)

Edit: sorry, that was on ninfer

yehyakar
•
5d ago

share the inference engine gh repo. and a 5090 :) 😜

SaltGrilledSalmon
•
5d ago

How's occamy for practical use cases? I feel like this model gets less attention than it deserves... What do you use it for?

yehyakar
•
5d ago

ah its a model. will look it up

2 more replies
u/goabacuscorp
•
Ad
On-Prem AI with Unlimited Token Usage. One Fixed Price.
Learn More
go.ai
Electrical-Loan-4156
•
5d ago

that's a wild jump from the earlier numbers, 300 tok/s on a 35B model with just 16GB is nuts

stackfullofdreams
•
5d ago

Well hot damn, never been so excited to go back a generation on a model

Biazzaaa
•
5d ago

At c1?

yehyakar
•
5d ago

c1 means?

2 more replies
Spuk1
•
4d ago

I only have 11gb vram with 32gb ddr5 do you think id be able to run this at decent speed?

yehyakar
•
4d ago

yes

3 more replies
dzedaj
•
4d ago

would that also work with Ornith-1.5-35B-A3B ?

yehyakar
•
4d ago

in general yes but some quants keep layers in precisions that are not supported out of the box. the repo has the details on how to check and work around it

ea_man
•
5d ago

A3B is still very good when you have to ingest a lot of logs and generate a summary table :)

No_Total_423
•
5d ago

Any benchmark vs PolyStrata?

yehyakar
•
5d ago

sadly no - i haven't checked polystrata yet - im playing around with basalt now. will check it out soon

2 more replies
Dropqt
•
5d ago

Very promising results on better gpus, I'm more curious about 2x 3070 rtx setups with high amount of ram, how does it do? Anyone here tried benchmarking that setup? Or any online resources where i could see and compare?

People also ask about section
People also ask about
UD_Q4_K_XL performance
Strata framework benefits
300 tok/s generation speed
7000 tok/s prompt processing
Qwen3.6-35B model usage
More posts you may like
Related posts
Strata now supports Qwen 3.6 35B
r/LocalLLaMA
•
5d ago
Strata now supports Qwen 3.6 35B
127 upvotes · 51 comments
volvocarusa
•
Ad
The Volvo EX90 designed to help keep every passenger safe.
volvocars.com
Learn More
For Qwen3.6-35B Lovers, UD_Q4_K_XL now runs in Strata with up to 300 tok/s generation and 7000 tok/s prompt processing - 16GB VRAM (RTX 5080)
r/Qwen_AI
•
5d ago
For Qwen3.6-35B Lovers, UD_Q4_K_XL now runs in Strata with up to 300 tok/s generation and 7000 tok/s prompt processing - 16GB VRAM (RTX 5080)
75 upvotes · 22 comments
Qwen3.8-27B UD-Q2_K_XL is usable at 9.8 GB — the smallest file that still behaves like the 4-bit one, but here's the catch.
r/LocalLLM
•
2mo ago
Qwen3.8-27B UD-Q2_K_XL is usable at 9.8 GB — the smallest file that still behaves like the 4-bit one, but here's the catch.
22 upvotes · 22 comments
Strata with Qwen3.8 Flash Next UD-Q4_K_XL
r/LocalLLaMA
•
19d ago
Strata with Qwen3.8 Flash Next UD-Q4_K_XL
28 upvotes · 69 comments
Qwen3.8-27B at ~100 tok/s on a single 7900 XTX (patched hipfire)
r/ROCm
•
5d ago
Qwen3.8-27B at ~100 tok/s on a single 7900 XTX (patched hipfire)
95 upvotes · 52 comments
Spoiler - filming
r/tsitp
•
5mo ago
Spoiler
Spoiler - filming
174 upvotes · 167 comments
Qwen 3.6 27B 30GB Same top p: 98.358 ± 0.033 % vs UD Q8 K XL 33GB Same top p: 97.426 ± 0.041 %
r/LocalLLaMA
•
5mo ago
Qwen 3.6 27B 30GB Same top p: 98.358 ± 0.033 % vs UD Q8 K XL 33GB Same top p: 97.426 ± 0.041 %
29 upvotes · 28 comments
Request: unsloth Please re-quantize Qwen3.6 35 A3B and 27B using UD 3.0
r/LocalLLaMA
•
2mo ago
Request: unsloth Please re-quantize Qwen3.6 35 A3B and 27B using UD 3.0
183 upvotes · 37 comments
I removed 10 layers from Qwen3.6-35B-A3B, healed it, and got a 12GB version running at ~44 tok/s on a Radeon 890M
r/LocalLLM
•
2mo ago
I removed 10 layers from Qwen3.6-35B-A3B, healed it, and got a 12GB version running at ~44 tok/s on a Radeon 890M
13 upvotes · 21 comments
Qwen3.8-Flash-Next UD-IQ4_XS (~94GB) on RTX 5090 Laptop + 128GB RAM — Strata 0.1.41 — 52.6 tok/s, 84.8% Expert Cache Hit
r/Qwen_AI
•
20d ago
Qwen3.8-Flash-Next UD-IQ4_XS (~94GB) on RTX 5090 Laptop + 128GB RAM — Strata 0.1.41 — 52.6 tok/s, 84.8% Expert Cache Hit
2 upvotes · 31 comments
Great results with Qwen3.6-35B-A3B-UD-Q5_K_XL + VS Code and Copilot
r/LocalLLaMA
•
6mo ago
Great results with Qwen3.6-35B-A3B-UD-Q5_K_XL + VS Code and Copilot
49 upvotes · 20 comments
Qwen3.6-35B-A3B UD-Q4_K_XL pp 1250t/s en rtx 3060
r/Qwen_AI
•
2mo ago
Qwen3.6-35B-A3B UD-Q4_K_XL pp 1250t/s en rtx 3060
36 upvotes · 31 comments
Open Source Kernel in Qwen3.6-35B-A3B for AMD MI350X: 78,498 output tok/s on 8 GPUs
r/LocalLLaMA
•
2mo ago
Open Source Kernel in Qwen3.6-35B-A3B for AMD MI350X: 78,498 output tok/s on 8 GPUs
58 upvotes · 22 comments
In The Prestige (2007), deaths parallel each other...(Major spoilers in images)
r/MovieDetails
•
4y ago
Spoiler
In The Prestige (2007), deaths parallel each other...(Major spoilers in images)
12K upvotes · 545 comments
Qwen 3.6 35B appreciation post
r/LocalLLaMA
•
20d ago
Qwen 3.6 35B appreciation post
85 upvotes · 47 comments
GMO Grape Ape
r/ukmedicalcannabis
•
5mo ago
GMO Grape Ape
15 upvotes · 24 comments
Strata with Qwen3.8 Flash Next UD-Q4_K_XL
r/LocalLLM
•
19d ago
Strata with Qwen3.8 Flash Next UD-Q4_K_XL
15 upvotes · 13 comments
Strata with Qwen3.8 Flash Next UD-Q4_K_XL
r/Qwen_AI
•
19d ago
Strata with Qwen3.8 Flash Next UD-Q4_K_XL
52 upvotes · 49 comments
Running unsloth/Qwen3.8-27B-UD-IQ4_XS 262k q4_0 KV + vision on 16GB VRAM @ 80t/s and 1500pp
r/LocalLLM
•
16d ago
Running unsloth/Qwen3.8-27B-UD-IQ4_XS 262k q4_0 KV + vision on 16GB VRAM @ 80t/s and 1500pp
61 upvotes · 24 comments
I have an ESC4000 G3 with 8x T4s in it - what is the fastest way I can deploy Qwen3.5-9B for about 10-15 users concurrently: currently using llama.cpp
r/LocalLLaMA
•
19d ago
I have an ESC4000 G3 with 8x T4s in it - what is the fastest way I can deploy Qwen3.5-9B for about 10-15 users concurrently: currently using llama.cpp
9 upvotes · 16 comments
Qwen3.8-Flash-Next Gufo peaks at 1,601 t/s prefill and 75.4 t/s MTP decode, still 1,405 / 72.6 t/s at 256K (Bosgame M5 - Windows 11)
r/StrixHalo
•
8d ago
Qwen3.8-Flash-Next Gufo peaks at 1,601 t/s prefill and 75.4 t/s MTP decode, still 1,405 / 72.6 t/s at 256K (Bosgame M5 - Windows 11)
22 upvotes · 34 comments
just wanted to share my latest sims ╰(*°▽°*)╯
r/thesims
•
7mo ago
just wanted to share my latest sims ╰(*°▽°*)╯
9 upvotes · 11 comments
Qwen 3.8 27B UD-IQ4_XS even faster on 16GB CUDA
r/LocalLLaMA
•
2mo ago
Qwen 3.8 27B UD-IQ4_XS even faster on 16GB CUDA
32 upvotes · 11 comments
Running unsloth/Qwen3.8-27B-UD-IQ4_XS 262k q4_0 KV + vision on 16GB VRAM @ 80t/s and 1500pp
r/LocalLLaMA
•
16d ago
Running unsloth/Qwen3.8-27B-UD-IQ4_XS 262k q4_0 KV + vision on 16GB VRAM @ 80t/s and 1500pp
35 upvotes · 43 comments
[16GB VRAM] Qwen 3.6 35BA3B - Unsloth's UD IQ4_XS - Great results
r/LocalLLM
•
6mo ago
[16GB VRAM] Qwen 3.6 35BA3B - Unsloth's UD IQ4_XS - Great results
42 upvotes · 17 comments
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
