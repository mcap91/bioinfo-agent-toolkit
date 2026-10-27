source: https://www.reddit.com/r/LocalLLM/comments/1x22inc/polystrata_strata_with_four_more_moe_models/
captured: 2026-10-27
playwright: 1.64.1
chromium: 156.0.8078.4

Skip to main content
PolyStrata: Strata with four more MoE models. Qwen3.6-35B-A3B at 73-75 tok/s on a laptop with an 8 GB card : r/LocalLLM
Sign Up
Log In
Expand user menu
Go to LocalLLM
r/LocalLLM
•
17d ago
u/Responsible_Froyo252
PolyStrata: Strata with four more MoE models. Qwen3.6-35B-A3B at 73-75 tok/s on a laptop with an 8 GB card
Project

I have been adding models to Strata, the engine that runs Qwen3.8-Flash-Next on consumer cards, and put the result in its own repository:

GitHub: https://github.com/VecSzn/PolyStrata

Edit: AMD support is in now, as a beta. iMilnb on GitHub ported the engine to HIP and it went into 0.1.42-poly.4. Linux only for now, there's no ready-made AMD engine for Windows yet. He ran it on an RX 7600 8 GB: Qwen3.6 UD-Q2_K_XL writes 64 tok/s, Ornith Mini 35 tok/s. Same install, ./setup.sh --family qwen36, it builds the engine for your card. Gemma 4, Tiel Coder and GLM haven't been tried on a Radeon yet, so if you run one of those I'd like to hear how it goes.

Update, Oct 11 (v0.1.42-poly.1):

Windows no longer needs Visual Studio or the CUDA toolkit. The release has a ready-made strata-poly (CUDA 13, RTX 20 to RTX 50) and the installer downloads it.

Faster on the same two machines. New numbers, same cells as the table below (short chat / after a ~31K prompt / reads):

Model |Laptop: RTX 4070 8 GB |Workstation: RTX 5090
Qwen3.6-35B-A3B UD-Q3_K_M |84-87 / 70-73 / 1,495-1,620 |385-393 / 241-246 / 6,350-6,552
Qwen3.6-35B-A3B UD-Q4_K_M |79-86 / 70-72 / 1,564-1,572 |328-393 / 243-255 / 6,231-6,577
Gemma 4 26B-A4B UD-Q3_K_M |85 / 58-60 / 2,095-2,098 |326-349 / 254-261 / 7,880-8,230
Gemma 4 26B-A4B UD-Q4_K_M |74-75 / 59 / 2,010-2,011 |316-338 / 232-238 / 7,039-8,055
Ornith 1.5 APEX-I-Compact |72-76 / 66-68 / 1,538-1,539 |303-315 / 218-226 / 6,083-6,360
Ornith 1.5 APEX-I-Quality (4-6 bit) |59-63 / 58-59 / 940-1,510 |289-298 / 203-204 / 6,040-6,392
GLM 5.3 Flash 3.0bit |does not fit in 32 GB of RAM |59-66 / 62-64 / 820-824 The Q4 sizes take 27-31 GB of RAM beside the 8 GB card, close to the laptop's 32 GB. In the 940 run part of Ornith's file came from the disk again.

Qwen3.6 on a card that can't hold all its experts now skips a few low-ranked ones, as Strata 0.1.42 does: about 9% faster on the laptop, and the answers move a little. STRATA_ROUTE_TAIL_SKIP=0 turns it off. The laptop numbers above are with it off.

Claude Code works against the local server. The README has a 30-second real-time clip of a Claude Code task on the laptop.

Strata 0.1.42 is merged in.

The title's number is from the first version; Reddit doesn't let me edit titles.

￼Strata's own engine is in it unchanged. Beside it there is a second engine for four more mixture-of-experts models, each read from its ordinary GGUF:

GLM 5.3 Flash (79 to 114 GB files, most of it stays in RAM)

Qwen3.6-35B-A3B

Ornith 1.5

Gemma 4 26B-A4B

The last three read pictures too.

What I measured. Each cell is: writes in a short chat / writes after a prompt of about 31,000 tokens (29,000 for GLM) / reads that prompt, all in tokens per second.

Model |Laptop: RTX 4070 8 GB, i7-14700HX, 32 GB RAM |Workstation: RTX 5090 32 GB, 120 GB RAM
Qwen3.6-35B-A3B UD-Q3_K_M |70-72 / 60-62 / 1,390 |332-334 / 186-189 / 5,520-5,580
Gemma 4 26B-A4B UD-Q3_K_M |70-71 / 51-53 / 1,907 |306 / 198-200 / 7,170-7,210
Ornith 1.5 APEX-I-Compact |70 / 59 / 1,340 |267-272 / 145-149 / 5,700-5,890
GLM 5.3 Flash 3.0bit |does not fit in 32 GB of RAM |57-59 / 54-57 / 784 (llama.cpp on the same PC: 26 writing, about 265 reading) How it works, briefly. The card holds the experts an answer uses most and the CPU computes the others straight from the mapped GGUF, so the model does not have to fit in VRAM. While an answer is written the cache follows it. The engine also guesses a few tokens ahead, from the model's own draft block or from a repeat of the conversation, and checks the guesses in one pass. With every expert on the CPU the answer is the same tokens with and without guessing, and without guessing the first 64 tokens are compared with llama.cpp on the same file.

It has a one-click installer for Windows and Linux, a web app, and an OpenAI- and Anthropic-compatible API on localhost.

Limits, so nobody wastes an evening: the four added models are experimental and need one NVIDIA card. They were measured on those two machines only. On Windows the installer compiles the engine, which needs Visual Studio's build tools and the CUDA toolkit (it offers to install them). AMD cards and several cards work for Qwen3.8-Flash-Next only.

Most of the code is the Strata project's. If you try it on other hardware I would like to hear the numbers, good or bad.

Repo: https://github.com/VecSzn/PolyStrata

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
chimpera
•
17d ago

I was hopping someone would do this. Have you looked at strata-nvfp4? Something like that would help with GLM flash. Thanks

Responsible_Froyo252
•
17d ago

Yeah, I took a look at the project and I do think NVFP4 is a cool idea, but for GLM the problem is mostly about the size. NVFP4 is 4 bits, so the model ends up at around 204GB which basically doesn't fit in RAM. The same person actually tried it with their other project (strata-glm) and the size really doesn't fit and they had to put experts on NVMe.

Sure_Leave9338
•
17d ago

I really can't get the reason to use Q3 or Q2 on smaller models. I can understand on a big model like GLM 5.3 Flash or qwen Flash Next, but can't understand why lobotomizing smaller models that already are less capable on theirself.

Responsible_Froyo252
•
17d ago

Q4_K_M is in there too for all 3 of the smaller models, you can pick it in the installer. Q3 is just the default because on an 8GB card more of the experts fit in VRAM so it's faster, and the file is easier on 32GB of RAM. On the 5090 it basically doesn't matter, Q4_K_M writes at 333-337 tok/s vs 332-334 for Q3. So if you have the memory just use Q4

3 more replies
Inchmine
•
17d ago

Can I use any glm 5.3 flash with it?

Responsible_Froyo252
•
17d ago

The installer offers three files: neuralll's 3.0bit (114 GB), Unsloth's UD-IQ2_XXS (102 GB) and patrickbdevaney's REAP50-Q3_K_M (79 GB, half of the routed experts removed). Those three are the ones that were run.

Other GGUFs of the model should load if they come from the same converters (neuralll's llama.cpp fork, Unsloth, patrickbdevaney, antirez), but I have not run them, so no promises. If you already have a file: ./setup.sh --family glm --gguf-dir /folder/with/the/file

1 more reply
Sensitive_Song4219
•
16d ago

Holy smoke nice job.

Confirmed this also works with Tiel Coder 35B-A3B (not officially in your list but similar architecture to the supported ones so figured I'd give it a try). Ornith was my previous daily driver (it's awesome) but Tiel is a bit smarter in my use-case and has been thinking-loop-free in the few weeks I've used it.

PolyStrata works perfectly with Tiel!

32GB DDR5 RAM; 8GB VRAM (RTX 5060 Mobile); Core Ultra 9 275HX CPU.

TG seems to have had a reasonable increase on my hardware, maybe 20%? On its own that's already worth it...

BUT PROMPT PROCESSING IS >4X AS FAST. That's... just... nuts. 1000 - 1500 tps pp (!) - up from around 200-350.

The slowest I measured on a large read:

And during an auto-compact that figure often climbs to >1400 tps.

Frankly, this transforms working with existing large codebases (where large reads are often unavoidable) and also turns context-compaction from a slog into something that's far more manageable.

Also the initial-prompt-process of larger harnesses (like OpenCode with its tooling) and/or agent-md files are non-events with this kind of speed.

Like Strata itself this likely opens the door to a lot of hardware that may have otherwise seemed infeasible.

Yours' and the Strata team's work is amazing; thank you.

Responsible_Froyo252
•
16d ago

Oh nice, didn't know Tiel Coder works. It's the same qwen35moe arch as Qwen3.6 so the engine just takes it. thanks for testing it on the 5060 and posting real numbers, prompt reading is where we gained the most so good to see it hold up at 140k

7 more replies
Kiseido
•
17d ago
•
Edited 17d ago

The glm 5.3 flash sounds mighty interesting, though I am a Radeon owner so... lol

Responsible_Froyo252
•
17d ago

Not yet, sorry. The current engine that runs GLM 5.3 Flash only supports CUDA rn, so it needs an NVIDIA card. On a Radeon the same repo still runs Qwen3.8-Flash-Next (12 GB or more), through Strata's AMD backend.

1 more reply
3 more replies
Alternative-Panic69
•
16d ago

Great work...

Got Ornith 1.5 Quality (35B-A3B MoE) Running at 85 tok/s and 200K Context on a 20GB 7900 XT + 32GB DDR4 RAM

Needed to do a few optimizations and remove hardcoded stuff in the backend to make it work.

Ported to Linux ROCm/HIP (gfx1100): Upstream was Windows/CUDA-only; built via Ninja/CMake for AMD RDNA3 with hipBLAS/rocBLAS.

Added Native INT8 KV Cache: Upstream only had FP16. At 200K tokens, FP16 KV took 9 GB VRAM. Our INT8 implementation with FP16 scales cut this to 4.5 GB, freeing 4.5 GB of VRAM to pin hundreds more experts.

Killed the Windows Eviction Watchdog (mind_vram()): Upstream had an auto-resizing watchdog meant for 8 GB Windows laptops. On ROCm, HIP kernel graph instantiations take ~390 MB of driver RAM, tripping the watchdog (free < reserve / 4). It panicked and dumped 990 experts into system RAM. Patched Engine::mind_vram() in engine.cpp:605-612 to return false;—locking all loaded experts pinned permanently.

Eradicated Swap Thrashing: Eliminated 12.3 GB of Linux swap bloat down to ~145 MB peak.

Config Tuning:

• --max-context 200000 (200K token ceiling)

• --kv int8

• --vram-reserve-mib 512 (maximizes resident expert space)

• --threads 4 (CPU cores for un-cached experts; zero GPU thread contention, as I have only 6 physical threads, on Ryzen 5500)

• --expert-swaps 16 (concurrent async PCIe DMA queues)

• --conversation-cache-mib 8192 + --conversation-cache-min-free-mib 2560 (8 GB RAM prefix cache with 2.5 GB free RAM floor)

Context Window: Up to 200,000 tokens active.

Additional details:

• VRAM Usage: 19.76 / 19.98 GB committed (98.88% utilization) rock-solid (0 evictions).

• Resident Experts: 7,458 of 10,496 experts (71.1%) pinned directly in VRAM.

• Short Decode: 84.6 tok/s.

• Medium Decode: 75.4 tok/s.

• Deep Context Decode (107,000+ tokens in context): 35.4 – 36.5 tok/s.

• MTP Speculative Acceptance: 84% – 93%.

• Prefix Cache Hit Rate: >50,000 tok/s (restores 108k tokens in 2.0 s from RAM).

• Cold Prefill: 200– 2000 tok/s (sometimes limited by sequential GDN loop and PCIe streaming).

Trying to optimize even more for my specific setup

Responsible_Froyo252
•
16d ago
•
Edited 16d ago

Thanks, this is really cool. I don’t have an AMD card, so a ROCm port is something I can’t do myself. Would you be up for opening a PR with it? Even as an experimental build it would help a lot of people on Radeon cards. The INT8 KV cache would be welcome as a PR too, ideally as its own PR so it can go in separately. I’ll measure how much it moves the output on our models before deciding whether it should be the default.

One note on mind_vram(): it gives VRAM back when free memory drops below a quarter of the reserve, because on 8 GB cards the CUDA graphs grow by about 200 MB over a long session. On HIP the graphs seem to take more (your 390 MB), so a bigger --vram-reserve-mib, say 1024, should keep the experts pinned without turning the check off.

v0.1.42-poly.1 just went out, so PRs on top of current main would be easiest to merge.

1 more reply
Ambitious_Ad9308
•
14d ago

Honestly, this might be one of the best real-world examples of why developers shouldn't depend solely on GitHub.
PolyStrata is a fantastic fork, and if I hadn't already cloned it locally I would have lost access overnight.
Glad you were able to move everything to Hugging Face. That's a survival trick I'm definitely adding to my own projects going forward.

Responsible_Froyo252
•
12d ago

Thank you! Both my account and the repo is back now.

u/BandaiNamcoMobile
•
Ad
Rival? Captain? Lieutenant? Build YOUR team, and carve your future, in BLEACH Mirrors High. Pre-register now!
bleach-mh-ww.go.link
Learn More
Jealous-Sink-9400
•
17d ago
former_farmer
•
17d ago

Can this actually do any meaningful work?

Responsible_Froyo252
•
17d ago

It's the same model output as llama.cpp on the same file, so it's as good as the model is. Qwen3.6-35B-A3B is decent for coding and normal chat stuff, and GLM 5.3 Flash is a lot stronger if you have the RAM for it (60-96GB next to a 32GB card). There's an OpenAI and Anthropic compatible API so you can plug either into a coding agent. What kind of work did you have in mind?

2 more replies
borobinimbaba
•
17d ago

It would be awesome if you could also include an estimate of how much context each quantization on different hardwares would give us.

Responsible_Froyo252
•
17d ago

Good idea, that's not in the docs yet. Context is pretty cheap on these models since most layers are linear or sliding window attention, it's about 0.7GB of VRAM per 32k tokens at fp16, and it comes out of the expert cache so it costs a bit of speed. I'll add a proper table to the README afterwards.

Vamsi-Thopu
•
16d ago

I have 16gb VRAM and 16gb ram(rx 6800 and ddr5 ram). What would you recommend me?

Responsible_Froyo252
•
16d ago

Right now PolyStrata isn’t a great fit for that setup. The four models I added only run on NVIDIA for now, and Qwen3.8-Flash-Next, which does run on the RX 6800, needs 32GB+ of RAM.

With 16GB of VRAM I’d use llama.cpp or LM Studio (Vulkan or ROCm) and pick something that fits on the card, like Gemma 4 26B-A4B UD-Q3_K_M (12.7GB) or Qwen3.6-35B-A3B UD-Q2_K_XL (12.6GB).

Someone already has a ROCm port of the new engine running, so AMD support for the other models might not be far off.

u/squarespace
•
Ad
Squarespace cuts out the setup so you can get to the part that matters.
Sign Up
squarespace.com
Collapse video player
fedorzh
•
17d ago

Is it possible to run qwen 3.6 using 6gb of VRAM?

Responsible_Froyo252
•
17d ago

Probably not, because around 6GB is already taken before any expert even goes on the card (thats with 32k context). it might fit if you lower the context but I haven't tried that so I can't promise.

4 more replies
Old-Juggernut-101
•
17d ago

Do the smaller models- 26b and 35b work on radeon gpu?

1 more reply
People also ask about section
People also ask about
Best AI models for Strata
Comparison of Strata models and performance
Tips for running Strata on Windows
Performance of Qwen3.8 with Strata
Strata compatibility with 8GB graphics cards
More posts you may like
Related posts
Qwen3.8-Flash-Next on Strata
r/LocalLLaMA
•
21d ago
Qwen3.8-Flash-Next on Strata
181 upvotes · 88 comments
Sephora
•
Ad
TLDR: get beauty from people who get beauty, only at Sephora.
sephora.com
Shop Now
Strata takes the promise of "MoE models just need a total amount of VRAM+RAM" and makes it a reality
r/LocalLLM
•
23d ago
Strata takes the promise of "MoE models just need a total amount of VRAM+RAM" and makes it a reality
157 upvotes · 143 comments
Qwen3.8 flash next w/Strata Performance on a few different configurations of budget rig
r/LocalLLM
•
5d ago
Qwen3.8 flash next w/Strata Performance on a few different configurations of budget rig
58 upvotes · 17 comments
Strata now supports Qwen 3.6 35B
r/LocalLLaMA
•
3d ago
Strata now supports Qwen 3.6 35B
121 upvotes · 51 comments
Benchmarked some Strata Qwen3.8-flash-next quants
r/LocalLLM
•
17d ago
Benchmarked some Strata Qwen3.8-flash-next quants
108 upvotes · 67 comments
Strata is seriously impressive, running Qwen 3.8 Flash Next on hermes at 512k context.
r/LocalLLM
•
24d ago
Strata is seriously impressive, running Qwen 3.8 Flash Next on hermes at 512k context.
251 upvotes · 154 comments
I'm not sure what's causing my little guy to get wrinkly :(
r/succulents
•
5y ago
I'm not sure what's causing my little guy to get wrinkly :(
561 upvotes · 85 comments
Strata: Qwen3.8-FN IQ3_S on a rtx 3070 - 1000pp - 40tps decode
r/LocalLLaMA
•
3d ago
Strata: Qwen3.8-FN IQ3_S on a rtx 3070 - 1000pp - 40tps decode
14 upvotes · 10 comments
Strata is amazing!
r/LocalLLM
•
25d ago
Strata is amazing!
14 upvotes · 17 comments
Ride or Die
r/AmazonPrimeVideo
•
3mo ago
Ride or Die
703 upvotes · 400 comments
Do not upgrade Strata! Tons of breaking changes!
r/LocalLLaMA
•
7d ago
Do not upgrade Strata! Tons of breaking changes!
222 upvotes · 152 comments
What did you think of Dawn releasing Ambipom?
r/pokemonanime
•
4mo ago
What did you think of Dawn releasing Ambipom?
16 upvotes · 37 comments
Strata on M5 Ultra 96GB Actualy Amazing on Qwen3.8 Flash next
r/LocalLLM
•
8d ago
Strata on M5 Ultra 96GB Actualy Amazing on Qwen3.8 Flash next
10 upvotes · 6 comments
PolyStrata (qwen3.6-35b-a3b-ud-q4_k_m) + Cline demo
r/LocalLLaMA
•
11d ago
PolyStrata (qwen3.6-35b-a3b-ud-q4_k_m) + Cline demo
9 upvotes · 7 comments
What products do you use to grow/maintain lashes?
r/AsianBeauty
•
7mo ago
What products do you use to grow/maintain lashes?
268 upvotes · 194 comments
My 3-year art improvement
r/drawing
•
6y ago
My 3-year art improvement
7.2K upvotes · 57 comments
Now that Strata is making MoE more popular, how much does budget vs expensive CPU matter?
r/LocalLLM
•
16d ago
Now that Strata is making MoE more popular, how much does budget vs expensive CPU matter?
16 comments
Please help me pick
r/Sephora
•
2y ago
Please help me pick
59 upvotes · 62 comments
Strata next flash, my findings
r/LocalLLM
•
18d ago
Strata next flash, my findings
26 upvotes · 84 comments
Strata - Qwen 3.8 Flash Next Getting Insane Speeds on 2x RTX 4090 (6553 pp, 271 t/s single stream)
r/LocalLLM
•
5d ago
Strata - Qwen 3.8 Flash Next Getting Insane Speeds on 2x RTX 4090 (6553 pp, 271 t/s single stream)
5 upvotes · 50 comments
Strata with Qwen3.8 Flash Next UD-Q4_K_XL
r/LocalLLaMA
•
17d ago
Strata with Qwen3.8 Flash Next UD-Q4_K_XL
28 upvotes · 68 comments
Strata 0.1.44.1 - Qwen3.8 IQ3_XXS - Tesla P40 + GTX 1080 + 48GB RAM
r/LocalLLM
•
13d ago
Strata 0.1.44.1 - Qwen3.8 IQ3_XXS - Tesla P40 + GTX 1080 + 48GB RAM
7 upvotes · 14 comments
As an experiment I painted up my Tzeentch Daemons Start Collecting box using only inks instead of paints! Pretty happy with the result
r/Warhammer40k
•
4y ago
As an experiment I painted up my Tzeentch Daemons Start Collecting box using only inks instead of paints! Pretty happy with the result
1K upvotes · 28 comments
Strata users, what hardware, model and context are we all using?
r/LocalLLM
•
19d ago
Strata users, what hardware, model and context are we all using?
70 comments
Show and tell: PolyStrata on my $20 Xeon server
r/LocalLLaMA
•
1d ago
Show and tell: PolyStrata on my $20 Xeon server
101 upvotes · 39 comments
VIEW POST IN
Français
Português (Brasil)
简体中文
繁體中文
Русский
日本語
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
